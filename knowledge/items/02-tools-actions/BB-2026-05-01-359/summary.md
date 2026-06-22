# BB-2026-05-01-359 Summary

## Article

- Title: Beyond the Menu Tree: How Yelp Built a Smarter Customer Success Chatbot with AI
- Source: BestBlogs / Yelp Engineering and Product Blog
- URL: https://www.bestblogs.dev/article/4293d345
- Date: 05-27
- Topic: `02-tools-actions`
- Tags: RAG, LLM, Chatbot, Vector Database, FAISS

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article from the Yelp Engineering Blog describes the evolution of their Customer Success chatbot from a static, rule-based system to a dynamic, LLM-powered conversational agent. The core innovation is a Retrieval Augmented Generation (RAG) pipeline that intelligently routes user queries into specialized workflows (QA, Billing, Refund, etc.). For the primary QA workflow, the team built a lean and highly accurate vectorstore by embedding only the metadata (title, summary, headers) from their ~370 Support Center articles, rather than the full article text. This approach, using OpenAI's text-embedding-ada-002 and FAISS for search, resulted in a compact 8MB in-memory index with a 94% recall@5. The article also covers their daily update pipeline for fresh knowledge, a solution for mitigating LLM hallucination of hyperlinks, and future plans for improvement. The project resulted in a doubling of the chatbot's resolution rate.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
