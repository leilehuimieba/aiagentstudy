# Repository Structure

This repository is best treated as several adjacent workspaces, not one flat knowledge dump.

## Current Module Boundaries

### Project Entry

- `START_HERE.md`: first operational entry for humans and agents.
- `AGENTS.md`: workspace rules that agents must follow.
- `README.md`: short project overview.
- `kb.ps1`: root command shortcut for knowledge-base search, rebuild, audit, status, and BestBlogs capture.

Keep these files at the root. They make the repository easy to operate without remembering script paths.

### AI-Agent Knowledge Base

- `knowledge/catalog/`: low-token index and topic map. Read this before opening items.
- `knowledge/items/`: curated knowledge entries grouped by agent-topic directories.
- `knowledge/retrieval/`: generated search metadata and SQLite FTS index.
- `knowledge/raw/`: capture scripts, raw evidence, reports, diagnostics, and external mirrors.

This module is for AI-agent study only. Non-agent domains should not enter `knowledge/items/`.

### Study Spaces

- `study_spaces/`: independent long-term study domains.

Each domain should have its own `catalog/`, `items/`, and `raw/` if it grows large. This prevents exam, security, course, or other materials from polluting the AI-agent retrieval surface.

### Product Experiments

- `product/`: runnable product prototype and related product data.
- `docs/PRODUCT_ROADMAP.md`: product direction and planning notes.

Treat product code as a separate application surface. It may read from the knowledge base, but should not define the knowledge-base source of truth.

## Recommended Target Shape

Current top-level shape (root kept to entry + operational-state docs; reference
docs live in `docs/`):

```text
.
|-- START_HERE.md          # entry
|-- AGENTS.md              # entry
|-- README.md             # entry
|-- REPO_STRUCTURE.md     # entry
|-- kb.ps1                # entry
|-- AI_AGENT_MEMORY.md    # operational state (written by capture scripts)
|-- PROJECT_BOARD.md      # operational state (read by weekly-review/coverage)
|-- PRODUCT_NOW.md        # operational state (read by weekly-review/coverage)
|-- docs/                 # reference docs (onboarding + roadmap)
|   |-- AI_AGENT_LEARNING_MODEL.md
|   |-- OPENCLI_NOTES.md
|   |-- KNOWLEDGE_BASE.md
|   `-- PRODUCT_ROADMAP.md
|-- knowledge/
|   |-- catalog/
|   |-- items/
|   |-- retrieval/
|   `-- raw/
|       |-- <stable scripts + README.md + MANIFEST.md>
|       |-- reports/      # batch reports & capture snapshots
|       |-- evidence/     # page/source captures
|       |-- diagnostics/  # one-off scripts & debug data
|       `-- external/     # multi-GB source mirrors (gitignored)
|-- study_spaces/
`-- product/
```

`knowledge/raw/` was the main cleanup target (it mixed stable scripts, historical
one-off scripts, raw page captures, batch reports, diagnostics, and multi-GB
external mirrors). As of 2026-06-30 the loose root was sorted into the
`reports/`, `evidence/`, `diagnostics/`, and `external/` subdirectories above;
only the stable, `kb.ps1`-referenced scripts plus `README.md`/`MANIFEST.md` remain
at the `knowledge/raw/` root.

## Raw Workspace Classification

Use these categories when adding or reorganizing raw material:

- `stable`: scripts used by current workflows, such as capture, query, retrieval build, verify, and audit.
- `evidence`: page states, content exports, network responses, and source snapshots that support a specific captured item.
- `reports`: batch reports and audit outputs.
- `diagnostics`: temporary debugging files, smoke tests, failed captures, and one-off probes.
- `external`: mirrored third-party source material used for deep study.

For now these categories are documented instead of physically enforced, because moving old files could break scripts or historical references.

## What Should Stay As-Is

- Keep `knowledge/catalog/` as the first lookup layer.
- Keep `knowledge/items/<topic>/<ID>/summary.md`, `article.md`, `source.md`, and `raw/` as the curated item format.
- Keep `knowledge/retrieval/` generated and rebuildable.
- Keep `study_spaces/` separate from `knowledge/`.
- Keep `kb.ps1` at the root as the stable command facade.

## What Should Be Cleaned Carefully

### 1. Root temporary files

Root files matching `tmp_*`, `tmp-*.html`, and similar diagnostics should not remain at the project root long term. They should either be moved under `knowledge/raw/diagnostics/` or deleted after confirming they are no longer needed.

### 2. External mirrors

`knowledge/raw/external/` is much larger than the curated knowledge base. Current large mirrors include:

- `claw-code`: largest external source mirror.
- `hello-agents`: large external source mirror.
- `claude-code`: smaller source mirror.
- `claude-code-npm`: npm package snapshot.
- `zhihu-2022433246449780672`: single-source article evidence.

Before moving or deleting these, decide whether they should be:

- kept in the repository as evidence,
- moved outside the repository and referenced by manifest,
- converted to a Git submodule,
- stored through Git LFS,
- or reduced to curated summaries plus source links.

### 3. Historical capture scripts

Old `capture-*`, `add-*`, `process-*`, and candidate scripts are useful as provenance, but they should not be the default path for future agents. Current agents should use:

- `.\kb.ps1 capture ...`
- `knowledge/raw/capture-opencli-latest-page.py`
- `.\kb.ps1 verify`
- `.\kb.ps1 rebuild`
- `.\kb.ps1 audit`

## Suggested Phased Cleanup

### Phase 1: Document and index

Add manifests and READMEs. Do not move large data yet.

- Add this repository structure guide.
- Add `knowledge/raw/external/README.md`.
- Optionally add `knowledge/raw/MANIFEST.md` for stable scripts and file families.

### Phase 2: Isolate diagnostics

Move or delete only obvious temporary root diagnostics after confirming they are not needed. Keep the `.gitignore` rules so new diagnostics do not clutter status.

### Phase 3: Decide external mirror policy

Pick one policy for `knowledge/raw/external/`. The most practical default is to keep small evidence snapshots in the repo and move large source mirrors outside the repo with a manifest that records path, origin, commit or version, and why it matters. Start with `knowledge/raw/external/MANIFEST.md`; `claw-code` is the first migration candidate because it dominates external mirror size.

### Phase 4: Split pipeline only if needed

If `knowledge/raw/` keeps growing, create a clearer pipeline directory:

```text
knowledge/
|-- pipeline/
|   |-- capture/
|   |-- retrieval/
|   `-- audit/
`-- raw/
    |-- evidence/
    |-- reports/
    |-- diagnostics/
    `-- external/
```

Do this only after the stable scripts have tests or wrappers, because path changes can break capture workflows.

## Agent Navigation Rule

When answering questions or doing maintenance:

1. Start at `START_HERE.md`.
2. Use `kb.ps1` for search, status, audit, rebuild, and capture.
3. Read `knowledge/catalog/` before item summaries.
4. Read full `article.md` only when needed.
5. Treat `knowledge/raw/` as evidence and tooling, not as the primary knowledge interface.
6. Avoid reading or moving `knowledge/raw/external/` unless the task explicitly needs source-level study.
