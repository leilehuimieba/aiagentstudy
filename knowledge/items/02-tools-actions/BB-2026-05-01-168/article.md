# The Next Frontier of AI in Production Is Chaos Engineerin...

- BestBlogs URL: https://www.bestblogs.dev/en/article/57fbe17a
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 24819
- Original publisher URL: https://towardsdatascience.com/the-next-frontier-of-ai-in-production-is-chaos-engineering/

---

Here is a question that no chaos engineering tool in production today can answer: Did your last experiment test the right thing?

Not ‘Did it stay within budget?’ That is what SLO error-budget gating handles. Not ‘Did the system survive?’ That is what abort conditions measure. The question is whether the experiment was designed to validate a specific belief about your system’s behavior, and whether its outcome changed what your team knows about failure propagation through your stack.

If your honest answer is ‘we terminated some pods, and they recovered,’ you ran a safe experiment. Whether you learned anything useful is a separate question that current tooling does not ask.

This article makes a concrete argument: chaos engineering has a mature safety layer and an almost nonexistent intent layer. Safety tells you how much to break. Intent tells you what breaking it will teach. These are different design problems requiring different tooling, and conflating them is why chaos programs at scale tend to accumulate scripts without accumulating insight.

The argument is grounded in the architecture I developed and patented (US12242370B2, Intent-Based Chaos Engineering for Distributed Systems), and in observations from practitioners across Intuit, GPTZero, Insurance Panda, Fruzo, and Coders.dev who have independently diagnosed the same structural gap. I will show you the architecture, walk through the data model with code, and explain why this is an AI problem, not just an orchestration problem.

1. The Safety Layer Is Good. It Is Also Incomplete.

Start by giving the current model its due. The SLO error-budget framework, popularized by Google’s SRE practice, gave chaos engineering its first principled safety mechanism. Tying experiment execution to the remaining error budget means you do not inject failure into a system already consuming its reliability headroom [3]. AWS Fault Injection Service’s stop conditions, Gremlin’s reliability score, and Harness ChaosGuard’s Rego policies all represent mature, production-ready implementations of this idea.

These tools answer a well-posed question: given the current state of my system, is it safe to run an experiment right now? The answer is computable, automatable, and reasonably accurate. The question they do not answer is equally important: given the current state of my system, which experiment would be most informative to run right now?

Safety and informativeness are orthogonal. An experiment can satisfy every safety constraint, stay within budget, trigger no aborts, cause no measurable degradation, and still produce nothing useful. If it tested a component not in the critical path of any user-facing behavior, you spent budget learning nothing. If it repeated a failure mode your system has survived a dozen times without updating your understanding of the propagation path, same result.

Core distinction: An experiment is safe when it stays within acceptable cost. An experiment is informative when its outcome updates your model of the system’s failure behavior. These require different design criteria, and only the first has mature tooling.

There is a second structural problem. Scripts are static at the moment of authorship. They encode assumptions about service topology, traffic patterns, and dependency behavior that may be accurate when written and silently wrong six months later. As microservice architectures change weekly, script-to-reality drift accumulates. The script still runs. It tests a world that no longer exists.

2. How Practitioners Describe the Ceiling

The following observations were gathered from practitioners via Qwoted, a platform connecting domain experts with researchers and journalists. A cross-industry survey of engineers who have built chaos programs in production converges on the same structural gap from different angles.

Abhishek Pareek, Founder and Director at Coders.dev, builds distributed systems tooling. His framing is the sharpest diagnosis of the problem:

“What we do not have is an understanding of intent-based resiliency. Existing tools are primarily script-based, and we need to create tools that can model the effects of a specific failure on a large number of microservices before executing the experiment. We need AI that understands the reasoning behind the failure in addition to the mechanics of the failure.” — Abhishek Pareek, Founder & Director, Coders.dev [6]

The word ‘reasoning’ is doing real work here. A script captures mechanics: terminate these pods, inject this latency. It does not capture reasoning: we are running this experiment because we believe the checkout circuit breaker should trip before user-facing error rates climb above 0.1%, and we want to know if it actually does. That reasoning, the hypothesis, is what makes an experiment informative. When it lives only in the engineer’s head, it evaporates as teams and systems change.

Edward Tian, CEO of GPTZero, runs AI inference infrastructure at scale and has developed precise language for what is missing:

