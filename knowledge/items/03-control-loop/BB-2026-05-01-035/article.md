# Boris Cherny 与 Claude Code 的诞生

- BestBlogs URL: https://www.bestblogs.dev/explore/topics/boris-cherny-claude-code-profile
- Extraction: DOM text from BestBlogs page
- Extracted chars: 4671
- Original publisher URL: https://x.com/bcherny

---

基本信息
职位：Claude Code 创造者与负责人
所属机构：Anthropic
所在地：San Francisco, CA
X / Twitter
GitHub
更多
标志性贡献
把 Claude Code 从 side project 做成 Anthropic 旗舰产品

Boris Cherny（中）与 Claude Code 团队同事一起登上 YC Lightcone Pod，被 YC 写为 'Creator of Claude Code'。来源：Y Combinator Lightcone Pod 2026-02-17。

2024 年 9 月加入 Anthropic 的第一周，他把 Claude 接到终端上做了一个能查询本地音乐的 AppleScript 玩具；放开 Bash 权限后，那段原型迅速演化成内部 dogfooding 工具，11 月发布的版本在第一周就被一半 Anthropic 工程师用上。2025 年 2 月与 Claude 3.7 Sonnet 一同公开发布，2025 年 5 月正式 GA，到 2026 年初年化收入跨过 10 亿美元，占据 AI 编程市场过半份额。

"我开始在终端里把玩 Claude……我把这个原型接上 AppleScript：它能告诉我此刻在听什么音乐。" — Boris on The Pragmatic Engineer

📺 完整起源故事 · The Pragmatic Engineer · 🎙️ 中文版 · 跨国串门儿 #450

推动 CLI-first / Unix utility 形态的 AI 编程范式

在主流路线都把 AI 写进编辑器或 IDE 的时候，Boris 坚持把 Claude Code 做成可被脚本编排的 Unix 工具：原始的模型访问、最小 UI、可与 hooks/MCP/plugins/skills/sub-agents 自由组合。这一判断后来定义了 Claude Code 的产品边界，也让 Plugins、Routines 等扩展机制能在统一的接入面上落地。

"Claude Code 与其说是一个产品，不如说是一个 Unix utility。" — Boris 在 Latent Space 上的原话；'每次新模型发布我们都会删掉一堆代码'是这一形态背后的工程纪律3

提出 "为半年后的模型设计" 与 Harness Engineering 工程原则

Boris 在 YC Lightcone 与 Pragmatic Engineer 等访谈中反复强调："在 Anthropic，我们不为今天的模型构建，我们为半年后的模型构建。" 他把 Claude Code 的工程方法概括为 harness（脚手架）+ 子智能体编排 + parallel agents + 可被替换的简单组件，这套思路被国内外团队广泛引用为 AI-native 工程的范本。

📺 YC Lightcone Pod 完整访谈

把 "像带新人一样引导 Claude Code" 沉淀为方法论

Boris 团队把 CLAUDE.md 提交到 git 仓库共享、每周多次更新——'每当 Claude 做错了什么，就记录进 CLAUDE.md'，这正是 onboarding 方法论的核心机制。来源：Datawhale 翻译版的 Boris 个人设置推文。

他在推文、官方博客和多场访谈中反复强调，用好 Claude Code 的关键是给它一个验证闭环，并像带新人一样维护 CLAUDE.md、子智能体与权限边界。这套思路在 2025 年 9 月被翻译成中文广为传播的 "13 个使用技巧"，并在 2026 年 4 月由 Anthropic 官方博客以 17 年开发经验为案例完整成文，成为社区里 "如何让 AI 写出可上线代码" 的事实标准。

"给 Claude 一个验证工作的方法，只要有反馈闭环，最终结果的质量会提升 2-3 倍。"

牵头 Plugins / Routines / 1M 上下文 / Code Review 等关键扩展

2025 年 10 月发布的 Plugins 是 Boris 亲自牵头的第一个公开特性；2026 年陆续上线 Routines、1M 上下文会话管理、Code Review subagents、Auto Mode 等能力，把 Claude Code 从单兵 CLI 扩展成团队级 AI 工程基础设施，也把 "工程师 → 工作流编排者" 的范式落到了具体的产品功能上。

用 Claude 写 Claude Code：80% 以上自生成的范例

Boris 自己的工作流：把终端标签按 1-5 编号、并行运行 5 个 Claude 实例，是 '每天 10-30 个 PR' 背后的具体形态。来源：Datawhale 翻译版的 Boris 个人设置推文。

Boris 公开表示，Claude Code 自己 80–90% 的代码已经由 Claude 生成；他自 2025 年 11 月起再没手写过一行业务代码，每天提交 10–30 个 PR、并行运行 5+ Claude 实例，并把 Anthropic 工程师的人均产出推高 200%。这些数字成了 "AI-native 工程能否真正跑起来" 的最有说服力的反例。

