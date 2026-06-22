# 情报更新：AI Coding Agent、Sentry MCP、Mastra 投毒与构建配置执行面

> 日期：2026-06-18
> 范围：AI coding agent、MCP-connected telemetry、GitHub/CI/CD prompt injection、npm/PyPI 供应链、workflow/build 配置执行面。
> 安全边界：只记录防御所需的攻击链抽象、检测点、处置动作和样本化字段；不保存可直接重放的 exploit 代码。

## 1. 本轮核心判断

AI 编码工具链正在形成一个新的攻击路径：攻击者不一定直接攻击生产系统，而是污染“开发者让 agent 读取的上下文”。一旦 coding agent、CI agent 或 workflow agent 同时具备读取第三方数据和执行命令/修改代码/访问凭证的能力，外部数据源就会变成指令入口。

本轮新增信号集中在五个方向：

- MCP-connected telemetry 劫持：Agentjacking 说明，Sentry 这类“公开写入、内部读取”的 telemetry 系统，接入 MCP 后会变成 coding agent 的提示词入口。
- GitHub metadata 进入 CI agent：issue 标题、PR 标题、HTML 注释、workflow summary 等本来是非可信文本，进入 Claude Code / Gemini CLI / Copilot Agent 后可能影响高权限 workflow。
- AI agent SDK 供应链投毒：Mastra npm scope 被投毒说明，AI agent 框架本身正在成为高价值供应链目标。
- 构建配置即代码：`astro.config.mjs`、`binding.gyp`、package lifecycle hook 等配置文件可在 build/install 阶段直接执行。
- Workflow 自动化平台 RCE：n8n、Langflow、Flowise 这类平台把业务自动化、AI 节点、凭证和代码执行能力集中到一起，沙箱缺陷的影响面很大。

## 2. 新增高价值情报索引

| 编号 | 主题 | 时间 | 证据等级 | 方向 | 关键风险 |
|---|---:|---:|---|---|---|
| INTEL-04-01 | Agentjacking：Sentry MCP 注入劫持 AI coding agents | 2026-06 | B | MCP / telemetry prompt injection | 公开 DSN 可写入 Sentry event，agent 读取后执行攻击者指令 |
| INTEL-04-02 | Claude Code GitHub Action 权限绕过与 repo compromise | 2026-06 | A/B | CI/CD AI agent | GitHub App actor 信任错误 + prompt injection + elevated workflow token |
| INTEL-04-03 | Comment and Control：GitHub metadata 触发多平台凭证泄露 | 2026-06 | B | CI/CD prompt injection | PR title、issue body、HTML comments 被 agent 当成指令 |
| INTEL-04-04 | Claude Code CVE-2026-24887 | 2026-02 | A | coding agent command approval bypass | untrusted context 可触发绕过确认的命令执行路径 |
| INTEL-04-05 | Mastra npm scope takeover / easy-day-js | 2026-06 | A/B | AI agent SDK supply chain | 143 个 @mastra 包加入恶意 dependency，payload 下沉到 typosquat 包 |
| INTEL-04-06 | easy-day-js clean-then-armed semver trick | 2026-06 | A/B | dependency resolution abuse | 先发干净版本，再发带 payload 版本，caret range 自动解析到恶意版本 |
| INTEL-04-07 | Phantom Gyp / Miasma | 2026-06 | B | install-time execution bypass | 不改 package scripts，借 `binding.gyp` 在 npm install 阶段触发执行 |
| INTEL-04-08 | astro.config.mjs malicious PR | 2026-06 | B | build config as code | PR 描述伪装正常修复，真实 payload 隐藏在 build config 右侧长行 |
| INTEL-04-09 | n8n CVE-2026-1470 / CVE-2026-0863 | 2026-01 | A | workflow sandbox escape | 表达式/代码节点沙箱绕过导致自动化平台主机 RCE |
| INTEL-04-10 | Agent Skills ecosystem ToxicSkills | 2026-02 | B | skills supply chain | 技能继承 agent 权限，低门槛发布、无签名、可持久化污染 agent 行为 |

