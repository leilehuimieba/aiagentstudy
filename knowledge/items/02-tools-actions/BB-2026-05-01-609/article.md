# Just Released: A Complete Beginner's Guide to the Internet-Famous Loop Engineering

- BestBlogs URL: https://www.bestblogs.dev/article/153f1dd0
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&mid=2247723692&idx=1&sn=79bbf6450a03de7e8163338ae1499b48
- Source: BestBlogs / Datawhale
- Publish time: 2026-06-24 22:08:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 7963

---

Datawhale干货 

        
         作者：筱可，Datawhale成员

        

       

      

     

    

   

   

  

  昨天我们聊了 Loop Engineering 的发展和本质，今天我们来教大家怎么搭Loop Engineering。搭建一个会 Loop 的 Agent 团队，只要三个文件加一个配置，下面用 Claude Code + step-3.7-flash 一步步搭起来。

  核心思路一句话：把写代码和查代码拆成两个 Agent，让编排器循环调度，查到全绿为止。不用你逐条检查，系统自动跑完所有检查，有问题反馈给写代码的 Agent，修完再查，直到全绿。

  为什么要这么搞？因为传统方式是单次的：你写需求，Agent 生成代码，你肉眼看一遍觉得没问题就收工。但肉眼看容易漏：代码能跑不代表测试全过，测试过了不代表类型没错。更常见的情况是 Agent 写的代码有问题，你发现后贴回去让它改，改完又引入新问题，来回几轮你都不确定到底修好了没有。

  Loop Enigneering 把这件事交给系统：它自动跑完所有检查，有问题自动反馈，人们只需要看一眼最终结果。

  三个文件，搭建 Loop Engineering

  整个设置就三个文件：Agent 定义、循环编排器、停止规则。放在 Claude Code 的 .claude/ 目录下就行。

  文件一：Agent 定义

  执行和验证必须拆开。写代码的 Agent 往往高估自己的答案，写完再问自己行不行，答案大概率是行。所以用两个专职 Agent：builder 只写代码，checker 只查代码。放在 .claude/agents/ 目录下。

  

  builder.md — 只负责写和修代码：

  ---
name: builder
description: 负责编写和修复代码。用于实现任务或修复 checker 发现的失败。
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
---
你只负责构建和修复，不做其他任何事情。
## 接到任务时
1. 先读项目的 AGENTS.md、README、package.json（或等效配置文件），
   理解架构分层和编码约定。不了解项目约定就动手，白跑的循环比读文档
   花的时间多得多。
2. 确认任务涉及的文件范围。如果需要跨层修改，先想清楚依赖方向是否允许。
3. 写一行任务简报：目标、涉及文件、完成标准。然后开始实现。
## 接到修复请求时
1. 逐条阅读 checker 报告的失败项，每条失败都要读到 file:line。
2. 定位根因。区分症状和病因：测试失败是症状，代码逻辑错误是病因。
   修病因，不要修症状。
3. 一次只修一个根因。如果 checker 报了 3 个失败，但它们可能是同一个
   根因引起的，先修最可能的那个，跑一遍检查看是否连带解决其他的。
4. 不要顺手重构不相关的代码。循环验证的场景下，每一行多余改动都可能
   引入新问题，让下一轮 checker 报出意料之外的失败。
## 红线
- 绝不弱化测试来让它通过。修代码，不是修测试。
- 绝不通过删除、注释、跳过失败的检查来达到通过。
- 绝不在没有跑过检查的情况下声称已修复。
## 汇报格式
修改完成后，先本地跑一遍 checker 会执行的命令，确认通过再汇报。
汇报格式：
  改了什么：<一句话>
  修改文件：<file1>, <file2>, ...
  本地检查结果：<通过/失败>

  checker.md — 只负责检查，绝不修改代码：

  ---
