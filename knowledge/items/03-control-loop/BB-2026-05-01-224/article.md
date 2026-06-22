# On AI Super Apps

- BestBlogs URL: https://www.bestblogs.dev/en/article/f84f59f3
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 18823
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247491935&idx=1&sn=870264e741e2c9634cc9c32bebe81383

---

从模型神话到软件工程秩序的回归...

过去几年，我们几乎默认了一个判断：AI 的终点，是更聪明的模型。更长的上下文，更强的推理能力，更低的幻觉率，更接近人类的规划、协作与自我修正。这个判断当然没有错，模型能力仍然是这场变革的发动机。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=4cd2fe5a&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz_png%2FoghJwiaPb1CupHicSIZNCpx3mbEkic781icYPxtv0N6mP9V5uwuBkKyibTJsdlQL6TyIicAhsO4licR20ibTqjxK3JChpNibhIY6IsmfkTfNg77cLYWk%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

但最近一系列变化，开始露出另一条更耐人寻味的线索。

Claude 开始认真强调 HTML 交互输出的价值，不再满足于 Markdown 式的线性文本（我之前也提到过类似观点：浏览器不会退出历史舞台，一旦将人拉入 agent loop 回路中，会让一切都复杂起来）；Codex 正从一个代码助手，演化成横跨桌面端、移动端、浏览器、终端、长任务、插件与 skills 的 Agent 工作台；MCP 试图用标准协议连接模型、工具、资源与外部系统；Skills 用得越多，越不像一句 prompt，反而像一个带说明书、脚本、资源文件、运行约束和交互界面的小型 Web 应用。

这很反直觉。AI 已经进入长上下文、多模态、复杂推理和自主任务阶段，为什么最后又频繁回到 HTML、JavaScript、浏览器、iframe、文件系统、终端、权限、沙盒和状态机这些“旧东西”？

表面看，这像是一种技术倒退。深处看，它更像是 AI 落地过程中不可避免的一次工程收敛。

早期 AI 给人的错觉是：模型会吞掉一切。Prompt 可以解决一切，长上下文可以解决一切，多 Agent 可以解决一切。只要模型继续变强，外部工程结构似乎都会退到幕后。可当 AI 真正开始读写文件、修改代码、控制浏览器、调用工具、执行命令、影响业务流程时，问题立刻变了：我们不再只关心它能不能生成答案，而要关心它如何行动、如何受限、如何恢复、如何审计，以及人类如何在关键节点重新接管。

这也是 Codex、Claude、MCP、Skills 和 HTML 交互在同一时间变得重要的原因。它们看似属于不同产品和技术栈，背后却都指向同一个变化：AI 正在从“回答系统”走向“行动系统”。回答可以停留在文本里，行动必须进入环境、协议、状态、权限和界面。

所以，本文探讨的并不是某个产品更新，也不是 Markdown 与 HTML 的格式之争，而是一个更大的架构转向：当非确定性的模型开始进入现实世界，它必然要重新接入那些最成熟、最稳定、最经得起摔打的软件工程结构。浏览器、文件系统、终端、Git、协议、沙盒、组件、状态机，正在被重新组织成 Agent 时代的基础设施。

这也许就是当前 AI 技术大融合最值得追问的地方：AI 并没有绕开旧世界。它正在借助旧世界，获得进入现实的形状。

结合 AI 趋势 & 技术背景，会发现这一切并不突然。推荐阅读：

- 深度思考：聊聊 AI 发展趋势

- 浅谈 AI 浏览器

- Agent 趋势浅思：原生化 & CLI 化

- 从 Prompt Engineering 到 Context Engineering

- 第一个 Agent 从 Pi 开始

- AI 编程生态：Anthropic 收购 Bun 意味着什么？

- 深度思考：聊聊 AI 发展趋势

- 深度解析：Codex Pet Skill

- 深度解析：Harness Engineering

- 深度解读：OpenClaw 架构及生态

- 深度解析：Claude Code 源码

- 深度解析：Claude Code Cowork

- 深度解析：Anthropic MCP 协议

- AI 操作系统：从指令到意图

- Agent Memory 架构本质

- AI 时代下的“认知投降”

- AI 浪潮下的开发者，又该何去何从？

- ...

Codex 超级入口

Codex 的变化，已经不能再用“代码助手”来概括。它正在跨过“代码片段补全”，进入“开发任务组织”阶段：围绕一个目标读仓库、改文件、跑命令、看页面、等审批、修错误、继续推进。真正关键的不是它更会写代码，而是它把本地执行、远程任务、浏览器观察、移动端控制、审批流、长任务和 skills 收束进同一个 Agent run 里。终端、浏览器、文件系统、Git、移动端和云端环境，不再是散落的工具，而是被重新编排进同一个行动回路。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=8e31b6f4&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FoghJwiaPb1CsrcorEtNKSgwULibsQcHMiaicd65KI1LYCptW1bbcLDqvYj3FuAfcKekzFcia9Fz2wYib9wOyERk3GciajyIMg0mic8bzTfWFUs09nxw%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

