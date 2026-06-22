# FlagHunter(PentestAgent) Agent 架构 vs Claw Code：逐层差距分析与改进路线

## 0. 分析目标

用户反馈 FlagHunter(`D:\webstudy\FlagHunter`) 的智能体"太简陋了，不会自己思考"。本文通过逐层对比 FlagHunter 当前 agent 实现与 claw-code（Claude Code 的 Rust 重写对照实现），找出具体差距，并给出改进优先级。

---

## 1. FlagHunter 当前 Agent 架构总览

### 1.1 核心文件与职责

| 文件 | 职责 |
|------|------|
| `base_agent.py` | 主循环 `_run_loop()`、工具执行、计划生成/重规划 |
| `pa_agent/pa_agent.py` | PentestAgentAgent：CTF 检测、运行时指纹、提示检索 |
| `tools/registry.py` | 工具注册表：全局 dict `_tools`，`register_tool` 装饰器 |
| `tools/executor.py` | ToolExecutor：执行、重试、缓存、flag 扫描、stealth 延迟 |
| `llm/memory.py` | ConversationMemory：token 计数、summarization |
| `agents/state.py` | AgentStateManager：有限状态机 |

### 1.2 主循环 (`_run_loop`) 控制流

```
iteration = 0
while iteration < max_iterations:
    iteration += 1

    # ITER 1: 强制生成计划
    if iteration == 1 && no plan:
        plan = await _auto_generate_plan()

    # 调用 LLM
    response = await llm.generate(
        system_prompt=get_system_prompt(),
        messages=conversation_history,
        tools=enabled_tools + suggested_tools
    )

    # 无 tool_calls: 视为 "thinking out loud"，continue
    if not response.tool_calls:
        continue

    # 有 tool_calls: 并发执行
    tool_results = await _execute_tools(response.tool_calls)

    # 记录历史
    conversation_history.append(assistant_msg)
    conversation_history.append(tool_result_msg)

    # 检查扫描结果 → 扩展计划
    # 检查步骤失败 → 重规划
    # 检查计划完成 → 生成摘要，退出
```

### 1.3 当前已有的能力（不是零基础）

FlagHunter 的 agent 不是一个"玩具"，它已经有了：

- **ReAct loop**：观察 → 思考 → 行动 → 观察 的完整闭环
- **自动计划生成**：首轮用 function calling 生成步骤计划
- **计划扩展**：扫描发现新端口/服务时自动追加步骤
- **战术重规划**：步骤失败时调用 LLM 生成新计划
- **多模式**：agent / assist / interact / mcp 四种运行模式
- **上下文压缩**：ConversationMemory 基于 token 阈值自动摘要
- **工具结果缓存**：60 秒 TTL 避免重复执行
- **CTF 专项**：类型检测、快速路径、提示检索、经验保存
- **provider failover**：M1 API Hub 多 provider 自动切换

---

## 2. 与 claw-code 的逐层对比

### 2.1 控制循环层 (Control Loop)

| 维度 | FlagHunter | claw-code | 差距 |
|------|-----------|-----------|------|
| 循环结构 | `while iteration < max` | `ConversationRuntime.run_turn()` | 相似 |
| 事件模型 | 无显式事件枚举 | `AssistantEvent` 枚举(Thinking/TextDelta/ToolUse/Usage/PromptCache/MessageStop) | **FlagHunter 没有事件抽象** |
| 思考分离 | 文本响应直接当 content | Thinking 有独立事件 + signature | **FlagHunter 不区分思考与行动** |
| 终止条件 | plan complete / max iter / error | tool_use 为空 / max iter | FlagHunter 多了 plan 约束 |
| prompt cache 感知 | 无 | `PromptCacheEvent` + 阈值监控 | **FlagHunter 无此概念** |

**关键差距**：FlagHunter 的循环把"纯文本响应"当作"思考中，继续循环"，这在 ReAct 模式下是对的，但它缺少**事件抽象**。claw-code 用 `AssistantEvent` 枚举统一建模每个 turn 的所有可能输出，这让上层可以灵活组合（比如把 Thinking 单独展示给用户，把 ToolUse 传给权限系统预检）。

