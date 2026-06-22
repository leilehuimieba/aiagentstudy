# BB-2026-05-01-214 Summary

## Article

- Title: Frontier AI models corrupt 25% of document content
- Source: BestBlogs / VentureBeat
- URL: https://www.bestblogs.dev/en/article/e60f3fb9
- Date: 05-13
- Topic: `04-evaluation-guardrails`
- Tags: AI Reliability, Delegated Work, LLM Evaluation, Autonomous Agents, Microsoft Research

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article reports on a study by Microsoft researchers that introduces the DELEGATE-52 benchmark, designed to measure how reliably large language models handle delegated knowledge work over multiple iterations. The benchmark simulates 20 consecutive editing tasks across 52 professional domains, using a 'round-trip relay' method to automatically evaluate content fidelity without human annotation. Testing 19 frontier models from OpenAI, Anthropic, Google, Mistral, xAI, and Moonshot, the study found that even the best models corrupt an average of 25% of document content. Critically, about 80% of degradation stems from sparse but massive catastrophic failures, where a single interaction drops at least 10% of content. Frontier models tend to actively rewrite and hallucinate content rather than simply delete it, making errors harder to detect. Providing models with generic agentic tools or adding distractor documents worsens performance. The study serves as a reality check for the hype around autonomous AI agents, recommending short, transparent tasks and incremental human review over complex long-horizon agents.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
