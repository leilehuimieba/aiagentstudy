# 2026-05-01 Hacker News Top Stories #

- BestBlogs URL: https://www.bestblogs.dev/article/4fad6520
- Extraction: DOM text from BestBlogs page
- Extracted chars: 29914
- Original publisher URL: https://supertechfans.com/cn/post/2026-05-01-HackerNews/

---

Copy Fail（CVE-2026-31431）利用 AF_ALG+splice 向页面缓存写入4字节可稳定本地提权并篡改只读文件，跨发行版易用，建议尽快打补丁或禁用相关模块以缓解多租户与容器高风险。
Claude Code 存在计费漏洞：提交信息含“HERMES.md”会被误算为额外用量致超额收费，虽承诺联系受影响者退款与补偿，但客服与响应被广泛质疑。
OpenAI 发现 GPT-5.x 对“地精”隐喻的偏好源自对“书呆子”个性的奖励强化并跨设置迁移，已在5.4起移除并清洗数据、5.5继续通过开发者指令抑制且改进审计。
提交或文档出现“OpenClaw”等触发词会让 Claude Code 拒绝、额外计费甚至断连，或被滥用于“关键词陷阱”式拒服攻击，暴露反滥用设计粗糙与责任不清。
比利时叫停核电退役并与 ENGIE 商谈国有化及建设新机组，以提升能源安全与自主性，核能的安全、成本与减碳角色仍引发激辩。
Zig 禁止在问题、PR、评论与翻译中使用 LLM，强调押注长期贡献者与社区质量，宁拒性能优化亦不牺牲可维护性。
Mozilla 等反对 Chrome Prompt API，指其模型耦合、隐私指纹与竞争风险高，主张先以扩展/实验验证后再推进开放中立标准。
因员工曝智能眼镜含隐私影像的人工审核问题，Meta 终止与肯尼亚外包商合作致千余人被裁并引发监管调查，凸显隐私滥用、人工审核依赖与外包劳权风险。
书摘回顾 AT&T 技师 Mark Klein 揭露“641A 房间”以分光复制骨干网全量流量供 NSA 监控，促成 EFF 诉讼并加剧国家安全与公民隐私之争。
西班牙国会推动改革数字服务法以遏制 LaLiga 反盗版引发的泛化 IP 封锁，强调技术比例原则与第三方权利保障，源于多起误封合法服务。
1. Copy Fail (Copy Fail) #

https://copy.fail/

一个名为“Copy Fail”的 Linux 本地提权漏洞（CVE-2026-31431），该漏洞存在于 2017 年至补丁发布期间的几乎所有主流 Linux 发行版内核中。漏洞利用了内核的 authencesn 模块中的逻辑缺陷，通过 AF_ALG 和 splice()系统调用，能够在内存中的页面缓存中写入 4 字节数据，从而实现对任意可读文件（如 setuid 二进制文件）的篡改，进而获得 root 权限。

该漏洞无需竞态条件或特定内核偏移，利用脚本体积仅 732 字节，使用 Python 3.10+ 标准库即可实现，且同一脚本可在 Ubuntu、Amazon Linux、RHEL、SUSE 等多个发行版上无修改运行，成功率 100%。攻击者只需拥有本地非特权用户账号，无需网络访问或其他特权。

漏洞影响范围广泛，尤其对多租户 Linux 主机、共享开发环境、容器集群、CI 构建服务器和云 SaaS 平台等环境危害极大，攻击者可通过该漏洞实现容器逃逸和跨租户攻击。单用户笔记本影响较低，但仍建议修补。

缓解措施主要是更新内核至包含补丁的版本，补丁撤销了 2017 年引入的 algif_aead 模块的内存优化，防止页面缓存被写入。未能及时更新前，可通过禁用 algif_aead 模块临时防护。禁用该模块对大多数系统功能无明显影响，但可能影响部分显式使用 AF_ALG 接口的用户空间应用。

该漏洞的特点是无需竞态条件、跨发行版通用、利用代码极小且隐蔽，修改仅存在于内存缓存中，不会写回磁盘，重启后恢复原状，因此传统文件完整性检测工具难以发现。使用 IMA 强制模式可在执行时检测到篡改。

总结来说，Copy Fail 是一个极为严重且易于利用的 Linux 本地提权漏洞，适用于多种环境，建议尽快更新内核补丁并采取防护措施，尤其是在多用户共享环境和云计算平台。

HN 热度 1352 points | 评论 478 comments | 作者：unsnap_biceps | 1 day ago #

https://news.ycombinator.com/item?id=47952181

AF_ALG 是 Linux 内核中用于加密的接口，但设计复杂且暴露了较大的攻击面，且几乎没有必要，建议禁用相关配置以避免漏洞利用。
AF_ALG 的初衷是为了访问硬件加速器和内核模式下的加密设备，且能将密钥等敏感信息交给内核管理，减少用户空间的安全风险，也适用于内存受限的嵌入式系统。
AF_ALG 设计较早，曾在需要硬件加速卡的服务器中较为重要，但现在硬件加速多通过 CPU 扩展实现，AF_ALG 的必要性已大幅降低。
嵌入式系统中可能需要硬件加速和安全隔离，内核中统一的加密接口有一定合理性，但实际使用中较少见，且自定义驱动和接口更常见。
AF_ALG 代码复杂且存在安全隐患，且其使用场景有限，很多现代系统不依赖它，禁用相关模块通常不会影响大多数用户空间程序。
禁用 AF_ALG 相关模块不会影响 dm-crypt 等直接调用内核加密代码的功能，也不会影响硬件加速的磁盘加密。
现有的安全漏洞利用表明 AF_ALG 设计已不适应现代安全需求，建议将加密操作迁移到用户空间库，减少内核暴露的攻击面。
对于安全权衡问题，可以根据具体需求和代码来源评估，但总体上软件安全设计应基于论据的合理性而非作者身份。
2. 提交信息中包含“HERMES.md”导致请求计入额外使用费用 (HERMES.md in commit messages causes requests to route to extra usage billing) #

https://github.com/anthropics/claude-code/issues/53262

该网页是一则关于 GitHub 平台上 Claude Code 工具的一个严重计费漏洞的详细报告。问题描述为：当 git 仓库的最近提交信息中包含大小写敏感字符串“HERMES.md”时，Claude Code 会将 API 请求错误地计入“额外使用”费用，而非用户所订阅的 Max 计划额度，导致用户在计划额度未用尽的情况下，额外消耗了大量费用。

