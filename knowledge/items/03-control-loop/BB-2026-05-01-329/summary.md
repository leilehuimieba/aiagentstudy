# BB-2026-05-01-329 Summary

## Article

- Title: 最小 Claude Code 风格开源实现蓝图：从研究结论到可开发主干
- Source: Internal synthesis / local KB
- URL: https://github.com/anthropics/claude-code
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: Claude Code, Implementation Blueprint, Agent Harness, Runtime, Tool Registry, Permission Gate, Task System, MCP

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Control Loop, Memory, Evaluation
- Layer: implementation blueprint and staged build plan

## Core Takeaway

如果要复刻一个“Claude Code 风格”的最小开源 coding agent，最稳的起步方式不是一上来堆满插件、MCP、IDE、市场和多代理，而是先收紧成一条可验证的主干：**控制循环 → 工具注册与分发 → 权限门 → session/compact → 计划与待办 → 子代理/任务 → 协议扩展 → 可观测与回归**。每一层都必须有独立的文件边界和验证方法，避免把整个系统塞进一个 REPL 或一个 giant tool executor。这样做的核心目标不是先做“像 Claude Code 的 UI”，而是先做“像 Claude Code 的 harness”。

## Reusable Principle

做 agent 实现蓝图时，先冻结模块边界，再安排阶段顺序，最后给每阶段绑定证据；没有验证点的“实现计划”通常只是愿望清单。
