# BB-2026-05-01-624 Summary

## Article

- Title: Frontend AI Coding for Scenario Marketing — AI Native Visual Restoration from Design Drafts
- Source: BestBlogs / 大淘宝技术
- URL: https://www.bestblogs.dev/article/6bd595a6
- Date: 06-24
- Topic: `01-context-memory`
- Tags: AI Coding, AI Agent, Frontend Development, Visual Restoration, Design Tools

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Starting from the pain points of visual restoration in the AI Coding era, the article analyzes multiple structural contradictions of traditional D2C platforms: reliance on manual layer selection, image slicing, multi-state recognition, and decoupling of visual restoration from business logic. The core insight is that design drafts should enter the Agent workflow as reference materials, not as full data pushes. Tarot Pixel's design philosophy is 'Don't build a pipeline, build a library': it exports design drafts once into structured HTML previews, provides REST APIs for the Agent to query on demand—the engineering layer handles noise reduction and data extraction, while the AI layer focuses on semantic understanding. The Agent autonomously decides implementation methods within a closed loop of 'Observe → Plan → Execute → Reflect', and supports continuous conversational corrections. The article also compares two approaches—Pencil (IDE native) and Figma MCP—and emphasizes that tools should be built for AI, providing precise context in natural formats.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