与此相呼应的，还有 Claude Cowork[1] 这类产品形态。Codex 更偏开发者场景，围绕代码库、终端、浏览器和远程执行环境组织任务；Cowork 更偏通用知识工作和企业流程，通过图形界面、连接器和插件，把法律、财务、运营、协作等工作流接入 Claude。它们表面上面向不同人群，底层却在争夺同一个位置：谁能成为用户真实工作流的控制面。

与其说这些产品要“接管用户操作系统”，不如说它们正在重写操作系统之上的行动层。传统 OS 管文件、进程、窗口和权限；新一代 Agent 宿主管理的，是目标、上下文、工具、审批、执行状态和可回滚工件。AI 不再只是悬浮在聊天框里的回答者，而是在逼近一个更危险、也更有想象力的位置：它开始进入用户的工作现场，组织行动，维持上下文，并在关键节点等待人类授权。

这才是 Codex 和 Cowork 真正值得警惕也值得兴奋的地方。它们争夺的不是聊天入口，而是工作流的主控权；不是替你多生成几段文本，而是把“人如何驱动软件完成任务”这件事，重新铺一遍底层线路。

多轨运行模式 & 沙盒隔离

在桌面端架构中，Codex 展现出了对现代软件工程复杂性的深刻理解。它并未采用单一的黑盒执行流，而是构建了极其明确的“多轨运行模式”，承认不同任务具有截然不同的隔离级别：

- 本地模式（Local）：Agent 贴着当前物理项目目录运行，适用于极短反馈闭环的局部 Bug 修复。它的优势是极致的快，但风险也最为直接。

- 工作树模式（Worktree）：针对重构和破坏性实验，系统在后台利用 Git Worktree 隔离出独立的物理工作区。它不是简单的后台线程，而是将 Agent 的破坏力死死封印在一个易于审查和瞬间回滚的版本控制边界内。

- 云端模式（Cloud）：将算力密集型的长周期任务剥离出本地机器，推向远程容器环境，实现了执行状态与物理主机的解绑。

为了保障这种多轨运行的安全性，Codex 引入了极其严格的沙盒化隔离机制。在 Windows 平台上（codex windows[2]），Codex 摒弃了对 WSL（Windows Subsystem for Linux）或重量级虚拟机的依赖，直接利用原生的 PowerShell 构建沙盒环境，这不仅大幅降低了系统的资源开销，还从操作系统内核层面限制了 AI 代理越权访问核心文件或发起未授权网络请求的可能。这种对审批流（Approvals）和沙盒边界的精确控制，使得“让 AI 自由接管操作系统”这一愿景变得工程上可控。

浏览器双轨控制

在处理非结构化 Web 界面和浏览器自动化任务时，Codex 采取极为务实且精密的“双轨制”策略：应用内浏览器（In-app Browser）与独立 Chrome 扩展程序（Chrome Extension）并行工作。

应用内浏览器主要被设计为一个封闭的、用于快速迭代的本地沙箱。它专注于处理本地开发服务器（如 localhost:3000）或无需身份验证的静态页面。在这个受限的视图中，Codex 能够精准读取渲染后的 DOM 树，直接接收用户对特定 UI 元素（例如悬浮框溢出、加载状态异常）的视觉反馈，并针对性地进行 DOM 节点的原子化修复。由于这种操作不涉及复杂的 Cookie 传递、第三方追踪脚本或跨域安全策略，因此它是极其高效且易于回滚的。研究显示，用户应当将此阶段的任务保持在极小的范围内，专注于验证特定的视觉状态，如空状态、加载中或错误反馈界面。

然而，当自动化任务超出了本地测试的物理范畴，涉及复杂的身份验证流程（OAuth）、受保护的历史会话，或需要操作如 Salesforce、LinkedIn 等高度封闭的第三方 SaaS 平台时，Codex 会自动将其执行流移交至专用的 Chrome 扩展程序。该扩展程序赋予了 AI 代理触达真实用户底层状态的特权，它能够接管带有登录态的常规浏览器配置文件，进行页面内的数据抓取、表单填写和跨标签页的复杂业务编排。为了防止 AI 滥用这些宽泛的浏览器权限（如读取所有网站数据、管理下载），Codex 实施了严格的“每次交互前询问（Ask before interaction）”协议，并辅以域名级别的白名单（Allowlist）和阻断名单（Blocklist）机制，在赋予智能代理空前执行力的同时，设立了不容跨越的安全边界。

控制面与执行面解耦

Codex 上手机，不只是多了一个入口（Work with Codex from anywhere[3]）。真正变化发生在工作流里：代码继续在 Mac、本地开发机、Devbox 或远程环境里跑，编译、测试、依赖管理、文件读写、终端命令也留在这些更稳定的地方。手机接过来的，是进度查看、结果审查、命令批准、模型切换和任务纠偏。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=ed68c64c&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz_png%2FoghJwiaPb1CvNpL0LOBickvJ8QGic3nQib8ygKUb5yTcIFwVSeceS3naTpPvibWjNye7mW179Gr1NFoEVyXbZaIbNicZV5VsNYkYnuJuWibtmuVqLE%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

