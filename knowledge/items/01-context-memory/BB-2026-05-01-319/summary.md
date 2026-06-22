# [BB-2026-05-01-319] Summary

## Article

- Title: ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization
- Source: arXiv
- URL: https://arxiv.org/abs/2509.13313
- Date: 10-20
- Topic: `01-context-memory`
- Tags: context-summarization, long-horizon, search-agents, state-compression, recurrent-context

## Model Mapping

- Blocks: Context/State, Memory, Evaluation
- Layer: research

## Core Takeaway

ReSum 直接命中了 FlagHunter 的 observation 膨胀问题：它把长任务中的轨迹压缩成“reasoning state summary”，让 agent 可以在 token 预算内继续推进，而不是被完整历史拖垮。论文最关键的不是“摘要”二字，而是它把 summary 当成下一阶段推理的状态表示，而不是单纯归档文本。对 FlagHunter 来说，这意味着 HTTP body、命令输出、错误栈都应该先提炼成任务相关状态，再决定哪些原文外置保存。

## Reusable Principle

- 压缩对象应是可继续推理的 state，而不是普通摘要。
- 保留高价值信号，外置低频原文，避免把截断当成压缩。
- 摘要后仍要支持回查原始观察，不能只留摘要丢原文。

## FlagHunter Relevance

- `ObservationStore`：把长输出提炼为 reasoning-state summary，并保留 raw pointer。
- `ContextManager`：引入阶段性 summary checkpoint，避免 token exceeded。
- `ReplayEvalHarness`：评估时可比较“原始轨迹 vs 压缩轨迹”对成功率的影响。