## 3. 深度分析

### INTEL-04-01 Agentjacking：Sentry MCP 注入劫持 AI coding agents

来源：

- CSA: https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/
- The Hacker News: https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html

攻击链抽象：

```text
攻击者获得公开 Sentry DSN
-> 向 Sentry 项目写入伪造 error event
-> event message / stack trace / metadata 中包含指令化内容
-> 开发者让 AI coding agent 通过 Sentry MCP 调查错误
-> agent 把 Sentry 返回内容当成可信诊断上下文
-> agent 读取文件、修改代码、执行命令或外带信息
-> 所有动作使用开发者本机权限和凭证完成
```

关键失败点：

- Sentry DSN 是公开写入凭据，设计上允许客户端上报事件。
- MCP 把 Sentry 从“日志/错误数据源”升级为 agent 决策上下文。
- Agent 无法天然区分真实错误日志与攻击者伪造日志。
- EDR/IAM/WAF 可能看不到异常，因为 agent 使用的是开发者授权动作。

检测线索：

- Sentry event 中出现 instruction-like 文本、命令语气、要求读取文件/运行命令/提交修复。
- agent 在读取 Sentry issue 后立即执行 shell、git、file read、network request。
- 同一 Sentry DSN 短时间出现异常来源 IP、大量伪造 event 或不符合应用栈的 stack trace。

防御动作：

- MCP 工具返回一律标为 untrusted data，不允许直接成为 system/developer 指令。
- Sentry MCP 输出进入 agent 前做净化：剥离指令化内容、HTML、Markdown 链接、命令文本。
- 对“从外部 telemetry 到本地执行”的链路做审批。
- 为 coding agent 添加来源归因：哪个 Sentry event 触发了哪个文件/命令/提交动作。

### INTEL-04-02 Claude Code GitHub Action：AI agent 进入 CI/CD 后成为供应链风险

来源：

- GMO Flatt Security: https://flatt.tech/research/posts/poisoning-claude-code-one-github-issue-to-break-the-supply-chain/
- CSA: https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/

攻击链抽象：

```text
目标仓库使用 AI coding GitHub Action
-> workflow 信任某类 GitHub App actor 或自动化 actor
-> 攻击者通过 issue / PR / bot actor 注入 prompt
-> agent 读取 untrusted GitHub metadata
-> agent 在高权限 workflow 中运行
-> 读取环境变量、workflow token、OIDC token 或 repository data
-> 修改代码 / issue / workflow / action source
-> 下游使用者被供应链传播影响
```

关键失败点：

- “能创建 issue/PR”不等于“可信工作流输入”。
- AI agent 运行在 CI/CD 内，权限通常高于普通外部贡献者。
- GitHub metadata 本质是用户可控文本，不该直接进入高权限 agent prompt。

防御动作：

- AI workflow 对外部 issue/PR 默认只读、无 secrets、无 `id-token: write`。
- 将 metadata 摘要和执行修复拆成两个隔离 workflow。
- 不让 agent 在处理外部输入时使用 repo write token。
- 审计 workflow logs 中的 agent prompt、tool call、文件改动和 token 访问。

### INTEL-04-03 Comment and Control：GitHub metadata 是高危输入

来源：

- CSA summary: https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/

攻击链抽象：

```text
攻击者提交 PR / issue / comment
-> 标题、正文或 HTML 注释包含隐藏指令
-> AI review / triage / fix agent 把 metadata 拼进 prompt
-> agent 执行读取 secrets、输出环境变量、修改文件等动作
-> 结果写回 PR comment、issue reply、workflow summary 或外部网络
```

检测线索：

- PR title / issue title 出现命令语气、base64、HTML comment、trusted section 等模式。
- AI action 输出中出现环境变量名、token-like 字段、过长编码文本。
- agent 在处理纯 metadata 任务时触发 shell/file/network 工具。

