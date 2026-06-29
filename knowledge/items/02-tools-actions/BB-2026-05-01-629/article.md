# We Built a Routing Layer to Cut Our AI Costs. It Broke the Product.

- BestBlogs URL: https://www.bestblogs.dev/article/a676552d
- Original publisher URL: https://towardsdatascience.com/we-built-a-routing-layer-to-cut-our-ai-costs-it-broke-the-product/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-27 23:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 26161

---

A team I was working with cut their AI inference bill by more than half last quarter. Eight weeks of clean engineering work. It was the win the engineering team had been chasing all year. It was also the wrong optimization. Three months later, customer satisfaction was dropping, churn was ticking up, and the cost savings were structurally tied to the quality loss. We had not won. We had just moved the cost somewhere we were not measuring.

  This is the pattern I expect to see across production AI deployments over the next six months. The 2026 conversation around AI economics has produced a consensus playbook. Route simple queries to cheap models. Keep expensive queries on capable models. Cut the bill, keep the quality. Every CFO has seen the math. Every engineering team has built it or is building it.

  The math is real. The Pareto trap is also real.

  The piece below is what I told the team after we ran the post-mortem. It describes the architecture they built, the failure mode they walked into, the detection methodology that would have caught it earlier, and the architectural pattern they should have built instead. It also covers two other deployments I audited after this one, in which the same pattern appeared across different industries. The combined evidence is that cost-optimization routing layers, in the shape the consensus playbook prescribes, are structurally fragile in production.

  What we built

  The team operated a customer support AI agent for a SaaS product with roughly 4 million monthly active users. The agent ran on a single capable model, the highest-tier reasoning model in their stack at the time of the build. Inference volume was high enough that the monthly bill from their model provider had grown into six figures and was tracking upward as adoption scaled.

  The routing layer was conceptually clean. A small classifier model, custom-trained on roughly 200,000 historical customer-support queries with quality labels, sat in front of the main agent and labeled each incoming query as either “simple” or “complex.” Simple queries are routed to a cheaper model in the same provider family. Complex queries continued to route to the capable model. The classifier itself was a fine-tuned encoder, light enough to run in under 30 milliseconds with negligible cost overhead.

  The classification taxonomy was built from production observation. Simple queries were what the team had repeatedly seen: account lookups, billing status questions, password resets, order tracking, and hours-of-operation questions. Complex queries were the ones that had historically required nuanced, multi-step reasoning: refund disputes, plan-change trade-offs, integration troubleshooting, and billing-cycle anomalies. The split looked like about 65 percent simple and 35 percent complex across a representative week of production traffic.

  The cheaper model the team selected was about a quarter of the per-token cost of the capable model. For the simple queries the classifier sent to it, side-by-side evaluation against the capable model showed equivalent answer quality across 94 percent of a 5,000-query holdout set. The 6 percent gap was visible, but the team judged it acceptable given the cost reduction. They monitored the cheaper model’s quality through their existing evaluation pipeline, which sampled production responses for human review at roughly half a percent of traffic.

  The build took eight weeks. Three engineers, one ML practitioner, partial allocation. They added schema validation between the classifier and the downstream models, instrumentation on the routing decision, and a fallback path in case the classifier itself failed. The deployment was gradual. Five percent of traffic for the first week, then ten, then twenty-five, then fifty, then full rollout over six weeks. Each rollout step held quality metrics in the green range. Latency stayed within their existing target. Cost decreased in line with the routing share.

  By the end of week eight, the monthly inference bill had dropped to roughly 40% of its previous level. The engineering team presented the work at the company’s all-hands. The CFO sent a thank-you note to the AI team. Adoption metrics inside the agent stayed flat to slightly positive. The team moved on to the next quarterly priority.

  The work was solid. The architecture was reasonable. The monitoring was in place. The team had done what every recent piece on AI cost optimization had recommended. Each individual decision was defensible. The combined system, however, had created a quality gap that the existing measurement architecture could not see.

  That gap took three months to surface in business metrics and another month to be correctly attributed. By the time they understood what was happening, four months had elapsed, and the customer impact was already in the room.

  What we measured (and what we did not)

  The team’s evaluation architecture before the routing layer was built on the assumption that they were running a single model. The quality signal came from three sources. A daily human-review sample of about 200 responses, scored for accuracy and helpfulness. An offline regression suite of approximately 12,000 labeled queries is run weekly against the production model. And a satisfaction signal from the agent’s in-product feedback widget, where users could rate responses with a thumbs-up or thumbs-down.

  When the routing layer went live, the team extended the human-review sample to maintain the same total of about 200 daily reviews but did not separate it by routing tier. They added the cheaper model to the offline regression suite, where it scored within their acceptance threshold. They left the in-product feedback widget unchanged because it had no way to determine which model had served the response.

  In retrospect, those three measurement choices were the seed of the problem. The aggregate human-review sample showed quality holding at roughly the pre-routing baseline. The offline regression suite showed the cheaper model passing on its sub-tier. The feedback widget aggregate stayed within historical variance. Everything they could see was green.

  What they were not seeing showed up at three different layers.

  The human-review sample, taken without tier-aware sampling, was effectively a weighted average, with 65 percent of the reviews on the cheap model and 35 percent on the capable model. Because the cheap model was equivalent in the easy cases (the high-volume center of the simple-query distribution), it pulled the aggregate up. Quality issues on the harder edge of the simple-query distribution were diluted to the point of invisibility in the aggregate.

  The offline regression suite tested both models against curated query sets, but the curation was static. It had been built six months before deployment, when the team had no notion of routing. The suite reflected an idealized distribution rather than the actual production distribution that the cheap model now had to handle. The cheap model passed the static suite but degraded on the live edge.

  The in-product feedback widget had a structural problem that the team had known about for over a year but had not prioritized fixing. Customer feedback was sparse. A typical session generated zero ratings. Customers thumbed down responses about 3 times per 1,000 interactions, and those thumbs-down votes were skewed toward customers who were already frustrated about something else entirely. The signal-to-noise ratio on the widget was too low to detect any change smaller than a major regression.

  None of these failures was specific to the routing layer. They were latent in the measurement architecture. The routing layer simply exposed them. As long as the system ran on a single model, the measurement gaps did not produce false-positive readings, because there was only one quality distribution to measure. The routing layer introduced two quality distributions, but the existing architecture could not observe them separately.

  The quality drift on the cheap-model tier began in week three after the full rollout. By week six, the drift was measurable in the regression suite, but the team interpreted the small regression as model-version drift from their provider rather than routing-related, because they were not segmenting their analysis by tier. By week ten, the cumulative impact on customer satisfaction was evident in product metrics. By week thirteen, churn was tracking measurably above the prior baseline.

  That was the point at which the team called me.

  What broke and how we found it

  The diagnosis took two weeks. We reconstructed the routing decisions from the instrumentation log, joined them with the in-product feedback events, and built a per-tier quality view that the team had not previously seen.

  The pattern surfaced immediately on the cheap-model tier. The cheap model was performing well on roughly 80 percent of the queries the classifier sent to it, which matched the equivalent-quality finding from the original 5,000-query holdout. But the other 20 percent in production were structurally different from the holdout in ways the classifier could not detect at decision time.

  The clearest example was billing queries. The classifier had been trained to recognize patterns such as “where is my charge from” or “I got billed twice” as simple queries, on the assumption that account lookup plus invoice retrieval was a reliable downstream pattern. In holdout testing, this was true. In production, a nontrivial portion of those billing queries hid more complex intents. A user asking “where is my charge from” was sometimes asking about an actual fraudulent charge, sometimes about a delayed reconciliation between two systems, and sometimes about a billing-cycle change they had not been notified about. The capable model had been quietly handling these nested intents correctly because it had the headroom to follow the conversation into the complexity. The cheap model treated each of them as the surface-level intent and answered a question the customer was not actually asking.

  The customers who got those wrong answers did not always thumb down. Many of them just disengaged from the agent and called the support line instead. The thumbs-down signal, therefore, underrepresented the failure. The cost of the failure was shifted to the human support team, who handled the same query a second time, with the human cost paid out of a different budget. The aggregate effect was that the AI agent’s measured deflection rate remained steady while the actual human-handled support volume began to climb.

  The team had not connected the rise in human-handled volume to the routing layer because the two teams operated in different cost centers, and the connection was not visible in any single dashboard.

  The cumulative impact on customer satisfaction was harder to measure cleanly, but it eventually showed up in two ways. First, the cohort of customers who interacted with the agent during the routing-layer rollout period showed measurably lower satisfaction scores at the 90-day post-interaction follow-up survey, compared to a baseline cohort from before the rollout. Second, customer retention at the 6-month mark trended downward against the prior baseline, with the steepest drop in segments most exposed to the failing routing patterns.

  When we ran the numbers together, the inferred cost impact of the quality loss was conservatively four to five times the cost savings from the routing layer. The team had cut inference costs by about $100,000 per month and incurred customer retention and support costs of between $400,000 and $500,000 per month. The math, once viewed in full, was unambiguous.

  This is the structural property of the Pareto trap. Cost savings on the inference layer are measured by the team that built the routing system. The cost of quality loss is borne by the customer experience, the human support team, and the retention function, none of which are owned by the team that did the optimization. Each team optimizes its own budget. The combined optimization is negative.

  The team rolled the routing layer back to a much more conservative setting in week sixteen. By week twenty, the customer-satisfaction trend was reversing. By week twenty-eight the retention numbers were back to baseline. The total elapsed cost of the experiment, between cost savings recovered and customer impact incurred, was roughly two quarters of net negative product value.

  Why cheap models break in the long tail

  The reason this pattern is structural rather than situational is worth slowing down on. It is not about the specific model the team chose, the specific provider, or the specific classifier they trained. It is about the geometry of the problem space.

  Customer queries in any production AI deployment follow a power-law distribution of difficulty. A large mass of queries clusters around the easy center. A smaller mass extends into a long tail of harder, more ambiguous, more context-dependent queries. Frontier models are over-provisioned for the easy center. They have far more capability than is needed to answer “what time do you open?” That over-provisioning is exactly why the cost-optimization opportunity is real. Routing the easy center to a cheaper model can yield real savings without sacrificing quality on those queries.

  The problem is that classifiers cannot reliably separate the easy center from the long tail at decision time. The classifier sees the surface form of a query. The long tail is hidden underneath surface forms that look easy. A query that reads as “where is my charge from” can be a trivial account lookup or the opening line of a fraud investigation that requires careful, multi-step reasoning. The classifier sees the same words. The cheap model gives the same surface answer. The customer in the fraud case receives an incorrect answer to a question they were not asking.

  This is the long-tail compression problem. Surface form is a poor predictor of the depth of intent for the queries that matter most. The queries where surface form is most reliable are the easy ones, which are also the ones where model choice matters least. The queries where surface form is least reliable are the hard ones, where model choice matters most. The classifier is well-calibrated exactly where it does not need to be, and poorly calibrated exactly where it does.

  There is a second mechanism. Frontier models tend to have recoverable failure modes. They will sometimes hedge, ask for clarification, or surface their uncertainty in ways that prompt a human to step in. Smaller models often fail confidently. They produce a complete, plausible, surface-coherent response that is wrong about the actual intent. The wrong response is harder for the customer to recognize as wrong than a hedged response would have been, which means the failure goes unflagged longer.

  The third mechanism is drift. Production query distributions evolve. New products launch. New customer cohorts are on board. New failure modes emerge. The classifier trained on six months of historical traffic gradually misroutes a growing share of queries as the distribution shifts away from its training set. The cost savings remain stable because the routing layer continues to send traffic to the cheaper model at the same rate. The quality cost grows quietly, because the classifier is increasingly wrong about which queries are actually simple.

  The combined geometry is unforgiving. The cheap-model tier handles the easy bulk well, fails opaquely on the hidden long tail, and degrades further as the distribution drifts. The savings are visible on a dashboard. The cost is paid downstream by people who cannot see the routing decision.

  This is what makes routing layers a Pareto trap rather than just a noisy optimization. The geometry is structural.

  Two other teams I audited after this

  After we worked through this case, I started looking for the same pattern in other AI deployments I had visibility into. Two surfaced quickly.

  The first was a mid-market SaaS company with a customer-success AI assistant. Smaller scale than the first team, monthly inference spend in the low five figures rather than six. Same architectural pattern. They had built a routing layer four months prior that sent simple queries (defined by an embedding-similarity classifier rather than a fine-tuned encoder) to a cheaper model. Cost savings were on the order of fifty percent. Quality metrics on their internal dashboard read green.

  When we segmented their feedback signal by routing tier, the cheap-model tier had a meaningfully lower satisfaction score for long-tail queries that the embedding classifier had labeled as simple. The team had been blind to the gap because the aggregate dashboard rolled the two tiers into a single number. They estimated the customer-trust impact at roughly two-and-a-half to three times the cost savings, although their measurement was less precise than the first team’s. They reverted the routing layer to a much smaller share within a month of the audit.

  The second was a regulated-industry case in fintech. Monthly inference spend is in the high six figures. They had built a more conservative routing layer that sent only what they considered “informational” queries (account balance, transaction history, basic product information) to a cheaper model, keeping anything that touched compliance or financial decisions on the capable model.

  The pattern showed up differently here. Cost savings were lower because the routing share was more conservative, at around 20%. But the long-tail failure on the cheap-model tier had compliance implications because some queries that read as informational actually carried regulatory weight. A customer asking “what is my interest rate” sometimes had a follow-up question that depended on the first answer being delivered with precision, which the cheap model could not reliably provide. The compliance team caught it through a manual audit before it became a regulatory issue, but the close call moved them to roll the routing back entirely.

  The fintech case was particularly clarifying. It made it obvious that the cost-quality tradeoff is not symmetric across industries. In customer support, a wrong answer is recoverable. In regulated industries, a wrong answer can be a violation. The Pareto trap is amplified in any context where long-tail costs are high or constrained.

  Across the three cases, the pattern was consistent. Cost savings were real and measurable. Quality loss was real and not measurable by the existing architecture. The teams that caught the gap caught it months later, after business metrics had absorbed the impact. The teams that did not catch it would have continued running net-negative optimizations against their own customer base for as long as the dashboards stayed green.

  Detecting the trap before three months pass

  The diagnostic methodology that would have caught any of these earlier is straightforward, but it requires changing the measurement architecture before the routing layer goes live. Three concrete additions to the observability stack.

  Per-tier quality monitoring is the foundational one. Every quality signal in the existing architecture must be split by routing tier, with the tier label propagated end-to-end through the instrumentation. Human-review samples should be stratified so that each tier receives proportional or oversampled review. Offline regression suites should be split into tier-specific subsets and evaluated separately. In-product feedback events should be joined with the routing decision log so satisfaction by tier becomes an aggregated dimension. The aggregate quality number, on its own, is structurally unable to reveal a tier-specific quality drift.

  Long-tail satisfaction sampling is the second addition. Because the long-tail problem is invisible in aggregate, the measurement architecture has to oversample the long tail to make it visible. This means sampling more heavily from queries the classifier was least confident about, or from queries that lie outside the centroid of the classifier’s training distribution. The goal is not to bias the human-review pool toward easy queries, as naive sampling does. The goal is to over-weight the queries where the model choice actually matters.

  Routing confidence drift is the third. The classifier itself is a source of quality signal that most teams do not monitor. The distribution of confidence scores on production traffic should be tracked against the distribution observed during training. When the production distribution shifts, the classifier operates outside its calibrated range, and routing decisions become increasingly unreliable. The drift signal precedes the quality signal by weeks, which is the lead time the team needs to course-correct.

  These three additions are not a checklist to score yourself against. They are a measurement architecture in which each component reveals a class of failure that the others cannot see. Together, they make the Pareto trap visible in days rather than months. The cost of implementing them in engineering time is far lower than the cost of running an undetected quality regression for a quarter.

  Two notes for teams considering this. First, retroactively deploying these measurements is much harder than building them in alongside the routing layer. Doing it before launch costs perhaps three engineer-weeks. Doing it after a quality issue has emerged often requires reconstructing data that was not captured. Second, the measurement architecture matters more than the routing decision itself. A team with good per-tier observability can experiment safely with aggressive routing because they will catch the drift. A team without it cannot safely operate any routing layer at scale.

  What the alternative looks like

  If the consensus playbook of pre-routing-by-classifier is a Pareto trap, the obvious question is what the alternative pattern is. There is one, and it is meaningfully better, though it carries its own tradeoffs.

  The pattern is an uncertainty-routed cascade. Instead of pre-classifying a query as simple or complex before any model touches it, every query starts at the cheaper model. The cheap model produces an answer with a calibrated confidence score, either through a built-in uncertainty estimate or through an explicit self-evaluation step appended to the response. When confidence is high, the response goes directly back to the user. When confidence falls below a threshold, the query is escalated to the capable model, and its response is delivered.

  This pattern inverts the failure mode. The cheap model now decides for itself rather than being decided about by a classifier. The hard queries, which the cheap model would have answered wrongly with confidence, instead surface as low-confidence and trigger escalation. The expensive model handles those cases. The cost profile depends on the cheap model’s confidence distribution, but in our work-through of the customer-support case, the modeled savings landed in roughly the same range as the pre-routing approach, with materially better quality in the long tail.

  Two enhancements compound with the cascade. Shadow scoring runs the capable model on a small percentage of production traffic in parallel with the cheap model, even when the cheap model is confident, to detect drift in real production conditions. Quality-weighted routing incorporates observed satisfaction signal back into the threshold tuning over time, so the cascade adapts as the production distribution evolves.

  The cascade has tradeoffs, the pre-routing approach does not. Latency on escalated queries is roughly the sum of cheap-model latency and capable-model latency, which is meaningfully worse than pre-routing would have been. Cost is harder to predict in advance because it depends on the production confidence distribution. Implementation complexity is moderately higher because calibrating the cheap model’s confidence is itself non-trivial.

  These tradeoffs are real and worth weighing. But they are tradeoffs against the quality floor that the cascade approach maintains and the pre-routing approach does not. In production deployments where the long tail carries material customer cost, the cascade pattern is the architecturally honest choice. For teams architecting AI agents for business automation at meaningful production scale, the cascade-with-observability pattern is the one that survives a quarter of real traffic.

  The optimization layer matters more than the optimization

  The first team I described in this piece eventually got to a stable architecture that combined uncertainty-routed cascades with per-tier observability. Their monthly inference cost settled at roughly 35% below the pre-optimization baseline, which is less of a savings than the pre-routing approach had achieved on paper. Their customer satisfaction returned to pre-experiment levels. The net product value of the deployment, accounting for both layers, is meaningfully positive.

  The lesson the team took from the experience was not that cost optimization is wrong. It was that cost optimization is a choice about which layer of the system you trust to make the right tradeoff. Pre-routing trusts a classifier that cannot see what matters. Cascades trusts the model itself to know what it does not know.

  The cheap optimization is the one that quietly breaks the product. The architecturally honest optimization is the one that survives the long tail. In production AI, the difference is usually a quarter of customer satisfaction.

  
  Pratik K Rupareliya is Co-Founder and Head of Strategy at Intuz. He has spent 18+ years deploying enterprise AI, IoT, and cloud platforms into production across 700+ projects. He writes on the economics of AI at scale for practitioners. What works, what fails, and where the budget actually goes. Based between San Francisco and Ahmedabad.