这避开了移动设备最尴尬的短板。手机不适合长时间跑构建，不适合管理复杂依赖，也不适合承载完整项目目录和本地凭据。把开发环境硬塞进手机，只会制造更多同步、权限和稳定性问题。Codex 选择了更现实的做法：项目现场留在原地，移动端只拿控制权。

这样一来，开发任务被拆成两层。执行环境保存真实状态：未提交变更、环境变量、测试缓存、依赖版本、本地工具链，都继续贴着项目运行。移动端看到的，则是被整理后的任务信息：线程状态、终端输出、代码 diff、错误反馈、审批请求和运行结果。用户不需要远程接管整台机器，只需要在关键节点做判断。

这和 OpenClaw 的思路有相通之处。OpenClaw 通过 Gateway + IM 把用户入口和执行环境分开，任务可以从聊天软件进入系统，Agent 在另一端持续运行。Codex 走的是第一方产品路线：ChatGPT mobile 负责入口，桌面 Codex / 本地环境负责执行，中间用会话状态、事件流、审批请求、终端输出和 diff 串起任务过程。二者都在做同一件事：让人类不必和 Agent 的执行现场绑定在一起。

这个拆分带来的第一个变化，是环境不用搬家。真实开发依赖完整现场：目录结构、构建脚本、依赖版本、本地配置、测试数据、未提交状态。同步到手机既不现实，也没必要。Agent 贴着真实环境行动，手机负责看和管，反而减少了状态偏差。

第二个变化发生在安全边界上。移动端远程控制并不等于把整台开发机交给远端黑盒。更合理的粒度应该落在具体动作上：批准某个命令，确认某次变更，放行某个高风险操作。授权对象从“整个环境”收缩到“具体副作用”。对 Agent 系统来说，这个差异很大。前者像托管机器，后者像治理行动。

长任务场景里，这种结构尤其有用。/goal 这类任务会持续写代码、跑测试、读错误、改实现、再验证。过去开发者得守在电脑前，随时处理审批、失败和分叉。现在人可以离开工位，只在手机上处理关键节点。Agent 继续推进，人类负责刹车、转向和验收。

所以 Codex 移动端改变的不是屏幕尺寸，而是开发任务的空间关系。执行环境可以固定，控制入口可以流动。桌面、本地环境、远程机器、浏览器、终端、手机，不再只是几个孤立入口，而是在同一个任务生命周期里分工协作：有的执行，有的观察，有的审批，有的纠偏。

这也是 Codex 接近分布式 Agent 工作台的地方。AI 编程不再被锁在一台电脑前，开发者也不再必须陪着 Agent 跑完整个过程。任务在真实环境里持续推进，人类从任意入口介入，把控制权从“坐在机器前操作”改成“在关键节点调度”。

Agentic Web 运行时

如果剥开 Codex 或 Claude Artifacts 的华丽外衣，我们会发现下一代 AI 应用的底层结构已经高度固化。这套被称为 Agentic Web Runtime 的运行时架构，像素级地复刻了现代分布式软件系统的经典分层：

- Surface（展现交互层）：跨越桌面、移动、IDE 和 IM 的全渠道入口，其核心不在于界面形态，而在于共享同一个底层任务生命周期。

- Runtime（状态伺服层）：负责维护上下文、记忆和执行线程，Codex 的 /goal 和 Ralph Loop 皆运行于此，确保 AI 不再是孤立响应，而是持续的状态推进。

- Capability（外部能力层）：MCP（模型上下文协议）和 Agent Skills 在此汇聚。

- Governance（治理审计层）：包含 Agent 的运行手册（Runbooks）、变更版本控制、离线评估脚手架以及基于阈值的回滚策略。在 2026 年，控制 Agent 运行成本和爆炸半径的治理层，已成为系统设计的核心考量。

- Artifact（工件物化层）：AI 的输出从“纯文本”升维为 Markdown 报告、结构化 JSON、A2UI 意图数据以及 HTML 交互原型。

早期的工具调用（Tool Calling）更像一次简单的函数调用：模型选择一个工具，传入参数，拿回结果。这种方式可以解决局部问题，却很难支撑复杂生产环境里的权限、状态、失败恢复、用户确认和结果呈现。MCP 的普及，正是在补这层缺口：它用传统的 Client-Server 架构，把 Agent 宿主与外部能力拆开，让工具、资源和上下文不再被硬编码进单个应用，而是通过相对稳定的协议边界暴露出来。

但 MCP 解决的主要是“能力如何连接”。真正让 Agent 变得可用的，还需要另一层东西：任务经验如何被封装。Skills 的演进就在这里显得重要。一个复杂 Skill 已经不再是一段虚无缥缈的 prompt，而更像一个可安装的任务包：里面有 Markdown 说明书、输入输出约束、脚本、资源文件、验证逻辑、错误处理策略，必要时还会配合宿主生成可交互的 UI 工件。它打包的不是单个函数，而是一整套“如何完成这类任务”的工程经验。

