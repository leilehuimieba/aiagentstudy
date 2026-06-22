# 高价值网安信息源清单

> Last updated: 2026-06-18

## P0 每日监控

| 来源 | 地址 | 适合收集什么 | 使用方式 |
|---|---|---|---|
| CISA Known Exploited Vulnerabilities | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | 已被利用漏洞、修复期限、厂商处置链接 | 每日看新增 CVE，优先映射到本地资产 |
| CISA Alerts / News | https://www.cisa.gov/news-events/cybersecurity-advisories | 重大漏洞、联合通告、政府应急口径 | 作为事实确认来源 |
| CISA Binding Operational Directives | https://www.cisa.gov/news-events/directives | 漏洞修复优先级和治理要求 | 用于理解防御基线变化 |
| NVD | https://nvd.nist.gov/ | CVE 元数据、CVSS、CWE | 补齐漏洞基础信息 |
| MSRC Security Update Guide | https://msrc.microsoft.com/update-guide | Windows / Microsoft 产品补丁和利用状态 | 补丁日重点检查 |
| SANS Internet Storm Center | https://isc.sans.edu/ | 每日威胁、扫描趋势、端口活动、Handler 日志 | 早晨快速扫一遍 Diary 和 Stormcast |
| CERT/CC Vulnerability Notes | https://kb.cert.org/vuls/ | 多厂商漏洞协调披露 | 适合供应链和协议类漏洞 |
| CISA ICS Advisories | https://www.cisa.gov/news-events/ics-advisories | 工控、OT、医疗和工业设备漏洞 | 关注 OT/ICS 风险 |

## P1 每周复盘

| 来源 | 地址 | 适合收集什么 | 使用方式 |
|---|---|---|---|
| Verizon DBIR | https://www.verizon.com/business/resources/reports/dbir/ | 年度入侵数据、攻击入口、人因风险 | 每年建立趋势基线 |
| Google Cloud Security Blog | https://cloud.google.com/blog/products/identity-security | 云威胁、Mandiant / GTIG 情报、云控制面风险 | 云安全和供应链重点来源 |
| Mandiant M-Trends | https://cloud.google.com/security/resources/m-trends | 事件响应统计、攻击者 dwell time、初始访问 | 和应急响应模块联动 |
| Google Project Zero | https://googleprojectzero.blogspot.com/ | 高质量漏洞研究、浏览器/内核/供应链细节 | 深度漏洞学习 |
| Google TAG | https://blog.google/threat-analysis-group/ | 国家级攻击、间谍软件、0day 使用 | 威胁行为体跟踪 |
| Microsoft Security Blog | https://www.microsoft.com/en-us/security/blog/ | 身份、云、勒索、国家级攻击 | 企业防御视角 |
| Microsoft Digital Defense Report | https://www.microsoft.com/en-us/corporate-responsibility/cybersecurity/microsoft-digital-defense-report | 年度威胁趋势和防御建议 | 年度战略复盘 |
| CrowdStrike Threat Intelligence | https://www.crowdstrike.com/en-us/resources/reports/ | eCrime、国家级攻击、breakout time、身份攻击 | 速度和攻击者画像 |
| Palo Alto Unit 42 | https://unit42.paloaltonetworks.com/ | 最新威胁研究、云安全、AI 安全、勒索 | 前线案例和专题报告 |
| Cisco Talos | https://blog.talosintelligence.com/ | 恶意软件、漏洞、攻击活动 | 网络设备和恶意软件线索 |
| Cloudflare Radar | https://radar.cloudflare.com/ | DDoS、网络流量、互联网层趋势 | 宏观态势观察 |

## P2 社区和媒体线索

| 来源 | 地址 | 适合收集什么 | 使用方式 |
|---|---|---|---|
| BleepingComputer | https://www.bleepingcomputer.com/ | 勒索、泄露、漏洞新闻 | 快速发现事件 |
| The Hacker News | https://thehackernews.com/ | 漏洞、攻击活动、厂商通告聚合 | 发现线索后回查原文 |
| Dark Reading | https://www.darkreading.com/ | 企业安全新闻、研究解读 | 趋势观察 |
| KrebsOnSecurity | https://krebsonsecurity.com/ | 网络犯罪、地下生态、支付和身份攻击 | 深度事件背景 |
| Risky Business | https://risky.biz/ | 高质量安全新闻和播客 | 周度复盘 |
| GreyNoise Blog | https://www.greynoise.io/blog | 互联网扫描和利用噪声 | 判断漏洞是否被大规模扫 |
| Shadowserver | https://www.shadowserver.org/news/ | 暴露资产、僵尸网络、漏洞扫描数据 | 外部暴露面观测 |
| Censys Blog | https://censys.com/blog/ | 互联网资产暴露、证书和服务指纹 | 资产暴露研究 |

## P2.5 社交媒体与开发者社区线索

| 来源 | 地址 | 适合收集什么 | 使用方式 |
|---|---|---|---|
| X / Twitter 安全研究者搜索 | https://x.com/search | 漏洞披露前后的研究者动态、IOC 变体、受害者反馈、PoC 讨论热度 | 用 Kimi / OpenCLI 复用登录态；发现线索后回查原厂、研究报告或补丁链接 |
| Hacker News Security 讨论 | https://news.ycombinator.com/ | 开发者真实部署方式、误配置争议、早期工具链风险 | 作为“工程实践信号”，不单独作为事实结论 |
| Reddit /r/cybersecurity | https://www.reddit.com/r/cybersecurity/ | AI Agent、MCP、供应链、组织治理的一线讨论 | 观察风险共识和工具需求，重要内容回链到原始报告 |
| Reddit /r/netsec | https://www.reddit.com/r/netsec/ | 新工具、研究论文、检测脚本、技术讨论 | 用于发现检测思路和开源工具 |
| LinkedIn 安全研究者与厂商动态 | https://www.linkedin.com/ | 厂商复盘、CISO 视角、事件传播范围 | 只作为线索源，避免引用无法验证的营销结论 |
| GitHub Security Advisories / issues | https://github.com/advisories | 漏洞修复、issue 讨论、PoC 风险和真实影响范围 | 优先读取 advisory、commit、release note，不运行 exploit |

## 专题来源

| 专题 | 来源 |
|---|---|
| Web 与应用安全 | OWASP、PortSwigger Web Security Academy、GitHub Security Lab、Bishop Fox |
| 云原生与供应链 | Wiz、Aqua Security、Chainguard、Snyk、Socket.dev、Trail of Bits |
| AI 与 Agent 安全 | OWASP Top 10 for LLM Applications、Cloud Security Alliance AI guidance、Unit 42、Google Cloud、Microsoft、Anthropic / OpenAI 安全公告 |
| OT / ICS | Dragos、Claroty、Nozomi Networks、CISA ICS Advisories |
| 中文安全生态 | FreeBuf、先知社区、SecWiki、绿盟科技、奇安信攻防社区、360CERT、安恒信息、腾讯安全、阿里云安全、深信服千里目 |

## 采集模板

```text
标题：
来源：
发布日期：
原文链接：
可信度：官方 / 原厂 / 一线情报 / 社区线索
风险分类：漏洞利用 / 供应链 / 身份 / 云 / AI / 勒索 / OT / 社工
影响资产：
攻击条件：
为什么重要：
建议动作：
关联笔记：
后续要验证：
```
