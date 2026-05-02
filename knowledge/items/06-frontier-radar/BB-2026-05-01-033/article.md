# 中国旗舰大模型横评 2026 春

- BestBlogs URL: https://www.bestblogs.dev/explore/topics/china-flagship-llm-2026-spring
- Extraction: DOM text from BestBlogs page
- Extracted chars: 4165
- Original publisher URL: https://www.bestblogs.dev/status/2046249571882500354

---

对比维度
维度	DeepSeek-V4 Preview
百万上下文 + 双思考的开源旗舰
	智谱 GLM-5.1
754B MoE 的 8 小时长程任务模型
	MiniMax M2.7
首个具备「自我进化」能力的中国旗舰
	Kimi K2.6
1T MoE，长程编码与 Agent 集群标杆

开源策略与许可	
权重 MIT 开源，Pro/Flash 双版本同步上 Hugging Face

ref-3、ref-6 验证论文与多硬件生态；可商用、可二次蒸馏。

	
权重 MIT 开源，Hugging Face + 华为云双线

ref-8 智谱官方解读；ref-13 上线华为云的国内合规通道。

	
M2.7 退回 MiniMax 专有许可（M2/M2.5 曾是 MIT）

ref-16 公布开源细节；ref-17 提示许可证从 MIT 调整为专有许可。

	
权重以修改版 MIT 形式公开，训练代码与数据未公开

ref-22 月之暗面官方解读；ref-26 第三方验证开源等级。


上下文窗口与模型规模	
1.6T / 49B 激活（Pro），284B / 13B 激活（Flash）；1M 上下文，最大输出 384K

ref-2 公布双思考与上下文；ref-4 给出 484 天换代细节。

	
754B / 40B 激活；200K 上下文，131K 最大输出

ref-10 给出 754B / 40B 与 SWE-Bench Pro SOTA；ref-9 中文版同步。

	
约 196K（192K 量级）上下文；具体激活参数未公开

ref-15 给出能力定位；ref-17 第三方报道补充上下文与价格。

	
1T / 32B 激活；256K 上下文

ref-22 与 ref-26 共同验证规模与上下文；MoonViT 视觉编码器是新增项。


编程能力（SWE-Bench / Arena）	
DeepSeek 自报『接近前沿』；LMSYS Arena Pro/Flash 排名靠前

ref-5 第三方实测；ref-27 LMSYS Arena 横向证据。

	
SWE-Bench Pro 58.4 全球第一，超过 GPT-5.4 与 Opus 4.6

ref-9、ref-10 双语版本；ref-12 Code Arena 开源榜独立排名。

	
SWE-Pro 56.22%，Terminal Bench 2 57%，多语言 SWE 76.5

ref-17 给出基准全集；ref-21 解释 Harness × 模型协同。

	
SWE-bench Verified 80.2%，SWE-Bench Pro 58.6

ref-26 第三方实测；ref-22 月之暗面自报与 ref-25 实战长文交叉验证。


长程任务 / Agent 集群	
双思考模式：Thinking / Non-Thinking 切换；Think Max 建议上下文 ≥384K

ref-2 官方双模式说明；适用于长链推理但缺『多 Agent 集群』的官方支持。

	
8 小时自主执行；可零介入交付完整 Linux 桌面系统

ref-8、ref-10 解释 8 小时长程；ref-9 给出端到端交付案例。

	
首个具备『自我进化』能力的国产旗舰，可承担 30-50% 强化学习工作流

ref-15 官方定位；ref-17 给出量化数字；ref-21 给出 Harness 协同视角。

	
4000+ 工具调用 / 12 小时连续运行 / 300 并行子智能体

ref-22、ref-25 共同披露；ref-24 给出 Hermes Agent 实战路径。


多模态能力	
以文本 / 代码为主；本次预览版未把多模态作为重点

ref-1、ref-3 中均未把多模态作为关键卖点。

	
聚焦智能体编码与桌面操作；多模态非本次发布重心

ref-9 与 ref-13 都把焦点放在 Coding 与长程任务，未列多模态突破。

	
文本 / 代码 / Agent 主线；多模态仍走早期 Hailuo 视频路线

ref-15、ref-17 主线均为文本与 Agent；多模态未在 M2.7 公告中强调。

	
MoonViT 视觉编码器加持，支持图像与视频输入

ref-22 月之暗面官方说明 MoonViT；ref-26 第三方验证视觉路径。


API 价格与部署生态	
Pro 输入 $1.74 / 输出 $3.48；Flash 输入 $0.14 / 输出 $0.28；华为昇腾 + 英伟达 Blackwell 双栈

价格见 ref-2、ref-5；硬件生态见 ref-6；实战切换见 ref-7（账单降 90%）。

	
权重 MIT 自托管；Z.AI 平台输出价较 Opus 4.6 便宜约 17×

