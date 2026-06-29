# BB-2026-05-01-648 Summary

## Article

- Title: Frontend AI Coding for Scenario Marketing — From Problems to Solutions
- Source: BestBlogs / 大淘宝技术
- URL: https://www.bestblogs.dev/article/7e12363e
- Date: 06-22
- Topic: `01-context-memory`
- Tags: AI Coding, LLM, AI Agent, Context Engineering, Prompt Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article first points out that the actual efficiency improvement of current AI Coding tools is far below expectations, primarily due to the O(n²) computational limitation of the Transformer attention mechanism, attention collapse under long contexts, and a mismatch in human-AI collaboration patterns. It then reviews two mainstream practices—Vibecoding and Spec-driven development—analyzing their respective advantages and limitations: Vibecoding is flexible but prone to cognitive overload and code rot, while Spec-driven development is structured but rigid and contrary to developers' cognitive habits. On this basis, the author proposes six core principles: respecting cognitive laws, separation of responsibilities, prioritizing multimodality, persistence and reuse, incremental updates, and maintaining human control. The article then details the design of the team's self-developed Specflow Agent (an independent client based on the Claude Agent SDK): multiple role-based SubAgents (Product, Design, Technology) conduct in-depth analysis of PRDs, design drafts, and codebases, producing structured task contexts that are then handed over to IDEs such as Cursor/Qoder for execution, thereby decoupling the analysis phase from the coding phase. It also covers engineering practices such as a task management board, MCP bidirectional communication, incremental updates, and team reuse.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
