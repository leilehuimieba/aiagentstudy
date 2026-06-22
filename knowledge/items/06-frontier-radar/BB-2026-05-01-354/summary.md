# BB-2026-05-01-354 Summary

## Article

- Title: Slack AI: The Path to Multi-Cloud
- Source: BestBlogs / Slack Engineering
- URL: https://www.bestblogs.dev/article/51b98efd
- Date: 05-28
- Topic: `06-frontier-radar`
- Tags: Multi-Cloud, AI Infrastructure, AWS Bedrock, GCP Vertex AI, LLM Serving

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article chronicles Slack AI's architectural evolution over three years, moving through four distinct phases to achieve a multi-cloud, multi-model AI serving platform. Starting with AWS SageMaker, the team faced operational overhead and model feature lag. They migrated to Amazon Bedrock for managed simplicity and immediate model access, but encountered efficiency gaps with Provisioned Throughput. This led to a hybrid strategy combining Provisioned and On-Demand capacity, and the development of an intelligent routing layer with model hierarchies and circuit breakers. The final phase expanded to Google Cloud's Vertex AI, creating a true multi-cloud footprint for infrastructural redundancy, model-to-feature optimization, and access to innovation. The article details the technical challenges, trade-offs, and engineering solutions at each stage, emphasizing the importance of abstraction layers, gradual migration, and cross-functional alignment.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
