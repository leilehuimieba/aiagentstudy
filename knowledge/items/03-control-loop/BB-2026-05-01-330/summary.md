# BB-2026-05-01-330 Summary

## Article

- Title: FlagHunter(PentestAgent) Agent 架构 vs Claw Code：逐层差距分析与改进路线
- Source: 自产分析 / FlagHunter + claw-code 源码
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: FlagHunter, PentestAgent, Agent Architecture, Gap Analysis, Claw Code, Control Loop, Permission, Subagent, Task Registry

## Model Mapping

- Blocks: Control Loop, Tools/Actions, Permission, Memory, Task/Subagent, Protocol Extension, Observability
- Layer: production agent gap analysis against Claude Code-style harness

## Core Takeaway

FlagHunter(PentestAgent) 的 agent 当前是一个**可工作的 ReAct loop + 计划驱动型执行器**，但与 claw-code/Claude Code 风格 harness 相比，缺失了以下关键层：**(1) 权限门禁层** — 工具直接执行无硬门；**(2) 子代理系统** — 无 Agent 工具、无独立 runtime 子代理；**(3) 任务注册表** — 无持久化任务生命周期；**(4) 思考模式分离** — thinking 和 action 混在一起；**(5) Hook 系统** — 无 pre/post 拦截点；**(6) 会话持久化** — 无 save/load session。改进应优先从权限门 + 子代理系统开始，因为这两项直接决定了 agent 能否"自己思考拆解任务"。