如果把一个 Skill 类比成前端微应用，那么 SKILL.md 就有点像它的 index.html。在传统 Web 应用里，index.html 是浏览器进入应用的入口：它声明页面结构，加载脚本、样式和资源，把后续的运行权交给 JavaScript。到了 Agent Skills 里，SKILL.md 扮演了类似角色：它不是最终能力本身，却是模型理解、加载、调用这个 Skill 的入口文件。它告诉 Agent 这个 Skill 是什么、什么时候使用、输入输出边界在哪里、需要调用哪些脚本、依赖哪些资源、失败时如何处理、最终应该产出什么工件。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=fe2d0c90&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz_png%2FoghJwiaPb1CuSvBa69IwrYf32MPCiaGsMhHuBkCyPNZhq3dowpuEt4QicPyFs6JhuIiarzkKgXlpLRmZlr14yVCuRicxunzb0R6dehVRZdMMqY8A%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

Ralph Loop：长周期自主任务

如果说 Codex 的跨端分布式架构解决了 AI 在“物理空间”上的无缝连接与调度问题，那么引入的 /goal 长任务指令及其背后的自主迭代机制，则彻底重构了人工智能在“时间”维度上的行为模式与存在形态。业界正在经历一场从基于单次请求-响应（Prompt-Response）的“事务性交互”，向以宏大目标为绝对导向的“自动化闭环伺服”的范式跃升。

/goal 工程本质

传统的大型语言模型应用（包括早期的 Copilot 工具），在设计哲学上高度依赖人类作为系统的“时钟发生器”与“推动器”。一旦代码生成出现语法报错、单元测试运行失败，或者遇到未预见的边界条件，AI 代理通常会立即中止当前执行流，并退回到等待状态，要求人类提供下一步的精确纠错指令。Codex 的 /goal 指令从底层状态机层面打破了这一局限，它允许用户将一个抽象的、长周期的业务目标绑定到当前活动的系统线程上。在接收到目标后，智能代理能够自主进行任务分解与规划、持续编写源代码、调用操作系统的 Shell 执行编译与测试命令，并最关键地——在面对海量报错信息时，具备读取错误堆栈、自我编辑相关逻辑并重新发起测试的自我修正能力（Self-Correction Loops），直至完全满足人类预先设定的验收标准或耗尽算力配额。

这一机制的出现，虽然赋予了 AI 极大的自治权，但也变相地极大地提高了人类操作者使用 AI 的工程门槛。提示词工程（Prompt Engineering）的核心范式发生了转移：人类的职责不再是事无巨细地描述“实现过程的每一步”，而是转变为精确定义“任务完成的边界（Definition of Done）”。使用者必须在自然语言提示词中明确、严谨地包含量化的验收标准、验证用的测试驱动脚本、代理被允许修改的代码边界，以及防止代理陷入死循环的硬性停止规则。对比 Claude Code 中包含独立评估器（Evaluator）的无人值守目标模式，当前 Codex /goal 机制官方措辞依然保持了一定程度的克制，将其定义为附加于当前线程的实验性目标跟踪器，但这并不妨碍其在实际生产中的巨大威力。

这种长周期任务能力的物理极限正在被不断突破。根据 METR（Measuring AI Ability to Complete Long Tasks[4]）的基准测试框架与长期追踪数据，前沿人工智能体在 50% 和 80% 系统可靠性下能够独立完成的软件开发任务长度，正在以惊人的约 7 个月为一个周期实现能力翻倍。OpenAI 的内部极限压力测试进一步印证了这一趋势：在“极高（Extra High）”推理模式的驱动下，基于 GPT-5.3-Codex 架构的智能体在一个完全空白的代码仓库中，面对构建一个完整 UI 设计工具的单一模糊指令，实现了长达约 25 小时的无人类干预连续运行。在此期间，该代理消耗了超过 1300 万个上下文 Token，自主生成并重构了约 3 万行有效代码，并在保持业务连贯性、执行规范验证以及从灾难性编译失败中恢复等核心指标上表现出了极高的工程韧性。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=35334f39&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FoghJwiaPb1CvhXvpxiajKWWRlW8NfRd6fiaj8L55GUjicJrje93T1yhoUKMa14ssCrlQaJAlnLN9YaM0VW07ice41gkNZHb9ljbdRPUHmcU3YaHE%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

克服上下文腐蚀

在实现这种超长周期任务的底层逻辑实现中，软件工程界不可避免地正面遭遇了当前基于 Transformer 架构的大型语言模型最致命的物理弱点——上下文腐蚀（Context Degradation/Rot）。随着对话轮次的不断延长和注入提示词的堆积，模型注意力机制（Attention Mechanism）的权重分配会被严重稀释。这不仅导致模型性能呈指数级下降，更会引发严重的逻辑幻觉、遗忘早期设定的安全约束条件以及做出极其糟糕的架构决策。

为了从系统工程层面彻底解决这一硬件级别的限制，开源社区和前沿工程师们演化出了一种被称为 “Ralph Loop” 的宏观架构范式。其本质，令人惊讶地，是一个极度简单、粗暴且高度确定性的 Bash 脚本循环结构（例如代码片段：while :; do cat PROMPT.md | claude ; done）。这种模式的命名带有某种浓厚的极客式黑色幽默——它源自美国动画《辛普森一家》中那个总是处于困惑状态、经常犯下愚蠢错误但却永远不知疲倦、一直往前冲的角色 Ralph Wiggum。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=0a7b8616&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FoghJwiaPb1CuycETHtQsA7oSMdTR6zzDic41D52EibLxwBM0EEdlc00wibgLSichV5ZIeU8brk9dYDNlL1x26elpEF6WJicEe1Kfcc1PK96TvbTPk%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

