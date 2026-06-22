# BB-2026-05-01-362 Summary

## Article

- Title: The Implementation of AI Shopping Assistant on vivo's Official Website
- Source: BestBlogs / vivo互联网技术
- URL: https://www.bestblogs.dev/article/d2710aed
- Date: 05-27
- Topic: `02-tools-actions`
- Tags: AI Shopping Assistant, Agent Workflow, Intent Recognition, RAG, Prompt Engineering

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article systematically describes the entire process from technology selection to implementation of the AI shopping assistant feature in vivo's official website app. First, by comparing three approaches—fine-tuning large models, building dedicated models, and using Agent workflows—the Agent workflow was chosen based on cost-effectiveness, technical risk, and business suitability. The overall architecture adopts a four-layer design: Application Layer, Strategy Layer, Jiuwen Layer (Agent platform), and Xuanji Layer (large model computation). Core solutions include: using a FastText small model for intent recognition (inference time ~10ms), designing two agents for phone parameter interpretation and product recommendation, enhancing answer accuracy through Prompt engineering and RAG knowledge bases, and achieving structured display of product cards, large model streaming output, and related posts. After launch, the first-character response time was controlled within 2.5 seconds, positively contributing to business GMV and resolution rate.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