“Current chaos tools inject arbitrary points of failure but do not provide any meaningful direction for the user in terms of what they are attempting to validate. The next evolution of chaos will involve targeting specific questions about resiliency, ‘can our systems sustain a degradation in the retrieval of data?’ or ‘are we capable of tolerating a model being unavailable due to a timeout?’, rather than the use of a one-size-fits-all script.”
– Edward Tian, Founder & CEO, GPTZero [7]

“Can our systems sustain a degradation in the retrieval of data?” is a behavioral hypothesis. It names a target behavior, a failure condition, and an implicit success criterion. That is more information than any current chaos tool accepts as input. It is the minimum information needed to design a test that answers the question.

3. The Intent-Based Architecture

US Patent 12242370B2 describes a system in which chaos experiment parameters are derived from behavioral intent specifications rather than hardcoded by engineers. Here is how the architecture works.

3.1 System Overview

The system has four layers. Each layer does something the script-based model cannot. The experiment generator replaces ‘pick a script’ with ‘derive the right experiment from what you want to learn.’ The safety evaluator adds behavioral context to the blast-radius calculation. The outcome recorder turns experiment results into model updates rather than postmortem notes.

Figure 1: Intent-Based Chaos Engineering system architecture (Image by author)
3.2 The Intent Specification

The specification is the input the system requires before generating any experiment. Here is a concrete example for a checkout resilience test:

Listing 1 – Intent specification for a checkout resilience experiment

# intent_spec.yaml
intent:
  id: exp-checkout-inv-2025-01
  target_behavior: checkout_completion
  hypothesis: >
    The checkout flow completes within SLO when the inventory
    service experiences elevated read latency (p99 > 500ms).
    The circuit breaker on inventory_read trips before the
    user-facing error rate exceeds 0.1%.
  acceptance_criteria:
    checkout_p99_latency_ms: 400
    checkout_error_rate_pct: 0.1
    slo_budget_fraction: 0.001   # max 0.1% of daily error budget
  exclusion_zones:
    - payment_auth
    - fraud_detection
    - session_management
  min_steady_state_window: 15m   # require stable baseline before injection
  max_experiment_duration: 20m

Notice what this encodes that a conventional chaos script does not: the hypothesis is a falsifiable statement about system behavior, not a description of what will be broken. The acceptance criteria define what ‘pass’ means in behavioral terms. The exclusion zones and steady-state window enforce constraints most teams handle manually and inconsistently.

3.3 From Specification to Experiment Candidates

The experiment generator traverses the service dependency graph to find all components on the critical path of the target behavior. Here is a simplified Python sketch of that traversal:

Listing 2 – Simplified critical-path traversal using a weighted dependency graph

from typing import List, Dict
import networkx as nx

def get_critical_path_components(
    graph: nx.DiGraph,
    target_behavior: str,
    exclusion_zones: List[str]
) -> List[Dict]:
    candidates = []
    for node in nx.descendants(graph, target_behavior):
        if node in exclusion_zones:
            continue
        edge_data = graph.edges[target_behavior, node]
        candidates.append({
            'component': node,
            'call_frequency': edge_data.get('call_freq', 0),
            'degradation_sensitivity': edge_data.get('sensitivity', 0),
            'in_blast_radius_of': list(nx.ancestors(graph, node))
        })
    return sorted(
        candidates,
        key=lambda x: x['degradation_sensitivity'] * x['call_frequency'],
        reverse=True
    )

The edge weights, call_frequency, and degradation_sensitivity are learned from past experiments and from observability telemetry (traces, service mesh metrics). A component that sits on every checkout request AND whose degradation historically propagates to user-facing errors ranks highest. One that sits on a background job ranks near zero.

4. Real-Time Safety Evaluation: Beyond Static Thresholds

Ishu Anand Jaiswal, Senior Engineering Leader at Intuit, identifies the component that makes safety evaluation genuinely intelligent rather than just automated:

“What’s missing for truly intelligent chaos is an AI planner that understands live topology and ‘resilience budget.’ It should continuously estimate how much additional latency, loss, or resource depletion the system can absorb, then select and sequence experiments that maximize learning while staying inside that budget, updating its model from every run and from real incidents.” — Ishu Anand Jaiswal, Senior Engineering Leader, Intuit [8]

