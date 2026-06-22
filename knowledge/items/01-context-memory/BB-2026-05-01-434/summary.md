# BB-2026-05-01-434 Summary

## Article

- Title: Why Vector Search Alone Isn't Enough: Hybrid Retrieval for RAG
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/1986e257
- Date: 06-02
- Topic: `01-context-memory`
- Tags: RAG, Hybrid Retrieval, Vector Search, BM25, Reciprocal Rank Fusion

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article identifies a critical failure mode in production RAG systems: vector embeddings, while excellent at semantic similarity, systematically fail at distinguishing specific entities like version numbers, error codes, and feature flag names. The author argues that most real-world queries are hybrid, requiring both semantic understanding and exact-match precision. The article provides a deep technical analysis of why embeddings fail (they are approximation engines), explains how BM25's IDF, term-frequency saturation, and length normalization mechanisms provide the missing precision, and presents Reciprocal Rank Fusion (RRF) as the practical solution for combining the two ranked lists without score normalization. The article includes detailed walkthroughs of three query types (semantic, exact-match, hybrid) with concrete RRF score calculations, production implementation guidance for Elasticsearch, and tuning recommendations for rank constant, kNN candidates, and cross-encoder reranking. The conclusion is definitive: hybrid search with RRF is not a workaround but the architecturally correct approach for production RAG systems.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
