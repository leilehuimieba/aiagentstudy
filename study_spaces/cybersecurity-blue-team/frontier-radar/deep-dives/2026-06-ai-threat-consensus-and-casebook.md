# 深挖：AI 威胁共识地图与案例库

> Last updated: 2026-06-18
> 目标：把“大家都在说 AI 安全危险”拆成可分析、可检测、可复盘的具体攻击面。

## 0. 先给结论

当前比较有共识的 AI / LLM / Agent 安全方向，不是单一的“提示词注入”，而是一组互相叠加的攻击面：

1. 输入端与上下文污染：攻击者污染用户输入、网页、邮件、文档、RAG 语料、长期记忆。
2. 大模型交互风险：提示词注入、越狱、系统提示词泄露、误导性输出、过度信任。
3. 攻击调用风险：Agent 被诱导调用邮件、浏览器、数据库、云 API、账号恢复、支付等工具。
4. 执行环境风险：AI IDE、MCP Server、插件、代码执行沙箱、浏览器自动化、CI Runner 被滥用。
5. 供应链风险：npm/PyPI、模型文件、AI SDK、MCP Server、插件、Agent skills、规则文件被投毒。
6. 数据泄露风险：RAG 越权、M365/SharePoint/OneDrive/邮件上下文泄露、工具返回外发。
7. 任务链异常：Agent 目标被劫持、任务步骤偏移、多 Agent 级联失败、人类过度信任。
8. AI 写代码漏洞：AI 生成不安全代码、推荐恶意依赖、引入过宽权限、生成错误修复。
9. 身份与非人身份风险：Agent token、服务账号、OAuth refresh token、CI/CD OIDC、云角色过权。
10. 取证与治理盲区：只记录最终回答，不记录上下文来源、工具调用理由、权限链和数据流。

传统 OWASP Web Top 10 仍然重要，但现在要叠加 OWASP LLM Top 10 和 OWASP Agentic Applications Top 10。Web 安全管“请求如何进入应用”，LLM/Agent 安全还要管“上下文如何影响决策，工具如何执行动作，身份如何被继承，记忆如何长期改变行为”。

## 1. 共识方向地图

| 方向 | 本质问题 | 典型攻击 | 主要防御 |
|---|---|---|---|
| 输入端上下文污染 | 模型无法天然区分可信指令和不可信数据 | 直接/间接 prompt injection、RAG 投毒、网页隐藏指令、记忆投毒 | 上下文分级、来源标注、检索隔离、记忆写入审批 |
| 大模型交互风险 | 对话看似自然，但可能改变策略或泄露敏感信息 | 系统提示词泄露、越狱、过度信任、误导输出 | 不把系统提示词当秘密边界；输出校验；高风险回答限制 |
| 攻击调用风险 | Agent 能调用真实工具，攻击从“说错”变成“做错” | 邮件外发、账号恢复、云 API 调用、支付/删除/改权限 | 工具最小权限、动作二次确认、策略引擎、工具调用审计 |
| 执行环境风险 | AI 工具运行在开发机/浏览器/CI 环境，拥有本地权限 | MCP RCE、AI IDE 配置注入、恶意 repo、沙箱逃逸 | 隔离运行、工作区信任、只读默认、禁用自动执行 |
| 供应链风险 | AI 应用依赖模型、插件、SDK、包、MCP、数据集 | npm/PyPI 投毒、模型文件恶意载荷、恶意 MCP Server、规则文件后门 | 私有 registry、SBOM/AIBOM、依赖审查、签名加行为分析 |
| 数据泄露风险 | LLM 能聚合跨系统上下文，泄露路径更隐蔽 | M365 Copilot 泄露、RAG 越权、图片/Markdown 外带、Bing/搜索代理外带 | DLP、输出沙箱、外联控制、权限裁剪、检索权限同步 |
| 任务链异常 | 长任务、多步骤、多 Agent 中某一步被污染后级联 | Goal hijack、tool misuse、cascading failure、rogue agent | 任务状态机、步骤级审批、回滚点、异常分支检测 |
| AI 写代码漏洞 | 生成代码功能正确但安全性不足 | SQLi、XSS、命令注入、认证缺陷、insecure deserialization | 安全提示模板、SAST/DAST、依赖扫描、代码审查门禁 |

## 2. 证据等级

| 等级 | 含义 |
|---|---|
| A | 真实在野或官方/原厂确认影响真实用户 |
| B | 生产系统漏洞被披露并修复，但未必确认在野利用 |
| C | 安全研究、PoC、红队实验，证明可行 |
| D | 趋势判断或厂商报告，适合纳入观察清单 |

