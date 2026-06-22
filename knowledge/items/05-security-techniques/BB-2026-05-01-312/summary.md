# [BB-2026-05-01-312] Summary

## Article

- Title: Server-Side Template Injection
- Source: PortSwigger Research
- URL: https://portswigger.net/research/server-side-template-injection
- Date: 08-05
- Topic: `05-security-techniques`
- Tags: ssti, template-engine, payload-design, engine-identification, rce

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation
- Layer: domain knowledge

## Core Takeaway

James Kettle 的这篇经典研究仍然是 SSTI 自动化探测最有用的源头之一，因为它把流程拆成了 Detect → Identify → Exploit 三段。对 FlagHunter 而言，最值得直接转成策略的，是“先用通用算术 payload 探测、再区分 plaintext context / code context、再做模板引擎识别”这条路径，而不是对所有参数盲打 payload 字典。它还覆盖了多种主流引擎和 sandbox escape 思路，非常适合做 strategy_registry 的基线策略。

## Reusable Principle

- SSTI 应先探测上下文，再探测引擎，最后再发 exploit payload。
- 通用算术 payload 比大而全字典更适合第一轮筛查。
- 对 text context 与 code context 必须分开判断和利用。

## FlagHunter Relevance

- `strategy_registry.web.ssti`：实现 Detect → Identify → Exploit 的三阶段策略。
- `ObservationParser`：把 49、报错栈、对象字符串化失败等信号结构化抽取出来。
- `HypothesisEngine`：根据上下文类型和引擎指纹动态切换后续 payload 家族。
