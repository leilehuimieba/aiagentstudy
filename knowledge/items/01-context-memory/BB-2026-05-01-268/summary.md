# BB-2026-05-01-268 Summary

## Article

- Title: Stop Idolizing RAG! Grep Makes a Comeback, Vector Indexing Becomes a Fallback?
- Source: BestBlogs / dbaplus社群
- URL: https://www.bestblogs.dev/article/3dcf5158
- Date: 05-18
- Topic: `01-context-memory`
- Tags: Claude Code, RAG, Grep, Code Search, AI Programming

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Centered on the core debate of 'Is RAG dead?', this article uses the leaked source code of Claude Code as a starting point to detail its zero-index code search mechanism. It first introduces Claude Code's core search loop: the LLM autonomously decides on a search strategy, using tools like GrepTool, GlobTool, FileReadTool, and AgentTool for iterative searches until sufficient information is gathered. Next, it delves into the performance principles of the underlying tool, ripgrep, including five layers of filtering, SIMD acceleration, and the Boyer-Moore algorithm. Real-world test data shows that for a developer's local project scale, brute-force scanning incurs only millisecond-level latency. The article also compares Claude Code with Cursor (dual-index architecture) and Codex (also zero-index), pointing out that architectural choice depends on data scale: zero-index is suitable for local projects, while indexing is geared towards large codebases. Addressing criticism of the Grep approach's high token cost, the article analyzes Claude Code's three-tier cost control mechanisms: prompt caching, auto-compaction, and sub-agent isolation. Finally, citing academic research (GrepRAG) and experimental data, it argues why exact matching outperforms semantic retrieval in code search, concluding that what is dying is not the RAG paradigm itself, but the default assumption that 'code search must rely on embedding pre-indexing'.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
