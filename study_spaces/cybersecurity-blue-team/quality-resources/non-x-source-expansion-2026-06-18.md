# 非 X 网安情报来源扩展

> Date: 2026-06-18
> Purpose: 后续收集不再依赖 X，改用更稳定、可验证、可回链的来源。

## 采集原则

1. **官方和原厂先确认事实**：CISA、NVD、CVE.org、MSRC、Cisco、Palo Alto、Check Point、GitHub Advisory Database。
2. **一线研究补攻击链**：Rapid7 ETR、The DFIR Report、Mandiant、Unit 42、Huntress、Sophos、Talos、Microsoft Threat Intelligence。
3. **互联网暴露和扫描态势补时间窗口**：GreyNoise、Shadowserver、SANS ISC、VulnCheck。
4. **开源供应链看专门源**：GitHub Advisory Database、Socket.dev、JFrog Security、OpenSSF、SLSA、Sigstore、Chainguard、Aqua Nautilus。
5. **邮件列表看早期披露**：SecLists Full Disclosure、oss-security、Openwall。
6. **社区内容只做线索**：Reddit、Hacker News、专业论坛可用于发现讨论，但入库前必须回链到公告、advisory、报告或代码仓库。

## 推荐来源分层

### Tier 0: 事实确认

- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- CISA Cybersecurity Advisories: https://www.cisa.gov/news-events/cybersecurity-advisories
- NVD: https://nvd.nist.gov/
- CVE.org: https://www.cve.org/
- GitHub Advisory Database: https://github.com/advisories
- SecLists Full Disclosure: https://seclists.org/fulldisclosure/
- Openwall oss-security: https://www.openwall.com/lists/oss-security/

### Tier 1: 攻击链和处置细节

- The DFIR Report: https://thedfirreport.com/reports/
- Rapid7 Emergent Threat Response: https://www.rapid7.com/blog/tag/emergent-threat-response/
- Unit 42: https://unit42.paloaltonetworks.com/
- Mandiant / Google Cloud Security: https://cloud.google.com/security/resources
- Huntress: https://www.huntress.com/blog
- Cisco Talos: https://blog.talosintelligence.com/
- SANS Internet Storm Center: https://isc.sans.edu/

### Tier 2: 扫描、暴露面和早期信号

- GreyNoise: https://www.greynoise.io/blog
- Shadowserver: https://www.shadowserver.org/news/
- VulnCheck: https://vulncheck.com/blog
- Censys Research: https://censys.com/blog/
- Shodan Blog: https://www.shodan.io/blog

### Tier 3: 供应链和开发者生态

- Socket.dev: https://socket.dev/blog
- JFrog Security Research: https://research.jfrog.com/
- OpenSSF: https://openssf.org/blog/
- SLSA: https://slsa.dev/
- Sigstore: https://www.sigstore.dev/
- Chainguard Academy / Blog: https://www.chainguard.dev/unchained
- Aqua Nautilus: https://www.aquasec.com/blog/
- Wiz Research: https://www.wiz.io/blog

### Tier 4: AI / Agent 安全

- GitHub Advisory Database AI/agent 相关 advisory: https://github.com/advisories
- Cloud Security Alliance AI Safety Initiative: https://labs.cloudsecurityalliance.org/
- OWASP GenAI Security Project: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP LLM Verification Standard: https://owasp.org/www-project-llm-verification-standard/
- Unit 42 AI Security: https://unit42.paloaltonetworks.com/
- Socket AI scanner / package research: https://socket.dev/blog

## 非 X 采集工作流

### 每日快速采集

1. CISA KEV / CISA Alerts：是否新增已利用漏洞。
2. GitHub Advisory Database：筛选 `type:reviewed severity:critical sort:updated-desc`，重点看 npm、pip、GitHub Actions、Go、Rust。
3. SANS ISC：看是否有新 exploit wave、Patch Tuesday、扫描异常。
4. Rapid7 ETR / GreyNoise：看是否出现 edge appliance、VPN、网关、RCE 的实际利用。
5. Socket / JFrog：看是否有恶意包、投毒、CI/CD token、registry compromise。

### 每周深度采集

1. 从 The DFIR Report、Unit 42、Mandiant、Huntress 选 2-3 个真实事件复盘。
2. 每个事件写清楚：初始访问、执行、持久化、横向移动、凭证、数据收集、外传、影响、检测证据。
3. 将事件拆成可测试样本：输入、信任边界、应阻断位置、应记录 telemetry。

### 每月来源复盘

1. 淘汰只转述新闻、没有原始证据的来源。
2. 提升能提供日志、时间线、检测规则、IoC、行为链的来源权重。
3. 单独维护“AI / Agent / MCP / 供应链”来源，因为这类风险变化速度快。

## 本轮新增关注点

- GitHub Advisory Database 对开源生态很有价值，尤其能捕捉恶意包、sandbox escape、AI/agent 组件漏洞。
- SecLists/Full Disclosure 适合发现厂商响应慢、补丁状态复杂或还未被主流媒体覆盖的 advisory。
- Rapid7 ETR 和 The DFIR Report 适合把 CVE 变成真实攻击链。
- GreyNoise / Shadowserver 不适合单独下结论，但适合判断“互联网上是否开始扫”和“暴露资产规模”。

