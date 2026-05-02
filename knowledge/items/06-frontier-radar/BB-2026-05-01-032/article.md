# 一文读懂 Andrej Karpathy：从 OpenAI 到 Software 3.0

- BestBlogs URL: https://www.bestblogs.dev/explore/topics/andrej-karpathy-profile
- Extraction: DOM text from BestBlogs page
- Extracted chars: 4491
- Original publisher URL: https://x.com/karpathy

---

基本信息
职位：AI 研究员、AI 教育者、连续创业者
所属机构：Eureka Labs 创始人；前特斯拉 AI 高级总监；OpenAI 创始团队成员；Stanford 博士
X / Twitter
GitHub
个人网站
更多
标志性贡献
OpenAI 创始团队与 LLM 早期布道

Karpathy 于 2015 年加入 OpenAI 创始团队担任研究科学家，参与了 GPT 系列前期研究方向的奠基工作，2017 年离开后仍在 GPT-2 / GPT-3 时代以技术写作和演讲持续解释“什么是 LLM、它为什么重要”。2023 年他短暂回到 OpenAI 负责中训练（midtraining）与合成数据相关团队，最终于 2024 年再次离开转向独立教育创作。即便他在 2025 年底也罕见地写下“我作为一名程序员从未感到如此落后”，把当下的范式跃迁称为行业“9 级地震”。在中文 AI 圈，他被反复称为“OpenAI 出来的 AK”，影响力很大程度来自“把研究讲给所有人听”的能力。

特斯拉 Autopilot 视觉栈与端到端神经网络化

2017–2022 年，Karpathy 担任特斯拉 AI 高级总监，主导从手工规则视觉管线向端到端神经网络的迁移，期间还短暂参与 Optimus 机器人项目。这段经历让他对“现实世界的边角案例”有强烈的直觉，也是他后来反复强调“演示 vs. 可靠产品的鸿沟”、“自主性滑块”等概念的来源。他在 2025 年试乘 HW4 上的 FSD v13 后公开称其为“近乎完美”的驾驶体验，并据此反思未来 AI 架构。

Eureka Labs 与 AI 原生学校

2024 年 7 月，Karpathy 创立 Eureka Labs，定位为“AI 原生学校”——用专家课程加 AI 教学助手的“老师 + AI 共生”模式，第一门课 LLM101n 直接带学生从零训练自己的 LLM。这一方向延续了他在 Stanford 设计 CS231n 的教育习惯，也回应了他在多个长访谈中提出的“专家把 AI 教好，再让 AI 教所有人”的设想。他自己也持续示范如何用 LLM 当“个人知识库”——把材料拆成可复习的笔记本，让模型陪练。

Karpathy 做客 No Priors（Sarah Guo & Elad Gil 主持），讲“每天 16 小时管理智能体团队”和 AutoResearch 实验。来源：No Priors Podcast, 2026-03-20。

📺 完整访谈与中文摘要 · BestBlogs 站内

nanochat / nanoGPT / minGPT / micrograd 教育性开源

Karpathy 的 GitHub 长期被视为 LLM 入门教科书：micrograd 用几百行实现自动求导，nanoGPT 是“最小可用”的 GPT 训练框架，minGPT 把 GPT 解释成可阅读代码，2025 年发布的 nanochat 则把训练 GPT-2 级模型的成本压到 100 美元以内、最终在 1 月 31 日的版本里降到约 73 美元、仅需单台 8xH100 节点 3 小时。同年底，他还放出 llm-council——一个让多个前沿模型彼此匿名互评的 Web 应用——继续把“看模型怎么思考”变成可上手的工具。这些项目的共同点是：极简、可复刻、不靠工业级框架。

Software 3.0 框架与上下文工程方法论

在 2025 年 6 月 YC AI Startup School 的演讲《Software Is Changing (Again)》中，Karpathy 提出软件正从“代码 1.0、神经网络权重 2.0”迈向“以英语提示驱动 LLM 的 3.0”，并归纳了 LLM 的“锯齿状智能”“顺行性遗忘”等心理学。同期他在 X 上力挺“上下文工程”这一术语，强调精心填充上下文窗口比措辞技巧更接近真实工业实践。2026 年初他进一步用“文件优于应用”框架解释：未来软件更像是一组 AI 原生的传感器与执行器，由 LLM 按需编排出定制临时应用——这是 Software 3.0 的具体落地形态。这一系列框架成为 2025-2026 年 AI 行业讨论被引用最多的概念。

Karpathy 在 YC AI Startup School 2025 演讲《Software Is Changing (Again)》，提出 Software 3.0 与 LLM 心理学的现场。来源：Y Combinator, 2025-06-17。

📖 演讲深读（Latent Space 整理）· BestBlogs 站内

核心观点
2026-04-09在 X 上回应一组关于人类与 AI 能力差距的讨论

Karpathy 指出，AI 能力的“认知鸿沟”正在扩大——不是模型与人类之间的鸿沟，而是“懂得用 AI 的人”与“不懂得用 AI 的人”之间的鸿沟。他强调真正决定生产力差异的是工程直觉和上下文构建能力，而非工具本身。

