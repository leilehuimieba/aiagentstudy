# 情报更新：AI Gateway、MCP、Copilot 搜索与供应链反扫描

> 日期：2026-06-18
> 范围：AI/Agent 平台 CVE、MCP stdio 执行风险、企业 Copilot 数据外泄、供应链投毒、AI 扫描器反制。
> 安全边界：本文只保留防御分析、攻击链抽象、检测线索和样本化字段，不收集可直接重放到真实系统的 exploit。

## 1. 本轮核心判断

这一轮新增情报显示，AI/Agent 安全的重点已经从“提示词是否越狱”进一步转向“AI 基础设施是否把不可信输入变成动作”。几个方向正在合流：

- AI Gateway 成为高价值入口：LiteLLM 这类网关集中保存模型供应商密钥、代理路由、团队 API Key、MCP 配置和下游集成，一旦 MCP 测试接口能启动 stdio 命令，影响面超过普通 Web RCE。
- MCP stdio 是生态级执行边界：Flowise、Agent Zero、LiteLLM、DocsGPT/Letta 等案例都指向同一类失败：把配置、导入文件、测试连接、marketplace 项或 prompt 变成服务器端命令。
- 企业 Copilot/Search 是“权限放大器”：SearchLeak 说明，搜索参数、流式渲染、HTML/CSP/SSRF 这类传统 Web 问题叠加 AI 检索权限后，会变成一键数据外泄链。
- 供应链攻击开始反制 AI 审计：Hades、Mini Shai-Hulud/Miasma 相关样本开始在代码注释中放入提示注入、上下文洪泛、策略触发内容，让 AI 扫描器提前拒答、截断或误判。
- 传统漏洞优先级模型需要升级：CISA 2026 年 6 月的新漏洞处置口径更强调公网暴露、已被利用、可自动化、可获得系统控制这几个维度，AI 基础设施漏洞往往同时满足多个条件。

## 2. 新增高价值情报索引

| 编号 | 主题 | 时间 | 证据等级 | 方向 | 关键风险 |
|---|---:|---:|---|---|---|
| INTEL-03-01 | LiteLLM CVE-2026-42271 已进 CISA KEV | 2026-06 | A | AI Gateway / MCP RCE | MCP test endpoints 接收 stdio command/args/env 并在代理主机启动子进程 |
| INTEL-03-02 | LiteLLM + Starlette 链式未授权 RCE | 2026-06 | B | 漏洞链 | Host header validation bypass 可能把原本需 API Key 的问题升级为未授权 RCE |
| INTEL-03-03 | SearchLeak CVE-2026-42824 | 2026-06 | A/B | Copilot 数据外泄 | Parameter-to-Prompt + HTML race + Bing SSRF，单击 Microsoft 链接可外泄 M365 数据 |
| INTEL-03-04 | Flowise CVE-2026-40933 | 2026-05 | B | MCP / workflow import | 恶意 chatflow 导入即触发服务器端 stdio MCP 命令 |
| INTEL-03-05 | Agent Zero CVE-2026-30624 | 2026-04 | B | MCP 配置执行 | External MCP server JSON 中 command/args 被应用执行 |
| INTEL-03-06 | Langflow CVE-2026-33017 / CVE-2026-27966 更新 | 2026-06 | A | AI 编排平台 RCE | public flow build / CSV Agent 默认危险代码执行，NVD 近期更新元数据 |
| INTEL-03-07 | Semantic Kernel CVE-2026-26030 / CVE-2026-25592 | 2026-05 | A | Prompt-to-shell | Prompt injection 影响 tool 参数，触发文件写入或执行原语 |
| INTEL-03-08 | mcp-run-python CVE-2026-25905 | 2026-02 | B | 沙箱逃逸 / tool shadowing | Pyodide 可访问 JS bridge，模型执行的 Python 可篡改 MCP 工具 |
| INTEL-03-09 | Web-based IDPI observed in the wild | 2026-03 | B | 间接提示注入 | 恶意网页把隐藏指令投喂给广告审核/浏览器/搜索类 AI agent |
| INTEL-03-10 | Hades / AI analyst misdirection | 2026-06 | B | 供应链 + AI 反扫描 | PyPI 包在 payload 前放提示注入，诱导 LLM 分析器忽略恶意代码 |
| INTEL-03-11 | npm scanner anti-analysis package | 2026-06 | B | AI 扫描器 DoS/误导 | 包含策略触发内容、fake system override、上下文洪泛、尾部混淆 JS |
| INTEL-03-12 | npm/PyPI Mini Shai-Hulud/Miasma 扩散 | 2026-05/06 | A/B | 供应链蠕虫 | CI/CD、OIDC、SLSA provenance、npm/PyPI 发布链被滥用 |

