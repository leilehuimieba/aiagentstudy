# BB-2026-05-01-261 Summary

## Article

- Title: EP216: RAGs vs Agents
- Source: BestBlogs / ByteByteGo Newsletter
- URL: https://www.bestblogs.dev/article/8bdb40d5
- Date: Yesterday
- Topic: `03-control-loop`
- Tags: RAG, Agents, LLM, Claude Code, System Design

## Model Mapping

- Blocks: Goal, Control Loop, Tools/Actions, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article clarifies the fundamental differences between Retrieval-Augmented Generation (RAG) and AI Agents, two key patterns for grounding LLM outputs. It explains that RAG is a linear, two-step process: retrieve relevant chunks from a knowledge base, then generate an answer grounded in that context. This makes it cheap, predictable, and easy to debug. In contrast, Agents use a reasoning loop, allowing the LLM to iteratively select and execute tools (like reading, writing, or editing files) to achieve a goal, making them more flexible but also more token-intensive and harder to debug. The article provides a simple rule of thumb: use RAG when the answer is in your documents, and use an Agent when the answer requires action on other systems. It also includes a detailed breakdown of how a request travels through Claude Code, explaining its agent loop, permission system, and context management strategies like budget reduction, snipping, and auto-compaction.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
