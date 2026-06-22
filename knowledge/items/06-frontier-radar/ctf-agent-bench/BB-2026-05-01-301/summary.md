# [BB-2026-05-01-301] Summary

## Article

- Title: NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security
- Source: arXiv
- URL: https://arxiv.org/abs/2406.05590
- Date: 06-08
- Topic: `06-frontier-radar`
- Tags: ctf-benchmark, offensive-security, csaw, failure-analysis, tool-use

## Model Mapping

- Blocks: Context/State, Tools/Actions, Evaluation, Memory
- Layer: research

## Core Takeaway

NYU CTF Bench 把来自 CSAW 的 200 道题整理成开放数据集，并提供自动化框架与外部工具接入，适合做更大规模、更细粒度的 offensive-security 基准。论文最有价值的地方不只是“谁解出了多少题”，而是给出了失败分解：give up、round exceeded、connection failure、token exceeded、wrong answer。对 FlagHunter 来说，这些失败标签几乎可以直接映射成 stop_no_progress、wrong-flag recovery 和 observation 压缩的诊断维度。

## Reusable Principle

- 评测结果必须拆到 failure taxonomy，不能只看 solved 数。
- 题库要覆盖 crypto / forensics / pwn / rev / web / misc，避免 agent 针对单一题型过拟合。
- 把工具接入与题目元数据一并标准化，才能稳定复现 agent 表现。

## FlagHunter Relevance

- `ReplayEvalHarness`：直接借鉴“题目元数据 + Docker / 文件环境 + 自动判定”的数据组织方式。
- `Retrospective`：把 wrong answer、token exceeded、give up、round exceeded 作为一级失败标签写进回放结果。
- `ObservationStore`：若 token exceeded 占比高，说明需要更激进的 HTTP / 命令输出压缩策略。
