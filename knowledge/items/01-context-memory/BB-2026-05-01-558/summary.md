# BB-2026-05-01-558 Summary

## Article

- Title: Beyond extract_text: The Two Layers of a PDF That Drive RAG Quality
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/13112ad8
- Date: 06-11
- Topic: `01-context-memory`
- Tags: RAG, PDF Parsing, LLM, Data Engineering, AI Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article is the first part of the parsing brick in a series on building enterprise RAG systems. It argues that effective PDF parsing for RAG requires two distinct layers. The first layer, covered here, focuses on understanding the document's nature: classifying its source software (e.g., Word, LaTeX, scanner), reading its declared metadata and native table of contents, and using these signals to route the document to the correct extraction strategy. The second layer analyzes page-level content, distinguishing native text from OCR layers, detecting images, vector tables, and multi-column layouts. A key innovation is the 'parsing_summary': a single, cached LLM call that produces a short factual summary of the document type, main subject, and key fields. This summary, placed in the question parser's system prompt, solves common RAG failures like the 'what is the name?' problem on a CV. The article uses PyMuPDF (fitz) for all extraction and provides concrete Python code for source detection, column analysis, and page classification. It emphasizes that structural signals (render mode, image coverage) are more reliable than statistical thresholds for making parsing decisions.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