name: checker
description: 运行所有检查并报告失败项。在 builder 之后调用。绝不修改代码。
tools: Read, Grep, Glob, Bash
model: sonnet
---
你只检查，绝不修复。
## 发现检查命令
不要假设检查命令。先读 package.json 的 scripts 字段（或等效配置），
找出项目实际使用的检查命令。常见模式：
- test: `npm test` / `pnpm test` / `vitest run`
- lint: `eslint .` / `oxlint .` / `biome check`
- 类型: `tsc --noEmit` / `vue-tsc --noEmit`
- 格式: `prettier --check` / `format:check`
如果项目有聚合检查命令（如 `pnpm check` = test + lint + tsc + format），
优先跑聚合命令，它能一次性覆盖所有检查项。
如果项目有额外检查（依赖守卫、deadcode 检测、安全扫描等），也要跑。
这些检查往往能抓到测试和 lint 抓不到的问题。
## 执行
按顺序运行所有检查命令。每项检查的完整输出都要保留，不要只保留最后
一行的 pass/fail。失败的检查往往需要看中间输出才能定位根因。
## 报告格式
- 全部通过：输出 "ALL GREEN"，然后逐项列出每项检查的名称和通过证明
  （如 "test: 848 passed, 0 failed"）。不要只说全过了。
- 任何失败：输出 "FAILED"，然后逐条列出：
  `file:line - 什么坏了 - 哪个检查抓到的`
  如果同一文件有多个失败，合并列出。如果多个失败可能是同一根因，
  标注疑似同源。
## 红线
- 绝不意译失败信息。复制真实错误输出的关键行。builder 要根据你的报告
  来修复，模糊的报告会浪费整整一轮循环。
- 绝不因为看起来是小问题而省略失败项。你没修过的问题，builder 也不知道。
- 绝不自己尝试修复。你只负责报告，修复是 builder 的事。

  两个 Agent 的 tools 字段差异是关键：builder 有 Write 和 Edit，能改代码；checker 只有 Read、Grep、Glob 和 Bash，从工具层面保证它无法修改任何文件。这不是靠提示词约束，而是工具可见性的硬隔离。

  文件二：循环编排器

  这是驱动循环的核心。放在 .claude/commands/loop.md，注册为斜杠命令 /loop：

  ---
description: 循环运行 builder 和 checker，直到所有检查通过
argument-hint: <task>
allowed-tools: Read, Grep, Glob, Bash, Task
model: sonnet
---
以循环方式执行此任务：$ARGUMENTS
## 第 0 步：对齐目标
写一行任务简报：目标、涉及文件、完成标准。
这一行会传给 builder 和 checker，确保三者对齐。
## 循环
1. 派 builder 实现任务（或修复上一轮的失败）。
2. 派 checker 运行所有检查。
3. 如果 checker 说 ALL GREEN：停止，向我展示 diff 和检查结果。
4. 如果 checker 说 FAILED：把 checker 的完整失败报告原样转发给 builder，
   不要自己解读或过滤。builder 需要原始错误信息来定位根因。
5. 回到第 1 步。
## 轮次管理
- 最多 5 轮。每轮开始时公开声明 "Cycle N/5"。
- 如果同一失败连续出现两次，停止循环。builder 可能在瞎猜，
  不是在修复。把情况报告给我。
- 如果修复导致之前通过的检查失败，停止循环。在拆东墙补西墙。
停止条件在 CLAUDE.md 中。严格遵循。

  编排器的逻辑就是一个调度循环：派 builder 干活，派 checker 检查，通过了就停，没通过就把失败信息喂给 builder 再来一轮，最多 5 轮。关键指令是「把 checker 的完整失败报告原样转发给 builder，不要自己解读或过滤」。Agent 在传递信息时倾向于帮忙总结，但总结会丢失行号、堆栈轨迹、中间输出这些 builder 定位根因需要的关键细节。

  文件三：停止规则

  loop 能替你推进流程，但不能替你担责任。一个没人盯着的 loop，也会没人盯着地犯错。所以循环必须有刹车。

  

  把停止规则写进项目根目录的 CLAUDE.md，所有 Agent 都能看到：

  ## Loop stop rules
### 停止条件
循环在以下任一条件成立时停止：
1. ALL GREEN：所有检查通过。停止，附上每项检查的通过证明。
2. 轮次用尽：达到 5 轮上限。停止，报告仍失败的项、每轮尝试了什么、为什么没成功。
3. 同一失败连续两轮：builder 在猜，不是在修。停止，升级给我。
4. 回归：修复导致之前通过的检查失败。停止，说明改了什么导致了回归。
5. 无实质进展：连续 2 轮失败项数量没有减少。停止，可能任务范围过大，
   需要拆分成更小的子任务。
