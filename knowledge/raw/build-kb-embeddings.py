"""Build the dense (semantic) retrieval index.

Reads chunks directly from knowledge/retrieval/kb.sqlite (produced by
build-kb-fts.py) so every embedded vector is row-aligned to a chunk rowid that
already exists in the FTS index. Run this AFTER build-kb-fts.py:

    .venv\\Scripts\\python knowledge\\raw\\build-kb-embeddings.py

Outputs:
  knowledge/retrieval/embeddings.npy        L2-normalized float32 [N, dim]
  knowledge/retrieval/embeddings-meta.json  model + ordered chunk rowids/item_ids/topics
  knowledge/retrieval/embeddings-report.json
"""

import json
import sqlite3
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import embed_lib as E  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = E.ROOT
DB_PATH = ROOT / "knowledge" / "retrieval" / "kb.sqlite"
REPORT_PATH = ROOT / "knowledge" / "retrieval" / "embeddings-report.json"


def load_chunks():
    if not DB_PATH.exists():
        raise SystemExit(
            "Missing kb.sqlite. Run build-kb-retrieval.js + build-kb-fts.py first."
        )
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT rowid, item_id, topic, title, heading, chunk_text
        FROM chunks
        ORDER BY rowid
        """
    ).fetchall()
    con.close()
    return rows


def main():
    rows = load_chunks()
    if not rows:
        raise SystemExit("No chunks found in kb.sqlite.")

    # Embed a CLEAN passage (title + chunk body) rather than the FTS
    # contextual_text. The latter prepends identical "Article:/Topic:/Source:/
    # Section:" boilerplate to every chunk, which injects a large shared vector
    # component, compresses cosine spread, and drowns the discriminative signal.
    # The title gives a lightweight topical anchor without that label noise.
    def passage_text(r):
        title = (r["title"] or "").strip()
        body = (r["chunk_text"] or "").strip()
        return f"{title}. {body}" if title else body

    texts = [passage_text(r) for r in rows]
    print(f"Embedding {len(texts)} chunks with {E.MODEL_NAME} ...", flush=True)
    vectors = E.encode_passages(texts)
    if vectors.shape[1] != E.EMBED_DIM:
        raise SystemExit(
            f"Model produced dim {vectors.shape[1]}, expected {E.EMBED_DIM}. "
            "Update EMBED_DIM in embed_lib.py."
        )

    np.save(E.VECTORS_PATH, vectors.astype(np.float32))

    meta = {
        "model": E.MODEL_NAME,
        "dim": int(vectors.shape[1]),
        "count": int(vectors.shape[0]),
        "chunk_rowids": [int(r["rowid"]) for r in rows],
        "item_ids": [r["item_id"] for r in rows],
        "topics": [r["topic"] for r in rows],
    }
    E.META_PATH.write_text(
        json.dumps(meta, ensure_ascii=False), encoding="utf-8"
    )

    report = {
        "model": E.MODEL_NAME,
        "dim": meta["dim"],
        "chunks": meta["count"],
        "vectors": str(E.VECTORS_PATH.relative_to(ROOT)).replace("\\", "/"),
        "bytes": int(E.VECTORS_PATH.stat().st_size),
    }
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
