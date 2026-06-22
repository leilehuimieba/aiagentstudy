# 2026-05-05 Hacker News Top Stories #

- BestBlogs URL: https://www.bestblogs.dev/en/article/12c375c5
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 30158
- Original publisher URL: https://supertechfans.com/cn/post/2026-05-05-HackerNews/

---

作者在健身房主动与35位陌生人交谈，一个月记录显示真诚与勇气能带来真实连接，适度且不功利的赞美与关心有效但过度会适得其反。
deepclaude 将 Claude Code 代理无缝切换到 DeepSeek 等更低价后端以显著降本并保留多工具循环能力，但受限于图像/并行支持且需权衡不同供应商的数据训练政策与隐私风险。
GameStop 提出以555亿美元收购 eBay 的激进要约引发对协同与融资可行性的质疑，市场分化反应且其盈利质量与长期增长模式被认为依赖利息和削减成本难以为继。
Spirit 航空停运后有人发起“Spirit 2.0”合作社众筹收购倡议以实现员工与社区所有、透明治理和低票价，但讨论指出航空业利润多靠信用卡与忠诚计划而非飞行本身。
欧盟自2027年起要求手机配备可用常规工具更换的电池并至少供货5年，虽或影响机身与防水但可通过设计化解，且对容量保持率达阈值者与特定设备有豁免。
伦敦现疑似班克斯新雕像：一名被国旗蒙眼的西装男正走向悬崖边，讽喻对民族主义的盲目追随与自毁。
BYOMesh 宣称在网状回传上带宽提升百倍并结合亚GHz与2.4GHz LoRa，但实际增益受法规合规、占空比与距离权衡所限，更适合低带宽遥测与消息场景。
作者警示智能代理编程虽提效却易引入复杂性、锁定与技能退化，应以理解与简洁为先、谨慎而有边界地使用而非盲目依赖。
GitHub 多项服务短暂异常后已恢复，社区将成因指向代理编程带来的使用激增与基础设施压力，并预测可能的限额/价格调整与部分用户转向自建。
1. 在健身房与陌生人交谈 (Talking to strangers at the gym) #

https://thienantran.com/talking-to-35-strangers-at-the-gym/

这篇文章讲述了作者 Thienan Tran 为了克服孤独感，尝试在健身房与陌生人交朋友的经历。作者毕业后虽然找到工作，但缺乏朋友，尝试通过健身这一常去的场所来社交。尽管担心打扰别人或陷入尴尬，作者决定每天主动与一位健身房常见的人搭话，起初使用固定的开场白“你在这里很常见，你力量很大，你的训练计划是什么？”，后来根据对方特点调整话题。

文章详细记录了作者一个月内与不同人的交流情况，包括对方的身份描述、对话时长、交流内容以及后续关系发展。例如，有的人成为偶尔打招呼的朋友，有的则因为搬走或不常见面而断了联系。作者还分享了自己因害怕社交而产生的行为，如不敢唤醒室友、假装不认识熟人等，表达了主动社交的困难与勇气。

整体来看，文章通过真实的社交实验，展示了孤独感的挑战和建立人际关系的努力，强调了主动迈出第一步的重要性，以及社交过程中可能遇到的各种反应和结果。

HN 热度 1083 points | 评论 515 comments | 作者：thitran | 13 hours ago #

https://news.ycombinator.com/item?id=48007438

真诚地赞美别人而不带任何目的，可以带来纯粹的快乐和满足感。
《人性的优点》这本书并非教人操控他人，而是强调真诚、善意和对他人兴趣的重要性。
人们能感受到你是否真心关心他们，真诚的关心会带来积极的互动和结果。
有些人误用书中的技巧进行操控或销售，导致别人对这些行为产生警惕和反感。
适度使用对方名字和赞美可以增进关系，但过度或刻意使用会让人感到不适。
书中部分内容因时代变迁显得过时，尤其是关于家庭和性别角色的章节。
记住并使用别人的名字能显著改善人际关系，即使对有注意力障碍的人也有效。
介绍名字的时机很重要，稍晚介绍名字并结合其他信息更容易让人记住。
2. DeepClaude——结合 DeepSeek V4 Pro 的 Claude 代码代理循环 (DeepClaude – Claude Code agent loop with DeepSeek V4 Pro) #

https://github.com/aattaran/deepclaude

该网页介绍了一个名为“deepclaude”的工具，它将 Claude Code 的自主编码代理与 DeepSeek V4 Pro、OpenRouter 或任何兼容 Anthropic 的后端结合使用，实现了相同的用户体验，但成本降低了 17 倍。Claude Code 是一个强大的自主编码代理，但费用较高（每月 200 美元且有使用上限），而 DeepSeek V4 Pro 在 LiveCodeBench 测试中得分 96.4%，输出令牌成本仅 0.87 美元/百万。

deepclaude 通过替换 API 调用的模型实现成本优化，保持了文件读取、编辑、bash 执行、多步骤自主编码循环等功能不变。用户只需获取 DeepSeek API 密钥，设置环境变量，安装脚本即可快速使用。该工具支持多种后端，包括 DeepSeek（默认）、OpenRouter、Fireworks AI 和 Anthropic，用户可根据需求切换后端。

DeepSeek 后端具有自动上下文缓存功能，大幅降低重复请求的成本。成本对比显示，使用 deepclaude 相比原 Anthropic 方案可节省 60%-90% 的费用。功能方面，deepclaude 支持文件操作、命令执行、搜索、多步骤工具循环、子代理生成及 Git 操作等，但在图像输入、并行工具使用和某些服务器工具支持上存在限制。

此外，deepclaude 支持在会话中实时切换后端，无需重启，方便用户根据任务复杂度选择最合适的模型。整体而言，deepclaude 为开发者提供了一个高效、低成本且功能丰富的自主编码解决方案。

HN 热度 650 points | 评论 273 comments | 作者：alattaran | 1 day ago #

https://news.ycombinator.com/item?id=48002136

