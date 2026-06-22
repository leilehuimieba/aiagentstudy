# Knowledge System Optimization Blueprint

Last updated: 2026-06-09

This document combines the current AI-agent knowledge-base experience with the target of building a general-purpose knowledge capture, storage, retrieval, and display system.

The local `knowledge/` folder remains scoped to AI-agent learning. The architecture below is intentionally domain-general so it can be reused later for other study spaces.

## North Star

Build a knowledge system that can:

1. Capture information from many source types.
2. Preserve raw evidence and source links.
3. Store normalized human-readable knowledge items.
4. Maintain machine-readable metadata for search and reuse.
5. Route new material through a quality pipeline before it becomes long-term knowledge.
6. Display the same knowledge differently for learning, research, engineering, decision-making, evidence review, and daily radar.

In short:

`source -> raw evidence -> candidate -> captured item -> retrieval index -> synthesized knowledge`

## Design Principles

| Principle | Meaning |
| --- | --- |
| Evidence first | Every durable item keeps `source.md` and `raw/` evidence. |
| Progressive disclosure | Use catalog and summaries before opening full text. |
| Capture routes are pluggable | RSS, API, browser, HTTP, PDF, file, repo, and media routes should share the same output contract. |
| Not everything deserves deep capture | Radar snapshots and RSS entries should feed a candidate queue before deep work. |
| Search is not one mode | Humans need briefs, evidence, timelines, comparisons, and watch views; models need stable context packs. |
| Domain-general, locally scoped | The method should work for any topic, but this workspace keeps `knowledge/` AI-agent-only. |

## Storage Layers

| Layer | Folder | Purpose |
| --- | --- | --- |
| Raw evidence | `knowledge/raw/` and item-level `raw/` | HTML, browser state, API JSON, RSS entries, extracted text, screenshots, diagnostics. |
| Candidate queue | `knowledge/candidates/` | Radar links and source signals that may later be promoted. |
| Durable items | `knowledge/items/<topic>/<ID>/` | `summary.md`, `article.md`, `source.md`, `raw/`. |
| Catalogs | `knowledge/catalog/` | Low-token maps, indexes, coverage, topic indexes. |
| Retrieval | `knowledge/retrieval/` | JSONL metadata, SQLite FTS, eval cases, search reports. |
| Schema | `knowledge/schema/` | Local contracts for items, sources, candidates, capture runs, and views. |

## Universal Item Model

Every durable item should be representable with these fields, even if some are only inferred from markdown today:

| Field | Meaning |
| --- | --- |
| `id` | Stable local ID, such as `BB-*`, `ARXIV-*`, `RSS-*`, `BROWSER-*`. |
| `type` | `article`, `paper`, `webpage_snapshot`, `forum_thread`, `repo`, `pdf`, `video`, `dataset`, `note`. |
| `status` | `radar`, `candidate`, `captured`, `synthesized`, `archived`. |
| `title` | Human-readable title. |
| `source_id` | Source registry ID when available. |
| `source_name` | Human-readable source name. |
| `source_url` | Captured URL or discovery URL. |
| `original_url` | Original publisher/source URL when different. |
| `captured_at` | Capture timestamp or collection date. |
| `published_at` | Source publication date when known. |
| `topic` | Local topic directory. |
| `tags` | Search and routing hints. |
| `entities` | People, products, models, organizations, repositories, papers. |
| `claims` | Key claims worth verifying or reusing. |
| `evidence` | Source links, raw paths, page state, feed entries, screenshots. |
| `relations` | Links to related local IDs or upstream sources. |

## Capture Routes

| Route | Best For | Output Contract |
| --- | --- | --- |
| `rss` | Blogs, newsletters, official feeds | Feed entry, extracted page text, source evidence. |
| `api` | arXiv, OpenReview, Semantic Scholar, GitHub APIs | Structured metadata, abstracts, URLs, raw JSON. |
| `browser` | Logged-in, dynamic, JS-rendered, or UI-state pages | Browser state, rendered text, links, raw OpenCLI result. |
| `http` | Static pages | HTML, extracted text, headers, source evidence. |
| `pdf` | Papers, reports, white papers | PDF file/path, extracted text, metadata, page evidence. |
| `file` | Local documents, notes, datasets | File metadata, extracted text, source path. |
| `repo` | GitHub projects and codebases | README, metadata, release notes, selected files. |
| `media` | Videos and podcasts | Transcript, metadata, source URL, timestamped evidence. |

All routes should either write a candidate or a durable item with the same core evidence contract.

## Candidate Lifecycle

| Stage | Meaning | Action |
| --- | --- | --- |
| `radar` | Source snapshot or feed item observed. | Store in `knowledge/candidates/inbox.jsonl`. |
| `candidate` | Worth reviewing for relevance. | Add reason, source, and proposed topic. |
| `captured` | Promoted into `knowledge/items/**`. | Create `summary.md`, `article.md`, `source.md`, `raw/`, update indexes. |
| `synthesized` | Used in a topic guide, comparison, or principle. | Link from a topic index or synthesis note. |
| `deferred` | Relevant but lower priority or waiting for timing/context. | Move to `deferred.jsonl` with reason and optional revisit date. |
| `rejected` | Low value, duplicate, blocked, or off-topic. | Record reason in `rejected.jsonl` to avoid repeated work. |

