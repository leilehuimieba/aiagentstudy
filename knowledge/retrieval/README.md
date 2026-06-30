# Retrieval Layer

Programmatic local retrieval for the AI agent knowledge base.

Scope note: this retrieval layer indexes `knowledge/items/**` only.
Other study domains should live under `study_spaces/` so they stay out of this agent-focused index.

## Outputs

- `articles-meta.json`: structured metadata array
- `articles-meta.jsonl`: one JSON object per item
- `kb.sqlite`: SQLite database with FTS5 search
- `embeddings.npy` + `embeddings-meta.json`: dense (semantic) vector index, row-aligned to `kb.sqlite` chunk rowids
- `aliases.json`: curated query aliases injected into retrieval metadata

`aliases.json` is a source file, not a generated report. Use it for stable synonyms, English/Chinese names, product aliases, and evidence-oriented search phrases that should not require editing every `summary.md`.

## Retrieval model

Hybrid search fuses three channels with Reciprocal Rank Fusion (RRF):

1. **Item BM25** — FTS5 over item-level fields (title, takeaway, tags, summary…)
2. **Chunk BM25** — FTS5 over ~1400-char article chunks
3. **Dense vectors** — cosine over `BAAI/bge-m3` (1024-dim) chunk embeddings, for
   paraphrase/cross-lingual (中⇄英) semantic recall that pure lexical (trigram)
   matching misses

The dense channel needs `sentence-transformers` + the bge-m3 weights, both in
`knowledge/retrieval/.venv` / `knowledge/retrieval/models/bge-m3` (Python 3.12,
which also ships SQLite ≥ 3.34 for FTS5). When either is absent the search
**degrades gracefully to BM25 only** — nothing breaks, recall just drops on
paraphrased queries. Pass `--no-dense` to force the BM25-only baseline.

Measured (RRF dense weight = 1.0, `KB_DENSE_WEIGHT` to override):

| eval set | metric | BM25-only | hybrid (bge-m3) |
|---|---|---|---|
| 52 lexical cases  | hit@5 / mrr      | 1.00 / 1.00 | 1.00 / 1.00 |
| 52 lexical cases  | recall@10 / ndcg | 0.973 / 0.971 | **0.989 / 0.988** |
| 12 paraphrase cases | recall@10 / ndcg | 0.382 / 0.262 | **0.528 / 0.353** |

Latency: BM25-only ~0.5s. Hybrid is ~10s **cold** (bge-m3 load ~9s + embed ~0.3s)
but **<1s warm** thanks to the resident embedding daemon below.

### Embedding daemon (warm hybrid queries)

Each `kb.ps1 search` spawns a fresh python, and `eval-search.py` spawns one *per
query*, so without a daemon every hybrid query re-pays the ~9s bge-m3 load. The
daemon (`knowledge/raw/embed_daemon.py`) loads the model once into a background
process listening on `127.0.0.1`, and `embed_lib.encode_query()` routes through
it — dropping warm queries to ~0.3–0.5s (a full 52-case `eval` likewise loads the
model once instead of 52×).

It is **lazy-started on the first hybrid query** (never on boot) and **leaves no
autostart entry** — after a reboot nothing runs until the next query spawns it
again. State lives in `.embed-daemon.json` (pid/port lock) + `.embed-daemon.log`
(both gitignored). Control it with:

- `.\kb.ps1 daemon status` — pid / port / uptime, or "not running"
- `.\kb.ps1 daemon stop` — free its ~2.5GB RAM (restarts lazily on the next query)
- `.\kb.ps1 daemon start` / `restart` — load now / reload (e.g. after `rebuild-embeddings`)

Env knobs: `KB_NO_DAEMON=1` forces pure in-process encoding (skips the daemon);
`KB_DAEMON_IDLE_SEC=1800` makes it auto-exit after that many idle seconds (default
`0` = resident until reboot or manual stop).

## Build

1. `node knowledge\raw\build-kb-retrieval.js`
2. `python knowledge\raw\build-kb-fts.py`  (use the venv / a SQLite ≥ 3.34 interpreter)
3. `knowledge\retrieval\.venv\Scripts\python knowledge\raw\build-kb-embeddings.py`

Or just `.\kb.ps1 rebuild` (runs all three; auto-resolves the venv) and
`.\kb.ps1 rebuild-embeddings` to refresh only the vector index.

One-time setup (venv + model weights):

```
# venv (Python 3.12 has a new enough SQLite for FTS5 and supports torch)
py -V:Astral/CPython3.12.12 -m venv knowledge\retrieval\.venv
knowledge\retrieval\.venv\Scripts\python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
knowledge\retrieval\.venv\Scripts\python -m pip install sentence-transformers numpy

# bge-m3 weights vendored locally (gitignored). hf.co is often unreachable in CN;
# hf-mirror.com has no unauthenticated rate-limit and curl -C - resumes reliably.
$d = "knowledge\retrieval\models\bge-m3"; mkdir $d, "$d\1_Pooling"
$base = "https://hf-mirror.com/BAAI/bge-m3/resolve/main"
foreach ($f in "config.json","config_sentence_transformers.json","modules.json","sentence_bert_config.json","tokenizer.json","tokenizer_config.json","special_tokens_map.json","sentencepiece.bpe.model") { curl.exe -sL "$base/$f" -o "$d\$f" }
curl.exe -sL "$base/1_Pooling/config.json" -o "$d\1_Pooling\config.json"
curl.exe -L -C - --retry 10 --retry-all-errors -o "$d\pytorch_model.bin" "$base/pytorch_model.bin"
```

`embed_lib.py` loads from `models/bge-m3` if present (fully offline), else falls
back to the `BAAI/bge-m3` hub id.

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
