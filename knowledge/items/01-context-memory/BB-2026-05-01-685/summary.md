# BB-2026-05-01-685 Summary

## Article

- Title: Has no one ever questioned OPD's reward design? We found that log itself is the problem—maybe it shouldn't be used!
- Source: BestBlogs / 青稞AI
- URL: https://www.bestblogs.dev/article/3baad5ef
- Date: 06-28
- Topic: `01-context-memory`
- Tags: Model Training & Inference, Reinforcement Learning, Reward Design, Knowledge Distillation, Large Language Models

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article first points out that On-Policy Distillation (OPD) has become a standard component in post-training of large models, but mainstream sampled-token OPD (vanilla OPD) suffers from severe training pathologies: accuracy first drops then rises, response length oscillates, and final performance falls more than 8 points behind full-vocab OPD. By analyzing the reward distribution, the author identifies the root cause as the unbounded log-ratio reward (negative tail approaching -50), with extreme rewards concentrated in the early rollout stage and persisting throughout training. Comparing post-hoc fixes such as clip, tanh, and z-score, it is found that none can fundamentally solve the problem because log itself amplifies low-probability differences into extreme values. To address this, the author proposes PowerOPD: replacing log with the Box-Cox power transformation yields a family of bounded ([-1,1]) and sign-consistent rewards, and introduces a tunable parameter α as a "probability region selector" to filter low-probability noise. Experiments on multiple Qwen3 teacher-student settings and six mathematical reasoning benchmarks show that PowerOPD significantly outperforms vanilla OPD (average +4.47 Avg@8 / +4.06 Pass@8), surpasses all post-hoc methods, and even beats full-vocab OPD (up to +2.59 Avg@8 / +8.90 Pass@8), while saving 59.2% training time and 23.1% GPU memory. Gradient norm analysis reveals that PowerOPD gradients remain consistently in the 0.25-0.35 range, whereas vanilla OPD has an initial spike close to 1000 (a 3000x gap), demonstrating fundamental stability.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
