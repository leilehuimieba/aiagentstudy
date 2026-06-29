# BB-2026-05-01-649 Summary

## Article

- Title: Water Cooler Small Talk， Ep. 11: Overfitting in RAG evaluation
- Source: BestBlogs / Towards Data Science
- URL: https://www.bestblogs.dev/article/2d145514
- Date: 06-26
- Topic: `01-context-memory`
- Tags: RAG, AI Evaluation, Overfitting, Machine Learning, Goodhart's Law

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article uses a water cooler anecdote to illustrate a subtle but common pitfall in RAG evaluation: treating the evaluation set as a development tool by iteratively tuning prompts or retrieval logic based on its results. This behavior effectively merges the evaluation set with the training process, leading to overfitting. The author explains the ML fundamentals of training/validation/test splits, then details three ways this happens in RAG—tuning prompts on the evaluation set, cherry-picking questions the system handles well, and building test questions from indexed documents. The antidote is to maintain a genuinely held-out test set, build questions independently of system behavior, and treat suspiciously high metrics with skepticism. The article also connects the issue to Goodhart's Law ('When a measure becomes a target, it ceases to be a good measure') and reward hacking, emphasizing that overfitting is a process discipline problem, not purely technical.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
