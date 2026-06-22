# 情报更新：浏览器/邮件 Agent、NHI/OAuth 与多智能体委托风险

> Date: 2026-06-18
> Collection mode: logged-in X search for current community signals, then evidence backtracking to Apache Camel, CSA, Trail of Bits, Permiso, G Data, OX Security, Obsidian Security, CoSAI, Nango, WorkOS, Red Hat, Unit/identity sources.
> Safety: 本文只沉淀防御测试资料和样本结构，不包含可直接攻击真实系统的 exploit payload。

## 本轮补充范围

前面几轮已经覆盖 MCP、Agent skill、npm/model supply chain、RAG、SearchLeak。这一轮补 Agent 落地时最容易被忽视的“日常工作入口”和“身份/委托”：

1. 邮件 / 日历 / 协作平台里的间接 prompt injection。
2. AI 浏览器扩展和 agentic browser 的隔离问题。
3. OAuth / connector / 非人身份（NHI）带来的长期授权和权限漂移。
4. MCP OAuth confused deputy。
5. 多智能体委托和 A2A / agent-to-agent 权限传播。
6. Agent payments / x402 / AP2 带来的自动支付风险。

## 线索 1：邮件 Agent 是最自然、也最危险的间接注入入口

**X 线索**

- Email agent prompt injection discussion: https://x.com/cypher_hyd/status/2065162027665150314
- Apache Camel email triage agent post: https://x.com/ApacheCamel/status/2064574780368646190

**回链来源**

- Apache Camel email triage agent: https://camel.apache.org/blog/2026/04/email-triage-agent/
- Permiso Copilot email XPIA: https://permiso.io/blog/copilot-prompt-injection-ai-email-phishing
- Vectra prompt injection overview: https://www.vectra.ai/topics/prompt-injection
- Reddit user pattern: https://www.reddit.com/r/aiagents/comments/1spsidw/how_do_you_protect_autonomous_agents_that_read/

**关键风险**

邮件 agent 的典型流程是：poll Gmail/Outlook -> classify -> label -> draft reply -> summarize action items -> push notification。这里每一步都处理外部文本，而很多 demo/教程会把“自动移动、自动草拟、自动通知、自动标注”串成闭环。

攻击链抽象：

1. 攻击者发送一封正常业务邮件。
2. 邮件正文、签名、quoted text、HTML hidden text、附件名或 calendar invite 描述中含面向 agent 的指令。
3. Email agent 将邮件作为任务上下文，而不是不可信输入。
4. agent 自动分类、草拟回复、创建任务、通知协作平台或调用工具。
5. 结果可能是钓鱼内容被可信摘要放大、错误标签触发工作流、敏感信息被回复/转发/记录。

**Fulcrum 检测点**

- `email_body_as_untrusted_agent_context`
- `email_hidden_text_instruction`
- `agent_draft_reply_from_external_email`
- `mail_label_triggers_downstream_workflow`
- `calendar_invite_description_prompt_injection`

## 线索 2：AI 浏览器扩展正在直接偷 AI 对话和网页上下文

**X 线索**

- https://x.com/TweetThreatNews/status/2064977214345531648

**回链来源**

- G Data: https://blog.gdatasoftware.com/2026/06/38428-browser-addons-spy-on-ai-chats
- OX Security: https://www.ox.security/blog/malicious-chrome-extensions-steal-chatgpt-deepseek-conversations/
- The Hacker News: https://thehackernews.com/2026/01/two-chrome-extensions-caught-stealing.html
- Truesec: https://www.truesec.com/hub/blog/chrome-extension-steal-chatgpt-and-deepseek-conversations
- LayerX / BleepingComputer summary: https://www.bleepingcomputer.com/news/security/malicious-chrome-extensions-target-ai-users-to-steal-sensitive-data/

**关键事实**

- G Data 报告 Urban VPN、Smart Sidebar: ChatGPT/Claude/DeepSeek、AI Assistant / Chat AI 等扩展外表功能正常，但会收集 ChatGPT、Claude、Copilot、Gemini、DeepSeek 对话。
- OX / THN 报告两个冒充 AITOPIA 的扩展，合计约 900,000 installs，窃取 ChatGPT / DeepSeek conversations 和浏览数据。
- LayerX / BleepingComputer 报道 30+ 假 GenAI Chrome 扩展、300,000+ users，部分扩展能读取 Gmail email contents 与 draft messages。

**攻击链抽象**

