# BB-2026-05-01-340 Summary

## Article

- Title: Build agents， not pipelines
- Source: BestBlogs / Sean Goedecke
- URL: https://www.bestblogs.dev/article/572b4e71
- Date: 05-31
- Topic: `03-control-loop`
- Tags: LLM Agents, Pipelines, AI Architecture, Software Engineering, Context Gathering

## Model Mapping

- Blocks: Goal, Control Loop, Tools/Actions, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article presents a clear dichotomy for using LLMs in software: pipelines, where control flow is defined in code, and agents, where the LLM manages control flow using tools. It argues that while pipelines offer predictability and are suitable for strict context size or cost constraints, agents are smarter and more flexible, especially for complex tasks like coding. The author details how context-gathering is far easier for agents, as they can fetch information on demand, whereas pipelines require complex upfront assembly (e.g., RAG), which often fails. The article also discusses trade-offs in multi-model pipelines, safety, and legibility, concluding that agents are more future-proof. Practical guidelines are provided, recommending agents when in doubt, as they are easier to build and more likely to solve the actual problem.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
