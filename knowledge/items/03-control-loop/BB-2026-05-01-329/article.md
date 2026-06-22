# 最小 Claude Code 风格开源实现蓝图：从研究结论到可开发主干

## 1. 目标：我们到底要实现什么

这份蓝图要解决的问题不是：

- “怎么做一个聊天框能调用几个工具”
- “怎么长得像 Claude Code”
- “怎么尽快把功能菜单补齐”

而是：

> **如何实现一个最小但结构正确的 Claude Code 风格 agent harness，使它能够稳定完成多轮代码任务，并且后续能自然长出 task、subagent、MCP、plan mode、hooks 等能力。**

所以这里的“最小实现”指的是：

- 控制循环要成立
- 工具控制面要成立
- 权限门要成立
- 长任务上下文治理要成立
- 后续扩展点要预留

而不是：

- 所有产品功能都做完
- UI、IDE、市场、MCP、插件一次性全上

---

## 2. 非目标：这一版明确不做什么

为了保证主干收口，第一版蓝图明确**不把这些东西当首发阻塞项**：

- IDE bridge
- 插件市场
- 完整 MCP transport 矩阵
- 多 worker fleet / team orchestration
- 复杂 proactive agent
- 远程触发平台
- 花哨终端 UI
- 细粒度 provider 路由优化

这些都可以后置。

第一版只要求：**能稳定做真实 coding task，并且结构上不像 demo。**

---

## 3. Harness 判断：最小主干必须包含哪些层

根据前面几篇条目的综合结论，最小 Claude Code 风格主干必须包含八层：

1. **Goal Framing**
2. **Control Loop**
3. **Session / Context State**
4. **Tool Registry + Dispatch**
5. **Permission Gate**
6. **Memory / Compaction / Artifact**
7. **Task / Subagent 基础能力**
8. **Verification / Telemetry**

如果少了第 4、5、6 层，它就很容易退化成：

- “一个会调用 bash 的聊天程序”

而不是：

- “一个可治理的 coding agent runtime”

---

## 4. 建议的最小目录骨架

下面给一个**语言无关但偏 Rust/TS 都能落地**的模块划分。  
重点是职责边界，不是语法。

```text
agent-harness/
├── cli/
│   ├── main            # CLI 入口 / prompt / resume / doctor
│   ├── repl            # 交互壳；只负责输入输出，不承载业务
│   └── render          # 文本渲染 / tool call 展示 / status
│
├── runtime/
│   ├── conversation    # 控制循环：run_turn / stream events / tool roundtrip
│   ├── session         # message history / session persistence / resume
│   ├── prompt          # system prompt assembly / model request building
│   ├── compact         # context compaction / summary / token budget
│   ├── permissions     # PermissionPolicy / mode / confirm contract
│   ├── hooks           # pre/post tool hooks / lifecycle hooks
│   ├── usage           # token / cost / turn counters
│   └── tracing         # session trace / structured events
│
├── tools/
│   ├── spec            # ToolSpec / schema / permission metadata
│   ├── registry        # builtin tools / runtime tools / search / allowed set
│   ├── dispatch        # execute_tool / parse input / normalize result
│   ├── file_ops        # read/write/edit/notebook
│   ├── search          # glob / grep / code search
│   ├── shell           # bash / powershell / sandbox / timeout
│   ├── web             # web fetch / web search
│   ├── plan            # todo / enter plan mode / exit plan mode / structured output
│   └── agent_task      # Agent / Task / Worker / Team / Cron surfaces
│
├── memory/
│   ├── claude_md       # project memory / instructions loading
│   ├── summaries       # compact summaries / handoff artifacts
│   └── retrieval       # optional retrieval / future RAG integration
│
├── integrations/
│   ├── provider        # Anthropic / OpenAI-compatible client abstraction
│   ├── mcp             # MCP registry bridge / lifecycle
│   ├── lsp             # LSP registry / semantic tool dispatch
│   └── plugin          # plugin / skill loading
│
├── tasking/
│   ├── registry        # task lifecycle
│   ├── subagent        # delegated runtime / manifest / allowed tools
│   └── packets         # task packet / handoff payload
│
├── tests/
│   ├── loop            # end-to-end turn loop tests
│   ├── permissions     # risk gating / path scope / shell checks
│   ├── session         # compact / resume / persistence
│   ├── tasking         # task registry / subagent lifecycle
│   └── parity          # mock provider parity harness
│
└── docs/
    ├── architecture    # runtime map / contracts
    ├── commands        # CLI / slash command surface
    └── verification    # regression / eval checklist
```

### 这套骨架的关键原则

- **REPL 不承载核心业务**
- **tool spec / registry / dispatch 分离**
- **permission 单独成层**
- **session / compact 不和 CLI 混在一起**
- **subagent / task 从一开始就留位置**
- **hooks / tracing 从一开始预留插槽**

---

## 5. 冻结实现面：第一版应该落到哪些具体模块

按 `plan-agent-implementation` 的要求，先把实现面冻结成可操作模块。

### 第一阶段必做模块

