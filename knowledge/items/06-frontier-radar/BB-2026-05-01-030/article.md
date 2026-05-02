# DeepSeek-V4 预览版发布

- BestBlogs URL: https://www.bestblogs.dev/explore/topics/deepseek-v4-preview-release
- Extraction: DOM text from BestBlogs page
- Extracted chars: 4608
- Original publisher URL: https://www.bestblogs.dev/article/95d5e07c

---

为什么值得关注

DeepSeek-V4 值得做成 Topic，不是因为它只带来一个“百万上下文”的标题，而是因为它把过去一年 DeepSeek 的几条技术线合到了一起：从 V3.2-Exp 的稀疏注意力，到 V3.2 的工具调用思考，再到 V4 的 Pro / Flash 双版本、1M 上下文默认化、Agentic Coding 优化和开源权重发布。对开发者来说，这意味着长文档、代码仓库、复杂工具调用轨迹不再只是“能塞进上下文”，还要以可承受的推理成本跑起来。12

事件时间线
2025-09-29

DeepSeek-V3.2-Exp 发布，引入稀疏注意力机制，提升训练与推理效率，并同步降价。

2025-12-01

DeepSeek-V3.2 正式版发布，强化 Agent 能力，并首次把“思考”融入工具调用。

2026-03-20

DeepLearning.AI 报道 DeepSeek 的华为布局，说明 DeepSeek 生态叙事已从模型延伸到硬件适配。

2026-04-24

DeepSeek-V4 预览版正式发布，包含 V4-Pro 与 V4-Flash，官网、App、API、开源权重和技术报告同步上线。

2026-04-25

量子位基于技术报告补充解读 V4 的 mHC、混合注意力、Muon 优化器、KV cache 压缩和国产芯片适配等细节。

核心变化与亮点

DeepSeek-V4 这次最容易被传播的标签是“1M 上下文”，但如果只把它理解为窗口长度增加，会错过真正重要的变化。V4 更像是 DeepSeek 把过去几代模型的效率路线做了一次集中发布：V3 系列已经证明 MoE、MLA、FP8 与低成本训练可以把开源模型推到前沿附近；V3.2-Exp 开始把稀疏注意力和 API 降价放在一起讲；V3.2 又把 Agent 场景里的工具调用思考单独拉出来强化。到了 V4，DeepSeek 把这些线索合并成 Pro / Flash 两个版本：Pro 负责拉高推理、知识和 Agentic Coding 的上限，Flash 负责把相近能力压到更低成本、更高吞吐的 API 服务里。这个产品拆分很关键，因为它说明 DeepSeek 不再只是在“发一个最强模型”，而是在给真实工作流提供不同的性价比档位。134

官方模型规格表：Pro / Flash 在参数、激活参数、预训练数据、上下文长度、开源与 API 服务上的差异。

1. 1M 上下文的重点不是“能装下”，而是“跑得起”

百万上下文过去常常是模型展示能力的一部分，但 V4 试图把它变成默认服务能力。官方明确说 1M 上下文将成为 DeepSeek 官方服务标配，这背后真正要解决的是 KV cache、注意力计算和显存成本，而不是简单扩大窗口。量子位对技术报告的解读提到，V4 通过混合注意力、压缩和稀疏选择等机制，把长上下文场景中的缓存与计算压力降下来；这与行业里围绕 KV cache 压缩、注意力变体、长序列稀疏化的研究方向一致。换句话说，V4 的亮点不只是“可以读更长”，而是把长文档分析、代码仓库理解、批量资料审阅、长链路工具调用放到更接近生产可用的成本区间。对于开发者和企业用户，这比单次 benchmark 更有现实意义。2242526

量子位技术报告解读图：CSA 先压缩 KV，再通过 lightning indexer 做 top-k 选择，解释了 1M 上下文降成本的技术路径。

这张结构图说明 V4 不是简单把窗口拉长，而是把注意力计算拆成“压缩、索引、选择、再计算”的流水线；下面的官方效率图则展示了这种设计最终落到计算量和 KV cache 上的结果。

官方长上下文效率图：对比 V3.2、V4-Pro 与 V4-Flash 在百万 token 序列下的单 token 计算量和累计 KV cache 大小。

2. Pro / Flash 双版本说明模型发布正在产品化

V4-Pro 和 V4-Flash 的分工很像一条成熟 API 产品线的开始：Pro 面向复杂推理、世界知识、代码和 Agent 任务；Flash 面向高频调用、低延迟、低成本和更广覆盖。此前很多模型发布会把所有能力放到一个模型名下，开发者只能自己在价格、速度和能力之间做取舍。V4 的双版本策略把这个取舍前置到官方产品设计里：复杂任务用 Pro，常规交互和成本敏感场景用 Flash。它也解释了为什么官方同时兼容 OpenAI 与 Anthropic API 格式，这降低了迁移门槛，让团队可以在现有调用层里切入 DeepSeek，而不是重写整套集成。1

官方 API 表：展示 deepseek-v4-pro 与 deepseek-v4-flash 的输入、输出价格和 1M 上下文配置。

3. Agent 能力不是口号，而是从 V3.2 延续过来的路线

