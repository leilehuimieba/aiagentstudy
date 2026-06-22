# Building an Evaluation Harness for Production AI Agents: A 12-Metric Framework From 100+ Deployments

- BestBlogs URL: https://www.bestblogs.dev/en/article/ed72fe59
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 25432
- Original publisher URL: https://towardsdatascience.com/building-an-evaluation-harness-for-production-ai-agents-a-12-metric-framework-from-100-deployments/

---

Three months into a healthcare AI deployment, our client’s compliance officer asked us a question we couldn’t answer.

“How do you know your agent isn’t hallucinating patient symptoms?”

We had unit tests. We had integration tests. We had a model that performed beautifully on the demo dataset. What we didn’t have was an evaluation harness that could measure hallucination rate, context faithfulness, or tool-selection accuracy in production.

That gap nearly killed the project. Six weeks later, we had a 12-metric evaluation framework running against every agent response, every tool call, every retrieval operation. The compliance team signed off. The agent shipped.

Across the 100+ enterprise AI agent deployments we’ve shipped since then, that framework has evolved into the playbook below. If you’re building production AI agents, this is the evaluation harness we wish we’d had on day one.

## The 12-Metric Framework at a Glance

| Category | Metric | What It Measures | Critical Threshold

| Retrieval | Context Relevance | Are retrieved chunks relevant to the query? | >0.85

| Retrieval | Context Recall | Did we retrieve all relevant info available? | >0.90

| Retrieval | Context Precision | Are top-ranked chunks the most relevant? | >0.80

| Retrieval | Retrieval Latency | How fast did the retrieval complete? | <200ms p95

| Generation | Answer Faithfulness | Does the answer match retrieved context? | >0.95

| Generation | Answer Relevance | Does the answer address the user’s question? | >0.90

| Generation | Hallucination Rate | How often does the model invent facts? | <2%

| Agent | Tool Selection Accuracy | Did the agent pick the right tool? | >0.92

| Agent | Tool Execution Success | Did tool calls succeed? | >0.98

| Agent | Multi-Step Coherence | Did the agent maintain logical flow? | >0.85

| Production | Cost per Query | Token + infra cost per request | <$0.05 typical

| Production | P99 Latency | End-to-end response time | <3s

Three categories cover the agent’s internal operations (retrieval, generation, and agent behavior). The fourth category measures what production cares about (cost and latency). Skip any one of these categories at your own risk.

## Why Most Teams Skip Evaluation (and Pay for It Later)

Across the projects we’ve audited, three patterns explain why teams ship AI agents without proper evaluation infrastructure.

Pattern 1: “We’ll add evaluation after the MVP.”

This is the most common and most expensive pattern. By the time the MVP ships, the team has built a UI, an API, integrations, and onboarded customers. Now they have to add evaluation infrastructure to a system that’s already in production, with users sending unpredictable queries. The retrofit takes 4-6 weeks. The data collection lag means they can’t catch a regression for days. By then, the trust damage is done.

Pattern 2: “Accuracy is enough.”

Accuracy on a held-out test set is necessary but not sufficient. A RAG agent can have 95% accuracy on benchmark questions and still hallucinate 30% of the time on real user queries that fall outside the benchmark distribution. Production traffic is always different from your eval set. Without faithfulness, hallucination rate, and tool-selection metrics, you’re flying blind.

Pattern 3: “Manual spot-checks are fine.”

Manual review works at 100 queries per day. It breaks at 10,000. The teams that try to scale manual review either burn out their engineers or accept that they’re not actually reviewing the volume they claim to. Automated evaluation isn’t optional once you cross a few thousand queries per day.

The framework below addresses all three patterns. Build it before you ship, instrument every layer, and let the metrics tell you what your manual reviews can’t.

For teams building AI agents for business automation, the evaluation harness often determines whether the project ships to production at all.

The framework groups 12 metrics into four categories. Each category answers a different question about how your agent is performing.

### Category 1: Retrieval Metrics (4)

If your agent uses retrieval (RAG, knowledge base lookup, document search), retrieval quality is the foundation. Bad retrieval upstream means no amount of clever prompting downstream can save the response.

#### 1. Context Relevance

What it measures: What fraction of the retrieved chunks are actually relevant to the user’s query?

Why it matters: Most RAG failures we see in production trace back to retrieval rather than generation. The model can only work with what you feed it. If you retrieve 10 chunks and only 3 are relevant, you’ve polluted the context and forced the model to filter signal from noise.

