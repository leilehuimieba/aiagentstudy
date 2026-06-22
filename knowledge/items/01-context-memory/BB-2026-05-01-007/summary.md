# BB-2026-05-01-007 Summary

## Article

- Title: RAG 已死？不，是 Grep 回归了！
- Source: BestBlogs / 腾讯云开发者
- URL: https://www.bestblogs.dev/article/409d9979
- Date: 2026-04-30
- Topic: `01-context-memory`
- Tags: RAG, Grep, code search, context engineering, AI Agent

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation/Guardrails
- Layer: architecture, engineering

## Core Takeaway

The article argues that code-search agents may not always need vector RAG. In some coding contexts, iterative LLM-driven grep/search loops can be simpler, fresher, and more controllable than prebuilt indexes.

## Reusable Principle

Choose retrieval by environment. For live codebases, deterministic search tools plus iterative reasoning may beat stale indexes. RAG is a tool pattern, not a religion.

## Follow-Up Questions

- When is vector indexing still useful?
- How should an agent decide between grep, AST search, semantic search, and docs retrieval?
- How do we evaluate search quality for coding agents?
