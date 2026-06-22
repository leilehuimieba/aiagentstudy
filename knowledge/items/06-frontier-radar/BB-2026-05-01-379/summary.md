# BB-2026-05-01-379 Summary

## Article

- Title: Kuaishou Open-Sources Keye 2.0: Introducing DSA Attention to Multimodal AI, Pioneering a New Paradigm for Enhanced Reasoning
- Source: BestBlogs / 魔搭ModelScope社区
- URL: https://www.bestblogs.dev/article/55b4de67
- Date: 05-30
- Topic: `06-frontier-radar`
- Tags: Kuaishou, Keye-VL-2.0, Multimodal Large Model, DSA, Sparse Attention

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article introduces the newly open-sourced multimodal large model, Keye-VL-2.0-30B-A3B, from Kuaishou. The core innovation of this model lies in being the first to introduce DeepSeek's DSA (DeepSeek Sparse Attention) mechanism into multimodal scenarios, achieving a 256K ultra-long context capability and reducing long-sequence Prefill costs by 50%. The model adopts an MoE architecture with 30B total parameters and only 3B activated parameters during inference. It achieves 30B-level SOTA on multiple video understanding benchmarks, including VideoMME V2, LongVideoBench, and MLVU, and surpasses several 200B+ open-source models. The article details the model's capabilities in long video understanding (e.g., process decomposition, documentary narrative deconstruction), highlight moment extraction, and Agent task scheduling. It also introduces the MOPD technique for overcoming catastrophic forgetting and the Context-RL mechanism for improving reasoning reliability. Finally, it provides examples of model deployment and invocation based on SGLang.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
