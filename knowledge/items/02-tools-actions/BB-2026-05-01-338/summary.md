# BB-2026-05-01-338 Summary

## Article

- Title: How Are Agent Skills in Large Language Models Carried in the Underlying LLM HTTP Interaction Flow?
- Source: BestBlogs / 腾讯云开发者
- URL: https://www.bestblogs.dev/article/0858ab05
- Date: 05-28
- Topic: `02-tools-actions`
- Tags: Agent Skill, Tool Calling, Cursor, LLM Protocol, AI Programming

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Using the author's self-implemented mp-read Skill as an example, the article provides a detailed breakdown of the underlying interaction flow of Agent Skill under the OpenAI-compatible protocol through 7 steps. The core conclusion is that Skill does not exist at the protocol level at all; it is 'compiled' by clients like Cursor into a combination of three protocol primitives: System/Developer Message injection instructions, Tools Definition for registering tools, and Multi-turn Tool Calling for looped execution. Starting with Skill discovery and description summary injection, the article progressively demonstrates how the LLM loads the SKILL.md file via the Read tool, executes pre-checks according to instructions, initiates core commands, and finally generates a response. Through real HTTP request/response JSON examples, the author concretizes abstract concepts and summarizes a complete protocol mapping table, revealing the elegance of this design pattern in fully reusing existing protocols without requiring any extensions.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