V4 的 Agent 叙事不是凭空出现的。V3.2 已经把“思考融入工具调用”作为重要更新，官方 X 动态也把 API、工具使用思维和技术报告连接在一起。V4 在这个基础上进一步面向 Agentic Coding、长文档生成、复杂自动化工作流优化。这里的核心变化是：模型不只是回答问题，而是要在长上下文里保持状态、调用工具、阅读代码、改写文件、验证结果。新智元对 V3.2 Agentic 能力的解读、Cursor Composer 等 agentic coding 产品案例，都说明行业关注点正在从“模型是否聪明”转向“模型能否在完整工作流里稳定交付”。V4 的意义正是在这个方向上继续加码。4891036

4. 技术报告里的关键词：mHC、混合注意力、Muon 与硬件适配

量子位对 V4 技术报告的解读把几个关键词拉了出来：mHC 架构、混合注意力机制、Muon 优化器、KV cache 压缩以及国产芯片适配。它们共同指向一个主题：DeepSeek 仍然在围绕“更高效地训练和服务超大模型”做系统工程，而不是只堆参数。mHC 试图改善超大规模模型训练中的稳定性，混合注意力服务于长上下文效率，Muon 代表优化器路线的探索，硬件适配则对应中国模型公司绕不开的算力约束。结合 DeepSeek-V3 的降本论文、华为昇腾与 DeepSeek 的推理性能报道，以及 UE8M0 FP8 引发的国产芯片讨论，V4 可以看作 DeepSeek 继续把算法、训练、推理和硬件协同放在同一张工程图里。213141517

量子位技术报告解读图：从普通残差连接、Hyper-Connections 到 manifold-constrained Hyper-Connections 的结构变化。

5. Benchmark 需要看，也需要谨慎看

官方 benchmark 图能说明 V4 的目标很明确：在知识、推理、长上下文和 Agentic Capabilities 之间取得平衡，而不是只刷单一榜单。V4-Pro 在 Codeforces、Apex Shortlist、Terminal Bench、Toolathlon 等项目上的表现被放在 Claude、GPT、Gemini、Kimi、GLM 旁边比较，这对读者理解它的定位很有帮助。但 Topic 页面应把这些数字标注为“官方评测”而不是独立结论。真正有价值的后续验证，是看它在真实代码仓库、企业知识库、长文档审阅、多工具 Agent 中能否稳定复现成本和效果优势。12

官方 benchmark 图：覆盖 Knowledge & Reasoning 与 Agentic Capabilities，但解读时应保留“官方评测，需独立复测”的边界。

6. 开源竞争进入“持续追赶”阶段

V4 不是孤立事件。它发布前后，Kimi、Qwen、Gemma、GLM、Seed-OSS 等开放或开源模型都在快速迭代：有的强调 1M 或 512K 长上下文，有的强调编程与 Agent，有的强调端侧、多模态或硬件生态。LangChain 对开源模型跨越临界点的判断、ByteByteGo 对开源 LLM 架构的梳理、Andrew Ng 对中国开放权重模型和半导体优势的评价，都说明 V4 应该被放进更大的竞争框架中理解。它不是“开源模型第一次追上闭源”，也不是“闭源模型已经失去优势”，而是一个更务实的信号：开放模型正在用更快的发布节奏、更低成本和更贴近工程的能力，持续压缩闭源前沿的领先窗口。202329303132

量子位报道中的社区评价截图：讨论 DeepSeek、Kimi、Qwen 在受限算力下通过架构创新提高训练和推理效率。

7. 阅读这次发布时应保持的边界

这个 Topic 不应把所有官方 benchmark 都直接写成确定结论。更稳妥的读法是把信息分成三层：第一层是 official_fact，例如 V4 预览版发布、Pro / Flash 双版本、1M 上下文、API 与开源权重同步上线；第二层是 official_claim，例如官方 benchmark、Agentic Coding 反馈、与闭源模型的对比；第三层是 reported_analysis 与 community_evaluation，例如技术报告解读、社区对效率路线的评价、真实用户对成本和稳定性的观察。第三层可以帮助理解方向，但不能替代独立复测。对读者来说，最值得跟进的不是一句“是否超越某模型”，而是 V4 会不会在真实代码仓库、企业知识库、长文档审阅和多工具 Agent 中带来可复现的成本与效果改善。

各方观点
official
官方把 V4 定位为全新系列预览版，强调 Pro / Flash 双版本、1M 上下文、Agent 能力和开源权重。
— DeepSeek
technical-analysis
量子位的解读把重点放在 mHC、混合注意力、Muon 优化器和 KV cache 成本下降，提醒读者不要只看参数规模。
— 量子位
architecture-context
开源 LLM 的竞争正在围绕 MoE、注意力机制和后训练展开，V4 应放在这个架构演进背景中理解。
— ByteByteGo / Ahead of AI
ecosystem
吴恩达此前强调中国在开放权重模型与半导体上的优势，V4 的发布进一步强化了这个观察维度。
— Andrew Ng
competitive-landscape
V4 发布前后，Kimi、Qwen、Gemma 等开放模型也在快速更新，说明“开源追赶闭源”已经是持续竞争，而不是单点事件。
— LangChain / Kimi / Qwen / Google DeepMind
编辑后记

这版 Topic 的重点不是替 DeepSeek 的 benchmark 背书，而是帮助读者判断 V4 为什么重要、它从哪里来、它与开源模型竞争和 Agent 工作流有什么关系。页面发布前建议人工校对官方指标表述，尤其是与 GPT、Gemini、Claude 的对比，只保留“官方声称 / 第三方解读 / 需独立评测”的清晰边界。