DeepSeek 的 API 目前不支持用户选择不用于训练数据，使用时需注意数据隐私问题。
OpenRouter 提供了账户级或请求级的数据不训练选项（ZDR），但使用 DeepSeek V4 时开启该选项会导致模型不可用。
其他推理服务如 HuggingFace、Together AI、DeepInfra 等可能支持不训练数据，但需自行确认其政策。
DeepSeek 目前是开放模型，但因训练政策限制，部分平台会标注警告，影响使用体验。
选择支持不训练数据的提供商可能导致暂时无法使用某些模型，需等待更多供应商支持。
美国的数据保护法律主要保护美国公民的数据，外国用户的数据保护较弱，且相关公司不一定会披露数据收集情况。
Anthropic、OpenAI 和 Google 等大厂通常提供数据训练的选择权，用户可以选择不被用于训练。
美国媒体和政府对中国的报道带有较强的政治色彩，部分美国人对外国人的权益关注度较低。
中美关系复杂，存在经济补贴、产业竞争和地缘政治等多方面矛盾，双方都存在问题。
美国在国际事务中有过多次干涉和争议行为，但这并不意味着中国没有问题。
中国模式注重经济发展和扶贫，部分发展中国家民众愿意以牺牲部分个人自由换取经济稳定和生活改善。
不同国家和文化背景下对治理模式的偏好不同，不能简单以单一价值观评判优劣。
3. GameStop 提出 555 亿美元收购 eBay 的要约 (GameStop makes $55.5B takeover offer for eBay) #

https://www.bbc.co.uk/news/articles/cn0p8yled1do

游戏零售商 GameStop 提出了 55.5 亿美元的现金和股票收购要约，拟收购电商巨头 eBay，报价为每股 125 美元，比上周五 eBay 的收盘价高出 20 美元。GameStop 首席执行官 Ryan Cohen 表示，在他的领导下，eBay 有望取得更大成功，甚至能与亚马逊竞争。他还表示，如果 eBay 董事会拒绝收购提议，他准备直接向股东发起收购。

eBay 表示将考虑该提议，但分析师对此持怀疑态度。摩根士丹利指出两家公司业务模式“根本不同”，伯恩斯坦则认为 GameStop 资产规模较小，难以完成收购。GameStop 在疫情期间因“迷因股”热潮而走红，目前在美国拥有约 1600 家门店，财务状况有所改善，2025 年净利润达 4.184 亿美元，较前一年增长，但销售额下降。

eBay 成立于 1995 年，曾是知名的在线市场，但用户数从 2018 年的 1.75 亿下降到目前的 1.36 亿。Cohen 认为 eBay 价值被低估，收购后他将担任新公司的 CEO，不领取薪酬，仅根据公司表现获得报酬。GameStop 计划通过 TD Securities 获得约 200 亿美元债务融资，并计划在收购完成后一年内削减 eBay20 亿美元成本，主要集中在销售和市场营销部门。

分析师认为该提议对 eBay 来说并不理想，因为这将使其承担 GameStop 的债务。GameStop 股价在消息公布后下跌超过 9%，而 eBay 股价上涨 5%。Cohen 表示，GameStop 的实体店网络将为 eBay 的“直播电商”等业务提供支持，他批评 eBay 在电商转型上的进展缓慢。

HN 热度 629 points | 评论 588 comments | 作者：n1b0m | 15 hours ago #

https://news.ycombinator.com/item?id=48006402

GameStop 通过发行新股融资，获得了大量现金，缓解了财务压力，但并未真正实现盈利。
2025 财年 GameStop 净利润约 4.18 亿美元，营业收入和总收入有所下降，业务规模在缩小。
关闭亏损门店使利润有所提升，但收入持续下滑，显示其零售业务面临困境。
GameStop 的现金利息收入占利润较大比例，未来合并后现金减少可能影响利息收益。
公司过去多年未实现收入增长，整体业务呈现衰退趋势，类似于 Blockbuster 或 Tower Records 的衰落。
股票价格上涨主要受“meme 股”效应影响，市场估值更多反映现金资产而非业务增长潜力。
GameStop 作为法律上的当铺，收购 eBay 可能带来协同效应，如本地交易和鉴定服务，但具体执行存在不确定性。
eBay 的鉴定业务依赖合作伙伴，GameStop 门店对鉴定服务的实际增值有限。
仅靠削减成本和关闭门店无法实现长期增长，缺乏有效的业务扩展和创新策略。
4. 让我们收购 Spirit 航空 (Let’s Buy Spirit Air) #

https://letsbuyspiritair.com/

Spirit 航空于 2026 年 5 月 2 日凌晨 3 点停止运营，44 万名乘客失去了这家航空公司。该网页介绍了一个名为“Spirit 2.0”的合作社重建计划，旨在让乘客、员工和社区共同拥有这家航空公司，类似于 NFL 的绿湾包装工队的社区所有制模式。

该计划提出最低认捐额为 45 美元，相当于一张单程机票的价格。每位成员无论认捐金额多少，都拥有一票投票权，确保民主治理；而利润分配则按认捐金额比例进行。认捐者将成为合作社成员，共同决定航线、领导层和战略方向，避免私募股权控制和过度负债。

Spirit 2.0 强调透明运营、员工持股、合理高管薪酬、以及提供负担得起的机票。该合作社模式借鉴了 REI、Ocean Spray、Land O’Lakes 等成功的社区所有制企业。

网页呼吁公众立即参与认捐，组建足够的资金和支持力量，在私募股权介入前提交合作收购方案。当前阶段仅为非绑定意向认捐，不收取资金，所有权、利润分配等细节需经法律审查确认。

该项目旨在让 44 万乘客成为航空公司的共同所有者，实现航空作为公共服务的社会价值。

HN 热度 569 points | 评论 541 comments | 作者：bjhess | 1 day ago #

https://news.ycombinator.com/item?id=48002777

