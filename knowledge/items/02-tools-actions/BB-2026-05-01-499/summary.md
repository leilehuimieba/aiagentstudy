# BB-2026-05-01-499 Summary

## Article

- Title: Her · हेर — a detective for your Claude Code sessions
- Source: BestBlogs / Hugging Face - Blog
- URL: https://www.bestblogs.dev/article/69db4622
- Date: 06-07
- Topic: `02-tools-actions`
- Tags: AI Agent, LLM, Developer Tools, Open Source, AI Safety

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article introduces Her (हेर), a tool built over a weekend during a Hugging Face hackathon. It addresses a common pain point: Claude Code sessions produce verbose JSONL trace files that are rarely read. Her ingests these files and provides a structured, human-readable investigation. It reconstructs the session's narrative, identifies risky actions (deploys, config changes, secret access), visualizes token and tool usage, and offers grounded suggestions for improvement. A key design principle is trustworthiness: the evaluation engine is deterministic, and the small language model (Nemotron-Mini-4B-Instruct) runs locally on the Hugging Face Space's GPU via ZeroGPU, with no data sent to third-party APIs. The tool also features a built-in copilot ('Ask Her') for querying the trace, and a tool identification database for recognizing common CLI tools. The article details the project's origin, its core features, the technical architecture (React frontend on Gradio, deterministic engine, local LLM), and the philosophy of suggesting rather than asserting.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
