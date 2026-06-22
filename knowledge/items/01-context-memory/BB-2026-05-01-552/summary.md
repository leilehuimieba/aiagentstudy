# BB-2026-05-01-552 Summary

## Article

- Title: Miles Project Technical Analysis (2) — Key Technologies
- Source: BestBlogs / 罗西的思考
- URL: https://www.bestblogs.dev/article/10a1a93e
- Date: 06-16
- Topic: `01-context-memory`
- Tags: Agentic RL, Reinforcement Learning, LLM, AI Agent, Training Framework

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This is the second article in the technical analysis series on the Miles project, focusing on the key technologies that upgrade the Slime research-grade RL framework into an Agentic-first enterprise production system. The article elaborates on 8 core technical points: agentic_tool_call acts as a decoupling adapter between Agent business logic and RL training infrastructure, using separation of concerns to allow Agent developers to focus solely on business logic; TITO (Token-In, Token-Out) addresses the tokenization drift issue in multi-turn Agent RL caused by the Chat Template's loop.last, ensuring strict token prefix consistency through incremental tokenization; the Session Server serves as the productized shell of TITO, providing stateful multi-turn session management; the training-inference consistency spectrum progresses from fully asynchronous to bit-level consistency, including staleness filtering, TIS/MIS, R3 route replay, and True On-Policy contracts. The article also covers Multi-Agent collaborative training, environment design, the MBridge model abstraction layer, and the RadixTree prefix reuse middleware. The content is technically deep and logically clear, offering systematic solutions to the engineering challenges in Agentic RL training.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
