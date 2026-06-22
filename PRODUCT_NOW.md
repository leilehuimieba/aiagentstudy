# Product Now

Cycle: 2026-06-18 to 2026-07-02

This file is the two-week execution surface. Keep the long-term plan in `PRODUCT_ROADMAP.md`; keep only active work here.

## Current Reality

The knowledge base is no longer a small prototype corpus.

| Fact | Current value |
| --- | ---: |
| Catalog rows | 592 |
| Latest BestBlogs ID | BB-2026-05-01-573 |
| BestBlogs rows | 561 |
| Retrieval items | 592 |
| FTS chunks | 6888 |
| Candidate inbox | 39 |

The product should now optimize for conversion:

`captured articles -> synthesized understanding -> usable learning/product flows`

## Cycle Goal

Build the first daily-usable learning loop on top of the existing corpus:

1. ask questions with citations
2. choose what to read next
3. record what changed in understanding
4. review the week as learning, not as a raw article list

## Must Ship

### 1. Question Answering MVP

Outcome: ask a natural-language question and receive an answer with local article IDs and dates.

Scope:

- read from `knowledge/retrieval/articles-meta.jsonl` or existing query scripts
- support time hints such as "recent", "this week", and "last month"
- return citations with local IDs and paths
- avoid unsupported answers when retrieval is weak

Done when:

- a command or endpoint answers "AI agent 可靠性最近有什么进展？"
- answer cites at least 3 local items when evidence exists
- empty-domain query clearly says the knowledge base has insufficient evidence

Suggested files:

- `product/api/db.py`
- `product/api/qa.py`
- `product/api/app.py`

### 2. Reading Queue MVP

Outcome: show a short queue of high-value items to read next.

Scope:

- prioritize A-level or synthesis-needed items
- start with rules, not ML
- include why each item is recommended

Initial queue seeds:

| ID | Reason |
| --- | --- |
| BB-2026-05-01-540 | Agent and skill evaluation framework. |
| BB-2026-05-01-549 | SkillTrustBench security benchmark. |
| BB-2026-05-01-558 | PDF extraction layers and RAG quality. |
| BB-2026-05-01-564 | Production-safe agent loop and audit trails. |
| BB-2026-05-01-572 | Agent security checks exposed by real usage. |

Done when:

- `product` can list at least 10 recommended items
- each item has an explanation
- ignored items can be excluded from the next queue

### 3. Topic Briefs

Outcome: the most important topics have human-readable synthesis, not just article lists.

Required updates:

| Topic brief | Additions |
| --- | --- |
| `agent-evaluation-benchmarks.md` | BB-540, BB-549, BB-562 |
| `agent-memory-context-engineering.md` | BB-558 and related context/RAG items |
| `claude-code-operating-guide.md` | BB-515, BB-523, BB-525 |
| control-loop topic | BB-522, BB-564, BB-572 |

Done when:

- each brief has key claims, related items, and open questions
- `.\kb.ps1 brief "<topic>"` surfaces the updated items
- selected A-level items can be converted into Obsidian card drafts with `.\kb.ps1 obsidian-card <ID>`

### 4. Weekly Learning Report Draft

Outcome: generate a local markdown report that answers "what did I learn this week?"

Scope:

- use captured items, notes if present, and topic changes
- separate "new articles" from "new understanding"
- include citations by local ID

Done when:

- running `.\kb.ps1 weekly-review --write` writes a markdown report under `product/data/reports/`
- report includes new concepts, strengthened topics, unresolved questions, and recommended next reads

Suggested file:

- `knowledge/raw/generate-weekly-review.py` for project-state reports
- later: `product/scripts/weekly_report.py` for user-learning reports

## Should Not Do This Cycle

- Do not build account systems.
- Do not rebuild the whole knowledge store.
- Do not add vector search before the citation QA loop works.
- Do not make a polished UI before command/API flows are useful.
- Do not deep-capture every candidate before reviewing value.

## Product Decisions

| Decision | Rationale |
| --- | --- |
| Use the existing knowledge base as source of truth. | `knowledge/items`, `catalog`, and `retrieval` are already stable. |
| Keep user/product data in `product/data/product.sqlite`. | Reading behavior and notes should not pollute curated knowledge items. |
| Start with rule-based ranking. | Current corpus size and metadata are enough for useful MVP behavior. |
| Require local citations. | The core product value is evidence-backed learning. |

## Active Risks

| Risk | Mitigation |
| --- | --- |
| Corpus grows faster than synthesis. | WIP limit: max 60 captures and at least 10 synthesized items per week. |
| Roadmap drifts from reality. | Refresh `current-coverage.md` and this file after each major capture. |
| Candidate queue becomes stale. | Review inbox weekly; promote, defer, or reject within 7 days. |
| Product work starts too broad. | Limit active product tasks to QA, reading queue, topic briefs, and weekly report. |

## Next Review

Review on 2026-07-02:

- Did QA answer real questions with citations?
- Did the reading queue change what I chose to read?
- Did at least three topic briefs become more useful?
- Did the weekly report describe learning rather than only listing articles?
