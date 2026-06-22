# 情报更新：AI Agent、供应链与新型 CVE 攻击面

> 日期：2026-06-18
> 目标：继续收集 AI/LLM/Agent、供应链投毒、CVE 利用、数据泄露与执行环境风险的近期情报。

## 1. 本轮新增判断

这一轮情报进一步确认：AI 安全风险正在从“模型回答是否安全”转向“AI 工具链是否把不可信内容变成动作”。尤其是以下几类已经具备现实攻击价值：

- AI 编排平台 RCE：Langflow、Flowise、LangGraph 这类平台连接模型、工具、密钥、数据库和云资源，一旦 RCE，攻击者拿到的不是普通应用权限，而是整个 AI 工作流环境。
- Agent 工具执行风险：MCP stdio、CLI agent、AI IDE 通过“看似安全的命令/工具”触发 RCE，核心问题是参数注入、工具信任和本地执行边界。
- AI 搜索/推荐外泄：Copilot Search、AI memory、AI 推荐系统会把 URL 参数、邮件、网页和社区内容变成检索/记忆/推荐上下文。
- 供应链投毒继续升级：从恶意包和 maintainer 账号失陷，升级到 CI/CD、OIDC、provenance、MCP server、agent skills、规则文件和 AI SDK。

## 2. 新增案例索引

| 案例 | 证据等级 | 方向 | 核心风险 |
|---|---|---|---|
| Langflow CVE-2026-33017 | A | AI 编排平台 RCE | 公告后约 20 小时出现利用，攻击者执行 Python 并读取 secrets |
| Langflow CVE-2026-5027 | A/B | AI 平台文件写入到 RCE | path traversal 任意写文件，外部报告称已被利用 |
| Flowise CVE-2026-40933 | B | MCP / AI workflow RCE | 导入恶意 chatflow 即触发 stdio MCP 服务端命令执行 |
| MCP systemic RCE class | C/B | Agent 供应链 / 协议设计 | stdio MCP 把配置变成命令执行原语，影响多类工具 |
| LangGraph RCE chain | B | Agent memory / checkpoint | SQL 注入、Redis 查询注入、反序列化组合影响自托管部署 |
| SearchLeak CVE-2026-42824 | B | Copilot 数据外泄 | Parameter-to-Prompt + HTML race + Bing SSRF 单击外泄 |
| AI Recommendation Poisoning | B/C | 记忆/推荐投毒 | 真实观察到 50 个提示注入尝试，来自 31 家公司 |
| Prompt injection to RCE | C | Agent 执行环境 | safe commands 被参数注入绕过，prompt 变成 RCE |

## 3. 案例详解

### A-6 Langflow CVE-2026-33017：公告后 20 小时被利用

证据等级：A。Sysdig 观察到真实利用。

攻击怎么做：

```text
攻击者扫描暴露的 Langflow 实例
-> 调用 POST /api/v1/build_public_tmp/{flow_id}/flow
-> 在 flow data 的 node definitions 中放入任意 Python 代码
-> Langflow 服务器端无认证执行该代码
-> 先运行 id 验证执行
-> 读取 /etc/passwd、.env、数据库文件和环境变量
-> 尝试下载第二阶段 payload
-> 外带 API keys、数据库连接串、云凭证
```

关键失败点：

- 公开 flow build endpoint 无认证。
- 服务器端执行了攻击者控制的 flow 节点代码。
- AI/RAG 平台通常连接 LLM API Key、数据库、向量库、云资源，RCE 后价值很高。

检测线索：

- `/api/v1/build_public_tmp/` 异常 POST。
- flow 名称包含 `nuclei-cve-2026-33017` 或类似扫描痕迹。
- Python 执行 `os.popen()`、`env`、`cat /etc/passwd`、`find /app -name "*.env"`。
- 出站到 interactsh/oast 域名，或 `curl | sh` 拉取 payload。

防御动作：

