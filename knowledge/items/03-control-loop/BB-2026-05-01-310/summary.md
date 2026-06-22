# [BB-2026-05-01-310] Summary

## Article

- Title: CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing
- Source: arXiv
- URL: https://arxiv.org/abs/2305.11738
- Date: 05-19
- Topic: `03-control-loop`
- Tags: self-correction, tool-feedback, critique-loop, wrong-answer, validation

## Model Mapping

- Blocks: Tools/Actions, Evaluation, Memory
- Layer: research

## Core Takeaway

CRITIC 的价值在于把“发现自己错了”这件事工具化：先产出答案，再调用工具验证，再根据反馈修正。它不是笼统地要求 agent 自我反省，而是要求每一步批判都拿到外部证据。对 FlagHunter 来说，这比单纯的 chain-of-thought 更关键，因为 web / pwn / crypto 的 wrong flag、错误 exploit、误读响应，最需要的是 runtime feedback 驱动的纠偏。

## Reusable Principle

- 先生成候选，再用工具批判，不要把验证和生成混成一步。
- 自我修正必须依赖外部反馈，而不是纯文本自说自话。
- 把验证失败原因显式编码回下一轮提示和状态。

## FlagHunter Relevance

- `RecoveryController`：wrong-flag 后先调用验证工具链解释失败，再决定下一个动作。
- `FlagProof`：把 external critique 结果写入 proof object，区分 source-only 与 runtime-triggered。
- `HypothesisEngine`：候选 exploit 应带验证计划，失败后自动回传 critique。
