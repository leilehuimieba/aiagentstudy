# BB-2026-05-01-652 Summary

## Article

- Title: A Three-Phase Factual Recall Circuit in Gemma-2B and Gemma-12B-IT
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/2f139dd0
- Date: 06-24
- Topic: `01-context-memory`
- Tags: Mechanistic Interpretability, Activation Patching, LLM, Gemma, Factual Recall

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author designs a battery of 60 clean/corrupt prompt pairs across 20 fact categories and uses activation patching with TransformerLens to isolate factual recall circuits in Gemma-2B and Gemma-12B-IT. A novel metric called TotalSwing is introduced to rank prompt pairs by signal strength. Four experiments progressively narrow down from full residual stream to individual attention heads. Results reveal a consistent three-phase circuit: (1) Storage in the residual stream at the entity token position (layers 0-14 in 2B, 0-27 in 12B), (2) Distributed routing via attention heads (no single dominant head), and (3) Readout as a pass-through in the final layers (layers 15-17 in 2B, proportionally in 12B). The circuit replicates at scale, but tokenizer differences cause dataset drift between models, a caveat for cross-model comparisons. The author discusses future work including path patching and SAE analysis, constrained by disk space limitations. The full codebase is open-sourced.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
