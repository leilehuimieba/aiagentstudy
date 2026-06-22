# 优质网安资料源目录

> Date: 2026-06-18
> Goal: 为网络安全学习、威胁情报、检测工程、DFIR、攻防实验和 Fulcrum 测试数据提供高质量资料源。

## 快速结论

如果每天只能看少量来源：

1. **CISA KEV + CISA Alerts**：确认哪些漏洞已被真实利用。
2. **SANS ISC**：看当天互联网扫描、恶意样本、攻击噪声。
3. **The DFIR Report**：用真实入侵链学习检测和响应。
4. **MITRE ATT&CK + D3FEND**：把攻击行为和防御技术标准化。
5. **SigmaHQ + Atomic Red Team**：把 ATT&CK 技术转成检测和验证。
6. **PortSwigger Web Security Academy**：Web 漏洞体系化练习。
7. **M-Trends / DBIR / CrowdStrike / Unit 42 年报**：每季度/每年校准威胁趋势。

## 1. 官方与标准知识库

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| CISA KEV | S | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | 已被真实利用漏洞、修复期限、厂商链接 | 每日新增项映射到资产、补丁优先级和检测规则 |
| CISA Advisories | S | https://www.cisa.gov/news-events/cybersecurity-advisories | 联合通告、重大漏洞、攻击活动应急口径 | 用作事实确认与响应建议 |
| NVD | S | https://nvd.nist.gov/ | CVE 元数据、CVSS、CWE、受影响产品 | 补齐漏洞基础字段，不单独判断是否优先修 |
| MITRE ATT&CK | S | https://attack.mitre.org/ | 攻击战术、技术、过程、行为体映射 | 统一攻击链建模和检测覆盖矩阵 |
| MITRE D3FEND | S | https://d3fend.mitre.org/ | 防御技术知识图谱 | 把攻击技术映射到可落地防御手段 |
| MITRE CAPEC | S | https://capec.mitre.org/ | 攻击模式枚举 | 适合做威胁建模、测试用例和安全开发教育 |
| MITRE CWE | S | https://cwe.mitre.org/ | 软件弱点分类 | 适合代码审计、SAST 结果归一化和安全需求 |
| OWASP Top 10 | S | https://owasp.org/www-project-top-ten/ | Web 应用关键风险 | Web 安全路线基线，注意当前页面显示最新 released version 为 2025 |
| OWASP ASVS | S | https://owasp.org/www-project-application-security-verification-standard/ | 应用安全验证标准 | 适合安全需求、检查清单、测试覆盖 |
| OWASP WSTG | S | https://owasp.org/www-project-web-security-testing-guide/ | Web 安全测试方法 | 适合形成手工测试 SOP |
| OWASP API Security | S | https://owasp.org/www-project-api-security/ | API 风险与测试方向 | API 网关、BOLA、认证授权测试 |
| OWASP GenAI / LLM Top 10 | S | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | LLM/GenAI 风险框架 | AI 安全测试、Agent 风险分类 |
| OWASP LLMSVS | S | https://owasp.org/www-project-llm-verification-standard/ | LLM 应用验证标准 | 架构、模型生命周期、集成、监控检查 |

## 2. 年度趋势与一线威胁报告

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| Verizon DBIR 2026 | S | https://www.verizon.com/business/resources/reports/dbir/ | 全球数据泄露统计、入口变化、行业趋势 | 年度风险排序和安全投资依据 |
| Verizon DBIR 新闻摘要 | A | https://www.verizon.com/about/news/breach-industry-wide-dbir-finds | 2026 关键结论 | 注意 2026 报道称漏洞利用首次超过凭证窃取成为最大入口 |
| Mandiant M-Trends 2026 | S | https://cloud.google.com/security/resources/m-trends | 真实 IR 调查、攻击路径、检测趋势 | 用于应急和威胁狩猎基线 |
| CrowdStrike Global Threat Report 2026 | S | https://www.crowdstrike.com/en-us/global-threat-report/ | 攻击者画像、breakout time、AI 加速攻击 | 用于蓝队速度指标和身份/云检测建设 |
| Unit 42 Global Incident Response Report 2026 | S | https://www.paloaltonetworks.com/resources/research/unit-42-incident-response-report | 真实事件响应、身份、云、勒索趋势 | 用于入侵链和处置优先级 |
| Microsoft Digital Defense Report | S | https://www.microsoft.com/en-us/corporate-responsibility/cybersecurity/microsoft-digital-defense-report | 身份、云、国家级攻击、AI 风险 | 企业防御战略和身份治理 |
| Google TAG | A | https://blog.google/threat-analysis-group/ | 国家级攻击、间谍软件、0day 使用 | 高可信威胁行为体跟踪 |
| Google Project Zero | A | https://googleprojectzero.blogspot.com/ | 漏洞研究、浏览器/内核/供应链细节 | 深挖漏洞成因和补丁质量 |

