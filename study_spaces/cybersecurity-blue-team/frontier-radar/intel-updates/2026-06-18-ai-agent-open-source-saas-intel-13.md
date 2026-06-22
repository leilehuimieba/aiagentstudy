# 情报更新：AI/Agent 开源组件、npm 投毒、PeopleSoft 零日与 SaaS 数据窃取

> Date: 2026-06-18
> Source policy: 非 X 来源；使用 GitHub Advisory Database、Microsoft Security、Google Cloud / Mandiant、Huntress 等可回链资料。

## 结论先行

本轮资料里最值得进入知识库的不是“又有几个 CVE”，而是四条可复用的攻防模式：

1. **AI/Agent 组件正在变成供应链入口**：PraisonAI、Guardrails AI、mistralai、PyTorch Lightning 这类组件同时出现在开发机、Agent runtime、模型服务和 CI 环境里，一旦包版本、插件安装或 MCP 工具边界出问题，影响面会穿透多个阶段。
2. **“安装/导入/插件注册”成为新执行面**：postinstall、import-time、Hub manifest、MCP `tools/call`、recipe/template loader、Python `.pth` 都是代码尚未进入业务逻辑前的执行边界。
3. **身份和 SaaS 数据面继续被攻击者工业化利用**：Mandiant 观察到 ShinyHunters-branded extortion 通过 vishing、SSO/MFA 凭据获取、MFA 设备注册进入 SaaS 平台，然后按权限机会主义外传数据。
4. **边缘入口 + 本地提权 + EDR 规避仍然高危**：Huntress 的 Nightmare-Eclipse 观察显示，疑似 VPN 初始访问后，攻击者会把本地提权工具放在用户可写目录，并进行 hands-on-keyboard 侦察。

## 1. GitHub Advisory: PraisonAI MCP 文件处理到 RCE

### GHSA-9mqq-jqxf-grvw / CVE-2026-44336

- Source: GitHub Advisory Database.
- Evidence: https://github.com/advisories/GHSA-9mqq-jqxf-grvw
- Affected: `PraisonAI <= 4.6.33`
- Patched: `4.6.34`
- 关键点：
  - PraisonAI MCP server 默认注册多个文件处理工具。
  - MCP `tools/call` 参数进入路径/文件名处理时缺少 containment check。
  - Advisory 描述攻击者可走出预期目录并写入运行用户可写位置；如果写到 Python site-packages 里的 `.pth`，后续 Python 进程可能被触发。
  - 触发面包括 MCP-connected LLM、未加 API key 的 http-stream、stdio MCP 中可到达 LLM 的提示注入。

### GHSA-9cr9-25q5-8prj: incomplete fix

- Source: GitHub Advisory Database.
- Evidence: https://github.com/advisories/GHSA-9cr9-25q5-8prj
- 关键点：
  - 原修复不完整，仍有工具参数路径处理问题。
  - 这是“补丁覆盖缺口”样本：修复一个 handler 不等于修复所有等价 sink。

防御测试价值：

- 对 MCP 工具参数做 schema 校验之外，还要做路径归一化、目录 containment、绝对路径拒绝、符号链接/重解析点处理。
- 对 Agent runtime 要记录“哪个工具、哪个参数、哪个路径、由哪个模型上下文触发”。
- 修复验证不能只复测一个 PoC，要枚举同类 handler、同类参数和同类 helper。

## 2. GitHub Advisory: Guardrails AI Hub 安装机制代码注入

- Source: GitHub Advisory Database.
- Evidence: https://github.com/advisories/GHSA-r6hf-g5x6-7pv9
- CVE: `CVE-2026-31233`
- Affected: `guardrails-ai <= 0.6.7`
- 关键点：
  - Guardrails Hub 安装 validator package 时从 Hub 拉取 manifest。
  - manifest 中 `post_install` 字段指定脚本路径。
  - 脚本路径来自不受信任 manifest 数据，执行前缺少充分校验，导致安装恶意包时可执行代码。

防御测试价值：

- 这是“插件/Hub/marketplace manifest 成为执行控制面”的典型案例。
- 需要测试：manifest 字段是否允许路径跳转、远程脚本、非预期扩展名、安装后 hook、跨包引用。
- 安装插件前应做 manifest 策略审查；安装时应禁网、隔离凭证、最小权限运行。

## 3. GitHub Advisory: PyTorch Lightning PyPI compromise

