# BB-2026-05-01-584 Summary

## Article

- Title: Baidu Open-Sources Unlimited OCR, Achieves Long-Range Parsing; Core Author 'YY' Suspected from DeepSeek
- Source: BestBlogs / 机器之心
- URL: https://www.bestblogs.dev/article/aa765f04
- Date: 06-23
- Topic: `01-context-memory`
- Tags: OCR, Document Parsing, Attention Mechanism, Long-Range Inference, Open Source Project

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article reports that Baidu has open-sourced the Unlimited OCR model. Building on DeepSeek OCR as a baseline, it replaces multi-head attention with Reference Sliding Window Attention (R-SWA), which limits the output-side KV Cache to a fixed window (default 128 tokens), thereby keeping computation and memory overhead constant during decoding, enabling true single-forward-pass long-range document parsing. Experiments show that Unlimited OCR achieves a total score of 93.23% on OmniDocBench v1.5, surpassing DeepSeek OCR by 6 percentage points, and performs consistently on complex layouts such as PPTs and magazines. In long-range tests, the edit distance for documents with 40+ pages is below 0.11, and Distinct-35 is approximately 97%. The article also analyzes the complementary relationship between R-SWA and DeepSeek OCR's encoder DeepEncoder, and speculates that the core author may be from DeepSeek, based on the technical report style, the author signature "YY", and personnel departures from DeepSeek.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