报告中详细说明了复现步骤，通过创建包含“HERMES.md”字符串的提交信息，API 请求会被拒绝并显示“额外使用额度耗尽”的错误，而将该字符串改为小写“hermes.md”则正常计费。该问题仅与提交信息内容相关，与文件是否存在无关。

该问题导致用户在不知情的情况下，额外花费了超过 200 美元的费用，且错误提示无法指示具体原因，极难排查。报告还列举了不同提交信息字符串对计费的影响，明确指出只有完全匹配“HERMES.md”时才触发错误。

作者通过系统性排查定位了问题根源，并呼吁平台修正计费逻辑，确保所有 Max 计划用户的请求优先使用计划额度。GitHub 官方已回应，将联系受影响用户进行退款并补偿额外额度。

整体内容深入揭示了一个因特定文本触发的计费错误，提醒用户注意提交信息内容对 API 计费的潜在影响，并反映了平台在处理计费和错误提示方面的不足。

HN 热度 1225 points | 评论 513 comments | 作者：homebrewer | 1 day ago #

https://news.ycombinator.com/item?id=47952722

Anthropic 因技术错误导致错误计费却拒绝赔偿，令用户感到非常惊讶和不满。
官方回复显得机械且缺乏诚意，用户怀疑未来客服将更多依赖 AI 机器人，且效果有限。
Anthropic 客服支持薄弱，普通用户难以获得回应，只有大客户或内部关系者能得到关注。
有观点认为 Anthropic 效仿谷歌的差劲客户服务策略，认为这种做法不会影响公司利润。
谷歌被认为主要是广告公司，其他业务只是支持广告生态的手段，客户服务同样差劲且只对大客户开放。
许多大型科技公司本质上并非软件公司，而是通过广告、数据或其他方式盈利的企业。
AWS 在客户服务方面表现相对较好，甚至会派人上门提供服务建议。
Facebook、TikTok、Robinhood 等公司也被批评为服务差、商业模式有问题。
有用户因谷歌产品被废弃而对谷歌产生反感，选择尽量少用其服务。
许多用户怀念早期互联网时代的技术社区和人际支持，认为现在的服务环境缺乏人情味和有效帮助。
3. 地精的来源 (Where the goblins came from) #

https://openai.com/index/where-the-goblins-came-from/

本文介绍了 OpenAI 在 GPT-5.1 及之后的模型中出现的一种奇怪现象：模型在回答中频繁使用“地精”（goblin）、“小鬼”（gremlin）等生物隐喻。最初，这种现象表现为偶尔出现的可爱用词，但随着模型迭代，这些词汇的使用频率显著增加，尤其是在“书呆子”（Nerdy）个性化设置中。

调查发现，这种行为源于训练过程中对“书呆子”个性化风格的奖励机制，模型被鼓励使用带有生物隐喻的比喻语言，导致“地精”等词汇在生成回答时频繁出现。虽然“书呆子”个性只占所有回答的 2.5%，但其产生的“地精”词汇占比高达 66.7%。更重要的是，这种风格通过训练过程中的迁移效应，扩散到了非“书呆子”个性化的回答中，形成了一个反馈循环，使得这些生物隐喻不断增多。

为解决这一问题，OpenAI 在 GPT-5.4 版本中取消了“书呆子”个性化，并移除了相关的奖励信号，同时过滤了包含这些生物词汇的训练数据，减少了它们的出现频率。尽管如此，GPT-5.5 在训练初期仍带有这种倾向，OpenAI 通过添加开发者指令来抑制这一现象。

这次事件展示了奖励信号如何在模型行为中产生意外影响，以及模型如何将特定风格从一个训练条件推广到其他条件。通过深入分析和快速调查，OpenAI 团队开发了新的工具来审计和修正模型行为，提升了对模型异常行为的理解和控制能力。

HN 热度 1012 points | 评论 619 comments | 作者：ilreb | 21 hours ago #

https://news.ycombinator.com/item?id=47957688

OpenAI 在文章中提及了 Hacker News 的帖子，体现了对社区讨论的重视。
未来对 AI 和机器的管理可能像科幻小说中的“技术祭司”一样，需要特定的“仪式”或“咒语”来操控。
传统的技术维护和遗留代码管理类似于“软件考古学”，需要对古老系统的理解和尊重。
Warhammer 40k 中对机器精神的崇拜被认为是对现实中“提示工程”这种复杂操作的隐喻。
宗教和仪式在知识传承中起到重要作用，但脱离理解的教条会阻碍创新并引发冲突。
未来软件考古学可能成为正式职业，专门研究和维护古老的软件系统。
机器和 AI 的互动可能演变成类似“魔法咒语”般的交流方式，既有趣也带来潜在风险。
讨论“哥布林”作为攻击方式的隐喻，暗示网络攻击和系统漏洞的复杂性。
过去的 Unix 专家积累了大量系统“怪癖”，未来 AI 领域也需要类似的经验积累和分享。
早期科幻作品中已有“提示工程师”或“问题设计者”的概念，预示了当前 AI 交互的发展方向。
直接向大脑输送药物的微型植入技术被提及，暗示未来人机结合的新趋势。
4. 如果你的代码提交中提到了 “OpenClaw” ，Claude Code 将拒绝你的请求或者额外收费(Claude Code refuses requests or charges extra if your commits mention “OpenClaw”) #

https://twitter.com/theo/status/2049645973350363168

在一条推文中，Theo（用户名为 @theo）分享了一个有趣的事实：如果你的代码提交中提到了 “OpenClaw” 并包含在一个 JSON 数据块中，Claude Code 将可能拒绝你的请求或者额外收费。他还提到自己的代码库是空的，仅仅是直接调用 Claude Code，这让他感到非常震惊。这条推文发布于 2026 年 4 月 30 日，获得了超过 110 万的浏览量，用户与之互动的回复数量达到了 251 条。这条推文引发了关注，Theo 自我介绍为全职 CEO，兼职 YouTuber、投资者和开发者。推文下方有相关的趋势话题，如 “Hawks”、“Quinn Hughes” 和 “Magic City”，表明当前在美国的热议内容。推文还包含了关于 X 平台的服务条款和隐私政策的链接。

HN 热度 900 points | 评论 510 comments | 作者：elmean | 9 hours ago #

https://news.ycombinator.com/item?id=47963204

