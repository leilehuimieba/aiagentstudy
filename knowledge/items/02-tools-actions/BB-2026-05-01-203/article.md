# Building production AI agents on Elasticsearch: 5 key lessons

- BestBlogs URL: https://www.bestblogs.dev/en/article/bf31b558
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 10833
- Original publisher URL: https://www.elastic.co/blog/building-ai-agents-elasticsearch-platform

---

5 lessons from a production agentic RAG system that handled one million messages across five AI tools from retrieval thresholds to token strategy

Since 2024, our Field Technology team has been building and deploying AI agents to meaningfully improve our support experience and simplify sales workflows. Our goal is to create systems and tools that give any user a useful, accurate answer the moment they need it. Our AI agents include:

-

Customer-facing Support Assistant: AI agent in our customer support hub to answer customer queries

-

Internal-facing Support Assistant: AI agent with an expanded knowledge base to accelerate support efficiency

-

Case Summarizer: AI agent that enables a support engineer to quickly parse through customer cases

-

Knowledge Drafter: AI agent that automatically drafts knowledge from a given case to expand our knowledge base

-

Sales Assistant: AI agent directly embedded into Salesforce to support revenue teams with account and opportunity analysis

Each tool shares the same underlying Elastic infrastructure but is scoped to a specific workflow and user population.

After one year and over one million messages, we have the data to show what actually happens when AI meets the real world. This inaugural report, Elastic's AI Year in Review,* is built entirely from the analysis of those messages enriched with structured quality metadata. Our analysis reveals a fundamental truth: The success of any AI initiative is about the feedback loop. The most impactful improvements do not come from selecting a specific large language model (LLM). They come from a dedicated focus on retrieval relevance and treating interaction logs as a strategic asset.

Here are the five most significant lessons we discovered in our journey from initial launch to mission critical engine.

Logs are the richest signals in your AI environment. They capture system behavior, application context, and dependencies in a way that other telemetry cannot. By extracting meaning and operational knowledge from logs, any development team can turn this passive data source into the primary engine for insight.

To capture this intelligence in our environment, we built a centralized AI gateway that evaluates all LLM traffic. Using an LLM, we took raw conversation logs, redacted PII data, and transformed this metadata into use case patterns, user engagement paths, and response accuracy metrics. We call this process Context Performance Monitoring, or simply Context Observability. This process enables us to evaluate the effectiveness of our core use cases by analyzing every conversation for sentiment, response quality, and accuracy.

The findings in this report are built entirely from those logs. Without them, we wouldn't have been able to uncover many of the insights that follow. By analyzing these interactions, we can rapidly augment our solutions and ensure we're meeting real-world user needs.

AI tool adoption does not distribute evenly. It clusters around power users.

Throughout 2025, our AI tools handled 209,220 conversation threads spanning five tools, multiple user populations, and dozens of distinct use cases. By the end of the year, nearly 8% of users (our "power users") had generated 80% of all sessions while the remaining 92% of users generated just 20% of all sessions.

This reveals a power law distribution where a small number of actors account for a disproportionately large share of activity. There is a significant divide between "casual users," who occasionally consult our knowledge base, and "power users," who have fully integrated AI into their daily workflows.

As we dug deeper, another pattern emerged. For every simple query, the assistants received three or more complex, technical ones. And as the year progressed, this pattern became even clearer. The questions people were asking in January 2025 were fundamentally different from the questions they asked by December. Power users weren't reaching for the assistant for simple how-tos. They were reaching for it for detailed architectural guidance consistently. This reflects a natural customer maturity curve: As users grow with our product, the demand for complex support increases alongside it.

By the end of the year, it was clear that our most important customers were our repeat users. We needed to ensure that we matured our knowledge base alongside them, so they had what they needed to succeed.

Perhaps the most significant finding in our analysis of retrieval augmented generation (RAG) was the impact of search relevance on LLM reasoning and answer quality.

To drive high relevance, we built a hybrid search retrieval layer combining keyword based search (BM25) with the Elastic Learned Sparse EncodeR (ELSER) — Elastic's sparse vector retrieval machine learning model that runs on Elasticsearch as the underlying vector database and search platform. We defined a quality measurement framework to evaluate AI accuracy using a sentiment analysis model to assess helpfulness, tone, and resolution of interaction. We then correlated those quality signals with user sessions across three distinct retrieval outcomes:

1.

