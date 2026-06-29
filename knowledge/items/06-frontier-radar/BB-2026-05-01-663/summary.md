# BB-2026-05-01-663 Summary

## Article

- Title: Reliability fail: No automated zone failover for Coinbase’s global trading service
- Source: BestBlogs / The Pragmatic Engineer
- URL: https://www.bestblogs.dev/article/55ff574f
- Date: 06-24
- Topic: `06-frontier-radar`
- Tags: Cloud Reliability, AWS, Availability Zone, Fault Tolerance, Distributed Systems

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article analyzes the May 7, 2026 outage at Coinbase that lasted nearly 10 hours, coinciding with an AWS regional failure. Coinbase confirmed its matching engine is pinned to a single AWS availability zone because of latency requirements from distributed consensus (Raft). However, the company had no automated failover to another zone, requiring emergency code changes to recover. The author contrasts this with Uber's 2016 preparation (regular failover drills) and criticizes Coinbase's engineering culture, especially CEO Brian Armstrong's focus on AI-generated code while basic infrastructure reliability is neglected. A previous outage in October 2025 led to a promise to review deployment strategy, but the single-AZ dependency was not addressed.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
