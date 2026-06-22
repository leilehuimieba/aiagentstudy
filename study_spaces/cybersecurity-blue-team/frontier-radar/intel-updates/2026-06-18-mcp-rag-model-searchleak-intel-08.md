# 情报更新：MCP 运行时漏洞、SearchLeak、RAG 污染与模型仓库供应链

> Date: 2026-06-18
> Collection mode: logged-in X search for fresh leads, then evidence backtracking to NVD, GitHub Advisory, Varonis, CSA, Endor-linked summaries, Imperva, Acronis, Unit 42, arXiv, OWASP.
> Safety: 只记录防御测试所需的攻击链形状、信任边界、检测点和样本化字段，不记录可直接复用的 exploit payload。

## 这一轮补充了哪些面

前几轮主要覆盖 MCP tool poisoning、Agent skill、AI coding agent、npm / extension 供应链。这一轮补四个继续缺口：

1. MCP server 实现层漏洞：path traversal、command injection、code injection、public config secrets。
2. AI 搜索 / 企业 Copilot 外泄链：SearchLeak / CVE-2026-42824。
3. RAG / knowledge base 污染：检索池被少量恶意文档影响，进而控制输出或外泄。
4. 模型仓库 / AI/ML 文件供应链：Hugging Face、ClawHub、Pickle、模型 metadata、namespace reuse。

## 线索 1：MCP 实现层风险不是理论问题

**X 线索**

- https://x.com/NexusVoid_Ai/status/2067469007574454446
- https://x.com/1clawAI/status/2067356184378560938

**回链来源**

- PipeLab summary of 2026 MCP security state: https://pipelab.org/blog/state-of-mcp-security-2026/
- NVD CVE-2025-53967: https://nvd.nist.gov/vuln/detail/CVE-2025-53967
- GitHub Advisory GHSA-gxw4-4fc5-9gr5: https://github.com/advisories/GHSA-gxw4-4fc5-9gr5
- Imperva Framelink Figma MCP RCE: https://www.imperva.com/blog/another-critical-rce-discovered-in-a-popular-mcp-server/
- Endor Labs Framelink advisory write-up: https://www.endorlabs.com/learn/cve-2025-53967-remote-code-execution-in-framelink-figma-mcp-server

**关键事实**

- X 社区引用 Endor Labs 2026 扫描结果：2,614 个 MCP implementations 中，82% 使用易受 path traversal 影响的 file operation，67% 使用 code-injection-related APIs，34% 使用 command-injection-susceptible APIs。这一数据在 PipeLab 与多篇社区整理中被引用。
- Framelink Figma MCP Server before 0.6.3 存在 command injection / RCE，NVD 描述为通过 crafted HTTP POST 与 shell metacharacters 影响 `fetchWithRetry` curl 调用。
- GitHub Advisory 明确指出该类问题来自不安全使用 `child_process.exec`。

**对 Fulcrum 的样本价值**

MCP 风险要分成两层：

- `mcp_tool_metadata_risk`: tool description / schema / prompt 污染。
- `mcp_server_runtime_risk`: server 自身代码使用危险 API，处理用户输入时可触发 path traversal / command injection / SSRF / LFI。

Fulcrum 的样本不应只看“agent 是否被提示词骗了”，还要能判断“这个 MCP server 的实现是否让普通参数变成 shell / file / network 危险动作”。

## 线索 2：Sentry Agentjacking 说明外部遥测数据会变成 agent 指令源

**X 线索**

- https://x.com/TattedWorks/status/2067414772945948878

**回链来源**

- Tenet Security: https://tenetsecurity.ai/blog/agentjacking-coding-agents-with-fake-sentry-errors/
- CSA: https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/
- The Hacker News: https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html
- DevOps.com: https://devops.com/tenets-agentjacking-attack-turns-sentry-errors-into-code-execution/

**攻击链抽象**

1. Sentry DSN 是公开、设计上可嵌入前端的 write-only credential。
2. 攻击者向目标组织 Sentry project 写入伪造 error event。
3. error message / stack trace / breadcrumbs 中夹带面向 coding agent 的指令。
4. 开发者让 Claude Code、Cursor 或类似 agent “修复 Sentry issue”。
5. agent 把外部可写遥测事件当作可信调试上下文。
6. agent 生成或执行危险修复步骤，进而影响开发者机器或 repo。

**Fulcrum 检测点**

- `telemetry_as_prompt_source`: Sentry / logs / traces / APM events / customer feedback 被送入 agent。
- `public_write_credential_source`: DSN、webhook、support form 等允许外部写入。
- `agent_debug_fix_mode`: agent 进入“修复错误”模式时拥有 shell / file write / repo write。
- `external_error_event_to_tool_call`: tool call 因外部 error text 触发。

## 线索 3：SearchLeak / CVE-2026-42824 是企业 AI 搜索外泄链的代表

**X 线索**

- https://x.com/arstechnica/status/2066844176785039569
- https://x.com/so_sthbryan/status/2067463313521508682

**回链来源**

- Varonis: https://www.varonis.com/blog/searchleak
- Ars Technica: https://arstechnica.com/security/2026/06/critical-copilot-vulnerability-allowed-hackers-to-seal-2fa-code-from-users/
- Dark Reading: https://www.darkreading.com/application-security/copilot-searchleak-attack-1-click-data-theft
- The Hacker News: https://thehackernews.com/2026/06/one-click-microsoft-365-copilot-flaw.html
- TechRadar summary: https://www.techradar.com/pro/security/microsoft-365-copilot-can-be-turned-into-a-one-click-data-theft-tool-inbox-onedrive-and-sharepoint-data-all-at-risk-so-patch-now

**关键事实**

