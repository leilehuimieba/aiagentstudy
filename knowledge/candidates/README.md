# Knowledge Candidates

This folder is the staging area between source radar and durable knowledge items.

Use candidates for links, papers, repos, products, reports, forum threads, and other signals discovered from RSS feeds, APIs, browser snapshots, source probes, or manual review.

## Lifecycle

```text
radar -> candidate -> captured -> synthesized
                  \-> deferred
                  \-> rejected
```

## Files

Active files:

- `inbox.jsonl`: newly discovered candidate signals.
- `promoted.jsonl`: candidates that became durable items under `knowledge/items/**`.
- `deferred.jsonl`: candidates intentionally postponed for later review.
- `rejected.jsonl`: duplicates, low-value items, off-topic items, blocked sources, or broken pages.

These files are created automatically by `knowledge/raw/manage_candidates.py`.

## Commands

```powershell
.\kb.ps1 watch --limit 20
.\kb.ps1 watch --summary
.\kb.ps1 watch --group-by source --limit 20
.\kb.ps1 watch --group-by topic --limit 20
.\kb.ps1 watch --group-by type --limit 20
.\kb.ps1 watch --json --limit 5
python knowledge\raw\manage_candidates.py validate
python knowledge\raw\manage_candidates.py seed-browser --limit-per-snapshot 12
python knowledge\raw\manage_candidates.py seed-browser --limit-per-snapshot 12 --replace-inbox
.\kb.ps1 promote CAND-2026-0001 --dry-run
.\kb.ps1 promote CAND-2026-0001 --method browser --profile qmvqcrb8
.\kb.ps1 defer CAND-2026-0001 --reason "review later" --until 2026-06-16
.\kb.ps1 reject CAND-2026-0001 --reason "duplicate or low value"
.\kb.ps1 restore CAND-2026-0001 --from-bucket deferred --reason "ready to review"
.\kb.ps1 bulk --action show --ids anthropic-news --limit 5
.\kb.ps1 bulk --action defer --ids anthropic-news --query "announcement" --limit 2 --reason "review later" --until 2026-06-16 --execute
.\kb.ps1 bulk --action reject --type product --limit 2 --reason "low-value product radar" --execute
.\kb.ps1 watch --bucket deferred --limit 20
.\kb.ps1 watch --bucket rejected --limit 20
```

Current behavior:

- Browser snapshots append relevant discovered links to `inbox.jsonl`.
- Existing browser snapshots can be backfilled with `seed-browser`.
- Use `--replace-inbox` only when rebuilding generated browser-snapshot candidates from scratch.
- RSS captures append successfully captured entries to `promoted.jsonl`.
- `promote` turns one inbox candidate into a durable item, then moves the candidate to `promoted.jsonl`.
- `defer` removes a candidate from the active inbox but keeps a revisit reason/date.
- `reject` removes a candidate from the active inbox and records why it should not be reviewed again.
- `restore` moves a deferred or rejected candidate back to `inbox.jsonl` and keeps prior status notes in `status_history`.
- `bulk` filters candidates by source ID, type, status, text query, bucket, and limit. `show` is read-only; `defer` and `reject` are dry-run by default and require both `--reason` and `--execute` to write.
- `.\kb.ps1 audit` validates candidate JSONL shape and duplicate candidate IDs/URLs.
- `watch` can now show a flat list, compact summary, grouped text view, or JSON payload. `--group-by` accepts `source`, `type`, `topic`, `route`, `date`, or `status`; `--json` is intended for scripts, dashboards, or other agents.

Browser candidate filtering is intentionally stricter than full-text search:

- Keep item-like URLs: article pages, paper pages, GitHub repo roots, Product Hunt product/post pages.
- Drop navigation, source homepages, category pages, sign-in/pricing/support pages, social links, and product-marketing entry points.
- Do not treat a broad source domain such as `ai.meta.com` as sufficient relevance; title/path evidence must still match AI-agent keywords or known item shapes.
- Candidate IDs are allocated incrementally across a batch, so `CAND-YYYY-0001` style IDs remain unique.

## Candidate Rules

1. Keep the source URL and evidence path.
2. Record why the item might be useful.
3. Prefer a topic hint, not a final topic, until promotion.
4. Do not promote without creating `summary.md`, `article.md`, `source.md`, and `raw/`.
5. Defer candidates when they are relevant but not urgent.
6. Reject candidates when they are duplicate, off-topic, low-value, blocked, or broken.

## Promotion Rule

Promoting a candidate should:

1. Create a durable item under `knowledge/items/<topic>/<ID>/`.
2. Preserve source evidence in item-level `raw/`.
3. Update `knowledge/catalog/articles-index.md`.
4. Update a specialized index when applicable, such as `paper-index.md` or `source-article-index.md`.
5. Rebuild retrieval and run eval when the batch is meaningful.

Use `--dry-run` before promotion when a candidate may be duplicated, low-value, or difficult to fetch. Use `--method browser --profile qmvqcrb8` for logged-in or JavaScript-rendered pages that HTTP cannot extract.

## Restore Rule

Restoring a candidate should:

1. Move it from `deferred.jsonl` or `rejected.jsonl` back to `inbox.jsonl`.
2. Reset `status` to `radar`.
3. Clear active `reject_reason` / `defer_reason` fields.
4. Preserve prior status notes in `status_history`.
5. Re-run candidate validation after bulk restore operations.

## Bulk Review Rule

Use bulk review for queue hygiene, not for deep capture.

1. Always preview first with `.\kb.ps1 bulk --action show ...`.
2. Keep write batches small enough to inspect, usually `--limit 1` to `--limit 10`.
3. Bulk `defer` when candidates are relevant but not urgent.
4. Bulk `reject` when candidates are duplicate, off-topic, blocked, broken, or repeatedly low value.
5. Bulk promotion is intentionally not supported; promote durable items one at a time so evidence, topic, and capture quality stay reviewable.
