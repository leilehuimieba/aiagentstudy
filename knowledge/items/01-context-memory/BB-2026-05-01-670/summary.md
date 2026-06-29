# BB-2026-05-01-670 Summary

## Article

- Title: Q&A: How KRAFTON Built PUBG Ally， a Co-Playable Character Powered by NVIDIA ACE
- Source: BestBlogs / NVIDIA Technical Blog
- URL: https://www.bestblogs.dev/article/f7655d96
- Date: 06-27
- Topic: `01-context-memory`
- Tags: AI Agent, Small Language Model, On-Device AI, Game AI, Speech Recognition

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

In this Q&A, KRAFTON's research lead and project manager explain the architecture and design decisions behind PUBG Ally, an AI teammate for PUBG: BATTLEGROUNDS that runs entirely on-device using NVIDIA ACE. The system combines automatic speech recognition, a quantized Mistral-NeMo-Minitron-2B small language model (SLM), and custom text-to-speech. Key engineering choices include running the SLM locally to avoid network latency, implementing a System 1/System 2 separation (behavior tree for reactive actions, language model for intent and speech), and constraining the game world to a single map and fixed item taxonomy for tractable domain adaptation. PUBG Ally supports English, Korean, and Chinese, uses teacher-student distillation for domain-specific knowledge, and includes structured long-term memory that persists across matches. The interviews also cover testing methodologies for non-deterministic AI, advice for other studios, and future directions for co-playable characters.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
