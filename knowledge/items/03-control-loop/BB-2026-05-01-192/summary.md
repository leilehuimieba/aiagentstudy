# BB-2026-05-01-192 Summary

## Article

- Title: "OncoAgent: A Dual-Tier Multi-Agent Framework for Privacy-Preserving Oncology Clinical Decision Support"
- Source: BestBlogs / Hugging Face Blog
- URL: https://www.bestblogs.dev/en/article/da90d61f
- Date: 05-09
- Topic: `03-control-loop`
- Tags: OncoAgent, Clinical Decision Support, Multi-Agent Systems, LangGraph, Corrective RAG

## Model Mapping

- Blocks: Goal, Control Loop, Tools/Actions, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This technical paper introduces OncoAgent, a comprehensive open-source system designed to assist oncologists with clinical decision-making while preserving patient privacy. The system features a dual-tier architecture that routes simple queries to a 9B parameter model and complex cases to a 27B deep-reasoning model, both fine-tuned via QLoRA on 266,854 oncological cases. A key innovation is the integration of a four-stage Corrective RAG pipeline over 70+ NCCN and ESMO guidelines, combined with a three-layer reflexion safety validator that enforces a strict Zero-PHI policy. The entire stack runs on a single AMD Instinct MI300X instance using ROCm, eliminating cloud API dependencies. The paper reports significant performance achievements, including a 56x throughput acceleration for synthetic data generation (6,800 vs. 120 cases/hour) and full-dataset fine-tuning in approximately 50 minutes. The system architecture decomposes clinical reasoning across eight specialized LangGraph nodes, each with bounded, auditable functions, and includes a mandatory human-in-the-loop gate for high-complexity cases.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
