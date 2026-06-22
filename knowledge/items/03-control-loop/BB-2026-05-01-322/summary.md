# [BB-2026-05-01-322] Summary

## Article

- Title: DEVIL'S ADVOCATE: Anticipatory Reflection for Failure Prevention in LLM Agents
- Source: arXiv
- URL: https://arxiv.org/abs/2501.12871
- Date: 01-15
- Topic: `03-control-loop`
- Tags: anticipatory-reflection, failure-prevention, no-progress, branch-switching, meta-reasoning

## Model Mapping

- Blocks: Context/State, Evaluation, Memory
- Layer: research

## Core Takeaway

如果 Reflexion 更像“事后复盘”，那 DEVIL'S ADVOCATE 更像“事前预演失败”。它的价值在于让 agent 在行动前显式思考：最可能的失败模式是什么、有哪些替代计划、遇到什么信号就该切换路径。对 FlagHunter 来说，这和你想解决的过早 stop_no_progress 很贴：不是等完全卡死再停，而是在前几步就布置退路和切换条件。

## Reusable Principle

- 在行动前先枚举高风险失败模式和切换条件。
- meta-reasoning 不应只回答做什么，还要回答何时放弃。
- 预判式反思能减少低价值重试和无效分支膨胀。

## FlagHunter Relevance

- `HypothesisEngine`：生成假设时同时生成 abort condition 与 fallback plan。
- `stop_no_progress`：改成基于预设失效信号的动态切换，而不是静态计数器。
- `RecoveryController`：更早触发分支切换，而不是等 wrong-flag 或硬失败。
