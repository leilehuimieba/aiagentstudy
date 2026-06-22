# Knowledge Workspace

This is the AI-agent knowledge base. Use `START_HERE.md` at the repository root for the full operating flow.

## Subdirectories

- `catalog/`: low-token map and article index. Read this first.
- `items/`: curated items grouped by topic. Open `summary.md` before `article.md`.
- `retrieval/`: generated metadata and SQLite FTS index for local search.
- `raw/`: capture scripts, raw evidence, batch reports, and maintenance utilities.

Useful guides:

- `items/README.md`: item format and topic boundaries.
- `raw/MANIFEST.md`: raw file-family map and stable script list.
- `raw/external/README.md`: large external mirror policy.

## Fast Path

From the repository root:

```powershell
.\kb.ps1 search "Claude" --limit 5
.\kb.ps1 pack "智能体评估" --limit 5
.\kb.ps1 rebuild
.\kb.ps1 audit
.\kb.ps1 status
```

If `.\kb.ps1 search ...` unexpectedly returns zero hits, run `.\kb.ps1 rebuild` and retry.

## Read Policy

1. Search retrieval or read `catalog/`.
2. Open matched `summary.md`.
3. Open `article.md` only for evidence, quotes, or deep reading.
4. Check `source.md` when provenance matters.
