# BB-2026-05-01-332 Summary

## Article

- Title: Embeddings Aren’t Magic: The Predictable Failure Modes of RAG Retrieval
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/47f5946d
- Date: 05-30
- Topic: `01-context-memory`
- Tags: RAG, Embeddings, Enterprise AI, Retrieval, Vector Search

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article, part of a larger series on enterprise document intelligence, provides a rigorous, empirical analysis of embedding models used in RAG retrieval. It begins by showcasing what embeddings do well: handling conceptual proximity, synonyms, typos, cross-lingual matching, and common polysemy. However, the core argument is that these successes are largely limited to public vocabulary seen during training. The article then systematically catalogs the predictable failure modes of embeddings in enterprise contexts. These include: (1) failure on specialist terms not in the model's training distribution (e.g., 'pool' in insurance), (2) a structural inability to distinguish term similarity from answer relevance (e.g., 'What is the capital of France?' retrieves 'Capital of Italy'), (3) complete blindness to negation, (4) inability to handle numerical magnitudes and thresholds, and (5) signal dilution in long documents. The author argues that these failures are architectural, not fixable by swapping to a larger embedding model or adding a reranker. The proposed solution is a shift in architecture towards strong upstream filtering using expert-curated keywords and document structure, rather than relying on embeddings as a magic bullet.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
