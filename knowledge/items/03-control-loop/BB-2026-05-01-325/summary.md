# BB-2026-05-01-325 Summary

## Article

- Title: Claude Code 公开实现层 + 发布包 + 历史逆向材料综合分析：智能体是如何落地的？
- Source: GitHub / npm / Anthropic Docs / BestBlogs
- URL: https://github.com/anthropics/claude-code
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: Claude Code, Agent Architecture, Plugin System, Subagents, Tools, Native Binary, Source Analysis

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Control Loop, Evaluation
- Layer: curated synthesis from official public artifacts + historical reverse-engineering materials

## Core Takeaway

当前能公开验证到的 Claude Code“源码”其实分成三层：第一层是官方 GitHub 仓库公开的插件、命令、agents、hooks、市场清单与工作流；第二层是 npm 发布的安装器与 `sdk-tools.d.ts`，可验证 Claude Code 暴露出的工具接口、子代理、任务、REPL、计划模式、远程触发等能力面；第三层才是核心 runtime，而它在当前版本中以平台原生二进制发布，并未在 GitHub 仓库中完整开源。因此，对 Claude Code 的“源码级分析”应区分：哪些是官方公开可证的实现层，哪些来自历史 source map 逆向文章，哪些只是基于这些证据做出的工程推断。综合现有证据，可以相对稳健地得出：Claude Code 的核心不是单次推理，而是一层围绕模型构建的 agent runtime / harness，包括能力面管理、上下文治理、多代理协作、权限控制、任务持久化与可观测性。

## Reusable Principle

做生产级 coding agent 时，不要把“模型调用”误认成系统本体；真正需要单独建模的是宿主循环、工具契约、上下文压缩、记忆外化、权限面和异步任务底座。