Ralph Loop 的核心控制论哲学在于“以无状态的纯粹应对有状态的复杂”，其技术内涵可解构为以下三个核心支柱：

- 系统状态的强制外置化：Ralph Loop 坚决反对在 LLM 脆弱的上下文窗口中积累冗长的历史对话和推理链条。相反，它强制要求智能代理将每一次迭代的思考结果和代码变更立即进行物理落盘，形成可追踪的 Git 提交记录或写入持久化的结构化文件。整个项目的代码库本体以及高度结构化的实施计划文档（Spec.md），成为了整个系统唯一不可撼动的“事实来源（Source of Truth）” 。

- 无损的认知刷新机制：在下一次 Bash 循环启动时，系统会无情地销毁上一个周期的代理实例，并生成一个全新的、认知处于“白纸状态”的智能体实例。这个新实例将重新读取硬盘上最新的文件状态，进行下一次严密的逻辑推理。这种类似于计算机冷启动的机制，巧妙且彻底地规避了长上下文模型因背负沉重历史包袱而必然陷入的“智能塌陷区（Dumb Zone）” 。正如开发者所言，AI 不像人类那样会因为频繁切换上下文而感到疲劳，它可以无限次地通过全新上下文循环而不产生任何倦怠。

- 宏观单体架构的回归：在面对极其复杂的长任务时，硅谷曾一度热衷于设计极其复杂、相互依赖且非确定性的多智能体通信网络（Multi-agent Orchestration）。然而，Ralph Loop 的倡导者认为，如同在微服务架构中引入非确定性会导致整个系统的灾难一样，与其构建混沌的多智能体集群，不如果断退回到最传统的单体架构（Monolithic Application）。通过在最外层包裹一个极其机械的、确定性的无限循环脚本，迫使非确定性的、具有创造力的 LLM 在每一步都必须脚踏实地，一步步逼近最终的验收目标。这种架构用极度死板的循环规则（确定性）死死禁锢了极其复杂的生成模型（非确定性），是现代软件工程在面对狂野 AI 时展现出的一种极具现实主义色彩的重要妥协与工程智慧。

展现层之争: Markdown vs HTML

随着智能代理输出的逻辑组件、代码层级和系统复杂度的呈指数级上升，机器与人类操作者之间进行信息交互的介质形式，在 2026 年引发了业界规模空前且极其激烈的学术与工程争论。这场争论的导火索，源于 Anthropic Claude 团队工程负责人 Thariq Shihipar 公开发表的一篇名为 The Unreasonable Effectiveness of HTML[5] 的深度技术文章。该文彻底点燃了关于 Markdown 与 HTML 哪种格式更适合作为下一代 AI 代理通用输出标准的思想交锋。这并非简单的美学品味之争，而是直指机器生成能力与人类认知吸收带宽之间的结构性错配。

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=8c10756c&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FoghJwiaPb1CuBQ0eulfdPfneB2F1WJTdgWXHklJOXt0h3ha5ibGdM9jPNKX09malaaDj6Cq2AeOrE4PfkrO5Y0CJ9NiczuocO91o2ozm38s7fg%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

机器算力效率 vs 人类认知负载边界

长期以来，Markdown 凭借其极高的文本压缩比、极低的 Token 消耗经济性以及无可挑剔的机器可解析性，无可争议地统治着整个 LLM 生态系统的输出层。据权威机构统计分析，将冗余的网页内容清洗并转换为极简的 Markdown 格式后，其在 LLM 推理过程中消耗的 Token 数量平均能够减少约 68%；而在那些充斥着层级嵌套和内联样式的真实世界复杂网页结构中，这种 Token 削减比例甚至可以达到惊人的 87% 。在纯粹的机器到机器（Machine-to-Machine）解析层面，Markdown 同样表现出色。在 GPT 系列模型针对表格数据提取的行业基准测试中，基于 Markdown 格式的系统准确率达到了 60.7%，显著高于直接解析庞杂 HTML 代码的 53.6%。此外，在检索增强生成（RAG）的数据管道中，摄入 Markdown 格式的文本往往能带来高达 35% 的准确率提升。

然而，这种对“机器算力绝对友好”的极简格式，在面对海量、高频、多维度的 AI 复杂输出时，迅速撞击到了碳基生物（人类）的视觉认知极限。哈佛商业评论（2026 年 3 月发布的 When Using AI Leads to “Brain Fry”[6]）的一项针对知识工作者的专项研究指出，那些在日常工作中需要监督并审核大量 AI 纯文本输出的工程师与管理者，报告其感受到的“信息超载率”增加了 19%，“决策疲劳度”飙升了 33% 。当人类面对动辄长达数百行的 Markdown 代码审查建议、没有层级高亮的架构规划文档或深层嵌套的无序列表时，其大脑经常会陷入一种被称为 “AI 大脑过载（AI Brain Fry）” 的病态疲劳状态。这种状态直接导致了一个严重的系统性浪费：大量由消耗了昂贵算力的 AI 所生成的高价值深度分析与代码，最终因为人类视觉解析系统的罢工而根本未被阅读和吸收。

