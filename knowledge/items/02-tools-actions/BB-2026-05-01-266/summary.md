# BB-2026-05-01-266 Summary

## Article

- Title: A Smarter Google AI Edge Gallery: MCP integration， notifications， and session continuity
- Source: BestBlogs / Google Developers Blog
- URL: https://www.bestblogs.dev/article/ad850b1e
- Date: 05-19
- Topic: `02-tools-actions`
- Tags: Google AI Edge Gallery, MCP, On-Device AI, Gemma 4, Agentic Workflows

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article announces significant updates to the Google AI Edge Gallery app, a showcase for on-device AI. The key new features are threefold. First, experimental support for the Model Context Protocol (MCP) over Streamable HTTP, allowing the on-device Gemma 4 model to dynamically import tool definitions and coordinate complex tasks across external data sources like Google Workspace and Google Maps, with all reasoning happening locally. Second, a new 'Schedule Notification' skill enables proactive, automated routines, such as daily mood tracking or calendar briefings, triggered by local notifications. Third, the app now supports persistent chat history using the fast prefill capability of the LiteRT-LM backend, allowing sessions to resume almost instantly with full context. The article also highlights the open-source community's contributions and provides developer tips for optimizing MCP tool descriptions for on-device models.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
