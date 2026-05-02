# Harness Engineering 完全指南 | BestBlogs.dev

- BestBlogs URL: https://www.bestblogs.dev/explore/topics/harness-engineering-guide
- Selector: main
- Extracted chars: 11194

---

## 领域概览

Harness Engineering 这个词最近被大量中文文章、OpenAI 演讲、平台方产品更新和工程案例同时推到台前，但它容易被误解成“给 Agent 多写几条规则”或“换一个更强模型”。更准确的理解是：**Harness 是围绕模型搭建的工程控制面**。模型负责生成、规划和调用工具；Harness 负责提供任务状态、上下文、权限边界、执行环境、反馈信号、质量门禁和人工接管点。Martin Fowler 用 feedforward / feedback 来解释这个概念：先把目标、约束和背景喂给 Agent，再用测试、审查、日志和人类判断形成反馈闭环。Ryan Lopopolo 的表述更像角色分工：人类掌舵，Agent 执行。

这也是为什么本页把 Harness Engineering 定义为 DOMAIN，而不是一次短期事件。2026 年 3 月以来的高质量素材显示，模型发布只是背景：OpenAI Agents SDK 增加沙箱、memory 与 open-source harness 控制；Anthropic 讨论长周期应用开发 Harness 和 Managed Agents；Cloudflare 把 AI Gateway、Workers AI、MCP Portal、AGENTS.md、Engineering Codex 和 AI code review 接成内部工程栈；中文工程案例则从 SPEC、Rule、Skill、Handoff、验证脚本、真实后端风险等角度补上落地细节。

