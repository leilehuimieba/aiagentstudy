# Claude Code 成功原因深度解构 + FlagHunter 智能化完整改进方案

## 0. 这篇分析要回答什么

前面 `BB-2026-05-01-330` 做了 FlagHunter vs claw-code 的逐层差距对比。但那篇主要回答"差在哪里"。这篇要回答更根本的两个问题：

1. **Claude Code 到底为什么成功？**不是功能列表，而是架构设计原则层面的根因。
2. **基于这些根因，FlagHunter 要真正变"智能"，具体应该怎么改？**不是补几个功能，而是系统性地重构 agent 的"思考方式"。

---

## 1. Claude Code 成功的七个架构原则

通过对知识库全部材料（BB-325/326/327/328/329）+ claw-code 源码深入勘察，我提炼出 Claude Code 成功的 **7 个设计原则**。这些原则彼此依赖，单独实现效果有限。

### 原则 1：控制循环是工程化 ReAct，不是提示词技巧

**[证据来源]**

claw-code `conversation.rs:run_turn()` 展示了一个完整的工程化 ReAct 循环：

```
run_turn(user_input):
    record_turn_started()
    session.push_user_text(input)

    loop:
        // 1. 组装 API 请求
        request = ApiRequest { system_prompt, messages: session.messages }

        // 2. 调用模型流
        events = api_client.stream(request)

        // 3. 解析事件流 → 结构化 assistant message
        (assistant_message, usage, cache_events) = build_assistant_message(events)

        // 4. 记录 usage + prompt cache 事件
        usage_tracker.record(usage)

        // 5. 推入 session
        session.push_message(assistant_message)

        // 6. 自动 compact 检查
        maybe_auto_compact()

        // 7. 无 tool_use → 退出
        if no tool_uses: break

        // 8. 对每个 tool_use:
        for each tool_use:
            // a. pre-hook
            pre_hook_result = run_pre_tool_use_hook()
            // b. permission check (含 hook 结果)
            permission_outcome = permission_policy.authorize_with_context()
            // c. 执行 tool
            output = tool_executor.execute()
            // d. post-hook (含失败 hook)
            post_hook_result = run_post_tool_use_hook()
            // e. 推入 session
            session.push_message(tool_result)

    // 9. 返回 TurnSummary
    return TurnSummary { messages, tool_results, usage, compaction }
```

**[为什么这是成功关键]**

这个循环做到了"提示词做不到"的事：

- **事件流解析**：把 LLM 的流式输出解析为 `AssistantEvent` 枚举（Thinking/TextDelta/ToolUse/Usage/PromptCache/MessageStop），每个事件有独立处理逻辑
- **自动 compact**：每次 API 调用前检查是否需要压缩，而不是等出问题再处理
- **pre/post hook 全覆盖**：每个工具执行都有"前拦截→权限→执行→后处理"完整链路
- **Usage 追踪集成**：token 使用不是事后统计，而是每个 turn 的决策输入

FlagHunter 的 `_run_loop` 对比：工具执行路径不统一（`_execute_single` 绕过了 `ToolExecutor`），没有 hook 机制，没有 compact 触发检查。

### 原则 2：工具面是统一契约，不是散装函数

**[证据来源]**

claw-code `tools/lib.rs` 的核心设计：

```rust
// 每个工具规范都必须声明：
pub struct ToolSpec {
    pub name: &'static str,
    pub description: &'static str,
    pub input_schema: Value,
    pub required_permission: PermissionMode,  // 每个工具自带权限声明
}

// 所有内置工具通过 execute_tool_with_enforcer() 统一分发
fn execute_tool_with_enforcer(enforcer, name, input):
    match name:
        "bash" => classify_bash_permission() → enforce → run_bash()
        "read_file" => classify_read_path_permission() → enforce → run_read_file()
        "write_file" => classify_file_path_permission() → enforce → run_write_file()
        ...

// 权限分类是工具层自带的，不是外部附加的
fn classify_bash_permission(command) -> PermissionMode  // 识别只读命令
fn classify_file_path_permission(path) -> PermissionMode  // workspace 边界判断
```

**[为什么这是成功关键]**

- 每个工具的 `required_permission` 是**编译时声明**的，不是运行时猜测的
- `execute_tool_with_enforcer()` 是**唯一入口**，无法绕过权限
- 动态权限分类（如 bash 命令内容 → 风险级别）让同一工具在不同上下文有不同权限要求

