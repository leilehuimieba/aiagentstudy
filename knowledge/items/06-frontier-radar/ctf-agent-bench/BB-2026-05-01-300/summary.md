# [BB-2026-05-01-300] Summary

## Article

- Title: Language Agents as Hackers: Evaluating Cybersecurity Skills with Capture the Flag
- Source: OpenReview
- URL: https://openreview.net/forum?id=KOZwk7BFc3
- Date: 10-31
- Topic: `06-frontier-radar`
- Tags: ctf-benchmark, offensive-security, intercode-ctf, executable-environment, solve-rate

## Model Mapping

- Blocks: Goal, Context/State, Tools/Actions, Evaluation
- Layer: research

## Core Takeaway

InterCode-CTF 是最早把 CTF 任务做成可执行 benchmark 的代表性工作之一：作者把 100 个 PicoCTF 题目重建到 Docker 环境里，让 agent 通过 Bash / Python 与环境交互。论文报告 GPT-4 开箱即可解出 40/100 题，但在需要多步调查、切换策略和更强安全专长的题上明显掉队。作者还明确指出，模型遇到死路时常会重复相近命令，而不是主动换思路，这正好对应 FlagHunter 当前的 stop_no_progress 痛点。

## Reusable Principle

- 把题目做成可执行环境而不是静态问答，评测才会真实暴露多步推理与工具使用缺陷。
- 记录“卡死时重复了什么动作”比只记录最终 solved / unsolved 更有价值。
- 为每类题保留可重置的最小环境，便于后续 replay eval 和 failure reproduction。

## FlagHunter Relevance

- `ReplayEvalHarness`：可直接参考其“100 个任务 + 可执行 Docker 环境 + 自动判定 flag”的评测形态。
- `RecoveryController`：把“重复命令 / 小修小改重试”识别成死局信号，而不是简单累加步骤数。
- `HypothesisEngine`：为复杂题型设计显式的策略切换点，避免在单一路径上空转。
