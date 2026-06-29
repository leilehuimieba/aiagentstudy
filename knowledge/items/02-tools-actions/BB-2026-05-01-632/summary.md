# BB-2026-05-01-632 Summary

## Article

- Title: CHAP: Collaborative Human Agent Protocol
- Source: BestBlogs / Hacker News - Newest: "AI Agent"
- URL: https://www.bestblogs.dev/article/c077a653
- Date: 06-24
- Topic: `02-tools-actions`
- Tags: AI Agent, AI Development, Protocol, Audit Trail, MCP Protocol

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

CHAP (Collaborative Human Agent Protocol) addresses the problem of tracking human edits and decisions in AI agent workflows. It defines a set of methods and envelope structures (task.create, decide.override, audit.read) that allow agents to draft artifacts and humans to override them with structured diffs, rationales, and tags. These overrides are chained by content hash, forming an immutable audit trail. The protocol includes optional profiles for security signing and transparency logs. The repository provides TypeScript and Python reference implementations, MCP and A2A server transports, conformance tests, and twelve worked scenarios. CHAP does not replace MCP or A2A but sits alongside them as a recording layer for shared human-agent work.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
