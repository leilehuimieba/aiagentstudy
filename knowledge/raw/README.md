# Raw Workspace

This directory holds capture scripts, raw extraction evidence, reports, and retrieval utilities. It is intentionally messy compared with `knowledge/catalog/` and `knowledge/items/`; use this README as the stable entry point.

For a file-family map, read `MANIFEST.md`.

## Stable Scripts

### Query

```powershell
python knowledge\raw\query-kb.py "Claude" --mode search --limit 5
python knowledge\raw\query-kb.py "智能体评估" --mode pack --limit 5
python knowledge\raw\brief-kb.py "browser use agents" --limit 5
python knowledge\raw\evidence-kb.py "Claude Code auto mode 原文 来源" --limit 5
```

Repository-root shortcut:

```powershell
.\kb.ps1 search "Claude" --limit 5
.\kb.ps1 pack "智能体评估" --limit 5
.\kb.ps1 brief "browser use agents" --limit 5
.\kb.ps1 evidence "Claude Code auto mode 原文 来源" --limit 5
```

If a query unexpectedly returns zero hits, rebuild retrieval first.

### Build Retrieval

```powershell
python knowledge\raw\build-item-metadata.py --execute
node knowledge\raw\build-kb-retrieval.js
python knowledge\raw\build-kb-fts.py
```

Shortcut: `.\kb.ps1 rebuild`

Shortcut for sidecars: `.\kb.ps1 build-item-metadata --execute`

Outputs go to `knowledge/retrieval/`.

`build-item-metadata.py` infers durable item `type` and `source_id` from explicit source fields and evidence URLs, not just from the local ID prefix. This keeps historical `BB-*` external references such as arXiv papers, OpenReview papers, GitHub repos, OWASP/PortSwigger pages, and local synthesis notes from being treated as BestBlogs captures.

`build-kb-retrieval.js` now prefers each item's `item.json` sidecar for stable fields such as title, source, topic, blocks, tags, status, URLs, source IDs, item type, and local paths. It still reads `summary.md` for takeaway/principle/summary text and `article.md` for previews and chunking, and it falls back to markdown plus `articles-index.md` if a sidecar is missing or invalid.

### Verify and Audit

```powershell
node knowledge\raw\verify-batch.js
node knowledge\raw\audit-kb.js
python knowledge\raw\audit-summary.py
python knowledge\raw\repair-audit.py
```

Shortcuts: `.\kb.ps1 verify`, `.\kb.ps1 audit`, `.\kb.ps1 health`, and `.\kb.ps1 repair-audit`

### Status

```powershell
.\kb.ps1 status
.\kb.ps1 source-health --limit 20
.\kb.ps1 weekly-review
.\kb.ps1 weekly-review --eval
.\kb.ps1 weekly-review --write
.\kb.ps1 coverage --write
```

Shows catalog row count, latest catalog ID, and retrieval build metadata.

`source-health` summarizes registered source coverage, candidate backlog, latest browser probe status, and recommended next actions.

`coverage --write` regenerates `knowledge/catalog/current-coverage.md` from repository state. `weekly-review` prints the operational project view: status, compact health, candidate summary, source-health focus, and links to the current management docs. Add `--eval` when you want the slower retrieval quality evaluation included. Add `--write` to save a durable report under `product/data/reports/`.

### Obsidian Card Drafts

```powershell
.\kb.ps1 obsidian-card BB-2026-05-01-564
.\kb.ps1 obsidian-card BB-2026-05-01-572 --module security
.\kb.ps1 obsidian-card <KB-ID> --module eval --write --date 2026-06-18
.\kb.ps1 obsidian-card BB-2026-05-01-564 --register-existing "D:\webstudy\Notes\obsidian\黑曜石\学习笔记\AI-Agent\03-控制循环与编排\2026-06-18-生产级Agent循环.md" --module control-loop
```

`obsidian-card` renders a draft note from an existing `summary.md` and `source.md`. By default it prints Markdown to the terminal. Use `--write` to save into the Obsidian vault, with topic-to-module routing unless `--module` overrides it. This is a bridge from the evidence store into the personal synthesis layer; review and edit the generated card before treating it as finished understanding.

When `--write` or `--register-existing` is used, the script updates:

- `knowledge/obsidian/cards-index.jsonl`
- `knowledge/catalog/obsidian-card-index.md`

This prevents silent duplicate card generation. Use `--force` only when the same KB item intentionally needs another Obsidian card.

### Candidate Watch

```powershell
.\kb.ps1 watch --limit 20
.\kb.ps1 watch --summary
.\kb.ps1 watch --group-by source --limit 20
.\kb.ps1 watch --group-by topic --limit 20
.\kb.ps1 watch --json --limit 5
```

`watch` reads `knowledge/candidates/*.jsonl` without moving records. Use `--summary` for a compact queue breakdown, `--group-by source|type|topic|route|date|status` for review batches, and `--json` when another script or AI agent needs machine-readable candidate metadata.

`verify-batch.js` checks basic article/source counts and sizes. `audit-kb.js` checks catalog/item consistency, `item.json` presence/validity, missing files, placeholder loss, and source evidence issues. Source evidence URL checks now use `item.json` type/source metadata, so BestBlogs URL requirements apply only to actual BestBlogs captures rather than every historical `BB-*` ID.

Known-short captures are documented in `knowledge/quality/article-length-overrides.json`. When an under-800-byte `article.md` is intentionally short, such as an abstract-only paper capture, benchmark stub, spec summary, README excerpt, metadata-only item, or genuinely short page, add a reason there. `audit-kb.js` reports those under `articleUnder800Accepted` and keeps `articleUnder800` for unresolved short captures only.

Use `.\kb.ps1 health` for a compact red/green health card before opening the full audit JSON. Use `.\kb.ps1 health --json` when another script or AI agent needs the same summary in machine-readable form.

`repair-audit.py` previews low-risk repair candidates by default. Use `.\kb.ps1 repair-audit --execute` only after reviewing the dry-run output; currently it fixes delimiter-equivalent `summary.md` title/source fields so they match the catalog table without touching real title/source conflicts.

Avoid raw `|` characters inside `knowledge/catalog/articles-index.md` title or source cells. The local catalog parser is intentionally simple and treats `|` as a table delimiter; use `/` in titles such as `Example Title / Publisher` and keep the richer source in the Source column or `source.md`.

### BestBlogs Capture

```powershell
python knowledge\raw\capture-opencli-latest-page.py --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date 2026-06-08
```

The script discovers latest BestBlogs article entries through OpenCLI Browser Bridge, writes item folders, appends `knowledge/catalog/articles-index.md`, updates `AI_AGENT_MEMORY.md`, and saves raw page/content/discovery JSON.

## File Families

- `current-opencli-latest-page*.json`: list API snapshots.
- `opencli-latest-batch-*.json`: batch reports.
- `current-edge-*`, `edge-latest-*`: older Edge/OpenCLI capture runs.
- `batch-*.json`: historical batch reports.
- `external/`: external source material preserved as raw evidence.
- `tmp*`, `test-*`, `*-direct.json`: temporary diagnostics; read only when debugging a related capture.

Read `external/README.md` before opening `external/`; it contains multi-GB source mirrors and should not be scanned by default.

## Rule

Prefer stable scripts above. Treat older one-off capture scripts as historical evidence unless a current script fails and you need a comparison.
