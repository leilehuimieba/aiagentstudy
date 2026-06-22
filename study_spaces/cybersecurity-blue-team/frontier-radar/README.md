# 前沿风险雷达

> Scope: 跟踪网络安全领域最新风险、挑战、漏洞利用趋势和防御优先级。
> Last updated: 2026-06-18

这个目录用于承接“最新网络安全风险”的持续收集，不和基础学习路线混在一起。它更像一个雷达台：先看高可信来源，再把信号转成学习主题、检测思路和复盘问题。

## 目录

- [高价值来源清单](source-watchlist.md)
- [2026-06-18 前沿网安风险简报](2026-06-18-frontier-risk-brief.md)
- [前沿风险深度分析框架](deep-analysis-framework.md)
- [深挖：漏洞利用窗口压缩与风险优先级重构](deep-dives/2026-06-vulnerability-exploitation-window.md)
- [深挖：AI、身份与 Agent 攻击面](deep-dives/2026-06-ai-identity-agent-attack-surface.md)
- [深挖：CVE 分析工作台](deep-dives/2026-06-cve-analysis-workbench.md)
- [深挖：供应链投毒攻击链与实例](deep-dives/2026-06-supply-chain-poisoning-cases.md)
- [深挖：从 OWASP Web Top 10 到 LLM / Agent 威胁](deep-dives/2026-06-from-owasp-web-to-llm-agent-threats.md)
- [深挖：AI 威胁共识地图与案例库](deep-dives/2026-06-ai-threat-consensus-and-casebook.md)
- [情报更新：AI Agent、供应链与新型 CVE 攻击面](intel-updates/2026-06-18-ai-agent-supply-chain-threat-intel-02.md)
- [情报更新：AI Gateway、MCP、Copilot 搜索与供应链反扫描](intel-updates/2026-06-18-ai-agent-threat-intel-03.md)
- [情报更新：AI Coding Agent、Sentry MCP、Mastra 投毒与构建配置执行面](intel-updates/2026-06-18-ai-coding-agent-supply-chain-intel-04.md)
- [情报更新：MCP Tool Poisoning、恶意 MCP 服务与 AI 凭证窃取](intel-updates/2026-06-18-mcp-tool-poisoning-credential-theft-intel-05.md)
- [情报更新：社交媒体与开发者社区里的 Agent 安全线索扩展](intel-updates/2026-06-18-social-community-agent-threat-intel-06.md)
- [情报更新：X 社区线索里的 Mastra 投毒与 Agent Skill 供应链风险](intel-updates/2026-06-18-x-community-agent-skill-mastra-intel-07.md)
- [情报更新：MCP 运行时漏洞、SearchLeak、RAG 污染与模型仓库供应链](intel-updates/2026-06-18-mcp-rag-model-searchleak-intel-08.md)
- [情报更新：浏览器/邮件 Agent、NHI/OAuth 与多智能体委托风险](intel-updates/2026-06-18-agent-browser-email-identity-delegation-intel-09.md)
- [情报更新：AI Coding / DevOps Agent 安全债与持久记忆污染](intel-updates/2026-06-18-coding-devops-memory-poisoning-intel-10.md)
- [情报更新：KEV、边缘设备、供应链蠕虫、Agent Skill 与云日志规避](intel-updates/2026-06-18-cross-domain-threat-intel-11.md)
- [情报更新：非 X 来源采集 - GitHub Advisory、SecLists、Rapid7、DFIR 与扫描态势](intel-updates/2026-06-18-non-x-source-threat-intel-12.md)
- [情报更新：AI/Agent 开源组件、npm 投毒、PeopleSoft 零日与 SaaS 数据窃取](intel-updates/2026-06-18-ai-agent-open-source-saas-intel-13.md)
- [情报更新：传统漏洞与论坛线索 - Exim、HTTP/2 Bomb、HashiCorp、边缘设备与企业应用](intel-updates/2026-06-18-traditional-vuln-forum-intel-14.md)
- [防御实验室：AI / Agent 威胁样本库](defensive-lab/README.md)
- [Fulcrum 专用评测样本包](fulcrum-test-data/README.md)

## 收集原则

1. 官方优先：CISA KEV / BOD、NVD、MSRC、厂商安全公告用于确认“是否真实被利用、是否需要处置”。
2. 前线情报补充：Google Cloud / Mandiant、Unit 42、CrowdStrike、Cisco Talos、Microsoft、SANS ISC 用于理解攻击路径和趋势。
3. 社区媒体提速：BleepingComputer、The Hacker News、Dark Reading、FreeBuf、先知社区等用于发现线索，但重大结论要回链到官方或原厂公告。
4. 中文生态落地：绿盟、奇安信、安恒、腾讯安全、阿里云安全、360CERT、深信服千里目等用于观察国内攻防环境、产品侧经验和应急口径。
5. 每条风险至少记录：主题、来源、发布日期、影响资产、攻击条件、处置建议、可学习知识点、关联 Obsidian 模块。
6. 重要主题必须补“攻击链、检测证据、补丁前缓解、取证回溯、练习任务”，避免只做新闻摘录。

## 重点观察面

- 漏洞利用窗口压缩：公开披露到利用从“周/月”缩短到“天/小时”。
- 第三方软件与供应链：npm、CI/CD、OIDC、SaaS 集成、外包服务商成为高频入口。
- 身份与非人身份：服务账号、API Key、自动化角色、AI Agent 权限边界和长期凭证。
- AI 加速攻防：AI 辅助侦察、凭证盗取、绕过、提示词攻击、企业 Shadow AI 数据泄漏。
- 云与容器：Kubernetes、云日志规避、云控制面权限、跨租户和托管 AI 平台风险。
- 勒索与反取证：数据窃取、日志删除、备份破坏、恢复阻断。
- 边缘设备和浏览器：VPN、防火墙、SD-WAN、浏览器引擎、网络设备成为初始访问重点。

## Obsidian 对应位置

主阅读入口在：

`D:\webstudy\Notes\obsidian\黑曜石\网络安全\21-前沿风险雷达\00-前沿风险雷达索引.md`