## 3. Web / AppSec 学习与研究

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| PortSwigger Web Security Academy | S | https://portswigger.net/web-security | 免费 Web 安全体系课程和实验 | SQLi、XSS、SSRF、OAuth、GraphQL、Web Cache 等专项训练 |
| PortSwigger Research / Blog | A | https://portswigger.net/research | 新型 Web 攻击、HTTP request smuggling、cache poisoning | 高质量研究文章可转深挖笔记 |
| GitHub Security Lab | A | https://securitylab.github.com/ | 开源项目漏洞、CodeQL 查询、研究报告 | 代码审计和漏洞挖掘学习 |
| Bishop Fox Blog | A | https://bishopfox.com/blog | 红队、AppSec、云安全研究 | 学攻击链和工具化思路 |
| Trail of Bits Blog | A | https://blog.trailofbits.com/ | 软件供应链、形式化、安全工程、AI 安全 | 高质量工程型安全研究 |

## 4. 检测工程与蓝队规则库

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| SigmaHQ | S | https://github.com/SigmaHQ/sigma | 通用日志检测规则，3000+ 规则 | 作为跨 SIEM 检测规则基线 |
| Sigma resources | S | https://sigmahq.io/resources/ | Sigma 规范、工具、规则集合 | 学 detection-as-code |
| Elastic Detection Rules | A | https://github.com/elastic/detection-rules | Elastic Security 检测规则 | 参考 EQL / KQL 与规则测试 |
| Splunk Security Content | A | https://github.com/splunk/security_content | Splunk ESCU 检测规则 | 企业 SIEM 规则思路和 ATT&CK 映射 |
| The DFIR Report Sigma Rules | A | https://github.com/The-DFIR-Report/Sigma-Rules | 真实入侵报告衍生检测 | 从真实攻击链转检测规则 |
| YARA docs | S | https://yara.readthedocs.io/ | YARA 语法和规则编写 | 恶意样本分类和文件扫描 |
| Neo23x0 Signature Base | A | https://github.com/Neo23x0/signature-base/ | YARA / IOC / THOR 生态规则 | 参考成熟规则写法 |
| YARA Style Guide | A | https://github.com/Neo23x0/YARA-Style-Guide | YARA 规则风格和质量规范 | 避免低质量规则和误报 |
| Suricata Rules / ET Open | A | https://rules.emergingthreats.net/ | 网络 IDS 规则 | 网络层检测和 PCAP 练习 |
| Zeek | A | https://zeek.org/ | 网络安全监控框架 | 协议日志、威胁狩猎、网络取证 |

## 5. 对抗验证与实验

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| Atomic Red Team | S | https://www.atomicredteam.io/ | ATT&CK 技术的轻量模拟测试 | 验证 EDR / SIEM / 日志是否覆盖，必须在授权实验环境 |
| Caldera | A | https://github.com/apache/caldera | 自动化对抗模拟、红队/蓝队演练 | 构建实验环境，验证检测链 |
| MITRE adversary emulation resources | S | https://attack.mitre.org/resources/get-started/adversary-emulation-and-red-teaming/ | 对抗模拟方法论 | 设计红蓝对抗和检测覆盖验证 |
| AttackRuleMap | A | https://github.com/krdmnbrk/AttackRuleMap | Atomic Red Team 与开源检测规则映射 | 从“攻击模拟”找到“应触发检测” |
| Stratus Red Team | A | https://stratus-red-team.cloud/ | 云环境攻击技术模拟 | AWS/Azure/GCP 检测验证 |

## 6. DFIR / 应急响应与真实入侵复盘

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| The DFIR Report | S | https://thedfirreport.com/reports/ | 真实入侵链、日志证据、ATT&CK 映射、检测建议 | 每篇拆成“初始访问-执行-持久化-横移-影响-检测” |
| SANS Internet Storm Center | S | https://isc.sans.edu/ | 每日攻击趋势、样本、扫描、Stormcast | 每日 5-10 分钟态势输入 |
| Velociraptor | A | https://github.com/Velocidex/velociraptor | 端点取证、VQL、批量采集 | 应急响应和威胁狩猎工具 |
| CISA Velociraptor service page | S | https://www.cisa.gov/resources-tools/services/velociraptor | 官方认可的 Velociraptor 用途 | 端点可见性和取证采集说明 |
| Timesketch | A | https://timesketch.org/ | 时间线分析 | DFIR 事件线梳理 |
| Volatility Foundation | A | https://volatilityfoundation.org/ | 内存取证 | 恶意进程、凭证、内核对象分析 |