1. `runtime/conversation`
   - 单轮 turn loop
   - tool_use roundtrip

2. `runtime/session`
   - message history
   - session save/load

3. `tools/spec`
   - 工具元数据
   - schema
   - required permission

4. `tools/registry`
   - builtin tool list
   - allowed tools 过滤

5. `tools/dispatch`
   - tool name → input parse → run handler

6. `tools/file_ops`
   - read / write / edit

7. `tools/search`
   - glob / grep

8. `tools/shell`
   - bash

9. `runtime/permissions`
   - read-only / workspace-write / full-access
   - confirm contract

10. `cli/main` + `cli/repl`
   - prompt
   - interactive loop

### 第二阶段必做模块

11. `runtime/compact`
12. `runtime/usage`
13. `tools/plan`
14. `memory/claude_md`
15. `tasking/registry`
16. `tasking/subagent`

### 第三阶段再做

17. `integrations/mcp`
18. `integrations/lsp`
19. `integrations/plugin`
20. `runtime/hooks`
21. `runtime/tracing`

这样能避免一开始把系统摊成一个巨大 blob。

---

## 6. 分阶段实现路线

下面是推荐的开发顺序。

## 阶段 0：先写合同，不急着写满功能

### 目标
把 runtime 的几个核心 contract 先固定下来。

### 必须产出的接口

- `ConversationRuntime.run_turn(input)`
- `ToolSpec`
- `ToolExecutor.execute(name, input)`
- `PermissionPolicy.authorize(tool, input)`
- `Session.save/load`

### 验证

- 能否在不接真实 provider 的前提下，用 mock provider 跑通一轮：
  - user → assistant(tool_use) → tool_result → assistant(final)

### 成功标准

- 已经有“运行时壳”
- 还没有任何 UI 依赖
- mock 测试可跑

---

## 阶段 1：控制循环最小闭环

### 目标
先把 agent loop 做成，而不是先把工具堆满。

### 范围

- `runtime/conversation`
- `runtime/session`
- `cli/main`
- `cli/repl`

### 必须支持

- 用户输入进入 session
- 发起模型请求
- 流式或伪流式组装 assistant message
- 识别 `tool_use`
- 写回 `tool_result`
- 继续下一轮直到终止

### 验证

- mock provider 测试：
  - 一轮纯文本响应
  - 一轮单工具调用
  - 多轮工具调用后输出 final text
- 死循环保护：
  - `max_iterations` 触发测试

### 成功标准

- 这是系统第一个真正“像 agent”的节点

---

## 阶段 2：最小工具控制面

### 目标
把工具从“散装函数”收口到统一 surface。

### 范围

- `tools/spec`
- `tools/registry`
- `tools/dispatch`
- `tools/file_ops`
- `tools/search`
- `tools/shell`

### 首发工具集合

- `read_file`
- `write_file`
- `edit_file`
- `glob_search`
- `grep_search`
- `bash`

### 设计要求

- 每个工具必须有：
  - name
  - schema
  - required permission
  - normalized result

### 验证

- schema 错误能明确返回
- tool name 未命中能明确报错
- read/write/search/bash 都有最小端到端测试

### 成功标准

- “工具面”已经可以被模型稳定调用

---

## 阶段 3：权限门先于高级能力

### 目标
在加 plan、task、subagent 之前，先把高风险动作收紧。

### 范围

- `runtime/permissions`
- `tools/dispatch` 中的 permission hook

### 最小模式

- `read-only`
- `workspace-write`
- `danger-full-access`

### 至少要做的风险分类

- read_file / glob / grep → read-only
- write/edit → workspace-write
- bash → 动态判定
  - 只读命令可 lower
  - 写命令或危险命令升到更高模式
- workspace 外路径直接升级风险或拒绝

### 验证

- 路径越界测试
- bash 读写分类测试
- write denied / write allowed 测试
- no prompt / prompt confirm 两条路径测试

### 成功标准

- agent 已经不再只是“能执行”，而是“可控地执行”

---

## 阶段 4：长任务治理——session、compact、artifact

### 目标
让系统开始能做长任务，不因上下文爆炸而立即失效。

### 范围

- `runtime/compact`
- `memory/summaries`
- `runtime/usage`

### 必做能力

- token / turn usage tracking
- compact trigger threshold
- compact summary artifact
- 大工具输出外置成 artifact 文件

### 验证

- 构造大上下文测试，确认达到阈值后 compact 触发
- compact 后 session 仍能继续运行
- 大输出结果不会直接塞爆上下文

### 成功标准

- 这是从 demo agent 到实用 agent 的关键跃迁

---

## 阶段 5：计划能力与结构化交付

### 目标
补上 Claude Code 风格 agent 很关键的“先规划再执行”能力。

### 范围

- `tools/plan`
- `memory/claude_md`

### 首发能力

- `TodoWrite`
- `StructuredOutput`
- `EnterPlanMode`
- `ExitPlanMode`
- `CLAUDE.md` / project memory 读取

### 设计要求

- plan mode 不是一条 prompt 文案，而是宿主状态
- todo 是结构化对象，不是字符串列表

