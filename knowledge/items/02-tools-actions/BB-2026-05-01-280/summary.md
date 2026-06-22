# BB-2026-05-01-280 Summary

## Article

- Title: VAPD AgentKit: A Composable Frontend General-Purpose Library for Agents
- Source: BestBlogs / vivo互联网技术
- URL: https://www.bestblogs.dev/article/811c9a29
- Date: 05-20
- Topic: `02-tools-actions`
- Tags: Agent, Frontend Architecture, Composable, Runtime Adapter, Message Model

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article focuses on the VAPD AgentKit developed by vivo's internet project team, aiming to solve the problem of redundant development of conversational AI capabilities across three major business scenarios: notes, knowledge bases, and project management. The core design principles are 'Message as Protocol, Runtime Pluggable, Frontend Orchestratable, and Progressive Enhancement.' Architecturally, it shields backend differences through a unified message model (covering message types such as User, Assistant, Thinking, ActionExecution, Result); achieves backend agnosticism through the Runtime Adapter interface (supporting any streaming protocol like SSE, GraphQL, WebSocket); and manages context, tool calls, and Agent turn loops through the frontend orchestration layer (AgentKit Provider, useAgentChat, useChat Hooks). The article elaborates on the conversion mechanism between event streams and message models, the implementation of Agent turn loops and tool calls (useAgentAction), the design of UI interactions and Suggestions, and provides a minimal getting-started example (3 steps to integrate Chat). Finally, the article looks forward to evolution directions towards knowledge base Q&A (RAG) and integrated workflow intelligence, and identifies the next steps needed to improve capabilities for history records, checkpoints, and Human-in-the-Loop.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
