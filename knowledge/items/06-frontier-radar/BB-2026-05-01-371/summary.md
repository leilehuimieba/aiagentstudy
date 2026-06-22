# BB-2026-05-01-371 Summary

## Article

- Title: TogetherAI Open Sources OSCAR: Surpassing TurboQuant! 2-bit KV Cache Quantization for Real-World Serving
- Source: BestBlogs / 魔搭ModelScope社区
- URL: https://www.bestblogs.dev/article/66047258
- Date: 05-25
- Topic: `06-frontier-radar`
- Tags: KV Cache, Quantization, OSCAR, Together AI, SGLang

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details Together AI's open-source OSCAR (Offline Spectral Covariance-Aware Rotation) scheme, which aims to solve the KV Cache memory bottleneck in long-context LLM inference. OSCAR's core innovation lies not in simply reconstructing the K/V vectors with low error, but in analyzing the attention mechanism to push quantization noise into directions that are insensitive to attention. Specifically, OSCAR uses query covariance to guide key rotation and score-weighted value covariance to guide value rotation, combined with Hadamard transform and bit-reversal techniques, achieving efficient quantization at approximately 2.28 effective bits per KV element. On the system implementation side, OSCAR has been integrated into SGLang, managing KV Cache with a three-stage token pool (BF16 sink + INT2 history + BF16 recent), and is compatible with paged KV and prefix cache. Evaluation results show that on models like Qwen3 and GLM-4.7, OSCAR's performance at 2-bit precision is close to BF16, improving by up to 40.1 points over 3-bit TurboQuant, achieving up to ~3x decode speedup and up to ~7x job-level throughput improvement. The article also provides a quick practical guide for deploying OSCAR on SGLang.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
