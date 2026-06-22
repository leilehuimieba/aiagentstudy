# BB-2026-05-01-218 Summary

## Article

- Title: bili-fe-workflow — Practices in Commercial Intelligent Development Workflow
- Source: BestBlogs / 哔哩哔哩技术
- URL: https://www.bestblogs.dev/en/article/12477550
- Date: 05-15
- Topic: `02-tools-actions`
- Tags: Harness Engineering, Intelligent Development Workflow, AI Programming, Frontend Engineering, MCP

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article systematically presents the Bilibili frontend team's practical achievements in AI-assisted development. The core idea is upgrading from scattered AI tool usage to a systematic workflow called Harness Engineering. The article first introduces the `.workflow` project knowledge base as infrastructure, providing AI with a comprehensive project overview and coding standards. It then breaks down several core workflows: `prd-preprocess` transforms raw product requirement documents into structured, actionable development documents, with AI performing requirement clarification and decomposition; `dev-workflow` is further divided into two paths: D2C (Design-Driven Code) and Dev (Requirement-Driven Code). The former automatically generates UI code from Figma design drafts and produces logic completion prompts, while the latter dynamically orchestrates skill sequences based on requirement complexity, enabling complete generation from technical plans to code. Additionally, automated testing workflows and AI Mock workflows are introduced. The article emphasizes that the core methodology of this system is "imitation" and "decomposition" — breaking down human developers' workflows into AI-executable steps, leveraging knowledge bases, MCP tools, and sub-agents to achieve long-task automation across the entire development lifecycle. The ultimate goal is to establish a new engineering consensus, transforming personal experience into shared intelligent development capabilities for the team.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