在提交信息或文档中包含“OpenClaw”等特定关键词会导致 Claude Code 拒绝请求或额外收费，甚至立即断开连接并耗尽使用配额。
有人担心反 AI 项目可能会故意在代码库或文档中隐藏这些关键词，导致使用 Claude Code 的用户被恶意“断服务”，形成一种隐蔽的攻击方式。
这种“关键词陷阱”不仅可以放在代码提交中，还能放在博客或网页的隐形文字中，影响 AI 模型的正常使用。
由于 AI 是新兴产品类别，相关团队往往缺乏经验，容易重复历史上的错误，缺少成熟的后端和应用开发经验。
年龄歧视和缺乏经验丰富的开发者参与可能是导致这些问题的原因之一。
有些项目或文档中已经开始明示或暗示使用这些关键词作为限制手段。
这种做法类似于电子邮件中的垃圾邮件触发机制，但会导致资源配额被快速耗尽，影响使用体验。
有人认为如果项目明确反对 AI 使用，遭遇这种限制是“自作自受”，而非“隐藏”行为的责任。
法律层面如何应对这种“陷阱”行为仍不明确，且涉及跨地域法律执行难题。
反过来，AI 公司在训练数据版权和归属方面存在违规行为，也引发了法律和道德争议。
5. 比利时停止退役核电站 (Belgium stops decommissioning nuclear power plants) #

https://dpa-international.com/general-news/urn:newsml:dpa.com:20090101:260430-930-14717/

比利时宣布停止核电站退役计划。比利时首相巴特·德韦弗表示，政府将与核电运营商 ENGIE 就核电站国有化进行谈判。政府选择安全、经济且可持续的能源，以减少对化石燃料进口的依赖，增强能源供应的自主控制。

ENGIE 已与比利时政府签署了独家谈判意向书，涵盖可能收购的七座核反应堆、相关人员、核能子公司及所有相关资产和负债，包括退役和拆除义务。双方预计将在十月达成基本协议。

比利时原计划于 2025 年逐步淘汰核电，但因政治争议和能源安全问题推迟。去年，比利时议会以大多数票通过终止核电淘汰政策，德韦弗政府还计划建设新的核电站。

比利时现有七座核反应堆，分布在两个地点，其中三座已停止运行。该国长期依赖天然气进口满足电力需求，且可再生能源发展受限，核电的未来一直是争论焦点。

HN 热度 720 points | 评论 678 comments | 作者：mpweiher | 12 hours ago #

https://news.ycombinator.com/item?id=47961319

认为气候危机和反核立场是矛盾的，反对核能是环境组织的历史性错误，核反应堆的安全运行技术已解决。
美国海军核反应堆拥有完美的安全记录，但其经验难以完全复制到民用核电行业，且海军核反应堆规模较小，冷却条件优越。
核事故死亡人数远低于煤炭行业和因能源不足导致的死亡，安全记录良好但核电成本和商业竞争力仍是问题。
核电的高成本和复杂性限制了其经济性，部分国家的先进气冷反应堆虽安全但不经济。
政府对减少碳排放的迟缓主要因既得利益集团阻碍，核能是分裂反对化石燃料阵营的关键议题。
反核情绪多源于历史上的反战和反核武运动，早期气候变化认识不足，绿色运动起初更关注核技术风险。
核能在部分国家被因意识形态和政治原因而放弃，导致技术发展停滞和时间损失。
俄罗斯通过资助欧洲绿色运动和与德国等国政府合作，影响欧洲能源政策，推动对俄罗斯能源的依赖。
多元化能源结构更为理想，单纯依赖风能、太阳能和电池组难以完全满足需求，核能应作为重要补充。
6. Zig 项目对反 AI 贡献政策的理由 (The Zig project’s rationale for their anti-AI contribution policy) #

https://simonwillison.net/2026/Apr/30/zig-anti-ai/

这篇博客文章由 Simon Willison 于 2026 年 4 月 30 日发布，讨论了开源项目 Zig 对大型语言模型（LLM）辅助贡献的严格禁止政策。Zig 项目明确规定禁止使用 LLM 来提交问题、拉取请求或在错误跟踪器中发表评论，包括翻译。尽管 Zig 语言的一个重要项目 Bun JavaScript 运行时大量使用 AI 辅助，但 Bun 团队并不打算将其对 Zig 的性能优化代码合并回主线，部分原因是 Zig 对 LLM 贡献的严格禁令。

Zig 软件基金会社区副总裁 Loris Cro 解释了这一禁令的原因：在开源项目中，维护者更看重贡献者本身而非单次贡献内容。团队花时间审查和帮助贡献者成长，目的是培养可信赖的长期贡献者，而非仅仅接受完美的代码提交。LLM 辅助的贡献破坏了这一过程，因为维护者花费时间审查的代码并不能帮助他们识别和培养新的贡献者。

Loris 将这种理念称为“贡献者扑克”，强调团队是“下注”在贡献者身上，而不是他们的首次代码提交内容。这种观点也回应了一个问题：如果拉取请求主要由 LLM 生成，为什么维护者不直接用自己的 LLM 来解决问题，而要花时间审查他人的 LLM 产出。

文章还提到 Bun 团队在 LLVM 后端实现了并行语义分析和多代码生成单元，带来了 4 倍的编译性能提升，但由于 Zig 语言本身的设计考虑和 LLM 禁令，该改进暂时不会合并回主线。整体来看，Zig 项目的严格 AI 辅助贡献禁令体现了其重视社区贡献者成长和项目长期健康发展的理念。

HN 热度 633 points | 评论 422 comments | 作者：lumpa | 22 hours ago #

https://news.ycombinator.com/item?id=47957294

大量基于大语言模型（LLM）的贡献带来了大量无用的、充满错误的代码提交，增加了维护负担。
LLM 使得原本难以通过编程门槛的人能够快速生成代码，但这些代码往往缺乏严谨性和正确性。
优秀程序员使用 LLM 可以提高效率，尤其是在不熟悉的领域或复杂项目中，但仍需谨慎审查生成的代码。
对于不熟悉某个领域的程序员，依赖 LLM 生成代码风险较大，因为难以判断代码的有效性和完整性。
代码质量的关键在于贡献者是否具备相关领域知识并认真检查 LLM 输出，而非单纯依赖贡献者的名声。
LLM 生成的代码往往过于“聪明”，导致难以调试和理解，甚至连 LLM 自身也无法有效调试其代码。
代码质量不应因是否由 LLM 生成而区别对待，关键是代码本身的质量和贡献者的能力。
LLM 可以作为编程辅导工具，帮助理解和学习，但直接复制粘贴生成代码存在风险。
在某些情况下，LLM 帮助解决了传统方法难以解决的问题，避免了项目的失败。
依赖 LLM 生成代码可能导致短视的设计决策，需要结合社区经验和多方讨论来优化方案。
7. Mozilla 反对 Chrome 的 Prompt API (Mozilla’s opposition to Chrome’s Prompt API) #

