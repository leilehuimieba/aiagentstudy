# AI Agent Knowledge Base

Low-token entry point.

> Scope: this document describes the AI-agent knowledge base under `knowledge/` only.
> Non-agent materials must not be added under `knowledge/items/`; put them in `study_spaces/<domain>/` instead.

For project-wide operation and command shortcuts, start with `START_HERE.md`.

## Read Order

1. `knowledge/catalog/README.md`
2. `knowledge/catalog/map.md`
3. `knowledge/catalog/articles-index.md`
4. Relevant `knowledge/items/**/summary.md`
5. Full `article.md` only when needed

## Structure

- `knowledge/catalog/`: small indexes and topic maps.
- `knowledge/retrieval/`: machine-friendly metadata and local search index.
- `knowledge/items/`: curated entries organized by topic and ID.
- `knowledge/raw/`: raw page states and command outputs.
- `item.json`: optional machine-readable sidecar inside each durable item directory.

Helpful navigation files:

- `knowledge/items/README.md`: item format and topic directory guide.
- `knowledge/raw/MANIFEST.md`: raw file families, stable scripts, historical scripts, reports, diagnostics, and external mirrors.
- `knowledge/raw/external/README.md`: policy for large external source mirrors.
- `knowledge/catalog/current-coverage.md`: current source coverage and capture routes.
- `knowledge/catalog/knowledge-system-optimization.md`: general knowledge-system optimization blueprint.
- `knowledge/catalog/obsidian-card-index.md`: registry of Obsidian synthesis cards generated or registered from knowledge items.
- `knowledge/schema/README.md`: target data contracts for items, sources, candidates, capture runs, and views.
- `knowledge/candidates/README.md`: candidate queue and promotion lifecycle.

## Capture Policy

For each collected item, preserve:

- `summary.md`: low-token structured summary and model mapping.
- `article.md`: full text exported from the BestBlogs page when available.
- `source.md`: evidence links, including both the BestBlogs page URL and the original publisher URL when BestBlogs exposes it.
- `raw/`: raw metadata, page state, or extraction output.

Default reading should still use indexes and summaries first. Full text exists for evidence and deep study, not for every routine lookup.

## Local Retrieval Layer

Use the local retrieval layer before opening full articles in large-batch lookup:

1. Build metadata: `node knowledge\raw\build-kb-retrieval.js`
2. Build SQLite item/chunk FTS: `python knowledge\raw\build-kb-fts.py`
3. Query candidates with item-level and chunk-level RRF fusion: `python knowledge\raw\query-kb.py "<query>" --mode search`
4. Build a stable context pack for model input: `python knowledge\raw\query-kb.py "<query>" --mode pack`
5. Build a human-readable topic brief: `python knowledge\raw\brief-kb.py "<query>"`
6. Show source links and raw evidence paths: `python knowledge\raw\evidence-kb.py "<query>"`
7. Check compact corpus health when needed: `python knowledge\raw\audit-summary.py`
8. Open matched `summary.md`
9. Open `article.md` only when evidence or deep reading is needed

When a query crosses module boundaries, keep strict topic filtering off or explicitly expand it:

```powershell
.\kb.ps1 search "browser runtime harness" --topic 03-control-loop --expand-topic
```

For model-facing context packs, `--profile auto` infers a retrieval strategy from query intent:

```powershell
.\kb.ps1 pack "Claude Code auto mode 原文 来源" --profile auto
.\kb.ps1 pack "Harness Engineering 权限 日志 验证" --profile deep
.\kb.ps1 pack "Harness Engineering 权限 日志 验证" --profile deep --grouped
.\kb.ps1 brief "browser use agents" --limit 5
.\kb.ps1 evidence "Claude Code auto mode 原文 来源" --limit 5
.\kb.ps1 health
.\kb.ps1 source-health --limit 20
.\kb.ps1 build-item-metadata --execute
```

Use `--grouped` when the result should separate core matches, background context, and evidence sources for model input.

Search quality can be checked with:

```powershell
.\kb.ps1 eval
```

## Candidate Radar

Source radar captures can now emit candidate records:

- `knowledge/candidates/inbox.jsonl`: discovered links waiting for review.
- `knowledge/candidates/promoted.jsonl`: source signals already captured as durable items.
- `knowledge/candidates/rejected.jsonl`: low-value, duplicate, blocked, or off-topic signals.

Use:

```powershell
.\kb.ps1 watch --limit 20
.\kb.ps1 watch --group-by source --limit 20
.\kb.ps1 watch --summary
.\kb.ps1 watch --json --limit 5
.\kb.ps1 source-health --limit 20
python knowledge\raw\manage_candidates.py validate
```