How we measure it: For each query, an LLM-as-judge evaluator scores each retrieved chunk on a 0-1 relevance scale relative to the query. We average across the top-k retrieved chunks.

Target threshold: >0.85 average relevance across top-10 chunks. Below 0.7 indicates a retrieval problem worth investigating before chasing model improvements.

Production note: When we see context relevance drop below 0.75 in production, the cause is almost always one of three things: index drift (new documents not chunked properly), query intent shift (users asking different questions than the eval set), or chunking strategy mismatch (chunks too large or too small for the query type).

#### 2. Context Recall

What it measures: Did we retrieve ALL the information needed to answer the query, or did we miss relevant chunks?

Why it matters: Recall is the silent killer of RAG systems. Low recall means the answer is incomplete or wrong, but the model has no way to signal “I don’t have enough context.” It will confidently generate from partial information.

How we measure it: This requires a labeled eval set in which human evaluators have identified all chunks containing information relevant to a benchmark query. We then compute the fraction of those “ground truth relevant” chunks that our retrieval actually returned.

Target threshold: >0.90 recall on benchmark queries. Below 0.80 means you’re systematically missing information, which leads to confident-but-wrong answers.

Production note: Recall drops are usually a symptom of an embedding model mismatch (your embedding model isn’t capturing the semantics of your domain) or of chunk-size issues (information is split across chunks in ways that defeat similarity search). The fix is often re-chunking, not re-modeling.

#### 3. Context Precision

What it measures: Of the retrieved chunks, are the most relevant ones ranked at the top?

Why it matters: Most production RAG systems pass only the top 3-5 chunks to the LLM context window due to token budgets. If your top-1 chunk is irrelevant but the relevant one is at position 7, you’ve effectively retrieved nothing useful.

How we measure it: We compute Mean Reciprocal Rank (MRR) — the average position of the first relevant chunk in the ranked retrieval results.

Target threshold: MRR >0.80 — your first relevant chunk should be in position 1 or 2 most of the time.

Production note: Precision improves dramatically when you add a reranker after the initial vector search. We’ve seen MRR jump from 0.55 to 0.92 by adding a BGE reranker on top of pgvector retrieval. The latency cost is ~50ms; the precision gain is worth it.

#### 4. Retrieval Latency

What it measures: Time from query receipt to when retrieved chunks are ready, measured at p95.

Why it matters: End-to-end agent response time is dominated by retrieval at scale. If retrieval takes 800ms, the user waits 800ms before the LLM even starts thinking.

How we measure it: Standard application performance monitoring on the retrieval service. We log the retrieval time for every query and report p50, p95, and p99.

Target threshold: p95 retrieval latency <200ms. p99 <500ms.

Production note: Latency spikes usually correlate with one of the following: index size growth without re-tuning HNSW parameters, network hops between the embedding service and the vector DB, or cold-start cache misses. Investigate which of the three before assuming you need a faster vector DB.

### Category 2: Generation Metrics (3)

Once the right context is retrieved, the quality of the generation determines whether the user receives a useful response. Three metrics matter here.

#### 5. Answer Faithfulness

What it measures: Does the generated answer accurately reflect the retrieved context, or does it contradict or fabricate information?

Why it matters: This is the most important metric for any AI agent serving regulated industries. An unfaithful answer in healthcare, fintech, or legal contexts is a compliance failure. Even outside regulation, faithfulness directly determines user trust.

How we measure it: For each generated answer, an LLM-as-judge evaluator extracts atomic claims from the answer, then checks each claim against the retrieved context. The faithfulness score is the fraction of claims supported by the context.

Target threshold: >0.95 faithfulness in regulated industries. >0.90 in general use cases. Anything below 0.85 needs immediate investigation.

Production note: Faithfulness drops usually indicate one of three causes: temperature settings too high (turn it down to 0.0-0.3 for production), context window overflow (your retrieved chunks plus prompt exceed context limits and the model hallucinates from training data), or prompt template encouraging extrapolation (“Based on the context, what do you think about…”).

#### 6. Answer Relevance

What it measures: Does the generated answer actually address what the user asked, or does it wander off-topic?

Why it matters: Relevance is distinct from faithfulness. An answer can be 100% faithful to context yet not address the user’s actual question. Both metrics must be high simultaneously for a good response.

How we measure it: LLM-as-judge evaluator generates 3-5 questions that the answer would be a good response to, then computes semantic similarity between those generated questions and the original user query.