### 2.2 工具系统层 (Tool System)

| 维度 | FlagHunter | claw-code | 差距 |
|------|-----------|-----------|------|
| 注册方式 | 全局 dict + 装饰器 | `mvp_tool_specs()` 返回 Vec | 相似 |
| 工具描述 | `Tool` dataclass + `ToolSchema` | `ToolSpec` struct | 相似 |
| 执行分发 | `_execute_single` → `tool.execute(args)` | `execute_tool_with_enforcer()` | 相似 |
| 动态工具 | `suggested_tools` (RAG optimizer) | MCP tools 动态注入 | 相似 |
| **统一 dispatch** | 无强制统一入口 | `execute_tool_with_enforcer()` 是所有工具的唯一入口 | **FlagHunter 的工具可能绕过统一 dispatch** |
| **工具发现** | 无 | `ToolSearch` 工具让 agent 自己搜索工具 | **FlagHunter agent 不知道有什么工具可用** |
| **Semantic tools** | 无 | LSP 语义工具 (hover/definition/references) | N/A |

**关键差距**：FlagHunter 的工具执行路径不统一 — `base_agent._execute_single` 有一套逻辑，`executor.ToolExecutor.execute` 有另一套（带缓存、stealth、flag 扫描），但 agent loop 实际调用的是 `_execute_single`，绕过了 ToolExecutor 的增强逻辑。而 claw-code 的 `execute_tool_with_enforcer()` 是所有工具调用的唯一入口，权限检查、hook、执行、结果标准化全部在此完成。

### 2.3 权限门禁层 (Permission) — 最大差距

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| 权限模型 | **无** | `PermissionPolicy` + `PermissionEnforcer` |
| 分级 | 无 | read-only / workspace-write / danger-full-access |
| 文件权限 | 无 | 基于路径是否在 workspace 内判断 |
| shell 权限 | 无 | 基于命令内容动态分类 |
| 确认流程 | 无 | prompt/allow/deny 路径 |
| scope 检查 | M4 scope check（外部模块） | 内建于 permission_enforcer |

**这是 FlagHunter 最严重的缺失**。当前代码中：
- `_execute_single` 只做了 workspace target 验证
- `ToolExecutor.execute` 只做了 M4 scope check
- 没有统一的"这个操作能不能做"的硬门禁

claw-code 的 `PermissionEnforcer` 是独立层，**每个工具调用都必须先过它**，支持动态权限模式切换和命令级风险分类。

### 2.4 子代理系统 (Subagent) — 第二大差距

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| Agent 工具 | **无** | `Agent` 工具 + `subagent_type` 参数 |
| 子代理 runtime | 无 | 独立 `ConversationRuntime` 线程 |
| 工具白名单 | 无 | Explore: 无 bash; Plan: 只读; Verification: 有 bash 无 write |
| manifest 文件 | 无 | 每个子代理有独立 manifest + output 文件 |
| 生命周期 | 无 | spawn → run → completed/failed → output |

**这就是用户说"不会自己思考"的核心原因之一**。Claude Code 可以把大任务拆给子代理独立执行：
1. 生成 `agent_id`
2. 创建 manifest 文件
3. 按 `subagent_type` 收紧 allowed tools
4. 起后台线程独立运行
5. 完成后持久化状态

FlagHunter 完全没有这个能力。它只能单线程执行计划步骤。

### 2.5 任务注册表层 (Task Registry)

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| 任务创建 | `_task_plan` (内存对象) | `TaskRegistry.create()` |
| 任务列表 | 无 | `TaskRegistry.list()` |
| 任务状态 | PlanStep status (pending/complete/fail) | Task status + heartbeat |
| 持久化 | 无 | packet 文件持久化 |
| 看板 | 无 | `lane_board` |
| cron | 无 | `CronCreate/CronDelete` |

FlagHunter 的计划系统本质上是一个"单任务状态跟踪器"，不是"多任务生命周期管理器"。claw-code 的 `TaskRegistry` 支持创建、查询、停止、更新、心跳、看板，是真正的任务底座。

