# Claw Code：一个对齐 Claude Code 产品表面的开源 Rust Agent Harness

## 1. 这份材料为什么值得单独落库

分析 Claude Code 时，一个很现实的问题是：**官方当前公开出来的并不是完整核心 runtime 源码**。  
这会导致两个常见误区：

1. 把 GitHub 上公开的插件、命令、workflow 仓误当成完整实现；
2. 把历史逆向文章里的内部切片误当成最新版事实。

`claw-code` 提供了第三种材料：它不是 Anthropic 官方源码，但它是一个**明确对齐 Claude Code 产品表面的开源 Rust harness**。这类项目的价值，在于让我们能把“一个 Claude Code 风格 coding agent 到底由哪些运行时部件组成”拆开来看。

---

## 2. 项目定位：不是官方源码，而是公开 Rust 实现

`README.md` 里给了两个非常关键的定位信号：

- “Claw Code is the public Rust implementation of the `claw` CLI agent harness.”
- 仓库声明 **not affiliated with, endorsed by, or maintained by Anthropic**

这意味着它应该被当成：

- 一个 **对照实现（comparative implementation）**
- 一个 **复刻型 / 对齐型 agent harness**
- 一个能帮助我们理解 Claude Code 工程结构的**可读样板**

而不应该被当成：

- Anthropic 官方主仓
- Claude Code 最新版完整源码
- 能直接证明官方实现细节的原件

本地证据路径：

- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code`
- HEAD：`d4494a8aeb8446164e1a7260def1d4e77cef243c`

---

## 3. 总体架构：它实现的是一个“模型外壳”，不是单纯 CLI 包装

从 `README.md`、`concept.md`、`rust/README.md` 三份入口文档综合看，`claw-code` 的核心不是“调用一次 API 输出文本”，而是完整的 agent 外壳：

- **CLI 宿主**：`rusty-claude-cli`
- **provider API 层**：`api`
- **runtime 层**：session、permission、prompt、MCP 生命周期、usage tracking
- **tools 层**：内置工具、tool search、skill / agent / task 等工具表面
- **plugins 层**：插件安装、启停、工具聚合
- **telemetry 层**：session trace / usage

这跟我们对 Claude Code 的推断很一致：真正的系统本体是 **runtime + tool surface + permission + context/session + task/memory + extensibility**。

---

## 4. control loop：`ConversationRuntime` 是它的主心骨

最值得看的文件是：

- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\conversation.rs`

这里定义了：

- `AssistantEvent`
- `ToolExecutor` trait
- `TurnSummary`
- `ConversationRuntime<C, T>`

### 4.1 事件模型

`AssistantEvent` 把模型流式响应拆成了几类事件：

- `Thinking`
- `TextDelta`
- `ToolUse`
- `Usage`
- `PromptCache`
- `MessageStop`

这个设计说明它不是拿完整响应后再处理，而是以**事件流**的方式把模型响应、tool_use、usage 和 prompt cache 统一进同一个 turn 内。

### 4.2 运行主循环

`run_turn()` 的链路很清楚：

1. 先做 session compaction 后的健康探针；
2. 把用户输入追加进 session；
3. 构造 `ApiRequest { system_prompt, messages }`；
4. 调 `api_client.stream()` 获取事件流；
5. 通过 `build_assistant_message(events)` 组装助手消息；
6. 扫描其中的 `ToolUse` block；
7. 对每个工具跑 pre-hook → permission → execute → post-hook；
8. 把 tool_result 再写回 session；
9. 如果还有 tool_use，继续下一轮；没有则退出。

这本质上就是一个**显式 ReAct loop**：

- 读当前会话上下文
- 调模型
- 看到 `tool_use`
- 执行工具
- 结果回灌上下文
- 再调模型

### 4.3 主循环的几个工程化细节

它不是只有最小闭环，还补了几层现实工程里很关键的东西：

- `max_iterations`：防死循环
- `UsageTracker`：累计 token usage
- `PromptCacheEvent`：观测 cache 读写异常
- `auto_compaction_input_tokens_threshold`：超阈值自动压缩
- `SessionTracer`：记录 `turn_started / assistant_iteration_completed / tool_execution_started / tool_execution_finished / turn_completed / turn_failed`

也就是说，这个 loop 已经不是“demo agent loop”，而是明显带有**生产级运行治理意识**的 loop。

---

## 5. 工具层：`tools` crate 像一个统一控制面

第二个核心文件是：

- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\tools\src\lib.rs`

这里做了三件事：

1. 定义 `ToolSpec { name, description, input_schema, required_permission }`
2. 给出 `mvp_tool_specs()` 的完整工具表面
3. 通过 `execute_tool_with_enforcer()` 把所有工具分发到实际 handler

### 5.1 工具不是散落实现，而是统一 schema surface

`mvp_tool_specs()` 暴露的是一个很像 Claude Code 的工具面，包含：

- 文件工具：`read_file` / `write_file` / `edit_file`
- 搜索工具：`glob_search` / `grep_search` / `WebFetch` / `WebSearch`
- 计划与结构化输出：`TodoWrite` / `EnterPlanMode` / `ExitPlanMode` / `StructuredOutput`
- agent 能力：`Agent`
- 扩展发现：`Skill` / `ToolSearch`
- 平台工具：`Task*` / `Team*` / `Cron*` / `MCP` / `LSP`
- 运行时辅助：`Config` / `SendUserMessage` / `REPL` / `PowerShell`

这说明项目作者不是只在做“六七个最小工具”，而是在试图对齐一整套 coding-agent product surface。

### 5.2 `execute_tool()` 是工具执行总闸门

`execute_tool_with_enforcer()` 体现了很典型的 harness 设计：

- 工具名 → 反序列化输入
- 动态分类所需权限
- permission check
- 路由到具体 `run_*`

尤其值得注意的是两类动态分类：

- bash / PowerShell 根据命令内容动态决定需要的权限级别
- 文件 / grep / glob 根据路径是否落在 workspace 内决定 `ReadOnly`、`WorkspaceWrite` 还是 `DangerFullAccess`

这比“给工具硬编码一个静态权限”更接近真实 agent 产品。

---

## 6. 权限门：`PermissionEnforcer` 把 mode 变成硬边界

对应文件：

- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\permission_enforcer.rs`

这里的关键点有三个：

### 6.1 权限是单独的 enforcement layer

`PermissionEnforcer` 不嵌在某个工具内部，而是独立出来。  
这意味着“权限”在架构上被视为**跨工具统一控制面**，而不是某个工具自己想起才检查一下。

### 6.2 既有静态模式，也有动态判定

它支持：

- `check()`：走 policy 的通用判断
- `check_with_required_mode()`：给 bash / PowerShell 这种动态模式使用
- `check_file_write()`：写文件时做 workspace 边界检查
- `check_bash()`：read-only 模式下只放行保守只读命令

### 6.3 权限模式不是摆设，而会改变工具可达面

当前的模式分层很清晰：

- `ReadOnly`
- `WorkspaceWrite`
- `DangerFullAccess`
- `Prompt`
- `Allow`

这和 Claude Code / Codex 一类产品的核心现实一致：  
**真正有风险的不是“模型会不会推理”，而是它能不能越过宿主边界执行动作。**

---

## 7. 子代理：不是假按钮，而是真的会起一个受限 runtime

`Agent` 工具是这份源码里最有意思的部分之一。

从 `run_agent()` → `execute_agent()` → `spawn_agent_job()` → `run_agent_job()` 这条链可以看到：

1. 先为子任务生成 `agent_id`
2. 在本地落 `output_file` 和 `manifest_file`
3. 记录 `description / prompt / subagent_type / model / timestamps`
4. 组装一个专门的 `system_prompt`
5. 基于 `subagent_type` 限定 allowed tools
6. 启一个后台线程
7. 在线程里重新构造 `ConversationRuntime`
8. 跑 `runtime.run_turn(prompt, None)`
9. 把完成态或失败态持久化回 agent manifest

### 7.1 它实现的不是“函数调用式子代理”，而是“持久化子运行体”

这很关键。  
很多项目所谓 sub-agent，只是函数里拼一个 prompt 再发一次请求。  
但这里已经有：

- 独立 manifest
- 独立输出文件
- 独立 allowed tool set
- 独立 runtime
- 后台线程执行

这已经明显更接近真正的**worker / lane / delegated runtime**。

### 7.2 子代理类型会改变工具白名单

`allowed_tools_for_subagent()` 给了几个子代理档位：

- `Explore`：偏只读探索，不含 `bash`
- `Plan`：允许 `TodoWrite` / `StructuredOutput`
- `Verification`：允许 `bash` 与 `PowerShell`，但不含 `write_file`
- 默认 general-purpose：工具面更宽

这体现的是一个很成熟的 harness 思路：  
**先定义子代理角色，再按角色收紧工具可达面。**

---

## 8. task / team / cron：长时程协作底座已经成形

对应文件：

- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\task_registry.rs`
- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\PARITY.md`

`TaskRegistry` 当前是一个线程安全的内存注册表，支持：

