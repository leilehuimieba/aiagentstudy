# 深挖：供应链投毒攻击链与实例

> Last updated: 2026-06-18

## 核心观点

供应链投毒不是“下载了一个坏包”这么简单。现代投毒的目标往往是开发者工作站、CI/CD Runner、发布权限、云身份和下游依赖生态。

典型攻击链：

```text
投毒入口
-> 安装时执行
-> 窃取开发/CI/CD/云凭证
-> 横向到代码仓库或云控制面
-> 重新发布更多恶意包
-> 删除日志、破坏数据或长期潜伏
```

## 常见投毒方式

| 技术 | 做法 | 为什么有效 |
|---|---|---|
| 维护者账号失陷 | 攻击 maintainer 的电脑、npm/GitHub 凭证 | 合法账号发布，信任链天然通过 |
| Typosquatting | 模仿热门包名、组织名、仓库元数据 | 利用拼写错误和信任迁移 |
| 生命周期脚本滥用 | `preinstall` / `postinstall` 自动执行 | 不需要业务代码 import，安装时就执行 |
| 恶意传递依赖 | 给可信包新增一个看似无害的依赖 | 源码逻辑不变，审查难度更高 |
| CI/CD 缓存投毒 | 污染 runner 缓存或依赖缓存 | 后续合法构建恢复缓存后执行攻击代码 |
| OIDC 信任滥用 | 利用 GitHub Actions 到云的信任关系换取临时云凭证 | 不需要长期云密钥，直接进入云控制面 |
| 有效 provenance 下的恶意构建 | 真实流水线被污染，仍能产生有效签名/证明 | provenance 证明“谁构建”，不证明“构建环境干净” |
| Worm 化传播 | 窃取 npm/GitHub token 后自动感染受害者可发布的包 | 影响面指数扩大 |

## 实例 1：Axios npm compromise

事件要点：

- 2026-03-31，两个恶意 Axios 版本被发布到 npm。
- 恶意版本不是大改 Axios 源码，而是注入 `plain-crypto-js@4.2.1` 这个依赖。
- 安装时脚本拉取第二阶段 RAT，覆盖 Windows、macOS、Linux。
- 上游 maintainer 后续披露，攻击与其账号/设备被入侵有关。

攻击链：

```text
维护者环境/账号被攻破
-> 攻击者发布 axios 恶意版本
-> 恶意依赖通过 postinstall 执行
-> 下载 OS 对应 RAT
-> 开发机或 CI Runner 被控
-> 凭证、token、代码仓库、云账号进入风险区
```

防御要点：

- lockfile 检查是否命中过恶意版本。
- 命中后不要只降级，要把开发机或 CI Runner 当成已失陷。
- 轮换机器上所有可能暴露的 token、密钥和凭证。
- 对高影响开源包采用 OIDC / Trusted Publishing / immutable release，但还要监控异常 publish。
- 禁用或限制自动升级，至少对关键依赖使用版本固定和变更审查。

## 实例 2：Typosquatted npm packages steal cloud and CI/CD secrets

事件要点：

- Microsoft 2026-05-28 披露，一名攻击者在 4 小时内发布 14 个恶意 npm 包。
- 包名模仿 OpenSearch、ElasticSearch、DevOps、环境配置相关库。
- 恶意包利用 npm 生命周期 hook 自动执行。
- 目标是 AWS、HashiCorp Vault、GitHub Actions、npm token 等云与 CI/CD 凭证。

攻击链：

```text
开发者误装 typosquat 包
-> preinstall 自动执行
-> 收集主机上下文并连接 C2
-> 下载/执行第二阶段载荷
-> 窃取 AWS、Vault、GitHub Actions、npm token
-> 利用 npm publish token 继续投毒下游包
```

检测思路：

- npm install 期间出现异常网络连接。
- `preinstall` / `postinstall` 执行未知脚本。
- CI Runner 访问 AWS IMDS、ECS metadata、Vault、Secrets Manager 的行为异常。
- npm token 被用于陌生 IP 或陌生时间窗口发布。

## 实例 3：QUIETVAULT / Nx 到 AWS 管理员

事件要点：

