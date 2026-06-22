# BB-2026-05-01-327 Summary

## Article

- Title: Claw Code：一个对齐 Claude Code 产品表面的开源 Rust Agent Harness
- Source: GitHub
- URL: https://github.com/ultraworkers/claw-code
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: Claw Code, Rust, Agent Harness, Conversation Runtime, Permission System, Task Registry, MCP, LSP, Subagents

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Control Loop, Memory, Evaluation
- Layer: open-source comparative implementation for Claude Code-style agent runtime

## Core Takeaway

`ultraworkers/claw-code` 不是 Anthropic 官方 Claude Code 主仓，也不是“泄漏出来的原版源码”，而是一个公开的 **Rust 实现 / 复刻型 CLI agent harness**。它最有价值的地方不在“证明 Claude Code 真源码长什么样”，而在于它把 Claude Code 风格的宿主外壳拆成了可以直接读到的工程部件：`ConversationRuntime` 负责用户输入 → 模型流 → tool_use → tool_result 的主循环；`tools` crate 提供 40 个左右工具规范与统一执行分发；`PermissionEnforcer` 把权限模式变成硬门禁；`TaskRegistry`、`Team/Cron`、`McpToolRegistry`、`LspRegistry` 则补上多任务、扩展协议、编辑器语义和长时程协作的基础设施。它更像是一个“如何开源实现 Claude Code 风格 harness”的样板，而不是 Claude Code 官方 runtime 的直接镜像。

## Reusable Principle

如果官方产品的核心 runtime 没有完整开源，那么最有研究价值的往往不是追逐“是否拿到真源码”，而是寻找一个结构上对齐的开源 harness，把控制循环、工具契约、权限门、任务底座和扩展协议逐层拆开分析。
