# [BB-2026-05-01-323] Summary

## Article

- Title: Acon: Optimizing Context Compression for Long-Horizon Agents
- Source: arXiv
- URL: https://arxiv.org/abs/2510.00615
- Date: 10-01
- Topic: `01-context-memory`
- Tags: context-compression, long-horizon, observation-filtering, interaction-history, agent-efficiency

## Model Mapping

- Blocks: Context/State, Memory, Evaluation
- Layer: research

## Core Takeaway

Acon 明确把 context compression 拆成两部分：环境观察压缩和交互历史压缩。这对 FlagHunter 很重要，因为 HTTP 响应体和 shell 输出并不是同一种信息源，应该采用不同压缩策略。它补足了 ReSum / Mem0 的一点：不仅要知道“保留什么”，还要知道“按什么来源分层压缩”。

## Reusable Principle

- 不同来源的观察需要不同压缩策略。
- 压缩策略应区分当前可行动信息与仅供追溯的信息。
- 长任务压缩不仅影响成本，也直接影响成功率。

## FlagHunter Relevance

- `ObservationStore`：为 HTTP body、headers、stderr、stdout 设计不同的 summary schema。
- `ContextManager`：按来源分层压缩，而不是统一截断。
- `ReplayEvalHarness`：评估不同压缩策略对轨迹成功率和 token 使用的影响。