ref-10、ref-13 给出价格区间与华为云部署；具体单价未单独披露，仅给出相对量级。

	
API 输入 $0.30 / 输出 $1.20 per 1M tokens；Hugging Face + Modelscope 开源

价格见 ref-17；许可调整说明见 ref-16；ref-19 给出 M2.5 时期『1 美金/小时』背景。

	
API 输入 $0.95 / 输出 $4.00 per 1M tokens；Hugging Face 自托管 + 多家三方平台

官方与第三方价格见 ref-22 与 ref-26；不同平台报价存在 ±20% 区间。

使用场景建议
国内自建推理 / 数据合规优先
→ DeepSeek-V4 Preview

DeepSeek-V4 是这四家里最完整的『MIT 开源 + 华为昇腾 + 英伟达 Blackwell 双栈』组合（ref-3、ref-6），1M 上下文与双思考模式覆盖了大部分企业内部场景。Flash 版本输出 $0.28 / 1M tokens，是当下国内合规自托管最现实的起点；ref-7 的真实切换案例已经把月账单打到了原来的 1/10。

开源模型相对闭源模型的能力差距正在快速收敛（LangChain，2026-04，[ref-28]）

8 小时长程任务 / 端到端交付
→ 智谱 GLM-5.1

GLM-5.1 把『8 小时自主执行 + SWE-Bench Pro 58.4 SOTA』做成了一句话定位（ref-8、ref-10）。ref-9 给出的『零介入交付完整 Linux 桌面』是其他三家目前都没做到的可验证场景。如果你要让模型独立跑完一个项目而不是补一段代码，GLM-5.1 是当下中国阵营里最稳的选择。

Simon Willison 在 GLM-5.1 上跑的『骑自行车的鹈鹕』经典生成测试，是他横评所有前沿模型的固定动作（[ref-11]）

真实工作流 + 自动化进化
→ MiniMax M2.7

MiniMax M2.7 是中国阵营首个明确做出『模型参与自身开发循环』承诺的旗舰（ref-15、ref-17）；定价 $0.30 / $1.20 + 主流编码与 Terminal-Bench 接近 GPT-5.3-Codex（ref-17）让它在『成本优先 + 真实生产工作流』场景下很有竞争力。ref-21 还把 Harness × 模型作为下一步重点，这是其他三家短期内不会跟进的角度。

MiniMax M2.7 自我进化能力示意图（VentureBeat，2026-03，[ref-17]）

Agent 集群 / 多 sub-agent 编排
→ Kimi K2.6

Kimi K2.6 在 SWE-bench Verified 拿到 80.2、SWE-Bench Pro 58.6（ref-26），并且首次把『4000+ 工具调用 / 12 小时 / 300 并行子智能体』作为一线指标（ref-22、ref-25）。ref-24 给出了 Hermes Agent + K2.6 的工程化路径，是当前最适合做『单 prompt 启动一支 Agent 团队』的中国旗舰。

常见误区
M2.7 的开源 regression：MIT 退到专有许可

MiniMax M2 / M2.5 曾以 MIT / Modified-MIT 形式开源，是这一波国产开源浪潮的代表作。但 M2.7 切回 MiniMax 自己的专有许可（ref-16、ref-17）。如果你的合规底线是『商用 + 二次蒸馏不受限』，M2.7 实际上不再满足。在工程选型上，M2.5 在不少团队仍被作为生产基线，M2.7 更像『官方推荐部署版本』而非『真正可二次发行的权重』。

SWE-Bench Pro 接近不等于真实工作可靠

GLM-5.1（58.4）/ MiniMax M2.7（56.22）/ Kimi K2.6（58.6）在 SWE-Bench Pro 上的分数十分接近，但 ref-25 与 ref-29 的实战复盘提醒：长程任务的真实瓶颈往往不是『一道编程题答对几次』，而是工具调用稳定性、上下文恢复、错误自愈与 Harness 适配。基准跑分应当只是入选条件，不是排序依据；真正决定可用性的是你的工作流模板能否在该模型上跑稳一周。

同期多家中国旗舰与 Opus 4.6 的对比快照（AINews / Latent.Space，2026-04，[ref-6]）

便宜不等于划算：自托管的硬件账

DeepSeek-V4 1.6T、Kimi K2.6 1T、GLM-5.1 754B 的『开源 + 极低 API 价』很容易让人觉得迁移就能立刻省钱。但 ref-6、ref-29、ref-30 综合给出的更现实图景是：1）自托管 1T+ MoE 仍需 H100 / Blackwell 集群或华为昇腾大池；2）国内可用算力价格还在波动；3）从闭源迁过来时的 prompt 重写、回归测试、Token 计量差异，单项就能吃掉首年节省。把价格当『参考』，把 TCO 当『决策依据』。
