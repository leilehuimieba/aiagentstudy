# BB-2026-05-01-331 Summary

## Article

- Title: Claude Code 成功原因深度解构 + FlagHunter 智能化完整改进方案
- Source: 自产综合分析 / knowledge base + claw-code + FlagHunter 源码
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: Claude Code, Claw Code, FlagHunter, PentestAgent, Agent Architecture, Intelligence, Harness Design, Improvement Plan

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Control Loop, Memory, Evaluation, Permission, Task/Subagent, Protocol Extension
- Layer: from architectural principles to concrete implementation roadmap

## Core Takeaway

Claude Code 的成功不是单一突破，而是 **7 个设计原则的同时生效**：(1) 控制循环是工程化 ReAct 而非提示词技巧；(2) 工具面是统一契约而非散装函数；(3) 权限是硬门禁而非事后补丁；(4) 子代理是一等公民而非 prompt 包装；(5) 记忆是外化工件体系而非模型隐式记忆；(6) 上下文是装配流水线而非"多喂点 tokens"；(7) 能力面是可演化生态而非一次性硬编码。FlagHunter 缺少其中 6 项。改进路线应按"先建控制面、再做智能感、最后做生态"的顺序：Phase 1 补权限门+统一工具面，Phase 2 补子代理+思考分离+工具搜索，Phase 3 补任务底座+上下文装配+外化记忆，Phase 4 补 MCP Client+Hook 系统+可观测性。