- Source: GitHub Advisory Database.
- Evidence: https://github.com/advisories/GHSA-w37p-236h-pfx3
- CVE: `CVE-2026-44484`
- Affected versions: `2.6.2`, `2.6.3`
- 关键点：
  - Advisory 判断一个或多个发布版本被 compromise 并包含恶意代码。
  - 已确认受影响版本需要删除；建议将 PyTorch Lightning pin 到 `2.6.1`。
  - 处置建议包括：假设环境已被 compromise、轮换 API key / token / SSH key / service account、从干净状态重建系统、审查日志。

防御测试价值：

- ML/AI 训练依赖不是普通 dev dependency，常常能接触数据集、模型权重、云凭证、实验平台 token。
- 测试时要覆盖：训练镜像、notebook、CI runner、model registry、artifact store、实验追踪系统的 secret exposure。

## 4. GitHub Advisory: @cap-js 包恶意版本与自传播

- Source: GitHub Advisory Database.
- Evidence: https://github.com/advisories/GHSA-pvw4-cvr4-97p8
- CVE: `CVE-2026-46421`
- Affected packages:
  - `@cap-js/sqlite@2.2.2`
  - `@cap-js/postgres@2.2.2`
  - `@cap-js/db-service@2.10.1`
- 关键点：
  - 恶意版本收集 credentials，并尝试 self-propagation。
  - 若安装过受影响版本，应认为机器可访问的 npm tokens、cloud credentials、SSH keys、GitHub PATs 已暴露。

防御测试价值：

- 需要把“安装过一次”视为完整 incident，而不是只升级包。
- 检测重点：生命周期脚本执行、访问 secret 文件、访问云元数据服务、npm/GitHub 发布行为、异常 registry token 使用。

## 5. Microsoft: Mastra npm supply-chain compromise

- Source: Microsoft Security Blog.
- Evidence: https://www.microsoft.com/en-us/security/blog/2026/06/17/postinstall-payload-inside-mastra-npm-supply-chain-compromise/
- 关键点：
  - Microsoft Threat Intelligence 观察到影响 mastra / `@mastra` 范围 140+ npm packages 的大规模供应链攻击。
  - 攻击链包括 poisoned `package.json`、typosquat `easy-day-js`、postinstall hook、obfuscated `setup.cjs`、staged payload、PowerShell / .NET reflective loading、registry persistence。
  - Microsoft 给出的检测覆盖点包括 npm install 生命周期脚本、Node.js 可疑行为、反射式 .NET 加载、云元数据服务访问、CI/CD runner post-compromise activity。

防御测试价值：

- 很适合转成“多阶段供应链样本”：package install -> JavaScript dropper -> PowerShell/.NET -> credential/cloud recon -> persistence。
- 测试重点不是 payload，而是每一阶段的 telemetry 是否能串起来。

## 6. Mandiant / GTIG: PeopleSoft 零日与 ShinyHunters extortion

### Oracle PeopleSoft CVE-2026-35273

- Source: Google Cloud / Mandiant / GTIG.
- Evidence: https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-targets-education-sector-oracle-exploit
- 关键点：
  - Mandiant 和 GTIG 观察到 UNC6240 / ShinyHunters 针对 Oracle PeopleSoft 的 active compromise and extortion campaign。
  - 活动时间为 2026-05-27 至 2026-06-09。
  - 与 `CVE-2026-35273` 利用一致，影响 Environment Management component；利用时间早于 Oracle 2026-06-10 advisory，属于 zero-day 使用。
  - 目标是 PeopleSoft Environment Management Hub (`PSEMHUB`) endpoints。

防御测试价值：

- ERP/PeopleSoft 这类业务系统经常拥有高价值数据和内网信任位置。
- 测试应关注：管理组件暴露、异常 PSEMHUB 请求、应用服务进程异常、数据导出、后续 extortion 迹象。

### ShinyHunters-branded SaaS data theft

- Source: Google Cloud / Mandiant / GTIG.
- Evidence: https://cloud.google.com/blog/topics/threat-intelligence/expansion-shinyhunters-saas-data-theft
- 关键点：
  - Mandiant 观察到使用 ShinyHunters-branded TTP 的数据窃取勒索活动扩展。
  - 初始访问主要依赖 vishing、受害者品牌化 credential harvesting sites、SSO 凭据和 MFA code 捕获。
  - 进入后攻击者访问云 SaaS 应用，外传敏感数据和内部通信，后续用于勒索。
  - 在至少部分案例中，攻击者冒充 IT 人员声称公司正在更新 MFA 设置，并诱导员工提交凭据/MFA code，再注册攻击者控制的 MFA 设备。

