# [BB-2026-05-01-316] Summary

## Article

- Title: OWASP Web Security Testing Guide - Reporting Structure
- Source: OWASP
- URL: https://owasp.org/www-project-web-security-testing-guide/latest/3-The_OWASP_Testing_Framework/1-Penetration_Testing_Methodologies/7-Reporting
- Date: 04-01
- Topic: `04-evaluation-guardrails`
- Tags: reporting, evidence, reproducibility, proof-of-concept, pentest

## Model Mapping

- Blocks: Evaluation, Deliverable, Memory
- Layer: engineering practice

## Core Takeaway

OWASP WSTG 的 Reporting Structure 很适合拿来定义 FlagProof 的最小字段集合，因为它把发现描述、影响、复现步骤、证据、修复建议明确拆开了。对 FlagHunter 来说，最关键的不是长篇报告，而是把“漏洞是什么、怎么重放、触发后看到了什么”压成结构化对象。它还提醒我们，证据必须服务复现，而不是服务叙事。

## Reusable Principle

- proof object 要显式区分发现描述、影响、复现步骤和证据。
- 复现步骤必须足够具体，能让另一条 agent 轨迹或人工验证复跑。
- 证据对象应优先保存触发结果与环境条件，而不是只保存结论。

## FlagHunter Relevance

- `FlagProof`：可直接映射成 issue summary / impact / steps / evidence / remediation 结构。
- `ReplayEvalHarness`：验证阶段输出应自动生成简化版重放步骤。
- `Retrospective`：失败案例也应保留最小复现证据，而不是只有错误文本。
