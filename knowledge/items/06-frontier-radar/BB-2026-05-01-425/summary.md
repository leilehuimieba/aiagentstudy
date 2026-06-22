# BB-2026-05-01-425 Summary

## Article

- Title: Step 3.7 Flash: A High-Efficiency Flash Model for Production-Grade Agents
- Source: BestBlogs / 魔搭ModelScope社区
- URL: https://www.bestblogs.dev/article/8d048f58
- Date: 05-29
- Topic: `06-frontier-radar`
- Tags: StepFun, Step 3.7 Flash, MoE, Multimodal, Agent

## Model Mapping

- Blocks: Model, Tools/Actions, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

StepFun has officially released and open-sourced the Step 3.7 Flash model, which is specifically designed for production-grade agent scenarios. Key features include: a sparse MoE architecture with 196B total parameters + 1.8B ViT, with only 11B activated parameters, achieving a balance between model capability and inference efficiency; a maximum generation speed of 400 Tokens/s, suitable for high-frequency, multi-turn agent applications; native multimodal understanding capabilities for processing complex visual inputs such as UI, charts, and documents; enhanced web search and visual search capabilities; and excellent tool calling performance, supporting highly reliable calling and orchestration of external systems like APIs, browsers, and terminals. The model has been adapted to mainstream agent frameworks including Claude Code, OpenClaw, and Hermes Agent, supports MCP/Skills protocols, and is available on the ModelScope community. The article also provides a detailed deployment guide, covering multiple deployment methods such as API calls, vLLM, SGLang, llama.cpp, and Transformers.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
