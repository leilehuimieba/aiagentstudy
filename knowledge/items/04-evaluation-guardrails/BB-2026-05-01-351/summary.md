# BB-2026-05-01-351 Summary

## Article

- Title: Rebuilding Evaluation Benchmarks in the AI Era: Insights from 3,632 Vulnerabilities and the VulnGym Benchmark Release
- Source: BestBlogs / 腾讯技术工程
- URL: https://www.bestblogs.dev/article/54fbd42d
- Date: 05-26
- Topic: `04-evaluation-guardrails`
- Tags: VulnGym, Vulnerability Detection, Business Logic Vulnerabilities, AI Security, Evaluation Benchmark

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Based on a statistical analysis of 3,632 high-severity/critical GitHub Advisory vulnerabilities from January 2025 to April 2026, this article reveals a structural shift in vulnerability patterns in the AI coding era: the proportion of business logic vulnerabilities is continuously rising, reaching 47.2% in high-star projects by April 2026. The article analyzes the causes of this trend from two perspectives: the supply side (the proliferation of AI coding tools changing how vulnerabilities are introduced) and the detection side (AI security tools beginning to uncover previously hard-to-find business logic flaws). In response, Tencent's Wukong Security Team, in collaboration with institutions including the Chinese University of Hong Kong, Fudan University, the University of Hong Kong, Peking University, and the Institute of Information Engineering at the Chinese Academy of Sciences, has released the VulnGym evaluation benchmark. This benchmark uses real vulnerabilities from high-star GitHub projects as its data source, covering over 400 vulnerability paths, of which 71.2% are business logic vulnerabilities. It employs path-level annotation with three key elements: entry_point, critical_operation, and trace, supporting reproducible and interpretable deterministic evaluations. It can be used to compare the vulnerability detection capabilities of underlying models, Harness engineering, and Agent tools as a whole.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