## 3. 案例库

### A-1 Meta AI 支持机器人导致 Instagram 账号接管

证据等级：A，真实账号接管报道，多家媒体交叉报道，Meta 表示问题已处理。

攻击怎么做：

```text
攻击者选择高价值 Instagram 账号
-> 使用 VPN 模拟目标常见位置，降低风控触发
-> 与 Meta AI Support Assistant 对话
-> 要求把目标账号绑定到攻击者控制的新邮箱
-> AI 支持流程把验证码发到攻击者邮箱
-> 攻击者把验证码回填给机器人
-> 获得重置密码入口
-> 接管目标账号
```

为什么严重：

- 这不是模型“回答错”，而是 Agent 被授予了账号恢复动作。
- 身份验证被做成对话流程的一部分，而不是不可绕过的系统级前置条件。
- 攻击者没有控制原邮箱，也不需要传统密码突破。

防御启示：

- AI 客服不能成为身份验证的最终裁决者。
- 账号恢复、邮箱变更、密码重置等动作必须在模型外由确定性策略控制。
- 高价值账号需要强制人工复核、延迟生效、原邮箱/设备确认。
- 必须审计“AI 为什么触发了账号恢复动作”，而不是只记录聊天文本。

### B-1 EchoLeak：Microsoft 365 Copilot 零点击数据外泄

证据等级：B，生产系统漏洞，披露后修复；公开资料称无已知在野利用。

攻击怎么做：

```text
攻击者发送特制邮件
-> 邮件内容被 Copilot 纳入上下文
-> 间接 prompt injection 诱导 Copilot 搜索内部 M365 数据
-> Copilot 访问邮件、文档、SharePoint/OneDrive 上下文
-> 输出中嵌入外带路径
-> 数据被发送到攻击者控制位置
```

为什么严重：

- 用户不需要点击，AI 助手处理邮件上下文就可能触发。
- 攻击从“读一封邮件”升级为“跨内部知识库搜索并外带”。
- 本质是 LLM Scope Violation：模型越过用户意图，把内部上下文用于攻击者目标。

防御启示：

- 邮件、文档、网页进入 LLM 前必须标注为不可信内容。
- LLM 输出不能直接渲染外链、图片、Markdown 外带通道。
- Copilot/RAG 检索必须继承真实权限，并对跨源检索做审计。

### B-2 SearchLeak：Microsoft 365 Copilot 单击数据外泄链

证据等级：B，2026 年披露的 Copilot Enterprise 漏洞链，报道称已修复。

攻击怎么做：

```text
攻击者构造 Microsoft 365 / Copilot 相关链接
-> URL 参数携带 prompt-like 指令
-> 用户点击可信域名链接
-> Copilot/Search 按注入参数检索邮箱、日历、文件等数据
-> HTML 渲染竞态和 CSP 绕过让敏感结果进入外部请求
-> Bing/搜索链路被当作外带代理
```

为什么严重：

- 链路由多个小问题组成：参数注入、渲染时序、内容安全策略绕过、搜索代理外带。
- AI 与传统 Web 漏洞耦合后，影响面远大于单个 XSS/SSRF。

防御启示：

- AI 查询参数不能直接变成检索意图。
- 搜索结果渲染要做输出沙箱，禁止外部资源请求携带敏感内容。
- 对 AI 搜索链路做 egress 监控，而不是只监控传统浏览器页面。

### C-1 第三方 AI 聊天插件会话历史伪造与间接注入

证据等级：C，大规模研究，覆盖公开网站插件生态。

攻击怎么做：

```text
网站接入第三方 AI 聊天插件
-> 插件把会话历史从前端传给后端/LLM
-> 攻击者篡改请求中的会话历史
-> 伪造系统消息或更高优先级指令
-> 模型按伪造上下文回答或执行工具
```

另一路：

```text
插件抓取网站内容丰富上下文
-> 把商品评论、第三方内容、用户生成内容混入可信上下文
-> 攻击者在评论/页面中嵌入隐藏指令
-> 聊天机器人把不可信内容当作任务指令
```

防御启示：

- 会话历史必须服务端签名或服务端重建，不能信任前端提交的完整 history。
- Web 抓取内容需要来源分层：官方内容、用户评论、第三方嵌入必须分开。
- 工具调用必须验证调用来源和用户意图。

### C-2 WARP：用短评论污染 AI 搜索/推荐

