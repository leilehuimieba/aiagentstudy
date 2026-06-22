# BB-2026-05-01-198 Summary

## Article

- Title: SocialReasoning Bench shows the limits of today’s AI agents
- Source: BestBlogs / Microsoft Research Blog
- URL: https://www.bestblogs.dev/en/article/d1e95073
- Date: 05-11
- Topic: `04-evaluation-guardrails`
- Tags: AI Agents, Social Reasoning, Benchmark, Principal-Agent, Negotiation

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This blog post from Microsoft Research introduces SocialReasoning-Bench, a new benchmark designed to evaluate the social reasoning capabilities of AI agents. The benchmark tests agents in two principal-agent scenarios: Calendar Coordination and Marketplace Negotiation. It measures not just task completion, but also Outcome Optimality (how much value the agent secures for the user) and Due Diligence (the quality of the decision-making process). The key findings are stark: while frontier models like GPT-4.1, GPT-5.4, Claude Sonnet 4.6, and Gemini 3 Flash complete tasks at near-perfect rates, they consistently produce poor outcomes. Agents often accept suboptimal meeting times or bad deals, failing to advocate effectively for their user. Defensive prompting helps but is insufficient to close the gap. The benchmark also reveals that agents are vulnerable to adversarial manipulation. The post argues that as agents interact in multi-party environments, these social reasoning gaps can compound, leading to widespread value loss. The work is presented as a crucial step toward building agents that act as trustworthy delegates.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