航空公司主要通过忠诚度计划和信用卡支付赚钱，飞行本身并不盈利。
有观点认为航空业应该成为受监管的公用事业，但也有人质疑这种说法的合理性。
航空公司盈利过多时有人呼吁监管，盈利不足时又有人认为需要监管，观点矛盾。
航空运输的核心服务类似于公共交通工具，但航空公司在服务和体验上存在差异。
超低成本航空公司如 Spirit 和 Frontier 的飞行体验与传统航空公司明显不同，服务质量较低。
传统航空公司和低成本航空公司在价格和服务上差异不总是很大，但低成本航空更频繁收取额外费用。
低成本航空公司常有多次推销和额外收费，传统航空公司也逐渐增加广告和推销。
航空公司通过多种收入来源补贴飞行服务，包括广告、信用卡推广等。
航空票价普遍较低，消费者倾向于选择价格最低的航班，限制了航空公司提价的空间。
有航空公司通过提高价格和改善服务实现更高盈利，如达美航空。
大部分美国主要航空公司仅靠售票和飞行本身难以盈利，飞行是信用卡业务的引流工具。
航空公司在成本和收入上几乎持平，票价收入无法覆盖全部运营成本。
5. 从 2027 年起，欧盟将强制要求智能手机配备可拆卸电池 (Removable batteries in smartphones will be mandatory in the EU starting in 2027) #

https://www.ecopv-eu.com/en/blog-en/replaceable-smartphone-batteries-2027-eu-regulation/

从 2027 年起，欧盟将强制要求新款智能手机和平板电脑必须配备可拆卸电池，用户能够使用标准工具自行更换电池。禁止使用需加热或溶剂才能拆除的胶粘剂。如果需要特殊工具，制造商必须免费提供。替换电池需保证至少 5 年内以合理价格供应。

此举旨在推动循环经济，减少电子废弃物，延长设备使用寿命，节省用户维修和更换成本，保护资源如锂和钴的回收利用，并提升回收过程中的安全性，防止因电池损坏引发火灾。

对用户而言，可自行维修降低维修费用，提高二手手机价值，并可能促使制造商延长软件支持周期。虽然可拆卸电池设计可能使手机稍微变厚或影响防水性能，但通过新型密封技术和结构设计，仍能实现防水功能。

部分特殊设备如医疗诊断设备或防爆工业手机可豁免此规定，若可拆卸电池影响安全性。

HN 热度 549 points | 评论 492 comments | 作者：rdeboo | 9 hours ago #

https://news.ycombinator.com/item?id=48009697

欧盟 2027 年起将强制智能手机使用可拆卸电池，但有电池容量保持率达到 80% 以上的例外情况，iPhone 等旗舰机型可能符合该例外。
电池容量保持率与充电策略有关，避免充满至最大电压（如 4.2V），充至 4.1V 或 4.05V 可显著延长电池寿命，但会牺牲部分容量。
电池充电电压与容量关系非线性，电池空电压约为 3V，充满电压约 4.2V，容量与电压的对应关系复杂。
电池寿命与充电周期定义有关，完整充放电周期（0%-100%-0%）与部分充电循环对电池影响不同。
现有法规中关于电池循环次数和容量保持率的具体要求存在差异，部分法规对专业维修人员提供电池有特殊规定。
充电周期和容量保持率的测量标准和定义存在争议，显示屏电量百分比反映的是当前容量的百分比。
用户普遍难以管理充电策略，设备系统（如 iOS）提供了智能充电管理功能以延长电池寿命。
通过智能插座和自动化手段可实现充电限制，如设定充电上限为 80%。
电池老化不仅与充电周期相关，还与使用时间长短有关，老化电池容量会自然下降。
实现 IP67 防水防尘等级的可拆卸电池设计是可能的，但“可拆卸”定义存在争议，拆卸难度和方式不同。
6. 伦敦新雕像，疑为班克斯作品，描绘一位被旗帜蒙眼的西装男士 (New statue in London, attributed to Banksy, of a suited man, blinded by a flag) #

https://www.smithsonianmag.com/smart-news/attributed-to-banksy-a-new-statue-of-a-suited-man-blinded-by-a-flag-and-walking-off-a-ledge-appeared-in-central-london-180988662/

近日，一尊疑似由街头艺术家班克斯（Banksy）创作的新雕像在伦敦市中心的滑铁卢广场悄然竖立。雕像描绘了一位穿西装的男子，手持一面被风吹得遮住视线的旗帜，正不知情地走向高台边缘。雕像底座上出现了班克斯的签名，随后班克斯的 Instagram 账号发布了相关视频，似乎确认了他的创作身份。

这尊雕像与周围其他历史人物雕像高度相仿，可能采用玻璃钢材质。附近有爱德华七世、南丁格尔以及克里米亚战争纪念碑等多座雕像。伦敦当局已在雕像周围设置安全护栏，并表示暂时无意拆除。伦敦市长萨迪克·汗的办公室称，班克斯的作品能够激发公众对现代艺术的兴趣和讨论，希望这件作品能被保存供市民和游客欣赏。

班克斯近期频繁推出公共艺术作品。2025 年圣诞节前，他曾发布两幅描绘仰望天空儿童的黑白壁画，关注儿童无家可归问题。尽管如此，班克斯的作品通常存在被迅速拆除的风险，比如 2025 年 9 月他在皇家法院绘制的法官暴力镇压抗议者的壁画就被当局迅速清除。

班克斯以壁画闻名，雕像作品较为罕见。2004 年，他曾在伦敦安装过一尊名为《饮酒者》的雕像，讽刺罗丹的《思想者》，表现一位头戴交通锥的男子坐姿。

此次雕像的出现延续了班克斯通过公共艺术表达社会和政治议题的传统，激发了公众的广泛关注和讨论。

HN 热度 543 points | 评论 532 comments | 作者：dryadin | 1 day ago #

https://news.ycombinator.com/item?id=48000152

这座雕像表现的是一个被国旗蒙蔽双眼的人，盲目自信地向前行进，象征着对国家主义的盲目追随。
雕像的姿态更像是无知地走下悬崖，而非英勇地迈向虚无，暗示盲目民族主义的危险和愚蠢。
走下悬崖意味着即将面临死亡或严重后果，比虚无更为可怕。
盲目行进的人缺乏对真实处境的认知，被民族主义的旗帜蒙蔽了双眼。
雕像中的人物形象是传统西方商人或政治家，体现了中老年男性形象。
有观点认为这象征着民族国家的衰亡或危机。
如果雕像使用其他国旗，比如巴勒斯坦国旗，可能引发更激烈的争议。
有评论指出，不同群体的盲目和偏见不应简单等同，强调民族主义中的极端行为更具威胁性。
热情和坚定信念有时是积极的，但狂热和盲目则往往带来问题。
爱国主义与民族主义之间存在区别，过于高声宣扬可能不是爱国主义的表现。
与极端分子对话往往无效，需识别“单向传输模式”避免无意义争论。
7. BYOMesh——全新 LoRa 网状无线电，带宽提升 100 倍 (BYOMesh – New LoRa mesh radio offers 100x the bandwidth) #

