# BB-2026-05-01-199 Summary

## Article

- Title: Accelerating LLM-Driven Developer Productivity at Zoox
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/en/article/a880e863
- Date: 05-14
- Topic: `02-tools-actions`
- Tags: Enterprise AI, Developer Productivity, LLM Platform, RAG, AI Agents

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This presentation details Zoox's journey in building an internal AI platform called Cortex to enhance developer productivity. Amit Navindgi, the lead, outlines the challenges of the developer lifecycle, from information discovery to customer support, and how AI can remove friction. The core of the talk is the platform's architecture: a secure gateway to models like Claude and Gemini, knowledge bases built via RAG from internal sources (Confluence, Slack, GitHub), and an agentic API that allows teams to create custom agents by composing tools. A key innovation is the 'agent as API' paradigm, where teams define tools once in a central registry and invoke agents via REST, separating business logic from platform concerns. The talk also covers critical enterprise features like human-in-the-loop for write actions, managing quotas, and supporting multimodal inputs. Beyond the platform, Navindgi emphasizes the importance of driving adoption through identifying AI champions, building usage dashboards, running hackathons, and creating a culture of sharing wins and failures. He advocates for a pragmatic 'build what you cannot buy' approach, citing the adoption of Cursor over an internal solution. The key takeaway is that a successful AI strategy requires not just building a robust platform but also actively evangelizing its use and measuring its impact.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