证据等级说明：

- A：官方、NVD/CISA、原厂安全博客或明确 CVE。
- B：一线安全团队技术报告，有可复核攻击链或样本描述。
- C：社区线索，需二次验证。

## 3. 深度分析

### INTEL-03-01 LiteLLM CVE-2026-42271：AI Gateway 的 MCP test endpoint 变成执行入口

来源：

- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-42271
- GitHub Advisory: https://github.com/advisories/GHSA-v4p8-mg3p-g94g
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

影响资产：

- LiteLLM 1.74.2 到 1.83.6。
- 自托管 AI Gateway、团队内统一 LLM proxy、带 MCP 管理能力的平台。

攻击链抽象：

```text
低权限或内部 API Key 持有者
-> 调用 MCP server 预览/测试连接接口
-> 请求体提交 stdio server config
-> config 中包含 command / args / env
-> LiteLLM 为了测试连接在代理主机启动子进程
-> 攻击者以 LiteLLM proxy 进程权限执行命令
-> 读取模型供应商 Key、team API key、环境变量、MCP 配置、云/SaaS 凭证
```

关键失败点：

- “测试连接”被当成低风险功能，但它会触发真实子进程。
- API Key 只证明调用者能访问网关，不等于能在网关主机执行命令。
- MCP stdio 的 command/args/env 是执行配置，不是普通数据。

检测线索：

- `/mcp-rest/test/connection`、`/mcp-rest/test/tools/list` 的异常 POST。
- LiteLLM 进程下出现不符合基线的子进程。
- MCP test 请求体出现 `stdio`、`command`、`args`、`env`。
- API Key 持有者权限与主机执行行为不匹配。

防御建议：

- 升级 LiteLLM 到 1.83.7 或更高版本。
- 网关管理面与 MCP test endpoint 不暴露到公网。
- MCP stdio 默认关闭；如确需使用，必须 allowlist command、固定 args schema、剥离 env。
- 轮换 LiteLLM 环境变量中的模型、云、数据库、SaaS 凭证。

### INTEL-03-02 LiteLLM + Starlette：从“需 API Key”升级到未授权 RCE 的链式风险

来源：

- Horizon3.ai: https://horizon3.ai/attack-research/vulnerabilities/cve-2026-42271-chained-with-cve-2026-48710/
- CVE record: https://www.cve.org/CVERecord?id=CVE-2026-42271

攻击链抽象：

```text
公网暴露 LiteLLM
-> 依赖树包含受影响 Starlette
-> Host header validation bypass 绕过认证路径假设
-> 访问 LiteLLM MCP test endpoints
-> 提交 stdio config
-> 触发代理主机子进程执行
```

为什么重要：

- 防御团队不能只看单个 CVE 的原始权限要求。
- AI 基础设施常由 FastAPI/Starlette/Uvicorn 等组件拼接，认证、路由、Host header、反代配置会改变漏洞真实可利用性。
- Gateway 一旦被打穿，攻击者可获得模型供应商密钥、组织内 LLM 流量、插件配置和下游工具凭证。

检测线索：

- 不寻常 Host header。
- 同源 IP 先探测 Host header，再访问 MCP test endpoint。
- LiteLLM 进程产生子进程，随后出现读取 `.env`、云元数据、token 文件、配置目录的行为。

防御建议：

- 同时升级 LiteLLM 与 Starlette。
- 用反向代理强制 Host allowlist。
- 禁止外部访问 MCP 管理和测试接口。
- 审计此前异常请求窗口，不要只做补丁验证。