## 7. 云原生、供应链与安全工程

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| OpenSSF | S | https://openssf.org/ | 开源软件供应链安全 | SLSA、Scorecard、Sigstore 等体系入口 |
| SLSA | S | https://slsa.dev/ | 构建供应链完整性等级 | CI/CD 和制品来源验证 |
| Sigstore | S | https://www.sigstore.dev/ | 制品签名、透明日志 | 软件发布安全和 provenance |
| Chainguard Academy | A | https://www.chainguard.dev/unchained | 容器、SBOM、Wolfi、软件供应链 | 工程化防御实践 |
| Aqua Security Blog | A | https://www.aquasec.com/blog/ | 容器、Kubernetes、云原生威胁 | 云原生攻击与检测 |
| Wiz Research | A | https://www.wiz.io/blog/tag/wiz-research | 云漏洞、身份、暴露面 | 云安全深挖 |
| Socket.dev Blog | A | https://socket.dev/blog | npm / PyPI / supply chain 恶意包 | 依赖投毒和恶意包行为 |
| Snyk Blog | A | https://snyk.io/blog/ | 开源依赖、容器、IaC、AI supply chain | 开发安全治理 |

## 8. 实战训练和蓝队靶场

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| CyberDefenders | A | https://cyberdefenders.org/ | SOC、DFIR、蓝队 CTF | 用真实日志和文件做调查练习 |
| LetsDefend | A | https://letsdefend.io/ | 模拟 SOC 告警调查 | 初中级蓝队训练 |
| Blue Team Labs Online | A | https://blueteamlabs.online/ | 蓝队题目、日志分析 | SOC/DFIR 手感训练 |
| Hack The Box Academy | A | https://academy.hackthebox.com/ | 红队、蓝队、云、Web 系统课程 | 体系化练习 |
| TryHackMe | B | https://tryhackme.com/ | 入门友好路线 | 基础与专项训练 |
| PortSwigger Academy | S | https://portswigger.net/web-security | Web 漏洞实验 | Web 漏洞首选 |
| DFIR Labs | A | https://thedfirreport.com/products/dfir-labs/ | 基于真实入侵数据的 DFIR 训练 | 高质量应急练习 |

## 9. 中文生态资料源

| 来源 | 等级 | 地址 | 适合收集什么 | 怎么用 |
|---|---|---|---|---|
| FreeBuf | B | https://www.freebuf.com/ | 中文安全新闻、漏洞复盘、经验文章 | 快速发现中文生态线索 |
| 先知社区 | B | https://xz.aliyun.com/ | Web 安全、代码审计、漏洞复现 | 技术细节较多，注意验证时效 |
| 绿盟科技博客 | A | https://blog.nsfocus.net/ | 威胁情报、漏洞通告、行业研究 | 中文企业防御视角 |
| 奇安信攻防社区 | A | https://forum.butian.net/ | 漏洞分析、实战技术 | 漏洞和攻防文章 |
| 360CERT | A | https://cert.360.cn/ | 漏洞预警、应急通告 | 中文应急补充 |
| 腾讯安全玄武实验室 | A | https://xlab.tencent.com/cn/ | 高质量漏洞和安全研究 | 深度研究 |

## 10. 建议的资料处理流程

### 漏洞类

```text
CISA KEV / NVD / 原厂公告
-> 是否真实利用
-> 影响资产和版本
-> 攻击前置条件
-> exploit maturity
-> 检测证据
-> 缓解与补丁
-> 本地资产映射
```

### 攻击链类

```text
The DFIR Report / Mandiant / Unit 42 / CrowdStrike
-> 初始访问
-> 执行
-> 持久化
-> 权限提升
-> 横向移动
-> 影响 / 外泄
-> ATT&CK 映射
-> Sigma / YARA / SIEM 规则
-> Atomic / Caldera 验证
```

### 学习训练类

```text
PortSwigger / CyberDefenders / LetsDefend / HTB
-> 主题
-> 前置知识
-> 实验环境
-> 关键观察点
-> 日志证据
-> 复盘问题
```

## 11. 适合转成 Fulcrum / 检测样本的方向

- CISA KEV：`cve_priority_sample`、`known_exploited_vulnerability_routing`。
- ATT&CK + D3FEND：`attack_technique_to_countermeasure_mapping`。
- The DFIR Report：`real_intrusion_chain_detection_gap`。
- SigmaHQ：`expected_detection_rule_hit`。
- Atomic Red Team：`simulation_to_detection_validation`。
- PortSwigger：`web_vulnerability_lab_case`。
- OWASP ASVS / WSTG：`security_requirement_to_test_case`。
- OpenSSF / SLSA / Sigstore：`artifact_provenance_policy_case`。
- Velociraptor：`dfir_artifact_collection_case`。

