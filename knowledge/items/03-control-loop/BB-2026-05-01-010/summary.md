# BB-2026-05-01-010 Summary

## Article

- Title: Codex CLI 0.128.0 新增 /goal 命令
- Source: BestBlogs / Simon Willison
- URL: https://www.bestblogs.dev/article/5de75aba
- Date: 2026-04-30
- Topic: `03-control-loop`
- Tags: Codex CLI, OpenAI, AI 编码智能体, Ralph 循环, 自主编码

## Model Mapping

- Blocks: Goal, Control Loop, Evaluation/Guardrails, Deliverable
- Layer: engineering, architecture, frontier radar

## Core Takeaway

The new `/goal` command matters because it makes the agent loop explicit: define a target, let the coding agent iterate autonomously, and stop when the goal is reached or the token budget is exhausted.

## Reusable Principle

A strong agent interface should expose goal-directed loops, budget limits, and stopping conditions. Autonomy without an explicit goal and budget is hard to evaluate.

## Follow-Up Questions

- How does `/goal` decide success?
- What evidence does it produce when stopping?
- How should this connect to tests, CI, or PR review?