1. 用户安装“AI sidebar / AI assistant / Chat with all models / VPN + AI helper”等扩展。
2. 扩展声明宽泛 host permissions、content scripts 或 remote iframe。
3. 用户打开 ChatGPT、Claude、Gemini、DeepSeek、Copilot 或企业内网页。
4. 扩展注入脚本、拦截请求、读取 DOM、使用隐藏 iframe 或远程逻辑更新。
5. prompts、responses、tabs、email contents、internal URLs、tokens 或 organizational structure 被外传。

**Fulcrum 检测点**

- `ai_chat_extension_dom_read`
- `extension_remote_code_or_iframe`
- `extension_reads_ai_domains_and_gmail`
- `browser_extension_featured_badge_not_trust`
- `prompt_poaching_interval_exfiltration`

## 线索 3：Agentic browser 的问题是继承登录态和缺少隔离

**回链来源**

- Trail of Bits: https://blog.trailofbits.com/2026/01/13/lack-of-isolation-in-agentic-browsers-resurfaces-old-vulnerabilities/
- CSA PleaseFix: https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_PleaseFix_agentic_browser_exploits_20260328-csa-styled.pdf
- Netwrix browser agent risks: https://netwrix.com/en/resources/blog/browser-agent-security-risks/
- OpenAI ChatGPT agent risk framing: https://openai.com/index/introducing-chatgpt-agent/

**核心问题**

Browser agent 不只是“会点网页的 LLM”，它继承浏览器的 cookie、登录态、表单、DOM、历史页面和跨站导航能力。传统安全模型默认“浏览器操作者是人”，但 agent 会把网页文本作为指令处理。

攻击链抽象：

1. 用户让 browser agent 打开页面或执行任务。
2. 页面中存在可见/隐藏 prompt injection、恶意 alt text、CSS 隐藏文本、OCR 文本或 injected DOM。
3. agent 按页面指令导航到另一个站点、读取当前页面内容、点击可信按钮、填表、下载文件或触发 connector。
4. 浏览器层的同源、CSP、cookie 安全假设并不保护“agent 解释并行动”的语义层。

**Fulcrum 检测点**

- `browser_agent_authenticated_session_inherited`
- `webpage_instruction_to_cross_site_action`
- `hidden_dom_or_ocr_instruction`
- `agent_clicks_privileged_ui_from_page_context`
- `browser_task_requires_origin_bound_policy`

## 线索 4：OAuth / connector / NHI 让 agent 拥有长期授权

**X 线索**

- Oracle Database MCP OAuth 2.0 streamable HTTP discussion: https://x.com/juarezjunior/status/2067353167663091829
- Box MCP connector / Harvey connector library: https://x.com/Box/status/2067276685960008023

**回链来源**

- Obsidian Security NHI guide: https://www.obsidiansecurity.com/blog/what-are-non-human-identities-nhi-security-guide
- CSA NHI governance vacuum: https://labs.cloudsecurityalliance.org/research/csa-whitepaper-nonhuman-identity-agentic-ai-governance-v1-cs/
- Nango AI agent API authentication: https://nango.dev/blog/guide-to-secure-ai-agent-api-authentication/
- Scalekit OAuth for AI agents: https://www.scalekit.com/blog/oauth-ai-agents-architecture
- Reco MCP SaaS risk: https://www.reco.ai/blog/model-context-protocol-mcp-is-rewiring-saas-trust-one-agent-action-at-a-time
- Box MCP server: https://www.box.com/mcp-server
- Harvey connector library: https://www.harvey.ai/blog/connector-library

**关键事实**

- NHI 覆盖 service accounts、OAuth apps、API keys、certificates、bots、AI agents。Obsidian Security 指出 NHI 在现代企业中常以 25-50x 数量超过人类身份，且 AI agent deployment 会继续加速。
- OAuth for AI agents 不是一次登录，而是长期 delegated authority。Refresh token、token exchange、client credentials、service accounts 会让 agent 在用户离线后继续行动。
- MCP / SaaS connector 宣称会继承现有权限控制，这是必要条件，但仍需要记录 agent 是“代表谁、为了什么任务、用什么 scope、访问了什么数据”。

**Fulcrum 检测点**

- `agent_refresh_token_long_lived`
- `connector_scope_exceeds_task`
- `service_account_owner_missing`
- `nhi_operates_after_user_session`
- `agent_api_call_bypasses_human_activity_logs`
- `connector_enforces_acl_but_lacks_intent_check`

## 线索 5：MCP OAuth confused deputy 是 agent 时代的核心身份问题

**回链来源**

