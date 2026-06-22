# [BB-2026-05-01-320] Summary

## Article

- Title: Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
- Source: arXiv
- URL: https://arxiv.org/abs/2509.17370
- Date: 09-23
- Topic: `01-context-memory`
- Tags: long-term-memory, retrieval, selective-retention, context-management, production-agents

## Model Mapping

- Blocks: Context/State, Memory, Evaluation
- Layer: research

## Core Takeaway

Mem0 给 FlagHunter 的直接启发是“不是所有观察都值得进入长期记忆”。它强调 selective memory：只保留未来大概率复用的信息，而非把整段上下文机械搬运。放到 CTF 里，像有效 URL 模板、疑似 secret、已证伪 payload、框架指纹就该优先保留，而完整响应体应该外置。

## Reusable Principle

- 长期记忆要基于未来复用价值做筛选。
- 短期上下文、工作记忆、长期记忆要有明确边界。
- 摘要与检索是配套设计，不是分离模块。

## FlagHunter Relevance

- `strategy_memory`：优先保存可迁移的框架指纹、payload 结果、失败教训。
- `ObservationStore`：将大响应体外置，只把高价值键值对写入主上下文。
- `HypothesisEngine`：优先检索与当前题型相似的历史线索，而非全量历史。
