# BB-2026-05-01-559 Summary

## Article

- Title: Estimating No-CoT Task-Completion Time Horizons of Frontier AI Models — LessWrong
- Source: BestBlogs / LessWrong
- URL: https://www.bestblogs.dev/article/3fbbd732
- Date: 06-11
- Topic: `01-context-memory`
- Tags: AI Safety, LLM, Chain of Thought, AI Evaluation, Frontier Models

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This paper from Redwood Research, the Astra Fellows Program, Aether Research, and MATS investigates a key AI safety question: how long of a task can frontier models complete without outputting any chain-of-thought (CoT) reasoning? The authors evaluate 14 models from GPT-2 (2019) to GPT-5.5 (2026) on 43 benchmarks spanning math, coding, knowledge, agentic tool-use, and safety-relevant questions. They prevent models from emitting reasoning tokens using benchmark-specific prompts and structured-output constraints. The difficulty of each question is estimated via two independent methods: human solve time and the minimum number of reasoning tokens required by o3-mini. The study finds that the 50% no-CoT time horizon (TH) doubles every 373 days (95% CI: 167-691), with GPT-5.5 achieving a TH of about 3 minutes. This is roughly half the growth rate of with-CoT THs since GPT-4, suggesting recent capability gains come primarily from externalized reasoning. Extrapolating forward, models could reach ~25 minutes of latent reasoning by 2030, which would enable much more sophisticated subversion and make CoT monitoring substantially less effective.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