HTML：信息密度的空间升维

在这种背景下，HTML 格式作为替代方案的强势崛起，其核心底层逻辑绝对不是为了追求无意义的视觉华丽效果（Visual Gloss），而是针对人类极其发达的视觉皮层（该区域占据了人类大脑皮层高达 30% 的比例）的高效刺激与信息带宽利用。

Thariq Shihipar 在论战中尖锐地指出，一旦 AI 输出的代码或规划文档超过 100 行的阈值，Markdown 那种传统的、从上到下的线性文本描述方式，就彻底丧失了向人类传达代码结构深层意图的能力。相反，如果通过系统指令要求模型强制输出结构化的 HTML 代码并调用浏览器引擎进行即时渲染，系统将实现信息密度的空间降维打击。此时，AI 不仅能够生成带有动态参数滑块的原型交互界面（Interactive Prototypes）、利用 SVG 底层路径绘制极其复杂的业务逻辑网络拓扑图，还能生成带有精准内联边距注释、色彩高亮差异的现代化审查面板。

在一个技术演示中（Using CC: The Unreasonable Effectiveness of HTML vs Markdown for Agent Outputs[7]），用户仅通过一句简单的指令：“映射此 Schema，但输出一个带有可折叠树状视图和可视数据流的单一交互式 HTML 文件”。三十秒后，一个功能完备的微型应用程序便在浏览器中渲染完成。用户可以直接点击节点、展开隐藏元素，直观地观察到如果删除某个数据库列，整个系统的 UI 将如何随之崩溃。这种“所见即所得”的 HTML 交互测试，被证明是验证 AI 代理是否真正理解了极其复杂的抽象任务结构的最高效路径——因为在视觉呈现中，如果 UI 逻辑链条断裂，意味着底层的业务推理逻辑必然是错误的。

“反效率”的尖锐批评

然而，学术界与部分坚持硬核工程哲学的开发者（如 The Unreasonable Ineffectiveness of HTML[8]）对这一趋势发出了严厉的警告。认为盲目追求 HTML 视觉包装本质上是一种破坏“内容与表现形式分离（Separation of Content and Presentation）” 这一经典软件工程原则的技术倒退。强制要求 AI 生成 HTML，意味着迫使模型将极其宝贵的推理注意力分散到诸如 CSS 内联样式调整、闭合标签对齐、SVG 路径坐标计算等与核心业务逻辑毫无关联的呈现层噪音上。

比 Token 成本激增更深层次的系统性危机在于：HTML 编译后的渲染界面虽然对人类极度友好，但其原始代码（Raw Source）对于人类眼睛而言几乎是不可读的灾难。如果知识工作者和开发者为了图方便，逐渐放弃阅读底层的 Markdown 源代码和配置文件，转而完全依赖 AI 生成的华丽 UI 界面，这本质上是在将人类最核心的“逻辑推理与系统审计权”彻底外包给机器。随着时间的推移，一旦我们集体摒弃了对源代码的阅读能力，我们将彻底丧失对整个系统架构边界的理性推理能力，只能可悲地对着虚有其表的 AI 漂亮输出傻笑，最终导致系统彻底失控。

A2UI：Google 的工程解法

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=de79e7d6&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FoghJwiaPb1CvmgwCn7KMqVkpTbtTyYVNdCicCqKs7ILpp79OYxUVj9Q9pToR8ibL3l5jicAgwPoG10qV9tDPwjIllbS63hlRhb3WjwwCAuO5CRc%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

面对这种不可调和的认知哲学争议，Google 的 A2UI[9] 未尝不是一种更工程化的解法。它没有让 Agent 直接生成 HTML，也没有退回纯 Markdown，而是把 UI 变成一种声明式数据：Agent 输出 JSON 形式的界面意图，客户端再用自己的组件库完成渲染。A2UI 官方将其定义为 Agent-to-User Interface，目标是让 Agent 能生成或填充富交互界面，同时避免直接运行 LLM 生成的任意代码。它目前仍处于 v0.8 Public Preview，但提出的问题很准：Agent 需要“说 UI”，却不一定应该亲自“写 UI 代码”。

这正好绕开了 HTML 争论中最危险的部分。直接让模型生成 HTML，本质上是让模型同时负责内容、结构、样式和交互，推理注意力很容易被 CSS、标签闭合、布局细节和事件脚本消耗掉。A2UI 则把这几层拆开：Agent 只描述需要什么组件、组件之间是什么关系、数据如何绑定；真正的 Card、Button、TextField、List 如何渲染，由宿主应用的 renderer 和 widget catalog 决定。换句话说，A2UI 重新恢复了“内容 / 表现 / 执行”的边界，只是这次边界发生在 Agent 与宿主应用之间。