![Cloudflare 内部 AI 工程栈](https://image.jido.dev/20260420223622_BLOG-3270_OG.png) _Cloudflare 的内部 AI 工程栈是一个很好的组织级 Harness 样本：路由、推理、MCP、仓库上下文、代码审查和团队知识库被放进同一套控制面，而不是散落在个人 prompt 里。_

### 1\. 先划清边界：Harness、Prompt、Context、Agent 不是一回事

Prompt Engineering 关心“怎么对模型说”；Context Engineering 关心“让模型看到什么”；Agent Architecture 关心“模型如何规划、调用工具、维持状态”；Harness Engineering 则更靠外一层，关心“这个非确定性的 Agent 系统如何被工程组织接住”。OpenClaw 的分析把 Prompt / Context / Harness 分成三个维度，Datawhale 的综述把 Agent 表达为 Model + Harness，Sebastian Raschka 则把 Coding Agent 拆成模型、工具、记忆、仓库上下文和执行循环。它们的共同点是：模型不是系统本身，模型只是系统里最会推理的部件。

如果只优化 prompt，Agent 仍然可能读不到正确代码、误用工具、越权访问、循环执行、忘记上一步结论，或者在没有测试证据时自信地宣布完成。Harness 的边界在于它把这些“模型外部的问题”做成系统能力：任务拆解、上下文装载、工具白名单、沙箱执行、checkpoint、日志、成本控制、评审门禁和回滚策略。换句话说，Prompt 是一句话，Context 是输入，Agent 是执行者，Harness 是让执行者在真实工程环境中可靠工作的轨道。

### 2\. 生产级 Harness 的六层结构

第一层是**任务与状态层**。每个任务需要目标、非目标、验收标准、当前状态、已知风险和退出条件。腾讯云关于 Agentic Engineering 的文章把 Spec-First、Knowledge as Code、小任务推进和多层验证作为核心实践；腾讯技术工程和阿里云开发者的案例都强调，如果没有清晰任务入口，Agent 在真实后端系统里会把“看起来能跑”误判为“可以交付”。

第二层是**上下文与知识层**。AGENTS.md、架构约定、服务目录、运行手册、团队规范、历史事故和领域术语都应该版本化，而不是只存在于某个工程师脑子里。好的 Harness 会把这些材料按任务最小化注入，而不是把所有文档一次性塞进上下文窗口。Context as Code 的目标不是让上下文更多，而是让上下文更准、更短、更可维护。

第三层是**工具与权限层**。Agent 能调用工具不代表它可以碰生产系统。OpenAI Agents SDK 的沙箱、memory 控制和可检查 harness，Anthropic Managed Agents 的运行时分层，Cloudflare MCP Portal 与 AI Gateway 的内部实践，都说明工具接入必须先经过授权、隔离、审计和成本控制。MCP、CLI、浏览器、数据库、内部 API 和文件系统都是“手”，但 Harness 要决定哪些手可以在什么场景下使用。

![OpenAI Agents SDK](https://image.jido.dev/20260415172541_Agents_SDK__SEO_Card.png) _OpenAI Agents SDK 的更新把沙箱、memory 与 open-source harness 控制作为官方能力呈现，说明 Harness 已经从社区方法论进入平台运行时层。_

第四层是**执行与编排层**。单个 Agent 可以完成局部任务，但生产级软件通常需要多阶段、多角色、长周期执行：需求理解、方案设计、代码修改、测试修复、文档更新、代码审查、部署验证。Anthropic 的长周期应用开发 Harness、LangChain Deep Agents Deploy、Anthropic Managed Agents 都在解决同一个问题：如何让 Agent 不只是一次性回答，而是在可恢复、可观察、可替换的运行时里推进任务。

第五层是**验证与质量层**。Harness Engineering 最容易被忽视的部分不是自动化，而是“如何证明做对”。自然语言规则只能表达原则；生产完成标准必须落成测试、lint、类型检查、安全扫描、CI 总验证、代码审查 Agent 和人工审查。腾讯 CDN LEGO 案例强调多模型对抗式 CR 和真实测试，Cloudflare 把 AI code review 接入合并请求，Fowler 则把 feedback 看作持续改进 Harness 的核心。

第六层是**组织与治理层**。当 Harness 从个人技巧变成团队基础设施，工程师的价值会从“亲手写多少代码”移动到“如何定义目标、拆边界、设计验证、沉淀知识、安排接管点”。这不是工程师退场，而是工程师从局部执行者上移为系统设计者和质量负责人。Ryan Lopopolo、MiniMax × Hermes Agent 对谈、Hung-yi Lee 的视频和“刚火可能就过时”的批判文章都在提醒同一件事：Harness 不应成为新口号，它必须经得起组织、成本、安全和模型演进的检验。

### 3\. 什么不算真正的 Harness

只写一份“万能 prompt”不算 Harness；只给 Agent 一个仓库和终端不算 Harness；只接 MCP 但没有权限、审计和回滚不算 Harness；只做 AI code review 但没有把问题回流成规则、测试和上下文，也不算 Harness。真正的 Harness 至少能回答四个问题：Agent 看到什么，能做什么，怎么证明做对，失败后系统如何变得更好。

![Coding Agent Components](https://image.jido.dev/20260404130259_49b97718-57f4-4977-99c8-8ad5c4d32af3_1548x862.png) _Coding Agent 的能力来自模型、工具、记忆、仓库上下文和执行循环的组合。Harness Engineering 关注的是这些部件之外的控制面和反馈机制。_

## 核心概念

Harness / 工程控制面

Harness 是围绕模型和 Agent 的工程控制面，负责目标、状态、上下文、权限、运行时、验证、日志和回滚。它不是 prompt 的同义词。

Feedforward / Feedback

Feedforward 是任务前给 Agent 的目标、约束和背景；feedback 是任务中和任务后的测试、审查、日志和人类判断。Harness 的质量取决于两者是否形成闭环。

Context as Code

把架构约定、AGENTS.md、运行手册、团队规范和领域知识版本化、可审查化，并按任务最小高信号注入上下文。

受控工具与沙箱

工具调用必须经过授权、隔离、审计和成本控制。沙箱、MCP、OAuth、vault、日志和权限策略共同定义 Agent 能做什么。

可执行质量门禁

完成标准不能只写在自然语言里，还要变成测试、lint、类型检查、CI、代码审查、安全扫描和人工发布决策。

组织级知识回流

每次失败都应回流到规则、上下文、测试、工具或流程中。否则 Harness 只是一次性自动化，不会成为团队资产。

## 入门路径

1.  1

    ### 从概念边界开始

    先读 Martin Fowler 和 Ryan Lopopolo：前者给出 feedforward / feedback 的清晰模型，后者解释人类掌舵、Agent 执行的角色变化。读完后应能区分 prompt、context、agent 和 harness。

2.  2

    ### 理解失败模式

    用腾讯技术工程、阿里云开发者和 Tw93 的材料理解真实系统中的失败：上下文缺失、跨文件影响判断不足、工具误用、状态丢失、不确定性表达差、验证不足。

3.  3

    ### 搭一个最小 Harness

    从一个真实任务开始，把 SPEC、任务分解、AGENTS.md、规则、Handoff 和总验证脚本跑通。先追求可观察、可验证、可回滚，而不是一步到位全自动。

4.  4

    ### 把工具接入变成平台能力

    当 Agent 要访问代码库、浏览器、内部 API 或生产数据时，再引入沙箱、MCP、网关、OAuth、日志和权限策略。OpenAI、Anthropic、Cloudflare 的官方/平台材料是这一阶段最重要的参考。

5.  5

    ### 把个人技巧沉淀成组织资产

    把失败案例、审查结论、测试缺口、上下文缺口和权限问题回流到代码、文档、规则和平台中。Harness Engineering 的成熟度不看 prompt 多长，而看团队是否越用越稳定。


## 进阶实践

### 实操检查清单

**1\. 任务入口是否有边界。** 每个 Agent 任务都应包含目标、非目标、上下文来源、验收标准、权限边界、风险提示和失败处理方式。没有边界的任务会把模型能力变成风险放大器。

**2\. 上下文是否可维护。** AGENTS.md、仓库规范、架构约定、服务目录、运行手册和团队知识需要 owner、版本和删除机制。过期上下文比没有上下文更危险，因为它会让 Agent 自信地遵守错误规则。

**3\. 工具权限是否最小化。** MCP server、浏览器、终端、数据库、内部 API、凭证和文件系统都要按任务授权。OpenAI 与 Anthropic 的平台材料共同说明，沙箱、memory 控制、brain / hands 分离和审计日志是 Agent 进入生产前的基础设施。

**4\. 验证是否在链路中。** 测试、lint、类型检查、CI、代码审查 Agent、安全扫描和人工发布决策应成为 Agent 工作流的一部分，而不是事后补救。真实后端系统尤其不能把“AI 说完成了”当作完成证据。

**5\. 失败是否会让系统变好。** 好的 Harness 会把失败沉淀为新测试、新规则、新上下文、新工具限制或新人工接管点。反复用口头提醒修正同类错误，说明 Harness 还没有形成组织记忆。

### 高级风险

**模型进步不会消灭 Harness。** 模型越强，能执行的任务越长，接触的系统越多，越需要边界、审计和恢复。腾讯科技关于“可能过时”的批判值得保留：如果模型把一部分 scaffold 内化，Harness 的形态会变化，但生产工程仍需要控制面。

**Harness 不能替代软件工艺。** 模块化、清晰命名、TDD、可读文档、领域边界和可观察性在 Agent 时代更重要，因为它们同时改善人类和 Agent 的理解成本。

**组织治理会成为瓶颈。** 当 Agent 可以自动写代码、开 PR、调工具、读内部系统时，问题从“能不能做”转为“谁授权、谁审查、谁承担风险、如何追责”。这需要平台、流程和文化共同变化，而不是单个工具解决。

## 工具与资源

-   [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

    用于构建可控 Agent，相关官方材料强调沙箱、memory 与 harness 控制。

-   [Model Context Protocol](https://modelcontextprotocol.io/)

    把工具和数据源接入 Agent 的协议层，生产使用时必须配合权限、审计和隔离。

-   [Claude Managed Agents](https://claude.com/blog/claude-managed-agents)

    Anthropic 的托管 Agent 产品，适合理解 brain / hands 分离和长任务运行时。

-   [LangChain Deep Agents Deploy](https://blog.langchain.com/deep-agents-deploy-an-open-alternative-to-claude-managed-agents/)

    开源/模型无关的生产 Agent harness 部署方案。

-   [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/)

    可作为 LLM 路由、观测、成本和策略控制层。

-   [AGENTS.md](https://agents.md/)

    把仓库级 Agent 指令沉淀为可版本化文件，是 Context as Code 的常见入口。


## 常见问题

Harness Engineering 和 Prompt Engineering 最大区别是什么？

Prompt Engineering 优化输入文字；Harness Engineering 设计整个执行系统。它包括上下文、工具权限、运行时、验证、反馈、日志和人工接管。prompt 可以是 Harness 的一部分，但不能替代 Harness。

小团队需要 Harness 吗？

需要，但不必一开始就平台化。最小版本可以只有 SPEC、AGENTS.md、任务拆解、工具白名单和一个总验证脚本。关键是让 Agent 的输入、动作和完成证据可追踪。

模型越来越强，Harness 会不会过时？

形态会变化，但生产系统仍需要边界、审计、验证和恢复。模型越能执行长任务，越需要系统决定它看到什么、能做什么、什么时候停、谁来接管。

Harness 和 MCP 是什么关系？

MCP 是工具和数据接入协议；Harness 是更大的控制面。一个 Harness 可以使用 MCP，但还要负责权限、沙箱、日志、验证、成本和回滚。只接 MCP 不等于已经有生产级 Harness。

如何判断一个 Harness 已经可以进入生产？

至少看五件事：任务入口清楚；上下文可维护；工具权限最小化；验证在执行链路内；失败能回流为规则、测试或平台改进。如果缺少其中任何一项，就应先限定使用范围。

## 延伸阅读

-   [

    Harness engineering for coding agent users

    Martin Fowler· 2026-04-02

    用 feedforward / feedback 建立概念边界，适合作为英文读者的起点。



    ](/article/1caa5015)
-   [

    Harness Engineering: How to Build Software When Humans Steer， Agents Execute — Ryan Lopopolo， OpenAI

    AI Engineer· 2026-04-17

    OpenAI 工程师 Ryan Lopopolo 的原始演讲，解释“人类掌舵、Agent 执行”的角色变化。



    ](/video/a392d2a)
-   [

    从第一性原理思考 Agentic Engineering

    腾讯云开发者· 2026-04-23

    从第一性原理推导 Agentic Engineering，适合建立中文读者的方法论底座。



    ](/article/f5d1601a)
-   [

    万字干货！Harness Engineering 如何工程化落地？

    腾讯云开发者· 2026-04-22

    把 SPEC、Rule、Skill、Handoff、验证脚本等落成工程流程。



    ](/article/d34819ba)
-   [

    Harness Engineering：AI 能在真正"出事会炸"的后端系统里写代码吗？

    腾讯技术工程· 2026-04-21

    真实后端系统案例，解释为什么生产代码需要更强的边界和验证。



    ](/article/e32a066c)
-   [

    The AI engineering stack we built internally — on the platform we ship

    Ayush Thakur· 2026-04-20

    Cloudflare 内部 AI 工程栈，是组织级 Harness 的高质量案例。



    ](/article/d73b4211)
-   [

    The next evolution of the Agents SDK

    OpenAI· 2026-04-15

    OpenAI Agents SDK 的沙箱、memory 与 harness 控制能力，补足官方定义。



    ](/article/a06d68e3)
-   [

    Harness design for long-running application development

    Anthropic Engineering· 2026-03-23

    Anthropic 关于长周期应用开发 Harness 的设计文章。



    ](/article/504ce725)
-   [

    Scaling Managed Agents: Decoupling the brain from the hands

    Anthropic Engineering· 2026-04-08

    Anthropic Managed Agents 的 brain / hands 分离，是运行时架构的重要参考。



    ](/article/46822472)
-   [

    Components of A Coding Agent

    Sebastian Raschka, PhD· 2026-04-04

    从工具、记忆、仓库上下文拆解 Coding Agent 的组成部分。



    ](/article/4e385f0b)

## 引用来源

1.  \[1\]

    [从第一性原理思考 Agentic Engineering](/article/f5d1601a)

    腾讯云开发者· 2026-04-23

2.  \[2\]

    [万字干货！Harness Engineering 如何工程化落地？](/article/d34819ba)

    腾讯云开发者· 2026-04-22

3.  \[3\]

    [Harness Engineering：AI 能在真正"出事会炸"的后端系统里写代码吗？](/article/e32a066c)

    腾讯技术工程· 2026-04-21

4.  \[4\]

    [从玩具到生产力：用真实项目讲透 AI Agent 的 Harness Engineering](/article/9dd92132)

    阿里云开发者· 2026-04-21

5.  \[5\]

    [The AI engineering stack we built internally — on the platform we ship](/article/d73b4211)

    Ayush Thakur· 2026-04-20

6.  \[6\]

    [Harness Engineering: How to Build Software When Humans Steer， Agents Execute — Ryan Lopopolo， OpenAI](/video/a392d2a)

    AI Engineer· 2026-04-17

7.  \[7\]

    [The next evolution of the Agents SDK](/article/a06d68e3)

    OpenAI· 2026-04-15

8.  \[8\]

    [Build long-running agents with more control over a](/status/2044466699785920937)

    OpenAI Developers· 2026-04-15

9.  \[9\]

    [最新！万字综述 Harness 革命！](/article/f0f5a2f7)

    Datawhale· 2026-04-13

10.  \[10\]

     [深度解析 OpenClaw 在 Prompt / Context / Harness 三个维度中的设计哲学与实践](/article/824a229d)

     阿里云开发者· 2026-04-13

11.  \[11\]

     [Harness Engineering：有時候語言模型不是不夠聰明，只是沒有人類好好引導](/video/f92dacb)

     Hung-yi Lee· 2026-04-12

12.  \[12\]

     [Deep Agents Deploy: an open alternative to Claude Managed Agents](/article/079cf7ed)

     LangChain Accounts· 2026-04-09

13.  \[13\]

     [Scaling Managed Agents: Decoupling the brain from the hands](/article/46822472)

     Anthropic Engineering· 2026-04-08

14.  \[14\]

     [Extreme Harness Engineering for Token Billionaires: 1M LOC， 1B toks/day， 0% human code， 0% human review — Ryan Lopopolo， OpenAI Frontier & Symphony](/article/c725aea4)

     Latent.Space· 2026-04-07

15.  \[15\]

     [Claude Managed Agents: get to production 10x faster | Claude](/article/3c819a5d)

     Claude Blog· 2026-04-07

16.  \[16\]

     [Components of A Coding Agent](/article/4e385f0b)

     Sebastian Raschka, PhD· 2026-04-04

17.  \[17\]

     [Harness engineering for coding agent users](/article/1caa5015)

     Martin Fowler· 2026-04-02

18.  \[18\]

     [Harness design for long-running application development](/article/504ce725)

     Anthropic Engineering· 2026-03-23

19.  \[19\]

     [你不知道的 Agent：原理、架构与工程实践 - Tw93](/article/58852dc5)

     Tw93· 2026-03-21

20.  \[20\]

     [技术教科书：顶级开发团队设计的 Harness 工程项目源码什么样](/article/3e1cd52f)

     腾讯技术工程· 2026-04-09

21.  \[21\]

     [当我们在讨论 Harness 的时候，我们在讨论什么 | 深度对谈: MiniMax × Hermes Agent](/article/56f3366c)

     十字路口Crossing· 2026-04-20

22.  \[22\]

     [Harness 刚火，可能就要成为过去时了｜Hao 好聊论文](/article/c7d5f93e)

     腾讯科技· 2026-04-13


本文由 AI 辅助生成并经编辑审核，围绕站内引用整理。若发现事实错误，欢迎反馈。