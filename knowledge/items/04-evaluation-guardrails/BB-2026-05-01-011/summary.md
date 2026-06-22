# BB-2026-05-01-011 Summary

## Article

- Title: 我们对 OpenAI GPT-5.5 网络能力的评估
- Source: BestBlogs / Simon Willison
- URL: https://www.bestblogs.dev/article/29a3b9f4
- Date: 2026-04-30
- Topic: `04-evaluation-guardrails`
- Tags: GPT-5.5, AI 安全, 网络安全, 漏洞发现, AI 安全研究所

## Model Mapping

- Blocks: Model, Evaluation/Guardrails
- Layer: evaluation, safety, frontier radar

## Core Takeaway

这是一篇很强的“能力评估 + 风险分级”案例。AISI 的结果表明，GPT-5.5 在其网络安全评测中已经进入前列，不仅在专家级窄任务上表现很强，还成为第二个能端到端完成其企业网络攻击模拟的模型。这意味着高能力模型的风险评估不能只看通用 benchmark，还要看真实攻击链、工具使用和预算约束下的表现。

## Reusable Principle

对智能体和前沿模型的评估，不能只做“有用性评测”，还要做“高风险能力评测”。随着模型具备更强的漏洞研究、利用链拼接和自主探索能力，权限控制、日志留痕、预算上限和场景隔离都需要跟着升级。

## Follow-Up Questions

- AISI 的 95 个网络安全任务分别覆盖了哪些技能层级？
- 对具备更强攻击面探索能力的模型，默认工具权限应如何收紧？
- 在安全敏感环境中，智能体至少应记录哪些操作证据与中间判断？
