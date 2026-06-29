# BB-2026-05-01-658 Summary

## Article

- Title: From 'Finding Videos' to 'Producing Videos': Kuaishou's RaG Propels Recommendation Systems into the Fully Generative Era
- Source: BestBlogs / 快手技术
- URL: https://www.bestblogs.dev/article/c674d376
- Date: 06-26
- Topic: `01-context-memory`
- Tags: Recommendation System, Video Generation, AIGC, Ad Tech, Multimodal Model

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article details Kuaishou's latest advancement in recommendation systems, RaG (Recommendation-as-Generation), which aims to break through the limitations of the traditional 'retrieve-and-rank' paradigm, shifting recommendation systems from 'finding videos' to 'producing videos'. Core innovations include: Disentangled Semantic IDs (D-SIDs), which decouple videos into content semantics and creative semantics as a unified semantic interface; Generative Recommendation Model (GRM), which autoregressively predicts user interest semantic tokens; Instruction Model, which translates semantics into shot-level production instructions; Video Generation Agents (VGAs), which organize video generation via a multi-Agent pipeline; and Synergistic Cross-Domain Reward Learning (SCRL), which incorporates user feedback, interest alignment, and video quality into closed-loop optimization. The article also elaborates on the industrial deployment architecture (online recommendation + nearline generation + cache expansion) and presents online experimental results: GRM improves upon traditional DLRMs by 3.526%, and the complete RaG further improves by 1.870% on top of GRM. Finally, the article discusses the paradigm expansion trend of recommendation systems from content distribution to content creation.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
