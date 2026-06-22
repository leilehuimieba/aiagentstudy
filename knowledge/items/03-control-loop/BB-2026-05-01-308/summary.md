# [BB-2026-05-01-308] Summary

## Article

- Title: Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models
- Source: arXiv
- URL: https://arxiv.org/abs/2310.04406
- Date: 10-06
- Topic: `03-control-loop`
- Tags: mcts, tree-search, planning, exploration-exploitation, self-reflection

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

LATS 把 MCTS、value function、自反思和环境反馈合并到一个统一 agent 框架里，本质上是在解决“不要只走一条路”的问题。对 FlagHunter 而言，它最有用的不是具体数学成绩，而是把 hypothesis 管理从线性队列升级成树搜索：每个分支都可以带价值估计、扩展预算和回溯逻辑。这正好能替代现在过于简单的假设生成 / 排序 / exhaustion 机制。

## Reusable Principle

- 把假设视为搜索树节点，而不是线性 checklist。
- 探索预算应按分支价值动态分配，而不是固定次数平均分。
- 环境反馈应同时服务扩展、剪枝和回溯。

## FlagHunter Relevance

- `HypothesisEngine`：引入树形假设图、value score 和回溯机制。
- `stop_no_progress`：当主分支价值下降时自动切到替代分支，而不是直接停机。
- `RecoveryController`：wrong-flag 或 exploit 失败后，可把失败信号回传给父节点做剪枝。
