# BB-2026-05-01-210 Summary

## Article

- Title: [Issue 3697] Claude Code Auto-Memory Feature Explained: Say Goodbye to Repeated Instructions, Let AI Remember Your Project
- Source: BestBlogs / 前端早读课
- URL: https://www.bestblogs.dev/en/article/4d48937e
- Date: 05-13
- Topic: `01-context-memory`
- Tags: Claude Code, Auto-Memory, MEMORY.md, CLAUDE.md, AI Programming

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Addressing the pain point of having to repeatedly provide project context every time a new session is started in Claude Code, this article details the auto-memory feature launched by Anthropic. The core of this feature is the introduction of a MEMORY.md file, which is automatically created and maintained by Claude. Unlike the user-written CLAUDE.md, MEMORY.md is a project context record autonomously built by Claude during collaboration, covering aspects such as build commands, coding preferences, and architectural decisions. The article delves into the working mechanism of auto-memory, including the storage location (~/.claude/projects/<project>/memory/), the 200-line limit, and the memory hierarchy (user-level, project-level, auto-memory). Through a practical demonstration of creating a RAG pipeline, it showcases the complete workflow from enabling the feature to testing with a cold-start session. Finally, the article provides various methods to control auto-memory, including disabling it for individual projects, globally, and in CI environments.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
