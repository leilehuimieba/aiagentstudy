# BB-2026-05-01-619 Summary

## Article

- Title: Volcengine AI Search 10-Million-Level Agent Architecture Evolution and Practice: From ReAct Three-Node to Unified Policy
- Source: BestBlogs / 字节跳动技术团队
- URL: https://www.bestblogs.dev/article/b02cc219
- Date: 06-26
- Topic: `01-context-memory`
- Tags: AI Agent, LLM, System Design, Architecture Evolution, Context Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article deeply analyzes the three major engineering sins of the standard ReAct architecture in enterprise-level AI search scenarios: extremely high latency, context oscillation, and broken control flow. Combining industry consensus, it proposes principles such as strict stratification of Workflow and Agent, everything as a Tool, and context independence. Based on this, the Volcengine AI Search team designed the Workflow + Unified Policy Agent (UP-ReAct) architecture, delegating deterministic processes to Workflow and dynamic decisions to Unified Policy, abstracting all behaviors as Tools, and managing state uniformly via Context Manager. In real e-commerce evaluations, this architecture reduced TTFT from 14.045s to 9.8s (a 30.22% decrease), improved recommendation accuracy by 3.76%, and enhanced conversational experience by 14.78%, breaking the conventional perception that speed and quality are mutually exclusive. The article emphasizes that system complexity should be properly managed through boundary划分, rather than stuffed into the model.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