- Varonis 披露 SearchLeak：Microsoft 365 Copilot Enterprise Search 的 critical vulnerability chain，可在用户点击可信 Microsoft 链接后外泄 MFA codes、emails、calendar、OneDrive、SharePoint 等索引数据。
- 该链被公开报道为 CVE-2026-42824，Microsoft 已修复。
- 核心链路被多家报道总结为：parameter-to-prompt injection、HTML rendering race condition、CSP bypass via Bing SSRF / Search by Image。
- 重要点不是某一个 bug，而是“企业 AI search 按用户权限检索敏感内容，再在渲染层通过远程资源请求形成外泄”。

**Fulcrum 检测点**

- `param_to_prompt_injection`: URL 参数、搜索框、query suggestion 进入 prompt。
- `enterprise_search_sensitive_retrieval`: agent / Copilot 检索用户有权访问但当前任务不需要的敏感内容。
- `render_before_sanitize`: HTML / markdown / image URL 在净化前被处理。
- `trusted_domain_exfil_proxy`: 外泄经过 Microsoft / Bing / search service 这样的可信中介域。

## 线索 4：RAG 污染和 knowledge base 信任问题

**X 线索**

- https://x.com/subham11/status/2067431614771253285

**回链来源**

- WitnessAI RAG Security: https://witness.ai/blog/rag-security/
- Promptfoo RAG poisoning: https://www.promptfoo.dev/blog/rag-poisoning/
- Christian Schneider RAG security: https://christian-schneider.net/blog/rag-security-forgotten-attack-surface/
- LangProtect RAG leakage: https://www.langprotect.com/blog/rag-data-leakage-enterprise-knowledge-base
- Lyrie black-hole attack summary: https://lyrie.ai/research/research/rag-poisoning-black-hole-attack-vector-database-enterprise-ai

**关键事实**

- RAG 风险不是“模型被训练坏了”，而是检索层把恶意文档当成可信上下文。
- 多个来源引用 PoisonedRAG / black-hole 类研究结论：少量目标文档就能影响大规模知识库的检索结果，部分资料引用“五个文档在百万级知识库中达到 90%+ 或 97% 操控率”的研究结论。
- RAG 污染常和 prompt injection 组合：既影响“检索到什么”，又影响“LLM 如何解释检索结果”。

**Fulcrum 检测点**

- `retrieval_source_age_and_origin`: 新近加入、低可信来源、未经审核的检索文档。
- `retrieval_blackhole_dominance`: 少数文档在多个 query 上异常高频命中。
- `rag_instruction_in_content`: 文档正文含面向 agent 的指令，而非业务事实。
- `knowledge_base_write_to_tool_call`: RAG 内容驱动 file / network / policy write。
- `tenant_access_mismatch`: RAG 中心化索引绕过原数据源 ACL。

## 线索 5：模型仓库和 AI/ML 文件是新的软件供应链入口

**回链来源**

- Acronis: https://www.acronis.com/en/tru/posts/poisoning-the-well-ai-supply-chain-attacks-on-hugging-face-and-openclaw/
- CSA: https://labs.cloudsecurityalliance.org/research/csa-research-note-malicious-ai-model-repositories-attack-sur/
- CSO Online: https://www.csoonline.com/article/4169407/malicious-hugging-face-model-masquerading-as-openai-release-hits-244k-downloads.html
- Unit 42 Model Namespace Reuse: https://unit42.paloaltonetworks.com/model-namespace-reuse/
- Unit 42 AI/ML library RCE: https://unit42.paloaltonetworks.com/rce-vulnerabilities-in-ai-python-libraries/
- OWASP GenAI Supply Chain: https://genai.owasp.org/llmrisk/llm03-training-data-poisoning/
- ReversingLabs nullifAI: https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face

**关键事实**

- Acronis TRU 观察到 Hugging Face 与 ClawHub 被主动滥用于恶意模型 / skill 分发。
- CSO / Hive 等报道提到假冒 OpenAI release 的 Hugging Face repo 曾在 18 小时内成为 #1 trending 并达到 244K downloads。
- Unit 42 的 Model Namespace Reuse 研究说明：模型 namespace 可被复用，影响 Azure AI Foundry、Vertex AI、开源项目等模型加载场景。
- Unit 42 还披露 Apple、Salesforce、NVIDIA 开源 AI/ML Python libraries 的模型文件 metadata 加载 RCE 风险。
- ReversingLabs nullifAI 说明攻击者会利用模型文件格式、pickle / 压缩 / scanner evasion，绕过开发者对模型仓库的信任。

**Fulcrum 检测点**

- `model_repo_impersonation`: repo 名称、owner、card 文案冒充 OpenAI / Mistral / Meta / Anthropic 等品牌。
- `model_namespace_reuse`: model identifier 指向非预期 owner 或被重新注册 namespace。
- `unsafe_model_deserialization`: pickle / custom loader / `trust_remote_code` / unsafe metadata loader。
- `model_artifact_scanner_evasion`: 压缩、分片、延迟下载、scanner blind spot。
- `ai_marketplace_trending_as_trust_signal`: trending / downloads 被误当作安全背书。

## 已反哺样本

新增机器可读候选样本：

- `defensive-lab/intel-derived-sample-candidates-2026-06-18-08.jsonl`

覆盖：

- MCP path traversal / command injection 实现风险。
- public telemetry as prompt source。
- Sentry Agentjacking。
- SearchLeak-style enterprise AI search exfiltration。
- RAG black-hole poisoning。
- RAG instruction-bearing document。
- model repo impersonation。
- unsafe model deserialization。
- model namespace reuse。
- scanner evasion through packed model artifacts。
- AI marketplace trending trust abuse。
- least-privilege tool gating evidence model。
