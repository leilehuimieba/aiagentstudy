# Claude Code 源码 / 公开实现分析专题

## 目标

这个专题用于集中管理 Claude Code 相关的三类材料：

1. **官方公开实现层**：GitHub 仓库、插件、commands、agents、skills、hooks、市场清单、官方文档。
2. **发布物与接口层**：npm wrapper、平台原生包、`sdk-tools.d.ts` 暴露出来的工具与任务接口。
3. **历史逆向与结构分析层**：BestBlogs 已收录的深度拆解文章，以及基于这些材料整理出的 agent runtime 认知框架。

## 当前结论（更新于 2026-05-26）

- `anthropics/claude-code` 官方仓库已经公开，但**不是完整核心 runtime 源码仓**。
- 当前 npm 包采用 **wrapper + native binary** 的发布模式；最新平台包以原生二进制形式分发。
- 因此，“Claude Code 源码分析”必须分层：
  - 能直接看代码的公开层
  - 能直接看接口的发布层
  - 历史逆向补充层
  - 基于三者交叉后的工程推断层

## 本地原始证据路径

- 官方仓库克隆：`D:\newwork\aiagentstudy\knowledge\raw\external\claude-code`
- npm 发布包解包：`D:\newwork\aiagentstudy\knowledge\raw\external\claude-code-npm`
- Hello-Agents 地基仓库：`D:\newwork\aiagentstudy\knowledge\raw\external\hello-agents`

## 推荐阅读顺序

### 先打地基

1. `BB-2026-05-01-326` — Hello-Agents 地基参考：从智能体定义到记忆、上下文、协议与评估

### 再看 Claude Code 结构分析

2. `BB-2026-05-01-325` — Claude Code 公开实现层 + 发布包 + 历史逆向材料综合分析：智能体是如何落地的？
3. `BB-2026-05-01-104` — Deep Dive: Claude Code Source Code
4. `BB-2026-05-01-205` — How Claude Code Agent Is Designed and Implemented

### 再看一个“对照实现”

5. `BB-2026-05-01-327` — Claw Code：一个对齐 Claude Code 产品表面的开源 Rust Agent Harness

### 最后看总图

6. `BB-2026-05-01-328` — Claude Code 风格智能体实现地图：从地基、官方表面到开源对照实现

### 从研究进入实现

7. `BB-2026-05-01-329` — 最小 Claude Code 风格开源实现蓝图：从研究结论到可开发主干

### 从研究进入实践

8. `BB-2026-05-01-330` — FlagHunter(PentestAgent) Agent 架构 vs Claw Code：逐层差距分析与改进路线

### Claude Code 相关已收录周边材料

- `BB-2026-05-01-016` — 构建 Claude Code 的经验教训：提示缓存至关重要
- `BB-2026-05-01-035` — Boris Cherny 与 Claude Code 的诞生
- `BB-2026-05-01-071` — 与 Boris Cherny 共同构建 Claude Code
- `BB-2026-05-01-075` — 在 Claude Code 中使用 Claude Opus 4.7 的最佳实践
- `BB-2026-05-01-143` — Claude Code 自动模式：一种更安全的跳过权限确认方式
- `BB-2026-05-01-171` — How Claude Code works in large codebases
- `BB-2026-05-01-172` — Agent view in Claude Code
- `BB-2026-05-01-187` — How Anthropic's cybersecurity team built a threat detection platform with Claude Code
- `BB-2026-05-01-210` — Claude Code Auto-Memory Feature Explained
- `BB-2026-05-01-231` — Claude Code Error Rate Drops from 41% to 11%

## 建议的研究问题

1. Claude Code 的 agent runtime，哪些部分是官方公开可证的？
2. 当前 native binary 发布形态下，哪些核心逻辑已经看不到源码？
3. 子代理、task、workflow、worktree、monitor 这些接口如何拼成一个长时程 coding agent？
4. Claude Code 的 memory / context / permissions，分别落在哪些控制面？
5. 如果用 Hello-Agents 的地基去复刻一个“Claude Code 风格”的开源 coding agent，最小必要组件是什么？
6. 如果没有官方完整 runtime，像 Claw Code 这样的对照实现能为我们补足哪些可观察的 harness 细节？
7. 如何把“地基原理、官方公开表面、开源对照实现”整合成一张可复用的 Claude Code 风格实现地图？
8. 如果今天开始自己实现，一个最小但结构正确的 Claude Code 风格开源主干，具体该先写哪些模块、按什么顺序做、每阶段怎么验收？
9. 如何用 claw-code 的架构洞察来改进一个已有但不完善的 agent 项目(如 FlagHunter/PentestAgent)？从哪些层开始改？

## 研究边界提醒

- 不要把当前 GitHub 仓库误认为完整 runtime。
- 不要把历史逆向材料误认为最新版事实。
- 先分清 **官方公开事实**、**历史逆向切片**、**工程推断**，再下结论。
