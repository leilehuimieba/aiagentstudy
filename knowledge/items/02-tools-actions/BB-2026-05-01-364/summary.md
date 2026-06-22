# BB-2026-05-01-364 Summary

## Article

- Title: How We Built an Interactive UI for LLMs with A2UI + Vue
- Source: BestBlogs / 哔哩哔哩技术
- URL: https://www.bestblogs.dev/article/1b6b25f2
- Date: 05-27
- Topic: `02-tools-actions`
- Tags: A2UI, Generative UI, Vue Renderer, AI Assistant, LLM

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article focuses on the core challenge of evolving AI assistants from text output to interactive interface generation. Based on a unified AI assistant framework, Bilibili's commercial advertising team identified the limitations of template-based solutions in complex multi-business scenarios and chose Google's A2UI protocol as the foundation. They developed a custom Vue renderer and a complete Agent toolchain, forming a comprehensive generative UI system. The article elaborates on key designs such as Runtime Schema assembly, a dual validation mechanism (structural and transitional validation), dual SSE channel output, and Wrapper component extensions. This solution achieves frontend-backend decoupling and protocol standardization, reducing business integration time from days to hours, and empowering the Agent with true interface generation capabilities. The article also demonstrates the complete workflow from user prompt input to component rendering through chart and form DEMO examples.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
