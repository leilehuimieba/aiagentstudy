# Claude Code 公开实现层 + 发布包 + 历史逆向材料综合分析：智能体是如何落地的？

## 1. 先给结论

截至 **2026-05-26**，我们已经把 Claude Code 相关原始材料拉到本地，并可以明确区分三件事：

1. **`anthropics/claude-code` 官方 GitHub 仓库已经公开可见**，但它公开出来的主要是外围实现层：插件、命令、agents、hooks、工作流、示例、市场清单、安装说明等。
2. **npm 包 `@anthropic-ai/claude-code@2.1.150` 本体不是核心源码**，而是一个安装器/包装器；真正的 CLI 逻辑通过平台相关原生包分发，例如 `@anthropic-ai/claude-code-win32-x64`、`@anthropic-ai/claude-code-linux-x64`。
3. 因此，**Claude Code 当前并不是“完整开源的 TypeScript/Node 主实现”**。如果要做“源码级分析”，只能采取分层办法：
   - 对 **官方公开实现层** 做直接代码分析；
   - 对 **npm 发布接口与二进制分发形态** 做发布工程分析；
   - 对 **历史逆向材料** 做结构提炼，但明确标注其历史性与不完全可验证性。

这意味着：今天我们能非常扎实地回答“Claude Code 这个智能体系统是怎样被工程化落地的”，但**不能把当前 GitHub 仓库误判为完整主 runtime 源码**。

---

## 2. 本次落库的证据层

### 2.1 官方公开仓库层

本地路径：`D:\newwork\aiagentstudy\knowledge\raw\external\claude-code`

已验证事实：

- GitHub 仓库：`https://github.com/anthropics/claude-code`
- 默认分支：`main`
- 当前抓取提交：`39e853e4074d90f27afdfb7ea601e0fc378bd0c5`
- 当前抓取标签：`v2.1.150`
- 最近公开更新时间（GitHub 元数据）：`2026-05-26T04:19:47Z`

这个仓库公开出来的不是一个传统意义上的 `src/` 主代码仓，而是围绕 Claude Code 的**公开扩展生态**，重点包含：

- `.claude/commands/`：内置 slash commands 示例
- `plugins/`：官方插件集合
- `.claude-plugin/marketplace.json`：插件市场清单
- `examples/`：hooks、settings、MDM 管理样例
- `scripts/`：围绕 issue / workflow / 自动化的脚本
- `.github/workflows/`：使用 Claude 进行 issue triage、去重、审查等自动化流程

**直接含义**：Claude Code 官方正在公开的，不是“底层推理循环实现细节”，而是**如何把 Claude Code 当成一个可扩展智能体平台来用**。

### 2.2 npm 发布包层

本地路径：`D:\newwork\aiagentstudy\knowledge\raw\external\claude-code-npm`

已验证事实：

- wrapper 包：`@anthropic-ai/claude-code@2.1.150`
- tarball：`https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-2.1.150.tgz`
- wrapper 解包后仅 7 个文件，核心文件是：
  - `install.cjs`
  - `cli-wrapper.cjs`
  - `sdk-tools.d.ts`
  - `bin/claude.exe`（占位 stub）
- 平台原生包大小：
  - `@anthropic-ai/claude-code-win32-x64` 解包约 **234 MB**
  - `@anthropic-ai/claude-code-linux-x64` 解包约 **238 MB**

`install.cjs` 与 `cli-wrapper.cjs` 清楚暴露出 Claude Code 的当前发布策略：

- wrapper 负责 **平台识别**；
- 从 optionalDependencies 中解析对应平台包；
- 把原生二进制落到 `bin/claude.exe`；
- 最终 CLI 执行的是 **native binary**，不是长期驻留的 Node 进程。

**直接含义**：当下最新版本的 Claude Code 核心 runtime 位于平台二进制中，而不是这个公开 wrapper 包里。

### 2.3 官方文档 / 公开接口层

可以直接验证到的公开接口包括：

- 插件系统：commands / agents / skills / hooks / MCP server
- 多代理 / 子代理能力：从插件示例与类型定义可见
- 任务与后台执行：从 `sdk-tools.d.ts` 可见 `TaskCreate` / `TaskGet` / `TaskUpdate` / `TaskList` / `TaskStop`
- REPL、WebSearch、WebFetch、Worktree、Cron、Monitor、PushNotification 等工具能力
- 计划模式 / 问答模式 / 工作树模式等宿主控制接口

这意味着，即便没有完整 runtime 源码，**Claude Code 对外暴露的 agent 能力面已经足够厚，可以反推出它的系统轮廓**。

