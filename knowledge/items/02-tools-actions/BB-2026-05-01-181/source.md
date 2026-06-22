# Source Evidence

- Title: QCon Beijing 2026 | Treating Automated Testing as AI Coding: A Practical Review of Xiaohongshu's GUI Agent
- BestBlogs URL: https://www.bestblogs.dev/en/article/852b6f4a
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247495245&idx=1&sn=b9a041f238016c2727189ef801b9b07f
- Original link text: https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247495245&idx=1&sn=b9a041f238016c2727189ef801b9b07f

## Captured Page Metadata

- Browser title: QCon Beijing 2026 | Treating Automated Testing as AI Coding: A Practical Review of Xiaohongshu's GUI Agent
- Description: This article is a transcript of the technical sharing by Xiaohongshu's Quality and Efficiency R&D team at QCon Beijing 2026, detailing the engineering implementation of their self-developed GUI Agent in intelligent testing. It first identifies two core challenges of traditional UI automation: poor test stability (script failures due to UI changes) and insufficient business understanding (testing expertise locked in human minds). To address these, the team designed a three-layer architecture: the Business Intent Layer (structured natural language describing test objectives), the Agent Exploration Layer (LLM-driven autonomous exploration and execution), and the Executable Code Layer (zero-token regression scripts after solidification). The key innovation lies in the dual-agent collaboration model: the main Agent (GPT/Sonnet scale) handles deep-thinking tasks like intent understanding and plan generation, while the visual sub-agent (Gemini 3 Flash) handles low-cost, high-success-rate atomic perception operations. The team also built an operation graph and a layered knowledge base to suppress Agent hallucinations, and adopted a Code-as-Action strategy to solidify verified interactions into executable test code, achieving zero token consumption for CI regression. The article concludes with two counterintuitive lessons learned: evaluation sets should not be used as optimization targets, and a pure exploration approach is not viable.
- Date: 05-12

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/852b6f4a: https://www.bestblogs.dev/en/article/852b6f4a
- https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247495245&idx=1&sn=b9a041f238016c2727189ef801b9b07f: https://mp.weixin.qq.com/s?__biz=Mzg4OTc2MzczNg==&mid=2247495245&idx=1&sn=b9a041f238016c2727189ef801b9b07f
