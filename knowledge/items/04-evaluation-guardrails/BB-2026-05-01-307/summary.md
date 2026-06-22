# [BB-2026-05-01-307] Summary

## Article

- Title: τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
- Source: OpenReview
- URL: https://openreview.net/forum?id=roNSXZpUDN
- Date: 01-22
- Topic: `04-evaluation-guardrails`
- Tags: tau-bench, pass@k, user-simulation, tool-use, reliability

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

τ-bench 对 FlagHunter 最大的启发是：只看单次成功率远远不够，必须测多次运行的一致性。论文提出的 pass^k 指标，非常适合拿来衡量同一题同一配置下 agent 的稳定解题率，而不是偶然一次撞对。更重要的是，它通过比较最终数据库状态和目标状态来判分，这种“看系统状态变化而非看文本解释”的做法，和漏洞利用 / flag 提交流程高度同构。

## Reusable Principle

- 对 agent 评测要同时看单次成功率和多次运行稳定性。
- 多轮交互任务更适合状态对比判分，而不是回复打分。
- 模拟用户或外部交互体时，要警惕评测噪声和不一致性。

## FlagHunter Relevance

- `ReplayEvalHarness`：为每题增加 pass^k 统计，衡量策略改动是否真的提高稳定性。
- `Retrospective`：将“偶然成功但不稳定”视为单独风险类型。
- `EvaluationReport`：对 web / terminal 题记录最终状态差异，而不只是是否返回某段文本。
