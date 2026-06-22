# BB-2026-05-01-281 Summary

## Article

- Title: Fine-Tuning NVIDIA Cosmos Predict 2.5 with LoRA/DoRA for Robot Video Generation
- Source: BestBlogs / Hugging Face Blog
- URL: https://www.bestblogs.dev/article/3f94f358
- Date: 05-19
- Topic: `06-frontier-radar`
- Tags: Cosmos Predict 2.5, LoRA, DoRA, Robot Learning, World Model

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article from the NVIDIA team on the Hugging Face Blog presents a comprehensive, practical guide for fine-tuning the Cosmos Predict 2.5 world model for robot video generation. It addresses the challenge of expensive real-robot data collection by proposing a scalable alternative: generating synthetic trajectories with a fine-tuned video world model. The core of the guide focuses on parameter-efficient fine-tuning (PEFT) using LoRA and DoRA, which inject small trainable adapters into the frozen 2B-parameter model, making it feasible on a single GPU. The article details the entire pipeline: setting up the environment, preparing the GR1-100 dataset, implementing the training loop with rectified flow loss, running inference with the fine-tuned adapter, and evaluating results using Sampson Error and LLM-as-a-Judge metrics. Quantitative results show that fine-tuning for 100 epochs significantly improves temporal stability, physical plausibility, and instruction following. The guide concludes with practical advice on choosing between LoRA and DoRA based on rank and budget, and provides links to the full codebase and further resources.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
