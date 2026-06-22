# BB-2026-05-01-363 Summary

## Article

- Title: From Individual Acceleration to Team Efficiency: Xiaomi's AI Coding Engineering Practices
- Source: BestBlogs / 小米技术
- URL: https://www.bestblogs.dev/article/7952a1b8
- Date: 05-28
- Topic: `02-tools-actions`
- Tags: AI Coding, Engineering Practices, Team Efficiency, Workflow, Knowledge Base

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article, authored by Xiaomi's technical team, systematically elaborates on the bottlenecks and solutions encountered after scaling AI coding engineering to hundreds of people. It points out that improvements in individual coding efficiency do not directly translate into organizational efficiency gains. The real bottlenecks lie in the loss during requirement translation, delays in decision feedback loops, and the scattering of context across terminals. To address this, the team built three layers of engineering practices: The first layer is the unified workflow VAF (Vibe Agentic Flow), which lowers the barrier to AI usage through a menu-driven, low-threshold process, enabling even developers unfamiliar with AI to get started, and introduces a convergence coordination pattern to support multi-service collaboration. The second layer is the code knowledge base VKF (Vibe Knowledge Flow). After the failure of VKF 1.0, which attempted to translate code into documentation, the team repositioned it as a knowledge index for code, helping AI find entry points and critical paths in real code faster and more accurately, rather than replacing the code itself. The third layer is the collaboration workstation eight-claw, an AI collaboration bot built within Feishu. It uses 'topics' as the smallest governance unit for parallel execution, making the AI's work process transparent within the team's collaboration space, thus solving the problems of information opacity and parallel collaboration. The article concludes by distilling four design principles and emphasizes that the accumulation of knowledge and collaboration is the organizational capability hardest to replicate in the AI era.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