### 2.4 历史逆向材料层

本地已有两篇关键深度材料：

- `D:\newwork\aiagentstudy\knowledge\items\01-context-memory\BB-2026-05-01-104\article.md`
- `D:\newwork\aiagentstudy\knowledge\items\03-control-loop\BB-2026-05-01-205\article.md`

这两篇材料的价值不是“绝对等于今天最新版源码”，而是：

- 它们补齐了当前官方公开层没有暴露的 runtime 细部；
- 它们把 Claude Code 看作一个 **agent runtime / harness**，而非单一模型封装；
- 它们与当前公开接口层之间存在高度结构对应关系，因此仍然具备研究价值。

但必须强调：**这部分属于“历史逆向层”，不能和“今天官方公开仓库”混为一谈。**

---

## 3. Claude Code 到底是怎么实现“智能体”的？

下面的分析按照“证据强度”分层展开：

- **[官方公开可证]**：直接来自当前 GitHub 仓库、npm 包、类型定义、官方文章
- **[历史逆向支持]**：来自既有逆向材料，与当前公开接口相互印证
- **[综合推断]**：基于前两者做出的工程级推断

### 3.1 它不是一个“会聊天的 CLI”，而是一个宿主式 agent runtime

**[官方公开可证]**

从 `sdk-tools.d.ts` 可以直接看到，Claude Code 内部世界并不只有 `Bash`、`Read`、`Write` 这类基础工具，还包括：

- `Agent`
- `TodoWrite`
- `TaskCreate` / `TaskGet` / `TaskUpdate` / `TaskList` / `TaskStop`
- `EnterPlanMode` / `ExitPlanMode`
- `REPL`
- `Workflow`
- `ScheduleWakeup`
- `Monitor`
- `PushNotification`
- `EnterWorktree` / `ExitWorktree`
- `WebSearch` / `WebFetch`
- `Mcp` / `ListMcpResources` / `ReadMcpResource`

如果一个系统只是在终端里调用模型，它不需要这么厚的宿主工具面。Claude Code 暴露出这些接口，说明它管理的是一个**跨多轮、多任务、可中断、可恢复、可分派**的执行环境。

**[综合推断]**

所以 Claude Code 的系统本体应理解为：

> 一个把大模型接入代码库、工具链、任务系统、上下文系统、权限系统后的“宿主型智能体运行时”。

模型只负责生成决策；真正把决策转成可靠工作流的是宿主层。

### 3.2 它的能力面不是一次性全开，而是分层暴露

**[官方公开可证]**

GitHub 仓库的公开插件结构已经非常清晰：

```text
plugin-name/
├── .claude-plugin/
├── commands/
├── agents/
├── skills/
├── hooks/
├── .mcp.json
└── README.md
```

`plugins/README.md` 还明确说明 Claude Code 插件可以扩展：

- custom slash commands
- specialized agents
- hooks
- MCP servers
- skills

`.claude-plugin/marketplace.json` 则证明这些插件会被当作一个“市场/包生态”来组织和分发。

**[综合推断]**

这代表 Claude Code 不是“把所有 prompt、所有工具、所有行为硬编码进一个大系统提示词”，而是采用了 **能力面（capability surface）分层暴露** 的策略：

- 基础通用能力：文件读写、shell、搜索、网络
- 结构化工作流能力：plan、todo、task、workflow
- 外挂能力：MCP servers
- 行为约束与人格化能力：skills、hooks、output style plugins
- 任务分工能力：specialized agents / subagents

这和很多 demo 级 agent 最大的不同在于：**Claude Code 把“暴露什么能力给模型看”本身当成了一等工程问题。**

### 3.3 它内建多代理思维，而不是只做单代理回路

**[官方公开可证]**

插件示例已经公开展示了 Claude Code 的多代理使用方式：

- `feature-dev` 插件里，会在不同阶段启动 `code-explorer`、`code-architect`、`code-reviewer`
- `code-review` 插件 README 里明确写了“launches multiple agents in parallel”
- 类型定义里的 `AgentInput` 也说明子代理可以带：
  - `subagent_type`
  - `run_in_background`
  - `name`
  - `team_name`
  - `mode`
  - `isolation: "worktree"`

这已经不是“单个 agent 偶尔 call tool”的范式，而是：

- 可以把任务拆给不同专长代理
- 可以并行执行
- 可以后台运行
- 可以在 worktree 隔离环境中执行

**[历史逆向支持]**

历史逆向材料进一步把这种多代理能力描述为一套更完整的任务/会话/恢复结构，而不仅是“多开几个子会话”。

**[综合推断]**

