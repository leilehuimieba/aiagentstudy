# Current Knowledge Coverage

Last organized: 2026-06-18

Use this page to understand what is already in the AI-agent knowledge base before starting another collection pass.

## Snapshot

| Area | Count | Notes |
| --- | ---: | --- |
| BestBlogs full captures | 561 | Main curated article corpus. Latest ID: `BB-2026-05-01-573`. |
| arXiv paper captures | 10 | Paper metadata and abstracts, indexed in `paper-index.md`. |
| RSS article captures | 28 | Official/engineering/newsletter captures, indexed in `source-article-index.md`. |
| Browser source snapshots | 8 | OpenCLI Browser Bridge rendered source radar pages. |
| Candidate promotions | 1 | Durable items promoted from candidate radar. |
| Total catalog rows | 608 | Retrieval should be rebuilt after meaningful collection. |
| Retrieval chunks | 6904 | SQLite FTS chunks generated from `articles-meta.jsonl`. |
| Candidate inbox | 45 | Radar candidates waiting for promote/defer/reject review. |

## Candidate Queue

| Bucket | Count |
| --- | ---: |
| inbox | 45 |
| promoted | 7 |
| deferred | 1 |
| rejected | 1 |

## Topic Distribution

| Topic | Count |
| --- | ---: |
| `01-context-memory` | 159 |
| `02-tools-actions` | 137 |
| `03-control-loop` | 80 |
| `04-evaluation-guardrails` | 104 |
| `05-security-techniques` | 4 |
| `06-frontier-radar` | 124 |

## Reading Order

1. Use `articles-index.md` for the complete corpus.
2. Use `paper-index.md` for paper-only lookup.
3. Use `source-article-index.md` for RSS and browser-captured source items.
4. Open only the matching `summary.md` first.
5. Open `article.md` when evidence, exact wording, or deeper reading is needed.

## Capture Routes

| Need | Command |
| --- | --- |
| Latest BestBlogs articles | `.\kb.ps1 capture --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date 2026-06-18` |
| Latest arXiv candidates | `.\kb.ps1 capture-arxiv --latest-candidates --limit 5` |
| RSS sources | `.\kb.ps1 capture-rss --ids langchain-blog simon-willison latent-space --limit 5` |
| Browser-rendered source radar | `.\kb.ps1 capture-browser --ids openai-news jiqizhixin github-trending huggingface-papers --profile qmvqcrb8 --limit 4` |
| Check source health | `.\kb.ps1 source-health --limit 20` |
| Watch candidate radar | `.\kb.ps1 watch --limit 20` |
| Rebuild search | `.\kb.ps1 rebuild` |
| Verify search quality | `.\kb.ps1 eval` |
| Review project management | `PROJECT_BOARD.md` and `PRODUCT_NOW.md` |

## Current Project Management Notes

- Capture throughput is now strong; synthesis and productization are the bottlenecks.
- Use `PROJECT_BOARD.md` for the radar/capture/synthesis/product workstreams.
- Use `PRODUCT_NOW.md` for the current two-week execution cycle.
- Keep candidate inbox below 50 and promote/defer/reject candidates within 7 days when possible.
- After each meaningful capture batch, run `verify`, `audit`, `rebuild`, and `eval`.

## Known Source Notes

- Browser snapshots are discovery radar, not final article-level evidence.
- Promote important linked articles or papers into deeper items after relevance checks.
- Use `source-health` before adding another source-specific capture path.
- Keep `knowledge/` scoped to AI-agent learning; put unrelated domains under `study_spaces/`.
