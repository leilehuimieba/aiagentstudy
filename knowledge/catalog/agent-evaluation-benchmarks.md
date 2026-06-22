# Agent Evaluation / Benchmarks 专题

## 目标

这个专题用于集中回答“怎样知道 agent 真的能用”的问题，覆盖：

1. 开放环境、浏览器、电脑使用、工具调用等 benchmark。
2. 任务是否完成、过程是否可靠、模型是否自信但错误。
3. 生产系统中的评估、观测、安全与零信任边界。

## 推荐阅读顺序

### 先建立评估问题意识

1. `BB-2026-05-01-206` — Why AI Agents Still Fail in Production in 2026
2. `BB-2026-05-01-419` — How to Know If an Agent Has Actually Finished Its Task?
3. `BB-2026-05-01-423` — The AI Model Confidence Trap
4. `BB-2026-05-01-445` — Harness Engineering-Based Business Agent Evaluation Scheme Using Top-Tier Agent

### 再看通用 Agent / Computer Use benchmark

5. `BB-2026-05-01-306` — OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
6. `BB-2026-05-01-305` — WebArena: A Realistic Web Environment for Building Autonomous Agents
7. `BB-2026-05-01-307` — tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
8. `BB-2026-05-01-213` — The Era of Auto Research: 47 Tasks Without Standard Answers Become the Ultimate Test for Agent Capabilities

### 再看垂直任务与安全评估

9. `BB-2026-05-01-190` — Agent Evaluation Practices for Intelligent Shopping Assistants
10. `BB-2026-05-01-198` — SocialReasoning Bench shows the limits of today's AI agents
11. `BB-2026-05-01-284` — DataClawBench: 492 Real-World Data Analysis Tasks
12. `BB-2026-05-01-351` — VulnGym Benchmark Release
13. `BB-2026-05-01-317` — OWASP Benchmark - Benchmark Data Format

### 最后看 guardrails 与治理

14. `BB-2026-05-01-011` — OpenAI GPT-5.5 网络能力评估
15. `BB-2026-05-01-391` — Zero Trust Framework for AI Agents
16. `BB-2026-05-01-397` — Coding agents in the social sciences
17. `BB-2026-05-01-381` — Qwen-Image-Bench

## 建议的研究问题

1. 一个 agent 任务的“完成”应该由模型自报、外部检查器、环境状态，还是用户验收决定？
2. Benchmark 是测模型、工具、harness，还是整个系统？
3. 评估应该记录最终答案、过程轨迹、工具日志、环境快照中的哪些证据？
4. 如何把离线 benchmark、回放测试、线上观测放进同一套可靠性闭环？
5. 权限、隔离、日志、回滚和评估指标之间如何互相约束？

## 本地查询入口

```powershell
.\kb.ps1 search "agent evaluation benchmark replay setup finished task" --topic 04-evaluation-guardrails --limit 10
.\kb.ps1 pack "agent 什么时候算完成 评估 验证" --profile auto --grouped
.\kb.ps1 search "OSWorld WebArena tau-bench agent benchmark" --topic 04-evaluation-guardrails
```