https://partyon.xyz/@nullagent/116499715071759135

该网页内容主要介绍了 partyon.xyz 这个独立的 Mastodon 服务器，定位为艺术家、活动家、创客和黑客的社区，致力于去中心化技术的交流与发展。管理员为 dataparty，当前活跃用户较少。

网页中重点发布了 @nullagent 关于 dataparty 团队即将推出的硬件产品 BYOMesh 的消息。BYOMesh 是一款极小且功能强大的 LoRa 伴侣开发套件，集成了 SX1276 芯片支持全子 1GHz ISM 频段，以及 SX1281 芯片支持高速 2.4GHz LoRa，适合网状网络爱好者使用。该设备旨在实现更高带宽的长距离无线连接，尤其适合复杂地形如山区的网络回传。

此外，讨论中提到 2.4GHz LoRa 相比传统 LoRa 在数据速率上有显著提升，能够在保持低功耗和长距离的同时，提供更高的带宽，达到传统 WiFi 技术难以实现的效果。社区成员还探讨了该技术的潜在应用、数据包大小优化、天线设计以及与其他无线协议的比较。

整体来看，网页内容围绕去中心化无线通信硬件的最新进展展开，展示了一个技术前沿且社区驱动的项目，适合对无线网状网络和 LoRa 技术感兴趣的开发者和爱好者关注。

HN 热度 469 points | 评论 150 comments | 作者：nullagent | 1 day ago #

https://news.ycombinator.com/item?id=47999636

“100 倍带宽”说法需证实，现有主流 LoRa 网状网络协议在美国可能不符合 FCC 规定，违规获得的带宽提升不等同于合法提升。
使用 800 kHz 和 1.6 MHz 带宽的 LoRa 配置符合 FCC 15.247 规定，2.4 GHz 频段允许更宽带宽，但代价是传输距离缩短，适合室内或定向天线环境。
欧洲 868 MHz 频段对低占空比（约 1%）有限制，而北美则没有类似限制。
频谱功率密度是监管重点，过窄带宽会导致信号功率集中，增加对其他用户的干扰风险。
FCC 要求使用扩频或跳频技术，目的是减少用户间的冲突和干扰。
频率过度使用会阻碍其他用户通信，存在违规风险。
2.4 GHz 频段环境复杂，存在大量 WiFi、蓝牙等设备，信号干扰严重。
这些 LoRa 网状网络主要适用于低带宽需求的场景，如远程传感、消息传递，不能替代传统互联网接入。
通过多设备轮换使用频率限制的做法理论上可行，但实际会被监管部门发现并处罚。
频谱规则复杂且多变，用户需权衡合法性与实际需求。
8. 智能代理编程是一种陷阱 (Agentic Coding Is a Trap) #

https://larsfaye.com/articles/agentic-coding-is-a-trap

本文探讨了当前业界流行的“智能代理编程”趋势，即通过 AI 代理自动生成代码，开发者主要负责规划和监督，而不直接编写代码。文章指出，这种方法虽然强大且便捷，但存在显著的权衡和风险。

首先，智能代理编程增加了系统复杂性，带来了 AI 生成代码的不确定性，同时导致开发者技能的退化。尤其是初级开发者缺少直接编写代码的实践，学习效果大打折扣。其次，依赖特定 AI 工具可能引发供应商锁定问题，且工具使用成本波动，给团队带来不稳定因素。

文章强调，成功运用此方法的关键在于开发者需具备较高的架构思维和批判性思维能力，能够在大量生成代码中发现潜在问题。然而，AI 工具的普及反而削弱了开发者的认知能力和批判性思维，形成了“监督悖论”：有效管理 AI 代理需要的技能正因过度依赖 AI 而退化。

此外，文章回顾了历史上编程抽象层次提升带来的争议，指出当前 AI 工具带来的影响更为直接和明显。资深工程师也面临认知模型模糊、难以全面理解复杂应用的问题。团队管理者也注意到，过度依赖 AI 会阻碍员工批判性思维和问题解决能力的培养。

最后，文章批评了当前 AI 编码工具过分追求速度和代码量的趋势，忽视了代码质量、理解深度和简洁性。作者呼吁重新认识编码的价值，强调编码不仅是技术实现，更是规划和思考的过程，直接参与编码有助于培养全面的技术视角和解决问题的能力。

HN 热度 423 points | 评论 330 comments | 作者：ayoisaiah | 1 day ago #

https://news.ycombinator.com/item?id=48002442

使用 agentic coding 可以快速学习语言和系统细节，但需要丰富经验来正确引导和纠正其错误。
认为必须对所有工作内容都了如指掌是不现实的，特别是在团队和大型代码库中，没人能完全掌握所有细节。
初学者容易过度依赖 agentic coding，缺乏判断和识别自身知识盲区的能力。
应该避免对 agentic coding 的绝对否定，需探索其合理和适度的应用方式。
学生与教师在目标和期望上的巨大差异导致教育难以有效进行，而编程者与管理者的目标通常较为一致。
程序员与智能代理的关系可以是互助共生，也可能变成依赖导致技能退化和价值降低。
掌握基础知识和系统设计能力依然重要，agentic coding 强调了这一点。
未来软件开发可能会高度依赖 agentic coding，采用增量发布和自动监控，深度调试将成为少数专家的职责。
依赖 AI 生成的代码作为生产代码存在风险，需求表达和错误检测仍然复杂且难以完全自动化。
AI 生成代码的缺陷可能通过渐进式发布和自动监控来缓解，允许在小范围内试运行并根据反馈调整。
AI 不必完美，只需达到项目可接受的“足够好”标准，哪怕带来更多失败也可能因节省成本而被接受。
9. Issues 和 Webhooks 事件 – 已解决 (Incident with Issues and Webhooks – Resolved) #

