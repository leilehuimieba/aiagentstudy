# BB-2026-05-01-197 Summary

## Article

- Title: Browser Run: now running on Cloudflare Containers， it’s faster and more scalable
- Source: BestBlogs / The Cloudflare Blog
- URL: https://www.bestblogs.dev/en/article/e8e66179
- Date: 05-13
- Topic: `02-tools-actions`
- Tags: Cloudflare, Containers, Browser Run, D1, Queues

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details Cloudflare's migration of its Browser Run service from shared infrastructure with Browser Isolation to its own Cloudflare Containers platform. The move was driven by the need to support rapidly growing demand, particularly from AI agent builders. Key technical challenges included managing global latency between Durable Objects and containers, which was solved by creating regional pools of pre-warmed containers. The most significant architectural change was migrating container state management from Workers KV to D1 and Queues, eliminating race conditions and enabling support for up to 500,000 containers per location through batched writes. The migration resulted in a 4x increase in concurrent browser limits (up to 120), a 50%+ reduction in Quick Action response times, and faster feature delivery, including WebGL and WebMCP support. The article serves as both a technical case study and a demonstration of Cloudflare's dogfooding philosophy.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
