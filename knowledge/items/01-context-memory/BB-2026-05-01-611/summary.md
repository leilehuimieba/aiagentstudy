# BB-2026-05-01-611 Summary

## Article

- Title: When RAG Users Ask Vague Questions: Clarify Once， Learn the Default
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/b00e30e3
- Date: 06-22
- Topic: `01-context-memory`
- Tags: RAG, LLM, Question Parsing, Structured Output, Agent Design Patterns

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article extends the question-parsing brick of an enterprise RAG system to handle ambiguous fields common in production queries. It identifies five failure modes (ambiguous field type, missing page scope, ambiguous date scope, ambiguous intent, implicit entity) and introduces two Pydantic schemas: `ClarificationRequest` to ask the user and `ClarificationDefault` to learn from the answer. A worked broker example demonstrates the loop: first time the system asks, records the answer, and later reuses the learned default silently. The update rules and gate function are provided in Python. The pattern is positioned as distinct from multi-turn dialogue; it emphasizes learning across requests rather than within a conversation. The article also discusses boundaries, deferred concerns (multi-field, adversarial users, cross-tenant sharing), and how the pattern integrates with storage and evaluation infrastructure.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
