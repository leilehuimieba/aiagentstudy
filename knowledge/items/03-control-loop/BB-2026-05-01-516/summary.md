# BB-2026-05-01-516 Summary

## Article

- Title: Cloud Native - AI Native Multi-Agent Digital Human Architecture Practice
- Source: BestBlogs / 阿里云开发者
- URL: https://www.bestblogs.dev/article/cb8e134b
- Date: 06-11
- Topic: `03-control-loop`
- Tags: AI Agent, Multi-Agent Collaboration, Cloud Native, AI Native, AgentTeams

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Starting with the scenario of automatic diagnosis of early morning alerts, the article highlights the necessity of multi-agent collaboration. The author traces the evolution from RPA to single agents and then to multi-agent collaboration, proposing that the core of AI Native is to 'design systems inherently around AI agents.' The core content revolves around AgentTeams: a collaboration orchestration and governance plane that uses four CRDs—Manager, Team, Worker, and Human—to declaratively model organizational structures, and designs a three-tier permission system (L1/L2/L3) to natively support HITL. The article details a deployment path based on cloud products, including security practices such as network connectivity and credential convergence to an AI gateway. Finally, it shares the real-world results of four AI Native scenarios (full-cycle R&D, intelligent on-call, open-source pipeline, business analysis), demonstrating capabilities such as a digital human team closing a ticket within 6 minutes and automatically analyzing issues and submitting PRs.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
