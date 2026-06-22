# 多源传统漏洞情报采集策略

> Date: 2026-06-18
> Purpose: 在 AI/Agent 风险之外，重新强化传统漏洞、企业基础设施、论坛讨论和多源交叉验证。

## 策略调整

后续不再排除 X，也不单押任何单一平台。

X、Reddit、Hacker News、论坛、微信群/社区转述都可以作为“发现线索”的入口，但进入知识库时要尽量回链到：

- 官方 CVE / NVD / CISA KEV。
- 原厂公告、发行版公告、项目安全公告。
- 一线研究机构技术分析。
- 专业论坛中的维护者答复、补丁状态、实际运维问题。
- DFIR 报告中的真实利用时间线。

## 传统漏洞优先观察面

1. **边缘设备和远程访问**：VPN、防火墙、SD-WAN、负载均衡、邮件网关、RDP 暴露面。
2. **企业中间件和业务系统**：Oracle PeopleSoft、SAP、Microsoft Exchange、Confluence、ActiveMQ、Revive Adserver。
3. **互联网基础协议和服务**：Exim、nginx/httpd/IIS/Envoy、HTTP/2、SMTP/TLS、DNS、SAML/OIDC。
4. **开发和基础设施工具**：HashiCorp Vault/Consul/Nomad/go-getter、CI/CD、template/rendering、MDX/SSR。
5. **供应链和包管理器**：npm、PyPI、GitHub Actions、容器镜像、Linux 发行版 backport。
6. **补丁状态和运维现实**：官方版本号、发行版 backport、临时缓解、禁用功能、是否需要重建镜像或轮换凭证。

## 高价值论坛 / 社区入口

### 技术讨论和维护者反馈

- Hacker News: https://news.ycombinator.com/
- Reddit r/netsec: https://www.reddit.com/r/netsec/
- Reddit r/linuxadmin: https://www.reddit.com/r/linuxadmin/
- Rocky Linux Forum: https://forums.rockylinux.org/
- HashiCorp Discuss Security: https://discuss.hashicorp.com/c/security/52
- F5 DevCentral: https://community.f5.com/

### 邮件列表和早期披露

- Full Disclosure: https://seclists.org/fulldisclosure/
- oss-security: https://www.openwall.com/lists/oss-security/
- Debian Security Announce: https://lists.debian.org/debian-security-announce/

### 论坛内容如何入库

论坛内容通常不直接作为最终事实，而是用于补充：

- 真实运维困惑：例如发行版包版本低但是否已 backport。
- 缓解取舍：例如临时禁用 HTTP/2 的兼容性和性能影响。
- 维护者反馈：例如某组件是否实际受影响。
- 社区复盘：例如漏洞根因、检测注意事项、误报和补丁坑。

## 采集模板

```text
主题：
漏洞 / 风险：
官方事实源：
技术分析源：
论坛 / 社区线索：
受影响资产：
攻击前提：
高层攻击链：
防御假设被破坏：
检测证据：
补丁 / 缓解：
Fulcrum 测试样本：
```

