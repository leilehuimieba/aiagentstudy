# BB-2026-05-01-374 Summary

## Article

- Title: Claude Opus 4.8: “a modest but tangible improvement”
- Source: BestBlogs / Simon Willison's Weblog
- URL: https://www.bestblogs.dev/article/2f7a0ee5
- Date: 05-29
- Topic: `06-frontier-radar`
- Tags: Claude Opus 4.8, Anthropic, LLM, AI Honesty, Model Release

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Simon Willison reviews Anthropic's Claude Opus 4.8 release, highlighting the lab's refreshingly honest framing of the model as a modest but tangible improvement. The key advancement is in honesty: Opus 4.8 is four times less likely to let flaws in its code pass unremarked, and achieves the lowest incorrect rate across benchmarks by abstaining on uncertain questions rather than guessing. Pricing remains unchanged at $5/$25 per million tokens, but fast mode pricing is significantly reduced. New developer features include mid-conversation system messages for dynamic instruction updates without breaking prompt cache, and a lower minimum cacheable prompt length of 1,024 tokens (down from 4,096). The context window stays at 1,000,000 tokens with 128,000 max output. Willison also demonstrates the model's capabilities by generating pelican-on-bicycle illustrations across five thinking levels, noting the max level produced the best result at a cost of 43 cents.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
