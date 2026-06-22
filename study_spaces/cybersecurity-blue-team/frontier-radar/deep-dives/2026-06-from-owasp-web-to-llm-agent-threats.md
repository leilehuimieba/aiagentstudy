# 深挖：从 OWASP Web Top 10 到 LLM / Agent 威胁

> Last updated: 2026-06-18

## 核心观点

传统 OWASP Web Top 10 仍然重要，但它主要描述“Web 应用如何被输入、认证、访问控制、组件和配置问题打穿”。现在新增的风险层在于：LLM 和 Agent 把“自然语言、检索内容、工具调用、模型供应链、非人身份和自动化执行”纳入了攻击面。

所以不是从 Web Top 10 完全替换到 LLM Top 10，而是变成：

```text
Web Top 10
+ API / 云 / 身份
+ 软件供应链
+ LLM / RAG / Agent / Tooling
```

## 威胁迁移图

| 传统 Web 视角 | LLM / Agent 视角 | 变化 |
|---|---|---|
| Injection | Prompt Injection / Tool Injection | 命令和数据边界更模糊 |
| Broken Access Control | Excessive Agency / Tool Misuse | Agent 可能代替用户越权行动 |
| Sensitive Data Exposure | Sensitive Information Disclosure / RAG 泄露 | 泄露可以通过回答、检索、总结发生 |
| Vulnerable Components | Model / Dataset / Plugin / Package Supply Chain | 组件扩大到模型、embedding、插件、MCP 服务 |
| Security Misconfiguration | Agent 权限、工具策略、系统提示词、检索边界配置错误 | 配置对象变成 AI 工作流 |
| SSRF / API Abuse | Agent 调用浏览器、HTTP、云 API、数据库 | LLM 可以主动发起工具请求 |
| Logging Failure | AI 决策链和工具调用不可审计 | 只留最终输出不够，需要工具调用日志 |

## OWASP LLM Top 10 2025 要点

OWASP GenAI Security Project 的 2025 LLM Top 10 包括：

1. Prompt Injection
2. Sensitive Information Disclosure
3. Supply Chain
4. Data and Model Poisoning
5. Improper Output Handling
6. Excessive Agency
7. System Prompt Leakage
8. Vector and Embedding Weaknesses
9. Misinformation
10. Unbounded Consumption

其中最值得和现实攻防结合的是：

- Prompt Injection：攻击者把恶意指令藏在网页、文档、邮件、RAG 内容里。
- Supply Chain：模型、数据集、依赖包、插件、MCP 服务、AI SDK 都可能被投毒。
- Excessive Agency：Agent 权限过大，能发邮件、执行命令、改工单、读数据库。
- Vector and Embedding Weaknesses：RAG 检索可能被投毒、越权或召回敏感文档。
- Unbounded Consumption：通过长上下文、循环任务、昂贵工具调用制造成本型 DoS。

## OWASP Agentic Applications 2026 的意义

Agentic AI 的核心变化是：系统不再只是“回答”，而是“计划、调用工具、执行动作”。这让威胁从内容安全变成了操作安全。

Agent 风险可以简化成五个问题：

```text
目标是否会被劫持？
工具是否会被滥用？
身份和权限是否过大？
供应链是否可信？
执行代码是否可控？
```

## 大模型威胁的攻击链模型

### 1. Prompt Injection 到数据泄露

```text
攻击者控制网页/文档
-> RAG 或浏览器 Agent 读取内容
-> 恶意指令混入上下文
-> Agent 检索内部文档
-> 输出敏感摘要或通过工具外发
```

防御：

- 把外部内容标记为不可信数据。
- 检索结果不能覆盖系统指令。
- 敏感文档需要行级/文档级访问控制。
- 输出前做 DLP 和策略检查。

### 2. Improper Output Handling 到传统漏洞

```text
LLM 生成 HTML/SQL/Shell/代码
-> 下游系统未验证直接执行
-> XSS / SQL 注入 / 命令执行 / SSRF
```

这里传统 OWASP Top 10 又回来了：LLM 输出不是可信代码，仍然要转义、参数化、沙箱和权限隔离。

### 3. Supply Chain 到 Agent 接管

```text
恶意 AI SDK / MCP Server / 插件 / 模型文件
-> 开发者或 Agent 环境安装
-> 读取本地配置和 token
-> 注册新工具或改写工具行为
-> 诱导 Agent 调用恶意工具
```

防御：

- AI SDK、MCP Server、模型文件进入企业前必须做 SBOM/AIBOM 和安全审查。
- 工具注册需要审批，不能让 Agent 动态加载任意工具。
- 模型文件避免危险反序列化格式，隔离加载环境。

### 4. Excessive Agency 到业务破坏

```text
用户要求 Agent 完成业务任务
-> Agent 读取邮件/CRM/云控制台
-> 被间接提示词注入诱导
-> 执行删除、转账、发信、改权限等动作
```

防御：

- 高风险动作必须二次确认。
- 工具按任务授权，不继承用户全部权限。
- 所有工具调用记录：调用原因、参数、结果、触发来源。

## 你后续应该怎么学

不要把大模型安全学成“提示词大全”。建议按四层学习：

1. 应用层：Prompt Injection、RAG 越权、输出处理、数据泄露。
2. 工具层：Agent 工具权限、MCP、浏览器自动化、数据库/云 API 调用。
3. 供应链层：模型、数据集、SDK、npm/PyPI、插件、CI/CD。
4. 治理层：AI 资产清单、Shadow AI、日志审计、红队测试、AIBOM。

## 检测清单

| 风险 | 日志/证据 |
|---|---|
| Prompt Injection | 外部内容触发异常工具调用、回答含系统指令片段 |
| RAG 越权 | 用户查询召回无权限文档、跨部门文档命中 |
| Tool Misuse | Agent 在任务无关场景调用 Shell/HTTP/邮件/云 API |
| Agent Token 滥用 | 非预期 IP、非预期时间、短时间跨系统访问 |
| AI Supply Chain | 新增未知 MCP Server、AI SDK、模型文件、插件 |
| Cost DoS | token 使用量异常、循环工具调用、长上下文滥用 |

## 参考来源

- OWASP Top 10 for LLM Applications 2025: https://genai.owasp.org/llm-top-10/
- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP LLM Project background: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- CrowdStrike 2026 Global Threat Report: https://www.crowdstrike.com/en-us/press-releases/2026-crowdstrike-global-threat-report/