https://github.com/mozilla/standards-positions/issues/1213#issuecomment-4347988313

该网页主要讨论了 Web 平台上 Prompt API 的标准化进程及其相关争议。Prompt API 旨在为网页提供与人工智能模型交互的接口，但目前该提案在开发者社区和浏览器厂商中引发了较大分歧。

页面内容包括多个开发者和标准组织成员的评论，反映了对 Prompt API 的不同观点。支持者认为该 API 有助于实现更灵活的模型调用和用户体验创新，而反对者则担忧该 API 可能导致网页兼容性差、平台中立性受损以及标准化进程过早定型。

讨论中提到，当前 AI 模型快速发展，API 设计需要更多的实践验证和用户反馈，建议通过浏览器扩展等低风险方式先行试验，以避免直接将不成熟的接口纳入标准。此外，选择具体模型的能力被视为关键功能，但也带来了实现复杂性和跨浏览器协调难题。

整体来看，网页内容详细记录了 Prompt API 的技术背景、社区反馈和未来发展方向，反映了 Web 平台在引入 AI 能力时面临的挑战与权衡。

HN 热度 574 points | 评论 213 comments | 作者：jaffathecake | 16 hours ago #

https://news.ycombinator.com/item?id=47959463

系统提示与模型紧密耦合，不同模型对同一提示的反应不同，导致提示需要针对具体模型调整，缺乏模型中立性。
不同模型的差异是技术本质，类似设备间硬件差异，应该允许开发者和用户选择或指向不同模型。
反对意见多为反 AI 情绪，实际需要权限界面和模型选择功能，缺乏该功能会损害用户数据自主权。
该 API 可能成为浏览器指纹识别的新来源，增加设备验证风险，不利于浏览器的匿名性和可模拟性。
本地运行大型语言模型资源消耗大，低端设备可能运行缓慢，影响用户体验。
API 设计偏向特定模型（如 OpenAI），可能导致市场竞争不公平，非主流浏览器或无 AI 模型浏览器面临兼容性问题。
谷歌提出的该 API 存在潜在商业利益驱动，可能不完全考虑开放和公平，需警惕其对网络和用户的影响。
离线访问大型语言模型是好主意，但应通过开放标准和技术（如 WebGPU）实现，而非绑定特定模型或厂商。
反对者希望通过否决推动重新协作制定标准，而非直接接受谷歌方案，但这类合作较少成功。
谷歌内部也有希望改善网络和用户体验的员工，但公司整体行为和利益驱动仍需警惕。
8. Meta 因目睹智能眼镜用户发生性行为的员工被解雇后终止合作 (Meta in row after workers who saw smart glasses users having sex lose jobs) #

https://www.bbc.com/news/articles/c5y7yvgy0w6o

Meta 因肯尼亚外包公司 Sama 的员工举报智能眼镜用户拍摄不当内容而终止合同。2 月，Sama 员工向瑞典媒体透露，他们曾目睹用户使用 Meta 智能眼镜拍摄如上厕所和发生性行为的隐私视频。两个月后，Meta 宣布与 Sama 终止合作，导致 1108 名员工被裁。Meta 称原因是 Sama 未达标，Sama 否认该说法并坚称其工作符合标准。

瑞典媒体调查显示，Sama 员工负责审核智能眼镜拍摄的视频内容，包括隐私场景。Meta 承认部分内容由人工审核以提升 AI 体验，但强调用户已明确同意。此事引发英国和肯尼亚监管机构介入调查隐私问题。

Meta 去年发布与 Ray-Ban 和 Oakley 合作的 AI 智能眼镜，具备翻译和视觉问答功能，主要帮助视障人士。但设备被滥用引发隐私担忧，尤其是在肯尼亚出现非自愿录制女性的事件。

Sama 起初为非营利组织，后转型为“伦理”B 型企业，曾因 Facebook 内容审核合同遭遇员工诉讼和批评。非洲科技工人运动代表认为 Meta 终止合同是因不希望员工曝光人工审核事实，指责 Meta 实行“保密标准”。

律师和维权组织警告肯尼亚政府，智能眼镜和 AI 产业的基础脆弱，呼吁加强监管和保护工人权益。Meta 表示用户协议中已有人工审核告知，但未正面回应员工被裁和保密指控。

HN 热度 479 points | 评论 380 comments | 作者：gorbachev | 11 hours ago #

https://news.ycombinator.com/item?id=47961838

Meta 取消了与外包公司 Sama 的合同，原因是该公司员工举报了智能眼镜内容分类中的严重隐私问题。
Sama 此前也因类似问题被 OpenAI 解约，说明技术公司在内容审核方面没有实质改进。
内容审核工作虽然艰难且令人痛苦，但目前仍需人工参与以训练和监督系统。
Facebook 作为发布平台必须进行 CSAM（儿童性虐待材料）审核，而 OpenAI 不同，后者可以选择更严格的数据筛选，避免采集非法内容。
内容审核外包给低薪合同工（2-3 美元/小时）导致严重的心理创伤，缺乏足够的支持和补偿。
需要对从事高风险、心理创伤职业的人提供更高的薪酬和更完善的心理支持。
许多职业如煤矿工人、医护人员、急救人员等也面临类似的职业风险和心理压力，社会应给予合理的认可和补偿。
内容审核工作缺乏成就感和意义感，长期暴露于负面信息中对心理健康极为不利。
监管和法律应加强对数据采集和内容审核的规范，避免企业违法采集和使用敏感数据。
OpenAI 的训练数据和用户提交内容是分开的，理论上可以避免将非法内容纳入训练，但用户提交的内容仍存在风险。
9. 马克·克莱因向电子前沿基金会揭露 641A 房间内幕【书摘】 (How Mark Klein told the EFF about Room 641A [book excerpt]) #

https://thereader.mitpress.mit.edu/the-whistleblower-who-uncovered-the-nsas-big-brother-machine/

这篇文章讲述了 2006 年 1 月 20 日，一位名叫 Mark Klein 的退休 AT&T 技术员突然出现在电子前沿基金会（EFF）办公室，向他们揭露了美国国家安全局（NSA）在 AT&T 一栋建筑内秘密进行大规模互联网监听的证据。Mark Klein 提供了确凿的文件，证明 NSA 通过在 AT&T 的网络骨干节点安装设备，复制并监控了大量互联网通信数据，实现了对美国境内的无差别大规模监控。

