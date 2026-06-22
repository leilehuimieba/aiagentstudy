# BB-2026-05-01-462 Summary

## Article

- Title: Thousand Token Wood: shipping a multi-agent economy on a 3B model
- Source: BestBlogs / Hugging Face - Blog
- URL: https://www.bestblogs.dev/article/d15e5749
- Date: 06-06
- Topic: `03-control-loop`
- Tags: AI Agent, LLM, Small Language Models, Multi-Agent Systems, Simulation

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article is a detailed field report from the Build Small Hackathon, documenting the creation of 'Thousand Token Wood', a tiny multi-agent economy simulation. The author explains why a small 3B model (Qwen2.5-3B) was chosen over a frontier model for its speed and cost-effectiveness, enabling real-time multi-agent interaction. The core engineering challenge was bridging the gap between the model's reliable JSON output (100% valid) and its poor economic reasoning, which was solved through sharper prompting and a tolerant parsing layer. The article highlights the necessity of 'designed scarcity' (diet variety, spoilage, a winter fuel crisis) to create meaningful economic activity and prevent market stagnation. A key feature is the 'Wood Legend' system, which injects historical market events (like Tulip Mania or a bank run) as real shocks, causing emergent, unscripted market behavior. The report concludes with quantitative results from a representative run and practical takeaways for building with small models, emphasizing structure and prompting over scale.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