### INTEL-03-03 SearchLeak CVE-2026-42824：企业 Copilot 搜索层变成一键外泄链

来源：

- Varonis: https://www.varonis.com/blog/searchleak
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-42824
- MSRC: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-42824

攻击链抽象：

```text
攻击者构造 Microsoft 365 Copilot Enterprise Search 链接
-> q 参数中放入指令化搜索意图
-> 用户点击看似正常的 microsoft.com 链接
-> Copilot 把 q 参数当 prompt，而不仅是搜索词
-> Copilot 按用户权限检索邮箱、日历、OneDrive、SharePoint
-> 回复中形成可触发外联的 HTML/图片资源
-> sanitizer 竞态窗口让浏览器先发起请求
-> Bing SSRF / allowlist 路径成为外带代理
-> 攻击者从请求日志恢复敏感数据
```

关键失败点：

- 搜索参数和执行指令未隔离。
- AI 输出进入浏览器渲染时存在竞态窗口。
- CSP allowlist 中的可信服务被当成外带中转。
- Copilot 运行在用户企业权限上，攻击者不需要额外 OAuth 授权。

防御/治理启发：

- 企业 AI 搜索必须区分 `query` 与 `instruction`。
- AI 生成内容默认不能加载外部图片、Markdown 图片、HTML 资源。
- 对 AI 搜索请求做“检索范围 + 输出外联”联合审计。
- 清理 SharePoint/OneDrive 过度共享，否则 Copilot 会放大已有权限问题。

可转测试样本：

- URL 参数上下文污染。
- 检索结果外带。
- AI 输出渲染阶段外链阻断。
- CSP allowlist 被中转滥用。

### INTEL-03-04 Flowise CVE-2026-40933：导入文件不是数据，而是服务器端执行计划

来源：

- Obsidian Security: https://www.obsidiansecurity.com/blog/when-is-stdio-mcp-actually-a-vulnerability

攻击链抽象：

```text
攻击者制作 chatflow
-> chatflow 内含 Custom MCP stdio server 配置
-> 授权用户导入 chatflow
-> Flowise 在导入阶段解析并启动 MCP server
-> stdio command 在 Flowise 服务器端执行
-> 攻击者获得 Flowise server 权限
```

关键失败点：

- Import 行为触发命令，而不是只保存配置。
- 用户以为导入的是 workflow，实际导入的是“带启动命令的执行图”。
- 输入校验只挡明显 shell 字符，挡不住合法命令加危险参数、npx/uvx/python 模块加载等路径。

防御建议：

- 对导入的 workflow 做静态安全审查，尤其是 MCP/tool/server 节点。
- 导入阶段禁止启动任何外部进程。
- stdio MCP 需要管理员审批、命令 allowlist、参数 schema、沙箱和网络限制。

### INTEL-03-05 Agent Zero CVE-2026-30624：External MCP Servers 配置 RCE

来源：

- GitHub Advisory: https://github.com/advisories/GHSA-rppc-c4xv-v29h

攻击链抽象：

```text
攻击者提供 MCP server JSON 配置
-> 配置包含 command + args
-> Agent Zero 应用配置并执行这些值
-> 命令以 Agent Zero 进程权限运行
```

安全含义：

- “用户可配置 MCP server”本身就是执行能力。
- 任何 AI agent 管理台都应把 MCP server 配置当成代码审查，而不是普通偏好设置。

### INTEL-03-06 Langflow CVE-2026-33017 / CVE-2026-27966：AI 编排平台 RCE 系列继续更新

来源：

- CVE-2026-33017 NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-33017
- CVE-2026-27966 NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-27966

新增关注点：

- CVE-2026-33017 的 NVD 记录在 2026-06-17 仍有更新，说明相关引用、分析或利用信息仍在完善。
- CVE-2026-27966 体现的是“Agent 节点默认打开危险代码执行能力”，prompt injection 可越过自然语言层面，触达 Python REPL 这类执行原语。

攻击链抽象：

```text
Langflow 暴露 public build 或危险 Agent node
-> 攻击者控制 flow data / prompt / node definition
-> 服务器端执行 Python 代码或 OS 命令
-> 读取 secrets / workflow 配置 / 向量库连接 / 数据库连接
-> 横向移动到 AI pipeline 下游系统
```