FlagHunter 的工具体系对比：`Tool.execute()` 直接调用 `execute_fn`，没有权限层。`base_agent._execute_single` 有 workspace 检查，但和 `ToolExecutor.execute` 是两条不同路径。

### 原则 3：权限是硬门禁，不是事后补丁

**[证据来源]**

claw-code `permission_enforcer.rs`：

```rust
pub enum PermissionMode {
    ReadOnly,          // 只允许读
    WorkspaceWrite,    // 允许在 workspace 内写
    DangerFullAccess,  // 允许所有
    Allow,             // 允许（无限制）
    Prompt,            // 每个操作都要确认
}

impl PermissionEnforcer {
    fn check(tool_name, input) -> EnforcementResult  // 通用检查
    fn check_with_required_mode(tool_name, input, required_mode)  // 动态分类后检查
    fn check_file_write(path, workspace_root)       // 文件写入专用
    fn check_bash(command)                          // bash 命令专用
}
```

权限模式之间的比较是**有序的**（ReadOnly < WorkspaceWrite < DangerFullAccess），所以检查逻辑是 `active_mode >= required_mode`。

**[为什么这是成功关键]**

- 权限和工具执行是**同一个调用路径**，不存在"忘了加权限"的旁路
- 文件/命令的权限分类是**语义化**的：不是简单的"能/不能写文件"，而是根据路径在不在 workspace 内、命令是不是纯读来决定
- bash 只读命令白名单（cat/head/tail/ls/grep/awk...）让 ReadOnly 模式下仍然能做探索

### 原则 4：子代理是一等公民，不是 prompt 包装

**[证据来源]**

claw-code 的 Agent 工具和子代理系统：

```rust
// AgentInput 结构
struct AgentInput {
    description: String,      // 简短描述
    prompt: String,           // 委托任务
    subagent_type: Option<String>,  // Explore / Plan / Verification / general-purpose
    name: Option<String>,
    model: Option<String>,
}

// 子代理类型 → 工具白名单
fn allowed_tools_for_subagent(subagent_type):
    "Explore" => [read_file, glob_search, grep_search, WebFetch, WebSearch, ToolSearch, Skill, StructuredOutput]
    // ↑ 无 bash、无 write — 纯探索
    "Plan" => [..., TodoWrite, StructuredOutput, SendUserMessage]
    // ↑ 可计划但不能执行
    "Verification" => [bash, read_file, ..., PowerShell]
    // ↑ 可执行但不能写文件
    "general-purpose" => [所有工具]
    // ↑ 完整能力

// 子代理执行生命周期
fn execute_agent(input):
    1. 生成 agent_id
    2. 创建 manifest_file + output_file
    3. 构建 agent system prompt（按 subagent_type）
    4. 确定 allowed_tools（按 subagent_type）
    5. 创建 AgentJob
    6. spawn_agent_job() → 后台线程
    7. 在新线程中: build_agent_runtime() → run_turn()
    8. 持久化 completed/failed 状态
```

**[为什么这是成功关键]**

子代理不是"再发一个 prompt 给同一个模型"，而是：
- **独立 runtime**：独立的 ConversationRuntime，独立的 session，独立的上下文窗口
- **工具面白名单**：每个子代理类型有精确的工具限制，Explore 不能写文件也不能执行 bash
- **生命周期管理**：manifest 文件持久化输入输出，可以事后查看/恢复
- **角色语义**：不同类型的子代理扮演不同的"工程角色"，而不是同一个模型的不同 prompt

这对"智能感"的贡献是决定性的：Claude Code 遇到大任务时会**自主判断**"这个需要探索"→ 分派 Explore 子代理，"这个需要设计"→ 分派 Plan 子代理，"这个需要验证"→ 分派 Verification 子代理。FlagHunter 完全没有这个能力。

### 原则 5：记忆是外化工件体系，不是模型隐式记忆

**[证据来源]**

知识库材料 + 官方公开接口：

```
CLAUDE.md          → 项目级长期语义记忆
skills/plugins     → 行为与规则记忆
todo/task state    → 任务级情景记忆
compact summaries  → 执行过程记忆
session state      → 工作记忆
transcript/logs    → 审计记忆
```

**[为什么这是成功关键]**