Helpful: Documents retrieved were directly relevant to the question being asked.

1.

Partial: Documents retrieved were tangentially related but not directly useful.

1.

None: No documents were retrieved at all.

The relationship between these outcomes and quality scores reveals a counterintuitive trend:

| RAG retrieval outcome | Avg. quality score

| Helpful (directly relevant) | 9.81/10

| None (no documents retrieved) | 9.18/10

| Partial (tangentially relevant) | 8.15/10

Partial retrieval produces worse answers than no context at all. When given documents that were only tangentially relevant, the model was inclined to use them anyway, and produced worse results because of it.

Retrieval thresholds matter more than retrieval volume. A system configured to return the top 10 documents regardless of relevance score will routinely deliver partial context and degrade quality. The correct behavior is to set a strict confidence threshold and return nothing when no document clears it. "I don't know" is a far more valuable and safer response than a confidently wrong one.

When a retrieval pipeline always returns something (even partial context that isn't very helpful), you never see your blind spots. While this is the default behavior in most implementations, it prevents you from identifying where your knowledge base genuinely fails to cover a topic.

It's critical to set a confidence threshold. Your system should only return documents when relevance clears a defined minimum floor and return nothing when nothing does. This design change serves two purposes: It prevents the partial context quality degradation described above, and it makes knowledge gaps visible.

Every query that returns nothing is a direct signal of an unmet user need. Implementing a strict confidence threshold transforms those failed retrievals into a context roadmap, allowing your team to prioritize building a knowledge base that's verified by actual user demand rather than editorial guesswork.

Initial industry assumptions often treat high token counts as a cost problem to be optimized for. Our analysis proved the opposite: Session depth correlates positively with quality and user satisfaction.

As builders who understand the cost elements, we initially saw high token counts as a red flag both from a cost perspective and as an indicator of a struggling user (someone who was trying to find an answer but couldn't and kept trying).

After a year, the data countered that assumption. Sessions exceeding 50,000 tokens (what we categorize as "deep sessions") averaged a quality score of 9.74 out of 10 — significantly higher than the global average of 9.45. Our top 10 sessions, averaging 583,000 tokens, averaged a quality score of 9.8 out of 10 — 9 of those top 10 sessions recorded a perfect 10/10.

When we dug into these deep sessions, we found that the architects who were deep into Elastic were using AI as a technical partner for tasks that would otherwise require hours of manual work. These sessions consumed the most tokens because they consisted of high-value engineering work, and that correlated with near-perfect accuracy.

The right question to ask is not "how do we reduce token usage?" but "what is the equivalent human cost of this task, and what did we save?" Before implementing rate limits, analyze your longest sessions. Treat high token counts as a signal to investigate, not a cost to optimize away.

These are some of our favorite insights from our year in review. Building AI on a unified platform like Elasticsearch allows us to treat interaction logs as a strategic asset, and that has surfaced insights we simply wouldn't have found otherwise. We're sharing these findings to help other teams move past the prototype phase and build AI that drives genuine business impact through technical precision.

Dive deeper into the most significant lessons from our journey building AI agents at Elastic.

Download the report

The data in this report is yours to build on, but you don't have to build alone. Join our Slack Community, a dedicated space for engineers and architects to discuss the retrieval strategies and operational challenges described in this review.

Join the Elastic Slack Community

*This report is drawn from data collected between January 1, 2025, and December 31, 2025, across five tools: the external Support Assistant, the internal Support Assistant, the Sales Assistant, the Case Summarizer, and the Knowledge Drafter.

---

The release and timing of any features or functionality described in this post remain at Elastic's sole discretion. Any features or functionality not currently available may not be delivered on time or at all.

In this blog post, we may have used or referred to third party generative AI tools, which are owned and operated by their respective owners. Elastic does not have any control over the third party tools and we have no responsibility or liability for their content, operation or use, nor for any loss or damage that may arise from your use of such tools. Please exercise caution when using AI tools with personal, sensitive or confidential information. Any data you submit may be used for AI training or other purposes. There is no guarantee that information you provide will be kept secure or confidential. You should familiarize yourself with the privacy practices and terms of use of any generative AI tools prior to use.

Elastic, Elasticsearch, and associated marks are trademarks, logos or registered trademarks of elasticsearch B.V. in the United States and other countries. All other company and product names are trademarks, logos or registered trademarks of their respective owners.