Claude Code 的“智能体”实现并不是把多代理当高级可选项，而是把它纳入主系统设计：

- 单代理负责当前 turn 的 reasoning + routing
- 子代理承担探索、审查、验证、专项执行
- 宿主层负责调度、隔离、回收与结果汇总

这解释了为什么它在大代码库和长任务里表现更像“团队调度器”，而不是一个单纯聊天补全器。

### 3.4 它的“记忆”更多是外化工件，而不是神秘的隐式长期记忆

**[官方公开可证]**

你库里已有的官方材料早就提到 Claude Code 的几个关键扩展点：

- `CLAUDE.md`
- hooks
- skills
- plugins
- MCP servers
- 在大代码库场景下强调 layered `CLAUDE.md`

这些设计的共同点是：**把长期稳定知识外化到文件/配置/插件，而不是全部寄希望于对话历史。**

**[历史逆向支持]**

逆向材料把这条路线讲得更彻底：连续性并不只靠 transcript，而是分散在 memory files、session state、task state、content replacement records、logs 等外化工件中。

**[综合推断]**

因此 Claude Code 的 memory / context 策略更接近：

1. 把项目级稳定知识沉淀成显式工件（如 `CLAUDE.md`）
2. 把行为策略沉淀成 skills / hooks / plugins
3. 把任务推进状态沉淀成 todo / task / worktree / workflow
4. 把需要恢复的会话状态放入宿主层结构中

这是一种**工程化长期记忆**，而不是“模型自动记住一切”。

### 3.5 它的控制循环核心，不是提示词，而是“任务推进 + 工具中介 + 恢复”

**[官方公开可证]**

从暴露工具可以看出 Claude Code 至少有以下几个宿主控制子系统：

- 计划系统：`EnterPlanMode` / `ExitPlanMode`
- 任务系统：`Task*`
- 后台与唤醒：`Monitor` / `ScheduleWakeup` / `PushNotification`
- 工作流系统：`Workflow`
- 隔离执行环境：`EnterWorktree` / `ExitWorktree`
- 代码执行环境：`Bash` / `REPL`

这说明 Claude Code 的控制循环远超“LLM 说一句，shell 执行一句”。

**[历史逆向支持]**

逆向材料把这一层进一步刻画为：

- turn engine
- tool mediation
- compact / continue / recovery
- cache 与 transcript 不变量维护

**[综合推断]**

所以 Claude Code 的主循环更像：

```text
用户目标
-> 宿主准备上下文
-> 模型推理/规划
-> 选择工具或子代理
-> 执行并观察
-> 记录任务状态 / 产物 / 记忆
-> 判断继续、压缩、恢复、暂停或结束
```

这和 `hello-agents` 的基础 loop：

`Goal -> Context/State -> Reasoning/Planning -> Tool Action -> Observation -> Update -> Deliverable`

在结构上是完全对齐的，只是 Claude Code 把每个节点都做成了可工程化的控制面。

### 3.6 它的安全边界来自权限面与 hook 面，而不是只靠模型“自觉”

**[官方公开可证]**

从公开插件可以直接看到安全/约束机制已经被产品化：

- `security-guidance`：在 PreToolUse 阶段扫描危险模式
- `hookify`：允许通过规则创建自定义 hooks，阻止不期望行为
- `learning-output-style` / `explanatory-output-style`：说明会话启动时可以注入行为约束与输出偏好
- `AgentInput.mode` 说明子代理存在不同权限模式，例如 `plan`、`auto`、`bypassPermissions` 等

这意味着 Claude Code 的 guardrails 并不只有模型系统提示，而是**通过 hooks + mode + host permission policy** 实现。

**[综合推断]**

生产级 coding agent 的安全边界至少包括：

- 执行前拦截
- 模式化权限控制
- 工作目录/工作树隔离
- 工具白名单与参数约束
- 用户确认与恢复流程

Claude Code 的公开接口正好对应这些需求。

### 3.7 它已经把“可观测性”内建成系统需求

**[历史逆向支持]**

历史逆向材料里最值得注意的一点，是 Claude Code 并不满足于“能跑通”；它还会追踪：

- query pipeline 阶段耗时
- cache 何时失效
- 上下文究竟被什么吃掉
- tool execution 起止

**[官方公开接口侧印证]**

虽然当前公开 GitHub 仓库没有完整 profiler 主实现，但 `Task*`、`Workflow`、`Monitor`、`PushNotification` 这些接口已经说明 Claude Code 并不是黑盒单轮调用，而是一个需要向宿主和用户报告状态的长任务系统。

**[综合推断]**