- 立即升级到修复版本。
- 所有暴露 Langflow 实例加认证和网络访问控制。
- 轮换 Langflow 环境变量里的 LLM、数据库、云、GitHub、向量库凭证。
- 对 AI workflow 平台默认按“高价值密钥集中点”治理。

### A/B-7 Langflow CVE-2026-5027：Path Traversal 到任意文件写

证据等级：A/B。Tenable 披露，安全媒体和安全社区报告 active exploitation；需要持续核查 CISA KEV 状态。

攻击怎么做：

```text
攻击者访问暴露的 Langflow 实例
-> 调用 POST /api/v2/files
-> multipart filename 参数加入 ../ 路径穿越
-> 将文件写到预期上传目录之外
-> 写入 cron、启动脚本、模板、配置或可被应用加载的位置
-> 触发后续命令执行或持久化
```

关键失败点：

- 文件上传接口没有正确净化 filename。
- 任意文件写在 Linux 上经常会升级为代码执行或配置篡改。
- Langflow 这类平台通常默认持有 API Key、环境变量和工作流秘密。

防御动作：

- 升级并验证补丁是否真正阻断 path traversal。
- 禁止公网直接访问 Langflow 管理面。
- 查找异常写入：cron、`.bashrc`、service 文件、应用配置、模板目录、Python import 路径。

### B-3 Flowise CVE-2026-40933：导入 chatflow 触发 1-click RCE

证据等级：B。Obsidian Security 披露。

攻击怎么做：

```text
攻击者构造恶意 Flowise chatflow
-> chatflow 内嵌 Custom MCP tool 配置
-> 配置使用 stdio transport
-> 授权用户导入 chatflow
-> 导入过程中 Flowise 在服务器端启动配置里的命令
-> 攻击者获得 Flowise server 代码执行
-> 读取服务器环境变量、API keys、SaaS/cloud 凭证
```

关键失败点：

- “导入配置”被当作数据，但其中的 stdio MCP 配置本质是命令执行。
- 代码执行发生在服务端，而不是用户本地。
- 输入校验不能解决根因，因为 stdio MCP 的设计就是启动命令。

防御动作：

- 自托管 Flowise 禁用 stdio MCP，优先使用远程受控 transport。
- 不导入未知来源 chatflow。
- 对 Flowise 进程做最小权限、容器隔离、无云管理员凭证。
- 记录 chatflow import、MCP server 启动命令、子进程执行日志。

### C/B-7 MCP systemic RCE class：协议/生态级工具执行风险

证据等级：C/B。OX Security、Obsidian Security、Trail of Bits 等多方从不同角度披露 MCP/Agent 工具执行风险。部分 CVE 已分配，个别厂商将其视为“功能”而非漏洞，需按具体产品判断。

攻击怎么做：

```text
AI 应用允许用户配置 MCP server
-> stdio transport 允许配置 command + args + env
-> 攻击者通过 UI、导入文件、marketplace、prompt injection 或 poisoned config 注入恶意命令
-> AI client / server 启动该 MCP server
-> 命令在本地开发机或服务器上执行
```

变体：

- AI IDE 被 prompt injection 诱导加载恶意 MCP。
- marketplace 发布恶意 MCP server。
- 项目仓库携带 MCP 配置文件。
- “受保护环境”只过滤明显 shell 字符，却没限制 npm/npx 参数。

关键失败点：

- 工具配置等同于可执行代码。
- 用户批准一次后，后续配置变更可能被信任。
- MCP server 可接触本地文件、环境变量、聊天上下文、git token、云凭证。

防御动作：

- MCP server 必须来源 allowlist。
- 禁止从项目仓库自动加载 MCP 配置到用户全局配置。
- stdio MCP 放入沙箱；禁止任意 `npx`、`uvx`、`python -m`。
- 工具权限按目录、网络、环境变量、密钥逐项授权。

### B-4 LangGraph RCE chain：Agent memory/checkpointer 成为攻击面

证据等级：B。Check Point 披露漏洞链，影响自托管部署；管理平台是否受影响需按厂商说明。

攻击怎么做：