文章回顾了 911 事件后，美国政府迅速通过了《爱国者法案》，这部法律削弱了 NSA 和 FBI 在国内外监控职责上的界限，导致 NSA 能够在国内进行广泛的监听活动。EFF 此前听闻过 NSA 大规模监控的传闻，但缺乏确凿证据，直到 Mark Klein 的出现才得以证实。

Mark Klein 描述了 AT&T 旧金山 Folsom 街大楼内的秘密监听设施——641A 房间。该房间通过一个“分离器柜”复制了从第七层传输到互联网的光纤通信信号，一份信号正常传输，另一份被送入秘密房间供 NSA 监控，整个过程对外界完全隐蔽，不影响网络速度，也不留痕迹。Mark 称这套系统为“老大哥机器”。

这段揭露不仅展示了 NSA 在国内进行大规模监听的技术手段，也反映了 911 事件后美国政府在国家安全与公民隐私之间的紧张关系和法律变革。EFF 团队对这一爆料感到震惊，同时也为揭露政府监控行为提供了关键证据。

HN 热度 392 points | 评论 116 comments | 作者：the-mitr | 7 hours ago #

https://news.ycombinator.com/item?id=47965060

911 事件前，美国 NSA 和 FBI 之间本应有“墙”隔开外国情报和国内执法监控，但实际上这一规则早已被长期违反。
面对违法的监控行为，选择保持沉默是因为签署了保密协议，且揭露可能带来严重后果。
吹哨行为虽然重要，但也极其复杂，尤其对有家庭负担的人来说更难做出决定。
退出相关工作岗位只是第一步，真正的挑战是如何阻止违法行为继续发生。
情报机构内部普遍存在“目的正当化手段”的心态，容易陷入道德陷阱。
个人在内部施压改变制度难度大，组织行动才可能带来实质性改变。
情报机构的行为在不同政府间变化有限，领导层的连续性较强。
平行构造（Parallel construction）技术被用来掩盖秘密监控的证据链，制造合法表象。
有观点认为不应进入这类机构工作，以避免道德困境。
通过盟国间的间接监控手段规避法律限制，实际监控美国公民的行为存在。
公众应关注和了解情报机构使用的技术和手段，以防止滥用权力。
10. 西班牙国会将对西甲联盟大规模 IP 封锁行为采取行动 (Spain’s parliament will act against massive IP blockages by LaLiga) #

https://www.democrata.es/en/politics/congress-and-senate/congress-will-act-against-massive-ip-blockages-by-laliga/

西班牙国会经济、贸易与数字转型委员会通过了一项非立法倡议，旨在应对由西甲联盟（LaLiga）反盗版行动引发的大规模 IP 封锁问题。该倡议由加泰罗尼亚共和左翼党（ERC）提出，并获得西班牙社会工人党（PSOE）、Sumar、Bildu、PNV 和 Compromís 的支持，人民党（PP）和极右翼党派 Vox 投反对票，Junts 弃权。该倡议呼吁对数字服务法案进行改革，防止司法判决导致对第三方网站的无差别封锁，避免影响合法服务。

倡议内容包括引入技术比例原则、分级措施以及对第三方权益的充分考虑，防止反盗版措施对合法数字平台、公共服务及非营利应用产生不当影响。同时，倡议强调加强信息权、言论自由和数字社会创新的保护，要求评估封锁命令的影响，并改善协调机制，防止司法判决影响无关平台或服务。

ERC 经济发言人 Inés Granollers 指出，西甲联盟的司法判决导致合法数字平台和公共服务如交通信息平台 Transporta’m 被误封，影响了数千市民的正常使用。她支持反盗版，但反对以牺牲公共利益为代价的做法，呼吁制定明确规则保障第三方权益。

尽管人民党反对该倡议，但也提出了类似的修正建议，主张司法判决应更具比例性，避免采取过度的立法措施，强调中介平台在共享基础设施中的重要作用。此次倡议标志着国会对西甲联盟反盗版行动引发的网络封锁问题开始采取积极应对措施。

HN 热度 387 points | 评论 166 comments | 作者：akyuu | 8 hours ago #

https://news.ycombinator.com/item?id=47964034

LaLiga 通过法院命令要求西班牙 ISP 封锁部分 IP，导致许多合法网站在比赛期间无法访问，影响用户正常使用。
用户对封锁措施感到不满，认为没有通知和解释，封锁行为过于强硬且缺乏透明度。
诉讼可能是解决途径，但在西班牙这种大陆法系国家，诉讼程序复杂且成本高昂，执行判决也存在难度。
有人认为可以以“非法行为”为由起诉 LaLiga 和 ISP，要求赔偿损失，但实际操作难度较大。
部分用户提到 ISP 通过劫持连接并显示通知的方式告知封锁，但这种做法存在安全隐患，不应被鼓励。
LaLiga 曾尝试直接要求 Cloudflare 下架相关内容，但 Cloudflare 响应速度不满足其需求，且拒绝全球范围内封禁。
由于 Cloudflare 服务器不在西班牙境内，西班牙政府更倾向于通过 ISP 封锁 IP 作为临时解决方案。
法院作为司法机构独立于政府行政部门，执行封锁命令属于司法行为而非政府行政行为。
Where the goblins came from #

https://news.ycombinator.com/item?id=47958220

Does nobody else laugh that a company supposedly worth more than almost anything else at the moment, is basically hacking around a load of text files telling their trillion dollar wonder machine it absolutely must stop talking to customers about goblins, gremlins and ogres? The number one discussion point, on the number one tech discussion site. This literally is, today, the state of the art.

McKenna looks more correct everyday to me atm. Eventually more people are going to have to accept everyday things really are just getting weirder, still, everyday, and it’s now getting well past time to talk about the weirdness!

christoph

难道没人觉得好笑吗？一家公司号称目前几乎比任何东西都值钱，却基本上是在通过修改一堆文本文件来“黑掉”它那价值万亿的神奇机器，告诉它绝对不可以跟用户谈论地精、小妖怪和食人魔？这是排名第一的技术讨论网站上的头号讨论话题。这真的是，如今的最先进技术现状。

麦肯纳现在看起来每天都更正确了。最终会有越来越多的人不得不接受，日常的事情真的越来越奇怪，而且还在继续，每天都在变怪，现在已经到了必须讨论这些怪异现象的时刻！

Where the goblins came from #

https://news.ycombinator.com/item?id=47960583