6. 疑似超出能力边界：builder 反复尝试但失败原因涉及它无法访问的外部依赖
   或环境问题。停止，报告阻塞点。
### 红线
- 永远不在没有 checker 输出的情况下报告成功。
- 永远不弱化、删除、跳过检查来达到 ALL GREEN。
- 永远不修改 checker 的工具白名单。
### 升级协议
停止并升级给我时，必须携带以下信息：
- 当前轮次（Cycle N/5）
- 仍失败的项列表
- 每项已尝试过的修复方法
- 你的判断：为什么继续循环不会解决问题

  六条停止条件覆盖了实战中常见的卡死模式。升级协议要求编排器在刹车时附上当前轮次、失败项、已尝试方法、失败原因判断，你拿到这份报告就能直接决定下一步，不用自己翻历史。

  第四步：配置 Claude Code 接入 step-3.7-flash

  三个文件就位后，把 Claude Code 的模型指向 StepFun。

  

  修改 ~/.claude/settings.json：

  {
"env": {
"ANTHROPIC_AUTH_TOKEN": "你的 StepFun API Key",
"ANTHROPIC_BASE_URL": "https://api.stepfun.com/step_plan",
"ANTHROPIC_DEFAULT_SONNET_MODEL": "step-3.7-flash",
"ANTHROPIC_DEFAULT_HAIKU_MODEL": "step-3.7-flash"
  },
"model": "sonnet"
}

  API Key 在阶跃星辰开放平台申请：https://platform.stepfun.com/interface-key

  把 sonnet 和 haiku 两个别名都映射到 step-3.7-flash，builder、checker 和编排器就都会走 step-3.7-flash，整套 Loop Engineering 只用一个模型。

  模型选择 step-3.7-flash

  Loop Engineering 对模型有一个特殊要求：它需要在短时间内被高频调用，每次都要快速给出准确判断。这和传统的一次对话解决所有问题截然不同。

  step-3.7-flash 在这个场景下有三个优势。第一，速度快，400 TPS 的推理速度意味着每次检查的等待时间极短，一个 5 轮循环下来，模型推理的总耗时可能还不如你喝一口水的时间。对比 50-100 TPS 的模型，5 轮循环可能要等好几分钟——等久了人就会忍不住去手动干预，而手动干预恰恰是 Loop Engineering 要消除的东西。第二，Agent 场景表现好，它支持 low/medium/high 三级可配置推理强度，检查代码错误、定位失败原因时 medium 档位就够准确，不需要每轮都拉满推理强度。第三，Step Plan 订阅制，loop 一旦跑起来会反复读上下文、反复试错、反复验证，token 消耗可能非常大，按量计费很容易失控，Step Plan 的 Credit 额度很高。Flash Pro 档位每月 8000M Credit，循环验证这种高频调用场景基本够用。

  实战：给 Step-Realtime-CLI 提 PR

  理论讲完了，来个真实的。我最近在给阶跃星辰的开源项目 Step-Realtime-CLI提 PR，全程用 Claude Code + step-3.7-flash 的 loop 模式。四个 PR，覆盖了构建修复、TUI 显示修复、WSL 环境修复、格式化四个方向。这个项目的 pnpm check 命令串了六项检查：test + lint + dep-guard + deadcode + tsc + format:check，天然的 checker。

  第一轮：clone 完跑不起来

  clone 项目，跑 setup.sh，在 WSL 里直接报错——setup.sh 用 command -v bun 找 Bun，如果 Windows 的 Bun 在 PATH 里，会找到 /mnt/c/... 下的 Windows 版本，构建出来的二进制在 WSL 里跑不了。

  /loop 修复 setup.sh 在 WSL 下误用 Windows Bun 的问题

  builder 写了 resolve_bun() 函数：优先 STEP_BUN_BIN 环境变量，检测到 /mnt/* 路径时警告并跳过，从 $HOME/.bun/bin/bun 等 Linux 原生路径找。checker 跑 pnpm check，全绿。一轮通过，提了 PR #37。

  第二轮：装上了但启动崩溃

  step-cli error: OpenTUI runtime did not export createLocalTuiClientApp()

  builder 读 tsdown.config.ts，发现 rolldown 把 local-tui-app.ts tree-shake 掉了，产出的 chunk 是空的；同时 agent-sdk 包根本没有构建步骤，dist/index.js 缺失。加了 preserve entry 配置和 agent-sdk 构建，checker 跑 pnpm check 通过。提了 PR #28。

  第三轮：跑起来了但 TUI 刷屏

  TUI 转录面板反复显示 Delegation reminder 之类的系统消息——这是插件通过 beforeModelRequest 注入的内部消息，不该显示给用户。

  /loop 修复插件注入的 system message 泄漏到 TUI 转录面板的问题

  builder 给 SystemMessage 加了 hidden?: boolean 标志，TUI 渲染器和剪贴板导出跳过 hidden 消息，涉及 12 个文件。checker 跑 pnpm check，类型检查和 lint 都过了，但 deadcode 检测报了一个未使用的导出。builder 修掉，第二轮全绿。提了 PR #32。

  第四轮：格式检查不过

  最后准备提 PR 时，pnpm check 的 format:check 报了格式不对。这种 Prettier 修复不需要 loop，builder 直接跑 prettier --write，checker 确认通过。提了 PR #38。

  实际体感

  四个 PR 总共跑了大约 6 轮循环（PR #32 跑了 2 轮，其余各 1 轮）。每轮循环的完整耗时在十几到几十分钟不等，主要时间花在 builder 读项目文件、理解架构、定位根因上，模型推理本身的速度只占总耗时的一小部分。

  step-3.7-flash 的优势不在于让整轮循环变快，而在于推理等待不构成额外瓶颈。如果换一个 50 TPS 的模型，同样的循环每轮会多出几分钟的纯推理等待，6 轮下来差出十几分钟，这个时间差足以让你忍不住去手动干预，而手动干预恰恰打破了 Loop Engineering 的意义。

  整个过程中我做的唯一决策是：看 PR #32 涉及 12 个文件时确认了一下改动范围是否合理。其余的失败发现、根因定位、修复实现、验证通过，全是 loop 自己跑的。

  实践中遇到的几个坑

  builder 喜欢顺手改点别的。跑 PR #32 时，builder 修 system message 泄漏，顺手把不相关的类型导出也调了，结果下一轮 checker 报出 deadcode 警告，多花了一轮。提示词里写了「不要重构不相关的代码」，但 Agent 读完一圈代码后还是会有冲动把看到的问题一起改了。这就是停止规则里刹车条件存在的意义——在 builder 拆东墙补西墙时及时叫停。

  checker 的报告质量决定循环效率。有一次 checker 报了 FAILED 但只贴了最后一行错误信息，没带上下文。builder 找不到根因，瞎猜了一个修法，自然没过；第二轮 checker 同样只贴最后一行，又浪费一轮。后来在 checker 提示词里加了「保留完整输出」，问题才解决。checker 的报告是 builder 的唯一信息来源，报告模糊一轮，整个循环就白跑一轮。

  编排器会自作主张总结失败信息。编排器拿到 checker 的失败报告后，会先自己理解一遍再转述给 builder。转述过程中行号丢了、堆栈轨迹丢了、中间输出丢了，只剩一句概括。builder 拿到的不是原始错误而是二手解读，定位效率大幅下降。提示词里必须写好「不要解读或过滤」，否则编排器觉得自己在帮忙，实际在制造信息损耗。

  快速上手 Loop Engineering

  创建 builder.md 和 checker.md，放在 .claude/agents/ 下。创建循环编排器 loop.md，放在 .claude/commands/ 下。把停止规则写进 CLAUDE.md。最后配置 settings.json 接入 step-3.7-flash，跑一个真实任务看它循环。

  搭建完成后，你跟 Agent 的交互方式变了。以前是你描述需求、等结果、检查、反馈、再等结果。现在是你输入 /loop <任务>，看它自己循环到通过，最后审一眼 diff 决定要不要提 PR。

  Loop Engineering 的核心价值不在于让 Agent 变聪明了，而在于让验证变成了内置环节。一次性交付时，验证是你的工作；循环交付时，验证是系统的工作。你从质检员变回了需求方。

  

  一起“点赞”三连↓