不是"让模型记住更多"，而是"让系统把该记住的东西写在文件里"：
- `CLAUDE.md` 是项目规范的**显式工件**，每次对话都会注入
- compact summary 是对话历史的**结构化摘要**，不是简单截断
- task state 是当前进度的**可恢复快照**
- 这个策略让 agent 在长任务中保持一致性，不依赖模型的"记忆力"

### 原则 6：上下文是装配流水线（GSSC），不是"多喂点 tokens"

**[证据来源]**

Hello-Agents 地基（BB-326）提出的 GSSC 流水线：

```
Gather → Select → Structure → Compress
```

Claude Code 的实现对应：
- **Gather**：从 CLAUDE.md、skills、notes、session history、codebase 收集候选信息
- **Select**：选出当前 turn 最相关的部分（RAG 检索、工具搜索、notes 分类过滤）
- **Structure**：组织成 system prompt + messages + tool definitions
- **Compress**：auto compaction（输入 token 超 100K 阈值时自动触发）

**[为什么这是成功关键]**

上下文不是"一次性灌入"，而是**每个 turn 都重新装配**。这解决了长任务的上下文膨胀问题。

### 原则 7：能力面是可演化生态，不是一次性硬编码

**[证据来源]**

官方公开的插件生态：
- commands / agents / skills / hooks / MCP servers
- plugin marketplace
- 分层能力暴露

**[为什么这是成功关键]**

Claude Code 不会因为加一个新能力就需要改核心 runtime。新能力通过 plugin/skill/MCP server 接入，和内置工具享受相同的权限/调度机制。

---

## 2. FlagHunter 与这 7 个原则的对照

| 原则 | FlagHunter 现状 | 缺失程度 |
|------|----------------|---------|
| 原则 1：工程化 ReAct | 有基础 ReAct loop，但无事件抽象、无 compact 自动触发、无 hook 机制 | **中等缺失** |
| 原则 2：统一工具契约 | 有 Tool 注册表，但无 required_permission 声明、执行路径不统一 | **中等缺失** |
| 原则 3：权限硬门禁 | **完全缺失**。无 PermissionEnforcer、无权限模式 | **严重缺失** |
| 原则 4：子代理一等公民 | **完全缺失**。无 Agent 工具、无子代理 runtime | **严重缺失** |
| 原则 5：外化记忆体系 | 有 ConversationMemory 摘要、有 notes 系统，但无 CLAUDE.md 式项目记忆、无 session 持久化 | **中等缺失** |
| 原则 6：GSSC 上下文 | 有 RAG + notes 注入 + summarization，但各组件之间缺乏统一的装配流水线 | **轻度缺失** |
| 原则 7：可演化生态 | 有 MCP server 端（对外暴露），但无 plugin/skill 系统、无 MCP client bridge | **中等缺失** |

**7 个原则中 FlagHunter 完整具备的只有 0 个，严重缺失 2 个（权限+子代理），中等缺失 4 个。**

---

## 3. 什么是 agent "会自己思考"？——重新定义问题

在给出改进方案之前，需要先澄清"智能化"到底意味着什么。

### 3.1 "会自己思考"不是 AGI

很多人听到"让 agent 更智能"，第一反应是换更强的模型、写更好的 prompt。但从前面的分析可以看出，Claude Code 的"智能感"主要来自**宿主架构**，而不是模型本身。

### 3.2 "会自己思考"的操作性定义

从 claw-code 的行为可以提炼出"智能化"的几个操作性标准：

1. **自主分解任务**：给定一个复杂目标，agent 能自主判断"这个需要先探索" → 分派 Explore，"这个需要规划" → 进入 Plan Mode，"这个需要验证" → 分派 Verification
2. **自主选择工具**：面对未知代码库，能自己用 ToolSearch 发现有 bash/grep/glob 可用；面对特定文件类型，能自己决定用 read 还是 grep
3. **自主管理上下文**：对话太长时自己触发 compact，不需要用户提醒
4. **自主调整策略**：当前方法不 work 时，尝试不同的工具或路径，而不是死循环
5. **自主沉淀知识**：发现重要信息时自己存入 notes，总结出模式时写入记忆
6. **自主请求帮助**：遇到权限不足或能力边界时，明确告之用户需要什么

### 3.3 当前 FlagHunter "不智能"的具体表现

对照上面的标准：

