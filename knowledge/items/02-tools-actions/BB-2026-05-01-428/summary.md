# BB-2026-05-01-428 Summary

## Article

- Title: A Guide to AI Cold Starts on Cloud Run
- Source: BestBlogs / Google Cloud Blog
- URL: https://www.bestblogs.dev/article/de02b525
- Date: 05-28
- Topic: `02-tools-actions`
- Tags: Cloud Run, Cold Starts, GPU, Serverless, AI Inference

## Model Mapping

- Blocks: Tools/Actions, Product Workflow, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article addresses the common challenge of high latency (up to 20 seconds) during AI model cold starts on Google Cloud Run. It deconstructs the cold start into four phases: Infrastructure Provisioning (~5s), Container Image Streaming (1-2s), Engine Initialization (5-15s), and Model Loading & VRAM Transfer. The core of the guide focuses on optimizing the final, most impactful phase by recommending the fastest storage option (Cloud Storage with concurrent download), using quantized models (e.g., 4-bit) and fast formats (GGUF, Safetensors), and ensuring VRAM fit. It also details infrastructure levers like Startup CPU Boost and Direct VPC Egress, and provides a formula for tuning concurrency to maximize throughput and avoid scale-out events. Scaling strategies include a single-region 'always-on' approach, a 'wake-up call' pattern using non-inference endpoints, and proper tuning of startup probes. The article concludes with lessons from Elastic's production deployment, which uses `enforce_eager=True` in vLLM and standalone LoRA checkpoints to minimize startup time.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