Target threshold: >0.90 relevance. Below 0.80, the agent is answering adjacent questions, not the user’s question.

Production note: Relevance issues often trace back to query rewriting steps in agentic flows. If your agent rewrites “How do I cancel my subscription?” into “What is the cancellation policy?” and then answers the rewritten query, the original intent gets lost.

#### 7. Hallucination Rate

What it measures: How often does the model generate facts, names, numbers, or claims that have no basis in the retrieved context or in verifiable reality?

Why it matters: Hallucination rate is the metric your CTO will ask about. Faithfulness measures fidelity to context; hallucination rate measures fabrication beyond context. They overlap but aren’t identical — a model can be faithful to bad context, or unfaithful in benign ways.

How we measure it: We sample 5% of production queries daily and run them through a dedicated hallucination detection pipeline that flags claims requiring fact-check, then human-reviews the flagged subset.

Target threshold: <2% hallucination rate for production agents. <0.5% for regulated industry deployments.

Production note: Hallucination spikes by query type. Open-ended questions hallucinate more than yes/no. Numeric questions hallucinate more than categorical ones. Build query-type classification into your eval pipeline so you can target investigation.

### Category 3: Agent-Specific Metrics (3)

If your AI system is an agent (multi-step, tool-using, goal-directed) rather than a simple RAG pipeline, three additional metrics matter.

#### 8. Tool Selection Accuracy

What it measures: When the agent has a choice of tools, does it pick the right one for the user’s intent?

Why it matters: Modern agents have access to dozens of tools — search, calculators, calendars, database queries, and API calls. Wrong tool selection cascades — the agent then tries to make a square peg fit a round hole, generating incorrect results downstream.

How we measure it: Build a labeled eval set of (query, correct_tool) pairs. Run the agent against the queries and compute the accuracy of tool selection at the first decision point.

Target threshold: >0.92 for binary tool choices. >0.85 for choices among 5+ tools.

Production note: Tool selection accuracy drops as the number of available tools grows. We’ve seen 95% accuracy with 3 tools collapse to 70% with 12 tools. The fix is usually clearer tool descriptions, fewer tools per agent (decompose into specialized sub-agents), or fine-tuning on tool-use traces from production.

#### 9. Tool Execution Success

What it measures: Of the tool calls the agent makes, what fraction execute successfully (correct arguments, valid responses, no errors)?

Why it matters: An agent can pick the right tool and still call it incorrectly — wrong argument format, missing required fields, malformed input. Tool execution success isolates this failure mode.

How we measure it: Track every tool call in production with success/failure status, error categorization, and retry attempts. Compute success rate per tool, per query type, and per time window.

Target threshold: >0.98 tool execution success rate. Below 0.95 indicates systematic argument-construction problems.

Production note: The most common failure mode is the agent confidently constructing arguments in a format that doesn’t match the tool’s actual schema (e.g., passing a date string when the API expects ISO 8601). The fix is structured-output enforcement (function calling, JSON Schema validation) at the tool boundary.

#### 10. Multi-Step Coherence

What it measures: When the agent executes a multi-step plan, does the logical flow remain coherent across steps?

Why it matters: Single-step accuracy is necessary but not sufficient for agentic behavior. An agent that picks the right tool in step 1, gets a good result, then forgets that result by step 4 has failed, even though every individual step succeeded.

How we measure it: Trace-level evaluation. For each multi-step trace, an LLM-as-judge evaluator scores whether each step builds on prior steps coherently and whether the final output reflects the full reasoning chain.

Target threshold: >0.85 coherence on traces of 4+ steps. Below 0.75, your agent is essentially doing multiple disconnected single-step queries.

Production note: Coherence drops with trace length. We see 95%+ coherence on 2-step traces collapse to 60% on 6-step traces. The fix is either decomposition (splitting a 6-step task into 2 separate 3-step tasks with an explicit handoff) or memory architecture (persistent state across steps rather than re-prompting with the full history each time).

### Category 4: Production Metrics (2)

The first ten metrics measure what the agent does. These two metrics measure what production cares about.

#### 11. Cost per Query

What it measures: Total cost (token cost + infrastructure cost + tool call costs) per user query, averaged across production traffic.

Why it matters: AI agents have a unique cost profile — a single user query can trigger 5-15 LLM calls (rewriting, retrieval grading, tool selection, generation, verification). Token sprawl turns a $0.02 query into a $0.30 query without anyone noticing until the monthly bill arrives.