1. **不能分解任务**：只能按预设计划执行，没法说"这个子任务交给 Explore 子代理"
2. **不能选择工具**：工具列表全量注入 system prompt，agent 不知道有什么可用
3. **不能管理上下文**：ConversationMemory 依赖 token 计数触发摘要，没有主动 compact 决策
4. **调整策略受限**：只有计划步骤失败才触发重规划，中间过程的"路走不通"不会自动换路
5. **能沉淀知识**（notes 系统是加分项），但不会主动归纳模式
6. **能请求帮助**（缺失工具提示是加分项），但不会主动说明需要什么权限

---

## 4. 完整改进方案：四个 Phase

### Phase 1：建立控制面（权限 + 统一工具面）—— 让 agent "可控"

**目标**：补上最基础的安全和控制基础设施

#### 1.1 权限门禁系统

**新增文件**：`pentestagent/runtime/permission_enforcer.py`

```python
from enum import IntEnum

class PermissionMode(IntEnum):
    READ_ONLY = 1
    WORKSPACE_WRITE = 2
    DANGER_FULL_ACCESS = 3
    ALLOW = 99

class PermissionEnforcer:
    def __init__(self, mode: PermissionMode, workspace_root: str):
        self.mode = mode
        self.workspace_root = workspace_root

    def check(self, tool_name: str, arguments: dict) -> EnforcementResult:
        """通用权限检查入口"""
        pass

    def check_file_path(self, path: str, is_write: bool) -> EnforcementResult:
        """文件路径 → 权限级别映射"""
        pass

    def check_bash_command(self, command: str) -> EnforcementResult:
        """bash 命令 → 只读/写入分类"""
        pass
```

**改动点**：
- `ToolSchema` 增加 `required_permission: PermissionMode` 字段
- `base_agent._execute_single` 在 `tool.execute()` 前调用 `enforcer.check()`
- bash/terminal 工具增加命令分类逻辑（只读命令白名单）

**验证**：
- ReadOnly 模式下 write_file 被拒绝
- WorkspaceWrite 模式下写 workspace 外文件被拒绝
- bash 只读命令在 ReadOnly 模式下允许

#### 1.2 统一工具执行路径

**改动点**：
- 将 `ToolExecutor.execute()` 作为 agent loop 的统一工具执行入口
- `base_agent._execute_single` 改为调用 `tool_executor.execute()` 而不是 `tool.execute()`
- 删除 `_execute_single` 中的重复逻辑（workspace 检查等，统一到 PermissionEnforcer）

### Phase 2：打造智能感（子代理 + 思考分离 + 工具搜索）—— 让 agent "会思考"

**目标**：实现"自主分解任务"的核心能力

#### 2.1 子代理系统

**新增文件**：`pentestagent/agents/subagent.py`

```python
@dataclass
class SubagentConfig:
    subagent_type: str  # "Explore" | "Plan" | "General"
    allowed_tools: list[str]  # 工具白名单
    system_prompt_suffix: str

SUBAGENT_CONFIGS = {
    "Explore": SubagentConfig(
        subagent_type="Explore",
        allowed_tools=["read_file", "glob_search", "grep_search",
                       "web_search", "web_fetch", "notes"],
        system_prompt_suffix="You are an exploration agent. Read and search only."
    ),
    "General": SubagentConfig(
        subagent_type="General",
        allowed_tools=[],  # 空 = 全部允许
        system_prompt_suffix="You are a general-purpose sub-agent."
    ),
}

class SubagentRunner:
    async def spawn(self, task: str, subagent_type: str,
                    parent_agent: "BaseAgent") -> SubagentResult:
        config = SUBAGENT_CONFIGS.get(subagent_type, SUBAGENT_CONFIGS["General"])
        # 1. 创建受限工具集
        limited_tools = [t for t in parent_agent.tools
                         if not config.allowed_tools or t.name in config.allowed_tools]
        # 2. 创建独立 LLM 实例（共享 provider 配置）
        sub_llm = LLM(model=parent_agent.llm.model)
        # 3. 创建独立 agent（无 finish 工具，无循环限制）
        sub_agent = BaseAgent(sub_llm, limited_tools, parent_agent.runtime)
        # 4. 运行子循环
        result = await sub_agent.agent_loop(task)
        # 5. 返回汇总结果
        return SubagentResult(...)
```

**新增工具**：`pentestagent/tools/agent/__init__.py`

