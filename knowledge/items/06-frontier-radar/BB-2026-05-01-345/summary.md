# BB-2026-05-01-345 Summary

## Article

- Title: Architecting Cloud-Native Kafka: From Tiered Storage Towards a Diskless Future
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/519d67f3
- Date: 05-26
- Topic: `06-frontier-radar`
- Tags: Apache Kafka, Cloud-Native, Tiered Storage, FinOps, KIP-848

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This comprehensive technical article examines the ongoing architectural transformation of Apache Kafka as it adapts to cloud-native environments. It begins by framing the economic pressures that drive this evolution, using a case study of Discover Financial Services to illustrate the cost realities of running Kafka in the cloud. The article then delves into several key Kafka Improvement Proposals (KIPs) that represent major architectural shifts. It covers KIP-405 (Tiered Storage), which decouples compute and capacity by moving cold data to object storage, and the associated FinOps risks like request amplification. The article details KIP-1267, which proposes cost attribution metrics for tiered storage, and provides a practical implementation guide using Prometheus and Grafana. It then explores KIP-848 (Next-Generation Consumer Rebalance Protocol), which enables safe Kubernetes autoscaling by eliminating stop-the-world rebalances. The article also discusses KIP-1134 (Virtual Clusters) for improved multi-tenancy and KIP-932 (Share Groups), which introduces queue-like semantics for partition-independent parallelism. Finally, it examines KIP-1150 (Diskless Topics), a controversial proposal to eliminate local broker disks entirely, weighing its potential for massive cost savings against significant trade-offs in latency, data integrity, and garbage collection. The article provides actionable guidance for architects and platform teams on when to adopt each new capability.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
