# BB-2026-05-01-550 Summary

## Article

- Title: How Box AI built enterprise content agents with Deep Agents
- Source: BestBlogs / LangChain Blog
- URL: https://www.bestblogs.dev/article/06adaad3
- Date: 06-12
- Topic: `01-context-memory`
- Tags: AI Agent, Enterprise AI, LLM, RAG, Deep Agents

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article presents a case study of Box AI's evolution from single-file Q&A to an enterprise-scale agentic system built on Deep Agents. It explains the architectural shift from hardcoded, specialized sub-agents to a recursive parent/child model where a 'Global Agent' dynamically spawns child agents to handle complex, multi-step tasks like cross-enterprise search and multi-document synthesis. Key design decisions include complete model agnosticism (supporting OpenAI, Anthropic, Google, etc.), the use of Deep Agents middleware for parallel citation generation, prompt caching, and context management, and a focus on engineering velocity that reduced agent shipping time from months to weeks. The article concludes with a vision for agents possessing the institutional knowledge of a long-tenured employee.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
