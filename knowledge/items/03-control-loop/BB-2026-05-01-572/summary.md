# BB-2026-05-01-572 Summary

## Article

- Title: AI agents expose the security checks you never actually wrote
- Source: BestBlogs / Stack Overflow Blog
- URL: https://www.bestblogs.dev/article/aa9f535e
- Date: 06-15
- Topic: `03-control-loop`
- Tags: AI Agent, LLM, AI Security, AI Safety, Software Engineering

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article analyzes the June 2026 attack on over 20,000 Instagram accounts, including the dormant Obama-era White House account, where attackers used Meta's AI support assistant to reset passwords without exploits or password guessing. The author argues this was not an AI mistake but an exposure of a security model that relied on human discretion—a support worker who would have sensed something wrong. The core problem is the 'confused deputy' pattern: an LLM agent, by design, cannot distinguish who is authorized and will execute any plausible-sounding request. The article warns that as agents gain access to payment, CRM, and other business systems, the blast radius multiplies. It explains why a better model cannot fix this (the model is the part an attacker controls) and prescribes concrete engineering fixes: verifying the principal outside the chat, scoping agent authority per action, gating irreversible actions with human approval, and maintaining provenance for every action. The conclusion reframes the challenge as an ordinary engineering gap—the human judgment that was once implicit must now be written as explicit code.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
