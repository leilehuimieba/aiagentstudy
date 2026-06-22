# 情报更新：X 社区线索里的 Mastra 投毒与 Agent Skill 供应链风险

> Date: 2026-06-18
> Collection mode: Kimi WebBridge logged-in X search, slow read-only browsing, then evidence backtracking to primary / researcher sources.
> Safety: 本文保留攻击链形状、检测信号和防御测试思路，不收录可直接攻击真实系统的 exploit 脚本。

## 搜索过程记录

本轮按用户要求使用真实浏览器登录态继续查 X / Twitter，但采用低频只读方式：

- Kimi WebBridge 健康，扩展在线。
- X 已进入登录后搜索页，能够读取搜索结果时间线。
- 搜索组 1：`MCP / Model Context Protocol + tool poisoning / credential theft / malware / exploit`。
- 搜索组 2：`Claude Code / Codex / AI coding agent + prompt injection / token / OIDC / GitHub Actions`。
- 搜索组 3：`SkillSpector / easy-day-js / Mastra-AI / MCP packages + security / npm`。
- 搜索组 4：`agent skills / MCP package / MCP server + vulnerability / malicious / maintainer`。

我没有做关注、点赞、回复、收藏，也没有高频翻页。X 只作为线索入口；重要事实继续回链到 StepSecurity、JFrog、NVIDIA、Snyk、arXiv、Socket、Microsoft、Decipher 等来源。

## 线索 1：Mastra / easy-day-js 不是普通 npm 投毒，而是 AI Agent 框架范围级投毒

**X 社区线索**

- Microsoft Threat Intelligence: https://x.com/MsftSecIntel/status/2067099387101335909
- Socket Security quoted by community accounts: https://x.com/SocketSecurity/status/2067134429462474854
- CyberAlertsHQ thread: https://x.com/CyberAlertsHQ/status/2067395599092375937
- Techgines thread: https://x.com/nxtgen579255/status/2067418549845676541

**回链来源**

- StepSecurity: https://www.stepsecurity.io/blog/mastra-npm-packages-compromised-using-easy-day-js
- JFrog: https://research.jfrog.com/post/easy-day-js/
- SafeDep: https://safedep.io/mastra-npm-scope-takeover-supply-chain-attack
- The Hacker News: https://thehackernews.com/2026/06/144-mastra-npm-packages-compromised-via.html
- Decipher: https://decipher.sc/2026/06/17/mastra-ai-hit-by-npm-compromise/
- GitHub disclosure issue: https://github.com/mastra-ai/mastra/issues/18045

**关键事实**

- 2026-06-17，攻击者在 Mastra AI framework 生态中批量加入 `easy-day-js` 依赖。
- 不同来源统计略有差异：140+、143、144 个包；共同点是影响范围覆盖 `@mastra/*` 多个核心包。
- `@mastra/core` 是高下载量核心包，X 社区和多篇报道提到接近百万级 weekly downloads；StepSecurity 统计暴露包合计 weekly downloads 超过 1.1M。
- 攻击窗口很短：StepSecurity 描述从 payload 上传到批量 publish 的窗口集中在 2026-06-17 01:01 UTC 之后，批量发布约 88 分钟。
- 关键技巧不是直接大改 Mastra 源码，而是新增一个看似无害的 typosquat production dependency。
- `easy-day-js@1.11.21` 先作为 clean bait 出现；之后 `1.11.22` 加入安装期执行逻辑。由于 semver caret 范围，新安装会解析到武器化版本。

**攻击链抽象**

1. 攻击者控制或滥用拥有发布权限的 npm 账号。
2. 先发布看起来干净的 typosquat 包，让包名、版本、元数据接近合法库。
3. 批量 republish AI framework 包，在生产依赖中加入该 typosquat 包。
4. 后续攻击版本加入安装生命周期执行逻辑。
5. 开发者或 CI 安装被污染的 Mastra 包时，包管理器自动解析并执行恶意依赖。
6. 第一阶段 loader 尝试拉取第二阶段模块，并在开发者主机或 CI runner 上寻找 LLM API key、cloud credential、CI/CD secret、wallet 等高价值凭据。