How we measure it: Instrument every LLM call with token usage logging, every tool call with associated API costs, and every infrastructure dependency with prorated cost. Aggregate per query, then per query type, then per time window.

Target threshold: Varies by use case. Internal employee tools: <$0.10/query is acceptable. Customer-facing products: <$0.05/query for sustainable economics. In regulated industries, cost matters less than other metrics.

Production note: Cost spikes usually trace to one of: prompt length growth (your system prompt grew over time), retry storms (failures triggering re-execution loops), or context window inflation (retrieved chunks getting longer as your knowledge base grows). All three are easy to instrument and fix.

For teams seeing cost-per-query trending upward unsustainably, the build-vs-buy decision often shifts toward custom infrastructure with capped costs rather than per-token API pricing.

#### 12. P99 Latency

What it measures: End-to-end time from user query to final response, measured at the 99th percentile.

Why it matters: Average latency hides the failure modes that frustrate users. A system with 1-second average latency but 15-second p99 has users abandoning sessions after 4-5 slow responses. P99 is what users remember.

How we measure it: Standard application performance monitoring. We log the end-to-end latency for every query and report p50, p95, p99, and max. We track these per query type because conversational queries should be much faster than analytical queries.

Target threshold: p99 <3 seconds for conversational agents. p99 <10 seconds for analytical agents that perform multi-step reasoning. Beyond 10 seconds, users disengage.

Production note: P99 latency is almost always dominated by one of three things: retrieval (vector DB cold cache), tool calls (external API timeouts), or LLM generation for long outputs (hitting token-by-token streaming bottlenecks). Identify the dominant cause before optimizing the wrong layer.

## A Decision Tree: Which Metrics to Prioritize First

Twelve metrics are a lot to instrument simultaneously. Here’s how we sequence implementation across project phases.

Phase 1 (Pre-launch — Week 0-2): Implement retrieval metrics (context relevance, recall, precision) plus answer faithfulness. These four catch the most common pre-launch failure modes.

Phase 2 (Soft launch — Week 3-6): Add hallucination rate, answer relevance, and tool selection accuracy. These catch issues that only emerge with real user traffic.

Phase 3 (Production stable — Week 7+): Add cost per query, P99 latency, tool execution success, multi-step coherence, and retrieval latency. These optimize the running system rather than catch launch-blocking failures.

Use case modifiers:

- Regulated industry (healthcare, fintech, legal): Prioritize faithfulness and hallucination rate above everything else. Aim for >0.97 faithfulness and <0.5% hallucination rate from day one.
- High-volume consumer product: Prioritize cost per query and P99 latency. Faithfulness matters but not at the expense of unit economics.
- Internal employee tools: Prioritize tool execution success and multi-step coherence. Employees forgive slow responses but not broken workflows.

## How This Framework Compares to Existing Tools

You don’t have to build all 12 metrics from scratch. Several open-source and commercial tools cover subsets of this framework.

Ragas covers context relevance, recall, precision, faithfulness, and answer relevance well. It’s the strongest open-source starting point for RAG-specific metrics. Doesn’t cover agent-specific metrics or production health.

TruLens covers similar RAG metrics with stronger observability tooling. Better integration with LangChain and LlamaIndex. Requires more setup than Ragas.

DeepEval offers a broader metric library with good agent-specific support (tool selection, faithfulness). Newer than Ragas, smaller community.

LangSmith provides production monitoring and evaluation for LangChain-based agents. Strong on traces and observability, weaker on offline benchmark evaluation.

Why we built our own framework on top: None of the existing tools cover all 12 metrics in one place, and the agent-specific metrics (tool selection accuracy, multi-step coherence) are particularly underserved. We use Ragas for RAG metrics, custom evaluators for agent metrics, and standard APM tools (Datadog, OpenTelemetry) for production health metrics. The framework above is the unified view across all three.

## Implementation Reality: What It Actually Costs to Build This

Setting up the full 12-metric framework takes 2-3 weeks of focused engineering effort, assuming you have an LLM-judge evaluator already configured.

Time breakdown:

- Eval set construction (labeled queries + ground truth): 4-6 days
- Metric implementation (Ragas or custom): 3-5 days
- CI/CD integration (run eval on every PR): 2-3 days
- Production monitoring instrumentation: 3-5 days
- Dashboards and alerting: 2-3 days

Tooling we use across deployments:

