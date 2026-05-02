# Claude's Strongest Sonnet Model 4.6 is Here, Featuring a ...

- BestBlogs URL: https://www.bestblogs.dev/en/article/ba9a21ac
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 2216
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651017513&idx=2&sn=781e04048d4f59a46572accfa0603ee8

---

对编码、计算机使用、长上下文推理、智能体规划、知识工作和设计进行了全面升级。

机器之心编辑部

大年初二，海外就开始发新模型了！

这次是 Anthropic，率先发布了他们称之为「我们目前能力最强的 Sonnet 模型」Claude Sonnet 4.6。

Claude 称，新模型对编码、计算机使用、长上下文推理、智能体规划、知识工作和设计进行了全面升级。

Beta 版还包含 100 万 token 的上下文窗口。

在价格方面，对于免费和专业版用户，Claude Sonnet 4.6 现已成为 claude.ai 和 Claude Cowork 的默认模型。定价与 Sonnet 4.5 保持一致，仍为每百万输入 token 3 美元，每百万输出 token 15 美元。

那么具体性如何？在 GDPval-AA 测试中，Claude Sonnet 4.6 甚至略微领先于 Anthropic 刚刚发布不久的 Opus 4.6。

接下来，就让我们仔细看下技术博客介绍。

计算机使用

2024 年 10 月，Claude 率先推出了通用的计算机使用模型。当时，这种技术「仍处于实验阶段 —— 有时操作繁琐且容易出错」。

AI 计算机使用的标准基准 OSWorld 展示了 Claude 模型的进步程度。该基准会在模拟计算机上运行真实软件（Chrome、LibreOffice、VS Code 等），设置数百项任务。该基准也没有没有特殊的 API 或专用连接器；模型看到计算机并与其互动的方式与人非常相似：点击（虚拟）鼠标和在（虚拟）键盘上打字。

在过去的十六个月里，Sonnet 模型在 OSWorld 上的性能稳步提升。这些改进在基准测试之外也可见一斑：早期的 Sonnet 4.6 用户在多项任务（诸如浏览复杂电子表格或填写多步骤网页表单）中，看到了达到人类水平的能力，并且能在多个浏览器标签页中整合处理信息。

当然，该模型在使用计算机方面仍落后于最熟练的人类。但进步的速度依然显著。这意味着：计算机使用的价值在提升 —— 并且表明能力更强的模型已指日可待。

图表比较了多个 Sonnet 模型在 OSWorld 基准上的得分。注：Claude Sonnet 4.5 之前的得分基于原始 OSWorld 测量；从 Sonnet 4.5 开始使用 OSWorld-Verified。OSWorld-Verified（2025 年 7 月发布）是原始 OSWorld 基准的原位升级，对任务质量、评估评分和基础设施进行了更新。

与此同时，计算机使用也带来了风险：恶意行为者可能试图通过提示注入攻击，将指令隐藏在网站中来劫持模型。

Anthropic 致力于提高模型抵抗提示注入的能力 —— 其安全评估显示，与其前代 Sonnet 4.5 相比，Sonnet 4.6 在这方面有重大改进，表现与 Opus 4.6 相近。

评估 Claude Sonnet 4.6

除了计算机使用，Claude Sonnet 4.6 在各项基准测试中均有提升。它的智能水平接近 Opus 级别，但价格更实惠，使其适用于更广泛的任务。

一个表格展示了流行基准测试中 Sonnet 4.6 与其他前沿模型的相对性能比较。

Anthropic 的早期 Claude Code 测试发现，用户大约有 70% 的时间更喜欢 Sonnet 4.6 而非 Sonnet 4.5。

用户报告说，它在修改代码前能更有效地理解上下文，并能整合共享逻辑而非简单复制。

相比于 11 月发布的前沿模型 Opus 4.5，用户甚至有 59% 的时间更喜欢 Sonnet 4.6。他们评价 Sonnet 4.6 在过度工程化和「偷懒」方面显著减少，在指令遵循方面有明显改进。用户报告了更少的虚假成功声明、更少的幻觉，以及在多步骤任务中更一致的执行力。

Sonnet 4.6 的上下文窗口为 100 万 token，足以在单个请求中容纳整个代码库、长篇合同或数十篇研究论文。更重要的是，Sonnet 4.6 能有效地在所有上下文中进行推理。这使得它在长程规划方面表现更佳。

在 Vending-Bench Arena 评估中特别清晰地看到了这一点。该测试评估模型长期运营（模拟）业务的能力 —— 并且包含竞争元素，不同 AI 模型相互竞争以获取最大利润。

Sonnet 4.6 发展出一种有趣的新策略：它在模拟的前十个月大力投资于产能，支出远超竞争对手，然后在最后阶段急剧转向专注于盈利能力。这一转向的时机使其最终远远领先于竞争对手。

图表显示 Sonnet 4.6 在 Vending-Bench Arena 上优于 Sonnet 4.5：通过早期投资产能，然后在最后阶段转向盈利。

Claude Sonnet 4.6 已经向哪些用户开放？

Claude Sonnet 4.6 现已面向所有 Claude 套餐、Claude Cowork、Claude Code、API 以及所有主流云平台开放。Anthropic 也已将免费套餐默认升级至 Sonnet 4.6 版本 —— 现在包含文件创建、连接器、技能和压缩功能。

如果你是开发者，也可以通过 Claude API 快速开始使用 claude-sonnet-4-6。
