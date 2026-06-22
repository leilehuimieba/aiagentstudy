# BB-2026-05-01-333 Summary

## Article

- Title: The VibeSec Reckoning
- Source: BestBlogs / Martin Fowler
- URL: https://www.bestblogs.dev/article/2fd44471
- Date: 05-27
- Topic: `04-evaluation-guardrails`
- Tags: Vibe Coding, AI Security, Software Engineering, DevSecOps, Harness Engineering

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article recounts the experience of the Thoughtworks Global Marketing AI applications team when asked to scale a video assembly prototype built by a citizen builder using Gemini, Replit AI, and Claude AI. The team discovered two critical security near-misses: the AI recommended making a storage bucket public and assigning excessive token permissions to a service account. These incidents led the author to argue that relying on prompts to ensure security is insufficient. The article presents a framework for 'harness engineering' that combines inferential controls (like a structured security context file fed to the AI) with deterministic computational sensors (like SAST scanners and deployment gates). It provides actionable short-term habits for individuals and medium-to-long-term organizational strategies, including a daily security intelligence feed and shared starter harnesses, to ensure that the speed of AI-assisted development does not compromise security.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
