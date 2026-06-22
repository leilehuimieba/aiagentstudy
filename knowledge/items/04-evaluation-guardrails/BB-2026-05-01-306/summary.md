# [BB-2026-05-01-306] Summary

## Article

- Title: OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
- Source: arXiv
- URL: https://arxiv.org/abs/2404.07972
- Date: 04-11
- Topic: `04-evaluation-guardrails`
- Tags: osworld, execution-based-eval, desktop-agents, state-setup, reproducibility

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

OSWorld 把“任务 setup + 执行 + 自动判分脚本”三件事打包成统一环境，是 replay eval 设计里很强的参考样板。它的关键价值在于每个任务都绑定详细初始状态配置和自定义 execution-based evaluator，因此失败不是一句“没做对”，而是能回到具体环境重放。论文中 best model 12.24% 对 humans 72.36% 的落差，也提醒我们：复杂环境下 agent 质量会被 UI grounding、操作知识和状态漂移同时拉低。

## Reusable Principle

- 每个任务都应保存 setup config，回放才能真正同态。
- execution-based evaluator 应当和任务一起版本化。
- 失败归因必须绑定环境状态，而不是只绑定模型回复。

## FlagHunter Relevance

- `ReplayEvalHarness`：非常适合参考其 initial-state setup + custom evaluator 脚本模式。
- `FlagProof`：proof object 应记录 challenge 初始状态、操作序列与验证脚本。
- `Retrospective`：把 GUI / protocol / environment drift 当成独立失败层归因。