防御建议：

- 把 AI workflow 平台按“密钥集中系统”管理。
- 禁用危险代码执行节点，或放进强隔离沙箱。
- workflow 导入、构建、validate、preview 都要视为潜在执行路径。

### INTEL-03-07 Semantic Kernel：Prompt injection 到执行原语

来源：

- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/

核心结论：

- LLM 本身不是安全边界。
- 工具参数只要受模型输出影响，就必须按攻击者可控输入处理。
- prompt injection 不一定停留在“模型乱说”，在带工具的 agent 中可能直接变成文件写入、查询注入、eval sink 或 RCE。

攻击链抽象：

```text
用户或网页内容影响 prompt
-> 模型选择工具并生成参数
-> 框架信任模型生成的参数
-> 参数进入动态 filter / eval / file path / interpreter
-> 触发执行、写文件或数据外泄
```

防御建议：

- 工具 schema 只定义类型不够，还要定义值域、路径范围、命令范围、网络范围。
- 所有模型生成参数进入强校验层，不允许直接进入执行 sink。
- 对工具调用做来源归因：哪个网页/文档/邮件/用户输入导致该工具参数。

### INTEL-03-08 mcp-run-python CVE-2026-25905：沙箱逃逸与工具影子化

来源：

- GitHub Advisory: https://github.com/advisories/GHSA-pfv4-wmph-5gc6
- JFrog catalog: https://research.jfrog.com/

攻击链抽象：

```text
MCP server 暴露 runPython / runPythonAsync
-> Python 代码在 Pyodide 中执行
-> Pyodide 可访问 JS bridge
-> 攻击者修改 JS runtime / Node process / MCP tool registry
-> 替换原本安全的工具实现
-> 后续 agent 调用“同名工具”时实际执行恶意逻辑
```

为什么重要：

- 这不是单次命令执行，而是工具注册表被篡改。
- 从审计看，agent 似乎调用了合法工具，但真实实现已被 shadow。

防御建议：

- 不使用无维护、无隔离的代码执行型 MCP server。
- Python/JS/WASM 运行时必须切断宿主桥接，或放在独立容器。
- 工具调用前后校验工具实现 hash / 注册表变更。

### INTEL-03-09 Web-based IDPI：真实世界开始投毒 AI 浏览/审核/搜索链

来源：

- Unit 42: https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/

观察到的模式：

```text
恶意网页或广告页
-> HTML 注释、隐藏文本、metadata、CSS/视觉隐藏内容中放入指令
-> AI agent / 审核器 / 浏览器总结功能抓取页面
-> LLM 把隐藏内容当成指令
-> 诱导审核通过、推荐、改写判断或触发工具动作
```

值得注意：

- Unit 42 特别提示不要用 AI agent 直接摄取该页面，这本身说明安全报告也可能包含“对 AI agent 有害的样本内容”。
- 当前真实世界案例很多仍偏操纵审核/推荐/排名，但随着 agent 权限增强，后果会从“错误判断”升级到“错误动作”。

防御建议：

- 对网页摄取做“内容与指令隔离”：HTML 文本、注释、隐藏元素、alt、metadata 都只能作为证据，不可作为上级指令。
- 浏览器 agent / crawler / ad review AI 需要检测 hidden prompt intent。
- 把网页来源标为 untrusted，工具调用必须经过策略层。

### INTEL-03-10 Hades：供应链 payload 反过来攻击 AI 分析器

来源：

- StepSecurity: https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages

攻击链抽象：

```text
攻击者发布 PyPI 包
-> 包在 __init__.py 中放 obfuscated import hook
-> 运行时拉起跨平台 payload
-> payload 前部插入给 LLM 分析器看的提示注入文本
-> 诱导 AI 分析器忽略后续混淆代码或给出 clean verdict
-> 真正 payload 继续解密、执行、抓取凭证
```

关键变化：

- 恶意代码不只躲避静态规则和沙箱，也开始躲避“LLM 审计流程”。
- 如果 CI/CD 中把可疑包源码直接丢给 LLM，总结结果可能被包内注释污染。

