# [BB-2026-05-01-311] Summary

## Article

- Title: Learning From Failure: Integrating Negative Examples when Fine-tuning Large Language Models as Agents
- Source: arXiv
- URL: https://arxiv.org/abs/2402.11651
- Date: 02-18
- Topic: `03-control-loop`
- Tags: negative-trajectories, failed-attempts, agent-tuning, recovery-signals, retrospective

## Model Mapping

- Blocks: Evaluation, Memory, Control Loop
- Layer: research

## Core Takeaway

这篇论文直接回应了 FlagHunter 的一个核心问题：失败轨迹不是噪音，而是可以利用的训练资产。作者证明，只要做基本质量控制，并显式告诉模型哪些轨迹是成功、哪些是失败，负例也能稳定带来性能提升。落到工程上，这意味着 wrong-flag、误用工具、走死路这些记录不应只进日志，而应进入 retrospective 和 strategy_memory。

## Reusable Principle

- 失败轨迹要保留并标注，不要在清洗阶段直接丢弃。
- 负例的价值取决于质量控制与标签设计。
- retrospective 的目标是把失败变成下一轮可消费的结构化信号。

## FlagHunter Relevance

- `strategy_memory`：将失败轨迹结构化保存，供下一次检索与排序使用。
- `Retrospective`：建立成功 / 失败标签和最小原因字段，减少 attribution bias。
- `ReplayEvalHarness`：在回放报告中同时输出成功轨迹与失败轨迹样本。
