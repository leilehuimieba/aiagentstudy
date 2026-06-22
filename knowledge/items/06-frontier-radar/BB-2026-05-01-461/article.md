# Stop Writing Specs, Start Writing Facts — The Entire SDD Movement Is Obsolete

- BestBlogs URL: https://www.bestblogs.dev/article/225fb88f
- Original publisher URL: https://www.wangjun.dev/2026/06/stop-writing-specs-start-writing-facts/
- Source: BestBlogs / 王俊博客
- Publish time: 2026-06-05 00:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 3441

---

1. 核心矛盾：Spec 是对模型的预测，不是与模型的契约
  

  Spec-Driven Development（SDD）在过去十个月里爆发式增长：Spec Kit 获近九万星、Kiro 来自 AWS、OpenSpec 半年三位数增长、BMAD 近五万星——五个主要框架加起来超过二十万 GitHub Star。

  但作者 Jaroslaw Wasowski 今天要收回自己之前写的五篇鼓吹 SDD 的文章。

  理由很简单：一份在 Sonnet 3.5 时代写的单元测试，穿越了 3.7、4、Opus 4.5+ 四个模型版本依然通过 CI。而描述同一 endpoint 的 1500 字 spec，被每个模型重新理解了一遍——四次重解释。

  Spec 不是契约，是对模型的预测。模型在变，预测就永远不准。

  2. 为什么 Spec 注定不靠谱

  非确定性机制

  LLM 读同一段 prose，本质是在回答”这个句子统计上最可能是什么意思”，而不是”作者精确想表达什么”。即使在 temperature 0.0 下，独立研究显示同一 prompt 在确定性模式下产生了 80 个不同的输出。

  根本原因不是 prompt 写得不好——是系统性的：浮点数非结合性、批调度、fused-attention kernel。这些你没法用更好的 prose 修复。

  

  最反直觉的数据来自 IBM 在金融领域的 RAG 研究：100B+ 模型在同 prompt 下只有 12.5% 的 run 产生完全一致输出，而 7-8B 的小模型却能做到完全一致。

  “等模型变好 spec 就能用了”这个策略，恰恰和实际趋势相反。

  意图差距（Intent Gap）

  微软研究院的 Shuvendu K. Lahiri 称之为 intent gap——”AI 生成的代码看起来合理，但不是构建时确保正确”。自然语言 spec 是 informal 且不可检验的。SDD 把”一个统计近似”当成了”一个答案”。

  Spec Drift

  Spec Kit 在 2026 年 5 月发布了 /speckit.spec-drift 命令。一个框架需要专门出一个命令来处理 spec 漂移——这本身就证明了 drift 是真实的运营风险。

  3. 什么是 Fact：一个可执行断言

  Fact 就是机器能自己检查的东西。测试通过/失败，exit code 0 或非 0。不需要模型解读，不需要采样，没有情绪。

  

  粒度分三层：

  
   单个测试：一个输入/输出对

   属性（Property）：全称量词谓词——”对所有已排序列表，binary_search 的结果都是正确的”

   契约（Contract）：前置条件 + 后置条件 + 不变式（Design by Contract 风格）

  

  每一个都是可执行断言，运行时验证，通过或失败。没有”看情况”。

  57 年的连续性

  Facts-first 不是新范式，是 57 年零散工作的 AI 时代综合：

  
   1969：Hoare triple {P} C {Q}——行为的最小事实单元

   1992：Bertrand Meyer 的 Design by Contract——require/ensure/invariant

   2000：QuickCheck——属性基测试

   2026：Agent Behavioral Contracts——AI 时代延续

  

  John Hughes 在 Quviq 的真实案例：六万行生产 Erlang 代码，450 行 PBT 测试，检测出 25 个 bug——包括例子测试无法触及的 race condition。测试代码与生产代码比例为 1:133。

  

  4. SDD 依然有用的三个场景

  作者坦诚地给出了 SDD 的适用边界：

  
   合规与监管：DO-178C、ISO 26262、EU AI Act——这里 Ceremony 就是产品本身

   跨团队 B2B 集成：五百个工程师二十个团队时，协调成本超过实现成本

   新人入职与知识传递：新人读 spec，不是读测试

  

  一个简单的判断标准：这个制品会被团队以外的人阅读吗？ 审计、合作伙伴、新员工——是，则保留为 SDD。不是，则迁移到事实集。

  

  5. 90 天迁移计划

  Phase 1 — 审计（第 1-30 天）

  把现存 spec 分成三堆：

  
   团队成员以外的人会读的 → 保留（SDD zone）

   没人打开过的死文档 → 弃用候选

   生产中只有 prose 声明的隐式不变量 → 溯源候选

  

  用 agent 反向工程运行时不变量。交付物：@draft 事实列表 + 弃用候选列表。

  Phase 2 — 转向（第 31-60 天）

  把边界 spec 转为事实：API 契约 → Pact 测试，属性/不变量 → Hypothesis 或 QuickCheck，数据模型不变量 → 运行时断言。

  新功能并行运行 30 天——spec 和事实共存，获得 A/B 置信度。

  Phase 3 — 门禁（第 61-90 天）

  facts check 成为必须通过的 CI 步骤，阻断合并。新功能需要在实现前先写一个会失败的事实——TDD 节奏的新外衣。

  

  实践经验：Facts check 验证整个仓库使用的 tokens 比朗读一次 spec 还少。迁移不仅降低认知开销，还节省 API 费用。

  6. 六个结论

  
   Spec 是对模型的预测，不是与模型的契约。 Prose 每次调用都被 LLM 采样——0 温度也不例外。

   Fact = 机器可检验的可执行不变量。 它穿越模型升级，因为它不经过模型解读。

   SDD 在审计、合作伙伴、新员工会读的地方获胜。 其他地方它都输了。

   90 天迁移：审计 → 转向 → 门禁。 每个阶段都有独立的 ROI 信号。

   从明天早上开始： 挑一个只存在于 spec 中的不变量，写一个测试，加入 CI。这，就是一个事实。

   归根结底： PRD 会消失。Spec 正在退出内循环。只有事实在哪儿都能活。

  

  

  7. 总结

  SDD 赢得了工具战争——近九万 Star、二十万生态星。但它输掉了认识论战争：非确定性、意图差距、spec drift 不是待修复的 bug，它们是系统的运作方式。

  Facts-first 不是新范式，是 57 年形式化方法的 AI 时代合成。从 Hoare triple 到 Agent Behavioral Contracts，正确的道路一直存在——只是在 AI 时代才真正找到了用武之地。

  从明天开始，写一个事实。就一个。一天也行。

  
   
    版权所有，本作品采用知识共享署名-非商业性使用 3.0 未本地化版本许可协议进行许可。转载请注明出处：https://www.wangjun.dev//2026/06/stop-writing-specs-start-writing-facts/
   

  

  
   Related posts

   
     不用 Claude Code 也能搭专业 AI 编程环境——OpenCode + OpenSpec 完整方案 

     手把手教你写第一个 Claude Code 技能（Skill）：一个能帮你省几十个小时的项目记忆系统 

     Scrapling：56k 星的 Python 爬虫框架，能自动适应网站结构变化 

     实测 Qwen3.7-Max vs Claude Opus 4.6 vs GPT-5.5：Agent 场景才是真正战场 

     OpenBMB VoxCPM2：2B 参数开源 TTS，支持 30 种语言、声音设计和语音克隆 

     学 AI 最慢的方式是上课——真正有效的方法是即时学习
