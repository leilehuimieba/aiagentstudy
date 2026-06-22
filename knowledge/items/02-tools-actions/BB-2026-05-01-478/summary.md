# BB-2026-05-01-478 Summary

## Article

- Title: EVA-Bench Data 2.0: 3 Domains， 121 Tools， 213 Scenarios
- Source: BestBlogs / Hugging Face - Blog
- URL: https://www.bestblogs.dev/article/f4bf8cb2
- Date: 06-04
- Topic: `02-tools-actions`
- Tags: LLM, AI Agent, Voice Agent, Benchmark, Enterprise AI

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article announces the release of EVA-Bench Data 2.0, a significant expansion of the enterprise voice agent benchmark. It introduces two new domains—Enterprise IT Service Management (ITSM) and Healthcare HR Service Delivery (HRSD)—alongside the original Airline Customer Service Management (CSM), totaling 213 evaluation scenarios across 121 tools. The post details five core design principles: voice-first scope, realism, variety, authentication, and reproducibility. It explains the joint generation process using the SyGra pipeline, which creates three interdependent components (user goal, initial database, expected final state) in a single pass to ensure consistency. A multi-stage validation loop, including structural checks, LLM-based consistency checks, and trace verification, is described. The article also covers manual review and a final frontier model validation pass. Deep dives into the ITSM and HRSD domains highlight their unique challenges, such as complex policy hierarchies and domain-specific terminology. Finally, it previews upcoming multilingual support, adapting scenarios for languages like French with localized names, locations, and phone numbers. The dataset, evaluation framework, and leaderboard are all open-source.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