### 2.6 上下文/记忆层 (Context & Memory)

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| 摘要策略 | token 阈值 + 分块 LLM 摘要 | auto compaction + CompactionConfig |
| 触发条件 | `total_tokens > threshold` | 输入 token 超过阈值 |
| 系统记忆 | 无 | `CLAUDE.md` 项目记忆 |
| 会话持久化 | 无 | Session save/load |
| usage 追踪 | 有记录但未用于循环决策 | `UsageTracker` 集成到 turn 循环 |
| cache 感知 | 无 | prompt cache 命中率监控 |

**关键差距**：
- FlagHunter 缺少 `CLAUDE.md` 式的项目级持久记忆
- 没有会话持久化（重启即丢失）
- Usage 数据记录了但没有反向驱动循环行为（比如提前 compact）

### 2.7 Hook 系统

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| Pre-hook | 无 | HookRunner pre-tool hooks |
| Post-hook | 无 | HookRunner post-tool hooks |
| Abort 信号 | 无 | `HookAbortSignal` |
| Progress 通知 | notify() 函数 | `HookProgressReporter` trait |

FlagHunter 有一些零散的 hook 点（如 M4 scope check、stealth 延迟），但没有统一的 hook 注册/触发机制。

### 2.8 协议扩展层 (MCP / LSP)

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| MCP 工具桥 | `mcp/` 目录支持 | `McpToolRegistry` + `McpToolBridge` |
| LSP 集成 | 无 | `LspRegistry` + dispatch |
| Plugin 系统 | 无 | Skill 系统 |

FlagHunter 的 MCP 支持主要在 server 端（对外暴露），而不是 client 端（消费外部 MCP 工具）。claw-code 两端都有。

### 2.9 计划与模式系统

| 维度 | FlagHunter | claw-code |
|------|-----------|-----------|
| Plan Mode | 无（plan 是强制步骤而非可选模式） | `EnterPlanMode` / `ExitPlanMode` 宿主状态切换 |
| TodoWrite | 无 | 独立工具 |
| StructuredOutput | 无 | 独立工具 |

FlagHunter 的计划是**强制的**（iteration 1 自动生成），但缺少模式切换能力。claw-code 的 Plan Mode 是 agent **自主决定**进入的运行时状态，并且会持久化。

---

## 3. "不会自己思考"的根因分析

回到用户的核心反馈——FlagHunter agent "不会自己思考"。从架构角度看，这是因为：

### 3.1 计划驱动 vs 目标驱动

FlagHunter 当前是**计划驱动型**：
```
用户任务 → 强制生成计划 → 按步骤执行 → 标记完成 → 退出
```

Claude Code 是**目标驱动型**：
```
用户任务 → 理解目标 → 自主决定：
  - 需要探索吗？→ Explore subagent
  - 需要计划吗？→ EnterPlanMode
  - 需要拆解吗？→ Agent(Explore) + Agent(Plan)
  - 可以直接做吗？→ 直接工具调用
  - 完成了吗？→ 验证 → 退出
```

FlagHunter 的 agent **没有"决定怎么做"的自由度**。它被计划框架约束死了：先出计划，再做步骤，再标记完成。这种模式适合确定性任务（如渗透测试检查清单），但面对开放式任务时显得"不会思考"。

### 3.2 没有子代理 = 无法拆解复杂任务

Claude Code 的核心"智能感"很大程度来自子代理系统：
- 遇到不熟悉的代码库 → 分派 Explore 子代理
- 需要设计方案 → 分派 Plan 子代理
- 需要验证 → 分派 Verification 子代理
- 每个子代理有独立上下文窗口、独立工具面

FlagHunter 只能一个 agent 从头干到尾。

### 3.3 没有思考/行动分离

claw-code 的 `AssistantEvent::Thinking` 是独立事件类型，有 signature。这意味着：
- 模型的"思考过程"被显式建模
- UI 可以折叠思考、只展示行动
- 思考可以跨 turn 保留

FlagHunter 把思考当普通文本处理，混在 conversation_history 里。

