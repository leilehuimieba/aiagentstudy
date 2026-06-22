# BB-2026-05-01-189 Summary

## Article

- Title: OpenAI Models in OpenClaw， Done Right — OpenClaw Blog
- Source: BestBlogs / OpenClaw Blog
- URL: https://www.bestblogs.dev/en/article/16e7e40b
- Date: 05-14
- Topic: `02-tools-actions`
- Tags: OpenClaw, Codex, AI Agent, Agent Platform, OpenAI

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This blog post from OpenClaw announces a significant architectural change in how OpenAI models are integrated into the OpenClaw agent platform. Previously, OpenClaw drove the entire model loop itself, translating between its own harness and OpenAI's runtime. Now, for `openai/gpt-*` agent turns, the native Codex app-server harness becomes the default runtime. This means Codex owns the low-level OpenAI loop, including native thread state, tool continuation, and code execution, while OpenClaw retains ownership of the product layer: channels, persona, memory, sessions, and its own integration tools. The key benefits include: visible replies are now deliberate (using a dedicated message tool instead of leaking internal reasoning), dynamic tool loading reduces prompt bloat (Codex can search for and load tool schemas on demand), and subscription-based authentication is supported. The post also discusses how lessons from this integration, such as cleaner tool boundaries and deferred catalogs, are being fed back into the default OpenClaw harness to improve the experience for all models, not just OpenAI's.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
