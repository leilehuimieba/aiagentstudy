# BB-2026-05-01-639 Summary

## Article

- Title: 3 Agents. 3 LLMs. 1 Aging GPU: Engineering Parallel Inference on Bare Metal
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/0807a4a4
- Date: 06-25
- Topic: `01-context-memory`
- Tags: System Design, GPU Inference, AI Engineering, Multi-Agent Systems, Performance Optimization

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article addresses the practical challenge of running three AI agents, each using a different small LLM, on a single GTX 1080 with only 8 GB VRAM. The naive approach of launching separate llama-completion processes fails because each process pre-reserves a large KV cache for the full context window, causing the second and third processes to OOM. The author introduces lmxd, a ~1500-line C++ daemon that acts as a VRAM bookkeeper. Agents communicate with the daemon over a Unix socket using a simple text protocol (REGISTER, DECODE, etc.). The daemon maintains a ledger that enforces a 90% VRAM cap, admits new agents only if the estimated memory fits, and loads models in a shared backend to avoid redundant CUDA context overhead. The article provides detailed code snippets, explains the critical order of operations (book before build), and presents benchmark results on the same hardware, showing that the daemon successfully admits all three agents where the naive approach admits only one. It also covers KV-swap mechanisms for time-slicing decode across agents, and draws an insightful analogy to Connection Admission Control (CAC) in cellular networks.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
