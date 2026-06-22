# [BB-2026-05-01-304] Summary

## Article

- Title: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- Source: arXiv
- URL: https://arxiv.org/abs/2310.06770
- Date: 10-10
- Topic: `04-evaluation-guardrails`
- Tags: swe-bench, execution-based-eval, deterministic-replay, github-issues, software-agents

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

SWE-bench 的核心启发是：真实 agent 任务不能用字符串相似度来判对错，而要用“把改动应用到真实仓库后，测试是否通过”这种 execution-based 标准。对 FlagHunter 来说，这和“提交 flag 是否正确”“漏洞是否真的触发”是同一种评测哲学。它还说明了另一个关键点：benchmark 必须绑定具体环境状态，否则后续复现和回归都会失真。

## Reusable Principle

- 评测判定要依赖环境执行结果，而不是模型解释文本。
- 任务输入必须包含可复现的初始状态，避免回放时环境漂移。
- 回归评测要固定样本集与判分脚本，减少“看起来更聪明”的错觉。

## FlagHunter Relevance

- `ReplayEvalHarness`：FlagHunter 的判定标准应优先使用 execution-based success，而不是摘要式 judge。
- `FlagProof`：proof object 里应包含可复现的环境状态和验证命令。
- `Retrospective`：失败分析要基于真实执行结果，不要只看 final answer 文本。
