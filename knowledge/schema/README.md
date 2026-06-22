# Knowledge Schema

This folder defines local contracts for the knowledge system.

The current implementation stores most data as markdown plus raw evidence. The schema below documents the target shape that scripts should preserve or emit.

## Item

Durable items live under:

```text
knowledge/items/<topic>/<ID>/
  item.json
  summary.md
  article.md
  source.md
  raw/
```

Required logical fields:

| Field | Required | Notes |
| --- | --- | --- |
| `id` | yes | Stable local ID. |
| `type` | yes | `article`, `paper`, `webpage_snapshot`, `repo`, `pdf`, `video`, `forum_thread`, `note`. |
| `status` | yes | Usually `captured`; can become `synthesized`. |
| `title` | yes | Must match catalog closely enough for audit. |
| `source_url` | yes | Captured or source URL. |
| `original_url` | when available | Original publisher/source URL. |
| `topic` | yes | One of the local topic directories. |
| `summary_path` | yes | Path to `summary.md`. |
| `article_path` | yes | Path to `article.md`. |
| `source_path` | yes | Path to `source.md`. |
| `raw_paths` | yes | Evidence paths under `raw/`. |

`item.json` is the machine-readable sidecar for the same durable item. It should remain stable across rebuilds and avoid volatile timestamps. Generate or refresh it with:

```powershell
.\kb.ps1 build-item-metadata
.\kb.ps1 build-item-metadata --execute
```

The sidecar stores stable fields such as `id`, `type`, `title`, `source`, `topic`, `blocks`, `tags`, `source_id`, source URLs, capture metadata, candidate metadata, paper metadata, and local paths. Markdown remains the human-readable source of truth; `item.json` is the structured contract for scripts. Retrieval builds prefer `item.json` for structured fields and keep markdown/index parsing as a compatibility fallback. Metadata generation should infer `type` and `source_id` from evidence URLs and explicit source fields, not only from local ID prefixes.

## Source

Sources are registered in:

```text
knowledge/sources/source-registry.json
```

Important fields:

| Field | Meaning |
| --- | --- |
| `id` | Stable source ID. |
| `name` | Human-readable name. |
| `url` | Landing URL. |
| `rss` / `api` / `docs` | Structured capture endpoints when available. |
| `capture_route` | Preferred route: `rss`, `api`, `http`, `browser`, or combinations. |
| `browser_needed` | Whether OpenCLI Browser Bridge is likely required. |
| `landing_topics` | Default topic routing hints. |
| `queries` | Suggested search/capture queries. |

## Candidate

Candidates are source signals waiting for review or promotion.

Suggested JSONL shape:

```json
{
  "candidate_id": "CAND-2026-001",
  "status": "radar",
  "type": "article",
  "title": "Example title",
  "url": "https://example.com/post",
  "source_id": "openai-news",
  "source_name": "OpenAI News",
  "discovered_at": "2026-06-09",
  "route": "browser",
  "topic_hint": "04-evaluation-guardrails",
  "reason": "Appeared in source snapshot and matches AI-agent keywords.",
  "evidence_path": "knowledge/items/.../raw/page-state.json",
  "promoted_id": "",
  "reject_reason": ""
}
```

Candidate files live under:

```text
knowledge/candidates/inbox.jsonl
knowledge/candidates/promoted.jsonl
knowledge/candidates/deferred.jsonl
knowledge/candidates/rejected.jsonl
```

Use `.\kb.ps1 watch` for the human-facing inbox view, `.\kb.ps1 watch --bucket deferred` or `--bucket rejected` for non-active queues, `.\kb.ps1 bulk --action show ...` for filtered batch previews, and `python knowledge\raw\manage_candidates.py validate` for schema validation.

Bulk `defer` and `reject` only operate on `inbox.jsonl`, require `--reason`, and stay read-only until `--execute` is provided.

When a candidate is restored from `deferred.jsonl` or `rejected.jsonl`, it returns to `inbox.jsonl` with `status: "radar"` and keeps previous status notes in `status_history`.

## Capture Run

Capture runs should keep enough information to explain what happened.

Suggested fields:

| Field | Meaning |
| --- | --- |
| `run_id` | Stable run ID or timestamp. |
| `route` | `rss`, `api`, `browser`, `http`, `pdf`, `repo`, `file`, `media`. |
| `source_ids` | Sources attempted. |
| `started_at` / `finished_at` | Run timing. |
| `captured_ids` | Durable items written. |
| `candidate_ids` | Candidates emitted. |
| `skipped` | Skips with reasons. |
| `errors` | Errors with enough evidence to debug. |
| `raw_report` | Path to full raw run report. |

## View

Views are ways to display the same knowledge for different tasks.

| View | Purpose |
| --- | --- |
| `search` | Ranked retrieval hits. |
| `pack` | Stable AI context pack. |
| `brief` | Human summary. |
| `evidence` | Source links and raw evidence. |
| `timeline` | Topic evolution by date. |
| `compare` | Side-by-side comparison. |
| `watch` | Recent source/candidate radar. |

## Quality Overrides

Quality overrides explain known exceptions without hiding them.

```text
knowledge/quality/article-length-overrides.json
```

`accepted_short_articles` maps local IDs to a short reason and note when `article.md` is intentionally brief. Use this for abstract-only papers, benchmark stubs, spec summaries, README excerpts, metadata-only items, and genuinely short pages. Audit reports these as accepted short captures and reserves unresolved `articleUnder800` warnings for items that still need review.
