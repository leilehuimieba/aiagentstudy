# BB-2026-05-01-455 Summary

## Article

- Title: Xiaomi MiMo， Explore and Love
- Source: BestBlogs / Hacker News
- URL: https://www.bestblogs.dev/article/bcd97e15
- Date: 06-08
- Topic: `02-tools-actions`
- Tags: LLM, Model Inference, Quantization, Speculative Decoding, AI Infrastructure

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article announces the release of Xiaomi MiMo-V2.5-Pro-UltraSpeed, a 1-trillion-parameter model capable of over 1000 tokens/s decode speed, achieved through deep collaboration between the MiMo model team and the TileRT inference system team. The key technical innovations include: (1) selective FP4 quantization of MoE Experts to dramatically reduce model size while preserving capability; (2) DFlash, a block-level masked parallel prediction method for speculative decoding that achieves high acceptance lengths (6.30 in coding scenarios); and (3) TileRT's paradigm-level execution model with persistent engine kernels and warp specialization, eliminating operator boundary overhead. The model is available via a limited-time, application-based API from June 9-23, 2026, at 3x the cost of the standard model but delivering approximately 10x the generation speed. The checkpoint has been open-sourced on HuggingFace. The article argues that breaking 1000 tps at the trillion-parameter scale represents a paradigm shift, enabling real-time decision loops, multi-path reasoning, and dramatically accelerated coding agents.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