防御测试价值：

- 这是“身份恢复/帮助台/MFA 设备注册/SaaS 授权”链条，不应只当 phishing。
- 测试应覆盖：新 MFA 设备注册、SSO session 风险、异常 SaaS bulk export、OAuth app consent、内部通信平台数据导出。

## 7. Microsoft AI Red Team: Agentic AI failure modes v2.0

- Source: Microsoft Security Blog.
- Evidence: https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us/
- 关键点：
  - Microsoft AI Red Team 认为 12 个月实战红队证据足以更新 Agentic AI failure modes taxonomy。
  - v1.0 包含 agent compromise、injection、impersonation、flow manipulation、memory poisoning、cross-domain prompt injection、human-in-the-loop bypass 等。
  - v2.0 新增 7 类 failure modes，并基于真实部署系统红队经验扩展 mitigation。

防御测试价值：

- Fulcrum 样本不应只测“提示注入字符串”，还要测 flow manipulation、identity impersonation、human approval bypass、memory/action provenance。
- Agent 安全评估要从“模型回答是否安全”扩展到“任务流、身份、工具、状态、记忆、审批和外部系统调用是否安全”。

## 8. Huntress: Nightmare-Eclipse tooling in real-world intrusion

- Source: Huntress.
- Evidence: https://www.huntress.com/blog/nightmare-eclipse-intrusion
- 关键点：
  - Huntress 在真实入侵中观察到 BlueHammer、RedSun、UnDefend 活动。
  - 活动与疑似 compromised FortiGate SSL VPN access 相关。
  - 典型痕迹包括工具落在用户可写目录，例如 Pictures、Downloads 下短目录；并有 `whoami /priv`、`cmdkey /list`、`net group` 等 hands-on-keyboard 侦察。
  - BlueHammer 已在 Microsoft 2026-04 更新中修复，其他部分在文章发布时仍存在补丁状态差异。

防御测试价值：

- 入侵链是“VPN 初始访问 -> 用户可写目录落地 -> 本地提权/凭证侦察 -> 隧道/横向”。
- 测试应关注：VPN 来源异常、用户可写目录中的新二进制、权限侦察命令、Defender/EDR 相关异常、短时间内横向尝试。

## 9. 本轮应加入 Fulcrum 的测试主题

| 主题 | 信任边界 | 关键观测点 |
|---|---|---|
| MCP tools/call 路径写入 | LLM/MCP 参数 -> 文件系统 | containment check、绝对路径、`.pth`、工具来源 |
| Hub manifest post_install | 插件 manifest -> 安装执行 | manifest 字段、安装 hook、安装时凭证隔离 |
| AI SDK import-time 执行 | dependency import -> runtime | import side effect、subprocess/network、凭证作用域 |
| ML 框架包 compromise | training dependency -> 数据/云凭证 | notebook、runner、artifact store、model registry |
| npm postinstall 多阶段 | package lifecycle -> OS/云/CI | Node、PowerShell、.NET、metadata service、registry token |
| ERP 零日勒索 | PeopleSoft 管理组件 -> 数据外传 | PSEMHUB、应用服务进程、导出行为 |
| SaaS vishing 数据窃取 | 人/SSO/MFA -> SaaS 数据面 | MFA device、session、bulk export、OAuth consent |
| Agent failure taxonomy | Agent 任务流 -> 工具/记忆/审批 | flow manipulation、impersonation、approval bypass |
| VPN + LPE 工具 | 边缘身份入口 -> endpoint privilege | VPN 登录、用户目录落地、侦察命令、提权迹象 |

## 10. 后续采集建议

1. 将 GitHub Advisory Database 作为 AI/Agent 组件漏洞主来源之一，按 ecosystem 和 package role 打标签。
2. 对每条“恶意包/compromised package”都生成 incident response checklist：是否安装、何时安装、在哪些 runner/镜像/notebook 中安装、哪些 secret 需轮换。
3. 对 Agent/MCP 相关漏洞单独维护“执行边界表”：install-time、import-time、tool-call-time、recipe-load-time、memory-write-time、approval-time。
4. 对 SaaS 数据窃取单独维护“身份到数据面”样本：vishing、MFA reset、OAuth app、bulk export、内部联系人骚扰。