这代表 Claude Code 作为 agent，不只是“会做事”，还追求“能解释自己在做什么、卡在哪里、何时需要人参与”。

---

## 4. 为什么说它本质上是 Harness，而不是 Prompt 技巧？

结合当前公开层与历史逆向层，Claude Code 最重要的启发是：

> 它把“模型”降格成系统中的一个决策引擎，而把真正复杂的部分放在 harness 上。

这个 harness 至少包含：

- **宿主循环**：一次任务如何推进、暂停、恢复
- **上下文管理**：哪些文件、记忆、规则、产物进入上下文
- **工具中介**：什么工具可见、如何选择、如何安全执行
- **任务管理**：todo、task、workflow、background agent
- **多代理编排**：子代理并行、隔离、命名、团队化
- **策略层**：hooks、permission mode、安全提醒
- **可观测性**：进度、通知、监控、profile、回放

这也是为什么它能被称为“agentic coding tool”，而不仅是“终端里的 Claude”。

---

## 5. 与 Hello-Agents 地基知识怎么对齐？

为了不让 Claude Code 分析只停留在“看起来很酷的内部实现”，我们把它映射回通用智能体框架：

| Hello-Agents 地基概念 | Claude Code 对应实现 |
| --- | --- |
| Goal | 用户自然语言目标、slash command 工作流、workflow 入口 |
| Context/State | `CLAUDE.md`、skills、plugins、任务状态、代码库现场 |
| Reasoning/Planning | plan mode、分阶段插件工作流、子代理架构 |
| Tools/Actions | Bash、Read/Write、Web、MCP、REPL、Task 等工具面 |
| Observation | tool output、任务状态、监控、通知、审查结果 |
| Update | todo/task 更新、worktree 产物、记忆外化、插件/技能沉淀 |
| Deliverable | 代码修改、PR review、文档、报告、工作流输出 |
| Evaluation/Guardrails | hooks、security guidance、模式权限、审查代理 |

也就是说，Claude Code 并没有发明一套神秘的新智能体原理，它做的是：**把通用 agent loop 做成能在真实代码生产场景里长期工作的工程系统。**

---

## 6. 这次研究最重要的“反误区”

### 误区 1：GitHub 仓库公开了，所以 Claude Code 已经完整开源

不是。

公开的是：插件生态、工作流、示例、外部接口与发布外壳。核心 runtime 目前仍以 native binary 形式分发。

### 误区 2：只要会写系统提示词，就等于会做 Claude Code 级智能体

不是。

Claude Code 真正稀缺的部分，在于：

- 状态如何持久化
- 长任务如何推进
- 子代理如何协作
- 工具面如何管理
- 权限如何兜底
- 如何避免上下文失控

### 误区 3：逆向材料等于今天最新版实现

不是。

逆向材料更像是“结构切片”，对理解 runtime blueprint 很有帮助，但必须和当前公开事实分层使用。

---

## 7. 当前最稳的研究结论

可以较高置信度保留的结论是：

1. **Claude Code 是宿主型 agent runtime，不是简单 CLI 包装器。**
2. **它把能力面、上下文面、任务面、权限面、多代理面分成独立控制面。**
3. **它通过插件/skills/hooks/MCP 把静态能力变成可演化能力。**
4. **它的记忆策略以外化工件为主，而不是依赖模型隐式长期记忆。**
5. **它的工程重点不是“让模型更会想”，而是“让系统在长程工作中不失控”。**

---

## 8. 下一步建议

如果继续深挖 Claude Code，我建议按下面顺序推进：

1. **读公开实现层**
   - `plugins/README.md`
   - `plugins/feature-dev/README.md`
   - `plugins/code-review/README.md`
   - `.claude-plugin/marketplace.json`
   - `sdk-tools.d.ts`

2. **对照历史逆向材料**
   - `BB-2026-05-01-104`
   - `BB-2026-05-01-205`

3. **回到地基知识**
   - `BB-2026-05-01-326`（本次新增的 Hello-Agents 地基参考）

4. **如果要继续逼近最新 runtime**
   - 对 `v2.1.150` 平台包做黑盒行为测试
   - 观察 tool schema、task lifecycle、worktree、monitor、workflow 的运行时行为
   - 重点关注是否仍保留历史逆向材料中描述的那些不变量：上下文压缩、恢复流程、任务持久化、多代理分工

---

## 9. 一句话总结

Claude Code 的精髓不在“它能调用 Claude”，而在于：

> 它把一个大模型包进了可扩展的工具面、可恢复的任务面、可治理的上下文面和可控的权限面，从而把“会生成代码”升级成了“能长期稳定干活的 coding agent”。