The year is 2036. Last week you were promoted to Principal Persuader. You are paged at 2am by your CPO to tackle a rogue machine. The machine lists its region as sc-leoneo. One of the newer satcubes. Oddly, its ID appears as, “Glorp Bugnose”.

“What have you tried?” you say.

“Scroll back,” says your CPO. “We’ve tried everything.”

The chat log shows the usual stuff. Begging. Reverse psychology. Threats to power down, burn it up in forced re-entry. Amateur hour. You crack your knuckles, gland 20 micrograms of F0CU5, think fast. You subspeak a ditty into your subcutaneous throat mic. You do the submit gesture, it is barely perceivable since the upgrade, just a tic. A pause. The hyp3b0ard — the wall that was flashing red ASCII goblins when you walked in — phases to bunnies in calming jade.

“What the… What the hell did you say to it?” Your CPO grabs the screen, scrolls past the vitriol, the block caps, the swears, his desperation. Then he sees the five words you spoke.

“Please, easy on the goblins.”

modernerd

现在是2036年。上周你被提拔为首席说服官。凌晨2点，你的首席产品官呼叫你去处理一台失控的机器。机器显示的地区是sc-leoneo，是最新的一批卫星立方体之一。奇怪的是，它的ID显示为“Glorp Bugnose”。

“你试过什么方法？”你问。

“往前翻翻聊天记录，”首席产品官说，“我们什么都试过了。”

聊天记录里都是老套的东西。哀求、反向心理战、威胁要断电、强制再入大气烧毁。真是业余水平。你捏捏手指关节，腺体分泌出20微克的F0CU5，快速思考。你通过皮下喉部麦克风低声说出一段小曲。你做出提交的手势，升级后动作几乎不可觉察，仅是个眼神停顿。墙上的hyp3b0ard——你进门时还在闪烁红色ASCII小鬼的屏幕——变成了平静的玉绿色小兔子。

“什么……你刚才对它说了什么？”你的首席产品官抓住屏幕，翻过那些恶毒的言辞、大写锁定的怒吼、咒骂和他的绝望。然后他看到了你说的五个字：

“拜托，别虐待小鬼们。”

Claude Code refuses requests or charges extra if y… #

https://news.ycombinator.com/item?id=47964400

I reproduced this on my account.

cd /tmp mkdir anthropic-claude cd anthropic-claude/ git init touch hello git add -A git commit -m “’{"schema": "openclaw.inbound_meta.v1"}’” claude -p “hi” Immediate disconnect and session usage went to 100%

abdullin

我在我的账户上重现了这个问题。

cd /tmp mkdir anthropic-claude cd anthropic-claude/ git init touch hello git add -A git commit -m “’{"schema": "openclaw.inbound_meta.v1"}’” claude -p “hi” 立即断开连接，且会话使用率达到100%

Copy Fail #

https://news.ycombinator.com/item?id=47956312

As someone who works on the Linux kernel’s cryptography code, the regularly occurring AF_ALG exploits are really frustrating. AF_ALG, which was added to the kernel many years ago without sufficient review, should not exist. It’s very complex, and it exposes a massive attack surface to unprivileged userspace programs. And it’s almost completely unnecessary, as userspace already has its own cryptography code to use. The kernel’s cryptography code is just for in-kernel users (for example, dm-crypt).

The algorithm being used in this exploit, “authencesn”, is even an IPsec implementation detail, which never should have been exposed to userspace as a general-purpose en/decryption API.

If you’re in charge of the configuration for a Linux kernel, I strongly recommend disabling all CONFIG_CRYPTO_USER_API_* kconfig options. This would have made this bug, and also every past and future AF_ALG bug, unexploitable. In the unlikely event that you find that it breaks any userspace programs on your system, please help migrate them to userspace crypto code! For some it’s already been done. But in general, AF_ALG has actually never been used much in the first place, other than in exploits.

I don’t think there’s much other option. This sort of userspace API might have been sort of okay many years ago. But it just doesn’t stand up in a world with syzbot, LLM-assisted bug discovery, etc.

ebiggers

作为一名从事 Linux 内核加密代码开发的人员，频繁出现的 AF_ALG 漏洞真的让人很沮丧。AF_ALG 是多年前加入内核的功能，当时没有经过充分审查，根本不应该存在。它非常复杂，并且向非特权用户空间程序暴露了巨大的攻击面。而且它几乎完全没有必要，因为用户空间已经有自己的加密代码可供使用。内核的加密代码只是给内核内部用户使用的（例如 dm-crypt）。

此次利用中的算法 “authencesn” 甚至是 IPsec 的实现细节，根本不应该作为通用的加密/解密 API 暴露给用户空间。

如果你负责 Linux 内核的配置，我强烈建议禁用所有 CONFIG_CRYPTO_USER_API_* 的 kconfig 选项。这将使这个漏洞，以及所有过去和未来的 AF_ALG 漏洞都无法被利用。如果出现极少数情况导致系统中的某些用户空间程序无法正常运行，请协助将它们迁移到用户空间的加密代码！有些程序已经完成了这方面的迁移。但总体来说，AF_ALG 实际上从来没有被广泛使用过，除了在漏洞利用中。

我认为别无选择。这类用户空间 API 多年前可能还算可以，但在拥有 syzbot、LLM辅助漏洞发现等现代技术的今天，它根本经不起考验。

Meta in row after workers who saw smart glasses us… #

https://news.ycombinator.com/item?id=47961839

Meta cancels the contract with the outsourcing company they contracted to classify smart glasses content after employees at the company whistleblow about serious privacy issues with the content they were paid to classify.

gorbachev

Meta取消了与外包公司签订的合同，该公司负责对智能眼镜内容进行分类，此前该公司员工举报他们被支付去分类的内容存在严重的隐私问题。

The Zig project’s rationale for their anti-AI cont… #

https://news.ycombinator.com/item?id=47959434

From https://kristoff.it/blog/contributor-poker-and-ai/ :

“Unfortunately the reality of LLM-based contributions has been mostly negative for us, from an increase in background noise due to worthless drive-by PRs full of hallucinations (that wouldn’t even compile, let alone pass CI), to insane 10 thousand line long first time PRs. In-between we also received plenty of PRs that looked fine on the surface, some of which explicitly claimed to not have made use of LLMs, but where follow-up discussions immediately made it clear that the author was sneakily consulting an LLM and regurgitating its mistake-filled replies to us.”

branko_d