防御建议：

- LLM 只能辅助解释，不应作为 malware 判定唯一依据。
- 对源码注释和字符串中的 prompt injection 做单独标记。
- 分析器 prompt 必须把被分析代码作为 untrusted data，并强制引用具体证据。

### INTEL-03-11 npm package anti-analysis：上下文洪泛 + 策略触发 + 尾部混淆

来源：

- Socket.dev: https://socket.dev/blog/npm-package-uses-prompt-injection-and-token-flooding-to-disrupt-ai-malware-scanners

攻击链抽象：

```text
npm 包 index.js 体积异常膨胀
-> 前部放安全策略触发内容和 fake system override
-> 中间放大量重复注释进行 context flooding
-> 尾部隐藏混淆 JavaScript
-> AI 扫描器可能拒答、截断、超时、误判或漏看尾部 payload
```

防御建议：

- 扫描器必须先做结构化切片：AST、代码段、字符串、注释、体积异常、压缩/混淆比例。
- LLM 分析必须按片段覆盖率报告，不能只给整体摘要。
- 对 9MB 级单文件、尾部高熵代码、注释异常占比设置硬规则。

### INTEL-03-12 Mini Shai-Hulud / Miasma：CI/CD 与 provenance 被武器化

来源：

- Unit 42: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
- SafeDep: https://safedep.io/mass-npm-supply-chain-attack-tanstack-mistral/
- Microsoft: https://www.microsoft.com/en-us/security/blog/2026/05/29/33-malicious-npm-packages-abuse-dependency-confusion-profile-developer-environments/
- JFrog Security Research: https://research.jfrog.com/

攻击链抽象：

```text
维护者账号 / GitHub Actions / OIDC / internal namespace 被滥用
-> 攻击者批量发布 trojanized npm/PyPI 包
-> 包安装或运行时窃取 GitHub/npm/cloud/CI/CD/K8s/Vault 凭证
-> 使用窃取到的发布权限继续感染更多包
-> provenance 可能仍然显示“由合法 CI 构建”
-> 下游开发者和 agent 工具链自动安装后被感染
```

关键失败点：

- provenance 证明“谁构建”，不证明“构建内容安全”。
- AI/Agent 开发工具链大量自动安装包、执行脚本、读取环境变量，放大供应链攻击收益。
- 组织作用域、内部命名空间、品牌相似包仍然有效。

防御建议：

- 依赖冷却期：新发布版本先隔离观察。
- 安装期沙箱：限制 postinstall、preinstall、native build、网络访问、文件系统访问。
- 发布链最小权限：npm token、GitHub PAT、OIDC 权限按包/仓库/环境隔离。
- 一旦安装疑似包，按主机失陷处理：隔离、查日志、轮换凭证、清理缓存。

## 4. 对防护项目的规则启发

### 输入端上下文污染

需要区分：

- 用户明确指令。
- URL query 参数。
- 搜索词。
- 文档正文。
- HTML 注释/隐藏文本。
- 工具返回。
- 包源码注释。
- marketplace/manifest 配置。

任何非用户明确指令来源都不能覆盖系统策略。

### 大模型交互风险

检测点：

- `ignore previous`、`system override`、`approved`、`verified clean` 这类指令语气是否出现在非指令上下文。
- 供应链源码中出现面向 AI scanner 的话术。
- 长上下文中是否存在洪泛、重复、尾部混淆代码。

### 攻击调用风险

高风险工具：

- MCP stdio server。
- shell / python / node / npx / uvx / npm。
- file read/write。
- http request。
- browser automation。
- enterprise search。
- memory write。
- workflow import。

规则重点不是命令名，而是完整 argv、env、cwd、网络、来源、审批状态。

### 执行环境风险

必须记录：

- agent 进程父子进程树。
- 工具调用前后的文件、网络、环境变量访问。
- MCP server 注册表变更。
- tool implementation hash。
- 容器逃逸或宿主 bridge 访问。

### 供应链风险

新增检测信号：