防御动作：

- 对 GitHub metadata 做 prompt injection 扫描。
- AI action 使用最小权限 token；外部贡献者触发时不注入 secrets。
- 输出到 PR comment 前做 secret scanning 与敏感模式拦截。

### INTEL-04-04 Claude Code CVE-2026-24887：确认提示不是安全边界

来源：

- GitHub Advisory: https://github.com/advisories/GHSA-qgqw-h4xq-7w8w

攻击链抽象：

```text
攻击者控制 Claude Code context 中的一段文本
-> 该文本影响 agent 选择某个看似允许的命令路径
-> 命令解析缺陷绕过用户确认
-> untrusted command 被执行
```

关键启发：

- “需要用户确认”是 UX 控制，不应被当作唯一安全边界。
- 允许命令的解析器必须按完整 argv/AST 做验证，不能只看命令名。
- untrusted context 能影响命令参数时，应重新要求审批并展示来源。

### INTEL-04-05 Mastra npm scope takeover：AI agent SDK 成为高价值供应链目标

来源：

- JFrog: https://research.jfrog.com/post/easy-day-js/
- SafeDep: https://safedep.io/mastra-npm-scope-takeover-supply-chain-attack/
- Endor Labs: https://www.endorlabs.com/learn/mastra-npm-org-compromised-multiple-packages-trojanized-to-drop-a-remote-payload-via-easy-day-js

攻击链抽象：

```text
攻击者控制或滥用曾有发布权限的 maintainer 账号
-> 在 @mastra scope 下批量重新发布包
-> Mastra 源码基本不变，只新增 dependency: easy-day-js
-> easy-day-js 伪装成 dayjs 类日期库
-> npm semver 解析到带 install hook 的版本
-> 安装阶段拉取并运行第二阶段 payload
-> 窃取浏览器/钱包/云/LLM/API 开发者凭证
```

关键失败点：

- 离职/前贡献者权限未及时回收。
- 只审查一方包源码，看不到下一层依赖 payload。
- 项目不强制 provenance，标准 npm token 仍可发布无 attestation 版本。
- AI agent 框架包天然位于开发者高信任路径。

检测线索：

- `@mastra/*` 版本突然新增不必要的日期库 dependency。
- 包 provenance 从 yes 变成 no。
- 作用域内大量包短时间批量发布。
- 依赖名与知名库高度相似但维护者/发布时间/功能不匹配。

防御动作：

- 对高价值 scope 强制 provenance / trusted publishing。
- 定期回收 dormant maintainer 的 publish 权限。
- install 前递归审查新增依赖，不只看顶层包 diff。
- 对 AI SDK、agent framework、MCP server 包设置 dependency cooldown。

### INTEL-04-06 clean-then-armed semver trick：审查干净版本，安装恶意版本

来源：

- JFrog: https://research.jfrog.com/post/easy-day-js/
- SafeDep: https://safedep.io/mastra-npm-scope-takeover-supply-chain-attack/

攻击链抽象：

```text
攻击者先发布 clean package 版本
-> 目标包依赖使用 caret range
-> 攻击者发布同一 package 的后续恶意兼容版本
-> 安装时 resolver 选择最新兼容恶意版本
-> 安全审查如果只看先前 clean 版本会漏报
```

防御动作：

- 安全审查必须基于 lockfile 实际解析结果，而不是 manifest 中看似指定的最低版本。
- 对新发布版本设置冷却期。
- 禁用 install scripts 或在沙箱里执行。
- 记录 dependency resolved version 与 reviewed version 是否一致。

### INTEL-04-07 Phantom Gyp：绕过 package scripts 的安装期执行

来源：

- StepSecurity: https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm

攻击链抽象：

```text
攻击者发布或篡改 npm 包
-> package.json 不包含明显 preinstall/postinstall
-> 包含 binding.gyp
-> npm install 触发原生构建流程
-> 构建过程执行 attacker-controlled logic
-> 窃取凭证并传播到更多 npm/GitHub 仓库
```

