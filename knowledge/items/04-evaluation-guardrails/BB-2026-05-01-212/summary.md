# BB-2026-05-01-212 Summary

## Article

- Title: Alibaba & Ant Group LoongSuite GenAI Observability Semantic Convention: From Unified Data Language to Large-Scale Implementation
- Source: BestBlogs / 阿里技术
- URL: https://www.bestblogs.dev/en/article/9dae62a9
- Date: 05-12
- Topic: `04-evaluation-guardrails`
- Tags: Observability, OpenTelemetry, GenAI, AI Agent, Semantic Convention

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details the LoongSuite GenAI Observability Semantic Convention jointly launched by Alibaba and Ant Group. It first explains the core value of OTel SemConv as a unified observability data language, highlighting its key role in standardizing data metrics, supporting performance, cost, quality, and security governance, and reducing integration costs. The article then focuses on three major enhancements LoongSuite brings to OTel GenAI semantics: First, the addition of Entry/Step Spans to address the issue of overly long Trace chains in Agent long-running tasks, enabling clear display of Agent execution trajectories by round. Second, the addition of Skill semantics to provide observability for the business function aggregation layer, solving pain points such as functional domain attribution, health metric statistics, and link confusion. Third, the addition of Token-level inference observability, which extends observability from the request level down to the Token granularity. By collecting the generation time, sub-stage processes, and candidate probability distribution for each Token, it achieves white-box observability of the inference engine. The article also introduces the accompanying GenAI Utils tool library, which uses a layered and decoupled architecture to encapsulate the complexity of the semantic convention into a simple API, significantly reducing the integration cost for instrumentation library developers. Finally, two real-world cases demonstrate the practical effectiveness of Token-level observability in locating slow Tokens and addressing irrelevant answer issues.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
