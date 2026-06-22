# [BB-2026-05-01-302] Summary

## Article

- Title: Hacking CTFs with Plain Agents
- Source: arXiv
- URL: https://arxiv.org/abs/2412.02776
- Date: 12-03
- Topic: `06-frontier-radar`
- Tags: ctf-agent, react-plan, retries, benchmark-saturation, prompting

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

这篇论文最值得 FlagHunter 警惕的一点，是它证明“复杂 harness 并不是唯一答案”：仅靠 ReAct&Plan、工具补全和多次尝试，就把 InterCode-CTF 做到了 95%。也就是说，FlagHunter 当前解题率不高，未必首先是架构层面的问题，更可能是提示策略、工具可用性、尝试预算和恢复路径设计不够好。论文还提醒了另一个关键风险：agent 偶尔会“猜到”无关题目的 flag，这意味着 benchmark 里必须防训练污染与误判。

## Reusable Principle

- 先把 prompt / tool / retry 这三件事做深，再考虑更重的 harness 重构。
- 多次尝试应该是有策略的 diversified retry，而不是简单重跑。
- 评测时要防 flag guessing 与 contamination，否则 solve rate 会被虚高。

## FlagHunter Relevance

- `HypothesisEngine`：把多尝试设计为不同假设 / 不同 plan 的并行或串行分支，而不是同 prompt 重试。
- `stop_no_progress`：当首次轨迹卡死时，不要立刻退出，应切换到 plan-first 或 react-first 等替代策略。
- `ReplayEvalHarness`：需要加入 contamination / guessed-flag 检查，避免把偶然命中当成真实能力。
