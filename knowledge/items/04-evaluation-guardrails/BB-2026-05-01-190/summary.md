# BB-2026-05-01-190 Summary

## Article

- Title: Agent Evaluation Practices for Intelligent Shopping Assistants
- Source: BestBlogs / 大淘宝技术
- URL: https://www.bestblogs.dev/en/article/dcc796ec
- Date: 05-15
- Topic: `04-evaluation-guardrails`
- Tags: Agent Evaluation, LLM-as-a-Judge, Intelligent Shopping Assistant, Multimodal, Benchmark

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article, from the Taobao Technology team, shares an end-to-end automated evaluation practice for home furnishing shopping agents. It first highlights the issues of high cost, strong subjectivity, and poor reproducibility in traditional manual evaluation, and proposes a closed-loop solution consisting of four modules: Benchmark creation, LLM-simulated manual evaluation, manual sampling verification, and automated evaluation reports. The core innovation lies in constructing a structured evaluation system comprising four primary dimensions (basic instructions, professional instructions, supplementary instructions, and user profiles) and 22 secondary dimensions, employing LLM-as-a-judge for automatic scoring, which achieves 91.9% accuracy after manual verification. Using this pipeline, the team conducted a horizontal comparison of four base models (gpt51, gemini25, external model XX, qwen3-vl), finding that gpt51 delivers the best overall performance with a total score of 0.680, a 16.4% improvement over the current online model qwen3-vl. The article also delves into three core bottlenecks of current agents: inability to recognize existing furniture leading to repeated recommendations, failure to capture core user needs resulting in off-topic responses, and recommending an excessive number of irrelevant items. This evaluation system provides a reusable engineering solution for quantitatively tracking agent capabilities under high-frequency iteration cycles.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
