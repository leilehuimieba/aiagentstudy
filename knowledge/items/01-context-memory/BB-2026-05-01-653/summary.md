# BB-2026-05-01-653 Summary

## Article

- Title: Challenging Google Analytics: Building a Scalable， Cost-Effective User Tracking Service
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/1cf7be55
- Date: 06-22
- Topic: `01-context-memory`
- Tags: User Tracking, System Design, Data Engineering, Scalability, Cost Optimization

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article presents a detailed talk by Alina Krasavina, an engineering manager at Delivery Hero, on building and scaling an internal user tracking service (Perseus) to replace Google Analytics. It covers the motivations: migration necessity, real-time data needs, GDPR compliance, and cost control. The initial MVP used a simple API with Pub/Sub processors, which proved highly scalable. The rollout involved parallel testing with a double pipeline (sending data to both GA and internal service), progressive rollout across brands, and load testing with 3x peak traffic. After rollout, data quality improved from 85% to 97% (measured by order match rate), and cost dropped to 25% less than GA, later to 3x cheaper. Post-MVP challenges included data completeness (null standardization), backend reliability (pod restart data loss solved by synchronous requests and retries), and further cost optimizations (data archiving, JSON storage, cheaper nodes). SDK improvements like event prioritization, non-blocking queuing, and monitoring helped prevent data loss during A/B tests. A key innovation was code-generated event models that enforce data quality at compile time, reducing governance overhead. The talk emphasizes the value of a simplistic initial architecture, careful KPI selection, thorough testing, and incremental improvements.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