https://www.githubstatus.com/incidents/72q3n8yxthcy

该网页是 GitHub 的状态页面，主要用于发布和更新 GitHub 平台的服务状态和故障通告。页面显示了最近一次 GitHub 服务中断事件的详细信息，包括受影响的服务范围、故障发生和恢复的时间节点，以及各个子服务（如 Issues、Webhooks、Codespaces、Pull Requests、Actions、Packages、Pages 和 Git Operations）的具体状态变化。

事件报告显示，GitHub 在 2026 年 5 月 4 日经历了一次多服务性能下降和可用性问题，涉及多个核心功能。页面详细记录了从发现问题、服务降级、持续调查到问题缓解和恢复正常的全过程。用户可以通过该页面订阅邮件、短信、Slack 或 Webhook 通知，实时获取 GitHub 服务的最新状态更新。

此外，页面还提供了 GitHub 相关产品、资源和支持的链接，方便用户获取更多技术文档、社区支持和开发者工具信息。整体内容旨在帮助用户了解 GitHub 服务的健康状况和维护进展，确保用户能够及时应对可能的服务中断。

HN 热度 419 points | 评论 252 comments | 作者：gen220 | 8 hours ago #

https://news.ycombinator.com/item?id=48010301

GitHub 使用率大幅增加，主要归因于智能代理编程的兴起，导致基础设施压力增大，未来可能调整限额或收费策略以控制负载。
GitHub 平台活动激增，提交次数和 GitHub Actions 使用时间大幅增长，工程师面临巨大扩展和稳定性挑战。
微软收购后，GitHub 通过价格和产品策略推动用户迁移到自家平台，减少对第三方工具的依赖，增加了核心服务的负载。
代理编程导致提交频率显著提升，部分是模型调整使代理更频繁提交，部分是真实工作量增加，尤其在自动化实验和研究中效果显著。
代理编程带来了工作效率的质变，能够自动进行复杂实验和迭代，大幅缩短时间并提升文档质量，但也带来了更多提交和计算资源消耗。
随着代理使用增加，GitHub 可能会通过计费来应对资源压力，用户需权衡成本与价值。
一些用户开始转向自建或开源平台以降低成本和提升控制力，尤其是个人项目和非商业用途。
未来代理编程的价值评估将更加重要，需将代码质量与业务价值紧密结合，避免无意义的资源浪费。
本地和开源模型的发展为用户提供了低成本替代方案，若商业服务价格过高，用户有可能转向这些替代品。
Talking to strangers at the gym #

https://news.ycombinator.com/item?id=48008672

One of the things I like about this is that OP is giving people genuine compliments without any particular agenda.

It reminds me of one of my favorite parts of How to Win Friends and Influence People by Dale Carnegie, where he tells a story about complimenting someone, and a student asks what he was hoping to gain from offering the compliment. Carnegie is incensed:

I was waiting in line to register a letter in the Post Office at Thirty-Third Street and Eighth Avenue in New York. I noticed that the registry clerk was bored with his job[…] So while he was weighing my envelope, I remarked with enthusiasm: “I certainly wish I had your head of hair.”

He looked up, half-startled, his face beaming with smiles. “Well, it isn’t as good as it used to be,” he said modestly. I assured him that although it might have lost some of its pristine glory, nevertheless it was still magnificent. He was immensely pleased. We carried on a pleasant little conversation, and the last thing he said to me was: “Many people have admired my hair.”

I told this story once in public; and a man asked me afterwards: “What did you want to get out of him?”

What was I trying to get out of him!!! What was I trying to get out of him!!!

If we are so contemptibly selfish that we can’t radiate a little happiness and pass on a bit of honest appreciation without trying to screw something out of the other person in return—if our souls are no bigger than sour crab apples, we shall meet with the failure we so richly deserve.

Oh yes, I did want something out of that chap. I wanted something priceless. And I got it. I got the feeling that I had done something for him without his being able to do anything whatever in return for me. That is a feeling that glows and sings in your memory long after the incident is passed.

mtlynch

我喜欢这一点，是因为楼主给人真诚的赞美，而没有任何别有用心的目的。

这让我想起戴尔·卡耐基的《如何赢取朋友与影响他人》中的一个我最喜欢的部分，他讲了一个关于赞美别人的故事，一个学生问他赞美别人究竟想得到什么。卡耐基非常愤怒地说：

“我在纽约三十三街和第八大道的邮局排队登记信件。我注意到登记员对他的工作感到厌烦……所以当他称重我的信封时，我热情地说：‘我真希望我能有你这么浓密的头发。’

他抬头，半惊讶，脸上露出了笑容。‘嗯，没以前那么好了，’他谦虚地说。我向他保证，虽然可能失去了一些原始的光彩，但仍然很棒。他非常高兴。我们进行了愉快的交谈，他最后对我说：‘很多人都很羡慕我的头发。’

我在公开场合讲过这个故事；之后有个人问我：‘你想从他那里得到什么？’

我想从他那里得到什么！！！我想从他那里得到什么！！！

如果我们自私到连传递一点点幸福和真诚的赞赏都不能，非得从别人那儿占点便宜——如果我们的灵魂和酸苹果一样小，我们就注定会遭到应得的失败。

哦，是的，我确实想从那个家伙那里得到点什么。我想要无价的东西。我得到了。我感觉自己为他做了一件事，而他却无法回报我。这种感觉在事件过去很久之后仍在你的记忆中闪耀和歌唱。”

DeepClaude – Claude Code agent loop with DeepSeek … #

https://news.ycombinator.com/item?id=48002640

#!/bin/sh export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic export ANTHROPIC_AUTH_TOKEN=sk-secret export ANTHROPIC_MODEL=deepseek-v4-flash export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 exec claude $@

aftbit

#!/bin/sh 导出 ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic 导出 ANTHROPIC_AUTH_TOKEN=sk-secret 导出 ANTHROPIC_MODEL=deepseek-v4-flash 导出 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 执行 claude $@

GameStop makes $55.5B takeover offer for eBay #

https://news.ycombinator.com/item?id=48006580