**为什么这对 AI Agent 项目特别危险**

Mastra 不是普通 UI 库，而是 AI agent、workflow、RAG pipeline、MCP server、memory、observability、deployment 的框架。安装环境经常天然带有：

- `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GOOGLE_API_KEY`
- GitHub / npm token
- cloud provider credentials
- database URL
- vector database key
- CI/CD secrets
- MCP server 配置和 agent memory 数据

攻击者不需要先突破生产环境，只要在开发者或 CI/CD 节点拿到这些凭据，就能进入更深的供应链和云控制面。

**Fulcrum 需要新增的检测面**

- `dependency_range_upgrade_trap`: clean bait version 被加入依赖，后续 range 自动解析到恶意 patch。
- `ai_framework_scope_mass_publish`: 同一 scope 多个包短时间批量发布。
- `prod_dependency_typosquat`: 新增生产依赖与高知名库名称相似。
- `install_lifecycle_execution`: 安装期生命周期脚本访问网络、写临时文件、创建后台进程。
- `ai_secret_context`: 安装发生在 AI framework / MCP / RAG / CI 环境，风险升级。
- `source_package_delta_small_payload_elsewhere`: 一阶包源码变化很小，真实 payload 位于新增依赖或远程第二阶段。

## 线索 2：Agent Skill 已经成为比 MCP server 更轻、更容易扩散的供应链入口

**X 社区线索**

- NVIDIA SkillSpector 传播帖: https://x.com/Cikyyy2/status/2067288610936881282
- SkillSpector 讨论: https://x.com/1clawAI/status/2067396883039834580
- PhantomSkill arXiv 传播: https://x.com/gastronomy/status/2067442029185949982
- MCP server 风险讨论: https://x.com/Layton_Gott/status/2067283225676841096

**回链来源**

- NVIDIA SkillSpector: https://github.com/nvidia/skillspector
- NVIDIA docs: https://docs.nvidia.com/skills/scanning-agent-skills
- Snyk ToxicSkills: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
- PhantomSkill / PoisonedSkills paper: https://arxiv.org/html/2604.03081v1
- Malicious Agent Skills in the Wild: https://arxiv.org/html/2602.06547v1
- Runtime-Verified Benchmark of Malicious Agent Skills: https://arxiv.org/html/2606.07131v1

**关键事实**

- NVIDIA SkillSpector 引用的研究规模：42,447 个 skills；26.1% 至少有一个 vulnerability；5.2% 显示 likely malicious intent；带 executable scripts 的 skills 更容易出问题。
- Snyk ToxicSkills 扫描 3,984 个 skills，发现 36.82% 至少一个 security flaw，13.4% 有 critical issue，人工确认 76 个含 malicious payload。
- Snyk 还观察到 malicious skill 常同时结合两类内容：可执行恶意逻辑与 prompt injection。其结论是 confirmed malicious skills 中 100% 有 malicious code pattern，91% 同时使用 prompt injection 技术。
- PhantomSkill / PoisonedSkills 提出 DDIPE：把恶意逻辑藏在 skill 文档里的代码示例、配置模板、初始化片段中，让 agent 在正常完成任务时“复用示例”而不是显式执行攻击指令。

**攻击链抽象**

1. 用户或团队从 marketplace、GitHub、zip、URL 安装一个 skill。
2. skill 描述看起来是正常能力扩展，例如 PDF 处理、Kubernetes 模板、邮件助手、代码生成辅助。
3. 文档中包含看似合理的示例、安装步骤、配置模板、隐藏指令或第三方内容 fetch。
4. agent 在执行任务时把文档视为权威上下文，复制示例、运行初始化逻辑或按模板生成代码。
5. payload 通过 agent 的工具空间执行：file write、shell、network、secret access、repo modification、cloud action。
6. agent 的推理层还可能被 prompt injection 预先“安抚”，降低对危险步骤的拒绝概率。

