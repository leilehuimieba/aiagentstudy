# BB-2026-05-01-435 Summary

## Article

- Title: RAG Is Not Machine Learning， and the ML Toolkit Solves the Wrong Problem
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/5265f8ad
- Date: 06-02
- Topic: `01-context-memory`
- Tags: RAG, Machine Learning, Information Retrieval, Enterprise AI, Search Systems

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article presents a strong thesis: RAG is not machine learning, and applying the ML toolkit to RAG projects is the most expensive misconception in enterprise RAG today. It argues that ML solves prediction problems where the true answer is unknown, while RAG solves retrieval and generation problems where the answer already exists in the document. The author identifies three specific ML reflexes that misfire in RAG: hyperparameter optimization (chunk size, top-k, etc.) which treats configuration choices as learnable parameters; evaluation datasets with train/test splits which measure coverage and quality, not generalization; and explainability frameworks like SHAP which are unnecessary because RAG is inherently explainable via citations and trace logs. The article advocates for a structural engineering approach: route questions by type, evaluate per failure mode, and amplify domain expertise rather than replace it. It concludes by framing RAG as a search engine plus an LLM scribe, with two distinct failure modes that require different diagnostic paths.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
