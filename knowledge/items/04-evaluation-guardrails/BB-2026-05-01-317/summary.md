# [BB-2026-05-01-317] Summary

## Article

- Title: OWASP Benchmark - Benchmark Data Format
- Source: OWASP
- URL: https://owasp.org/www-project-benchmark/
- Date: 05-24
- Topic: `04-evaluation-guardrails`
- Tags: ground-truth, expected-results, benchmark-format, reproducibility, labeling

## Model Mapping

- Blocks: Evaluation, Memory
- Layer: engineering practice

## Core Takeaway

OWASP Benchmark 对 FlagHunter 的最大启发，不是它测的是 SAST，而是它把 ground truth 做成了可比对的数据文件：每个 test case 对应一个明确的 expected result。对 Phase 6.5 的 FlagProof 和 Phase 6 Replay Eval 来说，这意味着“证据对象”不能只存自由文本，而要尽量对齐到可 machine-check 的字段。只要 proof 和 expected outcome 的映射足够清晰，自动回放和自动验收就会稳定很多。

## Reusable Principle

- ground truth 应以结构化字段表示，避免只靠人工阅读。
- expected result 与 observed result 应可自动比对。
- 证据格式一旦固定，就能支持跨版本回归与误报/漏报分析。

## FlagHunter Relevance

- `ReplayEvalHarness`：将 expected flag / expected exploit effect 结构化保存。
- `FlagProof`：将 observed evidence 设计成可与 expected outcome 自动比较的格式。
- `EvaluationReport`：支持误报、漏报、偏差三类结果拆分。
