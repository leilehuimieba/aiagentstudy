# [BB-2026-05-01-309] Summary

## Article

- Title: Reflexion: Language Agents with Verbal Reinforcement Learning
- Source: OpenReview
- URL: https://openreview.net/forum?id=vAElhFcKW6
- Date: 09-21
- Topic: `03-control-loop`
- Tags: reflection, verbal-rl, episodic-memory, retry, failure-recovery

## Model Mapping

- Blocks: Context/State, Evaluation, Memory
- Layer: research

## Core Takeaway

Reflexion 的核心思想非常适合 wrong-flag 后恢复：不是去改模型权重，而是把失败反馈写成语言化经验，存进 episodic memory，下一轮显式利用。它证明了“失败后总结一句可执行的教训”本身就是一种可扩展的控制机制。FlagHunter 当前恢复路径偏粗糙，如果能把 wrong flag、无效 payload、误判线索都沉淀成 verbal reflection，下一次切分支时就会更精准。

## Reusable Principle

- 失败后立即形成短小、可执行、可检索的 verbal reflection。
- 记忆应该是“如何避免重复犯错”，而不只是历史记录。
- 重试前先消费 reflection，再决定下一步动作。

## FlagHunter Relevance

- `RecoveryController`：wrong-flag 后生成面向下一轮的反思条目。
- `strategy_memory`：把失败 payload、误导线索、已证伪假设写成可检索负反馈。
- `HypothesisEngine`：新假设排序时要显式参考过往 verbal reflection。
