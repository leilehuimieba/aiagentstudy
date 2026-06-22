# How Claude Code Agent Is Designed and Implemented

- BestBlogs URL: https://www.bestblogs.dev/en/article/744fed55
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 18809
- Original publisher URL: https://juejin.cn/post/7638807947525816366

---

大家好，我是双越。wangEditor 作者，前百度 滴滴 资深前端工程师，慕课网金牌讲师，PMP，前端面试派 作者。

我正致力于两个项目的开发和升级，感兴趣的可以私信我，加入项目小组。

- 【划水AI】 Node 全栈 AIGC 知识库，包括 AI 写作、多人协同编辑。复杂业务，真实上线。
- 【智语】 AI Agent 智能体项目。一个智能面试官，可以优化简历、模拟面试、解答题目等。

本文介绍 Claude Code 智能体的设计和实现，核心的模块架构和流程。

## 源码泄漏事件

### 泄漏经过

2026 年 3 月 31 日，安全研究员 Chaofan Shou 在分析 Claude Code 的 npm 包（v2.1.88）时，发现包内附带了一个体积高达 59.8MB 的 .map 文件。这是 TypeScript 编译器生成的 Source Map——一种将编译后的 JavaScript 代码映射回原始 TypeScript 源码的调试文件，本不应该出现在发布包里。

原因很简单：Claude Code 使用 Bun 运行时进行打包，而 Bun 默认会生成 source map，打包脚本遗漏了排除该文件的步骤。就这样，整整约 51.2 万行、近 1900 个 TypeScript 文件的完整源码，以一种意外的方式进入了公众视野。

### 最令人惊讶的发现

研究者们深入分析之后，得出了一个出乎所有人意料的结论：

其中只有 1.6% 是真正的 AI 决策逻辑，其余 98.4% 都是确定性基础设施——权限控制、上下文管理、工具路由和错误恢复逻辑。

这个数字彻底颠覆了很多人对 AI 编程工具的想象。大多数人以为 Claude Code 的核心是某种精妙的 AI 推理机制，但实际上，真正调用模型的代码只是整个系统里薄薄的一层。支撑起整个产品的，是大量工程性极强、逻辑严密的"脚手架"代码。

这个发现有深刻的工程启示：构建一个可靠的 AI Agent，难点不在于调用模型，而在于如何管理模型周围的一切。

## 整体架构

### 架构全景图

### 各模块职责速览

- 入口层：解析 CLI 参数，完成初始化，按条件分发到五种运行模式之一。
- Agent 主循环：整个系统的驱动引擎，一个 while(true) 循环，负责协调所有其他模块。
- QueryEngine：与 Anthropic API 通信的唯一入口，封装了所有网络细节。
- 工具系统：插件化架构，40+ 内置工具 + 无限扩展的 MCP 外部工具。
- 权限控制：三种全局模式 × 四种工具权限等级的矩阵管控。
- 上下文压缩：五级梯度压缩策略，防止长任务因上下文溢出而崩溃。
- Memory 系统：三层架构，用"指针索引"代替"全量注入"，高效管理长期知识。

## 入口层

### 初始化阶段

main.tsx 是整个系统的入口文件，但它本身几乎不包含业务逻辑——它只负责"搭舞台"，然后把控制权交出去。启动时，它按顺序执行四个初始化步骤：

loadConfig() 按优先级合并多个配置源。优先级从高到低依次是：环境变量 → 项目级 CLAUDE.md → 用户级 ~/.claude/config → 内置默认值。这里有一个重要细节：CLAUDE.md 在这一步被一次性读入内存，后续不会再解析，这就是为什么修改 CLAUDE.md 之后需要重启 Claude Code 才能生效。

checkAuth() 查找 API Key，顺序是：ANTHROPIC_API_KEY 环境变量 → ~/.claude/auth 文件 → 提示用户登录。找不到则直接报错退出，这是最高优先级的前置条件。

registerTools() 将 tools/ 目录下所有工具加载到工具注册表（Tool Registry）。注意：此时只是"注册"元数据，不是真正初始化——标记了 defer_loading: true 的工具，要等到被实际调用时才会初始化。

detectMode() 读取命令行参数和环境变量，判断应该进入哪种运行模式，然后把控制权移交给对应的模块。从这一刻起，main.tsx 退出舞台。

### 五种入口方式

