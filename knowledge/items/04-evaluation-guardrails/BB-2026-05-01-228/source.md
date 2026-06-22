# Source Evidence

- Title: LLM Evals Are Based on Vibes — I Built the Missing Layer That Decides What Ships
- BestBlogs URL: https://www.bestblogs.dev/en/article/5a8c6f1b
- Original publisher URL: https://towardsdatascience.com/llm-evals-are-based-on-vibes-i-built-the-missing-layer-that-decides-what-ships/

## Captured Page Metadata

- Browser title: LLM Evals Are Based on Vibes — I Built the Missing Layer That Decides What Ships
- Description: The article identifies a critical failure mode in LLM evaluation: single-score thresholds miss confident hallucinations where a response sounds authoritative but is ungrounded. The author builds a three-layer system in pure Python: a scoring layer that measures attribution, specificity, relevance, and context quality; a decision layer that converts scores into ACCEPT/REVIEW/REJECT verdicts with plain-English reasons; and an action layer that routes responses to serve, retry, or regenerate. The key insight is splitting faithfulness into attribution (grounding in context) and specificity (concreteness), where high specificity plus low attribution signals a hallucination. The system runs locally in ~291ms, uses an LLM judge only for borderline scores (0.45-0.65), and includes a regression test suite for CI/CD quality gates. Real benchmark data shows it catches 2/2 hallucinations while maintaining sub-300ms latency.
- Date: Today
- Page fetch mode: direct
- Content fetch mode: direct

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/5a8c6f1b: https://www.bestblogs.dev/en/article/5a8c6f1b
- https://towardsdatascience.com/llm-evals-are-based-on-vibes-i-built-the-missing-layer-that-decides-what-ships/: https://towardsdatascience.com/llm-evals-are-based-on-vibes-i-built-the-missing-layer-that-decides-what-ships/
- Introducing workspace agents in ChatGPT: https://openai.com/index/introducing-workspace-agents-in-chatgpt
- The Multi-Agent Trap: https://towardsdatascience.com/the-multi-agent-trap/
- Gemini Embedding 2: Our first natively multimodal embedding model: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/
- Hybrid Search and Re-Ranking in Production RAG: https://towardsdatascience.com/hybrid-search-and-re-ranking-in-production-rag/
- Agents that remember: introducing Agent Memory: https://blog.cloudflare.com/introducing-agent-memory/
- Codex and Subagents — Vaibhav Srivastav & Katia Gil Guzman， OpenAI: https://www.youtube.com/watch?v=MhHEGMFCEB0
- Stop Treating AI Memory Like a Search Problem: https://towardsdatascience.com/stop-treating-ai-memory-like-a-search-problem/
- Your ReAct Agent Is Wasting 90% of Its Retries — Here’s How to Stop It: https://towardsdatascience.com/your-react-agent-is-wasting-90-of-its-retries-heres-how-to-stop-it/
- Building an Evaluation Harness for Production AI Agents: A 12-Metric Framework From 100+ Deployments: https://towardsdatascience.com/building-an-evaluation-harness-for-production-ai-agents-a-12-metric-framework-from-100-deployments/
- Beyond the Vector Store: Building the Full Data Layer for AI Applications: https://machinelearningmastery.com/beyond-the-vector-store-building-the-full-data-layer-for-ai-applications/
