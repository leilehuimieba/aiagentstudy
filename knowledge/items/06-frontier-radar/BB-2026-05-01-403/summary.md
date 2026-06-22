# BB-2026-05-01-403 Summary

## Article

- Title: Reachy Mini goes fully local
- Source: BestBlogs / Hugging Face Blog
- URL: https://www.bestblogs.dev/article/604f370b
- Date: 05-27
- Topic: `06-frontier-radar`
- Tags: speech-to-speech, Reachy Mini, local AI, Hugging Face, open-source

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article details how to set up a fully local speech-to-speech pipeline for the Reachy Mini robot, eliminating the need for cloud servers and API keys. It introduces Hugging Face's `speech-to-speech` library, a cascaded pipeline (VAD → STT → LLM → TTS) that exposes a Realtime API-compatible WebSocket. The guide covers running the LLM locally with `llama.cpp` and Gemma 4, installing and configuring the speech-to-speech library, and connecting the robot. It then delves into customization, explaining the rationale for a local setup (privacy, cost, control) and offering opinionated defaults for VAD (Silero), STT (Parakeet-TDT), and TTS (Qwen3-TTS). The article extensively covers LLM options, including running models in-process with MLX or Transformers, or decoupling the brain via a Responses API with various backends like vLLM, Hugging Face Inference Endpoints, or OpenAI. It concludes with instructions for running the engine on a laptop while the app runs on the robot.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