Claude Code 支持五种截然不同的运行模式，覆盖了从日常交互到 CI 自动化的全部场景。

Interactive 模式（默认）：直接输入 claude 启动，进入带有完整 UI 的交互对话循环。适合日常开发时的人机协作。UI 层由 React/Ink 驱动，支持键盘输入、流式输出和历史会话恢复（--resume <session-id>）。

Pipe 模式：当系统检测到 stdin.isTTY === false（即输入来自管道而非终端键盘），自动进入此模式。一次性读取 stdin 全部内容，执行完毕后退出，不进入交互循环。典型用法：

git diff | claude -p "帮我根据这份 diff 写一条规范的 commit message"cat error.log | claude -p "分析这个报错的根本原因"

Headless 模式：使用 -p 或 --print 参数时激活。不启动 UI，直接执行给定的 prompt，输出纯文本结果。与 Pipe 模式的区别在于触发条件——Pipe 是"输入来自管道"，Headless 是"显式声明无 UI 执行"。典型用法：

claude -p "给这段代码写单元测试" < utils.ts > utils.test.ts

SDK 模式：环境变量 CLAUDE_CODE_SDK_MODE=1 时激活，通常由官方 SDK 自动设置。通过 stdin/stdout 交换 JSON 消息，供其他程序（Python、Go 等）以编程方式控制 Claude Code，类似 Language Server Protocol 的设计思路。

SubAgent 模式：当环境变量 CLAUDE_SUBAGENT_MODE=1 时激活。这是被主 Agent 的 AgentTool 内部调用时自动触发的模式。子 Agent 拥有完全独立的上下文窗口，完成任务后将结果作为工具返回值传回父 Agent。

模式检测的优先级顺序是：SubAgent → SDK → Headless → Pipe → Interactive（默认兜底）。

### React/Ink 终端渲染器

Interactive 模式下，UI 层由 Ink 驱动。Ink 的核心思想是把 React 的组件树渲染到终端——你可以用写 Web 组件的方式写终端 UI。

这套渲染器采用游戏引擎式的脏检查优化：只重绘发生变化的行，而非每次刷新整个屏幕。这确保了在模型流式输出时，屏幕不会产生闪烁或撕裂。

架构上，UI 层和业务层通过共享的 AppState 对象通信，互不感知内部实现：

- UI 层负责捕获键盘输入、渲染消息气泡、展示流式 token
- 业务层（Agent 主循环）负责调用 QueryEngine、执行工具、管理状态
- 共享状态包括：messages[]、isLoading、currentToolCall、tokenUsage 等

这种分离让两层可以独立测试和替换，也是整个系统保持可维护性的基础之一。

## Agent Loop 主循环

### 七个阶段

Agent 主循环是整个系统的心脏。理解它，就理解了 Claude Code 的一切。

① 上下文加载：每轮循环开始时，系统构建本轮发送给模型的完整上下文。这包括：从 MEMORY.md 读取指针索引（体积小，始终驻留）、按需拉取被指针引用的主题文件、注入 CLAUDE.md 静态配置、以及计算当前剩余的 token 预算。

② 工具路由 & 延迟加载：决定本轮 API 调用中注入哪些工具的 schema。内置工具 40+，加上 MCP 外部工具可能有几百个，全部注入会耗尽大量 token。defer_loading 机制确保只有"本轮可能用到的"工具才会被注入（详见工具系统章节）。

③ 权限检查（预检） ：在发送 API 请求之前，对当前上下文中待执行的操作做粗粒度的权限过滤，并查询拒绝记录（DenialLog）——如果用户曾经拒绝过某个操作，这里会提前过滤掉，不再打扰。

④ 模型调用：整个循环中唯一真正调用 AI 的步骤，通过 QueryEngine.call() 完成。QueryEngine 内部处理所有网络细节：流式输出、错误重试、token 计费等。主循环只关心输入和输出，完全不感知 QueryEngine 的内部实现。

⑤ 响应解析 + stop_reason 路由：解析模型返回的内容，识别 stop_reason 并决定下一步走向。这是整个循环的控制流核心（详见下一节）。

⑥ 工具执行：当 stop_reason === 'tool_use' 时进入此阶段。先做精细的权限检查（包括向用户弹出确认提示），通过后调用对应工具的 execute() 函数，将返回的 tool_result 追加到 messages[]。

