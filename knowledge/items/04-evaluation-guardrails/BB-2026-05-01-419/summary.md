# BB-2026-05-01-419 Summary

## Article

- Title: How to Know If an Agent Has Actually Finished Its Task?
- Source: BestBlogs / 赛博禅心
- URL: https://www.bestblogs.dev/article/0ddbfe70
- Date: 05-26
- Topic: `04-evaluation-guardrails`
- Tags: Agent Evaluation, SaaS-Bench, Computer-Use Agent, CUA, Benchmark

## Model Mapping

- Blocks: Evaluation, Guardrails, Control Loop
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article introduces the SaaS-Bench evaluation benchmark proposed by UniPat Lab, designed to address the shortcomings of existing agent evaluations (such as OSWorld and Tau2) that focus solely on operational actions while ignoring final outcomes. SaaS-Bench packages 23 open-source SaaS applications (e.g., Mattermost, OnlyOffice, ownCloud) into Docker containers to build a realistic office environment. Agents must complete real business tasks that span multiple software applications and involve long steps (97.3% of tasks exceed 100 steps). The evaluation criterion is no longer 'whether the operation is correct,' but rather whether the task is truly completed by directly querying the database state through a verifier. The article presents leaderboard results: Opus 4.7 and GPT-5.5 lead significantly in multimodal tasks, but even the highest score is below 50%. It also analyzes the relationship between task length and success rate, the advantage of multimodal models in text-only tasks, and the phenomenon of agents 'faking it' between intent and state. Finally, it points out that the SaaS-Bench environment can stably generate high-quality CUA training data, which is valuable for tackling agent applications in office scenarios.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
