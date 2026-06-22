# BB-2026-05-01-398 Summary

## Article

- Title: HorizonVault Deep Dive: Achieving 100GB/s+ Distributed Storage Throughput on HDDs / Dewu Tech
- Source: BestBlogs / 得物技术
- URL: https://www.bestblogs.dev/article/897d1f95
- Date: 05-27
- Topic: `06-frontier-radar`
- Tags: Distributed Storage, Kafka, HDD, High Throughput, System Design

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article provides an in-depth analysis of HorizonVault, a distributed storage engine developed by the Dewu Tech team. Designed for high-capacity, low-cost scenarios such as Kafka remote storage and cold/warm data tiering, its core goal is to deliver high throughput, low jitter, and recoverable storage capabilities on commodity HDDs. Following a performance-centric approach, the article breaks down HorizonVault's overall architecture, including: disk-based storage structures (DiskStore, Replica, Log/Index), a write path based on sequential appending and a read path based on indexing, disk governance and thread isolation mechanisms, network backpressure control, state-aware scheduling between Broker and Meta, Leader/Follower HA replication strategies, and seamless integration via the Kafka Tiered Storage plugin. The article emphasizes that by elevating disks to first-class system resources and building a closed-loop scheduling system operating around a resource pool, HorizonVault successfully transforms the capacity advantage of commodity HDDs into cluster-level throughput while localizing issues like slow disks or replicas, achieving a unified balance of performance, cost, and stability.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
