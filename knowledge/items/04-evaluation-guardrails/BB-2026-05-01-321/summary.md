# [BB-2026-05-01-321] Summary

## Article

- Title: Retrospex: Language Agent Meets Offline Reinforcement Learning Critic
- Source: arXiv
- URL: https://arxiv.org/abs/2505.11807
- Date: 05-17
- Topic: `04-evaluation-guardrails`
- Tags: retrospective, offline-critic, failure-analysis, trajectory-scoring, recovery

## Model Mapping

- Blocks: Evaluation, Memory, Control Loop
- Layer: research

## Core Takeaway

Retrospex 最接近你要的 retrospective 机制：它不是事后写流水账，而是用 critic 去回看整条轨迹，给出更适合下次行动的评价信号。对 FlagHunter 来说，这意味着 retrospective 不该只总结“失败了”，而应输出哪一步偏离、哪类动作浪费预算、哪条证据被误读。这种轨迹级评价非常适合反哺 strategy_memory。

## Reusable Principle

- retrospective 的输出应是可行动的 critic signal，而不是纯描述。
- 要评价整条轨迹，而不是只盯最终成功/失败。
- 负反馈应当能回写到下一轮的策略选择和预算分配。

## FlagHunter Relevance

- `Retrospective`：实现 trajectory-level critic，总结偏航点与浪费动作。
- `strategy_memory`：把 retrospective 结果写成可检索负反馈样本。
- `HypothesisEngine`：用 critic 信号调低高失败率分支的优先级。