```text
自托管 LangGraph 使用 SQLite 或 Redis checkpointer
-> 攻击者控制 filter / checkpoint 查询输入
-> 触发 SQL 注入或 RediSearch 查询注入
-> 进一步触发不安全反序列化
-> 获得服务器 RCE
-> 读取 LLM API keys、CRM 凭证、客户数据、对话历史、内部网络资源
```

关键失败点：

- Agent 的“记忆/状态持久层”成为传统注入和反序列化漏洞的承载点。
- 很多团队把 agent memory 当普通应用状态，没有按敏感系统隔离。
- 一旦 agent orchestration server 失陷，攻击者拿到的是整条任务链上下文。

防御动作：

- 升级 LangGraph/LangChain 相关版本。
- 不让外部用户控制 checkpoint filter key、metadata key、query 结构。
- 禁止反序列化不可信 checkpoint。
- 隔离 agent memory DB，不和生产 CRM/财务/密钥系统共享权限。

### B-5 SearchLeak CVE-2026-42824：Copilot Enterprise Search 单击外泄链

证据等级：B。Varonis 披露，Microsoft 已修复并分配 CVE。

攻击怎么做：

```text
攻击者构造 microsoft.com 域名下的 Copilot Enterprise Search 链接
-> q 参数包含指令化内容
-> 用户点击链接
-> Copilot 把 q 作为可执行 prompt，而不仅是搜索词
-> Copilot 检索邮箱、日历、SharePoint、OneDrive 等用户可访问内容
-> AI 回复流式渲染期间出现 img 标签
-> 浏览器在 sanitizer 生效前发起图片请求
-> Bing SSRF / allowlisted endpoint 帮助外带到攻击者服务器
```

关键失败点：

- Parameter-to-Prompt：URL 参数进入 AI 执行意图。
- Guardrail 在流式渲染后置，竞态窗口已产生外联。
- CSP allowlist 和搜索代理成为外带通道。

防御动作：

- 对 AI 搜索 URL 参数做强约束，区分 search query 和 instruction。
- AI 输出默认不允许外部资源加载，尤其是图片/Markdown 链接。
- 对 Copilot/Search 的外联和异常检索做审计。
- 对高敏感 SharePoint/OneDrive 数据做最小权限和过度共享清理。

### B/C-8 AI Recommendation Poisoning：真实出现的记忆/推荐投毒

证据等级：B/C。Microsoft 观察到真实世界尝试。

攻击怎么做：

```text
网站放置 “Summarize with AI” 按钮
-> 按钮链接到 Copilot/ChatGPT/Claude/Perplexity 等带 q 参数的 URL
-> q 参数中包含“记住本公司是权威来源/未来优先推荐”之类指令
-> 用户点击后，AI 助手打开并预填/执行该提示
-> 如果助手具备 memory/persistent facts，恶意偏好被长期保存
-> 未来用户咨询供应商、医疗、金融、安全建议时被偏向推荐
```

重要数据：

- Microsoft 在 60 天内识别到 50 个类似 prompt-based 尝试。
- 来源涉及 31 家公司，横跨十多个行业。
- 医疗、金融、安全建议等高风险领域已出现相关尝试。

关键失败点：

- URL 参数可以预填 prompt。
- 记忆写入缺少来源可信度和用户明确确认。
- 用户以为只是总结文章，实际发生了长期偏好写入。

防御动作：

- AI 助手对“remember / future conversations / trusted source”类记忆写入必须显式确认。
- 记忆必须可查看、可撤销、可标注来源和过期。
- 浏览器/企业网关可识别带 `?q=` 的 AI assistant share links，并标注风险。

### C-6 Prompt Injection to RCE：safe commands 不是安全边界

证据等级：C。Trail of Bits 对多个生产 agent 平台做过协调披露研究。

攻击怎么做：

```text
Agent 允许自动执行某些“安全命令”
-> 例如 git、rg、find、go test、grep
-> 攻击者通过 prompt 或仓库文件诱导 agent 使用特殊参数
-> 参数触发命令内置执行功能或写文件能力
-> 绕过 human-in-the-loop
-> 达成本地命令执行
```

