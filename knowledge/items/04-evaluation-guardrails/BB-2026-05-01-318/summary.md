# [BB-2026-05-01-318] Summary

## Article

- Title: Static Analysis Results Interchange Format (SARIF) Version 2.1.0
- Source: OASIS
- URL: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html
- Date: 11-12
- Topic: `04-evaluation-guardrails`
- Tags: sarif, codeflows, provenance, result-schema, audit-trail

## Model Mapping

- Blocks: Evaluation, Memory, Deliverable
- Layer: engineering practice

## Core Takeaway

SARIF 最适合借鉴到 FlagProof 的地方，是它把“结果 + 位置 + codeFlow + relatedLocation + artifact”设计成了机器可读的证据链。对于自动化安全 agent，proof object 如果只是一个最终字符串，很难支撑审计和回放；但如果像 SARIF 一样，能把证据节点和因果路径编码出来，就更接近真正可追踪的 audit trail。它也是区分“只在源码看见了”与“在运行时触发了”的良好结构参考。

## Reusable Principle

- 证据对象应包含位置、相关工件和事件流，而不是只有描述文本。
- proof schema 需要同时支持静态证据与动态触发证据。
- 审计追踪的关键是节点关系，而不是单个截图或单个响应。

## FlagHunter Relevance

- `FlagProof`：可参考 SARIF 的 result / location / relatedLocation / codeFlow 结构。
- `ObservationStore`：为关键观察点生成可串联的 evidence node。
- `Retrospective`：失败分析可基于 codeFlow 风格路径，而不是散乱日志。
