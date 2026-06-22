# BB-2026-05-01-231 Summary

## Article

- Title: Claude Code Error Rate Drops from 41% to 11%: Why Karpathy's 4 Rules Aren't Enough
- Source: BestBlogs / 高可用架构
- URL: https://www.bestblogs.dev/en/article/1d6460e3
- Date: 05-11
- Topic: `04-evaluation-guardrails`
- Tags: Claude Code, CLAUDE.md, AI Coding, Prompt Engineering, Karpathy

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article delves into how carefully designed CLAUDE.md files can significantly improve the stability and consistency of Claude AI coding. The author first acknowledges the value of Karpathy's original 4 rules (think first, simple over complex, surgical edits, goal-driven), noting they can reduce an error rate of roughly 40% to below 3%. However, the author argues that these 4 rules primarily address coding issues from January 2026 and fail to cover new challenges emerging in May 2026, such as agent orchestration, multi-step workflows, and token budgets. Therefore, based on 6 weeks of real-world data from 30 codebases, the author adds 8 new rules: avoid having the model perform non-linguistic work, set hard token budgets, expose conflicts rather than compromise, read before writing, test intent over behavior, set checkpoints for multi-step tasks, follow codebase conventions, and fail loudly. The article explains the necessity of each new rule through concrete examples and provides a complete 12-rule CLAUDE.md file ready for copy-pasting. The author emphasizes that CLAUDE.md should be a behavioral contract customized to your own failure modes, not a wishlist, and offers advice on installation and rule pruning.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
