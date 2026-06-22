# BB-2026-05-01-459 Summary

## Article

- Title: How to Stop Shipping Low-Quality RL Environments (with Examples)
- Source: BestBlogs / Latent.Space
- URL: https://www.bestblogs.dev/article/cdd6597f
- Date: 06-06
- Topic: `03-control-loop`
- Tags: RL, AI Agent, Training Infrastructure, Data Quality, Software Engineering

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This guest post by Auriel W, an RL practitioner at Gemini, presents a practitioner's perspective on the critical importance of RL environment (harness) quality. The author argues that a flaky harness is not a minor inconvenience but a systematic data poisoner, as in RL the environment generates the training data. The article categorizes common harness failures into three main classes: The Stale Cache (returning old data), The Reward Hack (agent gaming the metric), and The False Resolution (rewarding status changes over problem resolution). It also lists additional failures like silent timeout defaults, non-deterministic state resets, and action space drift. For each failure, the author provides a concrete example (e.g., a SaaS sales agent, a coding agent, a customer support agent) and traces how a single bug poisons an entire training episode. The article concludes with practical advice: maintain a failure rate below 5%, adopt traditional software engineering best practices for harnesses, and treat the training harness as an extension of the production product.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
