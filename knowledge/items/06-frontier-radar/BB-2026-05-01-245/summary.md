# BB-2026-05-01-245 Summary

## Article

- Title: Next-Generation Large Model Inference Network Architecture: How ZCube Effectively Breaks the Network Bottleneck?
- Source: BestBlogs / 智谱
- URL: https://www.bestblogs.dev/article/dee23cb3
- Date: 05-21
- Topic: `06-frontier-radar`
- Tags: ZCube, Network Architecture, PD Separation, Large Model Inference, AI Computing Cluster

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details the ZCube network architecture jointly proposed by Zhipu AI, XunYin Network, and Tsinghua University, aimed at solving the increasingly severe structural network congestion problem in large model PD-separated inference scenarios. The article first demonstrates through controlled experiments that network bandwidth is a key factor affecting inference throughput and latency. It then analyzes the load hotspots and PFC backpressure issues in the traditional RoFT architecture caused by the source-destination asymmetry of KV Cache transmission in PD-separated inference. The core innovation of the ZCube architecture lies in: eliminating the Spine layer switches, adopting a fully flat network topology, dividing Leaf switches into odd and even groups with a complete bipartite graph interconnection, and connecting the two ports of the GPU NIC to the two groups of switches via single-rail and multi-rail methods respectively. This design ensures only one optimal path between any pair of GPUs, fundamentally avoiding multi-path routing conflicts and achieving ideal load balancing across all switches in the network. In real-world tests on a thousand-card GLM-5.1 coding production cluster, compared to the RoFT architecture, ZCube saves 1/3 of the switch and optical module costs while increasing the average GPU inference throughput by over 15% and reducing the TTFT P99 by 40.6%. The architecture has been running stably for over two weeks, proving that architectural innovation is an effective path to unlocking hardware potential.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
