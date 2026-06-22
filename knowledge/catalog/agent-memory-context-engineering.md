# Agent Memory / Context Engineering 专题

## 目标

这个专题用于回答三类问题：

1. Agent 需要什么上下文、记忆和知识库结构。
2. RAG、Grep、混合检索、上下文压缩各自适合放在哪一层。
3. 如何把材料组织成“摘要优先、证据可追溯、按需深读”的长期知识系统。

## 推荐阅读顺序

### 先看总框架

1. `BB-2026-05-01-020` — Agent Memory 与 Context Engineering
2. `BB-2026-05-01-238` — From Prompt to Context to Harness: The Three Evolutions of Engineering and the Endgame
3. `BB-2026-05-01-326` — Hello-Agents 地基参考：从智能体定义到记忆、上下文、协议与评估

### 再看长期记忆与上下文管理

4. `BB-2026-05-01-116` — From Context to Long-Term Memory: Architectural Design
5. `BB-2026-05-01-173` — Build Long-running AI agents that pause, resume, and never lose context with ADK
6. `BB-2026-05-01-254` — Context is the Key to the Agentic Architecture Revolution
7. `BB-2026-05-01-323` — Acon: Optimizing Context Compression for Long-Horizon Agents

### 再看检索与知识库

8. `BB-2026-05-01-007` — RAG 已死？不，是 Grep 回归了！
9. `BB-2026-05-01-430` — How Contextual Embeddings and Hybrid Search Fix Retrieval Failures
10. `BB-2026-05-01-434` — Why Vector Search Alone Isn't Enough: Hybrid Retrieval for RAG
11. `BB-2026-05-01-435` — RAG Is Not Machine Learning, and the ML Toolkit Solves the Wrong Problem

### 最后看产品化与边界

12. `BB-2026-05-01-426` — The permalink problem in AI chat
13. `BB-2026-05-01-432` — How to Write a Great Skill: The Ultimate Practical Guide
14. `BB-2026-05-01-437` — How to Build an AI Support Agent That Knows When NOT to Answer Tickets

## 建议的研究问题

1. 哪些信息应该进入 prompt，哪些应该进入长期记忆，哪些应该按需检索？
2. 什么时候用关键词 / FTS，什么时候加向量检索，什么时候需要重排？
3. Agent 记忆如何避免“越记越乱”：过期、冲突、来源、证据怎么处理？
4. 上下文压缩应该压摘要、压过程、压状态，还是压证据？
5. 技能、知识库、运行时记忆三者应该如何分工？

## 本地查询入口

```powershell
.\kb.ps1 search "Agent Memory Context Engineering RAG hybrid retrieval compression" --limit 10
.\kb.ps1 pack "上下文压缩 长期记忆 agent" --profile deep --grouped
.\kb.ps1 search "hybrid retrieval vector search alone isn't enough" --topic 01-context-memory
```

