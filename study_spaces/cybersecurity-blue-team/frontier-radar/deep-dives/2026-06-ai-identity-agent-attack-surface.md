# 深挖：AI、身份与 Agent 攻击面

> Last updated: 2026-06-18

## 一句话结论

AI 风险不是“模型会不会胡说”这么简单。更危险的变化是：AI 和 Agent 开始持有权限、调用工具、读取数据、连接 SaaS 和云平台；攻击者也用 AI 把侦察、凭证攻击、绕过和横向移动加速。

## 两条主线

| 主线 | 含义 | 典型风险 |
|---|---|---|
| AI 作为攻击加速器 | 攻击者使用 AI 提高效率 | 自动化侦察、脚本生成、凭证攻击、社工文案、日志规避 |
| AI/Agent 作为攻击面 | 企业自己的 AI 系统被攻击 | 提示词注入、工具滥用、RAG 数据泄露、Agent Token 被盗、MCP 工具越权 |

深度学习时要把这两条线分开，否则容易只停留在“AI 很危险”的泛泛判断。

## 攻击面分解

### 1. 数据入口

AI 系统读什么，就可能被污染什么：

- 用户输入。
- 网页内容。
- 邮件和 IM 消息。
- RAG 文档库。
- 工单、CRM、代码仓库、日志平台。
- 浏览器自动化读取的页面。

风险：

- 提示词注入隐藏在网页、文档、邮件里。
- RAG 检索把恶意指令带入上下文。
- 敏感资料被模型或插件返回到不该返回的位置。

### 2. 工具权限

Agent 能调用什么，就可能被诱导调用什么：

- 浏览器。
- 文件系统。
- Shell。
- 数据库查询。
- 邮件发送。
- Jira/飞书/Slack/CRM。
- 云控制台 API。
- MCP 服务。

风险：

- 用户看似只让 Agent 总结网页，网页却注入“读取本地密钥并发送”一类指令。
- 工具没有按任务隔离权限。
- Agent 持有长期 token，且缺少行为审计。

### 3. 身份与凭证

AI/Agent 让非人身份进一步膨胀：

- API Key。
- OAuth Refresh Token。
- 服务账号。
- CI/CD Token。
- 云角色。
- MCP Server 凭证。
- 浏览器登录态。

风险：

- 凭证长期有效。
- 权限大于任务需要。
- 行为混在正常自动化中，不容易被 SOC 识别。

## 攻击链模型

### 场景 A：提示词注入到工具滥用

```text
攻击者控制网页/文档内容
-> Agent 读取内容并把隐藏指令当作任务上下文
-> Agent 调用浏览器/文件/HTTP 工具
-> 敏感数据被读取或外发
-> 日志中表现为合法 Agent 行为
```

关键问题：

- Agent 是否区分用户指令、系统指令、网页内容、检索内容？
- 工具调用前是否需要权限确认？
- 工具有没有最小权限和作用域？
- 日志能否还原“是谁让 Agent 调了什么工具”？

### 场景 B：AI 开发平台或模型供应链被攻击

```text
开发者下载模型/插件/SDK
-> 依赖或模型文件携带恶意代码
-> 本地开发环境或 CI 环境执行
-> 窃取 GitHub Token / 云凭证 / npm Token
-> 攻击者进入供应链或云控制面
```

关键问题：

- 模型文件是否允许反序列化执行？
- CI/CD 是否持有过大的云权限？
- OIDC trust policy 是否限制 repo、branch、workflow？
- 开发环境密钥是否可被普通进程读取？

### 场景 C：Shadow AI 数据外泄

```text
员工把业务数据上传到未批准 AI 工具
-> 数据被第三方处理、留存或进入训练/日志
-> 敏感信息越过企业 DLP 和访问控制
-> 后续通过账户、浏览器插件或 API 再次泄漏
```

关键问题：

- 代理和网关能否识别 AI 工具流量？
- DLP 是否覆盖浏览器上传和 API 调用？
- 是否区分“批准 AI 工具”和“个人 AI 工具”？
- 是否有替代方案，否则员工会绕过限制。

## 检测思路

| 风险 | 可观察信号 |
|---|---|
| Agent 工具滥用 | 非预期工具调用、短时间跨系统访问、任务与工具不匹配 |
| Token 被盗 | 新地理位置、新 User-Agent、异常 API 调用、权限枚举 |
| Shadow AI | 上传大段代码/客户资料到未批准域名、AI API 调用激增 |
| RAG 数据泄露 | 检索敏感文档后马上外发、越权查询、异常导出 |
| AI 开发平台滥用 | 新建异常模型端点、运行未知 notebook、下载可疑模型/插件 |
| CI/CD 到云接管 | OIDC AssumeRole 异常、非主分支触发高权限部署、云管理员权限变更 |

## 防御设计原则

1. Agent 权限按任务授予，而不是按用户完整继承。
2. 工具调用要有审计日志，记录输入、决策、工具名、参数、结果摘要。
3. RAG 内容默认不可信，检索内容不能覆盖系统指令。
4. 高风险工具调用需要显式确认或策略审批。
5. Token 短期化、作用域最小化、按任务隔离。
6. 对 AI 工具建立允许清单和替代方案，单纯禁止通常会推动 Shadow AI。
7. CI/CD OIDC trust policy 必须限制组织、仓库、分支、workflow、环境。

## 学习实验

### 实验 1：Agent 权限清单

列出自己常用 AI 工具可能触达的资源：

```text
浏览器登录态：
本地文件：
代码仓库：
终端命令：
云账号：
Obsidian 笔记：
MCP 服务：
第三方 SaaS：
```

然后给每个资源标注：

```text
是否需要默认可用：
是否能只读：
是否需要二次确认：
日志在哪里：
token 多久过期：
```

### 实验 2：Shadow AI 排查

假设你是蓝队，设计 5 条发现 Shadow AI 的线索：

- 代理日志中的域名。
- DLP 命中。
- 浏览器插件安装。
- API Key 创建。
- 大文件上传。

### 实验 3：CI/CD OIDC 最小权限复盘

挑一个 GitHub Actions 到云平台的部署场景，检查：

- trust policy 是否限制 repo。
- 是否限制 branch/tag。
- 是否限制 workflow。
- 是否限制 environment。
- 云角色是否只能部署目标资源。

## 关联笔记

- [[20-AI安全与智能体安全/00-AI安全与智能体安全索引|20 AI安全与智能体安全]]
- [[20-AI安全与智能体安全/02-Agent攻击面与权限边界|Agent攻击面与权限边界]]
- [[20-AI安全与智能体安全/03-MCP与浏览器自动化安全|MCP与浏览器自动化安全]]
- [[20-AI安全与智能体安全/05-模型文件与供应链安全|模型文件与供应链安全]]
- [[15-蓝队专题/00-蓝队学习路线索引|15 蓝队专题]]

## 参考来源

- CrowdStrike 2026 Global Threat Report: https://www.crowdstrike.com/en-us/press-releases/2026-crowdstrike-global-threat-report/
- Verizon 2026 DBIR 新闻稿: https://www.verizon.com/about/news/breach-industry-wide-dbir-finds
- Google Cloud Cybersecurity Forecast 2026: https://cloud.google.com/security/resources/cybersecurity-forecast
- Unit 42 Threat Research: https://unit42.paloaltonetworks.com/