The ‘resilience budget’ concept is different from the SLO error budget. The error budget measures how much reliability you have already consumed this period. The resilience budget is prospective: given the system’s current state, how much additional stress of a specific type can it absorb before behaviors outside the experiment’s scope begin to degrade?

Table 1 below shows how static threshold gating compares to real-time resilience scoring across five key signals:

Signal	Static Threshold Gating	Real-Time Resilience Scoring
SLO error budget	Checked once at experiment start	Continuously monitored; abort triggered if burn rate spikes
Dependency health	Not checked	p99, error rate, circuit-breaker state read from service mesh before and during injection
Blast radius	Fixed fraction of replicas (e.g. 10%)	Dynamically estimated from dependency graph + historical sensitivity weights
Abort signal	Infrastructure metric crosses threshold	Target behavior degradation (e.g. checkout completion rate drops > 2%)
Topology awareness	None, script targets fixed components	Live dependency graph; experiment reroutes if target component already degraded
Learning	None, script unchanged after run	Predicted vs. actual blast radius delta updates edge weights for future runs
Table 1: Static threshold gating vs. real-time resilience scoring

The abort signal row is where the behavioral framing produces its most concrete difference. Instead of halting when service latency crosses a threshold, an intent-aware experiment halts when the target behavior, checkout completion, degrades beyond the acceptance criterion. A latency spike on an irrelevant component does not stop the experiment. A latency spike on the checkout critical path stops it immediately, regardless of what the infrastructure dashboards show.

5. The User-Context Problem Infrastructure Metrics Cannot Solve

Isabella Rossi, CPO at Fruzo, has built chaos mechanisms on top of behavioral signals rather than infrastructure metrics. Her observation cuts to a problem blast-radius control cannot address:

“Chaos engineering tools typically treat system resilience as a static property. They inject stress based on time of day or load thresholds, which misses how brittle a system can be in one user context and perfectly stable in another. A database timeout during signup is catastrophic. The same timeout during an optional feature is barely noticeable. Current tools don’t make that distinction.” – Isabella Rossi, Chief Product Officer, Fruzo [9]

This is technically precise, not just intuitive. A write timeout to the user registration table during a signup flow terminates a session. A write timeout to a feature-flag read cache during a preferences page falls back to defaults silently. Both events look identical on infrastructure dashboards, elevated timeout rate on a database connection pool. Their user impact differs by orders of magnitude.

Table 2 illustrates how the same fault, on the same component, produces wildly different blast-radius severity depending on which user behavior is active:

Fault	Component	User Context	Blast-Radius Severity
DB write timeout	user_profile_db	Signup flow	CRITICAL, session terminated, user lost
DB write timeout	user_profile_db	Preferences update	LOW, silent fallback to defaults, invisible to user
Pod termination	inventory_service	Active checkout	HIGH, checkout may fail or stall beyond SLO
Pod termination	inventory_service	Nightly batch sync	NEGLIGIBLE, batch retries automatically
Latency +200ms	recommendation_api	Homepage load	LOW, async; page renders without recommendations
Latency +200ms	recommendation_api	Checkout upsell step	MEDIUM, synchronous call; adds +200ms to checkout
Table 2: Blast-radius severity depends on active user behavior, not just component health

A script-based chaos tool has no way to populate the ‘User context’ column. It does not know which user behaviors are active when the experiment runs. An intent-based system can, because the intent specification names the target behavior, and the experiment generator only considers components in that behavior’s critical path under current traffic.

6. The Business-Signal Extension: Blast Radius in Dollars

Once you anchor experiments to behaviors rather than components, the logical extension of that principle reaches further than most SRE practice goes today.

James Shaffer, Managing Director at Insurance Panda, has rebuilt his entire chaos program around revenue signals:

“Static scripts are garbage. They don’t respect the network’s current state. We tied our fault injection engine directly to live business metrics, not just server loads. If active quote completions drop by even two percent, the test instantly kills itself. It’s an automated kill switch based on revenue, not latency. What’s missing from genuinely intelligent chaos testing isn’t better AI to break things. It’s AI that understands the blast radius in dollar amounts. A microservice failing might look like a catastrophic outage to an SRE. But if it doesn’t stop a user from buying an auto policy, who cares? Smart chaos needs to learn the difference between technical noise and actual financial bleeding.” — James Shaffer, Managing Director, Insurance Panda [10]

