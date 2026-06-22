# Browser / Computer Use Agents 专题

## 目标

这个专题用于研究“让 agent 操作浏览器或电脑环境”的 runtime 问题，尤其适合：

1. 浏览器自动化、登录态复用、页面状态导出。
2. Browser-use / WebBridge / OpenCLI 这类工具层如何接入 agent loop。
3. 电脑使用 agent 的环境隔离、权限、状态、日志与验证。

## 推荐阅读顺序

### 先看浏览器运行时

1. `BB-2026-05-01-185` — Browser Use: Building a Runtime Harness for Agents
2. `BB-2026-05-01-184` — Kimi WebBridge: Let AI Operate Your Browser
3. `BB-2026-05-01-252` — Best practices for computer and browser use with Claude
4. `BB-2026-05-01-438` — Give your AI agent its own computer

### 再看工程化运行环境

5. `BB-2026-05-01-197` — Browser Run: now running on Cloudflare Containers
6. `BB-2026-05-01-396` — All Web, No CLI? How We Transformed StarAgent WebTerminal
7. `BB-2026-05-01-218` — bili-fe-workflow: Practices in Commercial Intelligent Development Workflow
8. `BB-2026-05-01-283` — Insights from the Codex Official Team: How to Maximize Codex's Potential

### 再看 harness 与对照实现

9. `BB-2026-05-01-022` — Harness Engineering 完全指南
10. `BB-2026-05-01-019` — 当我们在讨论 Harness 的时候，我们在讨论什么
11. `BB-2026-05-01-177` — Designing a Production-Grade Multi-Agent Harness from Scratch
12. `BB-2026-05-01-327` — Claw Code：一个开源 Rust Agent Harness
13. `BB-2026-05-01-328` — Claude Code 风格智能体实现地图
14. `BB-2026-05-01-412` — Reflections After a Harness Study!

## 建议的研究问题

1. 浏览器是普通 tool，还是需要独立 runtime/harness？
2. 登录态复用时，权限边界、敏感数据导出、截图和网络响应应该如何控制？
3. 浏览器任务失败时，应该保存哪些证据：DOM、可见文本、HTML、网络、console、截图？
4. Computer use agent 是否应该使用独立容器、远程桌面、浏览器 profile 或本机真实浏览器？
5. OpenCLI Browser Bridge 这种“复用真实登录状态”的方式，如何和本地知识库采集流程衔接？

## 本地查询入口

```powershell
.\kb.ps1 search "browser automation logged-in browser runtime harness" --expand-topic --limit 10
.\kb.ps1 pack "浏览器自动化 复用登录状态 导出 页面状态" --profile deep --grouped
.\kb.ps1 search "computer and browser use Claude" --topic 02-tools-actions --expand-topic
```