### 验证

- 进入 / 退出 plan mode 的状态测试
- todo 更新回放测试
- structured output 空 payload / 正常 payload 测试

### 成功标准

- 系统开始具备“任务拆解与结构化交付”能力

---

## 阶段 6：子代理与任务底座

### 目标
让系统能把任务拆出去，而不是所有东西都堵在一个 loop 里。

### 范围

- `tasking/registry`
- `tasking/subagent`
- `tools/agent_task`

### 首发能力

- `TaskCreate / Get / List / Update / Stop`
- `Agent`
- task packet / handoff artifact
- subagent allowed tools 白名单

### 设计要求

- sub-agent 必须是独立 runtime 或独立执行体
- 不是简单“再发一个 prompt”
- 任务状态必须可读、可停、可看输出

### 验证

- subagent spawn 成功测试
- task registry 生命周期测试
- allowed-tools 限制测试
- 子任务完成后 manifest / output artifact 检查

### 成功标准

- 系统正式从单体 agent 走向可拆分 agent

---

## 阶段 7：协议扩展——MCP / LSP / plugin

### 目标
不再只靠内置工具箱。

### 范围

- `integrations/mcp`
- `integrations/lsp`
- `integrations/plugin`

### 推荐顺序

1. 先 MCP registry bridge
2. 再 LSP registry + dispatch
3. 最后 plugin / skill loading

### 原则

- 先做 bridge，不急着一开始打磨所有 transport
- 先做 registry，不急着一次实现全部下游 runtime 深度

### 验证

- mock MCP server tool listing / call
- LSP registry dispatch tests
- plugin tool name conflict tests

### 成功标准

- 外部能力可以扩，不必继续硬编码进 core runtime

---

## 阶段 8：观测、回归、parity harness

### 目标
让系统具备持续演化能力。

### 范围

- `runtime/tracing`
- `tests/parity`
- `runtime/hooks`

### 必做内容

- turn trace
- tool trace
- usage / cost report
- mock provider parity harness
- hooks 最小生命周期点

### 验证

- 关键场景录成固定 harness case：
  - streaming text
  - read file roundtrip
  - grep + synthesis
  - write allowed / denied
  - bash allowed / denied
  - compact triggered
  - subagent task handoff

### 成功标准

- 系统以后每次重构都有回归抓手

---

## 7. 最小改动路径：如果现在就开始写代码，先做哪五步

如果今天开始干，我建议按下面五步开工：

### 第一步：定义五个基础 contract

- `ConversationRuntime`
- `ToolSpec`
- `ToolExecutor`
- `PermissionPolicy`
- `Session`

> 先冻结接口，再写实现。

### 第二步：做 mock provider + 单工具回环

跑通：

- user
- assistant(tool_use read_file)
- tool_result
- assistant(final)

> 先证明 loop 结构是对的。

### 第三步：做统一工具注册，不要散写 handler

至少把六个首发工具挂上统一 registry。

> 先做“可管理工具面”，而不是“能跑几个函数”。

### 第四步：把 permission 接进 dispatch 总闸门

不要等全做完才补权限。

> 权限必须是主干的一部分，不是上线前加一层 if。

### 第五步：补 compact + session persistence

没有这步，系统只能 demo，做不了真正长任务。

---

## 8. 风险最高的三个点，要尽早验证

### 风险 1：控制循环会不会失控

典型问题：

- tool_use 回灌顺序混乱
- 无穷循环
- assistant message 与 tool_result 绑定错位

应对：

- 尽早写 mock harness
- 尽早设 `max_iterations`

### 风险 2：权限门是不是旁路化了

典型问题：

- 某些工具绕过统一 dispatch
- bash 分类过宽
- workspace 边界没收紧

应对：

- 所有工具统一走 dispatch
- 每个工具定义 required permission

### 风险 3：长上下文治理是不是过晚引入

典型问题：

- 一开始看起来能跑
- 任务一长就完全崩

应对：

- 在第 4 阶段前不要扩太多外设
- 先把 compact / artifact 做起来

---

## 9. 验证证据：每个阶段不能只靠“看代码”

按 harness 视角，最小验收证据必须包括：

### 自动化测试

- 单轮 loop
- 多轮 loop
- tool roundtrip
- permission denial
- session persistence
- compact trigger
- subagent allowlist

### 结构化工件

- session file
- compact summary
- task manifest
- subagent output
- usage / trace report

### 人工可检查输出

- `/status`
- `/doctor`
- `/cost`
- `/resume latest`
- 工具调用和权限拒绝日志

如果一个阶段只能说“我看代码觉得差不多”，那它其实还没验收。

---

## 10. 一句话交付标准

一个“最小 Claude Code 风格开源实现”到位时，应该能满足下面这条话：

> **它能在受控权限下，以多轮 control loop 稳定完成真实 coding task；能调用统一工具面；能保存和恢复 session；能处理长上下文；能拆子任务；并且每个关键路径都能被回归测试复现。**

如果达不到这条，就还只是“agent demo”，不是“agent harness”。
