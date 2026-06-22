# BB-2026-05-01-203 Summary

## Article

- Title: Building production AI agents on Elasticsearch: 5 key lessons
- Source: BestBlogs / Elastic Blog
- URL: https://www.bestblogs.dev/en/article/bf31b558
- Date: 05-14
- Topic: `02-tools-actions`
- Tags: AI Agents, RAG, Elasticsearch, Retrieval Augmented Generation, Production AI

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article presents five critical lessons learned by Elastic's Field Technology team after one year of deploying five AI agents (including customer-facing and internal support assistants, a case summarizer, and a sales assistant) that handled over one million messages. The core insight is that AI success hinges on the feedback loop from interaction logs, not just model selection. Key findings include: 1) Logs are the richest signal for AI observability, enabling Context Performance Monitoring. 2) AI adoption follows a power law, with 8% of power users generating 80% of sessions. 3) Partial retrieval in RAG is worse than no retrieval, producing lower quality scores (8.15/10) than no context at all (9.18/10). 4) Setting strict confidence thresholds for retrieval makes knowledge gaps visible and prevents quality degradation. 5) High token usage correlates with higher quality and user satisfaction, challenging the assumption that it is merely a cost problem. The article advocates for treating interaction logs as a strategic asset and prioritizing retrieval relevance over volume.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
