# Knowledge Catalog Entry

Low-token entry point for the AI agent learning knowledge base.

This catalog is scoped to AI-agent materials only.
If you add unrelated domains such as exam prep, store them under `study_spaces/` instead of `knowledge/items/`.

Read:

1. `map.md`
2. `current-coverage.md` when deciding where existing material already lives
3. `articles-index.md`

Then open only relevant item summaries.

For topic-level boundaries, read `knowledge/items/README.md` and the README inside each topic directory.

For programmatic lookup, build and query `knowledge/retrieval/` first, then open only matched summaries.

For source coverage and collection routes beyond BestBlogs, read `current-coverage.md` and `source-watchlist.md`.

For the combined optimization plan that turns this corpus into a more general capture, storage, retrieval, and display system, read `knowledge-system-optimization.md`.

For Obsidian synthesis cards generated or registered from knowledge items, read `obsidian-card-index.md`.

## Query Examples

```powershell
python knowledge\raw\query-kb.py "Claude" --mode search --limit 5
python knowledge\raw\query-kb.py "智能体评估" --mode pack --limit 5
```

If retrieval outputs are stale, rebuild them:

```powershell
node knowledge\raw\build-kb-retrieval.js
python knowledge\raw\build-kb-fts.py
```