- `create`
- `create_from_packet`
- `get`
- `list`
- `stop`
- `update`
- `output`
- `append_output`
- `set_status`
- `assign_team`
- `update_heartbeat`
- `lane_board`

这说明它已经不只是“task tool 返回固定 JSON”，而是有真实生命周期状态。

同时，`PARITY.md` 也说明：

- `TaskRegistry`、`Task wiring`、`Team+Cron`、`MCP lifecycle`、`LSP client`、`Permission enforcement`
- 都被当作独立 lane 去推进

这很像在主动把一个 coding agent 从“能跑起来”推进到“具备产品级控制面”。

---

## 9. MCP / LSP：协议桥接已有壳，但深度仍分层

### 9.1 MCP

`mcp_tool_bridge.rs` 提供：

- server 状态注册
- resource listing / reading
- tool listing
- auth status
- tool call 派发

它的定位非常明确：是 **MCP tool surface 与真实 runtime manager 之间的桥**。

这意味着：

- 表面上，模型已经能看到 `ListMcpResources` / `ReadMcpResource` / `MCP` / `McpAuth`
- 内部上，项目作者也承认更深的 transport / lifecycle 还依赖更底层 MCP runtime

### 9.2 LSP

`lsp_client.rs` 提供：

- server registry
- extension → language 路由
- diagnostics cache
- hover / definition / references / symbols / formatting 等 action dispatch

但从实现上看，它目前更像**registry + dispatch 壳**，而不一定是完整外部语言服务器编排器。

所以对这两个层次最稳妥的判断是：

- **工具表面已经成形**
- **注册表和分发桥已经成形**
- **完全成熟的外部 runtime 深度则未必都到位**

---

## 10. plan mode：它不是一个 prompt 技巧，而是宿主状态切换

`EnterPlanMode` / `ExitPlanMode` 这两个工具值得单独记一下。

它们不是仅仅告诉模型“现在开始做计划”，而是会：

- 改写 worktree-local settings
- 保存原始 local mode
- 写入/清理 plan mode state file
- 支持恢复已有 override

这说明它把 **plan mode 当成一个宿主状态机问题**，不是聊天层修辞问题。  
这和我们分析 Claude Code 时强调的观点很一致：  
**plan 是运行时控制面，不只是提示词风格。**

---

## 11. 验证结果：源码判断不是纯猜测

本次本地验证做了几件事：

- `cargo check -p runtime --lib` 通过
- `cargo test -p tools agent_tool_subset_mapping_is_expected` 通过
- `cargo test -p tools enter_and_exit_plan_mode_round_trip_existing_local_override` 通过
- `cargo test -p tools run_task_packet_creates_packet_backed_task` 通过

同时也发现一个很有价值的事实：

- `cargo test -p runtime ...` 在 Windows 测试构建里会因为 `std::os::unix::fs::PermissionsExt` 出现在测试模块中而失败

这说明：

1. 项目的主要 runtime crate 可以在当前环境完成 `cargo check`
2. tools 层的一些关键行为可以直接测试通过
3. 但 runtime 的测试层仍带有一部分 Unix-only 假设

这是一条很真实的成熟度信号：**主干已成，但跨平台测试收口还没完全做干净。**

---

## 12. 和 Claude Code 研究专题的关系

`claw-code` 对我们研究 Claude Code 最有帮助的地方，不是“它证明了 Anthropic 官方内部 exactly 这样写”，而是它把下面这些问题变成了**可以公开阅读的代码结构**：

1. 一个 coding agent 的主循环应放在哪里？
2. tool spec 和 tool execution 应不应该分离？
3. permission 是 policy 还是 per-tool if/else？
4. sub-agent 应该只是 prompt 复用，还是独立 runtime？
5. task / cron / team / MCP / LSP 这些能力，应该如何接入主循环？
6. plan mode、structured output、skill、plugin 这些“产品表面”背后，分别对应哪一层宿主逻辑？

换句话说，它是一个非常适合作为 **Claude Code 风格 open harness 对照样本** 的仓库。

---

## 13. 结论

如果把 `hello-agents` 视为“理论地基”，把 Claude Code 官方公开仓/文档/npm wrapper 视为“官方可证表面”，那么 `claw-code` 就可以视为中间那块很重要的桥梁：

- 它不是官方真源码；
- 但它是一个能直接看到 harness 分层的开源实现；
- 它让我们能把 Claude Code 风格 agent 的许多关键控制面，转化成可验证的工程结构。

因此，这份材料最适合放在 Claude Code 研究专题里，作为：

- **对照实现**
- **开源 harness 样板**
- **理解 runtime / permission / subagent / task / MCP / plan mode 的结构性证据**

而不是作为“官方源码已公开”的证据来使用。