所以 A2UI 更像一种 Agent UI IR，也就是界面中间表示。Markdown 适合保存事实、计划和审计记录；HTML 适合最终渲染和人类交互；A2UI 则夹在中间，把 Agent 的输出压成一份可验证、可流式传输、可增量更新、可由宿主管控的 UI 合约。它采用 JSONL stream，支持组件更新、数据模型更新和渐进式渲染，避免每次状态变化都重发整份界面。

这也给 HTML 批评者一个更稳的回答：问题不在于 AI 是否应该生成富界面，而在于它是否应该直接生成不可审计的界面源码。更健康的路径是让模型生成结构化 UI 意图，让 schema、catalog、renderer、policy 和事件日志接管安全与审计。也就是说，未来可能不是 Markdown 与 HTML 二选一，而是三层分工：Markdown 保存事实，A2UI 表达交互意图，HTML / Native Renderer 负责最终呈现。这不是技术倒退，而是边界修复：让模型回到意图生成的位置，让宿主重新掌握表现层、执行层和安全边界。

Agent 负责表达 UI 意图
协议负责约束 UI 结构
客户端负责具体渲染
组件目录负责能力边界
事件通道负责用户反馈
---------------------
Markdown / YAML / JSON：保存事实、计划、规范与审计记录
A2UI / UI Schema：表达可交互界面的结构化意图
HTML / Native Renderer：负责最终呈现、交互和平台适配

Bun：Zig → Rust