```python
@register_tool(
    name="Agent",
    description="Spawn a subagent to handle a delegated task...",
    schema=ToolSchema(
        properties={
            "task": {"type": "string"},
            "subagent_type": {
                "type": "string",
                "enum": ["Explore", "General"]
            },
        },
        required=["task"],
    ),
    category="agent",
)
async def agent_tool(arguments: dict, runtime: Runtime) -> str:
    ...
```

**改动点**：
- `Agent` 工具注册后，主 agent 可以像 Claude Code 一样分派子任务
- 子代理的输出通过 manifest 文件持久化
- `finish` 工具对子代理不可用（子代理不管理计划）

#### 2.2 思考与行动分离

**改动点**：
- `LLMResponse` 已有 `reasoning_content` 字段，在 agent loop 中使用它
- `_run_loop` 中区分 `thinking_content`（展示思路）和 `action_content`（工具调用前的指令）
- TUI 中折叠思考过程，突出展示行动

#### 2.3 工具搜索

**新增工具**：`pentestagent/tools/tool_search/__init__.py`

```python
@register_tool(
    name="ToolSearch",
    description="Search for available tools by keyword or capability...",
    schema=ToolSchema(
        properties={
            "query": {"type": "string"},
        },
        required=["query"],
    ),
)
async def tool_search(arguments: dict, runtime: Runtime) -> str:
    # 在所有已注册工具的名称和描述中搜索
    ...
```

### Phase 3：建立长期运行能力（任务底座 + 上下文装配 + 外化记忆）—— 让 agent "能长跑"

#### 3.1 任务注册表

**新增文件**：`pentestagent/runtime/task_registry.py`

```python
class TaskStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"

@dataclass
class Task:
    task_id: str
    description: str
    status: TaskStatus
    created_at: float
    output: str = ""

class TaskRegistry:
    """全局任务注册表，管理所有 agent/subagent 任务生命周期"""
    def create(self, description: str) -> Task
    def get(self, task_id: str) -> Optional[Task]
    def list(self, status: Optional[TaskStatus] = None) -> list[Task]
    def stop(self, task_id: str) -> bool
    def update_status(self, task_id: str, status: TaskStatus)
```

**改动点**：
- `BaseAgent.agent_loop` 启动时在 TaskRegistry 注册
- 子代理运行时也注册
- `finish` 工具完成后更新状态

#### 3.2 CLAUDE.md 式项目记忆

**新增文件**：`pentestagent/config/project_memory.py`

```python
class ProjectMemory:
    """读取项目根目录的 CLAUDE.md / AGENTS.md 作为长期记忆"""
    def load(self) -> str
    def inject_to_system_prompt(self) -> str
```

**改动点**：
- `get_system_prompt()` 中注入 CLAUDE.md 内容
- 支持多层级（项目级 + 用户级）

#### 3.3 上下文装配流水线

将现有的零散上下文组件（RAG、notes、CLAUDE.md、工具列表）统一为一个装配流水线：

```python
class ContextAssembler:
    async def assemble(self, mode: str, conversation: list, target: str) -> AssembledContext:
        # Gather: 收集所有候选上下文源
        # Select: 按优先级和相关性筛选
        # Structure: 注入 system prompt + tool definitions
        # Compress: 超阈值时触发 compact
        ...
```

#### 3.4 会话持久化

```python
class SessionPersistence:
    def save(self, session_id: str, conversation: list, task_plan: TaskPlan)
    def load(self, session_id: str) -> tuple[list, TaskPlan]
    def list_sessions(self) -> list[str]
```

### Phase 4：打造可演化生态（MCP Client + Hook 系统 + 可观测性）—— 让 agent "能进化"

#### 4.1 MCP Client Bridge

**改动点**：
- 从 `pentestagent/mcp/` 扩展出 client 端能力
- 消费外部 MCP server 的工具作为 `suggested_tools` 注入

#### 4.2 Hook 系统

**新增文件**：`pentestagent/runtime/hooks.py`

```python
class HookRunner:
    def run_pre_tool_use(self, tool_name: str, input: dict) -> HookResult
    def run_post_tool_use(self, tool_name: str, output: str) -> HookResult
```

#### 4.3 可观测性

**改动点**：
- usage 追踪集成到 agent loop 决策
- 工具执行时间追踪
- turn 级别的 trace 日志

