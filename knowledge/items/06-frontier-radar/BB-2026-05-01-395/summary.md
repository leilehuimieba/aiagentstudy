# BB-2026-05-01-395 Summary

## Article

- Title: MiMo-V2.5 Series Inference Full-Link Optimization: Pushing Hybrid SWA Efficiency to the Extreme
- Source: BestBlogs / Xiaomi MiMo
- URL: https://www.bestblogs.dev/article/616933e5
- Date: 05-30
- Topic: `06-frontier-radar`
- Tags: Hybrid SWA, KVCache, Inference Optimization, MoE, Multimodal

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article focuses on the MiMo-V2.5 series models (integrating Hybrid SWA, MoE, and multimodal Encoder), documenting the full-link engineering practices from KVCache management, hierarchical caching systems, SWA prefix caching trees, scheduling strategies, Prefill/Decode execution pipelines, to multimodal optimization. Core highlights include: splitting KVCache into Full Attention and SWA dual pools to achieve strict O(W) storage constraints, improving capacity efficiency by approximately 7x; designing a SWA-aware prefix caching tree to resolve the false hit issue of traditional RadixAttention in SWA mode; developing the self-owned GCache high-performance distributed cache, leveraging co-located GPU machines to achieve zero additional storage cost; implementing LLM-Router for KVCache affinity scheduling, boosting L2 cache hit rate by 25%; optimizing Prefill performance through EP reduction, length bucketing, and NUMA conflict fixes; enhancing Decode throughput via full SWA support and PD separation pre-allocation; and multimodal optimizations including EPD separation, GPU preprocessing, and parallel video decoding. Ultimately, the server-side KV Cache hit rate averages 93%, exceeding 95% in personal user scenarios.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
