# [BB-2026-05-01-324] Summary

## Article

- Title: AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems
- Source: arXiv
- URL: https://arxiv.org/abs/2605.08715
- Date: 05-13
- Topic: `04-evaluation-guardrails`
- Tags: failure-prediction, online-auditing, early-warning, trajectory-monitoring, attribution

## Model Mapping

- Blocks: Evaluation, Context/State, Memory
- Layer: research

## Core Takeaway

AgentForesight 把失败分析往前移了一步：不是任务结束后才复盘，而是在轨迹进行中做 online auditing，尽早预测高风险失败。对 FlagHunter 来说，这个思路很适合 stop_no_progress 和 wrong-flag 前的预警：一旦轨迹开始出现重复动作、证据矛盾、预算异常，就应该提前降权当前策略或触发回退，而不是等到最终提交失败。它也为“失败归因是策略错、工具错还是验证错”提供了实时监控视角。

## Reusable Principle

- 失败归因不应只做事后分析，也要支持在线预警。
- 轨迹级异常信号可以比最终失败更早暴露系统问题。
- 提前干预比事后回滚更节约探索预算。

## FlagHunter Relevance

- `stop_no_progress`：可扩展为在线风险评分，而不是固定步数阈值。
- `Retrospective`：把在线预警信号与最终失败标签对齐，减少 attribution bias。
- `RecoveryController`：在高风险信号出现时提前切换到 fallback plan。