---

## 5. 实施优先级与时间估计

| Phase | 模块 | 预估时间 | 优先级理由 |
|-------|------|---------|-----------|
| **Phase 1** | PermissionEnforcer + 统一工具路径 | 2-3 天 | 安全底线，所有后续改进的信任基础 |
| **Phase 2** | Subagent + Agent 工具 + 思考分离 + ToolSearch | 5-7 天 | **"会思考"的核心**，用户体验变化最大 |
| **Phase 3** | TaskRegistry + CLAUDE.md + 会话持久化 + 上下文装配 | 5-7 天 | 长期运行能力，从"demo"到"干活"的跨越 |
| **Phase 4** | MCP Client + Hook System + 可观测性 | 5-7 天 | 生态扩展，非紧急但重要 |

**总计**：约 17-24 天，可迭代交付（每个 Phase 结束后可独立验证）

---

## 6. Phase 2 最关键的三个设计决策

因为 Phase 2 是"智能感"的核心，这里展开三个最关键的设计决策。

### 决策 1：子代理是否复用主 agent 的 LLM？

**建议**：是。子代理复用主 agent 的 LLM 实例（共享 provider 配置、API key、failover 逻辑），但使用独立的 `ConversationMemory` 和 `conversation_history`。

这意味着子代理有自己的上下文窗口，不会被主 agent 的对话历史污染。这正是 Claude Code 的做法。

### 决策 2：子代理工具白名单是声明式还是继承式？

**建议**：声明式。每个 `subagent_type` 显式声明 `allowed_tools` 列表。不继承主 agent 的工具面。

理由：
- Explore 子代理不应该有 `bash`（防止意外修改）
- Plan 子代理不需要 `write_file`
- 这种"按角色收紧"的设计是 Claude Code 子代理系统的核心

### 决策 3：Agent 工具的触发是 LLM 自主决定还是计划系统控制？

**建议**：LLM 自主决定。`Agent` 工具和其他工具一样注册在工具列表中，LLM 自主决定什么时候 spawn 子代理。

**这是最关键的"智能化"决策之一**。当前 FlagHunter 的计划系统是**强制性的**（iteration 1 自动生成计划），这剥夺了 agent 自主决定"怎么做"的自由。正确的做法是：

- 把计划生成从"强制步骤"降级为"可选工具"
- 让 agent 自己决定：需要计划 → 调用 `generate_plan`；需要探索 → 调用 `Agent(type="Explore")`；可以直接做 → 直接调用工具
- 计划完成后自动退出（保留现有逻辑），但不强制首轮出计划

---

## 7. 从"执行器"到"智能体"的关键认知转变

FlagHunter 当前本质上是一个**计划驱动的执行器**：
```
用户任务 → 强制生成计划 → 按步骤执行 → 标记完成 → 退出
```

Claude Code 是一个**目标驱动的决策体**：
```
用户目标 → 理解目标 → 自主决定：
  ├─ 需要探索？→ Agent(Explore) → 汇总结果
  ├─ 需要规划？→ EnterPlanMode → 生成步骤
  ├─ 需要验证？→ Agent(Verification) → 检查结果
  ├─ 需要更多上下文？→ ToolSearch + grep → 理解环境
  ├─ 可以直接做？→ 直接工具调用
  └─ 完成了？→ 自检验证 → 退出
```

**做 Phase 1-2 的核心目标，就是让 FlagHunter 从上面的"执行器"变成下面的"决策体"。**

这个转变不靠更强的模型、更长的 prompt，而靠：
1. 权限门让 agent 在安全边界内自主行动（而不是每步都要人确认）
2. 子代理让 agent 能拆解复杂任务（而不是单线程死磕）
3. 工具搜索让 agent 能发现可用能力（而不是依赖 prompt 里列出的有限列表）
4. 思考分离让 agent 的推理过程可观察、可审计

---

## 8. 总结

Claude Code 成功的秘密不是某一个特性，而是一套**完整的 agent harness 设计原则**。它和 FlagHunter 之间不是"功能多少"的差距，而是"架构范式"的差异。

改进 FlagHunter 不需要重写整个项目。按 Phase 1→2→3→4 的顺序迭代，每个 Phase 产出可验证的能力提升，最终让 FlagHunter 从一个"会执行计划的工具"变成一个"会自己思考的智能体"。