- Eval orchestration: Ragas + custom evaluators in Python
- LLM-as-judge: GPT-4 for high-stakes evaluation, Claude Sonnet for cost-sensitive eval, Llama 3 70B for fully self-hosted compliance environments
- Storage: PostgreSQL for eval results, S3 for raw traces
- Dashboards: Grafana for production metrics, Streamlit for offline eval reports
- Alerting: PagerDuty integration for threshold breaches

Common pitfalls we’ve watched teams hit:

1. Using the same model for generation and judging. This produces inflated scores. Use a different model family for the judge than for the generator.
1. Skipping the labeled eval set. Without ground truth labels, you can’t compute recall or measure regression. The labeling cost is real but pays back within the first month.
1. Running eval only on success cases. You need failure cases in your eval set, or you’ll never catch regressions. Sample production failures aggressively.
1. Treating eval scores as absolute. Track trends and deltas, not absolute scores. A 0.85 score that drops to 0.78 over a week is more meaningful than the absolute number.

## Frequently Asked Questions

### What Is the Minimum Eval Setup for a New AI Agent Project?

For a new project, implement context relevance, answer faithfulness, and tool selection accuracy. These three catch 70% of pre-launch failures with minimal setup overhead. Skip the production metrics until you have actual production traffic.

### How Often Should We Run the Full Eval Suite?

Run offline eval (against labeled benchmark set) on every code change that affects retrieval, prompts, or agent logic. Run online eval (sampled production traffic) continuously, with daily rollup reports. Full benchmark re-runs are expensive but should happen at least weekly to catch regressions.

### Should We Use LLM-as-Judge or Human Evaluation?

Both are sequenced. Use LLM-as-judge for scale (evaluate 100% of production traffic at low cost), use human evaluation for calibration (evaluate a 1-2% sample to verify the LLM judge agrees with human consensus). When the LLM judge and human evaluation diverge, retrain the judge prompt.

### What Is the Difference Between Offline and Online Evaluation?

Offline evaluation runs against a labeled benchmark dataset with known correct answers. Online evaluation runs against real production traffic, where you don’t know the ground truth answer in advance, so you measure proxy signals (faithfulness, relevance, hallucination) rather than accuracy. Both are necessary. Offline catches regressions before they ship. Online catches issues that emerge from real user behavior.

### How Do We Handle Evaluation for Non-Deterministic Agents?

Run each evaluation query 3-5 times and report the mean and variance of scores. High variance indicates the agent’s behavior is unstable, which is itself a signal worth investigating. For production traffic, sample sufficiently to overcome the noise from variance.

### What Metrics Matter Most for RAG Versus Agentic Systems?

Pure RAG systems: prioritize the four retrieval metrics plus faithfulness. Agentic systems: add tool selection accuracy, tool execution success, and multi-step coherence on top of the RAG metrics. The production metrics (cost, latency) matter equally for both.

### How Do We Measure User Satisfaction in Eval?

User satisfaction is downstream of the 12 metrics above. If your faithfulness, relevance, and latency metrics are all in target range, satisfaction will track. Direct satisfaction signals (thumbs-up/down, follow-up questions, session abandonment) are useful as production health indicators but lag behind the metrics that cause them.

### What Is the Eval Cost — Is It Worth It?

LLM-as-judge evaluation costs roughly 30-50% of your inference cost (every production query also gets evaluated by an LLM). For a $4K/month inference budget, expect $1,200-$2,000/month in eval costs. The ROI is preventing a single production incident that would cost engineer-weeks to debug or trust-damage to recover from. After the first prevented incident, eval pays for itself indefinitely.

## Closing Thought

The teams shipping AI agents successfully in 2026 aren’t the ones with the best models. They’re the ones with the best evaluation infrastructure. Models are commodities. Evaluation is differentiation.

If you’re building production AI agents and want a second opinion on your evaluation framework grounded in 100+ deployments, the Intuz team is happy to help.

## Resources

- Ragas — open-source RAG evaluation framework
- TruLens — evaluation and tracking for LLM applications
- DeepEval — open-source LLM evaluation framework
- LangSmith — LangChain’s observability and eval platform
- OpenTelemetry — production observability standard
- HumanEval benchmark — Github
- Ragas paper — automatic evaluation of RAG

Pratik K Rupareliya is the Co-Founder and Head of Strategy at Intuz, where he leads enterprise AI strategy across 100+ deployments spanning healthcare, fintech, manufacturing, and retail. Connect with him on LinkedIn.