[Image: https://wechat2rss.bestblogs.dev/img-proxy/?k=374eab0d&u=https%3A%2F%2Fmmbiz.qpic.cn%2Fsz_mmbiz_png%2FoghJwiaPb1CuVMVCzS7ayFkgD7LXRW59kXyK8LVHvw4iciaLZC4WtmvibvtyTgm0BpzEP63jP9KyBzN8FWQDcW98MQYiaKVHKjyXTgW8XB82nPTY%2F640%3Fwx_fmt%3Dpng%26from%3Dappmsg]

这种工程收敛并不只发生在 AI 产品层。近期 Bun 的 Zig → Rust 迁移，也可以作为一个更底层的旁证（PR 已合并 Rewrite Bun in Rust[10]）。

如果只看表面，很容易把它理解成一次语言站队：Rust 取代 Zig，成熟生态取代锋利工具，安全类型系统取代低层自由度。但 Bun 的 PORTING.md[11] 真正值得注意的地方，并不是“用 Rust 重写 Zig” 这个结果，而是它把重写过程本身变成了一套高度结构化的工程协议。

这份文档开头就把任务拆成两个阶段：Phase A 先在 .zig 文件旁边生成同名 .rs 草稿，要求忠实捕捉原始逻辑，甚至“不需要编译”；Phase B 再按 crate 逐步让它编译通过。这个分层很重要。它没有要求一次性完成“完美重写”，而是先保留语义，再处理类型、依赖、生命周期、构建系统和 Rust 生态约束。换句话说，它把一次高风险迁移拆成了可检查、可回滚、可并行推进的状态机。

更有意思的是，它的写法非常像 Agent Skill 或系统级 prompt。文档不是泛泛说“把 Zig 翻译成 Rust”，而是给出大量明确约束：.rs 必须和 .zig 放在同目录、同 basename；不要发明 crate layout；禁止引入 tokio、rayon、hyper、async-trait、futures；不要使用 async fn，继续保持 callbacks + state machines；Zig 里已经 unsafe 的地方可以用 Rust unsafe，但每个 unsafe block 都必须写清楚 SAFETY 注释；不确定的地方要留下 TODO(port)，性能语义有偏差的地方要留下 PERF(port)。这些规则本质上不是普通文档，而是一套执行边界。它告诉执行者什么能做，什么不能做，哪里必须保守，哪里可以变形，哪里必须留下证据。

这正好呼应了本文讨论的核心：当系统复杂到一定程度，真正重要的不是“模型是否足够聪明”，而是有没有一套足够硬的外部结构把它管住。Bun 的迁移文档里有 crate map、type map、idiom map、lifetime 规则、allocator 规则、borrow checker reshape 规则、错误类型映射规则。这些东西看起来琐碎，却正是大规模重写能否成功的关键。没有这些约束，AI 或人类都会很容易把重写做成“看起来像 Rust，实际上丢掉 Zig 语义”的灾难。

所以 Bun 的案例不能简单理解为 Rust 对 Zig 的胜利。更准确地说，这是一个工程项目从“性能突破期”进入“长期治理期”之后的自然收敛。早期 Bun 需要 Zig 的锋利、直接和低层控制；当系统规模扩大，跨平台兼容、安全修复、团队协作、长期维护、IDE 支持、CI 检查和类型系统约束开始变得更重要，Rust 的工程秩序就变得更有吸引力。

它和 AI 这条主线是同构的。AI 早期迷信 prompt、长上下文和模型涌现；Bun 早期依赖语言锋芒和极致工程控制。等系统走向长期运行，真正决定上限的都不再只是能力本身，而是能不能被约束、被审查、被迁移、被维护。AI 回到 Web、协议、权限、沙盒和工件；Bun 回到 Rust、Cargo、类型系统和明确的 porting harness。表面看像“回退”，深处都是复杂系统成熟后的秩序重建。

这也让 “Skills 越来越像 HTML + JS 混合体”这个判断变得更清楚。Skill 不是魔法能力包，PORTING.md 这种文档也不是普通说明书。它们都在把专家经验、工程边界、执行步骤、错误处理和验收标准固化成可被 Agent 执行的行为结构。未来的大规模重写，很可能不再是“把任务交给一个聪明模型”，而是给模型一套类似 Bun PORTING.md 的严格迁移协议，让它在明确的类型表、crate map、idiom map、TODO 规则、PERF 规则和安全注释约束下工作。

换句话说，真正成熟的 AI 编程，不是 Vibe Coding，而是 Spec-driven Porting、Harness-driven Rewrite 和 Evidence-based Refactor。

结语

AI 技术范式升维中的“倒退”，实则是一种极其高明的“伪回归”。当前 AI 核心系统在最终展示层和外部工具调用架构上，向古老的 HTML、JavaScript 技术栈重新靠拢，绝非技术创新能力的枯竭与倒退。相反，这是软件工程学在面对现实复杂性之后，形成的一种理性收敛。大语言模型的本质结构，终究是一个基于海量语料概率分布的生成引擎；为了让这匹充满创造力、也充满危险性的野马，能够真实进入商业交易、医疗诊断、航空航天等容错率极低的严苛领域，我们必须为其打造一套高度确定、标准化且普遍适用的刚性约束框架。而历经互联网三十多年残酷安全攻防演进的 Web 协议栈与 DOM 事件模型，刚好充当了这座沟通神经网络生成世界与人类符号逻辑世界的坚固巴别塔。

赋予人工智能实现长周期自主性的基石，绝不是盲目扩大模型上下文窗口，而是建立在严格的状态外置、物理隔离与控制循环之上。无论是 Codex 推出的 /goal 命令，还是在开源社区大放异彩的 Ralph Loop 模式，都在用工程事实证明：要让 AI 长时间自主工作而不陷入漂移，必须对超长上下文累积中可能出现的认知腐蚀保持警惕。将每一步阶段性成果落盘为物理文件，如 Markdown 规划、代码差异、测试日志与审批记录，并通过“记忆刷新、实例重启、事实重读”的方式进行系统状态流转，是当前突破模型注意力衰减与长任务不稳定性的关键工程路径。

人类受限于生物演化的认知带宽，最终决定了前沿技术交互的物理形态。围绕 Markdown 与 HTML 的争论，其核心深处，实际上是在重新平衡机器的廉价计算成本与人类昂贵的认知处理成本。作为记录系统“事实真相”的底层介质，极简的符号文本，如 Markdown/YAML，凭借其信息压缩比、机器解析友好度、可读性与可 diff 能力，在未来仍将不可替代；然而，作为人类验收、审计 AI 复杂工作成果的高级媒介，带有空间折叠、色彩语义和动态交互能力的富媒体界面，如 HTML 组件，则是人类在信息爆炸时代降低决策疲劳、避免认知系统过载的刚需。

当下的 AI 技术演进，正在经历一场影响深远的“系统性祛魅”。AI 不再是那个潜藏在黑色终端背后、输出神奇文本的不可知黑盒；它正在被现代软件工程学拆解，还原为一个通过 HTTP/WebSocket 等标准协议通信、通过 JSON/YAML 等结构化格式交换状态、最终在沙盒化环境中渲染 HTML/JS 视图的分布式系统组件。这种史诗级的大融合，让一切曾经令人敬畏的技术都变得有迹可循：智能体在虚拟数字世界中的思考与行为轨迹，正在被重新映射回现代软件工程师最熟悉的经典体系结构之中。这或许是技术演进史上最迷人、也最令人安心的时刻——通过回归人类最朴素、最成熟的标准协议，我们正在尝试驯化人类历史上所创造出的最复杂的智能系统。

References

[1]

Claude Cowork:https://claude.com/product/cowork
[2]

codex windows:https://developers.openai.com/codex/app/windows
[3]

Work with Codex from anywhere:https://openai.com/index/work-with-codex-from-anywhere
[4]

Measuring AI Ability to Complete Long Tasks:https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks
[5]

The Unreasonable Effectiveness of HTML:https://x.com/trq212/status/2052809885763747935
[6]

When Using AI Leads to “Brain Fry”:https://hbr.org/2026/03/when-using-ai-leads-to-brain-fry
[7]

Using CC: The Unreasonable Effectiveness of HTML vs Markdown for Agent Outputs:https://www.reddit.com/r/ClaudeCode/comments/1t9pa38/using_cc_the_unreasonable_effectiveness_of_html
[8]

The Unreasonable Ineffectiveness of HTML:https://kurtis-redux.medium.com/the-unreasonable-ineffectiveness-of-html-5bd01ae1e879
[9]

A2UI:https://github.com/google/A2UI
[10]

Rewrite Bun in Rust:https://github.com/oven-sh/bun/pull/30412
[11]

PORTING.md:https://github.com/oven-sh/bun/blob/46d3bc29f270fa881dd5730ef1549e88407701a5/docs/PORTING.md
