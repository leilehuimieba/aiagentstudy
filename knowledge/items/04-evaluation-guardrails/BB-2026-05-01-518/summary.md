# BB-2026-05-01-518 Summary

## Article

- Title: The Truth of Scaling Law Lies in Those "Useless" Parameters / Hao Chat Trends
- Source: BestBlogs / 腾讯科技
- URL: https://www.bestblogs.dev/article/23d850ea
- Date: 06-15
- Topic: `04-evaluation-guardrails`
- Tags: Scaling Law, LLM, Model Training and Inference, Parameter Redundancy, Attention Sink

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Starting with the ShortGPT pruning experiment (removing a quarter of LLaMA-2-13B's layers with almost no drop in MMLU), the article introduces the "parameter redundancy puzzle." The author breaks down the model lifecycle into three stages—training, inference, and post-training—to reveal the four identities of redundant parameters: 1) During training, large parameters provide "isolation space" for long-tail tasks, protecting them from gradient interference from high-frequency tasks; 2) During training, some attention heads achieve numerical pressure relief by dumping useless attention onto the Beginning-of-Sequence (BOS) token, satisfying the Softmax normalization constraint; 3) During inference, intermediate layers perform information compression (compression valley), providing stable input for the multi-step reasoning chains in the final 15% refinement layers; 4) During post-training, redundant parameters act as a "plasticity reserve," offering write space for fine-tuning and preventing catastrophic forgetting. The article cites multiple cutting-edge findings, including a joint Stanford-Anthropic study, Oxford University's "curse of depth," NYU's pruning limits, and a paper co-authored by Yann LeCun. The final conclusion: Scaling Law has not hit a wall; rather, mainstream benchmarks (like MMLU) fail to measure the real gains in long-tail task retention, deep computational chain construction, and plasticity reserve.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