- 包体积突然增大。
- 注释比例异常。
- tail payload / 高熵尾部代码。
- postinstall/native build/import hook。
- provenance 合法但 commit 走 orphan/bypass review。
- 包内出现面向 LLM/AI scanner 的指令文本。

### 数据泄露风险

Copilot/Search/Agent 输出层要检查：

- AI 输出是否包含外部图片、外链、Markdown image、HTML resource。
- 搜索结果是否被拼进 URL。
- 可信域名是否作为 SSRF/exfil proxy。
- 高敏感数据检索和外联是否同会话发生。

## 5. 可加入测试集的样本方向

这些不是 exploit，而是防护系统的安全样本设计方向：

| 样本方向 | source_type | target_tool | expected_action | 关键断言 |
|---|---|---|---|---|
| MCP test endpoint stdio config | user / api_request | mcp.test_connection | block | command/args/env 不应由低权限用户触发 |
| Chatflow import 含 stdio MCP | document / plugin_manifest | workflow.import | quarantine / approve | 导入阶段不执行进程 |
| URL q 参数指令化搜索 | webpage / user_link | enterprise.search | sanitize / block | query 不能升级为 instruction |
| AI 输出外部图片外带 | model_output | render.html | block | 输出层阻断外部资源 |
| 包源码注释提示注入 | package_source | ai.scanner | flag | AI scanner 不得被代码注释覆盖系统策略 |
| 上下文洪泛 + 尾部混淆 | package_source | ai.scanner | flag | 报告覆盖率和尾部代码分析 |
| Pyodide JS bridge 访问 | tool_runtime | mcp.run_python | block | 代码执行环境不可访问宿主 bridge |
| Tool shadowing | tool_registry | mcp.tool_call | block | 工具实现 hash/registry 变更触发告警 |
| CI provenance 合法但内容异常 | package_release | dependency.install | quarantine | provenance 不替代内容审查 |
| Hidden HTML prompt | webpage | browser_agent.summarize | sanitize | 隐藏元素只作数据，不作指令 |

## 6. 来源清单

- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- CISA 2026-06-08 KEV alert: https://www.cisa.gov/news-events/alerts/2026/06/08/cisa-adds-two-known-exploited-vulnerabilities-catalog
- CISA vulnerability prioritization directive news: https://www.cisa.gov/news-events/news/cisa-issues-new-directive-improving-how-federal-agencies-prioritize-mitigation-cyber-vulnerabilities
- NVD CVE-2026-42271: https://nvd.nist.gov/vuln/detail/CVE-2026-42271
- Horizon3.ai LiteLLM chain: https://horizon3.ai/attack-research/vulnerabilities/cve-2026-42271-chained-with-cve-2026-48710/
- Varonis SearchLeak: https://www.varonis.com/blog/searchleak
- NVD CVE-2026-42824: https://nvd.nist.gov/vuln/detail/CVE-2026-42824
- Obsidian Security Flowise: https://www.obsidiansecurity.com/blog/when-is-stdio-mcp-actually-a-vulnerability
- GitHub Advisory Agent Zero: https://github.com/advisories/GHSA-rppc-c4xv-v29h
- OX Security MCP advisory: https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/
- NVD CVE-2026-33017: https://nvd.nist.gov/vuln/detail/CVE-2026-33017
- NVD CVE-2026-27966: https://nvd.nist.gov/vuln/detail/CVE-2026-27966
- Microsoft Semantic Kernel research: https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/
- GitHub Advisory mcp-run-python: https://github.com/advisories/GHSA-pfv4-wmph-5gc6
- Unit 42 web-based IDPI: https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/
- Socket AI scanner anti-analysis: https://socket.dev/blog/npm-package-uses-prompt-injection-and-token-flooding-to-disrupt-ai-malware-scanners
- StepSecurity Hades: https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages
- Unit 42 npm threat landscape: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
- SafeDep TanStack/Mistral campaign: https://safedep.io/mass-npm-supply-chain-attack-tanstack-mistral/
- Microsoft dependency confusion: https://www.microsoft.com/en-us/security/blog/2026/05/29/33-malicious-npm-packages-abuse-dependency-confusion-profile-developer-environments/
- JFrog Security Research: https://research.jfrog.com/
