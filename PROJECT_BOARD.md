# Project Board

Last reviewed: 2026-06-18

This board turns the repository from an article collection into a managed knowledge and product pipeline.

Use it with:

```powershell
.\kb.ps1 weekly-review
.\kb.ps1 weekly-review --eval
.\kb.ps1 weekly-review --write
.\kb.ps1 coverage --write
.\kb.ps1 obsidian-card BB-2026-05-01-564 --module control-loop
```

## Operating Principle

Articles are raw material. The durable deliverables are:

- captured evidence
- topic synthesis
- reusable project/product decisions
- learning paths
- product features

Every new signal should move through one of these paths:

`radar -> candidate -> captured item -> synthesis -> product/learning output`

## Current Snapshot

Generated from `.\kb.ps1 status` on 2026-06-18.

| Metric | Value |
| --- | ---: |
| Catalog rows | 592 |
| Latest BestBlogs ID | BB-2026-05-01-573 |
| BestBlogs rows | 561 |
| arXiv rows | 5 |
| RSS rows | 18 |
| Browser snapshots | 7 |
| Retrieval items | 592 |
| FTS chunks | 6888 |
| Candidate inbox | 39 |

## Workstreams

### 1. Radar

Goal: discover signals without polluting the durable knowledge base.

Definition of done:

- candidate is reviewed within 7 days
- candidate is promoted, deferred, or rejected with a reason
- source health is updated if a route fails

Current queue:

| Status | Count | Next action |
| --- | ---: | --- |
| inbox | 39 | group by source and review in batches of 20 |
| promoted | 1 | keep as provenance |
| deferred | 1 | revisit when source/topic is active |
| rejected | 1 | keep reason to avoid repeated work |

Commands:

```powershell
.\kb.ps1 watch --group-by source --limit 50
.\kb.ps1 watch --group-by topic --limit 50
.\kb.ps1 bulk --action show --limit 20
```

### 2. Capture

Goal: convert selected signals into durable items with evidence.

Definition of done:

- `summary.md`, `article.md`, `source.md`, `raw/`, and `item.json` exist
- `knowledge/catalog/articles-index.md` is updated
- `AI_AGENT_MEMORY.md` records the batch when appropriate
- verification and retrieval rebuild pass

Current policy:

- capture at most 60 new BestBlogs articles per week
- stop a batch when duplicates or low-value items dominate
- separate data-batch changes from tooling changes in commits

Commands:

```powershell
.\kb.ps1 capture --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date 2026-06-18
.\kb.ps1 verify
.\kb.ps1 build-item-metadata --execute
.\kb.ps1 rebuild
.\kb.ps1 audit
```

### 3. Synthesis

Goal: turn captured articles into reusable topic-level understanding.

Definition of done:

- at least one topic index links the item
- the item contributes a claim, pattern, timeline point, comparison, or open question
- `brief` or `pack` can retrieve the synthesized view

Current priority topics:

| Topic | Why it matters | Next synthesis |
| --- | --- | --- |
| Agent evaluation and skills | New items BB-540, BB-549, BB-562 strengthen the eval track. | Update `agent-evaluation-benchmarks.md`. |
| Agent memory and context | Corpus is now large enough to compare memory, RAG, compression, and PDF extraction. | Update `agent-memory-context-engineering.md`. |
| Production-safe agent loops | New items BB-522, BB-564, BB-572 connect reliability, audit trails, and security. | Add a control-loop synthesis note or section. |
| Claude Code and skills | New skill-related items BB-515, BB-523, BB-525 connect skills, engineering brain, and workflows. | Update `claude-code-operating-guide.md`. |

Command bridge:

```powershell
.\kb.ps1 obsidian-card <KB-ID> --module eval --write
.\kb.ps1 obsidian-card <KB-ID> --module security --write
.\kb.ps1 obsidian-card BB-2026-05-01-572 --register-existing "D:\webstudy\Notes\obsidian\黑曜石\学习笔记\AI-Agent\05-Agent安全\2026-06-18-Agent权限边界与Confused-Deputy.md" --module security
```

Use this bridge to create an Obsidian draft from a captured item. The generated card is a starting point; the synthesis is done only after personal notes, links, and reusable claims are edited in Obsidian.

Registered cards are tracked in `knowledge/catalog/obsidian-card-index.md` and `knowledge/obsidian/cards-index.jsonl`. This table is the project-side guard against duplicating synthesis work.

### 4. Product

Goal: expose knowledge as a usable learning system, not just files.

Definition of done:

- feature reads from the existing knowledge/retrieval layer
- output includes citations or local IDs
- feature is useful in daily study

Current product priorities are tracked in `PRODUCT_NOW.md`.

## WIP Limits

| Area | Limit | Reason |
| --- | ---: | --- |
| Candidate inbox | 50 | Prevent radar backlog from becoming another raw dump. |
| Weekly deep captures | 60 | Keep collection aligned with synthesis capacity. |
| Weekly synthesis targets | 10 items | Force knowledge conversion, not just accumulation. |
| Active product tasks | 3 | Keep MVP execution narrow. |

## Weekly Cadence

| Day | Review | Action |
| --- | --- | --- |
| Monday | `status`, `source-health`, `watch --summary` | Choose source focus and candidate batch. |
| Tuesday | capture reports | Capture or promote selected signals. |
| Wednesday | `verify`, `audit`, `rebuild`, `eval` | Keep corpus healthy. |
| Thursday | topic indexes | Synthesize 5-10 high-value items. |
| Friday | product plan and roadmap | Convert synthesis into product tasks. |
| Weekend | weekly report draft | Review what changed in understanding. |

## Done Criteria for a Weekly Cycle

- `.\kb.ps1 audit` has no missing files or source issues.
- `.\kb.ps1 eval` does not regress materially.
- Candidate inbox is at or below 50.
- At least one topic synthesis was improved.
- `PRODUCT_NOW.md` still reflects the next concrete product step.

## Parking Lot

- Add metadata for item value tier: A/core, B/reference, C/radar.
- Add timeline and compare views once entity/relation extraction is stable.
- Add a product-facing weekly learning report that combines project state with user notes once reading behavior exists.
