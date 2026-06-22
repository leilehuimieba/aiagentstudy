# AI Agent Study Workspace

This folder is a durable context capsule and local knowledge base for studying AI agents.

For day-to-day operation, start with `START_HERE.md`.
For module boundaries and cleanup policy, read `REPO_STRUCTURE.md`.

> Scope note: `knowledge/` is the AI-agent learning knowledge base only.
> Non-agent study materials should go under `study_spaces/` so they do not pollute agent retrieval, indexing, or audit flows.

Read `AGENTS.md`, `AI_AGENT_MEMORY.md`, `AI_AGENT_LEARNING_MODEL.md`, `OPENCLI_NOTES.md`, and `KNOWLEDGE_BASE.md` first.

For the knowledge base, use `knowledge/catalog/` first and read full articles only when needed.

For local search over a growing knowledge base, build `knowledge/retrieval/` and query that layer first.

Use `study_spaces/` for other long-term study domains such as exams, courses, or non-agent topic collections.

## Working Flow

1. Read the workspace instructions first.
2. Use `knowledge/catalog/` as the low-token entry point.
3. Open `summary.md` before `article.md`.
4. Preserve evidence when capturing new items.
5. Verify each completed batch with `node knowledge\\raw\\verify-batch.js`.
6. Rebuild local retrieval after meaningful knowledge-base changes:
   - `node knowledge\\raw\\build-kb-retrieval.js`
   - `python knowledge\\raw\\build-kb-fts.py`
7. Run search eval after retrieval changes: `.\kb.ps1 eval`

## Quick Commands

```powershell
python knowledge\raw\query-kb.py "Claude" --mode search --limit 5
python knowledge\raw\query-kb.py "智能体评估" --mode pack --limit 5
node knowledge\raw\audit-kb.js
```

Shortcut:

```powershell
.\kb.ps1 search "Claude" --limit 5
.\kb.ps1 pack "智能体评估" --limit 5
.\kb.ps1 search "browser runtime harness" --topic 03-control-loop --expand-topic
.\kb.ps1 pack "Claude Code auto mode 原文 来源" --profile auto
.\kb.ps1 pack "Harness Engineering 权限 日志 验证" --profile deep --grouped
.\kb.ps1 audit
.\kb.ps1 eval
.\kb.ps1 status
```

See `knowledge/raw/README.md` for capture, verification, and retrieval maintenance commands.
See `knowledge/raw/MANIFEST.md` when deciding which raw files are stable, historical, diagnostic, or external evidence.

## Knowledge Capture Rule

Each collected item should preserve:

- `summary.md`: low-token summary and agent-model mapping
- `article.md`: full text when available
- `source.md`: BestBlogs URL plus original publisher URL when exposed
- `raw/`: raw extraction data and debugging evidence

Do not claim capture success unless `article.md`, `source.md`, and index updates are actually written.

## Git Notes

- Remote repository: `git@github.com:leilehuimieba/aiagentstudy.git`
- Default branch: `main`
- Line endings are normalized with `.gitattributes`