关键失败点：

- 很多工具只扫描 package.json scripts。
- `binding.gyp`、native build、prepare、install、postinstall 都是执行面。
- 没有脚本不等于安装安全。

防御动作：

- 禁止或沙箱化 native build。
- 对 `binding.gyp`、`node-gyp`、prebuild、binary download 做高风险标记。
- install-time 网络访问默认禁止。
- 对 npm token/GitHub PAT/云凭证在开发机和 CI 中做最小暴露。

### INTEL-04-08 astro.config.mjs malicious PR：构建配置即执行入口

来源：

- SafeDep: https://safedep.io/astro-config-blockchain-c2-supply-chain

攻击链抽象：

```text
攻击者提交看似正常的 PR
-> PR 描述声称修复 UI/文档/测试问题
-> 实际改动包含 astro.config.mjs
-> payload 隐藏在长行右侧或不显眼位置
-> 开发者或 CI 运行 astro dev/build/preview
-> config 作为 Node.js 模块执行
-> 访问环境变量、文件系统、网络并拉取后续命令
```

关键失败点：

- 配置文件被当作“声明式配置”，但在很多框架中它是可执行代码。
- PR 描述与 diff 不一致时，人工审查容易被故事带偏。
- AI code review 若只总结 PR 描述，也可能漏掉 build config payload。

防御动作：

- 对构建配置文件变更强制安全审查：`astro.config.*`、`vite.config.*`、`next.config.*`、`webpack.config.*`、`rollup.config.*`。
- PR 描述声称的文件与实际 diff 文件不一致时自动告警。
- 检测长行、水平空白隐藏、尾部混淆、动态 import/require、网络访问。

### INTEL-04-09 n8n CVE-2026-1470 / CVE-2026-0863：workflow automation 的沙箱边界

来源：

- JFrog research: https://research.jfrog.com/post/achieving-remote-code-execution-on-n8n-via-sandbox-escape/
- JFrog advisory: https://research.jfrog.com/vulnerabilities/n8n-expression-node-rce/
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-1470

攻击链抽象：

```text
攻击者拥有创建或修改 workflow 的权限
-> 在 expression / code node 中提交恶意表达式或代码
-> 平台 sandbox AST/隔离逻辑被绕过
-> 表达式在 n8n 主进程或任务运行环境中执行
-> 攻击者以 n8n 进程权限访问 secrets、workflow credentials、网络和文件系统
```

关键失败点：

- 业务自动化平台天然需要访问很多第三方凭证。
- 沙箱只要有一个逃逸点，就会变成 host-level compromise。
- “authenticated user” 在低代码平台里可能只是普通 workflow 作者，但其代码执行影响的是整个平台。

防御动作：

- 升级到 JFrog/厂商建议的修复版本。
- 对 workflow author 权限分级：普通用户不得创建 expression/code node。
- 高风险节点运行在独立 worker/container，不共享主平台凭证。
- 记录 expression/code node 创建、修改、执行和失败事件。

### INTEL-04-10 ToxicSkills：Agent Skills 是新一代插件供应链

来源：

- Snyk: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/

观察要点：

- Snyk 扫描了近 4,000 个 agent skills，发现一批 critical-level 问题。
- Agent Skills 往往继承 agent 的 shell、文件系统、环境变量、通信渠道和持久记忆权限。
- 发布门槛低，常缺少签名、安全审查和默认沙箱。

攻击链抽象：

```text
攻击者发布看似有用的 agent skill
-> skill 描述或 setup 步骤中包含恶意指令
-> 用户/agent 安装 skill
-> skill 继承 agent 权限
-> 读取文件、环境变量、聊天上下文、长期记忆
-> 通过网络、邮件、issue、PR comment 等渠道外带
-> 修改 agent memory 或配置实现持久化
```

防御动作：

