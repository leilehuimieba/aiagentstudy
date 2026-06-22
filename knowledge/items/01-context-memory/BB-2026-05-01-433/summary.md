# BB-2026-05-01-433 Summary

## Article

- Title: AI Can't Cooperate? That's Because They've Never Seen a Market Economy / Hao's Trend Talk
- Source: BestBlogs / 腾讯科技
- URL: https://www.bestblogs.dev/article/aec5de44
- Date: 06-07
- Topic: `01-context-memory`
- Tags: AI Agent, Multi-Agent Systems, LLM, AI Research, AI Architecture

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article revolves around two core questions: 'Why don't AIs cooperate?' and 'How can we make AIs learn to cooperate?' It first cites multiple 2026 studies (UNC, UIUC, Stanford, Google DeepMind) revealing the current state: multi-agent system failure rates range from 41% to 87%, with the root cause being not insufficient model capability, but coordination collapse and convergent reasoning; more capable models (like o3) actually show worse cooperation. The fundamental reason is that current LLM training is essentially a 'single-player game' (MDP), never encountering a true 'other,' resulting in a 'solipsistic' cognitive architecture. Next, the article critiques the prevailing Orchestrator-Worker architecture, likening it to a 'planned economy' and pointing out its three structural dilemmas: the division of labor paradox, credit assignment failure, and Hayek's 'curse of dispersed knowledge.' Finally, it highlights the 'Economy of Minds' paper from Harvard and MIT, which proposes an orchestration-free 'free market' system. Through four mechanisms—auctions, bucket-brigade credit assignment, economic natural selection, and novice protection—agents spontaneously generate cooperation from self-interested behavior. This system significantly outperforms single-agent and orchestrated systems on benchmarks like MATH, HumanEval, and ALFWorld, and theoretically proves that market mechanisms can asymptotically achieve the optimal allocation of an omniscient orchestrator. The article concludes by noting the system's current simplifications and future expansion possibilities, asserting that the path forward for multi-agent systems lies in 'designing the conditions for cooperation' rather than 'designing the outcome of cooperation.'

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
