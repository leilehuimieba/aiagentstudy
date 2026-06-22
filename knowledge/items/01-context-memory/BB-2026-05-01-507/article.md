# Hermes Agent: The Open-Source AI Agent That Actually Remembers What It Learned Yesterday

- BestBlogs URL: https://www.bestblogs.dev/article/fc741cce
- Original publisher URL: https://www.wangjun.dev/2026/06/hermes-agent-remembers-what-it-learned/
- Source: BestBlogs / 王俊博客
- Publish time: 2026-06-06 00:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 6929

---

引子
  

  你用的每个 AI Agent 都有同一个问题。

  周一你教会了它你的项目结构、编码偏好、部署流程。到了周二，它全忘了。你又回到了起点，重新解释一切。

  就像每天早上都要培训一个新实习生。

  Nous Research 构建了 Hermes Agent 来终结这个循环。

  Hermes 是一个开源、自托管的 AI Agent，运行在你自己的服务器上，从每个完成的任务中学习，并且随着使用时间的增长变得可测量地更好。自 2026 年 2 月发布以来，它已经收获了超过 64,000 个 GitHub 星标，并引发了开发者们所说的”从 OpenClaw 迁移的浪潮”。

  有趣的部分不是采用数字。而是它底层的架构——以及它对那些希望 AI 能随时间累积价值、而不是每次会话都重置归零的人来说意味着什么。

  核心思想：会自己写剧本的 Agent

  当 Hermes 成功完成一个任务时，它不只是记录结果然后继续下一步。它会运行一个执行后评估——识别出产生结果的确切步骤序列、工具调用和推理过程——然后将该序列编码为一个可复用的 Skill 文档。一个 Markdown 文件，Agent 下次遇到类似任务时会引用它。

  这就是 Nous Research 所说的闭环学习：执行 → 评估 → 提取 → 优化 → 检索。而且它会复利增长。

  根据 Nous Research 发布的基准测试，运行自建 Skill 的 Agent 完成研究任务的速度比零提示调优的全新实例快 40%。

  你在 5 美元 VPS 上运行了三个月的 Hermes 实例，知道你的代码库、你的部署怪癖、你偏好的提交信息格式、以及在你那个奇怪的遗留集成中能用的精确 API 调用序列。一个新安装的实例对这些一无所知。

  Skills vs. Tools：一个关键的区别

  Hermes 对 Skills 和 Tools 做出了一个尖锐的架构区分，这比听起来重要得多。

  Tools（工具）是通过 JSON Schema 暴露给 AI 模型的 Python 函数。它们确定性执行。想想浏览器自动化、文件操作、流式进程。修改它们意味着编辑核心 Python 文件。

  Skills（技能）是 Markdown 文档。Agent 像阅读指令一样读取它们，并自主遵循记录在案的程序。这里是关键部分：Agent 可以自主编写自己的 Skill。不需要代码修改。不需要人来编辑配置文件。Agent 观察自己在某件事上成功，写下它是怎么做的，并将该知识存储起来供下次使用。

  Agent 在不触及自己源代码的情况下变得越来越聪明。确定性的工具层保持稳定和安全。知识层持续增长。

  四层记忆系统

  上下文太少，Agent 会做出糟糕的决策。太多，你会烧掉 Token、增加延迟、模型开始在巨大的提示词中丢失指令。

  Hermes 用四层记忆系统解决这个问题，按 Agent 需要信息的紧急程度分层：

  Tier 1：Agent 的个人笔记（MEMORY.md）

  存储环境事实、项目约定和操作经验。上限大约 800 Token，在会话开始时直接注入系统提示。想想 Agent 的”小抄”。

  
   
    # MEMORY.md 示例片段
