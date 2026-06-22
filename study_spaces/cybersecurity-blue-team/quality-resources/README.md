# 优质网安资料源目录

> Created: 2026-06-18
> Scope: 长期可复用的高质量网络安全资料源、训练资源、检测工程资源和年度报告。

这个目录和 `frontier-radar/` 分工不同：

- `frontier-radar/` 追踪“正在发生什么”：最新漏洞、攻击活动、供应链事件、AI/Agent 新风险。
- `quality-resources/` 沉淀“长期值得反复用什么”：官方标准、权威知识库、检测规则、DFIR 报告、训练靶场、年度趋势报告。

## 文件

- [cybersecurity-quality-source-catalog-2026-06-18.md](cybersecurity-quality-source-catalog-2026-06-18.md): 人读版目录，按用途分组。
- [source-catalog-2026-06-18.jsonl](source-catalog-2026-06-18.jsonl): 机器可读源清单，适合后续接入采集、打标签和检索。
- [non-x-source-expansion-2026-06-18.md](non-x-source-expansion-2026-06-18.md): 非 X 来源扩展路线，后续优先从 advisory、邮件列表、IR 报告、扫描态势和研究机构采集。
- [multi-source-traditional-vuln-collection-2026-06-18.md](multi-source-traditional-vuln-collection-2026-06-18.md): 多源传统漏洞采集策略，X、论坛、社区可作为线索，但入库要回链官方/原厂/研究报告。

## 质量分级

| 等级 | 含义 | 使用方式 |
|---|---|---|
| S | 官方、标准、原厂、权威年度报告 | 可作为事实和框架依据 |
| A | 一线研究、公开规则库、真实事件复盘 | 可作为攻击链、检测、实验样本依据 |
| B | 社区训练、课程、博客、靶场 | 可作为学习和练习来源，重要结论需要回链 |

## 推荐使用顺序

1. 先用 S 级来源确认事实、术语和框架。
2. 再用 A 级来源补攻击链、日志证据和检测规则。
3. 最后用 B 级来源做练习、题解和手感训练。