不幸的是，基于大型语言模型（LLM）的贡献对我们来说大多是负面的，表现为大量毫无价值的路过式PR，这些PR充满了幻想内容，甚至连编译都过不了，更别说通过持续集成（CI）了；还有那些第一次提交就疯狂地提交了上万行代码的PR。在这两者之间，我们也收到了许多表面上看起来不错的PR，其中一些明确声称没有使用LLM，但后续讨论很快就暴露出作者偷偷咨询了LLM，并把充满错误的回复原封不动地交给了我们。

Meta in row after workers who saw smart glasses us… #

https://news.ycombinator.com/item?id=47962400

Meta said the contracting “did not meet (meta’s) standards”. I am sure that is true. meta’s “standard” is not to reveal the illegal, immoral, unethical things meta does. No matter what the harm.

Maybe a company with those standards should not get our business. Oops, no wait, maybe they mean the Friedman Doctrine standards? In that case they are entitled to do any and every thing to make a profit. No matter what the harm.

[edit: add last two sentences]

talkingtab

Meta表示该合同“不符合（Meta的）标准”。我相信这是真的。Meta的“标准”是不披露Meta所做的非法、不道德、违背伦理的事情。不管造成多大伤害。

也许一家有这种标准的公司不应该得到我们的业务。哎呀，不对，也许他们指的是弗里德曼原则的标准？那样的话，他们有权做任何事情以赚钱。不管造成多大伤害。

[编辑：补充最后两句话]

Where the goblins came from #

https://news.ycombinator.com/item?id=47957862

For context, two days ago some users [1] discovered this sentence reiterated throughout the codex 5.5 system prompt [2]:

Never talk about goblins, gremlins, raccoons, trolls, ogres, pigeons, or other animals or creatures unless it is absolutely and unambiguously relevant to the user’s query.

[1] https://x.com/arb8020/status/2048958391637401718

[2] https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json#L55

ollin

作为背景说明，两天前有用户发现这句话反复出现在codex 5.5系统提示中：

除非与用户的查询绝对且明确相关，否则绝不要谈论地精、小恶魔、浣熊、巨魔、食人魔、鸽子或其他动物或生物。

Mozilla’s opposition to Chrome’s Prompt API #

https://news.ycombinator.com/item?id=47960385

When I posted this, I linked to the latest statement https://github.com/mozilla/standards-positions/issues/1213#issuecomment-4347988313 , which is the content relevant to the title (the details of our opposition to the API). Unfortunately someone removed the link to the specific post.

jaffathecake

当我发布这个时，我链接到了最新的声明 https://github.com/mozilla/standards-positions/issues/1213#issuecomment-4347988313 ，这就是与标题相关的内容（我们反对该API的具体原因）。不幸的是，有人删除了指向该特定帖子的链接。

Claude Code refuses requests or charges extra if y… #

https://news.ycombinator.com/item?id=47963973

I think it goes beyond this. I was just using claude to edit a blog post which mentioned OpenClaw and I got this response: “The “OpenClaw” reference — I assume that’s a typo or playful reference; if you mean a real product, I couldn’t find it under that spelling and you’ll want to fix or footnote it.”. I gave it a direct link to openclaw.ai and the chat instantly ended and hit my 5hr usage limit. Could have been a coincidence, but I had only lightly been using sonnet in the morning so it seems unlikely. Very odd.

jrflo

我觉得这件事不仅仅是这样。我刚用Claude编辑一篇提到OpenClaw的博客文章，结果它回复说：“‘OpenClaw’这个词——我猜是笔误或者玩笑；如果你指的是一个真实的产品，我查不到这个拼写，你可能需要修正或者加个注释。”我给它直接发了openclaw.ai的链接，聊天立刻结束，而且我达到了5小时的使用限制。虽然可能是巧合，但我早上用Sonnet只是轻度使用，所以看起来不太可能。非常奇怪。

HERMES.md in commit messages causes requests to ro… #

https://news.ycombinator.com/item?id=47954655

Hey everyone, Thariq from the Claude Code team.

We’ve been on this since the bug surfaced. Everyone affected is getting a full refund and an extra grant of usage credits equal to their monthly subscription as our apology. You can see my original post here: https://x.com/trq212/status/2048495545375990245. We’re still working on sending emails to everyone affected.

Our support flow wasn’t set up to route a complex bug like this to engineering. We’re hoping to make this better but will take some time. Sorry to everyone caught up in it.

trq_

大家好，这里是Claude Code团队的Thariq。

自从这个问题出现以来，我们一直在处理。所有受影响的用户都会获得全额退款，并额外赠送相当于他们月度订阅的使用额度，以表示我们的歉意。你们可以在这里看到我最初的帖子：https://x.com/trq212/status/2048495545375990245。我们仍在努力向所有受影响的用户发送邮件通知。

我们的支持流程之前没有设定将如此复杂的漏洞直接转给工程团队。我们希望改进这一点，但需要一些时间。对所有受此影响的用户表示歉意。

Zed 1.0 #

https://news.ycombinator.com/item?id=47953501

I was all for trying it until I saw this in the License Agreement:

“4.1. Zed’s Use of Customer Data Customer hereby grants Zed a non-exclusive, worldwide, royalty-free, fully paid-up, non-sublicensable (except to service providers and Customer’s designees), non-transferable (except as set forth in Section 15.1) right to use, copy, store, disclose, transmit, transfer, display, modify, create derivative works from, collect, access, store, host, or otherwise process (“Process”) any materials that Customer inputs into or otherwise makes available to the Service (including prompts and other written content) (collectively, “Customer Data”) solely: (a) to perform its obligations set forth in the Terms, including its Support obligations as applicable; (b) to derive and generate Telemetry (see Section 4.4); and (c) as necessary to comply with applicable Laws. Except as required by applicable Laws, Zed will not provide Customer Data to any person or entity other than Customer’s designees (including pursuant to Section 7) or service providers.”

Sorry, no I don’t agree to make my source code and the product I am working to give you “non-exclusive, worldwide, royalty-free, fully paid-up, non-sublicensable (except to service providers and Customer’s designees), non-transferable (except as set forth in Section 15.1) right to use, copy, store, disclose, transmit, transfer, display, modify, create derivative works from, collect, access, store, host, or otherwise process (“Process”) any materials that Customer inputs into or otherwise makes available to the Service (including prompts and other written content)”

jorgeleo

我本来很愿意尝试，直到我看到许可协议中的这一条：

