# BB-2026-05-01-355 Summary

## Article

- Title: From TF-IDF to Transformers: Implementing Four Generations of Semantic Search
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/c60fa5c1
- Date: 05-25
- Topic: `01-context-memory`
- Tags: Semantic Search, TF-IDF, Sentence Transformers, Fine-tuning, DistilBERT

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article provides a hands-on, educational walkthrough of four generations of semantic search systems, using the task of comparing a student's art critique with expert critiques as a consistent example. It begins with a rule-based system combining TF-IDF cosine similarity with heuristic features like keyword overlap and recency. The second method replaces handcrafted rules with supervised learning, using Logistic Regression on TF-IDF features to classify critiques as expert-like or novice-like. The third method introduces dense semantic embeddings from a Sentence Transformer, enabling similarity comparisons based on meaning rather than exact vocabulary. The final method fine-tunes a DistilBERT transformer model for contextual classification. The article discusses the strengths and limitations of each approach, emphasizing the trade-off between interpretability and semantic understanding, and highlights the progression from human-designed features to learned representations.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
