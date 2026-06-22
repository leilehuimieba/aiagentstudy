# BB-2026-05-01-353 Summary

## Article

- Title: Face Intelligence Open-Sources Two Edge-Side Models: MiniCPM5-1B Beats 2B with 1B Parameters, BitCPM-CANN Unlocks 6x VRAM Efficiency
- Source: BestBlogs / 魔搭ModelScope社区
- URL: https://www.bestblogs.dev/article/d3bef8a8
- Date: 05-26
- Topic: `06-frontier-radar`
- Tags: Face Intelligence, MiniCPM5, BitCPM, Edge-Side Large Models, 1.58-bit

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Face Intelligence, in partnership with Tsinghua University and the OpenBMB open-source community, released two models during the Edge-Side Large Model Open Source Week. MiniCPM5-1B, with only 1B parameters, surpasses all models under 2B parameters (including Qwen3.5-2B) on the AA-Index. After INT4 quantization, its weights are only 0.5GB, enabling it to run on mobile phones, browsers, and even pure CPU environments. Its training data employs a tiered data governance system, and it open-sources the high-quality synthetic dataset Ultra-FineWeb-L3. BitCPM-CANN is a 1.58-bit ternary large model fully trained end-to-end on the Huawei Ascend platform, available in four sizes: 0.5B, 1B, 3B, and 8B. Compared to BF16, it unlocks approximately 6x VRAM efficiency while retaining 90%-97.2% of its capabilities. The article also details model deployment and fine-tuning methods, highlighting that the ForgeTrain framework was entirely written by AI, validating the feasibility of AI manufacturing AI.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
