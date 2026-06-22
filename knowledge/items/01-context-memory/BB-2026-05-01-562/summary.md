# BB-2026-05-01-562 Summary

## Article

- Title: Building a 100x Cheaper Trace Judge with Fireworks
- Source: BestBlogs / LangChain Blog
- URL: https://www.bestblogs.dev/article/d92ae42f
- Date: 06-15
- Topic: `01-context-memory`
- Tags: LLM, AI Agent, Fine-Tuning, Model Evaluation, AI Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details a collaboration between LangChain and Fireworks to build a cost-effective 'Trace Judge' for mining signals from production agent traces. The core idea is to detect 'Perceived Error'—when a user believes the assistant made a mistake—a general-purpose signal applicable across applications. The team fine-tuned a Qwen-3.5-35B model using LoRA SFT on Fireworks, training it on data from one internal dataset (chat-langchain) and testing its transferability to another (Fleet). Results show the fine-tuned model matches or exceeds frontier models (like GPT-4 and Claude Opus) in accuracy, while being 10-100x cheaper to serve. The article also discusses the data preparation process, the use of model-assisted labeling with human review, and future research directions for trace understanding and continual learning.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
