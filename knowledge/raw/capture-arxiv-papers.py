import argparse
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[2]
ITEMS_ROOT = ROOT / "knowledge" / "items"
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"
PAPER_INDEX_PATH = ROOT / "knowledge" / "catalog" / "paper-index.md"
RAW_CANDIDATES_DIR = ROOT / "knowledge" / "raw" / "source-candidates"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {
    "User-Agent": "aiagentstudy-arxiv-capture/1.0",
    "Accept": "application/atom+xml,application/xml,text/xml,*/*",
}

TOPIC_RULES = [
    (
        "04-evaluation-guardrails",
        ["benchmark", "bench", "eval", "evaluation", "safety", "alignment", "rlhf", "guardrail", "robust"],
        ["Evaluation", "Guardrails", "Model"],
    ),
    (
        "03-control-loop",
        ["agent", "agentic", "multi-agent", "subagent", "delegation", "tool use", "computer use", "web agent", "harness", "planning"],
        ["Goal", "Context/State", "Control Loop", "Evaluation"],
    ),
    (
        "01-context-memory",
        ["context", "retrieval", "rag", "memory", "long-form", "long context"],
        ["Context/State", "Memory", "Control Loop"],
    ),
    (
        "06-frontier-radar",
        ["reinforcement learning", "post-training", "policy optimization", "pretraining", "training efficiency"],
        ["Model", "Training", "Optimization"],
    ),
    (
        "02-tools-actions",
        ["serving", "inference", "quantization", "kv cache", "speculative decoding", "fine-tune", "fine-tuning", "lora"],
        ["Model", "Tools/Actions", "Infrastructure"],
    ),
]


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def md_cell(text):
    return re.sub(r"\s+", " ", text or "").replace("|", "/").strip()


def normalize_space(text):
    return re.sub(r"\s+", " ", text or "").strip()


def arxiv_id_from_url(url):
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#\s]+)", url or "", re.I)
    if not match:
        return ""
    return match.group(1).removesuffix(".pdf")


def canonical_arxiv_id(entry):
    raw_id = arxiv_id_from_url(entry.get("id", ""))
    if raw_id:
        return raw_id
    for link in entry.get("links", []):
        raw_id = arxiv_id_from_url(link.get("href", ""))
        if raw_id:
            return raw_id
    return ""


def abs_url(arxiv_id):
    return f"https://arxiv.org/abs/{arxiv_id}"


def pdf_url(arxiv_id):
    return f"https://arxiv.org/pdf/{arxiv_id}"


def fetch_text(url, timeout=90):
    session = requests.Session()
    session.trust_env = False
    response = session.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def atom_text(element, name):
    found = element.find(f"{{http://www.w3.org/2005/Atom}}{name}")
    return found.text.strip() if found is not None and found.text else ""


def parse_atom_entries(xml_text):
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    entries = []
    for entry in root.findall("atom:entry", ns):
        links = []
        for link in entry.findall("atom:link", ns):
            href = link.attrib.get("href")
            if href:
                links.append({"href": href, "rel": link.attrib.get("rel", ""), "type": link.attrib.get("type", "")})
        categories = [cat.attrib.get("term", "") for cat in entry.findall("atom:category", ns) if cat.attrib.get("term")]
        doi = atom_text(entry, "doi")
        entries.append(
            {
                "title": normalize_space(atom_text(entry, "title")),
                "summary": normalize_space(atom_text(entry, "summary")),
                "published": atom_text(entry, "published"),
                "updated": atom_text(entry, "updated"),
                "id": atom_text(entry, "id"),
                "authors": [atom_text(author, "name") for author in entry.findall("atom:author", ns)],
                "categories": categories,
                "doi": doi,
                "links": links,
            }
        )
    return entries


def discover_arxiv(query, max_results):
    encoded = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": "0",
            "max_results": str(max_results),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"https://export.arxiv.org/api/query?{encoded}"
    return {
        "source_id": "arxiv",
        "url": url,
        "query": query,
        "entries": parse_atom_entries(fetch_text(url)),
    }


