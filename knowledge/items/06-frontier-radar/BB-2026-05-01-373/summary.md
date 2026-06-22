# BB-2026-05-01-373 Summary

## Article

- Title: Introducing DSA Attention to Multimodal Models: Kuaishou Keye 2.0 Opens a New Paradigm for Enhanced Reasoning
- Source: BestBlogs / 快手技术
- URL: https://www.bestblogs.dev/article/1a4247e6
- Date: 05-26
- Topic: `06-frontier-radar`
- Tags: Keye-VL-2.0, Kuaishou, Multimodal Large Language Model, DSA, Sparse Attention

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article is an official technical blog post from the Kuaishou AI team, detailing the core technological breakthroughs of their latest multimodal large language model, Keye-VL-2.0-30B-A3B. It first identifies the pain points of long video understanding: the computational bottleneck and information dilution caused by ultra-long visual contexts. Keye-VL-2.0 addresses this by being the first to apply the DeepSeek Sparse Attention (DSA) architecture in a multimodal setting, combining sparse attention with feature aggregation. This enables deep perception of a 256K ultra-long context, achieving results on video understanding benchmarks like TimeLens and LongVideoBench that surpass closed-source models like Gemini and comparable open-source models. Secondly, the model natively incorporates an Agent collaboration mechanism, demonstrating system-level execution potential in scenarios like Code Agent and Tool Agent. It overcomes catastrophic forgetting in multi-task learning through the innovative MOPD multi-expert policy distillation technique, leading to a comprehensive surge in general capabilities. Finally, the article introduces the Context-RL reward mechanism and a rigorous data engine used in the post-training phase to ensure inference reliability, and discusses the model's potential applications in real-world business scenarios such as Kuaishou's recommendation system and video material production.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
