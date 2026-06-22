# [BB-2026-05-01-303] Summary

## Article

- Title: Training Language Model Agents to Find Vulnerabilities with CTF-Dojo
- Source: arXiv
- URL: https://arxiv.org/abs/2508.18370
- Date: 08-25
- Topic: `06-frontier-radar`
- Tags: ctf-dojo, execution-grounding, replayable-runtime, verifiable-feedback, pass@1

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation, Memory
- Layer: research

## Core Takeaway

CTF-Dojo 把“可验证执行反馈”从软件工程 benchmark 推进到了网络安全 agent 训练：658 个可复现 Docker challenge、486 条 execution-verified 轨迹、跨 InterCode-CTF / NYU / Cybench 的统一收益。对 FlagHunter 来说，这篇论文最重要的不是 SOTA 分数，而是它证明了 replayable runtime + verified trajectory 能同时服务训练和评测。也就是说，Phase 6 Replay Eval Harness 不只是做回放，它未来还可以反哺策略学习。

## Reusable Principle

- 优先建设可复现执行环境，因为它既能做 eval，也能沉淀训练轨迹。
- trajectory 要求 execution-verified，不能只存模型自述。
- 跨 benchmark 对比时统一使用 pass@1 / absolute gain 这类稳定指标。

## FlagHunter Relevance

- `ReplayEvalHarness`：可直接参考其 Docker 化、可重放、可校验的 challenge runtime 设计。
- `StrategyMemory`：把 execution-verified 成功轨迹当成高质量经验样本沉淀。
- `RecoveryController`：失败回放不应只输出日志，而要产出可训练的负例 / 正例轨迹。