Shaffer’s kill switch, triggered by a 2% drop in quote completions, is a direct production implementation of a behavioral acceptance criterion. The abort signal is the business transaction rate, not a p99 latency threshold. Here is what that looks like in the outcome data model:

# outcome_record.yaml
outcome:
  experiment_id: exp-checkout-inv-2025-01
  hypothesis_result: SUPPORTED   # circuit breaker tripped as predicted
  abort_reason: null             # experiment ran to completion
  # behavioral signals (acceptance criteria)
  checkout_p99_latency_ms: 312   # passed: < 400ms
  checkout_error_rate_pct: 0.04  # passed: < 0.1%
  checkout_completion_rate_delta: -0.3%  # passed: < 2% threshold
  # blast radius: predicted vs actual
  predicted_blast_radius:
    - inventory_read_service
  actual_blast_radius:
    - inventory_read_service
    - cart_service   # DISCOVERED dependency, not in graph model
  budget_consumed_pct: 0.00083
  # model update signals
  graph_updates:
    - add_edge: [checkout, cart_service]
      sensitivity_weight: 0.34
  blast_radius_prediction_error: 0.34

The most valuable line in this record is the discovered dependency: cart_service was not in the graph model, but the experiment revealed it responds to inventory_read degradation. That update propagates forward, the next checkout experiment will include cart_service in its blast-radius evaluation. This is how the system’s model of itself improves over time, without human curation.

7. Why This Is an AI Problem, Not Just an Orchestration Problem

The reasonable objection at this point is that everything described above sounds like engineering work, dependency graph traversal, threshold comparison, structured logging. Do we really need AI for this, or just better plumbing?

The plumbing handles deterministic decisions: if burn rate exceeds X, abort. If latency crosses Y, halt. These are the guardrails current tools implement. They are valuable and closed under known assumptions. The problems that require learned models are the ones where the decision space is not enumerable:

Blast-radius prediction on novel topologies. Predicting second-order effects of a fault on components not directly targeted requires generalization from behavioral patterns in past experiments. You cannot enumerate all possible service graphs at authoring time.
Hypothesis generation. Translating ‘test checkout resilience under inventory degradation’ into a ranked list of fault types ordered by expected informativeness is not rule execution. It requires reasoning about semantic relationships between service behaviors.
Sensitivity weight learning. The edge weights in the dependency graph are not static properties. They shift with traffic patterns, caching behavior, and deployment changes. They need to be learned continuously from experimental outcomes.
Anomaly attribution during experiments. When multiple signals move simultaneously during an experiment, determining which movement is caused by the injected fault versus pre-existing conditions requires a counterfactual model. That is a causal inference problem.

This last point is where the field is furthest from a solution. Adaptive chaos tools are decent at correlating signals but cannot explain why a specific fault cascades the way it does through a given topology [4]. Building that capability requires something no current chaos tool attempts: a causal model of failure propagation that can be updated from experiment outcomes and interrogated with counterfactual queries.

Figure 2: Safety-Driven Chaos Vs. Intent-Driven Chaos (Image by author)
8. The Counterargument, Taken Seriously

Mature teams already write hypothesis statements. The Chaos Engineering principles from Basiri et al. (2016) require defining steady-state behavior before injection [2]. Netflix, Google, and Intuit run disciplined programs where engineers document what they expect to happen before running experiments. Is ‘intent-based chaos engineering’ just a description of what careful practitioners already do?

The objection is partially correct. Mature teams do maintain hypothesis statements. The problem is that they maintain them in documentation, not in tooling. The hypothesis exists in a Notion page. The chaos tool that executes the experiment has no access to it. This creates four specific gaps:

•  The tool cannot verify that the experiment design actually tests the stated hypothesis, a mismatch between documented intent and configured fault is never caught

•  The tool cannot adapt the experiment based on real-time system state relative to the hypothesis, it runs regardless of whether current conditions make the test meaningful

•  The tool cannot update a dependency model based on the delta between predicted and actual blast radius, that signal is lost to a postmortem document

•  The tool cannot prevent the same hypothesis from being tested redundantly, script libraries grow, insight does not

