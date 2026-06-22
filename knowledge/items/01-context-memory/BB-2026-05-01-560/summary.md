# BB-2026-05-01-560 Summary

## Article

- Title: Anatomy of a high-performance EP kernel
- Source: BestBlogs / Hacker News
- URL: https://www.bestblogs.dev/article/f5ca4d76
- Date: 06-11
- Topic: `01-context-memory`
- Tags: AI Infrastructure, LLM Inference, Expert Parallelism, MoE, DeepEP

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article provides a deep technical analysis of the communication kernels used for Expert Parallelism (EP) in Mixture-of-Experts (MoE) large language model inference. It focuses on the 'dispatch' and 'combine' operations that move token activations between GPUs to meet their assigned experts. The author builds up the anatomy of two primary kernel shapes, as pioneered by DeepSeek's DeepEP library. The high-throughput shape uses a coordination pass to learn the exact number of tokens each expert will receive, allowing for a compact, dynamically-sized buffer that saves HBM memory. The low-latency shape, crucial for the decode phase, skips the coordination round trip by pre-allocating fixed, worst-case-sized buffers for each source rank, trading memory for speed. The article details the mechanics of each approach, including the use of prefix sums, RDMA queues, NVLink forwarding, per-source-rank layouts, and per-expert permutation. It concludes by discussing the evolution of these kernels, including DeepEP V2's move to NCCL, the UCCL project for broader hardware support, and ongoing work on load balancing and fused compute-communication primitives.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
