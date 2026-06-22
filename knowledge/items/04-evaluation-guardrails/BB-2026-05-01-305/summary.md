# [BB-2026-05-01-305] Summary

## Article

- Title: WebArena: A Realistic Web Environment for Building Autonomous Agents
- Source: OpenReview
- URL: https://openreview.net/forum?id=zlsj9akpaa
- Date: 11-07
- Topic: `04-evaluation-guardrails`
- Tags: webarena, functional-correctness, reproducibility, web-agents, long-horizon-tasks

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

WebArena 最适合借鉴的不是“网页自动化”本身，而是它对现实 web 任务做了三件关键工程化处理：自托管、可复现、按 functional correctness 判分。论文中最醒目的数字是 GPT-4 agent 只有 14.41% 成功率，而人类能到 78.24%，这说明一旦任务变成长程、多页面、带真实状态变化，模型能力会迅速塌陷。对 FlagHunter 的 web 题评测来说，这正是需要 replay harness 的原因。

## Reusable Principle

- 网页任务评测必须自托管并可重置，否则结果不可比较。
- 长程任务应以 functional correctness 判定，而不是只比最终文本。
- 真实任务难度会远高于 toy benchmark，必须预留 trajectory 分析能力。

## FlagHunter Relevance

- `ReplayEvalHarness`：web 类 CTF 题可以采用“自托管靶场 + 重置脚本 + 功能性判分”的模式。
- `ObservationStore`：多页面状态变化需要结构化记录，而不是只保存最终 HTML。
- `Retrospective`：轨迹失败点应绑定页面状态与操作序列。
