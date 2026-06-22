# AI Source Registry

This folder is the source-intelligence layer for the AI-agent knowledge base.

It answers three questions:

1. Which websites should we monitor for AI agents, frontier AI, model training, model optimization, evaluation, and safety?
2. Which capture route should each source use: RSS/API, direct HTTP, OpenCLI Browser Bridge, or manual review?
3. Where should captured items land in `knowledge/items/**`?

This folder is not a replacement for `knowledge/items/`.
It is the watchlist and routing layer used before creating durable knowledge items.

## Files

- `source-registry.json`: structured source registry.
- `capture-strategy.md`: capture routes, dedupe rules, and local storage policy.
- `paper-sources.md`: AI paper/research sources and recommended queries.
- `opencli-probes/`: generated probe reports from Browser Bridge checks.
- `../catalog/current-coverage.md`: current captured coverage and known source notes.

## Quick Commands

```powershell
.\kb.ps1 discover-sources --max-results 10
.\kb.ps1 capture-arxiv --latest-candidates --limit 5
.\kb.ps1 capture-arxiv --query 'all:"agentic" OR all:"tool use" OR all:"post-training"' --max-results 20 --limit 5
.\kb.ps1 capture-rss --ids langchain-blog simon-willison latent-space --limit 5
.\kb.ps1 probe-sources --profile qmvqcrb8 --ids arxiv huggingface-papers openai-news langchain-blog
.\kb.ps1 capture-browser --ids openai-news jiqizhixin github-trending huggingface-papers --profile qmvqcrb8 --limit 4
.\kb.ps1 source-health --limit 20
.\kb.ps1 source-health --ids openai-news anthropic-news huggingface-papers
```

## Default Routing

- Public RSS/API sources should be captured without browser state when possible.
- Dynamic, logged-in, or JavaScript-heavy pages should use OpenCLI Browser Bridge profile `qmvqcrb8`.
- BestBlogs remains a high-signal aggregator, but it should no longer be the only source.
- Captured source documents still become normal items under `knowledge/items/<topic>/<ID>/`.
- Browser captures are source radar snapshots for discovery. Promote individual linked articles or papers into deeper items after relevance checks.

## Source Health

Use `.\kb.ps1 source-health` to summarize local source coverage, candidate backlog, latest browser probe status, and suggested next actions.

Status meanings:

- `backlog`: source has active candidates waiting for review.
- `active`: source has local captures or a readable recent probe.
- `probe_attention`: latest browser probe opened but did not produce usable text.
- `needs_capture`: RSS/API source is registered but has no local captures yet.
- `unseen`: source is registered but has no local signal yet.