This prevents the system from becoming a pile of raw captures.

## Display Modes

| Mode | Use Case | Example Future Command |
| --- | --- | --- |
| `search` | Find relevant items. | `.\kb.ps1 search "agent memory"` |
| `pack` | Provide stable context to an AI assistant. | `.\kb.ps1 pack "Claude Code auto mode" --profile auto` |
| `brief` | Human short summary across items. | `.\kb.ps1 brief "browser use agents"` |
| `evidence` | Source links, raw paths, and evidence pointers. | `.\kb.ps1 evidence "Project Glasswing"` |
| `timeline` | Topic evolution over time. | `.\kb.ps1 timeline "AI coding agents"` |
| `compare` | Compare tools, models, papers, or patterns. | `.\kb.ps1 compare "LangGraph AutoGen CrewAI"` |
| `watch` | Show newest source signals. | `.\kb.ps1 watch --group-by source --limit 20` |
| `bulk` | Preview or clean candidate batches. | `.\kb.ps1 bulk --action show --ids anthropic-news` |
| `promote` | Turn a candidate into a durable item. | `.\kb.ps1 promote CAND-2026-001` |
| `source-health` | Review source coverage, backlog, and probe health. | `.\kb.ps1 source-health --limit 20` |
| `build-item-metadata` | Generate stable item JSON sidecars. | `.\kb.ps1 build-item-metadata --execute` |

The immediate system already has `search`, `pack`, `brief`, `evidence`, `status`, `source-health`, `build-item-metadata`, `audit`, `repair-audit`, `eval`, capture commands, and a candidate review loop from `watch` to `bulk` to `promote`.

## Current Optimization Priorities

| Priority | Change | Why |
| --- | --- | --- |
| P1 | Add candidate queue files and schema. | Stop radar captures from becoming long-term clutter. |
| P1 | Emit candidate links from browser snapshots. | Make source radar actionable. |
| P1 | Add `watch`, `bulk`, and `promote` commands. | Turn collection into a repeatable workflow. |
| P2 | Add `brief` and `evidence` views. | Make retrieval output useful for humans and AI agents. |
| P2 | Add source health reports. | Track which sites fail, redirect, challenge, or need browser state. |
| P3 | Add vector or hybrid semantic retrieval. | Improve concept search once the corpus grows further. |
| P3 | Add entity/relation extraction. | Support comparison, timelines, and synthesis. |

## Minimum Next Implementation

1. Done: create candidate JSONL files automatically through `knowledge/raw/manage_candidates.py`.
2. Done: browser snapshots append filtered item-like links to `knowledge/candidates/inbox.jsonl`.
3. Done: RSS captures append successfully captured entries to `knowledge/candidates/promoted.jsonl`.
4. Done: add `.\kb.ps1 watch` to show source radar candidates.
5. Done: extend audit to validate candidate JSONL shape and duplicate IDs/URLs.
6. Done: add batch-safe candidate ID allocation and browser-candidate noise filters for navigation, category, social, and product-entry links.
7. Done: add `.\kb.ps1 promote` to turn one inbox candidate into a durable item, with `--dry-run`, HTTP capture, and OpenCLI Browser Bridge capture for logged-in/dynamic pages.
8. Done: add `reject` and `defer` commands so low-value or lower-priority candidates can leave the active inbox without losing provenance.
9. Done: add `restore` command for revisiting deferred or mistakenly rejected candidates while preserving status history.
10. Done: add bulk candidate review helpers for filtered previews, batch deferral, and batch rejection from the active inbox.
11. Done: add `repair-audit` for low-risk catalog/summary normalization.
12. Done: add `evidence` view for source links, local evidence paths, and raw file pointers.
13. Done: add `brief` view for human-facing topic synthesis.
14. Done: add `source-health` reports for local source coverage, candidate backlog, probe status, and recommended next action.
15. Done: add `item.json` metadata sidecars to reduce markdown parsing and give scripts a stable structured contract.
16. Done: update `audit` and `source-health` internals to use or validate `item.json`.
17. Done: update retrieval build internals to prefer `item.json` when present while preserving markdown/index fallback.
18. Done: normalize historical item metadata so external papers, repos, web articles, and local synthesis notes are not misclassified as BestBlogs items; tighten source-evidence audit checks to apply BestBlogs URL requirements only to real BestBlogs captures.
19. Done: normalize remaining catalog/summary naming drift by replacing raw title separators like `| Claude` with markdown-table-safe `/ Claude` forms and aligning local synthesis source names.
20. Done: add article-length quality overrides so known-short abstracts, benchmark stubs, spec summaries, README excerpts, and short pages are recorded as accepted short captures instead of unresolved audit warnings.
21. Done: add `health` / `audit-summary` compact status output for red/green corpus checks without reading the full audit JSON.
22. Done: extend `watch` with summary, grouped, and JSON views so candidate review remains usable as source volume grows.

## Non-Goals

- Do not mix unrelated domains into `knowledge/items/`.
- Do not deep-capture every feed or browser link.
- Do not rely on browser snapshots as final evidence.
- Do not replace markdown with a database-only format; human-readable files remain the durable source of truth.
