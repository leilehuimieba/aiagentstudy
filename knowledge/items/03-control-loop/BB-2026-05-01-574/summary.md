# BB-2026-05-01-574 Summary

## Article

- Title: What to Do When Reflection Won't Fix Your AI Agent's Output
- Source: BestBlogs / freeCodeCamp
- URL: https://www.bestblogs.dev/article/4be45766
- Date: 06-23
- Topic: `03-control-loop`
- Tags: AI Agent, LLM, Prompt Engineering, Production AI, LangGraph

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author shares production experience at a large-scale web company where LLM reflection (having an LLM critique its own structured output) failed to reliably fix errors, often producing 'confidently wrong' approved output. The proposed solution separates error detection (using deterministic validators like JSON Schema and custom business rules) from error correction (feeding exact error messages back to the LLM for targeted fixes). A complete LangGraph implementation is provided, demonstrating a generate-validate-retry loop that achieves near-perfect correctness. The article also discusses when this pattern is applicable (deterministic constraints) vs. when subjective quality still requires reflection or human review. Key insight: LLMs are good at fixing specific errors but bad at finding their own; deterministic validators excel at perfect detection.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
