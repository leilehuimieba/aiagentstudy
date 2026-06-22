# BB-2026-05-01-348 Summary

## Article

- Title: GitHub Slashes Agent Workflow Token Spend up to 62% with Daily Audits and MCP Pruning
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/22bc26b4
- Date: 05-29
- Topic: `02-tools-actions`
- Tags: GitHub, Token Efficiency, Agentic Workflows, MCP, CI/CD

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

GitHub published a detailed case study on reducing token consumption in its own agentic CI workflows. The company achieved up to a 62% reduction in effective tokens (ET) by implementing a systematic optimization loop. Key strategies included pruning unused Model Context Protocol (MCP) tools, which add significant schema overhead per API call, and replacing MCP calls for common tasks like fetching pull request diffs with pre-downloaded `gh CLI` commands. To drive this optimization, GitHub built two specialized agents: a Daily Token Usage Auditor that aggregates consumption and flags anomalies, and a Daily Token Optimiser that reads source code and logs to file a GitHub issue with specific fixes. The team also introduced an 'Effective Tokens' (ET) metric to normalize cost across different model tiers, weighting output tokens by 4x and cache reads by 0.1x. Results across a dozen production workflows showed sustained reductions, with Auto-Triage Issues seeing a 62% drop. The article also notes the limits of MCP pruning, as one workflow saw no benefit because the tool manifests were a negligible fraction of its context. The Auditor and Optimiser agents are now available in the `gh-aw` CLI tool.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
