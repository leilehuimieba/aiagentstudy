# BB-2026-05-01-526 Summary

## Article

- Title: Spring AI 2.0.0 GA Available Now
- Source: BestBlogs / Spring Blog
- URL: https://www.bestblogs.dev/article/9ed27696
- Date: 06-12
- Topic: `01-context-memory`
- Tags: Spring AI, Java, AI Agent, MCP Protocol, LLM

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article announces the general availability of Spring AI 2.0.0, a major release that re-architects the framework on a Spring Boot 4 and Spring Framework 7 foundation. Key improvements include an upgrade to Jackson 3 for better JSON serialization, full JSpecify null-safety annotations, and a complete refactoring of the options and configuration properties system for consistency and immutability. The core project now focuses on a curated set of chat model providers (OpenAI, Anthropic, Amazon Bedrock, Google GenAI, Mistral AI, DeepSeek, Ollama), leveraging vendor SDKs. The most significant architectural change is the lifting of the tool-calling loop into the advisor chain, making it a composable, first-class component via the new `ToolCallingAdvisor`. This enables unified tool calling, progressive tool disclosure for scaling to hundreds of tools, and structured self-correcting output. The release also integrates the official MCP Java SDK 2.0.0, introduces an annotation-driven programming model for MCP servers and clients, and makes Streamable HTTP the default transport. New community extensions for event-sourced conversation memory and agentic patterns are highlighted.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
