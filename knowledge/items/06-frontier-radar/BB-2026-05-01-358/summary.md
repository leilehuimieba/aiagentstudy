# BB-2026-05-01-358 Summary

## Article

- Title: Welcome NVIDIA Cosmos 3: The First Open Omni-model for Physical AI Reasoning and Action
- Source: BestBlogs / Hugging Face Blog
- URL: https://www.bestblogs.dev/article/d3576a02
- Date: 06-01
- Topic: `06-frontier-radar`
- Tags: NVIDIA Cosmos 3, World Foundation Model, Physical AI, Mixture-of-Transformers, Omni-Model

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

NVIDIA has released Cosmos 3, a major advancement in world foundation models for physical AI. Unlike previous versions that required separate models for world generation, reasoning, and policy generation, Cosmos 3 is a unified omni-model built on a Mixture-of-Transformers (MoT) architecture. It processes text, image, video, audio, and action modalities within a single framework, using an autoregressive subsequence for reasoning and a diffusion subsequence for generation, connected via joint attention. The release includes two model sizes: Cosmos 3 Nano (8B parameters) for workstation-grade GPUs and Cosmos 3 Super (32B parameters) for large-scale synthetic data generation and research. Cosmos 3 is available on Hugging Face with Diffusers integration, post-training scripts on GitHub, and a set of open synthetic data generation datasets for robotics, autonomous driving, and warehouse safety. The model supports multiple input-output modality combinations including text/image/video to video, video to text/action, and image/text to video and action, making it suitable for applications like robot policy learning, autonomous driving simulation, and synthetic training data generation.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
