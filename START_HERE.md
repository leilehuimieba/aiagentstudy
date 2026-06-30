# Project Entry

This workspace is a durable AI-agent study knowledge base. Start here when you need to query, maintain, or extend the repository.

## Read Order

1. `AGENTS.md`
2. `README.md`
3. `REPO_STRUCTURE.md`
4. `AI_AGENT_MEMORY.md`
5. `docs/AI_AGENT_LEARNING_MODEL.md`
6. `docs/OPENCLI_NOTES.md`
7. `docs/KNOWLEDGE_BASE.md`
8. `knowledge/catalog/README.md`
9. `knowledge/catalog/map.md`
10. `knowledge/catalog/articles-index.md`

Open item summaries before full articles. Full `article.md` files are for evidence and deep reading.

## Common Tasks

### Manage the project

```powershell
.\kb.ps1 weekly-review
.\kb.ps1 weekly-review --eval
.\kb.ps1 weekly-review --write
.\kb.ps1 coverage --write
```

Project management entry points:

- `PROJECT_BOARD.md`: radar, capture, synthesis, and product workstreams.
- `PRODUCT_NOW.md`: current two-week product execution plan.
- `docs/PRODUCT_ROADMAP.md`: long-term product direction.

### Turn a captured item into an Obsidian card draft

```powershell
.\kb.ps1 obsidian-card BB-2026-05-01-564
.\kb.ps1 obsidian-card <KB-ID> --module security --write
.\kb.ps1 obsidian-card BB-2026-05-01-564 --register-existing "D:\webstudy\Notes\obsidian\黑曜石\学习笔记\AI-Agent\03-控制循环与编排\2026-06-18-生产级Agent循环.md" --module control-loop
```

The command reads an existing `summary.md` and `source.md`, then renders a draft card for the personal synthesis layer. Use `--write` only when you want to save into the Obsidian vault; otherwise it prints the draft Markdown for review. Written and registered cards are tracked in `knowledge/catalog/obsidian-card-index.md`.

### Search the knowledge base

```powershell
python knowledge\raw\query-kb.py "Claude" --mode search --limit 5
python knowledge\raw\query-kb.py "智能体评估" --mode pack --limit 5
```

Shortcut:

```powershell
.\kb.ps1 search "Claude" --limit 5
.\kb.ps1 pack "智能体评估" --limit 5
.\kb.ps1 status
```

Then open matched `summary.md` files. Open `article.md` only when the summary is insufficient.
If a query unexpectedly returns zero hits, rebuild retrieval and try again.

### Rebuild retrieval

```powershell
node knowledge\raw\build-kb-retrieval.js
python knowledge\raw\build-kb-fts.py
```

Shortcut:

```powershell
.\kb.ps1 rebuild
```

### Verify knowledge-base health

```powershell
node knowledge\raw\verify-batch.js
node knowledge\raw\audit-kb.js
```

Shortcut:

```powershell
.\kb.ps1 verify
.\kb.ps1 audit
.\kb.ps1 status
```

### Capture BestBlogs latest articles

Use OpenCLI Browser Bridge with the default local browser profile:

```powershell
opencli doctor -v
opencli profile list
python knowledge\raw\capture-opencli-latest-page.py --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date 2026-06-08
node knowledge\raw\verify-batch.js
node knowledge\raw\build-kb-retrieval.js
python knowledge\raw\build-kb-fts.py
```

Shortcut:

```powershell
.\kb.ps1 doctor
.\kb.ps1 capture --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date 2026-06-08
.\kb.ps1 verify
.\kb.ps1 rebuild
```

Use the current date for `--discovery-date`.

## Directory Map

- `knowledge/catalog/`: low-token human and agent index.
- `knowledge/items/`: curated knowledge items by topic and ID.
- `knowledge/retrieval/`: generated local search index.
- `knowledge/raw/`: scripts, raw captures, reports, and external evidence.
- `study_spaces/`: non-agent study domains; keep them out of `knowledge/items/`.
- `product/`: product/project planning material.
- `PROJECT_BOARD.md`: current knowledge/project operating board.
- `PRODUCT_NOW.md`: near-term product execution plan.

See `REPO_STRUCTURE.md` for module boundaries and cleanup policy.

## Maintenance Rule

Do not claim a capture or knowledge-base update is complete unless the item files, catalog index, verification, and retrieval rebuild are actually done.