项目使用 Vue 3 + Nuxt 3 + PrimeVue
测试框架：Vitest
部署：Cloudflare Pages（自动通过 git push 触发）
CI：GitHub Actions（运行 lint + test + build）

   

  

  Tier 2：用户档案（USER.md）

  维护一个关于你是谁、你的技术水平、时区、沟通风格的模型。大约 500 Token。也在启动时注入。

  Tier 3：会话搜索

  将跨所有历史会话的所有内容归档在一个 SQLite 数据库中。Agent 按需查询，使用全文搜索（FTS5）结合 LLM 摘要器。这就是深层历史上下文的所在。

  Tier 4：外部记忆插件

  连接到基于图的检索系统，如 LightRAG、Supermemory 或自定义向量存储。这对企业用途来说变得非常强大，支持跨复杂关系映射的多跳查询。

  前两层使用冻结快照模式：更改立即写入磁盘，但不修改活动系统提示，直到下个会话开始。这保留了语言模型的前缀缓存，确保整个长会话期间的低延迟。在对话中途修改提示会使该缓存失效，拖慢推理速度。

  还有一个周期性推送机制值得理解。Hermes 运行时会利用空闲时刻主动提示 Agent 评估最近的交互并提取关键事实——在上下文窗口填满、旧轮次被压缩掉之前。Agent 在这次主动刷新中没有标记的事实就不会存活。这是要用或者丢弃的记忆管理方式。

  深度研究：不仅仅是花哨的网页搜索

  当你交给 Hermes 一个复杂的研究任务时，它会先调用 think_tool——一个强制性的策略暂停，促使模型在做任何事情之前阐述一个实际的调查计划。

  
   映射数据向量

   定义范围

   形成假设

  

  只有在这个规划阶段之后，Agent 才能开始执行。

  然后它并行化。ConductResearch 工具不会发出单个查询。它将特定的研究主题委托给独立的子 Agent，每个都有自己的干净上下文窗口、隔离的终端会话和受限的工具集。

  
   一个子 Agent 可能通过无头浏览器抓取监管文件

   另一个查询数据库

   第三个运行 Python 脚本生成统计分析

  

  它们同时执行，并将结构化的 JSON 返回给主编排器。

  并行工作完成后，Agent 再次调用 think_tool。这第二次过程强制综合：评估返回了什么，检查是否有缺口，判断目标是否达成。如果没有，循环用新的研究向量迭代。如果有，它调用 ResearchComplete 并进入报告生成阶段。

  最终报告由一个大上下文模型（至少 64K Token 窗口）将模块化的迷你报告合并成一个有引用来源的连贯文档。

  安全故事：为什么这比功能更重要

  这里是与 OpenClaw 比较让人不安的地方。

  在 2026 年 3 月 18 日到 21 日之间，四天内针对 OpenClaw 发布了九个 CVE，包括一个 CVSS 9.9 的关键漏洞，允许认证用户提升到管理员权限。到 4 月初，安全研究人员在 63 天窗口内追踪到 138 个 CVE。每天大约 2.2 个新漏洞。

  供应链数字更糟糕。安全公司 Antiy CERT 确认 ClawHub 市场中有 1,184 个恶意 Skill——高峰期大约每五个包中就有一个。SecurityScorecard 发现超过 135,000 个 OpenClaw 实例暴露在公共互联网上，使用不安全的默认配置。ClawHavoc 活动甚至不需要寻找漏洞。攻击者只是上传看起来令人信服的 Skill，等人来安装。

  Hermes 采取了根本更保守的方法。因为 Agent 基于你特定的工作流在内部生成自己的 Skill，它完全绕过了外部供应链攻击向量。你不是从匿名贡献者编写的公共注册表中拉取可执行代码。Agent 从你环境中观察到的成功中编写自己的操作知识。

  在基础设施方面，Hermes 强制终端执行的容器隔离、子 Agent 进程的加密命名空间隔离以及动态凭据轮换。它会在将任何外部数据注入系统提示之前扫描提示注入。

  动手实操：周末部署指南

  你需要安装 Git。仅此而已。安装程序会处理 Python 3.11+、Node.js v22、ripgrep 和 ffmpeg。支持 Linux、macOS、WSL2 和 Android（通过 Termux）。不支持原生 Windows。

  第一步：安装

  
   
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

   

  

  安装程序检测你的操作系统并自动配置依赖。Python 通过 uv——一个基于 Rust 的包管理器，创建一个无需 sudo 的隔离虚拟环境。

  第二步：运行 Setup

  
   
    hermes setup

   

  

  交互式向导引导你完成模型选择和初始配置。如果你从 OpenClaw 迁移，向导会自动检测 ~/.openclaw 并提供迁移你的设置、记忆、Skill 和 API 密钥。

  第三步：选择模型

  
   
    hermes model

   

  

  Hermes 与模型无关。你可以连接到 Anthropic、OpenAI、DeepSeek 或 OpenRouter（通过单个端点访问 400+ 模型）。对于深度研究任务，至少需要 64K 上下文 Token 的模型。

  如果你想要零 API 成本和完全的数据隐私，通过 Ollama 拉取本地模型：

  
   
    ollama pull qwen2.5-coder:32b

   

  

  然后将 Hermes 指向你的本地端点：http://localhost:11434/v1。完全自主，没有外部 API 调用，没有数据离开你的机器。

  第四步：设置网关

  
   
    hermes gateway setup

   

  

  将 Hermes 绑定到 Telegram、Discord、Slack、WhatsApp 或 Signal。网关作为持久后台服务运行，所以你可以在 Agent 在你的服务器上运行重型任务时，从手机给它发消息。

  一个注意事项：消息界面非常适合监控和异步更新，但它们本质上是线性的。对于深度协作工作，比如复杂的代码库变更，消息线程很快就会成为瓶颈。对于那种交互，使用 CLI 或专用工作区。

  第五步：容器化执行

  
   
    hermes config set terminal.backend docker

   

  

  这确保所有 Agent 生成的代码在隔离的容器内运行。如果出了问题，你的主机系统不受影响。

  第六步：让它学习

  从简单的、可重复的任务开始：周报、PR 审查、API 数据处理、研究汇编。观察 Skills 目录。在成功完成后，你会看到新的 .md 文件出现——Agent 自编的操作手册。几周后，以前需要几分钟的任务开始只需要几秒钟。

  诚实评估：Hermes 的局限性

  本地推理的硬件现实

  文章建议通过 Ollama 拉取 qwen2.5-coder:32b 进行免费本地推理，这需要现实的检验。在主编排器上运行 32B 模型是可以的。但前面描述的深度研究并行化——多个子 Agent 每个都需要自己的活动推理线程和干净的上下文窗口——这需要严重的 GPU 资源。

  更现实的本地设置是对子 Agent 路由和数据提取使用较小的量化模型，保留 32B 模型给主编排器和最终综合。如果你只有一个消费级 GPU，预计并行研究工作流会严重瓶颈。

  自建 Skill 是脆弱的

  内部 Skill 系统绕过了 OpenClaw 的供应链风险，但当底层的世界发生变化时，Markdown 操作手册会失效。如果一个遗留 API 更新了它的认证流程，或者一个网站重新设计了它的 DOM，Agent 记住的程序就会失败。

  与具有可视化错误处理路径的确定性工作流工具不同，Hermes 必须失败、重新评估并从头重写 Skill。学习循环处理这个，但这不是即时的。

  除非你真需要，跳过 Tier 4 记忆

  文章提到了 LightRAG 和 Supermemory 集成，但对大多数单服务器设置来说，SQLite 全文搜索（Tier 3）提供了速度和召回率的最佳平衡。让平面 MEMORY.md 文件与重型外部向量数据库保持同步会引入延迟和状态冲突问题，不值得开销——除非你在运行企业级多 Agent 工作流。

  设置复杂性是真实的

  OpenClaw 让你从安装到工作 Agent 更快。如果你需要 50+ 平台集成和消费级简单性，OpenClaw 仍然是更易访问的选择。

  框架才两个月大

  版本 0.8.0 于 2026 年 4 月 8 日发布，开发速度非常激进。但项目仍在成熟中。预计会有粗糙的边缘。

  自我改进是渐进的，不是神奇的

  40% 的基准提升来自于持续数周的使用，而不是一个快速演示。不要期望一夜之间的转变。

  更大的图景

  AI Agent 领域正在分裂为两个阵营。连接（OpenClaw 的赌注：连接到一切、任何地方）对比认知（Hermes 的赌注：随着时间的推移变得更聪明）。两者对不同用例都有效。有些团队同时运行两者，用 OpenClaw 做接收和路由，用 Hermes 做深度分析工作。

  对你我这样的开发者来说，一个会真正学习的 Agent 的复利优势是很难忽视的。安装需要五分钟。学习循环会负责剩下的部分。

  关键选择指南

  
   
    
     需求
     推荐工具
    

   
   
    
     需要大量平台集成
     OpenClaw
    

    
     需要深度分析/研究
     Hermes Agent
    

    
     安全优先
     Hermes Agent（隔离架构）
    

    
     快速上手
     OpenClaw
    

    
     需要记忆/学习能力
     Hermes Agent
    

    
     企业多Agent工作流
     两者组合
    

   
  

  我的看法

  作为一个每天都在用 Hermes 的人，最让我惊讶的不是它的功能数量——而是随着时间的推移，它真的在变好。第三周的时候，我发现它开始主动提醒我之前做过的决策，而我完全没告诉它要记住。

  “你说过这个模块的测试覆盖率要保持在 80% 以上，我刚看到新代码把覆盖率拉低到了 72%。”

  这种主动性的来源不是某个单独的功能，而是四层记忆系统的相互作用。MEMORY.md 提供了基础事实，会话搜索提供了历史上下文，Skill 系统提供了可复用的知识。

  它的确不是完美的——本地推理的硬件需求是真实的，自建 Skill 在面对外部变化时是脆弱的。但对于任何运行重复性复杂工作流的人来说，一个会积累知识的 Agent 和每天重置的 Agent 之间，差距只会越来越大。

  说人话的总结

  Hermes Agent 的核心创新用一个词概括：复利。

  大多数 AI Agent 是”每次会话归零”模式——你花时间建立的上下文、发现的模式、调试出的解决方案，在会话结束后全部丢失。

  Hermes 打破了这种模式。它把每次成功的操作转化为永久的、可复用的知识。今天你花 30 分钟解决的问题，明天它自己就能搞定。后天，它可能在你发现之前就已经处理好了。

  用还是不用，取决于你是否愿意让你的 AI 拥有记忆。

  
   
    版权所有，本作品采用知识共享署名-非商业性使用 3.0 未本地化版本许可协议进行许可。转载请注明出处：https://www.wangjun.dev//2026/06/hermes-agent-remembers-what-it-learned/
   

  

  
   Related posts

   
     Karpathy的4条CLAUDE.md规则减少30%错误，我加了4条后降到5% 

     95%的开发者都在用错AI Agent——一份Hermes实战指南 

     Scrapling：56k 星的 Python 爬虫框架，能自动适应网站结构变化 

     不用 Claude Code 也能搭专业 AI 编程环境——OpenCode + OpenSpec 完整方案 

     OpenBMB VoxCPM2：2B 参数开源 TTS，支持 30 种语言、声音设计和语音克隆 

     向量检索搞不定 PDF？试试 Docling + 层级树 + Gemma 3.5 Flash 这套结构化方案
