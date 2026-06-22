# BB-2026-05-01-505 Summary

## Article

- Title: SQL Compliance Rate Raised to 95%: A Full Analysis of De Wu Data Warehouse's Harness Practice
- Source: BestBlogs / dbaplus社群
- URL: https://www.bestblogs.dev/article/f747d09f
- Date: 06-04
- Topic: `01-context-memory`
- Tags: AI Coding, LLM, AI Agent, Prompt Engineering, Developer Tools

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Based on the practice of the De Wu offline data warehouse team using an AI coding tool (Claude Code), this article deeply analyzes three core pain points in AI-assisted development: AI's 'memory loss' due to the context compact mechanism, unstable compliance enforcement, and rapid context depletion during large-scale requirement development. To address these issues, the author proposes a five-layer defense system based on the Claude Code Harness mechanism: hardcoding rules into CLAUDE.md for persistence, using Auto Memory for automatic accumulation, implementing automatic SQL compliance checks and dangerous DDL interception via hooks, isolating high token consumption operations with subagents, and modifying the SKILL file invocation method. The article provides detailed configuration code, script examples, and workflow designs for each layer, along with a complete implementation roadmap. Ultimately, the author summarizes this approach as an upgrade from 'AI writing code for me' to 'AI embedded in the development pipeline,' with the core being the migration of semantics and rules from the unreliable LLM memory to deterministic hooks and persistent files.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