Important background: https://investor.gamestop.com/news-releases/news-details/2026/GameStop-Announces-Long-Term-Performance-Award-for-Ryan-Cohen/default.aspx

CEO gets paid “only if GameStop achieves a market capitalization of $20 billion.” Buying a $55bn company would certainly achieve that quickly. I’m not sure how they’d manage that (buy with what? Memes?), other than the should-be-illegal process of putting debt on the acquired company’s balance sheet.

pjc50

CEO只有在GameStop市值达到200亿美元时才会获得报酬。收购一家市值550亿美元的公司肯定会很快达到这个目标。我不确定他们会如何做到这一点（用什么买？用梗？），除了一种本应是非法的做法——将债务计入被收购公司的资产负债表。

Removable batteries in smartphones will be mandato… #

https://news.ycombinator.com/item?id=48009960

There’s an exception for batteries that “retain at least 80% of its original capacity after 1,000 charge cycles.” Coincidentally, iPhones and probably other flagships already qualify for this exception.

wmf

有一个例外是电池在经过1000次充电循环后“仍保持至少80%的原始容量”。巧合的是，iPhone和可能其他旗舰机已经符合这个例外条件。

Let’s Buy Spirit Air #

https://news.ycombinator.com/item?id=48003932

Company makes too much money: “they’re extracting monopolist rents! They need to be a regulated utility!”

Company makes too little money: “there’s no money in this industry! They need to be a regulated utility!”

gruez

公司赚的钱太多：“他们在赚取垄断利润！应该被当作公用事业进行监管！”

公司赚的钱太少：“这个行业根本赚钱不了！应该被当作公用事业进行监管！”

Agentic Coding Is a Trap #

https://news.ycombinator.com/item?id=48003369

Interestingly I’ve learned more about languages and systems and tools I use in the last few years working with agentic coding than I did in 35 years of artisanal programming. I am still vastly superior at making decisions about systems and techniques and approaches than the agentic tools, but they are like a really really well read intern who knows a great deal of detail about errata but have very little experience. They enthusiastically make mistakes but take feedback - at least up front - even if they often forget because they don’t totally understand and haven’t internalized it.

The claim you should know everything about everything you work on is an intensely naive one. If you’ve worked on a team of more than one there’s a lot of stuff you don’t totally grok. If you work in an old code base there’s almost every bit of it that’s unfamiliar. If you work in a massive monorepo built over decades, you’re lucky if you even understand the parts everyone considers you an expert in it.

I often get the impression folks making these claims are either very junior themselves or work basically alone or on some project for 20 years. No one who works in a team or larger org can claim they know everything in their code base. No one doing agentic programming can either. But I can at least ask the agent a question and it will be able to answer it. And after reading other people’s code for most of my adult life, I absolutely can read the LLMs. The fact a machine wrote crappy code vs a human bothers me not in the least, and at least the machine will take my feedback and act on it.

fnordpiglet

有趣的是，过去几年我在使用智能代理编程时，学到的关于语言、系统和工具的知识，比我35年手工编程的经验还要多得多。虽然我在系统、技术和方法的决策上依然远远优于智能代理工具，但它们就像一个读书非常多、对各种错误细节了如指掌但经验很少的实习生。它们热情地犯错，但会接受反馈——至少一开始是这样——即使它们经常因为不完全理解或未内化而忘记这些反馈。

“你应该对所做的一切都知无不言、无所不晓”的说法非常幼稚。如果你曾在一个多人的团队工作过，会发现有很多内容你并不完全理解。如果你在一个老旧代码库工作，几乎每部分代码都对你很陌生。如果你在一个历经数十年构建的大型单一代码库中工作，哪怕是在别人眼中你是专家的部分也难保证你完全理解。

我经常觉得提出这种观点的人，要么本身经验很少，要么基本上是单打独斗，或者在同一个项目上干了20年。没有哪个在团队或更大机构里工作的人能说自己对整个代码库了如指掌。做智能代理编程的人也不可能做到这一点。但我至少可以问智能代理一个问题，它能回答。经过成年后的大量阅读别人的代码，我完全能理解大型语言模型（LLM）写的代码。机器写出糟糕代码这事儿根本不会困扰我，况且至少机器会接受我的反馈并根据反馈调整自己的行为。

GameStop makes $55.5B takeover offer for eBay #

https://news.ycombinator.com/item?id=48008525

The original shorting of GameStop back in 2021 gave them a bit of a boost back into the green. While people were doing the GME to the moon, GameStop made more shares to sell, and paid off a bit of its debts, I think it made about a billion dollars in profit, they’re still struggling, but it helped prolong their life.

A friend of mine also pointed out and this made it click for me that it makes 100% sense, GameStop is setup as a legal pawnshop in every state. So a pawnshop buying out eBay makes insane sense.

This merger in theory could be good for both eBay and GameStop if they don’t mess it up. Imagine being able to list your eBay items locally without having to have people needing to come to your house, or better yet, getting a cut of what you wanted up front since they’re basically a pawn shop, and then they list it on eBay and turn a bit of a profit with a local pickup option available.

I could see this working out decently, assuming the CEO of GameStop doesn’t mess it up completely.

giancarlostoro

2021年对GameStop的最初做空让他们的股价稍微回升了一点。虽然大家都在喊着“GME要飞向月球”，但GameStop增发了更多股票出售，并偿还了一部分债务，我觉得他们大概赚了10亿美元的利润，虽然他们仍在挣扎，但这帮助他们延长了存活时间。

我有个朋友还指出了一点，让我顿悟了，这完全说得通，GameStop在每个州都被设立为合法的当铺。所以一个当铺收购eBay简直是天作之合。

理论上，如果两家公司不搞砸，这次合并对eBay和GameStop都有好处。想象一下，你可以在eBay上本地发布商品，而不需要别人来你家，或者更好的是，既然它们本质上是当铺，你还能先拿到你想要的部分钱，然后他们再在eBay上挂牌出售，同时提供本地取货选项，从中赚取一点利润。

我觉得这有可能挺奏效的，前提是GameStop的CEO别把事情完全搞砸。

Let’s Buy Spirit Air #

