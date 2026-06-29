# BB-2026-05-01-616 Summary

## Article

- Title: Vector RAG Isn’t Enough — I Built a Context Graph Layer for Multi-Agent Memory
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/0b2a6406
- Date: 06-26
- Topic: `01-context-memory`
- Tags: Multi-Agent Systems, AI Memory, RAG, Context Graph, LLM Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author describes building a multi-agent system where agents frequently fail to recall decisions made by other agents, even when full transcripts are available. After identifying the issue as a structural retrieval problem rather than a token compression or staleness issue, they propose a context graph architecture that stores facts as (subject, predicate, object) triples in a NetworkX graph, enabling multi-hop traversal for join queries. A deterministic benchmark with 18 graded queries across five scenarios compares three architectures: raw history dump (61.1% accuracy, 490.9 tokens/query), vector-only RAG using TF-IDF (50.0%, 75.9 tokens/query), and the context graph (88.9%, 26.9 tokens/query). The graph wins both accuracy and efficiency, with the largest gap on join queries (80% vs 20%). The article also discusses two identified bugs—entity vocabulary mismatch and stale fact retrieval—and their fixes, which are critical for production use.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