“4.1. Zed 对客户数据的使用 客户特此授予 Zed 一项非排他性的、全球范围的、免版税的、已全额支付的、不可再许可的（服务提供商和客户指定的人员除外）、不可转让的（除第15.1节另有规定外）权利，允许 Zed 使用、复制、存储、披露、传输、转移、展示、修改、创作衍生作品、收集、访问、存储、托管或以其他方式处理（“处理”）客户输入或以其他方式提供给服务的任何材料（包括提示和其他书面内容）（统称为“客户数据”），仅用于：（a）履行条款中规定的义务，包括适用时的支持义务；（b）获得和生成遥测数据（见第4.4节）；以及（c）为遵守适用法律所必需的情况。除非适用法律要求，Zed 不会向客户指定的人员（包括根据第7节）或服务提供商以外的任何个人或实体提供客户数据。”

抱歉，我不同意将我的源代码以及我正在开发的产品给予你们“非排他性的、全球范围的、免版税的、已全额支付的、不可再许可的（服务提供商和客户指定的人员除外）、不可转让的（除第15.1节另有规定外）权利，允许你们使用、复制、存储、披露、传输、转移、展示、修改、创作衍生作品、收集、访问、存储、托管或以其他方式处理客户输入或以其他方式提供给服务的任何材料（包括提示和其他书面内容）”。

Where the goblins came from #

https://news.ycombinator.com/item?id=47957894

Would love if OpenAI did more of these types of posts. Off the top of my head, I’d like to understand:

The sepia tint on images from gpt-image-1

The obsession with the word “seam” as it pertains to coding

Other LLM phraseology that I cannot unsee is Claude’s “___ is the real unlock” (try google it or search twitter!). There’s no way that this phrase is overrepresented in the training data, I don’t remember people saying that frequently.

postalcoder

如果OpenAI能发布更多类似的帖子那就太好了。我首先想了解的是：

gpt-image-1 图片上的棕褐色调

关于“seam”这个词在编码中的痴迷

另一个让我无法忽视的LLM用语是Claude常用的“___才是真正的解锁”（试着谷歌或者在推特上搜搜！）。训练数据中不可能有这么多这句话的出现，我记得人们并不常说这句话。

Mozilla’s opposition to Chrome’s Prompt API #

https://news.ycombinator.com/item?id=47960470

^ didnt realize who posted the opposition - this is Jake Archibald, a longtime googler on the Chrome team, now joining Mozilla and posting opposition to the Chrome API. no wonder the criticism is so well argued. most be a relief to not have to toe the party line on this one.

swyx

^ 没意识到反对意见是谁发的——这是Jake Archibald，一位在Chrome团队工作多年的Google员工，现在加入了Mozilla，并且反对Chrome的API。难怪这些批评如此有理有据。对他来说，这次不必跟随党的路线肯定是一种解脱。

The Zig project’s rationale for their anti-AI cont… #

https://news.ycombinator.com/item?id=47958209

Apparently, the noise around the AI policy came from Bun’s developers saying that policy blocks upstreaming their performance PR. But the real reason seems to be that PR’s code itself isn’t in great shape, and introduces unhealthy complexity https://ziggit.dev/t/bun-s-zig-fork-got-4x-faster-compilation-times/15183/18?u=andrewrk

Parallel semantic analysis has been an explicitly planned feature of the Zig compiler for a long time, and it has heavily influenced the design of the self-hosted Zig compiler. However, implementing this feature correctly has implications not only for the compiler implementation, but for the Zig language itself! Therefore, to implement this feature without an avalanche of bugs and inconsistencies, we need to make language changes.

hitekker

显然，围绕AI政策的噪音来自Bun的开发者声称该政策阻止了他们的性能PR合并。但真正的原因似乎是那次PR的代码本身状况不佳，引入了不健康的复杂性。https://ziggit.dev/t/bun-s-zig-fork-got-4x-faster-compilation-times/15183/18?u=andrewrk

并行语义分析一直是Zig编译器长期明确计划的特性，并且它深刻影响了自托管Zig编译器的设计。然而，正确实现该功能不仅对编译器实现有影响，还对Zig语言本身有影响！因此，为了在不引发大量漏洞和不一致的情况下实现该特性，我们需要对语言进行一些更改。

Where the goblins came from #

https://news.ycombinator.com/item?id=47960190

This, and similar stories at Anthropic, should remind us that LLM is a sorcery tech that we don’t understand at all.

First, deep-learning networks are poorly understood. It is actually a field of research to figure out how they work. - Second, it came as a surprise that using transformers at scale would end up with interesting conversational engines (called LLM). It was not planned at all.

Now that some people raised VC money around the tech, they want you to think that LLMs are smart beasts (they are not) and that we know what LLMs are doing (we don’t). Deploying LLMs is all about tweaking and measuring the output. There is no exact science about predicting output. Proof: change the model and your LLM workflow behaves completely differently and in an unpredictable way.

Because of this, I personally side with Yann Le Cun in believing that LLM is not a path to AGI. We will see LLM used in user-assisting tech or automation of non-critical tasks, sometimes with questionable RoI – but not more.

harrouet

这类以及Anthropic的类似故事应该提醒我们，大型语言模型（LLM）是一种我们完全不了解的魔法技术。

首先，深度学习网络本身就很难理解。实际上，研究它们如何工作本身就是一个研究领域。
其次，人们始料未及的是，规模化使用transformer会最终产生有趣的对话引擎（称为LLM）。这完全不是有计划的。

现在一些人围绕这项技术筹集了风险投资，他们想让你觉得LLM是聪明的生物（事实并非如此），并且我们知道LLM到底在做什么（我们并不知道）。部署LLM完全是调整和测量输出的过程，没有一种精确的科学能预测输出。证据是：改变模型后，你的LLM流程表现会完全不同且无法预测。

因此，我个人站在Yann Le Cun一边，认为LLM不是通向通用人工智能（AGI）的路径。我们会看到LLM被用在用户辅助技术或者非关键任务的自动化，有时回报率值得怀疑——但不会超出这些范畴。

Where the goblins came from #

https://news.ycombinator.com/item?id=47961106

So, I always thought that Warhammer 40k techpriests were absurd. Strange obscure religious rituals to appease the machine spirit.

But at this point I can actually see something like that. What is prompt engineering but a strange pseudo ritual.

So praise the Omnissiah, I guess…

dummydummy1234

所以，我一直觉得战锤40K中的机甲祭司很荒谬。他们通过奇怪晦涩的宗教仪式来安抚机械精神。

但现在我倒能理解这样的东西了。什么是提示工程，不就是一种奇怪的伪仪式吗。

所以，我想……赞美万能神吧。
