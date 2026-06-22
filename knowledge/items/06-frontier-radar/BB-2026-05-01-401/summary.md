# BB-2026-05-01-401 Summary

## Article

- Title: NVIDIA Dynamo Snapshot: Fast Startup for Inference Workloads on Kubernetes
- Source: BestBlogs / NVIDIA Technical Blog
- URL: https://www.bestblogs.dev/article/2c1ca519
- Date: 05-28
- Topic: `06-frontier-radar`
- Tags: NVIDIA Dynamo, Inference, Kubernetes, CRIU, Checkpoint/Restore

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This technical blog post from NVIDIA details the design and implementation of Dynamo Snapshot, a system for dramatically accelerating the startup of AI inference workloads on Kubernetes. The core problem is the cold-start delay, which can take several minutes as GPUs initialize engines, load weights, and warm up kernels. The solution leverages CRIU (Checkpoint/Restore in Userspace) and cuda-checkpoint to serialize and restore the full state of an inference worker. The post describes a Kubernetes-native architecture using a privileged DaemonSet (snapshot-agent) to manage checkpoints and restores without modifying runc. Key optimizations include: (1) unmapping and releasing the KV cache before checkpointing to drastically reduce artifact size, (2) modifying CRIU to use parallel memfd restore and Linux native AIO for memory restoration, achieving up to 7.9x speedup over upstream CRIU, and (3) introducing a GPU Memory Service (GMS) to decouple model weights from the process checkpoint, enabling concurrent restoration of process state and weights. The results show end-to-end restore times approaching speed-of-light, with a proof-of-concept achieving sub-5-second startup for a 120B parameter model, a 21x improvement over cold start.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