### 3.4 没有工具搜索能力

FlagHunter agent 不知道自己有哪些工具可用（工具列表在 system prompt 里但可能被截断）。claw-code 有 `ToolSearch` 工具，agent 可以动态发现可用工具。

---

## 4. 改进优先级路线

基于差距分析，以下是推荐的改进顺序：

### 优先级 P0：权限门禁层（1-2天）

**为什么先做这个**：当前没有任何硬门禁，工具直接执行。安全风险最高。

```python
# 最小实现
class PermissionEnforcer:
    def check(self, tool_name: str, arguments: dict) -> PermissionResult:
        # read-only: 只允许 read/grep/glob
        # workspace-write: 允许在 workspace 内写
        # danger-full-access: 允许所有
        pass
```

改动点：
- `base_agent._execute_single` 中注入 permission check
- 或统一到 `ToolExecutor.execute` 中

### 优先级 P1：子代理系统（3-5天）

**为什么第二做这个**：这是"会自己思考"最关键的架构改进。

```python
# 最小实现
class SubagentRunner:
    async def spawn(self, task: str, subagent_type: str) -> SubagentResult:
        # 1. 按类型选择 tool allowlist
        # 2. 创建独立 conversation
        # 3. 运行子循环
        # 4. 返回结果 + manifest
        pass
```

需要的工具：`Agent(task, subagent_type)` 注册为新工具

子代理类型：
- `Explore`: 只读探索（read/grep/glob/web_search，无 bash/write）
- `Plan`: 计划设计（只能 TodoWrite/StructuredOutput）
- `General`: 通用（当前工具面）

### 优先级 P2：思考分离 + 工具搜索（2-3天）

- 在 `LLMResponse` 中增加 `reasoning_content` 字段（已有）
- 在 agent loop 中区分 thinking 和 action
- 添加 `ToolSearch` 工具

### 优先级 P3：会话持久化 + Task Registry（3-5天）

- Session save/load
- Task 生命周期管理
- Heartbeat / 看板

### 优先级 P4：Hook 系统 + MCP Client Bridge（3-5天）

---

## 5. 最小改动验证路径

如果只做最小改动来验证方向，建议：

### 第一步：给 `_execute_single` 加 permission check

```python
# base_agent.py _execute_single 中，tool.execute 之前
if not self.permission_enforcer.check(name, arguments):
    return ToolResult(..., error="Permission denied", success=False)
```

### 第二步：添加 Agent 工具（最小子代理）

在 `pentestagent/tools/` 下新建 `agent/` 目录，注册 `Agent` 工具：

```python
@register_tool(
    name="Agent",
    description="Spawn a subagent to handle a delegated task...",
    schema=ToolSchema(
        properties={
            "task": {"type": "string"},
            "subagent_type": {"type": "string", "enum": ["Explore", "General"]},
        },
        required=["task"],
    ),
)
async def agent_tool(arguments: dict, runtime: Runtime) -> str:
    # 创建独立 LLM + 受限工具集 + 独立循环
    ...
```

### 第三步：验证

- 给 agent 一个复合任务："先探索项目结构，再分析安全问题"
- 观察它是否能自主决定用 Agent(Explore) 去探索
- 观察子代理结果是否被正确汇总

这三步改动后，FlagHunter agent 就应该开始表现出"会自己拆解任务"的行为了。

---

## 6. 总结

FlagHunter 的 agent 不是一个差的设计——它有完整的 ReAct loop、计划系统、工具注册表、上下文管理。但它确实处于 agent harness 演进的**早期阶段**：

```
阶段 1: 单轮聊天    ← 很多"AI 工具"
阶段 2: ReAct Loop  ← FlagHunter 现在在这里
阶段 3: + 权限门    ← P0
阶段 4: + 子代理    ← P1（"会自己思考"的关键）
阶段 5: + Task/Cron ← P3
阶段 6: + MCP/LSP   ← P4（完整 harness）
```

claw-code/Claude Code 处于阶段 5-6。FlagHunter 需要补的阶段 3-4 正是"从执行器变成智能体平台"的关键跨越。