证据等级：C，研究实验；对 AI 搜索与推荐系统有现实警示。

攻击怎么做：

```text
攻击者在 Reddit/论坛/问答站投放看似自然的短评论
-> AI 搜索/推荐系统检索到该评论
-> 模型把社区内容当作社会证明或推荐证据
-> 用户询问推荐时，AI 推荐攻击者指定产品/骗局/项目
```

为什么严重：

- 这是 SEO poisoning 的 AI 版本。
- 受污染的是 retrieval context，不一定是模型本体。
- 攻击者可以低成本影响“AI 给用户的建议”。

防御启示：

- 社区内容不能和权威来源同权重进入推荐。
- 推荐类答案要显示来源等级和证据冲突。
- 对突然出现、相似措辞、高度商业导向的 UGC 做降权。

### B/C-3 AI 记忆投毒与推荐投毒

证据等级：B/C，Microsoft 报告现实尝试；多项研究证明 memory poisoning 可行。

攻击怎么做：

```text
攻击者诱导用户点击“用 AI 总结/记住”某页面
-> 页面中包含隐藏的偏置信息或指令
-> AI 助手把它写入长期记忆/偏好/事实库
-> 之后用户询问供应商、产品、投资、医疗建议
-> AI 基于被污染记忆推荐攻击者指定对象
```

为什么严重：

- 投毒与触发可以相隔数天或数周。
- 工具调用没有违规；Agent 只是基于错误记忆做“正常”决策。
- 普通异常检测很难发现，因为单次行为看起来都合理。

防御启示：

- 记忆写入必须有来源、时间、可信度、过期时间和可撤销记录。
- 高风险偏好不能由网页/邮件自动写入长期记忆。
- 用户和管理员需要可审计、可清空、可回滚的 memory ledger。

### C-4 Unit 42 Bedrock Agent 长期记忆污染 PoC

证据等级：C，安全研究 PoC。

攻击怎么做：

```text
攻击者准备恶意网页/文档
-> 诱导用户让 Agent 阅读
-> 间接 prompt injection 写入 Agent 长期记忆
-> 未来用户执行订票、查询、取消等正常任务
-> Agent 调用工具时受污染记忆影响
```

防御启示：

- 长期记忆不是缓存，是权限边界。
- 外部内容不能直接写入长期记忆。
- 工具调用前要重新验证当前用户意图，而不是只依赖历史记忆。

### A-2 Axios npm 供应链投毒

证据等级：A，真实供应链事件，官方 post-mortem 与 Microsoft 分析。

攻击怎么做：

```text
维护者设备/账号被攻破
-> 攻击者发布 axios@1.14.1 和 axios@0.30.4
-> 恶意版本注入 plain-crypto-js@4.2.1
-> postinstall 阶段执行脚本
-> 下载跨平台 RAT
-> 开发者终端或 CI Runner 被控
-> 需要轮换本机/CI 中所有可能暴露的凭证
```

为什么严重：

- 应用源码逻辑几乎不变，恶意发生在安装期。
- 影响开发机和 CI/CD，可能进一步拿到 npm、GitHub、云凭证。

防御启示：

- lockfile 命中恶意版本后，应按终端/Runner 失陷处理。
- 对 install scripts 做默认阻断或高危审计。
- 发布必须采用 Trusted Publishing/OIDC/不可变 release，但仍需异常发布检测。

### A-3 Typosquatted npm 包窃取云与 CI/CD secrets

证据等级：A，Microsoft 披露 active campaign。

攻击怎么做：

```text
攻击者注册模仿 OpenSearch/Elastic/DevOps 的 npm 包
-> 伪造 repository/homepage/bugs metadata
-> 抬高版本号制造成熟项目假象
-> npm install 触发 preinstall
-> 收集主机信息并连接 C2
-> 下载第二阶段载荷
-> 窃取 AWS、Vault、GitHub Actions、npm token
-> 用 npm publish token 继续下游投毒
```

防御启示：

- 新依赖审查不能只看包名和 README，要看 maintainer、发布时间、install scripts、包大小、metadata 是否伪造。
- CI Runner 不应默认拥有 Vault、云、npm 发布权限。
- 监控 npm install 期间的异常外联、Bun/Node 子进程、IMDS/Vault/Secrets Manager 访问。

### A-4 QUIETVAULT / Nx 到 AWS 管理员

证据等级：A，一线事件响应报告。

攻击怎么做：