2026-03-09对 nanochat 进行自主研究（autoresearch）实验后在 X 上汇报

Karpathy 让一个智能体自主对 nanochat 进行调优，识别出 20 项可叠加的改进（QKnorm 缩放、AdamW 参数、权重衰减等），把“训练到 GPT-2 水平”的耗时从 2.02 小时压到 1.80 小时。他认为，这种“把人类从研究循环里逐步搬出去”的工作流，将是前沿实验室的“最终 Boss 战”。

2026-02-19用一小时“氛围编程”做出有氧运动看板后，在 X 上发表的反思

Karpathy 认为，独立、预构建的 App Store 模式正在过时：未来更像是一组 AI 原生的传感器与执行器，由 LLM 按需编排出“一次性的、定制的临时应用”。行业要从面向人类的 Web 界面转向“智能体原生”接口（API/CLI），界面本身要为 agent 重新设计。

2025-12-202025 年 LLM 年度盘点（X 长串），由宝玉翻译为中文

Karpathy 用六个范式转变总结 2025：可验证奖励的 RL 替代纯模仿、AI 智能像“召唤幽灵”一样参差不齐、LLM 应用层（Cursor 等）成为新软件范式、AI 走向本地化（如 Claude Code）、Vibe Coding 让代码变得廉价、未来大模型迎来“图形界面时代”。他强调 LLM 的潜力被挖掘得不到 10%，2025 既是“天才也是智障”。

2025-10-17Dwarkesh Patel 长访谈：AGI 仍需十年

Karpathy 反对“AGI 即将到来”的口号，认为 LLM 仍存在持续学习不足、多模态弱、计算机交互薄等关键缺陷。他用“用吸管吸取监督”形容当前的强化学习——奖励稀疏且噪声大，与人类细致反思的学习方式相差甚远。他还警告合成数据中的“模型坍塌”问题，并把 AGI 对经济的影响描述为渐进式融入 2% GDP 增长的过程。

这条观点的原始来源——Dwarkesh Patel 长访谈，Karpathy 系统阐述 AGI 时间表与对 RL 的批评。来源：Dwarkesh Patel, 2025-10-17。

📺 完整访谈与中文摘要 · BestBlogs 站内

2025-06-25在 X 上回应 Tobi Lütke 提出的“上下文工程”一词

Karpathy 力挺“上下文工程”代替“提示工程”：精心填充上下文窗口（任务描述、few-shot、RAG、多模态、工具、历史状态）才是工业实践的核心。他把整个工作描述为一门同时讲究艺术与科学的工程，远不止改写一句 prompt，并提醒大家“ChatGPT wrapper”这一称呼极度低估了真实工程量。

代表作品
Software Is Changing (Again) — YC AI Startup School 2025
talk

2025 年 6 月在 YC AI Startup School 的主题演讲，提出软件 3.0、LLM 心理学和“自主性滑块”等被广泛引用的概念。

nanochat
project

全栈、极简的 LLM 训练 + 推理仓库，演示如何在 100 美元成本内训练出 GPT-2 级模型。

nanoGPT
project

“最简、最快”的中等规模 GPT 训练/微调实现，是 LLM 入门最常被引用的代码教科书。

minGPT
project

用极少的代码把 GPT 训练管线讲清楚，强调“可读、可复刻”而非性能。

micrograd
project

用几百行 Python 实现自动求导引擎和迷你神经网络库，是“神经网络从零到一”课程的核心教具。

llm.c
project

用纯 C/CUDA 训练 LLM 的实验性仓库，去掉 PyTorch 等抽象，露出底层数学和算子调度。

Neural Networks: Zero to Hero
talk

面向所有人的神经网络与 LLM 系列课程，配合 micrograd / makemore / nanoGPT 一步步从零搭建。

重要时间线
2011-09-01

在 Stanford 攻读博士，研究方向为卷积/循环神经网络，参与设计 CS 231n（Stanford 第一门深度学习课）。

2015-12-01

加入 OpenAI 创始团队担任研究科学家。

2017-06-01

出任特斯拉 AI 总监，主导 Autopilot 视觉栈神经网络化，并短暂参与 Optimus。

2023-02-01

回到 OpenAI，负责中训练（midtraining）与合成数据相关团队建设。

2024-02-01

再次离开 OpenAI，转向独立 AI 教育内容创作。

2024-07-16

宣布创立 Eureka Labs，定位“AI 原生学校”，首门课为 LLM101n。

2025-06-17

在 YC AI Startup School 发表《Software Is Changing (Again)》演讲，提出软件 3.0。

2025-10-13

发布 nanochat：全栈、极简的 LLM 训练 + 推理流水线。

2025-10-17

做客 Dwarkesh Patel 长访谈，主张 AGI 仍需约十年。

2025-12-20

发布 2025 年 LLM 年度盘点，归纳六大范式转变。

2026-01-31

宣布 nanochat 进一步降本到约 73 美元、单节点 3 小时即可训练出 GPT-2 级模型。

2026-03-20

做客 No Priors 播客，详谈代码智能体、AutoResearch 与 AI 循环时代。