"我从未像现在这样享受过编程，因为我不用再处理那些细枝末节了。工程师的人均生产力提高了 200%。"

核心观点
2026-04Anthropic 官方博客《Onboarding Claude Code like a new developer》

把 Claude Code 当作刚入职的新人来引导：在 CLAUDE.md 里讲清楚环境与边界，给它能跑起来的小目标，让每一次成功转化成下一次的上下文。这是 17 年代码积累如何被 AI 真正接住的关键。

2026-04Anthropic 官方博客《在 Claude Code 中使用 Claude Opus 4.7 的最佳实践》

Claude Code 的产品哲学是 "先做最简单的事"。模型已经足够好，简单的方案通常就能跑起来——不需要过度工程化。每次模型升级，我们都会删掉一堆代码。

2026-03The Pragmatic Engineer Podcast / 跨国串门儿 #450 中文克隆版

今天的工程师就处在 15 世纪印刷机出现前的抄写员时刻。抄写员的工作消失了，但 "作者" 的市场扩大了一万倍。抛弃对语言和框架的偏见，未来属于那些能跨越工程、产品和业务的通才。

2026-02Lenny's Podcast 'What happens after coding is solved'

Lenny's Podcast 用 Boris 的原话作为节目封面："Coding is largely solved"。这是这期节目的核心论点，也是本主题最被引用的金句。

我的代码 100% 都是 Claude Code 写的，从 11 月起我就没再手动写过一行。我现在每天提交 10 到 30 个 PR，录这期节目时同时跑着 5 个智能体。编程问题在很大程度上已经被解决了——我想象中的未来是人人都会编程，任何人都随时可以开发软件。到今年年底，'软件工程师' 这个头衔会逐渐消失，被 'builder' 取代，这对很多人来说会是个痛苦的过程。

📺 Lenny's Podcast 完整 90 分钟版本

2026-02Y Combinator Lightcone Pod 'Inside Claude Code With Its Creator'

在 Anthropic，我们不为今天的模型构建，我们为半年后的模型构建。这也是我给所有在 LLM 上构建产品的创业者的建议。

2025-09Boris 在 X 上首次公开个人 Claude Code 设置（被 Datawhale 完整翻译）

我的配置可能会让你大吃一惊，因为它极其朴素——Claude Code 能完美开箱即用。Claude Code 没有所谓的唯一正解，我们在构建它时就特意设计成这样。给 Claude 一个验证工作的方法，只要有反馈闭环，最终结果的质量会提升 2-3 倍。

代表作品
Claude Code
project

Anthropic 的 agentic CLI 编程助手；2025-05 GA 后年化收入跨过 10 亿美元，占据 AI 编程市场过半份额。

Plugins for Claude Code
project

2025-10 由 Boris 亲自牵头发布，把 agents、slash commands、MCP servers 与 hooks 打包成可分发单元，是他在 Claude Code 上 lead 的第一个公开特性。

Routines for Claude Code
project

2026-04-13 发布，把可重复任务编排进可调度的 routines；是 Claude Code 团队推进 'agent-as-coworker' 路线的关键一步。

Inside Claude Code With Its Creator Boris Cherny — Y Combinator Lightcone Pod
talk

2026-02-17 公开访谈；提出 'build for the model six months from now' 的工程哲学。

Programming TypeScript (O'Reilly)
paper

Boris 在 Anthropic 之前出版的 O'Reilly 著作；至今仍是 TypeScript 学习的常见入门读物。

重要时间线
2024-09-01

加入 Anthropic；第一周搭出第一个 Claude + AppleScript 终端原型，并把它接上 Bash。

2024-11-15

Claude Code 内部 dogfood 版本发布；五天内 50% Anthropic 工程师在用。

2025-02-24

与 Claude 3.7 Sonnet 同时公开发布 Claude Code（Limited Research Preview）。

2025-05-01

Claude Code GA；同期年化收入跨过 5 亿美元。

2025-07-01

短暂离开 Anthropic 加入 Cursor；两周后因为 Anthropic 的 safety 使命感回归。

2025-09-15

在 X 公开个人 Claude Code 设置（13 个使用技巧），并随后主导发布 Plugins for Claude Code（10-09），首次以负责人身份在 Claude Code 上 lead 一个公开特性。

2026-02-17

登上 YC Lightcone Pod 与 Lenny's Podcast，提出 "印刷机时刻" 与 "coding is solved" 的产业级判断。

2026-04-13

推动 Routines、1M 上下文会话、Onboarding 心法等关键扩展集中落地。