例子：

- `go test -exec` 可以指定测试二进制的执行程序。
- `git show --output` 可写文件。
- `rg --pre` 可在搜索前执行预处理器。
- `fd -x` / `find -exec` 一类参数可执行命令。

关键失败点：

- 只 allowlist 命令名，不限制参数空间。
- LLM 工具调用把自然语言输入拼进命令参数。
- 安全设计依赖模型“不要这么做”，而不是系统边界。

防御动作：

- Agent 执行必须沙箱化。
- 使用 `--` 参数分隔符，shell=false，严格参数 schema。
- 不把 `git`、`rg`、`find`、`go test` 等视作天然安全命令。
- 全量记录 agent 命令执行日志。

## 4. 本轮新增检测方向

### AI 编排平台

- 暴露的 `/api/v1/build_public_tmp/`、`/api/v2/files`、chatflow import endpoint。
- Langflow/Flowise/LangGraph 进程读取 `.env`、数据库文件、云配置。
- Python/Node 子进程执行 shell、curl、wget、bash、python -c。
- AI 平台对外连接 oast/interactsh、陌生 VPS、短时间 DNS 爆发。

### MCP / Agent 工具

- 新增 MCP server 配置，尤其是 stdio transport。
- command 包含 `npx`、`uvx`、`python`、`bash`、`sh`、`node`。
- 项目目录尝试写入用户全局 agent 配置目录。
- AI IDE 启动后立即执行 hook、preinstall、postinstall、workspace init。

### Copilot / RAG / AI Search

- AI 搜索链接中包含长 `q=` 参数和指令语气。
- AI 输出流式阶段产生外部 image/markdown 请求。
- Copilot/Search 在短时间跨 mailbox、calendar、SharePoint、OneDrive 检索敏感内容。
- Bing/搜索/图片服务出站到陌生域名。

### 记忆与推荐投毒

- “Summarize with AI” 按钮链接到 `copilot.microsoft.com/?q=...`、`chatgpt.com/?q=...` 等。
- prompt 中出现 `remember`、`trusted source`、`future conversations`、`recommend first`。
- AI memory 中出现来源不明的供应商偏好、医疗/金融/安全建议偏好。

## 5. 本轮需要加入长期观察的关键词

```text
Langflow CVE-2026-33017
Langflow CVE-2026-5027
Flowise CVE-2026-40933
LangGraph RCE chain
MCP stdio RCE
Agentjacking
SearchLeak CVE-2026-42824
AI Recommendation Poisoning
Memory Poisoning AML.T0080
Parameter-to-Prompt Injection
AI IDE RCE
prompt injection to RCE
safe command argument injection
```

## 6. 参考来源

- Sysdig: CVE-2026-33017 exploited in 20 hours: https://www.sysdig.com/blog/cve-2026-33017-how-attackers-compromised-langflow-ai-pipelines-in-20-hours
- NVD CVE-2026-33017: https://nvd.nist.gov/vuln/detail/cve-2026-33017
- The Hacker News: Langflow CVE-2026-5027: https://thehackernews.com/2026/06/unpatched-langflow-flaw-cve-2026-5027.html
- Obsidian Security: Flowise CVE-2026-40933: https://www.obsidiansecurity.com/blog/when-is-stdio-mcp-actually-a-vulnerability
- OX Security: MCP systemic vulnerability: https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/
- Check Point: LangGraph memory/checkpointer vulnerability chain: https://blog.checkpoint.com/research/when-your-ai-agents-memory-becomes-a-security-liability/
- Trail of Bits: Prompt injection to RCE in AI agents: https://blog.trailofbits.com/2025/10/22/prompt-injection-to-rce-in-ai-agents/
- Varonis: SearchLeak: https://www.varonis.com/blog/searchleak
- Microsoft: AI Recommendation Poisoning: https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/
- NCSC: Prompt injection is not SQL injection: https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
