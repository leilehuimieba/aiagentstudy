# BB-2026-05-01-546 Summary

## Article

- Title: Tencent Hunyuan AI Infra New Open Source: Comprehensive Upgrade of HPC-Ops Inference Core Operators
- Source: BestBlogs / 腾讯混元
- URL: https://www.bestblogs.dev/article/f8d006eb
- Date: 06-11
- Topic: `06-frontier-radar`
- Tags: AI Infra, LLM, Inference Optimization, Open Source Project, Operator Library

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article is an official release from the Tencent Hunyuan AI Infra team regarding a major upgrade to its open-source inference operator library, HPC-Ops. It details the technical principles, design concepts, and performance data of five core operators: Attention adopts runtime dynamic load scheduling to address long-tail latency, achieving a 2.95x speedup for long-text scenarios; Router GEMM uses a dual BF16 combination to simulate FP32 precision, achieving up to a 3.22x speedup over FP32 cuBLAS while maintaining high accuracy; FusedMoE integrates the entire MoE inference process into a unified pipeline, delivering a 1.2x-1.6x performance improvement over vLLM/SGLang; Fused AllReduce+Norm deeply fuses communication and normalization computation, achieving up to a 1.68x speedup; Sampler fuses over a dozen kernels into 2, achieving a 4.0x-7.5x speedup over vLLM. All capabilities are derived from Tencent Hunyuan's online production practices and have been fully open-sourced.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