The difference between ‘teams do this manually’ and ‘tooling does this computable’ is the difference between a practice that scales with the team and one that does not. When the engineer who wrote the hypothesis statement leaves, so does the intent. When the system topology changes, the hypothesis may no longer correspond to any real experiment design, and nothing catches that.

9. Three things the field needs to build

The architecture exists. The safety primitives it depends on are mature. The observability infrastructure it requires is widely deployed. Three specific gaps remain between where the field is and where it needs to go.

Gap 1: A standard intent specification schema

Every team that does hypothesis-driven chaos engineering uses its own format, a Notion template, a runbook section, a JIRA ticket type. None of these are machine-readable by chaos tooling. The five fields in Listing 1 above (target_behavior, hypothesis, acceptance_criteria, budget_fraction, exclusion_zones) capture the essential structure. Standardizing this schema, analogous to how OpenAPI standardized service interface descriptions, would let tooling ingest, validate, and act on hypotheses rather than ignoring them.

Gap 2: Structured experiment outcome data

Blast-radius prediction requires training data. Almost no teams currently record experiment outcomes in a structured, queryable format. Outcomes live in Slack threads and postmortem documents. The outcome schema in Listing 4 is a starting point. Instrumenting existing chaos tools to emit structured outcomes automatically, and storing them in a queryable format alongside the dependency graph, would generate the training signal that predictive models need.

Gap 3: Hypothesis-quality evaluation

Chaos programs are currently evaluated on coverage (how many services have been tested) and survival (did the system hold). Neither measures whether experiments were informative. A hypothesis-quality score, did this run’s outcome change the team’s belief about the system, and by how much?, would give practitioners a signal for improving experiment design rather than just accumulating scripts. None of these require new research. They require the field to agree on representations and invest in the data infrastructure that makes learning from experiments computable rather than anecdotal.

Conclusion

Chaos engineering has the right safety primitives. What it lacks is an equally principled approach to informativeness. Without an intent layer, chaos programs tend toward two failure modes: scripts that test the same things repeatedly, and experiments that stay within budget while producing nothing worth learning.

The intent-based architecture addressed in this article does not replace the safety mechanisms the field has built. It adds a layer that makes those mechanisms more meaningful, grounding them in what the operator is actually trying to learn, deriving experiments from behavioral specifications rather than engineering folklore, and accumulating a model of the system’s failure dynamics that improves with each run.

The gap is real, structural, and solvable. The question is whether the field builds the infrastructure to close it, or keeps writing scripts.

References

[1] M. P. Amador, K. P. Annamali, S. Jeuk, S. Patil, M. F. K. Wielpuetz, Intent-Based Chaos Level Creation to Variably Test Environments, US12242370B2 (2025), Cisco Technology Inc., United States Patent and Trademark Office

[2] A. Basiri, N. Behnam, R. de Rooij, L. Hochstein, L. Kosewski, J. Reynolds, C. Rosenthal, Chaos Engineering (2016), IEEE Software, 33(3), 35–41

[3] B. Beyer, C. Jones, J. Petoff, N. R. Murphy, Site Reliability Engineering: How Google Runs Production Systems (2016), O’Reilly Media

[4] D. Kikuta, H. Ikeuchi, K. Tajiri, ChaosEater: Fully Automating Chaos Engineering with Large Language Models (2025), arXiv:2501.11107

[5] L. C. Opara, O. N. Akatakpo, I. C. Ironuru, K. Anyaene, B. O. Enobakhare, Chaos Engineering 2.0: A Review of AI-Driven, Policy-Guided Resilience for Multi-Cloud Systems (2025), Journal of Computer, Software, and Program, 2(2), 10–24

[6] A. Pareek, Expert Practitioner Response on Intent-Based Resiliency (2025), Qwoted — Coders.dev

[7] E. Tian, Expert Practitioner Response on Hypothesis-Driven Chaos Engineering (2025), Qwoted — GPTZero

[8] I. A. Jaiswal, Expert Practitioner Response on AI Planning and Resilience Budgets (2025), Qwoted — Intuit

[9] I. Rossi, Expert Practitioner Response on User-Context Resilience (2025), Qwoted — Fruzo

[10] J. Shaffer, Expert Practitioner Response on Business-Metric Chaos Engineering (2025), Qwoted — Insurance Panda
