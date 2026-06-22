# BB-2026-05-01-437 Summary

## Article

- Title: How to Build an AI Support Agent That Knows When NOT to Answer Tickets
- Source: BestBlogs / freeCodeCamp
- URL: https://www.bestblogs.dev/article/f3be1fc9
- Date: 06-02
- Topic: `01-context-memory`
- Tags: AI Support Agent, RAG, Escalation-First Design, LLM Safety, Software Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article, written by a full-stack engineer who placed 9th out of 1,349 participants in a hackathon, argues that standard RAG-based AI support agents fail on sensitive tickets like fraud reports. The author proposes an 'escalation-first' design where a pure Python function, not an LLM, makes the routing decision. This decider routes tickets to one of three paths: a grounded reply, a polite template decline for benign off-topic requests, or an escalation to a human. The system also includes a two-judge consensus verifier with an arbiter for disagreements to ensure answer faithfulness. The article details the implementation, cost-saving measures like Jaccard pre-checks and caching, and honestly discusses five gaps in the author's own submission, emphasizing the critical importance of investing in a robust labeled dataset over over-engineering the pipeline.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
