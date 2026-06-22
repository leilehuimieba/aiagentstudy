# BB-2026-05-01-326 Summary

## Article

- Title: Hello-Agents 地基参考：从智能体定义到记忆、上下文、协议与评估
- Source: Datawhale / GitHub
- URL: https://datawhalechina.github.io/hello-agents/
- Date: 2026-05-26
- Topic: `03-control-loop`
- Tags: Hello-Agents, Agent Fundamentals, ReAct, Memory, Context Engineering, MCP, Evaluation

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Control Loop, Memory, Evaluation
- Layer: curated foundation pack for later Claude Code and coding-agent analysis

## Core Takeaway

`hello-agents` 这套材料可以作为分析 Claude Code 这类 coding agent 的通用地基：第一章给出智能体的定义与“感知-决策-行动”闭环；第四章给出 ReAct、Plan-and-Solve、Reflection 三种经典控制范式；第八章把记忆拆成层级化系统；第九章把上下文工程明确为一个独立的工程问题；第十章把 MCP / A2A / ANP 放到协议基础设施层；第十二章则说明必须用 benchmark 和任务指标去评估 agent，而不是凭感觉判断“像不像智能”。把这六块拼起来，再回看 Claude Code，就能更清楚地区分：哪些属于模型能力，哪些属于 harness 设计，哪些属于工具和协议基础设施，哪些属于评估与守护栏。

## Reusable Principle

先用通用 agent 心智模型搭地基，再去读具体产品；否则容易把某个产品的工程补丁误当成普适原理。
