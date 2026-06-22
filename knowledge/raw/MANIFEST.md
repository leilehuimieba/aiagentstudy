# Raw Manifest

This manifest classifies `knowledge/raw/` so future agents can find the right files without scanning everything.

## Stable Operational Files

Use these first for normal work:

- `capture-opencli-latest-page.py`: current BestBlogs capture script through OpenCLI Browser Bridge.
- `query-kb.py`: local knowledge-base query and context-pack tool.
- `build-kb-retrieval.js`: builds JSON and JSONL retrieval metadata.
- `build-kb-fts.py`: builds SQLite item-level and chunk-level FTS retrieval indexes.
- `verify-batch.js`: basic batch verification.
- `audit-kb.js`: deeper catalog and item consistency audit.
- `eval-search.py`: regression check for search quality using curated query/relevant-ID cases.

Root shortcut:

```powershell
.\kb.ps1 search "Claude" --limit 5
.\kb.ps1 pack "智能体评估" --limit 5
.\kb.ps1 search "browser runtime harness" --topic 03-control-loop --expand-topic
.\kb.ps1 pack "Claude Code auto mode 原文 来源" --profile auto
.\kb.ps1 pack "Harness Engineering 权限 日志 验证" --profile deep --grouped
.\kb.ps1 capture --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date 2026-06-08
.\kb.ps1 verify
.\kb.ps1 rebuild
.\kb.ps1 audit
.\kb.ps1 eval
.\kb.ps1 status
```

## Generated Retrieval Outputs

Generated files live under `knowledge/retrieval/` and should be rebuilt, not hand-edited.

- `articles-meta.json`
- `articles-meta.jsonl`
- `kb.sqlite`
- `build-report.json`
- `fts-report.json`

## Batch Reports

Files like `batch-*-report.json`, `opencli-latest-batch-*.json`, and `edge-latest-batch-*.json` record capture outcomes. Use them for provenance and debugging only.

## Evidence Snapshots

Files like `current-opencli-latest-page*.json`, `current-edge-*`, `latest-*`, `candidates-*`, and `weekly-*` are raw discovery snapshots. They are useful when auditing why an item was or was not captured.

## Historical Scripts

Files such as `add-*`, `capture-batch-*`, `capture-edge-*`, `capture-latest-live.js`, and one-off inspection scripts are historical. Do not use them as the default capture path unless the stable script fails and a comparison is needed.

## Diagnostics

Temporary smoke tests, `tmp-*`, `test-*`, extracted HTML, screenshots, and direct network responses should be treated as debugging material. Keep them out of root when possible.

## External Mirrors

`external/` contains third-party source mirrors. Read `external/README.md` before opening it. This folder is large and should not be scanned during normal knowledge-base lookup.

## Maintenance Rule

If a new script becomes the preferred path, update this manifest, `README.md`, and root `kb.ps1` together. If a script is a one-off investigation, name it clearly and document the related batch or issue.
