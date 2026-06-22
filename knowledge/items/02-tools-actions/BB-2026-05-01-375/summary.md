# BB-2026-05-01-375 Summary

## Article

- Title: How CodeRabbit Used Claude to Build an Agent Orchestration System / Claude
- Source: BestBlogs / Claude Blog
- URL: https://www.bestblogs.dev/article/8bcc405f
- Date: 05-27
- Topic: `02-tools-actions`
- Tags: Agent Orchestration, AI Coding, CodeRabbit, Claude, Planning System

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article from the Claude Blog details how CodeRabbit, an AI code review platform, built an agent orchestration system using the Claude model family to address a critical failure mode in AI-assisted coding: code that compiles and passes tests but doesn't solve the intended problem. The root cause is identified as an 'internal knowledge gap' where developers assume AI systems share their implicit context. CodeRabbit's solution inserts a planning layer before code generation, coordinating multiple Claude models (Opus for strategy, Sonnet for planning, Haiku for narrow tasks) to produce a collaborative PRD. This plan is validated by stakeholders before implementation, serving as a quality gate. The team also built an evaluation harness to measure plan quality, iterating on the right level of abstraction. The article concludes with best practices for teams adopting AI coding workflows, emphasizing explicit specification and assumption surfacing.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