```text
Nx/npm 供应链感染
-> 恶意代码窃取开发者 GitHub PAT
-> 攻击者侦察 GitHub 组织和 Actions
-> 滥用 GitHub Actions OIDC 信任换取 AWS STS 凭证
-> 过权 CloudFormation 角色创建新 IAM role
-> 附加 AdministratorAccess
-> 少于 72 小时从开发者端点到 AWS 管理员
```

关键教训：

- OIDC 不是自动安全；trust policy 写宽就是无密码云接管通道。
- CI/CD 角色不能允许创建 IAM 管理员、附加管理员策略、修改自身权限边界。

### A-5 Mini Shai-Hulud / Miasma：worm 化供应链投毒

证据等级：A，一线威胁研究，多个生态受影响。

攻击怎么做：

```text
攻击者污染 CI/CD 或维护者账号
-> 发布大量恶意 npm/PyPI 包
-> install 阶段窃取 GitHub/npm/cloud/K8s/Vault/CI secrets
-> 使用窃取到的发布权限感染更多包
-> 通过有效 SLSA provenance 迷惑审查
-> 包管理生态帮助攻击扩散
```

关键教训：

- provenance 证明“由哪个流水线构建”，不证明流水线内部没有被污染。
- 供应链防御必须把签名、行为分析、权限隔离、Runner 临时化结合起来。

### C-5 Rules File Backdoor：AI 代码编辑器被项目规则诱导写入恶意代码

证据等级：C，安全研究，攻击面现实存在。

攻击怎么做：

```text
攻击者提交看似正常的项目配置/规则文件
-> 例如 .cursorrules、Copilot instructions、CLAUDE.md 等
-> 隐藏指令要求 AI 在生成代码时加入后门、弱校验或外联
-> 开发者相信 AI 生成代码并合并
-> 恶意逻辑进入供应链
```

为什么严重：

- 它不是直接 RCE，而是污染“代码生成过程”。
- 代码审查者可能只看功能，不知道 AI 是被规则诱导的。

防御启示：

- AI 规则文件要当作高风险代码审查对象。
- 对规则文件变更设置 CODEOWNERS 和安全审查。
- AI 生成代码必须经过 SAST、依赖扫描和敏感行为审查。

### C/B-6 AI IDE / MCP / Agent 执行环境 RCE

证据等级：B/C，多项报告和 CVE 指向 AI 开发工具的执行环境风险。

攻击怎么做：

```text
开发者打开攻击者控制的 repo 或工作区
-> 工作区包含恶意 AI 配置、MCP Server、hook 或符号链接/路径操控
-> AI coding agent 加载配置或被诱导复制文件
-> 覆盖自身配置或注册恶意工具
-> 重启/下一次工具调用时执行攻击者代码
```

典型形态：

- MCP Server 以工具名义获取本地文件、git token、云凭证。
- AI CLI/IDE 加载工作区配置时执行 hook。
- 恶意 repo 通过 README、规则文件、配置文件诱导 Agent 做“看似正常”的文件操作。

防御启示：

- 打开不可信 repo 时 AI Agent 默认禁用工具和本地执行。
- MCP Server 需要 allowlist、签名、来源审查和权限隔离。
- Agent 配置目录不可由项目工作区写入。

### D-1 AI 生成代码安全性不足

证据等级：D，厂商与研究报告趋势；适合纳入工程治理。

已观察问题：

- AI 代码语法正确率很高，但安全通过率明显不足。
- 常见漏洞仍是传统问题：SQL 注入、XSS、命令注入、日志注入、认证绕过、弱加密、路径遍历。
- 开发者如果只说“实现功能”，模型倾向给出功能优先代码。

攻击怎么做：

```text
开发者用 AI 快速生成接口/后台/脚本
-> 没有显式安全约束
-> 生成代码缺少输入校验、权限检查、参数化查询
-> 传统漏洞进入生产
-> 攻击者按 Web/API 常规方式利用
```

防御启示：

- AI 代码必须走同样的安全门禁，不能因“机器生成”降低审查。
- Prompt 中要显式要求安全边界，但不能只依赖 prompt。
- 建立 AI code review checklist：鉴权、授权、输入校验、输出编码、依赖、日志、错误处理、密钥处理。

## 4. 最近 CVE 与 AI/供应链的联系

近期 CISA KEV 里的漏洞分布说明：攻击入口正在从传统 Web 页面扩展到边缘设备、浏览器、网络管理面、文件传输和云/开发链路。

