# BB-2026-05-01-291 Summary

## Article

- Title: How Snapchat Serves a Billion Predictions Per Second
- Source: BestBlogs / ByteByteGo Newsletter
- URL: https://www.bestblogs.dev/article/d142a736
- Date: 05-19
- Topic: `06-frontier-radar`
- Tags: ML Platform, System Design, Recommendation Systems, Snapchat, Bento

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article explores the engineering behind Snapchat's Bento ML platform, which handles the immense scale of serving over a billion predictions per second for content ranking, ad auctions, friend suggestions, and AR lenses. It explains how the system is architected around the fundamental asymmetry of ranking requests, where a single user request expands into hundreds of candidate evaluations. The platform is split into a training half, which uses a layered code structure on Kubeflow for rapid experimentation, and a serving half, which tackles the hard operational problems of feature serving at scale. Key design choices include a split feature store (Robusta) to prevent train-serve skew, two strategies for handling high fanout (feature collocation and a dedicated Retrieval service), and a model export step that splits the compute graph between GPU and CPU. The article highlights a critical optimization where reducing serialization overhead led to a 2x latency reduction and 10x cost savings. A continuous feedback loop, with monitoring for drift and a Kubernetes-style reconciliation deployment system, ensures the platform can absorb massive growth, such as a 20x increase in model size over two years.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