⑦ 状态更新 & 压缩检查：更新 token 计数，将当前 session 状态持久化到磁盘（支持 --resume 恢复），并检查是否需要触发上下文压缩策略。

### 伪代码

async function agentLoop(userMessage: string) {// 将用户消息加入历史 messages.push({ role: 'user', content: userMessage }) while (true) {// ① 上下文加载 const context = buildContext({ messages, // 完整对话历史 memoryIndex, // MEMORY.md 指针索引（始终在内存中） claudeConfig, // CLAUDE.md 静态配置（启动时加载一次） tokenBudget, // 当前剩余 token 预算 })// ② 工具路由：按需决定注入哪些工具 schema const tools = selectTools(context)// ③ 权限预检（查拒绝记录，粗筛）// 主要在步骤 ⑥ 精细检查，这里是快速过滤// ④ 调用模型（唯一的 AI 步骤） const response = await queryEngine.call({ messages: context.messages, tools: tools, system: context.systemPrompt, })// ⑤ 解析 stop_reason，决定走向 const { stop_reason, content } = response if (stop_reason === 'end_turn') {// 模型说"我完成了" → 输出给用户，结束本轮displayToUser(content) break } if (stop_reason === 'max_tokens') {// 上下文撑满 → 触发压缩，重置预算，重试 await compressContext() continue }// stop_reason === 'tool_use' → 执行工具// ⑥ 工具执行 const toolCalls = extractToolCalls(content) for (const call of toolCalls) {// 精细权限检查（可能弹出用户确认） if (!await checkPermission(call)) { messages.push(toolResult(call.id, 'Permission denied')) continue }// 执行并写回结果 const result = await executeTool(call) messages.push({ role: 'user', content: toolResult(call.id, result) }) }// ⑦ 状态更新updateTokenCount()persistSession() // 写磁盘，支持 --resumecheckCompression() // 是否需要触发压缩策略// 循环继续 → 模型将看到 tool_result 后决定下一步 }}

工具调用不会退出循环，而是把结果追加回 messages，让模型在下一轮看到工具执行结果再决定下一步。这就是 Claude Code 能"自主完成多步任务"的根本原因。

### stop_reason 状态机

stop_reason 只有三个值，但它们决定了循环的全部控制流：

- end_turn：模型认为任务完成，输出内容给用户，break 跳出循环，等待下一条消息。
- tool_use：模型要调用工具，附带工具名和参数。执行工具、将结果写回 messages[]，continue 回到循环顶部。
- max_tokens：生成过程中上下文窗口被填满，无法继续。触发压缩策略，重置 token 预算后重试当前轮次。

### 实例演示

来看一个真实场景：你让 Claude Code "找出项目里所有未使用的变量并删除"。

第 1 轮（stop_reason = tool_use）：模型思考后决定先了解项目结构。调用 BashTool，执行 find . -name "*.ts" | head -50，返回 38 个 TypeScript 文件的列表。tool_result 追加到 messages[]，循环继续。

第 2 轮（stop_reason = tool_use）：模型看到文件列表，决定运行静态检查。调用 BashTool，执行 npx tsc --noEmit 2>&1，返回 12 条"变量已声明但未读取"的 warning。由于输出较大，QueryEngine 自动用 MicroCompact 压缩工具输出后存入上下文。循环继续。

第 3 轮（stop_reason = tool_use）：模型分析 12 条 warning，决定一次性修改多个文件。它返回了 5 个 tool_use 块（Anthropic API 支持一次返回多个），对应 5 个文件的 FileEditTool 调用。权限检查弹出确认（ask 模式），用户确认后，5 个文件被依次修改。

第 4 轮（stop_reason = end_turn）：模型再次运行 npx tsc --noEmit 验证，0 个 warning。生成最终回复："已在 5 个文件中删除 12 个未使用变量，编译检查通过。" break 退出循环。

整个过程，用户只输入了一句话。模型自主决定了"读结构 → 静态分析 → 修改 → 验证"四步，每一步都是它在看到上一步的 tool_result 后做出的独立决策。

## QueryEngine 的作用

### 一句话说明

QueryEngine 是 Claude Code 与 Anthropic API 通信的唯一入口和智能 HTTP 客户端——你给它对话历史和工具列表，它替你处理好所有网络层的复杂性，返回模型的响应。

### 输入与输出

输入： messages[] 完整对话历史 tools[] 工具 schema 列表（只含 name/description/input_schema，不含 execute 函数）system 系统提示词输出： stop_reason 'end_turn'|'tool_use'|'max_tokens' content[] 文本块 + 工具调用块的混合数组 usage { input_tokens, output_tokens, cache_read_tokens, ... }

### 核心能力详解

流式输出（Streaming） ：模型的 token 是一个个生成的，QueryEngine 通过 Server-Sent Events 接收流式响应，边接收边推送给 UI 层。用户看到的"字符一个个出现"的效果就来自这里。流式模式还有一个好处：如果用户中途按 Ctrl+C，可以立即中断，不必等到整个响应生成完毕。

缓存（Prompt Caching） ：Anthropic API 支持对系统提示词和长对话历史做服务端缓存（Cache Breakpoints）。QueryEngine 自动在合适的位置插入缓存标记，让重复内容（如固定的工具 schema、项目上下文）命中缓存，显著降低 API 成本和响应延迟。usage 字段中的 cache_read_tokens 就是缓存命中的 token 数。

错误后重试：QueryEngine 内置了完整的重试策略：

- 网络错误：指数退避重试，最多 3 次，间隔 1s → 2s → 4s。
- 429 Rate Limit：解析响应头中的 Retry-After，精确等待对应时间后重试，不做无效轮询。
- 500/502/503 服务端错误：同样指数退避，与网络错误共享重试计数。
- 超时：单次请求超过 120 秒则超时，触发重试逻辑。

Token 计费与成本追踪：每次 API 调用后，QueryEngine 从 usage 字段提取 token 消耗，累加到会话级的成本统计。这是 Claude Code 能在右上角实时显示"本次会话花费 $X.XX"的数据来源。同时，token 消耗会用于更新上下文预算，触发压缩策略的判断。

双模型策略：QueryEngine 内部并非只调用一个模型。对于需要深度推理的主循环调用，使用 Opus；对于上下文压缩摘要、工具输出摘要等辅助任务，自动切换到 Haiku。Opus 更强但更贵，Haiku 更快且便宜——这个切换对主循环完全透明，每天节省大量 API 成本。

## 工具系统

### 类型定义

所有工具都继承自 Tool.ts 中定义的抽象基类，该基类只有四个核心字段：

abstractclassTool {// ① 工具名：模型调用时使用的唯一标识abstractname: string// 例："bash", "read_file", "agent"// ② 输入 Schema：定义模型调用时的参数格式（JSON Schema）abstractinput_schema: JSONSchema// 模型必须按此格式传参，否则直接报错，不执行// ③ 权限等级：决定需要什么授权才能运行abstractpermission_level: 'read' | 'write' | 'execute' | 'network'// 主循环在步骤 ③ 和步骤 ⑥ 都会检查这个字段// ④ 执行函数：真正做事的地方abstractexecute(input: ValidatedInput): Promise<ToolResult>// 返回的 ToolResult 会被追加到 messages[] 作为 tool_result}

40+ 个工具，每一个都是在实现这四个字段，没有其他魔法。工具系统之所以可以无限扩展，正是因为接口足够简单——任何人实现这个接口，就能给 Agent 增加新能力。

### 三个经典工具

BashTool：权限等级 execute，风险最高。接受 command、timeout、workdir 三个参数，在指定目录执行任意 shell 命令。有黑名单保护（禁止 rm -rf / 等危险命令），默认 30 秒超时强制中止。这是工具系统里能力最强的工具，权限系统的大部分复杂度都是为了管控它而存在的。

FileReadTool：权限等级 read，风险最低。接受 path、offset、limit 三个参数，读取指定文件的内容。单次最多返回 2000 行，超出自动截断并提示，防止大文件直接撑满上下文窗口。它是 ask 模式下唯一无需用户确认即可自动执行的工具类别。

AgentTool：权限等级 execute，性质特殊。接受 task、context、tools 三个参数，在内部以 sub-agent 模式启动一个全新的 Claude Code 子进程，将任务交给它独立完成，最终把子 Agent 的输出作为 tool_result 返回给父 Agent。这是多 Agent 协作架构的核心入口。

### 工具调用流程

Agent 主循环响应解析器Tool Registry权限系统具体工具API 允许一次返回多个 tool_use 块例如并行读取多个文件或启动多个子 Agentpar[并行执行多个工具]解析模型响应返回 tool_use 和多个 tool callsget read_file toolToolDefinitioncheckPermissionallowedexecute a.tstool_result_1get read_file toolToolDefinitionexecute b.tstool_result_2get agent toolToolDefinitioncheckPermissionask userexecute sub agenttool_result_3push tool results into messagescontinue next agent loopAgent 主循环响应解析器Tool Registry权限系统具体工具

关于并行调用：Anthropic API 允许模型在一次响应中返回多个 tool_use 块。主循环用 Promise.all 并发执行所有工具，然后将所有 tool_result 一起追加到 messages[]。这是 Claude Code 能并行读取多个文件、或同时启动多个子 Agent 的底层机制。

### 延迟加载 defer_loading

Claude Code 内置 40+ 工具，加上用户配置的 MCP Server 工具，总数可能超过 200 个。每个工具的 input_schema 平均约 300 token。如果每次 API 调用都注入全部工具，仅工具 schema 就会消耗 6 万+ token，严重压缩留给对话内容的空间。

defer_loading 机制解决了这个问题：

interfaceToolDefinition {name: stringinput_schema: JSONSchemapermission_level: PermissionLeveldefer_loading: boolean// 是否延迟加载 load_when?: (ctx: Context) =>boolean// 触发条件execute: (input: unknown) =>Promise<ToolResult>}functionselectTools(context: ConversationContext): ToolDefinition[] {return [...toolRegistry.values()].filter(tool => {if (!tool.defer_loading) returntrue// 核心工具：始终注入if (!tool.load_when) returnfalse// 无条件：始终不注入return tool.load_when(context) // 按条件判断 })}

核心工具（bash、read_file、glob、grep）标记 defer_loading: false，始终注入。上下文相关工具（如 web_fetch）和 MCP 外部工具标记 defer_loading: true，只有当 load_when(ctx) 返回 true 时才注入。实践中，每轮调用只注入 8-12 个工具，节省了约 96% 的工具 schema token 消耗。

## 权限控制

### 全局权限模式

Claude Code 提供三种全局权限策略，通过 --permission-mode 参数或 CLAUDE.md 配置：

- auto 模式：所有工具调用自动执行，不询问用户。适合 CI/CD 流水线或完全信任的自动化场景，但出错时没有任何拦截机制。
- ask 模式（默认）：write/execute/network 级别的操作需要用户确认，read 级别自动放行。日常开发推荐使用，在效率和安全之间取得平衡。
- manual 模式：所有操作（包括 read）都需要确认。极度谨慎的场景使用，但会严重降低效率。

### 工具权限等级

每个工具在定义时静态声明自己的 permission_level，共四个级别：

- read：只读操作，FileReadTool、GlobTool、GrepTool。不修改任何状态，ask 模式下自动放行。
- write：修改磁盘文件，FileEditTool、FileCreateTool。ask 模式下首次需要确认。
- execute：执行任意命令，BashTool、AgentTool。影响范围最广，需要明确授权。
- network：发起网络请求，WebFetchTool 和 MCP 工具。防止数据意外外泄。

两个维度交叉形成权限判断矩阵：

//权限判断矩阵（两个维度交叉）constpermissionMatrix= {//autoaskmanualread: { auto:true, ask:true, manual:false },write: { auto:true, ask:false, manual:false },execute:{ auto:true, ask:false, manual:false },network:{ auto:true, ask:false, manual:false },}//false=需要用户确认才能执行

### 拒绝跟踪与优雅降级

当用户拒绝某个操作后，系统需要记录这个意图——否则 Agent 可能在同一任务中反复请求同样的权限，持续打扰用户。这就是拒绝跟踪（Denial Tracking）系统的作用。

下面是这个系统的 46 行核心实现：

classDenialLog {// 会话级拒绝记录（重启后清空，不做持久化）private denied = newSet<string>()private allowed = newSet<string>() // "本次会话全部允许"的工具// 检查是否已被拒绝（最高优先级）isDenied(toolName: string): boolean {returnthis.denied.has(toolName) && !this.allowed.has(toolName) }// 记录拒绝record(toolName: string) {this.denied.add(toolName) }// 用户选择"本次会话全部允许" → 覆盖之前的拒绝allowForSession(toolName: string) {this.allowed.add(toolName) }}asyncfunctioncheckPermission(tool: ToolDefinition): Promise<PermissionResult> {// 第一关：查拒绝记录（最高优先级，直接拒绝不再询问）if (denialLog.isDenied(tool.name)) {return { allowed: false, reason: 'previously_denied' } }// 第二关：查权限矩阵const needsConfirm = !permissionMatrix[tool.permission_level][currentMode]if (!needsConfirm) {return { allowed: true } // 直接放行 }// 第三关：弹出用户确认const answer = awaitaskUser({message: `Allow ${tool.name}?`,options: ['Allow once', 'Allow this session', 'Deny', 'Deny this session'] })if (answer === 'Deny' || answer === 'Deny this session') { denialLog.record(tool.name) // 写入拒绝记录return { allowed: false, reason: 'user_denied' } }if (answer === 'Allow this session') { denialLog.allowForSession(tool.name) }return { allowed: true }}

代码之所以只有 46 行，是因为简单性是刻意追求的。权限系统越复杂，出现漏洞的可能性越高。这套实现编码了一个核心原则：当用户失去信任时，优雅降级，不反复打扰。 被拒绝的操作返回 "Permission denied" 作为 tool_result，模型看到后会寻找其他方案或告知用户，而非陷入无限重试。

## 上下文压缩

### 五级上下文压缩策略

Agent 运行时，messages[] 随着每一轮工具调用不断膨胀。不加管理，10-20 轮后必然触达上下文窗口上限，Agent 崩溃或被迫截断历史。Claude Code 设计了五级梯度压缩策略，从轻到重按需触发：

Snip（零成本） ：直接从 messages[] 头部删除最旧的若干轮对话（保留系统消息和最近 N 轮）。有损且粗糙，但零延迟、零成本，是最后的紧急兜底手段。

MicroCompact（零成本） ：在工具输出写入 messages[] 之前，检查其长度。超过阈值（约 2000 行）则直接截断，末尾追加 [Output truncated: X lines omitted]。纯本地字符串操作，无语义理解，快但精度差——适合日志、编译输出等信息密度低的场景。

ApiMicroCompact（低成本） ：与 MicroCompact 的区别在于"有语义"。把超大的工具输出发给 Haiku，生成结构化摘要后存入磁盘缓存（key 是输出内容的 hash）。后续引用摘要而非原始输出。相同命令重复执行时，可直接命中缓存，无需再次 API 调用。

AutoCompact（中成本） ：当上下文剩余 token 低于 13,000 时触发（留出压缩本身所需的空间）。调用 Haiku，生成最多 20,000 token 的结构化摘要替换旧历史，压缩后预算大幅恢复。内置熔断机制：连续失败 3 次（如摘要本身太长），停止重试，降级到 Snip。

Full Compact（高成本） ：用户手动执行 /compact 或系统开启 ContextCollapse feature flag 时触发。彻底压缩整个对话历史，同时重新注入：最近访问的文件（每文件上限 5,000 token）、当前活跃的任务计划、相关工具 schema。完成后工作预算重置为 50,000 token，相当于给长任务一个全新的"干净起点"。

### 压缩调用流程

async function checkCompression(state: AgentState): Promise<void> { const remaining = state.totalBudget - state.usedTokens// 工具输出截断：在步骤 ⑥ executeTool 的输出阶段执行// （MicroCompact / ApiMicroCompact 在这里，不在 checkCompression 里）// AutoCompact：接近上限时触发 if (remaining < 13_000) { const success = await autoCompact(state) if (!success) {// 压缩失败，熔断计数 state.compactFailCount++ if (state.compactFailCount >= 3) {// 连续失败 3 次 → 降级到 Snipsnip(state) state.compactFailCount = 0 } } else { state.compactFailCount = 0// 压缩成功，预算恢复 state.usedTokens = state.usedTokens * 0.3 } return }// Snip：极端情况下的兜底（ratio > 0.98） if (state.usedTokens / state.totalBudget > 0.98) {snip(state) }}

优先级从高到低：AutoCompact > Snip。MicroCompact 和 ApiMicroCompact 在工具执行阶段独立运作，不通过 checkCompression 触发。Full Compact 是用户主动触发的独立操作。

### AutoCompact 并不随意

AutoCompact 不是让模型"随便总结一下"，而是生成固定结构的摘要，确保关键信息一定被保留：

const AUTOCOMPACT_PROMPT = `你是一个对话历史压缩助手。将以下对话压缩为结构化摘要。必须包含以下章节，不得省略：## 已完成的任务（列出本次会话中已经完成的所有操作，要具体）## 关键发现（代码结构、重要文件位置、已知问题、重要约束等）## 当前状态（此刻正在做什么，进行到哪一步）## 待完成事项（还需要做什么，按优先级排列）## 重要决策（已经做出的技术决策和原因，避免重复讨论）压缩后长度不得超过 20,000 token。`

固定章节的设计有一个深层用意：每次压缩后，模型都能从同样结构的上下文里找到它需要的信息，行为保持一致。 如果摘要格式每次不同，模型在压缩后的表现可能会出现难以预测的漂移。这也是 AutoCompact 的"优雅"之处——它不只是缩短了上下文，而是重新整理了上下文，让 Agent 能以稳定的状态继续工作。

## 三层 Memory 架构

### 架构设计

上下文压缩解决了"历史如何瘦身"，但还有另一个问题：项目相关的长期知识（认证逻辑、数据库 schema、API 规范……）该如何在多次会话之间持久保存，又不占满上下文？

答案是三层 Memory 架构：

第一层：MEMORY.md 指针索引（始终在上下文中）

这是唯一保证始终驻留在上下文窗口的文件，但它本身非常轻量——每条索引约 150 字符，整个文件保持在 ~2,000 token 以内。它只存"指针"，不存内容：

# Memory Index- auth-system → memory/auth.md (JWT 实现, refresh token 逻辑)- db-schema → memory/db-schema.md (users 表, orders 表结构)- api-design → memory/api-design.md (REST 规范, 错误码定义)- deployment → memory/deploy.md (CI/CD 流程, 环境变量清单)

第二层：主题文件（按需加载）

被 MEMORY.md 引用的具体知识文件，存储在 memory/ 目录下。每个文件聚焦一个主题，可以任意详细。需要时，模型通过 FileReadTool 读取对应文件，用完后无需保留在上下文——下次需要时再读即可。

第三层：CLAUDE.md 静态配置

项目级的固定偏好和约定，启动时一次性读入，始终驻留。适合存放：编码规范、工具链偏好、项目特殊约束等不会频繁变化的配置。

### 关键洞见

永远不把全量知识放入上下文，只放指针。

这个设计和数据库索引的思路完全一致：数据库不会把所有数据加载到内存，而是维护一个精简的 B+ Tree 索引，需要时按索引定位磁盘上的具体数据。Memory 系统做的是同样的事——用 2,000 token 的索引管理任意大小的知识库，按需取用，不预先占用上下文空间。

## SubAgent

### SubAgent 架构设计

User父 Agent（主进程）AgentTool子 Agent 进程独立上下文窗口\n独立运行主循环\n多轮工具调用...par[并行启动 3 个子 Agent]"重构 auth 模块，同时更新测试和文档"分析任务，决定拆分为 3 个子任务tool_use: agent\n{ task: "重构 auth 模块" }spawn(claude, SUBAGENT_MODE=1)\nstdin: { task, context, tools }stdout: 最终输出文本tool_result: "auth 模块重构完成..."tool_use: agent\n{ task: "更新所有单元测试" }spawn(claude, SUBAGENT_MODE=1)测试更新完成tool_resulttool_use: agent\n{ task: "更新相关文档" }spawn(claude, SUBAGENT_MODE=1)文档更新完成tool_result收集 3 个 tool_result，生成最终回复"三个子任务均已完成..."User父 Agent（主进程）AgentTool子 Agent 进程

关键设计决策：父子 Agent 完全隔离。 子 Agent 拿不到父 Agent 的 messages[]，也感知不到其他子 Agent 的存在。父子之间的接口只有两个：输入是 task + context 文本描述，输出是子 Agent 的最终回复文本。

这个强隔离带来三个好处：① 上下文干净——子 Agent 的多轮工具调用不污染父 Agent 的上下文；② 可并行——多个子 Agent 互不依赖，可以真正同时运行；③ 可替换——父 Agent 不关心子 Agent 内部实现，只要最终结果符合预期。

### AgentTool

const AgentTool: ToolDefinition = { name: 'agent', permission_level: 'execute', // 继承调用方权限 defer_loading: false, // 核心工具，始终可用 input_schema: {type: 'object', properties: { task: { type: 'string', description: '子任务的完整描述，越具体越好' }, context: { type: 'string', description: '传递给子 Agent 的背景信息' }, tools: { type: 'array', description: '允许子 Agent 使用的工具列表' }, }, required: ['task'] }, execute: async (input) => {// ① 以 sub-agent 模式启动子进程const child = spawn('claude', [], { env: { ...process.env, CLAUDE_SUBAGENT_MODE: '1', // main.tsx 据此进入 subagent 模式 CLAUDE_PARENT_TASK: input.task, } })// ② 通过 stdin 传入任务描述// 注意：父 Agent 的 messages[] 不传给子 Agent// 子 Agent 只知道自己的任务，完全不知道父 Agent 的上下文 child.stdin.write(JSON.stringify({ task: input.task, context: input.context, tools: input.tools ?? defaultSubAgentTools, }))// ③ 等待子进程完成（可与其他子 Agent 并行等待）const result = await waitForCompletion(child)// ④ 子 Agent 的最终输出作为 tool_result 返回// 父 Agent 只看到这一句话，不知道子 Agent 内部跑了多少轮return {type: 'tool_result', content: result.finalOutput, } }}

父 Agent 调用多个 AgentTool 时，主循环用 Promise.all 并发执行，实现真正的并行处理：

// 主循环步骤 ⑥：并行执行多个工具（包括多个 AgentTool）const results = awaitPromise.all( toolCalls.map(call =>executeToolCall(call)))// 所有结果一起追加到 messages[]for (const [call, result] ofzip(toolCalls, results)) { messages.push(toolResult(call.id, result))}

## MCP 集成

### MCP 是什么

MCP（Model Context Protocol）是 Anthropic 提出的开放协议，解决一个核心问题：如何让外部服务以标准方式暴露工具给 Claude Code，而无需 Anthropic 为每个服务单独编写内置工具。

任何服务——Asana、GitHub、自建数据库、企业内部 API——只要实现 MCP 协议，就能被 Claude Code 当作工具使用，不需要修改 Claude Code 的任何代码。MCP 之于 Claude Code，类似 USB 协议之于电脑：定义了标准接口，让外设可以即插即用。

### 集成过程

启动时握手与工具发现：Claude Code 启动时，对每个配置的 MCP Server 发起 initialize 请求，握手成功后立即请求 tools/list，获取该 Server 提供的工具列表和每个工具的 schema。

注册到 Tool Registry：Claude Code 将 MCP 返回的工具 schema 包装成内部 ToolDefinition 格式，注入工具注册表，并标记 defer_loading: true（MCP 工具几乎全部延迟加载）。从这一刻起，MCP 工具和内置工具在主循环眼里完全一致。

运行时调用：模型需要调用 MCP 工具时，execute() 函数内部由 mcpProxy 将调用转发给对应的 MCP Server，返回结果包装成标准 tool_result，写入 messages[]。整个过程对主循环透明。

配置方式：

# CLAUDE.mdmcp_servers:-name:asanatype:httpurl:https://mcp.asana.com/sse-name:my-db-tooltype:stdiocommand:node./mcp-server/index.js

MCP Server 支持三种传输方式：stdio（本地子进程）、SSE（HTTP Server-Sent Events）和 HTTP（标准 REST）。无论哪种传输方式，Claude Code 侧的集成逻辑完全相同。

## 总结

学完 Claude Code 的整个架构，最深的感受是：这不是一个"AI 项目"，而是一个"以 AI 为核心的工程项目"。

整个系统中，真正属于 AI 的部分只占 1.6%——就是 QueryEngine 里调用 Anthropic API 的那一段代码。其余 98.4% 都是严肃的工程：精心设计的状态机、多层次的权限系统、梯度化的资源管理策略、可组合的插件架构。

这揭示了一个对所有 AI 应用开发者都有价值的洞见：

让 AI Agent 能做什么，取决于工具系统。让 AI Agent 做得好不好，取决于上下文管理。让 AI Agent 在真实任务中稳定运行，取决于权限控制和错误恢复。 模型本身的能力固然重要，但包裹在模型外面的工程基础设施，才是决定产品体验的关键。

Claude Code 的每一个设计决策都体现了这种思维：用 defer_loading 把 token 留给真正有用的内容，用 DenialLog 的 46 行代码保证用户体验不被权限弹窗破坏，用五级压缩策略让 Agent 在任意长的任务中都能稳定工作，用强隔离的 SubAgent 实现安全的并行协作。

构建可靠的 AI Agent，本质上是一道工程题，不是一道 AI 题。