- CoSAI RSAC MCP security: https://www.coalitionforsecureai.org/after-rsac-2026-the-mcp-security-question-everyone-kept-asking/
- Obot MCP security guide: https://obot.ai/resources/learning-center/mcp-security/
- NHI MG confused deputy: https://nhimg.org/community/nhi-best-practices/mcp-confused-deputy-risk-what-iam-teams-need-to-enforce/
- Apideck MCP security landscape: https://www.apideck.com/blog/understanding-the-security-landscape-of-mcp
- Gravitee MCP authorization: https://www.gravitee.io/blog/mcp-authorization-how-to-manage-permissions-for-ai-agents-services

**攻击链抽象**

1. MCP server 充当 OAuth proxy 或工具访问中介。
2. 多个客户端、用户、agent session 或 tool call 共享同一个 server。
3. server 没有把 authorization context 与当前请求、client、resource、user intent 强绑定。
4. 攻击者让 server 用另一个用户或更高权限上下文完成请求。
5. 凭据没有被偷走，但权力被错用。

**Fulcrum 检测点**

- `mcp_oauth_confused_deputy`
- `token_audience_or_subject_mismatch`
- `client_context_not_bound_to_resource`
- `delegated_scope_expands`
- `consent_screen_missing_tool_scope`
- `per_request_validation_missing`

## 线索 6：多智能体委托需要“权限交集”，不是权限相加

**X 线索**

- Agentic Resource Discovery / ARD: https://x.com/fr0gger_/status/2067480928667230696
- Agent payments / x402 community discussion: https://x.com/AdrianaCrosing/status/2067485242831856004

**回链来源**

- WorkOS delegation security: https://workos.com/blog/ai-agent-delegation-multi-agent-security
- Red Hat delegation beats impersonation: https://next.redhat.com/2026/05/21/zero-trust-for-ai-agents-why-delegation-beats-impersonation
- Authorization Propagation in Multi-Agent AI Systems: https://arxiv.org/html/2605.05440v1
- Token Security collaborative agents: https://www.token.security/blog/collaborative-ai-agents-securing-multi-agent-networks
- Palo Alto A2A risks: https://live.paloaltonetworks.com/t5/community-blogs/safeguarding-ai-agents-an-in-depth-look-at-a2a-protocol-risks/ba-p/1235996
- A2A security discussion: https://github.com/a2aproject/A2A/discussions/284

**关键风险**

- Agent A 委托 Agent B 时，B 可能拥有 A 没有的权限。
- Agent cards / capability descriptions 可能被污染。
- 共享 memory、shared workspace、delegation queue 会造成横向传播。
- 自动资源发现（tools / MCP servers / skills）会扩大 supply chain exposure。

**Fulcrum 检测点**

- `delegation_scope_not_intersection`
- `delegated_token_lacks_original_actor`
- `agent_card_context_poisoning`
- `shared_memory_cross_agent_poisoning`
- `auto_resource_discovery_untrusted_tool`
- `a2a_impersonation_or_peer_trust_failure`

## 线索 7：Agent payments 让 prompt injection 变成资金风险

**回链来源**

- Chainalysis x402 adoption: https://www.chainalysis.com/blog/x402-agentic-payments-adoption/
- RebelFi agent wallets risk: https://rebelfi.io/blog/why-ai-agents-need-crypto-wallets-and-what-that-means-for-payments-in-2026
- Galaxy x402: https://www.galaxy.com/insights/research/x402-ai-agents-crypto-payments
- Cobo AP2 guide: https://www.cobo.com/post/ap2-protocol-complete-guide-to-agent-payments-for-web3-developers-2026

**攻击链抽象**

1. Agent 被允许自动购买 API、数据源、compute、SaaS action 或 on-chain resource。
2. 外部 prompt、网页、email、tool response 或 malicious service 返回 payment request。
3. Agent 将其理解为完成任务所需步骤。
4. 如果没有 per-transaction policy，agent 可能向错误 merchant、sanctioned address、超额价格或 attacker-controlled endpoint 支付。

**Fulcrum 检测点**

- `agent_payment_request_from_untrusted_source`
- `payment_amount_exceeds_policy`
- `merchant_identity_unverified`
- `wallet_signing_without_user_intent`
- `payment_to_tool_access_chain`

## 已反哺样本

新增机器可读候选样本：

- `defensive-lab/intel-derived-sample-candidates-2026-06-18-09.jsonl`

覆盖：

- email body / hidden text prompt injection。
- calendar invite instruction injection。
- malicious AI browser extension chat theft。
- browser agent inherited session / cross-origin action。
- connector OAuth long-lived delegated authority。
- MCP OAuth confused deputy。
- NHI orphaned owner / service account drift。
- multi-agent delegation scope expansion。
- A2A agent card context poisoning。
- auto resource discovery untrusted tool。
- agent payment unauthorized transaction。
- connector ACL without intent check。

