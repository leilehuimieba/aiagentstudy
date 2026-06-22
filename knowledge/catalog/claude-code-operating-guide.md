# Claude Code Operating Guide 专题

## 目标

这个专题不是源码考古入口，而是用于回答“Claude Code / Claude Code 风格 agent 怎么用、怎么控、怎么评估”的操作型问题。

如果问题是源码、发布包、公开实现和逆向材料，请优先读 `claude-code-source-analysis.md`。

## 推荐阅读顺序

### 先看使用与上下文

1. `BB-2026-05-01-171` — How Claude Code works in large codebases
2. `BB-2026-05-01-016` — 构建 Claude Code 的经验教训：提示缓存至关重要
3. `BB-2026-05-01-210` — Claude Code Auto-Memory Feature Explained
4. `BB-2026-05-01-231` — Claude Code Error Rate Drops from 41% to 11%

### 再看权限与 auto mode

5. `BB-2026-05-01-143` — Claude Code 自动模式：一种更安全的跳过权限确认方式
6. `BB-2026-05-01-357` — Safer Than YOLO: Auto Mode for Exec Approvals
7. `BB-2026-05-01-445` — Harness Engineering-Based Business Agent Evaluation Scheme Using Top-Tier Agent

### 再看实现地图与对照

8. `BB-2026-05-01-104` — Deep Dive: Claude Code Source Code
9. `BB-2026-05-01-205` — How Claude Code Agent Is Designed and Implemented
10. `BB-2026-05-01-325` — Claude Code 公开实现层 + 发布包 + 历史逆向材料综合分析
11. `BB-2026-05-01-327` — Claw Code：一个对齐 Claude Code 产品表面的开源 Rust Agent Harness
12. `BB-2026-05-01-328` — Claude Code 风格智能体实现地图

### 最后看生态对照

13. `BB-2026-05-01-375` — How CodeRabbit Used Claude to Build an Agent Orchestration System
14. `BB-2026-05-01-404` — DeepSeek Takes a Mixue-Style Approach to Build China's Version of Claude Code
15. `BB-2026-05-01-410` — Hands-on with Claude Opus 4.8

## 建议的研究问题

1. Claude Code 在大代码库里为什么需要目录规则、记忆和上下文预算？
2. auto mode 和 YOLO 模式的关键区别是什么？
3. 权限确认应该按命令、参数、路径、历史行为还是风险等级分类？
4. 如何把 Claude Code 的用法经验转化成自己的 agent harness 规则？
5. Claude Code 的评估应该看完成率、错误率、回滚能力，还是开发者可控感？

## 本地查询入口

```powershell
.\kb.ps1 search "Claude Code auto mode source large codebases harness" --limit 10
.\kb.ps1 pack "Claude Code auto mode 权限 证据 来源" --profile auto --grouped
.\kb.ps1 search "Claude Code large codebases memory instructions" --topic 01-context-memory --expand-topic
```

