# BB-2026-05-01-328 Summary

## Article

- Title: Claude Code 风格智能体实现地图：从地基、官方表面到开源对照实现
- Source: Internal synthesis / GitHub / docs / local KB
- URL: https://github.com/anthropics/claude-code
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: Claude Code, Claw Code, Agent Harness, Architecture Map, Control Loop, Tools, Permissions, MCP, Subagents

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Control Loop, Memory, Evaluation
- Layer: architecture map / comparative synthesis built from foundation + official public surface + open comparative implementation

## Core Takeaway

如果把 Claude Code 风格智能体拆成一张实现地图，最稳的分层方式不是按“功能菜单”拆，而是按 **agent harness 层** 拆：最上面是目标输入与用户任务；中间是 `ConversationRuntime / QueryLoop` 这类控制循环；再往下是 session、memory artifact、context compaction、tool registry、permission gate、subagent runtime、task/team/cron、MCP/LSP/plugin/skill 等控制面；最底层才是文件系统、终端、网络、代码库、外部服务这些真实环境。就当前公开证据而言，Claude Code 官方可证的是大量产品表面与接口层，而 `claw-code` 这样的开源 Rust 对照实现则补足了很多 runtime 分层的“可读代码形态”。因此，要研究或复刻 Claude Code，最关键的不是抄某个 prompt，而是把这张“控制循环 + 工具契约 + 权限 + 任务 + 协议 + 记忆”的地图搭完整。

## Reusable Principle

研究 production agent 时，优先画“运行时实现地图”，再谈单点技巧；没有这张地图，看到的只是功能点，有了地图，才能分清哪些是核心骨架、哪些是扩展件、哪些只是表面交互。
