# BB-2026-05-01-651 Summary

## Article

- Title: Krea 2 Open Source: 12B DiT Text-to-Image Dual Versions + Nine Official LoRAs Released, Now Available on ModelScope AIGC Section
- Source: BestBlogs / 魔搭ModelScope社区
- URL: https://www.bestblogs.dev/article/18283f68
- Date: 06-26
- Topic: `06-frontier-radar`
- Tags: Model Release, Text-to-Image, AI Image Generation, Open Source Model, LoRA

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article details the open-sourcing of Krea 2. Krea 2 is a 12B dense DiT text-to-image model that adopts the Qwen3-VL text encoder and Qwen Image VAE, ranking high on the Artificial Analysis text-to-image leaderboard. The open-source release includes Raw (base fine-tunable) and Turbo (8-step 2K image fast inference) dual versions, along with nine official LoRAs covering styles such as anime, photography, and painting. In terms of technical design, it draws on the LLM multi-stage training paradigm (pre-training → mid-training → SFT → PO → RL → distillation), introduces the STPO variant in the PO stage to avoid policy drift, uses multi-reward training in the RL stage (general aesthetics, instruction following, text rendering, artifacts and structure), and adopts Trajectory Distribution Matching (TDM) for distillation. The article also provides operational guidelines for online inference and training on the ModelScope AIGC section, as well as local deployment code examples based on DiffSynth-Studio, covering the full process of installation, inference parameters, and LoRA training.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
