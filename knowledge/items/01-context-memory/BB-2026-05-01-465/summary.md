# BB-2026-05-01-465 Summary

## Article

- Title: First Token Latency Reduced by 3.6x: Tencent Hunyuan Proposes Stem Sparse Attention Algorithm, New SOTA for Long-Context Inference Acceleration
- Source: BestBlogs / 腾讯混元
- URL: https://www.bestblogs.dev/article/c1e21993
- Date: 06-05
- Topic: `01-context-memory`
- Tags: LLM, AI Inference, Sparse Attention, Model Acceleration, Long Context

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details the Stem sparse attention algorithm and its accompanying HPC operator optimization proposed by the Tencent Hunyuan team. It first identifies the performance bottleneck in the prefill phase of long-text inference, stemming from the quadratic complexity of Transformer self-attention, and analyzes the shortcomings of existing sparse attention solutions at both the algorithmic level (uniform budget allocation, ignoring Value information) and the operator level (high overhead of block skipping). The core innovations of the Stem algorithm include: Token Position Decay (TPD), which allocates more sparse budget to initial tokens based on their importance in the causal information flow; and Output-Aware Metric (OAM), which combines attention scores with the magnitude of Value vectors to more accurately select key tokens. At the operator level, HPC-Stem accelerates the evaluation and block selection process by tens of times through mathematical simplification, while HPC-BSA is designed for the Hopper architecture, enabling near-zero overhead block-level skipping. The article provides end-to-end test data on the Tencent Hunyuan Hy3 preview model, showing a 3.7x reduction in first token latency for a 128K context while maintaining model accuracy. The paper has been accepted by ICML 2026, and the related code has been open-sourced.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
