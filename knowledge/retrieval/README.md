# Retrieval Layer

Programmatic local retrieval for the AI agent knowledge base.

Scope note: this retrieval layer indexes `knowledge/items/**` only.
Other study domains should live under `study_spaces/` so they stay out of this agent-focused index.

## Outputs

- `articles-meta.json`: structured metadata array
- `articles-meta.jsonl`: one JSON object per item
- `kb.sqlite`: SQLite database with FTS5 search
- `aliases.json`: curated query aliases injected into retrieval metadata

`aliases.json` is a source file, not a generated report. Use it for stable synonyms, English/Chinese names, product aliases, and evidence-oriented search phrases that should not require editing every `summary.md`.

## Build

1. `node knowledge\raw\build-kb-retrieval.js`
2. `python knowledge\raw\build-kb-fts.py`

## Query

- `python knowledge\raw\query-kb.py "Claude Code auto mode"`
- `python knowledge\raw\query-kb.py "context engineering" --topic 01-context-memory`
- `python knowledge\raw\query-kb.py "自动模式" --limit 3 --json`
- `python knowledge\raw\query-kb.py "自动模式" --mode pack --limit 3`

## Retrieval Rule

Use this layer to narrow candidates before opening article files:

1. Search `kb.sqlite` or `articles-meta.jsonl`
2. Read matched `summary.md`
3. Open `article.md` only for evidence or deep reading

## Modes

- `--mode search`: human-readable search results with scores and snippets
- `--mode pack`: stable low-variance context pack for model input, designed to reduce prompt-shape drift and help cache reuse
