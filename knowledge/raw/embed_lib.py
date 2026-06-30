"""Shared helpers for the dense (semantic) retrieval channel.

The knowledge base is Chinese+English, so we use a small multilingual model
(intfloat/multilingual-e5-small, 384-dim). e5 models expect role prefixes:
"query: ..." for queries and "passage: ..." for indexed documents.

Vectors are stored as a single L2-normalized float32 matrix in embeddings.npy,
row-aligned to the chunk rowids listed in embeddings-meta.json. Cosine similarity
is therefore a plain dot product. With ~9k chunks this brute-force search is
sub-10ms in numpy, so no vector database is needed.

The model + sentence-transformers live in knowledge/retrieval/.venv; this module
is only importable from that interpreter. query-kb.py imports it lazily and falls
back to pure BM25 when the import or the index files are missing.
"""

import json
import os
from pathlib import Path

import numpy as np

# The model is downloaded once (see build-kb-embeddings.py) and cached under
# ~/.cache/huggingface. At query time we never want a network round-trip — it
# would add latency and fail on offline/blocked networks. Force offline + quiet.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

ROOT = Path(__file__).resolve().parents[2]
RETRIEVAL_DIR = ROOT / "knowledge" / "retrieval"
VECTORS_PATH = RETRIEVAL_DIR / "embeddings.npy"
META_PATH = RETRIEVAL_DIR / "embeddings-meta.json"

# BAAI/bge-m3: SOTA open multilingual (esp. Chinese<->English) retrieval model.
# Unlike e5, bge-m3 takes raw text with no role prefixes for retrieval.
MODEL_NAME = "BAAI/bge-m3"
EMBED_DIM = 1024
QUERY_PREFIX = ""
PASSAGE_PREFIX = ""
# bge-m3 defaults to an 8192-token window. Our chunks are ~1400 chars and CJK is
# ~1 token/char, so the default makes CPU embedding ~3x slower for no recall gain.
# Cap at 512: captures each chunk's retrieval signal at a fraction of the cost.
MAX_SEQ_LENGTH = 512

# Weights are vendored locally (knowledge/retrieval/models/bge-m3) so loading is
# fully offline and never depends on the HF cache or a reachable hub. Falls back
# to the hub id when the local copy is absent.
LOCAL_MODEL_DIR = RETRIEVAL_DIR / "models" / "bge-m3"


def model_ref():
    if (LOCAL_MODEL_DIR / "config.json").exists():
        return str(LOCAL_MODEL_DIR)
    return MODEL_NAME

_MODEL = None


def get_model():
    """Load the embedding model once per process (cold start ~1-3s)."""
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer

        _MODEL = SentenceTransformer(model_ref())
        try:
            _MODEL.max_seq_length = MAX_SEQ_LENGTH
        except Exception:
            pass
    return _MODEL


def _encode(texts, prefix, batch_size=32, progress_every=0):
    model = get_model()
    prefixed = [prefix + (t or "") for t in texts]
    if not progress_every:
        vectors = model.encode(
            prefixed,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.asarray(vectors, dtype=np.float32)

    # Manual batching with progress so long CPU builds are observable.
    import sys
    import time

    out = []
    total = len(prefixed)
    start = time.monotonic()
    for i in range(0, total, batch_size):
        batch = prefixed[i : i + batch_size]
        vecs = model.encode(
            batch, batch_size=batch_size, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False
        )
        out.append(np.asarray(vecs, dtype=np.float32))
        done = min(i + batch_size, total)
        if done % progress_every < batch_size or done == total:
            rate = done / max(time.monotonic() - start, 1e-6)
            eta = (total - done) / max(rate, 1e-6)
            print(f"  embedded {done}/{total}  ({rate:.1f}/s, ETA {eta:.0f}s)", file=sys.stderr, flush=True)
    return np.concatenate(out, axis=0)


def encode_passages(texts, batch_size=32, progress_every=512):
    return _encode(texts, PASSAGE_PREFIX, batch_size, progress_every=progress_every)


def encode_query_local(text):
    """Encode a query in THIS process, loading the model if needed (cold ~9s)."""
    return _encode([text], QUERY_PREFIX, batch_size=1)[0]


def encode_query(text):
    """Encode a query, preferring the resident daemon for a warm <1s round-trip.

    Falls back to in-process encoding when the daemon is unavailable or disabled
    (KB_NO_DAEMON), so the dense channel never breaks. The daemon server calls
    encode_query_local() directly to avoid recursing back through here.
    """
    try:
        import embed_daemon

        vec = embed_daemon.client_encode(text)
        if vec is not None:
            return vec
    except Exception:
        pass
    return encode_query_local(text)


def index_exists():
    return VECTORS_PATH.exists() and META_PATH.exists()


def load_index():
    """Return (vectors[N,dim] float32, meta dict) or (None, None) if missing."""
    if not index_exists():
        return None, None
    vectors = np.load(VECTORS_PATH)
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    return vectors, meta
