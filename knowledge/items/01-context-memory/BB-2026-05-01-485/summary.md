# BB-2026-05-01-485 Summary

## Article

- Title: Two Misconfigurations That Caused Spark OOM Failures on Kubernetes
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/72544a86
- Date: 06-03
- Topic: `01-context-memory`
- Tags: Spark, Kubernetes, Cloud Migration, Performance Optimization, Data Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article documents a real-world incident where a Spark batch pipeline, stable for years on-premises, began experiencing daily executor OOM failures after migrating to Azure Kubernetes Service (AKS). The author details a systematic investigation that ruled out common Spark tuning issues like heap undersizing and data skew. The root cause was traced to two compounded infrastructure misconfigurations introduced during the lift-and-shift migration: setting `spark.kubernetes.local.dirs.tmpfs=true`, which backed shuffle spill directories with node RAM instead of disk, and a hard `podAffinity` rule that forced all four executors onto a single 64GB node. This combination concentrated memory pressure, causing the kernel OOM killer to terminate executors during shuffle-heavy stages. The article provides a step-by-step timeline of the investigation, a clear root cause analysis explaining the compounding effect, and the specific fixes applied: disabling tmpfs, increasing scratch volume sizes from 1Gi to 10Gi, and replacing the hard affinity rule with a preferred podAntiAffinity. The resolution resulted in zero OOM incidents over six months. The article concludes with a practical OOM prevention checklist for Spark-on-Kubernetes deployments and discusses broader implications for cloud migrations.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
