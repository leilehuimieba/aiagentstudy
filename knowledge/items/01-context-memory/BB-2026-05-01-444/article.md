# Just In: Windows' 'Dream Machine' Turns Your PC into an Agent Workstation

- BestBlogs URL: https://www.bestblogs.dev/article/42e93f45
- Original publisher URL: https://www.ifanr.com/1667971?utm_source=rss&utm_medium=rss&utm_campaign=
- Source: BestBlogs / 爱范儿
- Publish time: 2026-06-03 22:12:42
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 5660

---

微软和 OpenAI 的蜜月期，曾经是整个 AI 行业最重要的联盟。

  一方握着模型，另一方手握云服务、办公软件、开发者工具和企业客户，双方互相成就，几乎让微软在 AI 时代提前拿到一张头等舱门票。但即便联盟再紧密，微软也不能永远把最关键的 AI 想象力寄托在别人身上。

  尤其是在双方关系开始脱钩之后。

  

  刚刚召开的 Build 2026 因此变成一场特殊的发布会。微软比以往任何时候都需要一场酣畅淋漓的 AI 胜利，向外界证明自己究竟是 AI 时代的主角，还是依旧只是 OpenAI 的云服务商？

  从 MAI 模型、Azure AI Foundry、到量子计算以及本地智能体能力，再加上黄仁勋和龙虾之父的相继站台，微软展示了一整套覆盖开发、模型、数据、算力和治理的完整生态，其目标也很清晰：将 AI 从 OpenAI 主导的模型红利，转变为微软主导的平台生意。

  微软自研模型发布， MAI 补上 AI 供应链最关键一环

  相比去年，微软这次把模型放在了更重要的位置。微软 CEO 纳德拉称，Microsoft Foundry 目前已有超过 11000 个模型，覆盖 OpenAI、Anthropic 和微软自研 MAI 模型。

  微软的判断是，企业和开发者不会只依赖一个模型完成所有任务。不同任务会对应不同模型，也会受到延迟、成本和能力边界的约束。因此，模型目录、模型选择、运行环境和企业治理，会一起构成新的平台竞争点。

  今天，微软自研模型家族正式一口气推出了七款新模型，覆盖推理、代码、图像、语音和转录等方向。

  

  MAI Thinking 1 是其中的推理模型。它采用稀疏 MoE 架构，35B active 参数，总参数规模约 1T，支持 256K token 上下文，足以容纳大约 600 页文档。

  微软 AI 负责人穆斯塔法·苏莱曼强调，这个模型没有使用第三方模型蒸馏，训练数据来自干净且合规授权的数据，并在预训练中排除了 AI 生成内容。它已在 Microsoft Foundry 私有预览，之后会进入 MAI Playground 公测。

  

  代码模型 MAI Code 1 Flash 面向日常开发工作流。它由微软端到端训练，使用干净且合规授权的数据，正在向 Visual Studio Code 中的 GitHub Copilot 个人用户推出，入口包括模型选择器和默认自动选择器。

  微软称，这个模型针对 GitHub Copilot harness 做了训练和适配，支持 Agentic coding，也支持 adaptive thinking。简单请求保持简洁，复杂任务会投入更多推理预算。

  微软把 MAI Code 1 Flash 直接拿来和 Claude Haiku 4.5 比较。

  MAI Code 1 Flash 在 SWE Bench Pro 上达到 51.2%，高于 Claude Haiku 4.5 的 35.2%；在 IF Bench 精确指令跟随上领先 28.9 分，在 Advanced IF 上领先 14.5 分。它将支撑微软 GitHub Copilot 的常见编码场景，尤其是代码修改、多轮指令和真实开发环境里的 Agent 任务。
   

   图像和语音模型也被纳入 MAI 体系。

  MAI Image 2.5 和 Flash 版本支持文本生成图像和图像编辑，已经进入 PowerPoint，并会扩展到 OneDrive 和 Foundry。

  

  MAI Transcribe 1.5 支持 43 种语言，微软称其速度达到竞品 5 倍，正在集成到 GitHub、Teams、Copilot 和 Dynamics 365 Contact Center。

  MAI Voice 2 支持 15 种语言，可通过短样本适配声音，同时内置防滥用保护；低成本版本 MAI Voice 2 Flash 也在计划中。

  微软还把 MAI 模型和自己的芯片联系起来。MAI Thinking 1 已针对 Maia 200 优化，端到端运行 MAI 模型时，还能获得 1.4 倍每瓦性能提升。

  

  企业定制也是 MAI 模型的重要方向。未来所有企业不仅会调用模型，也会把自己的流程训练进模型。

  为此，微软还发布了 Microsoft Frontier Tuning，核心是 reinforcement learning environments。企业可以把真实工作轨迹、任务步骤、决策、工具调用和评价标准变成训练环境，让模型学习组织内部的工作方式。

  PC 变成 Agent 工位，你的桌面就是数据中心

  除了模型，微软也把重点转向本地算力。

  

  Surface RTX Spark Dev Box 是这部分最值得一提的产品。纳德拉把它称为面向开发者的「dream machine（梦中神机）」。这台设备提供 1 petaflop AI 算力、20 个 CPU 核心和 128GB 统一内存，计划在今年秋季推出。

  

  Surface RTX Spark Dev Box 基于 Nvidia RTX Spark 平台。正如 APPSO 前几天所报道的，RTX Spark 是面向 PC 的下一代 SoC，把 CPU、GPU 和 AI 能力整合到一颗芯片中，并支持统一内存架构和集成 DRTM。

  英伟达 CEO 黄仁勋在视频连线中表示，PC 正在从个人电脑走向个人 AI。他举例称：用户外出时，可以给自己的 PC 发消息，让本地 Agent 调用工具、修改代码、推进设计，再和用户继续迭代。

  PC 不再只是一个被人操作的工具，也开始变成可以持续运行任务的 AI 助手。

  此外，微软还为 Surface RTX Spark Dev Box 预装开发优化的 Windows 11 Pro，内置 VS Code、WSL、PowerShell 7、GitHub Copilot、Coreutils for Windows 等工具。

  现场演示中，这台设备默认没有新闻流、组件弹窗和通知，使用深色模式；Windows Insider 版本还加入了纵向任务栏，不仅开发工具被进一步系统化，命令行和容器体验也更接近 Linux。

  

  硬件上，它采用阳极氧化铝 3D 打印一体机身，拥有 1000 个通风孔，热设计功耗 100W，接口包括 USB-C、USB-A、HDMI、以太网和耳机接口。

  Windows 将在 AI 时代大有作为。本地 AI 要让 PC 成为 Agent 工作流的一部分：开发者可以在本地调试、运行模型、调用工具、看日志、开容器、跑子 Agent，再把更大规模任务交给云端。

  Agent 需要新入口，微软探路下一代 AI 终端

  相比 Surface RTX Spark Dev Box 面向开发者，Project Solara 更像微软对 Agent 设备形态的提前试探。下一台计算机不会只是一台设备，而是一组协同工作的设备。

  微软展示了两类参考设备。

  第一类是固定在桌面上的工作终端，基于联发科芯片。

  

  用户走近后，系统会安全识别身份，并让用户进入自己的 Agent 工作环境，访问基于 Work IQ 的 Microsoft 365 Copilot。

  它可以显示当天重要事项，也支持点按或语音交给 Agent 处理任务，还能作为 Windows PC 伴侣，或通过 Windows 365 接入 Cloud PC。它更像企业办公桌上的 Agent 控制终端，负责身份识别、任务提醒、语音交互、Copilot 调用和 Cloud PC 接入。

  第二类是可佩戴数字工牌，使用 Qualcomm 可穿戴芯片，面向移动工作场景。

  

  演示中，用户通过指纹解锁后，要求 Copilot 为社交媒体帖子收集现场素材。工牌负责拍摄画面，Agent 负责挑选镜头、清理画面，并发送给本人和团队审阅。发布会还展示了医疗场景：护士可用它进行免提语音记录、区分说话人、核验生命体征、扫描药物并验证护理流程。

  这两类设备只是参考形态。

  手机和 PC 仍然重要，但一些工作场景需要更靠近人、空间和传感器的硬件。面对未来的 Agent 时代，企业可以更换 Agent，调整外观、屏幕、传感器和输入方式，在同一硬件和软件基础上适配不同垂直行业。

  龙虾之父站台，微软给个人 Agent 加上企业护栏

  Surface RTX Spark Dev Box 讲的是本地算力，Project Solara 讲的是新设备形态，OpenClaw on Windows 则把焦点转到个人 Agent 如何安全进入企业。

  微软展示了适用于 OpenClaw 的 Windows 套件，可以帮助用户设置自己的 OpenClaw，或连接已经托管在 Windows 和 WSL 中的 OpenClaw。

  

  应用里可以查看 gateway、参与 OpenClaw 的其他机器、会话和使用情况，也能快速进入 chat、canvas 和主控制台。

  安全演示围绕文件权限展开。

  OpenClaw Windows Companion app 允许用户控制 Agent 能访问哪些文件夹，以及这些文件夹是只读、可写还是隐藏。它也可以配置剪贴板访问、联网权限等细粒度选项。

  微软在现场要求 OpenClaw 删除桌面上的所有文件，并临时关闭 OpenClaw 自身的安全层，只保留 MXC 的系统级限制。由于桌面文件夹被设置为只读，OpenClaw 多次尝试删除和检查目录，最后仍无法删除文件，桌面上的 94 张 JPG 得以保留。

  

  龙虾之父 Peter Steinberger 也透露，过去几个月 OpenClaw 与 Microsoft、GitHub、OpenAI、Nvidia 等团队合作，增加了可观测性、自动权限模式，并重新设计访问控制。现在权限不再只有全部允许或全部禁止，用户可以指定哪些文件夹只读、哪些可写、哪些对 Agent 隐藏。

  他还宣布，OpenClaw 可以在公司内部运行，harness 本身已经插件化。企业可以接入自己信任的 Copilot、Codex 或其他系统，把已有规则带进 OpenClaw，再获得持续记忆、heartbeat，以及在 Slack 或 Teams 中使用 OpenClaw 的能力。

  AI 下半场，微软盯上企业平台入口

  除前述硬件和 Windows 更新外，微软还发布了更多产品。

  开发工具方面，微软发布新的 GitHub Copilot app。它更像一个 Agent 编码会话管理器，开发者可以同时启动多个 issue 会话，并用 Git worktree 隔离，让多个 Agent 并行工作。

  

  Agent Merge 则负责跟踪 PR 的 CI 检查、代码审查和合并冲突。微软还发布 Raven，这是一个 Agent first SDK，用于连接 backend as a service，处理身份、存储和数据库 schema 等后端问题。

  上下文能力由 Web IQ 承担。

  Agent 要进入企业流程，需要连接网络新信息、企业业务对象、实时运营状态、人员关系和组织流程。Web IQ 负责外部网络信息，支持网页、新闻、图片和视频，模型无关、MCP native，可接入任意 Agent runtime，让 Agent 的回答建立在更新、可验证的内容上。

  

  Copilot 也在升级为更复杂的工作入口。

  纳德拉称，今年夏天会把 chat、cowork 和 code 放入同一个 Copilot，并发布 Autopilots。首个 Autopilot 名为 Scout，面向 Copilot Frontier 用户开放，可在 Teams 群聊和 Outlook 线程中工作。

  企业治理层面，微软发布 Agent 365。它为 Agent 提供身份、权限、访问控制和合规管理，并接入 Entra、Defender 和 Purview。Agent 365 可管理托管在 Azure、AWS、GCP 或其他环境中的 Agent，也支持不同框架构建的 Agent。

  科研方向则是 Microsoft Discovery。纳德拉把它定义为面向科学发现的 Agent 平台，希望把论文研究、候选方案生成、仿真计算、实验设计和自动化实验室连接成连续流程。

  发布会最后，微软还正式发布了新一代量子芯片 Majorana 2，其量子比特平均寿命可达 20 秒，最高接近 1 分钟，比 Majorana 1 高约 1000 倍；操作时间为 1 微秒，尺寸仍为 0.01 毫米量级，并采用全数字控制。

  

  至此，这场拼图庞大且野心勃勃的发布会终于完整。AI 的第一阶段，主导行业叙事的是模型公司；第二阶段，主导产业落地的可能是平台公司。

  谁来选择模型，谁来分配任务，谁来管理 Agent，谁来定义权限和审计，谁就更接近企业 AI 的核心入口。当模型逐渐成为标准能力之后，真正决定价值归属的，将是承载这些模型运行的系统。

  如果说当年那张 AI 时代的头等舱门票，很大程度上是借助盟友 OpenAI 的力量抢下的；那么现在，微软已经坐进了驾驶舱，并打算亲自接管这架飞机的航向。
