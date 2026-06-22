# BB-2026-05-01-448 Summary

## Article

- Title: I Spent May Evaluating Different Engines for OCR
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/aba895ac
- Date: 06-04
- Topic: `01-context-memory`
- Tags: OCR, LLM, AI Evaluation, Document Processing, Benchmarking

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author conducted a hands-on experiment to evaluate 14 different OCR engines—ranging from classical open-source tools like Tesseract to modern specialized models and general-purpose vision-language models—against a diverse set of 93 documents. The documents spanned easy (clean invoices), medium (bank statements, tax forms), and hard (handwritten notes, legacy reports, charts) categories. Key metrics included Coverage (how much ground truth text was captured), Precision/Recall, and latency. The results showed that Gemini Flash 3.1 Lite was the best all-rounder for mixed production documents, Tesseract remains unbeatable for clean high-volume print, and Mistral OCR offers a cost-effective option for structured table extraction. The author emphasizes that there is no universal best engine; OCR is a routing problem where document type, cost, structure needs, and failure tolerance dictate the optimal choice. The article also discusses cost scaling, failure modes of different engines, and caveats about benchmark limitations.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
