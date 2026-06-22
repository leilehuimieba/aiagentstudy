# BB-2026-05-01-249 Summary

## Article

- Title: The Open Agent Leaderboard
- Source: BestBlogs / Hugging Face Blog
- URL: https://www.bestblogs.dev/article/8adef831
- Date: 05-18
- Topic: `04-evaluation-guardrails`
- Tags: AI Agents, Benchmarking, General-Purpose Agents, Evaluation Framework, Open Source

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article announces the Open Agent Leaderboard, a collaborative project between IBM Research and Hugging Face. It addresses a critical gap in AI evaluation: most benchmarks only score models, but deployed agents are complex systems involving planning, tool use, memory, and error recovery. The leaderboard evaluates full agent systems across six diverse benchmarks (SWE-Bench Verified, BrowseComp+, AppWorld, tau2-Bench variants) covering coding, customer service, research, and personal assistance. It introduces a unified protocol to standardize interactions across these different benchmarks. Key findings include: general-purpose agents are already competitive with specialized ones, agent architecture (beyond just the model) measurably impacts results and costs, and failed runs cost 20-54% more than successful ones. The project is fully open-source, including the Exgentic evaluation framework and a companion paper. The leaderboard aims to become a community standard for evaluating general-purpose agent systems.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
