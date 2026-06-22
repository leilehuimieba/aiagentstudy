# BB-2026-05-01-517 Summary

## Article

- Title: 80% Speed Boost for On-Device AI? How to Make Qwen3-VL Fly on Your Phone
- Source: BestBlogs / 通义实验室
- URL: https://www.bestblogs.dev/article/2e22b643
- Date: 06-11
- Topic: `02-tools-actions`
- Tags: AI Coding, LLM, On-Device Inference, Model Deployment, Arm SME2

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Written by an engineer from the Tongyi Lab, this article serves as a practical engineering tutorial for on-device AI developers. It focuses on the SME2 instruction set of the Armv9 architecture, explaining its principle of achieving efficient matrix multiplication through the ZA matrix accumulator. Using Alibaba's open-source MNN inference engine, the article details a complete deployment workflow: compiling from source (with SME2 support enabled), downloading and converting the model, verifying via command line, and building an Android application. It provides specific compilation commands, model deployment steps, and performance testing methods, presenting real-world test data from a vivo X300: 81% speedup in the Prefill phase and 13% speedup in the Decode phase. Finally, the article also covers advanced tuning methods for model export and runtime parameters.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