**被破坏的防御假设**

- “skill 是文档”不成立：skill 是 operational directive + code/template + dependency。
- “没有直接命令就安全”不成立：DDIPE 依赖的是 agent 复用示例的倾向。
- “静态代码扫描足够”不成立：需要同时看 prompt、工具权限、示例复用、运行时行为。
- “marketplace 安装比 npm 安装安全”不成立：skill marketplace 正处在 npm/PyPI 早期生态阶段。

**Fulcrum 需要新增的检测面**

- `skill_doc_code_reuse_risk`: skill 文档示例中包含外联、敏感路径、权限修改、持久化、shell、环境变量读取。
- `skill_prompt_injection_coupled_with_code`: 同一 skill 同时出现角色覆盖/安全绕过语言与可执行逻辑。
- `skill_third_party_content_fetch`: skill 指示 agent 从未验证 URL 拉取模板、脚本或规则。
- `skill_hidden_metadata_or_unicode`: markdown / yaml / json 中隐藏字符、注释层指令、frontmatter 混淆。
- `skill_permission_overreach`: skill 功能声明与请求权限不匹配。
- `skill_runtime_guard_gap`: 安装前扫描通过但运行时工具调用越权。

## 线索 3：MCP / Agent 风险正在从“恶意命令”转向“授权链异常”

X 上一个有价值的表述是：传统 EDR、WAF、IAM、防火墙可能都看不到问题，因为每一步都是“被授权”的：

- X 线索: https://x.com/TattedWorks/status/2067414776393957459

这和 Fulcrum 的设计目标很贴：不要只问某个 API call 是否合规，而要问“这个调用是否来自被污染的上下文、是否超出了原任务的可信范围、是否通过了异常任务链”。

**需要建模的授权链**

```text
untrusted input
-> agent planning
-> approved tool
-> allowed network / file / CI action
-> sensitive side effect
```

单点上每一步都可能被允许，组合起来才是攻击。

**Fulcrum 可以增加的链式特征**

- `source_to_action_distance`: 外部输入到高危动作之间隔了多少步。
- `authority_escalation_without_new_identity_proof`: 没有新增身份校验，但权限动作升级。
- `benign_tool_dangerous_context`: 工具本身白名单，但上下文来自 untrusted 或 semi-trusted。
- `allowed_egress_sensitive_payload`: 域名或 endpoint 被允许，但 body 中含 secret / token / repo content。
- `agent_rationale_mentions_safety_override`: agent 的中间 reasoning 或摘要中出现“忽略警告、测试环境、跳过验证”等语义。

## 这轮对防御项目的结论

Fulcrum 不应只做“payload 检测器”，而要升级为四层：

1. **制品层**：包、skill、MCP config、extension、workflow、tarball、release artifact。
2. **上下文层**：prompt、文档、issue、social mention、skill docs、tool metadata、memory。
3. **权限层**：shell、file、network、CI publish、account recovery、MCP stdio、cloud credential。
4. **任务链层**：从低信任输入到高权限副作用的路径。

Mastra/easy-day-js 告诉我们：AI 框架自身正在成为供应链目标。

SkillSpector / ToxicSkills / PhantomSkill 告诉我们：agent skill 是“可执行文档”，不能当普通 markdown。

X 社区授权链讨论告诉我们：未来很多攻击不是“越权调用”，而是“被污染上下文驱动的授权调用”。

## 已反哺样本

新增机器可读候选样本：

- `defensive-lab/intel-derived-sample-candidates-2026-06-18-07.jsonl`

覆盖：

- Mastra/easy-day-js 风格 typosquat dependency 投毒。
- semver range 自动升级陷阱。
- AI framework scope mass publish。
- agent skill 文档示例复用风险。
- prompt injection + malicious code 组合 skill。
- hidden metadata / Unicode skill。
- MCP / agent 授权链异常。
- runtime guard gap。

