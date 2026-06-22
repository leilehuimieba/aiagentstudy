# BB-2026-05-01-399 Summary

## Article

- Title: DongSQL V1.2.0 Released: Deepening the Retail Database Kernel with Dual Leaps in Performance and Stability
- Source: BestBlogs / 京东技术
- URL: https://www.bestblogs.dev/article/bb9fd95c
- Date: 05-27
- Topic: `06-frontier-radar`
- Tags: DongSQL, Database Kernel, MySQL, Performance Optimization, Hot Row Update

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article, published by JD.com's retail database team, details the core technical upgrades of the self-developed database kernel, DongSQL V1.2.0. The new version achieves major breakthroughs in several key areas: significantly improving high-concurrency write and master-slave replication performance through group commit unicast notification and semi-synchronous replication optimization; introducing execution plan caching to avoid regenerating execution plans, notably enhancing OLTP query performance; expanding the support scope for single-point query optimization, adding support for unique indexes and VARCHAR/CHAR types; innovatively utilizing file extended attributes (xattr) for ultra-fast startup of massive tables, reducing startup time for millions of tables from minutes to seconds; using AVX2 instruction set to accelerate SQL digest computation; most notably, the hot row update optimization, through a batch merge mechanism for SQL layer cache updates, achieves up to a 9x TPS improvement and a 95% latency reduction in high-concurrency scenarios; additionally, it adds support for stress testing with live traffic, porting of the Statement Outline feature (version 5.7), and multiple monitoring and performance optimizations. The article provides detailed performance test data and best practice recommendations, showcasing JD.com's deep expertise in database kernel technology.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
