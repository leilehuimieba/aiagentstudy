# BB-2026-05-01-183 Summary

## Article

- Title: What I Learned Building Multi-Agent Systems From Scratch
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/en/article/06440a10
- Date: 05-13
- Topic: `03-control-loop`
- Tags: Multi-Agent Systems, Claude Code, Shopify, Agent Orchestration, AI Engineering

## Model Mapping

- Blocks: Goal, Control Loop, Evaluation, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This presentation transcript details Paulo Arruda's journey at Shopify, from early experiments with test generation using dependency graphs to the discovery that agentic search (as in Claude Code) outperforms codebase indexing. A pivotal hackday project revealed that two Claude Code instances could solve a problem that one could not, leading to the creation of a multi-agent orchestration tool called Swarm. The talk covers the adoption of this tool across Shopify, with success stories like reducing theme review time from 22 hours to 7-20 minutes. Key lessons include treating agents as narrow-focused experts, avoiding token waste on personas, and empowering domain experts rather than centralizing AI knowledge. The talk concludes with a vision for 2026 as the year of making agents useful at scale through context engineering, proposing an 'llm-fuse' adapter layer to expose data to agents efficiently and a memory system with a 'Defrag' tool to manage context bloat.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
