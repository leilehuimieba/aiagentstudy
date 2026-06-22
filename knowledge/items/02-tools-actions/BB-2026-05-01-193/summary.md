# BB-2026-05-01-193 Summary

## Article

- Title: Stop Manual Log Checking: Diagnose Bugs with AI + MCP in One Click
- Source: BestBlogs / dbaplus社群
- URL: https://www.bestblogs.dev/en/article/3e018134
- Date: 05-13
- Topic: `02-tools-actions`
- Tags: MCP, Claude Code, AI Programming, Log Diagnosis, Bug Localization

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Based on the practical experience of the Dewu technology team, this article proposes an engineering solution for automating backend bug diagnosis using AI. The core idea is to encapsulate the fixed and time-consuming process of 'checking logs → extracting key information → scanning code → locating the problem' through the MCP (Model Context Protocol) and Claude Code's Skill mechanism. The article first explains the principles and configuration of the log platform MCP, allowing AI to obtain dynamic log data in real-time. It then focuses on the design of the /log-diagnosis Skill, including its complete execution chain (from traceId time estimation, paginated log retrieval, cross-service analysis to code localization), core capabilities (automatic token management, cross-service analysis, code linkage), and detailed installation and configuration steps. Through a real-world SQL bug case, the article demonstrates how AI automatically pulls logs, reconstructs the call chain, extracts SQL, and discovers a subtle bug caused by inconsistent field logic, ultimately locating the code and providing a fix. Finally, the article summarizes the key points for diagnosis efficiency and highlights the core idea: transforming an engineer's experience and workflow into reusable AI capabilities is the core competitiveness of engineers in the AI era.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