- Google Cloud Threat Horizons H1 2026 披露，Mandiant 处理过一起从 npm 包感染到云环境完全失陷的案例。
- 初始投毒来自 Nx npm 框架里的 QUIETVAULT，窃取开发者 GitHub PAT。
- 攻击者再利用 GitHub 到 AWS 的 OIDC 信任关系获取临时 AWS STS 凭证。
- 因 CloudFormation 角色过度授权，攻击者创建新 IAM 角色并附加 AdministratorAccess。
- 从开发者 endpoint 到 AWS 管理员权限，少于 72 小时。

攻击链：

```text
Nx/npm 供应链感染
-> 开发者插件/依赖更新触发恶意代码
-> GitHub PAT 被窃取
-> GitHub 环境侦察
-> 滥用 GitHub Actions OIDC 信任进入 AWS
-> CloudFormation 创建管理员角色
-> S3 数据外泄和生产环境破坏
```

关键教训：

- OIDC 比静态密钥安全，但信任策略写宽了，仍然会变成云接管路径。
- CI/CD 角色不能允许任意创建 IAM 角色或附加管理员策略。
- GitHub token、Actions 权限、云角色、CloudFormation 权限必须一起审计。

## 实例 4：Mini Shai-Hulud 与 worm 化投毒

Unit 42 在 2026-06 披露，npm 生态在 Shai-Hulud 之后进入更高后果阶段，攻击从零散 typosquat 变成系统化投毒和 worm 化传播。其报告提到：

- 2026-06-01，至少 32 个 `@redhat-cloud-services` npm 包被投毒。
- 2026-05，TanStack、Mistral AI、UiPath、OpenSearch 等生态受到影响。
- 攻击目标包括 GitHub token、npm token、SSH key、AWS/GCP/Azure 凭证、Kubernetes token、Vault secrets、CI/CD secrets。
- 有案例出现有效 SLSA provenance，但构建环境本身已被污染。

这说明单纯“看有没有签名/证明”不够。签名证明来源，不能证明构建过程中没有被恶意状态污染。

## 防御路线图

### 1. 开发者终端

- 开启 EDR，关注 npm/pnpm/yarn install 触发的异常进程和外联。
- 密钥不要长期放在本地环境变量、`.npmrc`、shell profile、项目目录。
- 使用短期 token 和细粒度 PAT。
- 对高价值 maintainer 强制硬件密钥、设备健康检查和独立发布设备。

### 2. 依赖治理

- 锁定版本，不对核心依赖使用过宽 semver。
- 新增依赖必须审查：包名、维护者、发布时间、下载量突变、install scripts、仓库和包内容是否一致。
- 对 install scripts 设默认拒绝或审计策略。
- 使用私有 registry/proxy，把未审查包隔离在进入内网之前。

### 3. CI/CD

- Runner 使用一次性环境，构建后销毁。
- 不把生产密钥注入普通 build job。
- GitHub Actions 权限默认最小化，`id-token: write` 只给需要发布的 workflow。
- 禁止 pull_request_target 直接 checkout 或执行 fork 代码。
- 缓存恢复要有边界，不能让 PR 污染 release cache。

### 4. 云身份

- OIDC trust policy 限制 org、repo、branch、workflow、environment。
- CI/CD 云角色禁止创建 IAM 管理员角色、附加 `AdministratorAccess`、修改自身 trust policy。
- 对 STS AssumeRole、CloudFormation IAM 创建、Secrets Manager 枚举、S3 批量读取做告警。

### 5. 应急处置

命中投毒包后，不要只删除依赖：

```text
冻结 affected runner / endpoint
-> 保存 npm/pnpm/yarn cache、lockfile、shell history、网络日志
-> 搜索恶意包名、hook、C2、异常进程
-> 轮换 GitHub/npm/cloud/Vault/K8s/CI/CD token
-> 检查是否有下游包被重新发布
-> 回滚到干净版本并重建 runner
```

## 参考来源

- Axios post-mortem: https://github.com/axios/axios/issues/10636
- Microsoft: Mitigating the Axios npm supply chain compromise: https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/
- Microsoft: Typosquatted npm packages used to steal cloud and CI/CD secrets: https://www.microsoft.com/en-us/security/blog/2026/05/28/typosquatted-npm-packages-used-steal-cloud-ci-cd-secrets/
- Google Cloud Threat Horizons H1 2026: https://cloud.google.com/security/report/resources/cloud-threat-horizons-report-h1-2026
- Unit 42: The npm Threat Landscape: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