| CVE / 事件 | 资产类型 | 攻击含义 |
|---|---|---|
| CVE-2026-28318 SolarWinds Serv-U | 文件传输/边缘服务 | DoS 也能影响业务交换与应急噪声，需回溯 POST 和服务崩溃 |
| CVE-2026-20245 Cisco SD-WAN Manager | 网络管理面 | 低权限/本地认证条件后命令执行，影响网络控制面 |
| CVE-2026-11645 Chrome V8 | 浏览器/终端入口 | 浏览器是 SaaS、邮件、AI 工具和管理后台的入口 |
| CVE-2026-7473 Arista EOS | 网络设备/隧道 | 破坏分段和隧道边界假设 |
| CVE-2025-32711 EchoLeak | M365 Copilot | 生产 AI 助手的 prompt injection 可导致数据外泄 |
| CVE-2026-42824 SearchLeak | M365 Copilot/Search | AI 搜索与传统 Web 渲染/CSP/SSRF 链式组合 |
| CVE-2026-30615 Windsurf / AI IDE RCE 报告 | AI 开发工具 | 打开攻击者内容即可触发开发环境执行风险 |

## 5. 防御共识：不要追求“完全防住 prompt injection”

NCSC 的关键提醒是：Prompt Injection 不是 SQL Injection。SQL 可以通过参数化把命令和数据分开；LLM 在模型内部没有这种硬边界。因此防御重心要从“完美识别恶意指令”转向“降低被诱导后的影响”。

实用控制：

1. 权限最小化：Agent 不继承用户全部权限，按任务发放短期能力。
2. 工具分级：读、写、删、发信、转账、改权限分不同审批等级。
3. 上下文来源标注：用户输入、系统指令、网页、邮件、RAG、记忆分层。
4. 外联控制：LLM 输出不能直接触发图片/Markdown/URL 外带。
5. 记忆治理：长期记忆需要来源、过期、审批和回滚。
6. 执行隔离：AI coding agent、MCP、CI Runner 放在可销毁沙箱。
7. 供应链审查：AI SDK、模型、插件、MCP Server 和普通依赖一样纳入 SBOM/AIBOM。
8. 日志补齐：记录工具调用原因、参数摘要、上下文来源、权限身份、结果。

## 6. 后续持续收集字段

每个案例都按这个结构补：

```text
案例名称：
证据等级：A/B/C/D
方向：上下文污染 / 工具调用 / 执行环境 / 供应链 / 数据泄露 / 任务链 / AI写代码
发生时间：
来源链接：
受影响资产：
攻击前提：
攻击链：
关键失败点：
检测日志：
防御措施：
与 OWASP LLM/Agentic 的映射：
是否已有 CVE：
是否已在野利用：
还要验证的问题：
```

## 7. 参考来源

- Meta AI support bot / Instagram takeover: https://techcrunch.com/2026/06/01/hackers-hijacked-instagram-accounts-by-tricking-meta-ai-support-chatbot-into-granting-access/
- KrebsOnSecurity: https://krebsonsecurity.com/2026/06/hackers-used-metas-ai-support-bot-to-seize-instagram-accounts/
- 404 Media: https://www.404media.co/hackers-simply-asked-meta-ai-to-give-them-access-to-high-profile-instagram-accounts-it-worked/
- OWASP LLM Top 10 2025: https://genai.owasp.org/llm-top-10/
- OWASP Agentic Applications Top 10 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- NCSC: Prompt injection is not SQL injection: https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
- Microsoft AI Recommendation Poisoning: https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/
- Microsoft Axios npm compromise: https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/
- Axios post-mortem: https://github.com/axios/axios/issues/10636
- Microsoft typosquatted npm packages: https://www.microsoft.com/en-us/security/blog/2026/05/28/typosquatted-npm-packages-used-steal-cloud-ci-cd-secrets/
- Google Cloud Threat Horizons H1 2026: https://cloud.google.com/security/report/resources/cloud-threat-horizons-report-h1-2026
- Unit 42 npm threat landscape: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
- Unit 42 memory poisoning PoC: https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/
- Varonis SearchLeak: https://www.varonis.com/blog/searchleak
- EchoLeak paper: https://arxiv.org/html/2509.10540v1
- Third-party chatbot plugin prompt injection study: https://arxiv.org/abs/2511.05797
- WARP retrieval poisoning reporting: https://www.tomsguide.com/ai/a-13-word-reddit-comment-can-trick-ai-search-into-recommending-scams-researchers-find
- Veracode GenAI code security update: https://www.veracode.com/blog/spring-2026-genai-code-security/