def latest_candidate_file():
    files = sorted(RAW_CANDIDATES_DIR.glob("source-candidates-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def load_entries_from_candidate_file(path):
    data = json.loads(read_text(path))
    for discovery in data.get("discoveries", []):
        if discovery.get("source_id") == "arxiv":
            return discovery.get("entries", []), discovery
    return [], {"source_id": "arxiv", "url": "", "query": ""}


def existing_arxiv_ids():
    ids = set()
    if not ITEMS_ROOT.exists():
        return ids
    for source_path in ITEMS_ROOT.glob("*/ARXIV-*/source.md"):
        text = read_text(source_path)
        for match in re.finditer(r"arxiv\.org/(?:abs|pdf)/([^)\s]+)", text):
            ids.add(match.group(1).removesuffix(".pdf"))
    return ids


def next_local_id(year):
    max_num = 0
    pattern = re.compile(rf"^ARXIV-{re.escape(str(year))}-(\d{{3}})$")
    for path in ITEMS_ROOT.glob(f"*/ARXIV-{year}-*"):
        match = pattern.match(path.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"ARXIV-{year}-{max_num + 1:03d}"


def classify(entry):
    haystack = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
    for topic, keywords, blocks in TOPIC_RULES:
        if any(keyword in haystack for keyword in keywords):
            return topic, blocks
    return "06-frontier-radar", ["Model", "Frontier Radar", "Research"]


def tags_for(entry):
    haystack = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
    tags = ["arXiv", "AI Research"]
    keyword_tags = [
        ("agent", "AI Agent"),
        ("agentic", "Agentic AI"),
        ("benchmark", "Benchmark"),
        ("evaluation", "Evaluation"),
        ("rlhf", "RLHF"),
        ("reinforcement learning", "RL"),
        ("post-training", "Post-training"),
        ("tool", "Tool Use"),
        ("context", "Context Engineering"),
        ("retrieval", "Retrieval"),
        ("inference", "Inference"),
        ("quantization", "Quantization"),
        ("large language model", "LLM"),
        ("llm", "LLM"),
    ]
    for needle, tag in keyword_tags:
        if needle in haystack and tag not in tags:
            tags.append(tag)
    return tags[:8]


def why_relevant(entry):
    text = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
    signals = []
    for needle, label in [
        ("agent", "agent / agentic workflow"),
        ("delegation", "delegation intelligence"),
        ("harness", "harness-guided behavior"),
        ("benchmark", "benchmark / evaluation"),
        ("rlhf", "alignment / RLHF"),
        ("post-training", "post-training"),
        ("inference", "inference optimization"),
        ("tool", "tool use"),
        ("context", "context limits"),
    ]:
        if needle in text:
            signals.append(label)
    return ", ".join(signals[:4]) or "frontier AI research signal"


def published_date(entry):
    value = entry.get("published") or entry.get("updated") or datetime.now().isoformat()
    return value[:10]


def write_item(entry, discovery, collection_date):
    arxiv_id = canonical_arxiv_id(entry)
    year = published_date(entry)[:4]
    local_id = next_local_id(year)
    topic, blocks = classify(entry)
    item_dir = ITEMS_ROOT / topic / local_id
    raw_dir = item_dir / "raw"
    title = entry.get("title") or arxiv_id
    date = published_date(entry)
    authors = entry.get("authors", [])
    tags = tags_for(entry)
    abstract = entry.get("summary", "")
    categories = entry.get("categories", [])
    arxiv_abs = abs_url(arxiv_id)
    arxiv_pdf = pdf_url(arxiv_id)
    relevance = why_relevant(entry)

    summary = f"""# {local_id} Summary

## Article

- Title: {title}
- Source: arXiv
- URL: {arxiv_abs}
- Date: {date}
- Topic: `{topic}`
- Tags: {", ".join(tags)}

## Model Mapping

- Blocks: {", ".join(blocks)}
- Layer: paper radar capture, pending deep reading

## Core Takeaway

This arXiv paper is captured as a research radar item because it matches: {relevance}. The current durable capture preserves metadata, abstract, authors, arXiv URL, PDF URL, and raw API evidence. Open `article.md` for the abstract and source metadata; open the PDF only when a full technical read is needed.

## Reusable Principle

Use paper captures as early signals first. Promote a paper from abstract-level radar to deep notes only when it changes the agent mental model, introduces an implementable method, or becomes a benchmark/evaluation source.
"""

    article = f"""# {title}

---

- Local ID: {local_id}
- Source: arXiv
- arXiv ID: {arxiv_id}
- Date: {date}
- Authors: {", ".join(authors)}
- Categories: {", ".join(categories)}
- URL: {arxiv_abs}
- PDF: {arxiv_pdf}
- Capture depth: metadata + abstract

---

## Abstract

{abstract}

## Capture Notes

This is an abstract-level paper capture from the arXiv API. The PDF URL is preserved for full-text reading and later deep extraction.
"""

    source = f"""# Source Evidence

- Title: {title}
- Source URL: {arxiv_abs}
- Original publisher URL: {arxiv_abs}
- PDF URL: {arxiv_pdf}
- arXiv ID: {arxiv_id}
- DOI: {entry.get("doi", "")}
- Authors: {", ".join(authors)}
- Categories: {", ".join(categories)}
- Published: {entry.get("published", "")}
- Updated: {entry.get("updated", "")}
- Collection date: {collection_date}

## Evidence Notes

- Discovery source: arXiv API query `{discovery.get("query", "")}`.
- API URL: {discovery.get("url", "")}
- Capture depth: metadata + abstract. Full PDF text is not extracted yet.
"""

    write_text(item_dir / "summary.md", summary)
    write_text(item_dir / "article.md", article)
    write_text(item_dir / "source.md", source)
    write_text(raw_dir / "arxiv-entry.json", json.dumps(entry, ensure_ascii=False, indent=2) + "\n")
    write_text(raw_dir / "discovery.json", json.dumps(discovery, ensure_ascii=False, indent=2) + "\n")

    return {
        "id": local_id,
        "date": date,
        "title": title,
        "source": "arXiv",
        "topic": topic,
        "blocks": blocks,
        "status": "Paper metadata + abstract captured",
        "arxiv_id": arxiv_id,
        "url": arxiv_abs,
        "pdf": arxiv_pdf,
        "item_dir": str(item_dir.relative_to(ROOT)).replace("\\", "/"),
    }


def append_index(rows):
    if not rows:
        return
    index = read_text(INDEX_PATH)
    additions = [
        f"| {row['id']} | {md_cell(row['date'])} | {md_cell(row['title'])} | {md_cell(row['source'])} | `{row['topic']}` | {md_cell(', '.join(row['blocks']))} | {md_cell(row['status'])} |"
        for row in rows
    ]
    if not index.endswith("\n"):
        index += "\n"
    write_text(INDEX_PATH, index + "\n".join(additions) + "\n")


def ensure_paper_index():
    if PAPER_INDEX_PATH.exists():
        return
    write_text(
        PAPER_INDEX_PATH,
        """# AI Paper Index

Durable paper captures from arXiv, OpenReview, Hugging Face Papers, ACL Anthology, Semantic Scholar, and conference proceedings.

Use this as the low-token paper entry point before opening individual `summary.md` files.

| ID | Date | Title | Source | Topic | Capture |
| --- | --- | --- | --- | --- | --- |
""",
    )


def append_paper_index(rows):
    if not rows:
        return
    ensure_paper_index()
    text = read_text(PAPER_INDEX_PATH)
    additions = [
        f"| {row['id']} | {md_cell(row['date'])} | {md_cell(row['title'])} | arXiv | `{row['topic']}` | metadata + abstract |"
        for row in rows
    ]
    if not text.endswith("\n"):
        text += "\n"
    write_text(PAPER_INDEX_PATH, text + "\n".join(additions) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Capture arXiv papers as durable knowledge items.")
    parser.add_argument("--query", default='all:"AI agent" OR all:"large language model" OR all:"tool use"')
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-file", help="Use an existing source-candidates JSON file instead of querying arXiv.")
    parser.add_argument("--latest-candidates", action="store_true", help="Use the newest knowledge/raw/source-candidates JSON file.")
    parser.add_argument("--collection-date", default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    if args.candidate_file or args.latest_candidates:
        candidate_path = Path(args.candidate_file) if args.candidate_file else latest_candidate_file()
        if not candidate_path:
            raise SystemExit("No source candidate file found.")
        if not candidate_path.is_absolute():
            candidate_path = ROOT / candidate_path
        entries, discovery = load_entries_from_candidate_file(candidate_path)
    else:
        discovery = discover_arxiv(args.query, args.max_results)
        entries = discovery.get("entries", [])
        RAW_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_CANDIDATES_DIR / f"arxiv-capture-query-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        write_text(out_path, json.dumps({"generated_at": datetime.now().isoformat(timespec="seconds"), "discoveries": [discovery]}, ensure_ascii=False, indent=2) + "\n")

    seen = existing_arxiv_ids()
    captured = []
    skipped = []
    for entry in entries:
        arxiv_id = canonical_arxiv_id(entry)
        if not arxiv_id:
            skipped.append({"title": entry.get("title", ""), "reason": "missing_arxiv_id"})
            continue
        if arxiv_id in seen:
            skipped.append({"arxiv_id": arxiv_id, "title": entry.get("title", ""), "reason": "already_captured"})
            continue
        captured.append(write_item(entry, discovery, args.collection_date))
        seen.add(arxiv_id)
        if len(captured) >= args.limit:
            break
        time.sleep(0.2)

    append_index(captured)
    append_paper_index(captured)

    print(json.dumps({"captured": captured, "skipped": skipped, "count": len(captured)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
