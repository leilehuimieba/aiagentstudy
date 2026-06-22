# [BB-2026-05-01-314] Summary

## Article

- Title: Tplmap: Server-Side Template Injection and Code Injection Detection and Exploitation Tool
- Source: GitHub
- URL: https://github.com/epinna/tplmap
- Date: 05-24
- Topic: `05-security-techniques`
- Tags: tplmap, automation, ssti-detection, engine-fingerprinting, sandbox-escape

## Model Mapping

- Blocks: Tools/Actions, Evaluation
- Layer: domain knowledge

## Core Takeaway

Tplmap 的价值不在于“替你全自动打下目标”，而在于它把 SSTI 自动化拆成了可实现的步骤：参数级注入点确认、引擎识别、上下文识别、能力探测（file read / write / os-shell / code eval）。这非常适合反向指导 FlagHunter 的 strategy_registry，把 SSTI 从单次 payload 尝试升级成能力渐进发现流程。它还明确给出了黑盒下的最小证明路径，比如 {{7*7}} -> 49。

## Reusable Principle

- 自动化探测要先确认 injectable parameter，再识别引擎和上下文。
- 利用阶段应按 capability 递进：read / write / code-eval / shell。
- 黑盒 PoC 需要最小化、低破坏、可重复。

## FlagHunter Relevance

- `strategy_registry.web.ssti`：引入 parameter -> engine -> context -> capability 的流水线。
- `ObservationParser`：提取 Tplmap 风格的 capability 结果，帮助 agent 决定下一步。
- `Retrospective`：记录某引擎 / 上下文下哪些 capability 已被证伪。
