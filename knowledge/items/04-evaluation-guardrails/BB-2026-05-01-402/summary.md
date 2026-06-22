# BB-2026-05-01-402 Summary

## Article

- Title: Stragglers， Not Failures: How Adaptive Hedged Requests Reduce p99 Latency by 74 Percent
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/999ebcec
- Date: 05-28
- Topic: `04-evaluation-guardrails`
- Tags: Tail Latency, Hedged Requests, DDSketch, Distributed Systems, Performance Engineering

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article addresses the problem of tail latency in distributed systems, specifically the p99 degradation caused by stragglers (slow but not failed requests) in fan-out architectures. It argues that retries, the standard response to latency, are counterproductive for stragglers as they add load to already-struggling back-ends. The proposed solution is an adaptive hedging mechanism that uses DDSketch to learn the real-time latency distribution per host, fires a backup request when a primary request exceeds the current p90 latency, and uses a token bucket budget to prevent load amplification during genuine outages. The article provides a detailed explanation of the algorithm, including the use of a tumbling window for adapting to changing conditions, and presents benchmark results showing a 74% reduction in p99 latency (from 65ms to 17.3ms) with only 8.9% overhead, matching the best hand-tuned static threshold without any manual configuration. It also discusses the application of this technique to LLM inference, where measuring Time to First Token (TTFT) is critical, and provides a reference implementation as a Go library.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
