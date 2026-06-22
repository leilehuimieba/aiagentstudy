# BB-2026-05-01-173 Summary

## Article

- Title: Build Long-running AI agents that pause， resume， and never lose context with ADK
- Source: BestBlogs / Google Developers Blog
- URL: https://www.bestblogs.dev/en/article/7be5372c
- Date: 05-12
- Topic: `01-context-memory`
- Tags: Agent Development Kit, Long-running Agents, State Machine, Persistent Sessions, Event-driven Architecture

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article from the Google Developers Blog presents a comprehensive architectural guide for building long-running AI agents that can survive idle periods, server restarts, and multi-day workflows. Using a New Hire Onboarding Coordinator Agent as a concrete example, the author walks through three key architectural shifts that separate production agents from stateless demo chatbots: implementing durable memory schemas via explicit state machines instead of relying on raw conversation history, using event-driven dormancy gates with webhooks instead of active polling, and employing multi-agent delegation for specialized sub-tasks. The tutorial provides complete Python code examples using the ADK framework, including state schema definition, persistent SQLite session storage, webhook endpoints for external event handling, and a resume handler that hydrates sessions and applies state transitions atomically. It also covers golden evaluation tests for validating multi-day flows and deployment to Google's Agent Runtime. The core insight is that stateless agents fail on real enterprise workflows due to prompt context pollution, token cost explosion, and reasoning hallucinations over idle time, and the solution is a fundamentally different architecture where agent state is explicit, durable, and decoupled from raw chat history.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
