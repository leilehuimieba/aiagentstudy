# BB-2026-05-01-365 Summary

## Article

- Title: RenderFlow: Agentic Code Delivery Practices for Baidu's Vertical Search Presentation Service
- Source: BestBlogs / 百度Geek说
- URL: https://www.bestblogs.dev/article/315cb4a3
- Date: 05-25
- Topic: `03-control-loop`
- Tags: LLM, Code Generation, Agentic Delivery, Executable Engine, Multi-round Repair

## Model Mapping

- Blocks: Goal, Control Loop, Tools/Actions, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details the RenderFlow system developed by Baidu's online search architecture team, aimed at addressing pain points in traditional manual delivery processes for search result presentation scenarios. Traditional approaches suffer from long delivery cycles, repetitive adaptations, and high adjustment costs. RenderFlow builds an Agentic delivery loop around "generation, execution, feedback, repair, and release." Its core design includes: an executable engine (based on the Yaegi interpreter, decoupling logic from services, supporting dynamic loading and minute-level activation), a multi-round repair mechanism (using Coder/Reviewer dual-role collaboration and monotonically accumulating repair constraints to reduce manual intervention to below 5%), and a quality assurance system spanning pre-release, during-release, and post-release phases. Since deployment, the system has compressed single-scenario delivery cycles from days to minutes and supports nearly a thousand scenarios in production. The article concludes with practical insights, noting that while the approach offers strong production controllability in well-defined scenarios, it has limitations such as performance ceilings in interpreted execution and the need for manual intervention in complex scenarios.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
