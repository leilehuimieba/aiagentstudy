# BB-2026-05-01-524 Summary

## Article

- Title: How Open-Weight Models Changed the AI Landscape
- Source: BestBlogs / ByteByteGo Newsletter
- URL: https://www.bestblogs.dev/article/380212f2
- Date: 06-16
- Topic: `01-context-memory`
- Tags: LLM, Open-Weight Models, MoE Architecture, AI Engineering, Model Training

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article argues that the rise of open-weight models has fundamentally changed the pace of AI innovation by enabling public, indirect collaboration between competing teams. It begins by clarifying the distinction between 'open-weight' and 'open-source' models, noting that while trained parameters are public, training data and code often remain private. The core of the analysis focuses on the Mixture-of-Experts (MoE) transformer architecture, which has become the common skeleton for all frontier open-weight LLMs. The article explains how MoE separates total parameters (knowledge capacity) from active parameters (compute cost), making large models practical. It then examines three key areas where teams make divergent design choices: attention strategies (GQA, MLA, Sparse Attention), expert count and sparsity (ranging from 16 to 384 experts), and post-training approaches (RL with verifiable rewards, distillation, synthetic agentic data). The article highlights a 'borrow-and-build' pattern, using examples like DeepSeek's MLA being adopted by Kimi K2, and DeepSeek's sparse attention being adopted by Zhipu AI's GLM-5, with each team contributing novel infrastructure (e.g., MuonClip optimizer, Slime framework) that the next team can build upon. The conclusion emphasizes that while specific models will be overtaken, the framework for understanding their design choices will remain relevant.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
