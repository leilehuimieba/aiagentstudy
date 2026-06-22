# BB-2026-05-01-442 Summary

## Article

- Title: Big News! Anthropic's Internal Skills Experience Revealed!
- Source: BestBlogs / Datawhale
- URL: https://www.bestblogs.dev/article/eceaa686
- Date: 06-07
- Topic: `01-context-memory`
- Tags: AI Coding, Claude Code, Skills, Prompt Engineering, AI Workflow

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article is an in-depth compilation and interpretation of Anthropic's official blog post "Lessons from building Claude Code: How we use Skills." It first corrects the common misconception of equating a Skill with a prompt, pointing out that a Skill is more like a folder organized around a task, which can contain documents, scripts, templates, examples, and hooks. The core content is divided into three main parts: First, Anthropic internally categorizes Skills into 9 types, covering the complete software workflow from filling knowledge gaps (library/API reference), adding verification (product verification), supplementing data (data fetching), to integrating processes (business process automation), building scaffolding (code scaffolding), conducting reviews (code quality), and connecting to production (CI/CD, runbooks, infrastructure ops). Second, the writing principles emphasize focus, prioritize verification (recommending engineers spend a week polishing it), prioritize recording gotchas (details the team knows by default but the model doesn't), avoid writing content the model already knows, use SKILL.md as a table of contents rather than a catch-all, leave room for judgment, and design setup and description in advance. Third, the evolution direction after a Skill matures: developing memory (persistent logs), scripts (pre-built helper functions), and on-demand hooks (e.g., /careful to intercept high-risk operations), as well as team-level distribution (repo check-in or marketplace) and governance (sandbox trial before formal inclusion). The article also mentions that Skills can be combined and that usage metrics can be tracked using the PreToolUse hook.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