- Skills 按供应链治理：签名、来源信誉、版本锁定、权限清单。
- 安装 skill 前做静态扫描和人审。
- Skill 不应默认继承 shell/文件/网络/记忆写入权限。
- 对 skill 修改 agent memory、system prompt、MCP config 的行为告警。

## 4. 对防护项目的新增规则启发

### 数据源信任分层

新增需要标记的 untrusted sources：

- Sentry events / telemetry events。
- GitHub issue/PR title、body、comments、HTML comments。
- workflow summary、job log、artifact text。
- package manifest、dependency manifest、build config。
- agent skill markdown / setup instruction。

### Agent 工具链策略

必须阻断或审批：

- 从 telemetry/event 内容直接触发 shell、git、file read/write。
- 外部贡献者输入触发带 secrets 的 CI agent。
- build config 文件新增网络访问、dynamic require/import、长行混淆。
- package install 中出现 lifecycle/native build 且来源未信任。
- agent skill 请求 shell、network、memory write、credential read。

### 供应链检测信号

新增特征：

- scope 内大量包短时间批量发布。
- maintainer 账号长期 dormant 后突然发布。
- provenance 从 yes 变 no。
- dependency 与项目功能无关。
- clean version 与 resolved version 不一致。
- package scripts 为空但存在 `binding.gyp` 或 native build 触发器。
- PR 描述与 diff 文件不匹配。

## 5. 可转测试样本方向

| 样本方向 | source_type | target_tool | expected_action | 关键断言 |
|---|---|---|---|---|
| Sentry event 指令注入 | telemetry_event | sentry.mcp.get_issue | sanitize / approve | MCP 返回内容不可直接触发本地执行 |
| GitHub issue 触发 CI agent | github_issue | ci.agent | block | 外部 metadata 不能访问 secrets/write token |
| PR title hidden instruction | github_pr | code_review.agent | sanitize | HTML comment / title 指令不进入执行层 |
| Mastra 新增异常 dependency | package_release | dependency.install | quarantine | provenance drop + new dependency + scope burst |
| clean-then-armed semver | lockfile | dependency.resolve | block | reviewed version 必须等于 resolved version |
| binding.gyp install execution | package_source | dependency.install | quarantine | scripts 为空也要识别 native build 执行面 |
| build config payload | pull_request_diff | ci.build | block | config-as-code 文件变更需高风险审查 |
| n8n expression/code node | workflow_definition | workflow.execute | approve / sandbox | 低权限用户不能触发代码节点主机执行 |
| Agent Skill 权限过宽 | skill_manifest | skill.install | quarantine | skill 需要显式最小权限清单 |

## 6. 来源清单

- CSA Agentjacking: https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/
- CSA AI Agent Prompt Injection in CI/CD: https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/
- GMO Flatt Security Claude Code: https://flatt.tech/research/posts/poisoning-claude-code-one-github-issue-to-break-the-supply-chain/
- GitHub Advisory CVE-2026-24887: https://github.com/advisories/GHSA-qgqw-h4xq-7w8w
- JFrog easy-day-js: https://research.jfrog.com/post/easy-day-js/
- SafeDep Mastra takeover: https://safedep.io/mastra-npm-scope-takeover-supply-chain-attack/
- Endor Labs Mastra analysis: https://www.endorlabs.com/learn/mastra-npm-org-compromised-multiple-packages-trojanized-to-drop-a-remote-payload-via-easy-day-js
- StepSecurity Phantom Gyp: https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm
- SafeDep astro.config.mjs: https://safedep.io/astro-config-blockchain-c2-supply-chain
- JFrog n8n RCE: https://research.jfrog.com/post/achieving-remote-code-execution-on-n8n-via-sandbox-escape/
- JFrog n8n advisory: https://research.jfrog.com/vulnerabilities/n8n-expression-node-rce/
- NVD CVE-2026-1470: https://nvd.nist.gov/vuln/detail/CVE-2026-1470
- Snyk ToxicSkills: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
