# BB-2026-05-01-440 Summary

## Article

- Title: How Harmonic Rebuilt Scout on Deep Agents and 4x'd Retention with LangSmith
- Source: BestBlogs / LangChain Blog
- URL: https://www.bestblogs.dev/article/eca5ff15
- Date: 06-03
- Topic: `01-context-memory`
- Tags: AI Agent, LLM, LangGraph, Agent Architecture, AI Product Design

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details how Harmonic, a startup intelligence platform for venture capital, rebuilt its Scout AI agent. The first version used a rigid, multi-subgraph pipeline that required constant tuning and failed on open-ended user requests. The V2 architecture is a deliberate simplification: a single frontier model in a Deep Agents harness with access to two tool categories—one for Harmonic's global data layer (40M companies, 200M people) and one for firm-specific context (CRM, emails, connections). This shift unlocked emergent use cases like personalized outreach drafts and abstract investment thesis searches. The article highlights key UX design principles, such as ensuring the model can see everything the user sees (shared filesystem for search results, inline rendering of visualizations). LangSmith Deployment handles durable execution, scaling, and observability, while LangSmith Engine identifies failure modes and suggests improvements. The results are dramatic: 4x retention and 10x session duration, allowing Harmonic to expand its TAM beyond VC firms to innovation, corporate development, and GTM teams.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
