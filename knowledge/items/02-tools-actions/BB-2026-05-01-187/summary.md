# BB-2026-05-01-187 Summary

## Article

- Title: How Anthropic's cybersecurity team built a threat detection platform with Claude Code / Claude
- Source: BestBlogs / Claude Blog
- URL: https://www.bestblogs.dev/en/article/5087293a
- Date: 05-11
- Topic: `02-tools-actions`
- Tags: Claude Code, Cybersecurity, AI Agent, Threat Detection, Security Automation

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details how Jackie Bow's Detection Platform Engineering team at Anthropic built CLUE (Claude Looks Up Evidence), a detection and response platform that leverages Claude Code and tool use to automate and enhance cybersecurity operations. The platform addresses the common problem of security analysts being overwhelmed by data and alerts, requiring context-switching between multiple tools. CLUE consists of two main components: CLUE Triage, which performs first-pass alert enrichment and dispositioning, and CLUE Investigate, which allows analysts to query security logs using natural language. The platform connects to Anthropic's internal systems (Slack, docs, code repos, data warehouses) to provide crucial context for alerts. Key results include a reduction in false positives from ~33% to 7%, automated processing of 12,000 queries and 27,000 tool calls in 30 days, and an estimated 5-10x time savings. The team is exploring future directions like proactive threat hunting, using investigation transcripts as a knowledge base, and embracing non-deterministic investigation paths.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