https://news.ycombinator.com/item?id=48003498

Fundamental problem: Flights don’t make money. Airlines actually make all of their money through loyalty programs and credit card payments. They basically should have turned into regulated utilities long ago, but loyalty program revenue saved them.

Unless this initiative will turn into a credit card company (which nobody likes or wants to do) it won’t go anywhere

Private equity will likely sell the company for parts. There is no operational improvements for cash flow that they can do.

Useful watch (skip to 2:20): https://youtu.be/ggUduBmvQ_4?si=cyysP7aH_CIEDZRq

rapatel0

根本问题：航班本身不赚钱。航空公司实际上所有的收入都来自于积分奖励计划和信用卡支付。它们本应该早就转型成受监管的公共事业，但积分奖励计划的收入救了它们。

除非这个计划变成一家信用卡公司（没人喜欢也没人想这么做），否则不会有进展。

私募股权很可能会把公司拆卖。它们无法通过运营改进现金流。

有用的视频（跳到2:20看）：https://youtu.be/ggUduBmvQ_4?si=cyysP7aH_CIEDZRq

New statue in London, attributed to Banksy, of a s… #

https://news.ycombinator.com/item?id=48000980

The point is not just that he’s blinded by the flag: He’s boldly marching into the void, confident. “wrapped in the flag” is a great saying.

ggm

重点不仅仅是他被旗帜蒙蔽了双眼：他还带着自信大胆地走向空无。“裹着旗帜”是个很形象的说法。

Security through obscurity is not bad #

https://news.ycombinator.com/item?id=48000195

Obscurity can be fine but it’s not security. I think of it like cover and concealment in the military. Security is cover. Something you can get behind so the bullets don’t hit you. Obscurity is concealment. Harder to see, harder to find, so the enemy doesn’t know where to shoot, but it’s not stopping any bullets. Both have advantages and disadvantages and can complement each other depending on how they’re used.

rascul

隐蔽性可能没问题，但它不是安全性。我把它看作军事中的掩护和伪装。安全性是掩护，就是你可以躲在后面，子弹打不到你的东西。隐蔽性是伪装，更难被发现，更难被找见，所以敌人不知道往哪里射击，但它无法阻挡任何子弹。两者各有优缺点，且根据使用方式不同，可以相辅相成。

Does Employment Slow Cognitive Decline? Evidence f… #

https://news.ycombinator.com/item?id=48012294

The problem isn’t retirement per se, it is that people don’t have things to occupy themselves with. They retire and they vegetate. I worked with a lady that was in her 70s who was deathly afraid of retiring because she didn’t have anything to do. That’s beyond depressing to me, to be incapable of even conceiving of doing something that doesn’t involve going to a job.

We have created people that never develop as human beings outside the context of their being economic entities in the workforce and that’s not something to celebrate.

b00ty4breakfast

问题不在于退休本身，而是人们没有事情可做来充实自己。他们退休后就变得呆板无趣。我曾经和一个70多岁的女士共事，她极度害怕退休，因为她不知道该做什么。对我来说，这非常令人沮丧，甚至无法想象自己做些不需要上班的事情。

我们培养出的人，从未在脱离工作身份的情况下作为人类自身得到发展，这绝不是值得庆祝的事。

Talking to strangers at the gym #

https://news.ycombinator.com/item?id=48008887

I avoided this book for a long time. for some reason I got it in my head that it’s a sort of red pilled book that teaches you how to manipulate people. I know it’s very shallow on my side, but I somehow crystallized this opinion based on a few acquaintances that claimed to read it and instead that they include the name of a person they just met in every sentence because it made that person like them more.

Your comment made me consider reading it. This rant about radiating happiness towards people without expecting something in return gives me a different insight on his reasons for writing the book.

I might give it a shot. Thank you

alexmuresan

我很长时间都没读这本书。出于某种原因，我脑海中形成了这样一个想法：这是一本让你学会操控别人的“觉醒”书。我知道这是我自己的偏见，但我就是根据几个说自己读过这本书的熟人得出了这样的结论，他们说书中会在每句话里加入刚认识的人的名字，因为这样能让那个人更喜欢他们。

你的评论让我考虑去读这本书了。关于无私地向别人传递快乐而不求回报的这段激烈表达，让我对作者写这本书的原因有了不同的理解。

我可能会试试看，谢谢你。

Let’s Buy Spirit Air #

https://news.ycombinator.com/item?id=48003876

Why does any of this imply they should become a regulated utility? This seems like a textbook case of the free market pushing prices down to cost. Having alternative revenue streams pushed that minimal price down; but even without that, there is no reason to think the market would have done anything other than push prices to the lowest level possible in that environment as well.

gizmo686

为什么这些情况会意味着他们应该成为受监管的公共事业？这看起来像是自由市场将价格压低到成本价的典型案例。拥有替代收入来源使得这个最低价格进一步降低；但即使没有这些收入来源，也没有理由认为市场在那种环境下会做出除将价格压到最低可能水平以外的任何事情。

New statue in London, attributed to Banksy, of a s… #

https://news.ycombinator.com/item?id=48002674

Strong disagree. First, like many of the other comments mention, Banksy is known for being clever and witty, but not particularly subtle.

But more to the point, while you may think the meaning is a bit obvious, the fact that the flag is unadorned (which/whose flag is it?), and the man is unknown, makes me think this statue could be the ultimate Rorschach test. I’m sure there are tons of people thinking “Ha ha, this is the perfect commentary on all those idiot <people on the other side who I disagree with> wrapping themselves up in their ideology of <patriotism/social justice/cause du jour> as they march <some particular country/society/the world at large off a cliff>”.

In other words, I’m guessing you probably felt the meaning was “obvious” because you filled in the blanks in the above madlibs-style statement in a way that feels obvious to you, and I think folks on “the other side” would probably fill in the blanks with the exact opposite notions in a way that feels “obvious” to them.

hn_throwaway_99

坚决反对。首先，正如许多其他评论所提到的，班克斯以机智巧妙著称，但并不特别含蓄。

