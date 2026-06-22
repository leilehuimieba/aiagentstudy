# BB-2026-05-01-330 Source

## Primary Sources

1. **FlagHunter(PentestAgent) 源码**
   - 仓库：`D:\webstudy\FlagHunter`
   - 核心文件：
     - `pentestagent/agents/base_agent.py` — BaseAgent 主循环 (`_run_loop`)
     - `pentestagent/agents/pa_agent/pa_agent.py` — PentestAgentAgent (CTF/planning)
     - `pentestagent/tools/registry.py` — 工具注册表
     - `pentestagent/tools/executor.py` — 工具执行器
     - `pentestagent/llm/memory.py` — ConversationMemory 上下文管理
     - `pentestagent/agents/state.py` — AgentStateManager 状态机
     - `pentestagent/config/settings.py` — 全局设置
     - `pentestagent/config/constants.py` — 常量定义

2. **Claw Code 对照实现**
   - 仓库：`D:\newwork\aiagentstudy\knowledge\raw\external\claw-code`
   - 核心文件：
     - `rust/crates/runtime/src/conversation.rs` — ConversationRuntime
     - `rust/crates/tools/src/lib.rs` — 工具系统
     - `rust/crates/runtime/src/permission_enforcer.rs` — 权限门禁
     - `rust/crates/runtime/src/task_registry.rs` — 任务注册表

3. **已有知识库条目**
   - [[BB-2026-05-01-325]] — Claude Code 官方表面
   - [[BB-2026-05-01-327]] — Claw Code 对照分析
   - [[BB-2026-05-01-328]] — 实现地图
   - [[BB-2026-05-01-329]] — 实现蓝图

## Changes

- 2026-05-26: 初始创建，基于 FlagHunter 源码全面勘察 + claw-code 对照分析
