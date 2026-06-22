# BB-2026-05-01-243 Summary

## Article

- Title: Maintainability sensors for coding agents
- Source: BestBlogs / Martin Fowler
- URL: https://www.bestblogs.dev/article/0c8ed596
- Date: 05-20
- Topic: `04-evaluation-guardrails`
- Tags: AI Coding Agents, Static Code Analysis, ESLint, Code Maintainability, Software Engineering

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Martin Fowler discusses the challenge of maintaining codebase maintainability when using AI coding agents, drawing from his experience rebuilding an internal analytics dashboard with AI. He defines maintainability as making it easy and low-risk to change code over time, noting that AI agents face similar issues as human developers in tangled codebases. The article focuses on using 'sensors'—tools that provide feedback to agents for self-correction. The primary sensor explored is ESLint, configured with custom rules targeting common AI failure modes like excessive function arguments, file length, and cyclomatic complexity. A key innovation is the use of custom ESLint formatters that provide guidance text, instructing the agent on how to handle warnings (e.g., making judgment calls on type suppression, or slightly increasing thresholds as a last resort). Fowler observes that AI frequently increased the cyclomatic complexity threshold, suggesting the guidance text was effective. He notes that managing warnings becomes more feasible with AI, as agents can handle the tedious task of suppression. The article concludes that the cost-benefit balance of static analysis has shifted: AI reduces the cost of creating custom rules, and the benefit increases by catching common AI mistakes. However, he warns against a false sense of security, as static analysis cannot catch semantic quality issues, and there is a risk of feedback overload leading to over-engineering.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