更重要的是，虽然你可能觉得这个意义有点明显，但旗帜是简洁的（这是谁的旗帜？），而且这个人身份不明，这让我觉得这座雕像可能是终极的罗夏墨迹测试。我相信很多人会想，“哈哈，这正是对那些愚蠢的<我不同意的另一方的人>裹挟自己于<爱国主义/社会正义/当日热点议题>的意识形态中，边游行边把<某个特定国家/社会/整个世界>带向悬崖的完美评述。”

换句话说，我猜你觉得意思“显而易见”，是因为你以自己觉得显而易见的方式，填充了上述Mad Libs式的空白，而我认为“对立面”的人们很可能会以完全相反的观念填充这些空白，对他们来说同样“显而易见”。

Talking to strangers at the gym #

https://news.ycombinator.com/item?id=48009041

I avoided this book for a long time. for some reason I got it in my head that it’s a sort of red pilled book that teaches you how to manipulate people.

FWIW this book came out in the 1930s, long before “red pilling” was a thing. I’ve read it before and it’s not about manipulating people unless you consider being a genuinely sincere person to be manipulative in some way. It’s a good book, if a little outdated, and, if I could summarize it in one glib sentence, its lesson is “If you want people to like you, then be nice to them, be genuine, and show enthusiasm and interest in what they show enthusiasm and interest in.”

nozzlegear

我很长时间都避免读这本书。出于某种原因，我脑海里一直认为它是一种“红丸”书，教你如何操控别人。

顺便说一句，这本书是在1930年代出版的，远早于“红丸”这个概念。我以前读过，书里并不是教你操控别人，除非你把做一个真诚的人看作某种操控。它是一本好书，虽然有点过时。如果我要用一句轻松的话来总结，书的教训就是：“如果你想让别人喜欢你，那就对他们好，真诚待人，对他们感兴趣的事情表现出热情和关注。”

Microsoft Edge stores all passwords in memory in c… #

https://news.ycombinator.com/item?id=48013060

This feels like a case of “It rather involved being on the other side of this airtight hatchway”[1]. If you can read arbitrary process memory, you’re probably also in a position to just dump out the passwords by pretending to be the user in question.

If an attacker gains administrative access on a terminal server, they can access the memory of all logged‑on user processes.

If an attacker has administrative access, they can also attach a debugger to every chrome process and force it to decrypt all the passwords. The only difference this really makes is in coldboot attacks, but even then it’s still not clear whether it makes the attacker’s job slightly easier, or allows an attack that’s otherwise not possible.

[1] https://devblogs.microsoft.com/oldnewthing/20060508-22/?p=31283

gruez

这感觉像是“处于这扇密封舱口另一侧的情况”[1]。如果你能读取任意进程内存，你很可能也能通过伪装成相关用户来导出密码。

如果攻击者获得了终端服务器的管理员权限，他们就可以访问所有已登录用户进程的内存。

如果攻击者拥有管理员权限，他们也可以附加调试器到每个 Chrome 进程，强制其解密所有密码。其实这唯一的区别在于冷启动攻击，但即使如此，目前也不清楚这是否让攻击者的工作稍微轻松一些，或者是否允许了原本不可能实现的攻击。

[1] https://devblogs.microsoft.com/oldnewthing/20060508-22/?p=31283

DeepClaude – Claude Code agent loop with DeepSeek … #

https://news.ycombinator.com/item?id=48002559

I’m not exactly sure what the point of this is. Deepseek already has instructions to use its API with many CLI’s including Claude Code directly:

https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code

vitaflo

我不太确定这的意义是什么。Deepseek已经有使用其API与许多命令行工具（包括Claude Code）直接集成的说明：

https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code

Denuvo has been cracked in all single-player games… #

https://news.ycombinator.com/item?id=48002677

During the time of the Soviet Union, it was an urban legend that during supply shortages, Soviet factories would have no real work, but workers needed to keep up the appearance of working, so they would have one line of workers continuously assembling devices, feeding into another line that would continuously disassemble them, all in a loop where nothing gets produced.

In many ways, it feels like we are seeing this today in the digital world. As a specific example, GTA 5 (singleplayer) is a game that has been pirated for about 10 years now, and has received zero content updates in that time, yet somewhat recently (maybe a few years ago?) they updated the game on Steam to have new DRM that constantly conflicts with the Steam Deck sleep mode and kicks you out of the game at random after waking up, or just won’t even let you launch if you’re without internet and haven’t launched it within a few days. Nothing worthwhile was produced by this endeavor, that’s for sure.

a2128

在苏联时期，有一个都市传说，说是在物资短缺的时候，苏联工厂实际上没有真正的工作可做，但工人们需要保持正在工作的假象，所以他们会让一条生产线上工人不停地组装设备，然后再送到另一条生产线上不停地拆解设备，形成一个循环，实际上没有任何产品被生产出来。

在很多方面，我们今天在数字世界中似乎也看到了类似的情况。举一个具体例子，GTA 5（单人模式）这款游戏已经被盗版了大约十年，期间没有收到任何内容更新，但最近（也许是几年前？）他们在Steam上给这款游戏更新了新的数字版权管理（DRM），这个DRM不断与Steam Deck的休眠模式冲突，唤醒后会随机把你踢出游戏，或者如果几天内没有联网启动游戏，甚至根本无法启动。可以肯定的是，这个举动并没有带来任何有价值的成果。

GameStop makes $55.5B takeover offer for eBay #

https://news.ycombinator.com/item?id=48009110

“I think it made about a billion dollars in profit”

It raised over a billion dollars of capital (i.e. issued shares in return for cash). It did not make a billion dollars in profit (and has never had a year when it did).

rahimnathwani

我认为它赚了大约十亿美元的利润。

它筹集了超过十亿美元的资本（即通过发行股票换取现金）。它并没有赚取十亿美元的利润（而且从未有过一年利润达到这个数）。

How far behind is each major Chromium browser? #

https://news.ycombinator.com/item?id=47999161

I would like to see all “desktop” applications that use Electron listed and how big of a Chromium drift is there, especially how many applications are shipping runtimes with unfixed vulnerabilities.

butz

我希望能看到所有使用Electron的“桌面”应用程序的列表，以及它们与Chromium版本的差异有多大，特别是有多少应用程序仍然使用带有未修复漏洞的运行时。
