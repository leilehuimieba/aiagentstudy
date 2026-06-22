# BB-2026-05-01-350 Summary

## Article

- Title: How Vercel Cut Build Wait Times From 90 Seconds To 5
- Source: BestBlogs / ByteByteGo Newsletter
- URL: https://www.bestblogs.dev/article/a325599a
- Date: 05-26
- Topic: `06-frontier-radar`
- Tags: Vercel, Hive, Firecracker, MicroVMs, Build Infrastructure

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article from ByteByteGo Newsletter provides a detailed technical analysis of how Vercel achieved an 18x improvement in build provisioning time by building Hive, its internal build infrastructure platform. The core challenge was hostile multi-tenancy: Vercel must run untrusted customer code on shared hardware, requiring stronger isolation than standard containers provide. The article explains why containers were insufficient for this adversarial threat model and how Vercel adopted AWS Firecracker microVMs as the foundation. Firecracker provides VM-level isolation with near-container speed, booting in ~125ms. On top of this, Vercel layered three key optimizations: faster boot times via image caching and block device snapshotting, a warm pool of pre-booted cells to eliminate cold-start latency for most builds, and leveraging Firecracker's inherently fast boot speed. The article also discusses the tradeoffs, including the cost of maintaining warm pools and the significant engineering investment required to build from primitives rather than using off-the-shelf solutions like Kubernetes. The key takeaway is that Vercel achieved speed by first accepting a harder constraint (adversarial isolation) and then optimizing within that constraint.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
