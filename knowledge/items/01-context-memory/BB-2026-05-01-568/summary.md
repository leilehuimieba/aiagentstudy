# BB-2026-05-01-568 Summary

## Article

- Title: We Open-Sourced MiniMax M3
- Source: BestBlogs / MiniMax 稀宇科技
- URL: https://www.bestblogs.dev/article/cecfce08
- Date: 06-15
- Topic: `01-context-memory`
- Tags: Model Release, Open-Source Model, Multimodal AI, LLM, Sparse Attention

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article is the official announcement from MiniMax regarding the open-sourcing of the M3 model. It first introduces the core technical features of M3: 428B total parameters, 23B activated parameters, making it the first open-source model to undergo multimodal mixed training from the pre-training stage. By leveraging large volumes of interleaved text, images, and other modality data, it achieves deep cross-modal semantic fusion. Concurrently, the MSA (MiniMax Sparse Attention) technical paper was released, detailing the architecture and engineering implementation to significantly reduce computational costs for long contexts. The article then showcases market feedback two weeks post-launch: achieving the highest ranking among open-source models on the Artificial Analysis Comprehensive Intelligence Index, ranking first among domestic models on the Vals.AI leaderboard, and citing positive feedback from industry figures such as the CEO of Vercel and the founder of Y Combinator. The article also addresses developers' primary concerns regarding service stability and cost, announcing that output speed has been increased from approximately 30 TPS to approximately 80 TPS, with plans for a further 30-40% improvement. Additionally, a Token Plan usage dashboard has been launched. Finally, the article elaborates on M3's design philosophy: ensuring high intelligence levels in complex reasoning, long-text, and multimodal scenarios while making it accessible and affordable for developers and enterprises.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
