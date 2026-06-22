# [BB-2026-05-01-313] Summary

## Article

- Title: Server-side template injection
- Source: Web Security Academy
- URL: https://portswigger.net/web-security/server-side-template-injection
- Date: 05-24
- Topic: `05-security-techniques`
- Tags: ssti, labs, context-detection, object-chain, exploitation-workflow

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation
- Layer: domain knowledge

## Core Takeaway

Web Security Academy 的价值在于把 PortSwigger 的研究论文落实成了可执行方法学：从 fuzzing 特殊字符，到按上下文探测，再到识别引擎、阅读文档、探索对象链、构造自定义攻击。相比纯研究文章，它更适合直接转成 agent 的分步策略和实验清单。对 FlagHunter 的 web 题来说，这相当于一份 SSTI strategy playbook。

## Reusable Principle

- 先 fuzz 特殊字符，再做 context-specific probe。
- 引擎识别后要立刻切到文档 / 对象链 / 开发者对象三条利用路径。
- SSTI 探测应该显式区分“有异常”“有求值”“可对象遍历”三类证据。

## FlagHunter Relevance

- `strategy_registry.web.ssti`：可直接映射成 agent 的分步 checklist。
- `FlagProof`：把 fuzz 异常、数学表达式求值、对象链访问等证据分层记录。
- `RecoveryController`：某条利用链失败后，切换到 developer-supplied objects 或 custom attack 分支。
