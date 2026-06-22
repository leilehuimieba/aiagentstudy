# BB-2026-05-01-262 Summary

## Article

- Title: Xiaohongshu Engine Architecture Team's ICDE 2026 Breakthrough: CCD-Aware Orchestration Breaks Multi-Core CPU Vector Search Performance Ceiling
- Source: BestBlogs / 小红书技术REDtech
- URL: https://www.bestblogs.dev/article/7aff9979
- Date: 05-18
- Topic: `06-frontier-radar`
- Tags: Vector Search, CCD Architecture, Multi-Core CPU, Cache Affinity, Thread Orchestration

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details the latest research results from the Xiaohongshu Engine Architecture team, presented at ICDE 2026. The team systematically analyzed the core performance bottlenecks of industrial-grade vector ANNS services on AMD EPYC multi-Chiplet (CCD) architecture CPUs, including cross-CCD cache invalidation, cache pollution caused by Hot-Hot co-location, and the destruction of cache affinity due to global task stealing. To address these issues, the team proposed a CCD-aware adaptive thread orchestration framework. The framework comprises three core modules: a unified task submission interface compatible with HNSW and IVF algorithms; a hot-cold aware mapping scheduler that uses a greedy double-ended scanning algorithm to pair hot and cold tables on the same CCD, achieving traffic balance and avoiding cache contention; and a topology-aware hierarchical task stealing mechanism that uses three levels of stealing priority (local, same CCD, cross-CCD) to reduce the cross-CCD task stealing rate from 80% to below 5% while ensuring load balance. Experimental results on Xiaohongshu's real-world workloads show that on a 96-core CPU, the framework achieves up to a 3.7x throughput improvement, a 60%-90% reduction in P999 tail latency, a 6%-30% reduction in L3 cache miss rate, and a 20%-80% reduction in CPU stall time. This work provides a systematic solution for optimizing the performance of industrial-grade vector retrieval on new CPU architectures.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
