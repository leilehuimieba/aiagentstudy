# BB-2026-05-01-344 Summary

## Article

- Title: Interpreter Skills: Building Workflows for Agents
- Source: BestBlogs / LangChain Blog
- URL: https://www.bestblogs.dev/article/1bc76c41
- Date: 05-29
- Topic: `02-tools-actions`
- Tags: Agent Skills, Interpreter, LangChain, Deep Agents, Agent Workflows

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This blog post from LangChain introduces a new concept called 'interpreter skills,' which extends the existing agent skills framework. Traditional skills provide agents with instructions (via a SKILL.md file) on how to perform a task, but rely on the model to follow those instructions correctly. Interpreter skills add a TypeScript module (e.g., index.ts) that the agent's built-in interpreter can import and execute directly. This shifts the deterministic part of a routine from fallible prompt instructions to reviewable, testable, and version-controlled code. The post argues that this approach combines the best of two worlds: the flexibility and discretion of modern agent harnesses (where the model decides *when* to use a skill) with the reliability and verifiability of traditional, predefined workflows. It provides a detailed example of a GitHub repository triage skill, where the agent calls a single function that spawns subagents, clusters issues, and returns a structured result, avoiding the model's tendency to lose coherence over long, multi-step tasks. The post also discusses how interpreter skills can be used to manage agent state and answers common questions about their design, positioning them as a solution for making critical agent subroutines more robust and evaluable.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
