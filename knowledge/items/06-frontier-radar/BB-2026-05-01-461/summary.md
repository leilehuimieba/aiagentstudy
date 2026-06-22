# BB-2026-05-01-461 Summary

## Article

- Title: Stop Writing Specs, Start Writing Facts — The Entire SDD Movement Is Obsolete
- Source: BestBlogs / 王俊博客
- URL: https://www.bestblogs.dev/article/225fb88f
- Date: 06-05
- Topic: `06-frontier-radar`
- Tags: AI Coding, LLM, Engineering Practices, Software Engineering, Testing & Quality

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Author Jaroslaw Wasowski retracts his previous article advocating for SDD, pointing out the core contradiction: a Spec is a statistical prediction about an LLM, not a verifiable contract. The non-deterministic nature of LLMs, the Intent Gap, and Spec Drift are systemic issues that cannot be fixed with better prose. The article proposes a Facts-first paradigm: Facts are machine-verifiable executable assertions (tests, properties, contracts) that remain unchanged across model upgrades. This concept traces back to a 57-year tradition of formal methods, starting with Hoare triples in 1969. The author honestly identifies three scenarios where SDD still applies (compliance and regulation, cross-team B2B integration, onboarding new hires) and provides a 90-day migration plan (Audit → Shift → Gate), emphasizing starting to write one fact tomorrow.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
