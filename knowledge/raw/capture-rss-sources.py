import argparse
import html
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import requests

from manage_candidates import append_promoted, candidate_is_relevant, make_candidate


ROOT = Path(__file__).resolve().parents[2]
ITEMS_ROOT = ROOT / "knowledge" / "items"
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"
SOURCE_ARTICLE_INDEX_PATH = ROOT / "knowledge" / "catalog" / "source-article-index.md"
REGISTRY_PATH = ROOT / "knowledge" / "sources" / "source-registry.json"
RAW_CANDIDATES_DIR = ROOT / "knowledge" / "raw" / "source-candidates"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {
    "User-Agent": "aiagentstudy-rss-capture/1.0",
    "Accept": "application/atom+xml,application/rss+xml,application/xml,text/xml,text/html,*/*",
}

DEFAULT_KEYWORDS = [
    "ai",
    "agent",
    "agentic",
    "llm",
    "large language model",
    "model",
    "claude",
    "openai",
    "anthropic",
    "gemini",
    "rag",
    "retrieval",
    "inference",
    "training",
    "post-training",
    "benchmark",
    "eval",
    "tool",
    "browser",
    "computer use",
]

TOPIC_RULES = [
    (
        "04-evaluation-guardrails",
        ["benchmark", "eval", "evaluation", "safety", "alignment", "guardrail", "security", "reliability", "observability"],
        ["Evaluation", "Guardrails", "Model"],
    ),
    (
        "03-control-loop",
        ["agent", "agentic", "multi-agent", "orchestration", "workflow", "delegation", "harness", "planning", "langgraph"],
        ["Goal", "Context/State", "Control Loop", "Evaluation"],
    ),
    (
        "01-context-memory",
        ["context", "memory", "rag", "retrieval", "knowledge", "embedding", "long context"],
        ["Context/State", "Memory", "Tools/Actions"],
    ),
    (
        "02-tools-actions",
        ["tool", "api", "sdk", "browser", "computer use", "inference", "serving", "deployment", "gpu", "kv cache"],
        ["Tools/Actions", "Model", "Infrastructure"],
    ),
]


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_stack = []
        self.parts = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg", "nav", "footer", "header"}:
            self.skip_stack.append(tag)
        if tag == "title":
            self.in_title = True
        if tag in {"p", "div", "section", "article", "h1", "h2", "h3", "li", "br"} and not self.skip_stack:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.skip_stack and self.skip_stack[-1] == tag:
            self.skip_stack.pop()
        if tag == "title":
            self.in_title = False
        if tag in {"p", "div", "section", "article", "h1", "h2", "h3", "li"} and not self.skip_stack:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_stack:
            return
        text = html.unescape(data).strip()
        if not text:
            return
        if self.in_title:
            self.title = (self.title + " " + text).strip()
        self.parts.append(text)
        self.parts.append(" ")

    def text(self):
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def md_cell(text):
    return re.sub(r"\s+", " ", text or "").replace("|", "/").strip()


def clean_text(text):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_text(url, timeout=45):
    session = requests.Session()
    session.trust_env = False
    response = session.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def load_registry():
    registry = json.loads(read_text(REGISTRY_PATH))
    by_id = {}
    for group in registry.get("groups", []):
        for source in group.get("sources", []):
            row = dict(source)
            row["group_id"] = group.get("id", "")
            by_id[row["id"]] = row
    return by_id


def first_text(element, names):
    for name in names:
        if ":" in name:
            prefix, local = name.split(":", 1)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "content": "http://purl.org/rss/1.0/modules/content/",
                "dc": "http://purl.org/dc/elements/1.1/",
            }.get(prefix)
            found = element.find(f"{{{ns}}}{local}") if ns else None
        else:
            found = element.find(name)
        if found is not None and found.text:
            return found.text.strip()
    return ""


def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    root_tag = root.tag.lower()
    entries = []
    if "atom" in root_tag or root.tag.endswith("feed"):
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            links = []
            for link in entry.findall("atom:link", ns):
                href = link.attrib.get("href")
                if href:
                    links.append({"href": href, "rel": link.attrib.get("rel", ""), "type": link.attrib.get("type", "")})
            entries.append(
                {
                    "title": clean_text(first_text(entry, ["atom:title"])),
                    "summary": clean_text(first_text(entry, ["atom:summary", "atom:content"])),
                    "published": first_text(entry, ["atom:published", "atom:updated"]),
                    "updated": first_text(entry, ["atom:updated"]),
                    "id": first_text(entry, ["atom:id"]),
                    "authors": [clean_text(first_text(author, ["atom:name"])) for author in entry.findall("atom:author", ns)],
                    "links": links,
                }
            )
        return entries

    channel = root.find("channel")
    if channel is None:
        return entries
    for item in channel.findall("item"):
        link = first_text(item, ["link"])
        entries.append(
            {
                "title": clean_text(first_text(item, ["title"])),
                "summary": clean_text(first_text(item, ["description", "content:encoded"])),
                "published": first_text(item, ["pubDate", "dc:date"]),
                "updated": "",
                "id": first_text(item, ["guid"]) or link,
                "authors": [clean_text(first_text(item, ["dc:creator", "author"]))],
                "links": [{"href": link, "rel": "alternate", "type": "text/html"}] if link else [],
            }
        )
    return entries


def entry_url(entry):
    for link in entry.get("links", []):
        href = link.get("href", "")
        if href and (link.get("rel") in {"", "alternate"} or link.get("type", "").startswith("text/html")):
            return href
    for link in entry.get("links", []):
        if link.get("href"):
            return link["href"]
    return entry.get("id", "")


def normalize_url(url):
    try:
        parsed = urlparse(url or "")
    except ValueError:
        return ""
    return parsed._replace(fragment="", query="").geturl().rstrip("/")


def existing_urls():
    urls = set()
    for source_path in ITEMS_ROOT.glob("**/source.md"):
        text = read_text(source_path)
        for match in re.finditer(r"https?://[^\s)]+", text):
            normalized = normalize_url(match.group(0))
            if normalized:
                urls.add(normalized)
    return urls


def next_local_id(year):
    max_num = 0
    pattern = re.compile(rf"^RSS-{re.escape(str(year))}-(\d{{3}})$")
    for path in ITEMS_ROOT.glob(f"**/RSS-{year}-*"):
        match = pattern.match(path.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"RSS-{year}-{max_num + 1:03d}"


def classify(source, entry, page_text):
    haystack = f"{entry.get('title', '')} {entry.get('summary', '')} {page_text[:4000]}".lower()
    for topic, keywords, blocks in TOPIC_RULES:
        if any(keyword in haystack for keyword in keywords):
            return topic, blocks
    landing = source.get("landing_topics") or ["06-frontier-radar"]
    return landing[0], ["Model", "Frontier Radar", "Source Signal"]


def tags_for(source, entry, page_text):
    haystack = f"{entry.get('title', '')} {entry.get('summary', '')} {page_text[:4000]}".lower()
    tags = [source.get("name", source["id"]), "RSS"]
    for needle, tag in [
        ("agent", "AI Agent"),
        ("agentic", "Agentic AI"),
        ("llm", "LLM"),
        ("large language model", "LLM"),
        ("rag", "RAG"),
        ("retrieval", "Retrieval"),
        ("benchmark", "Benchmark"),
        ("eval", "Evaluation"),
        ("training", "Training"),
        ("inference", "Inference"),
        ("tool", "Tool Use"),
        ("browser", "Browser Automation"),
        ("safety", "Safety"),
    ]:
        if needle in haystack and tag not in tags:
            tags.append(tag)
    return tags[:8]


def is_relevant(entry, page_text, keywords):
    haystack = f"{entry.get('title', '')} {entry.get('summary', '')} {page_text[:5000]}".lower()
    return any(keyword.lower() in haystack for keyword in keywords)


def parse_date(value):
    if not value:
        return datetime.now().strftime("%Y-%m-%d")
    match = re.search(r"(20\d{2})[-/](\d{1,2})[-/](\d{1,2})", value)
    if match:
        return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
    match = re.search(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\s+(20\d{2})\b", value)
    if match:
        months = {m.lower(): i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
        month = months.get(match.group(2)[:3].lower())
        if month:
            return f"{match.group(3)}-{month:02d}-{int(match.group(1)):02d}"
    return datetime.now().strftime("%Y-%m-%d")


def extract_page(url):
    try:
        page_html = fetch_text(url, timeout=45)
    except Exception as exc:
        return {"html": "", "text": "", "title": "", "error": str(exc)}
    parser = TextExtractor()
    parser.feed(page_html)
    return {"html": page_html, "text": parser.text(), "title": clean_text(parser.title), "error": ""}


def write_item(source, entry, feed_url, page, collection_date):
    url = entry_url(entry)
    date = parse_date(entry.get("published") or entry.get("updated"))
    local_id = next_local_id(date[:4])
    topic, blocks = classify(source, entry, page.get("text", ""))
    item_dir = ITEMS_ROOT / topic / local_id
    raw_dir = item_dir / "raw"
    title = entry.get("title") or page.get("title") or url
    page_text = page.get("text", "")
    summary_text = entry.get("summary", "")
    article_body = page_text if len(page_text) > max(800, len(summary_text)) else summary_text
    tags = tags_for(source, entry, page_text)
    source_label = f"RSS / {source.get('name', source['id'])}"

    summary = f"""# {local_id} Summary

## Article

- Title: {title}
- Source: {source_label}
- URL: {url}
- Date: {date}
- Topic: `{topic}`
- Tags: {", ".join(tags)}

## Model Mapping

- Blocks: {", ".join(blocks)}
- Layer: multi-source RSS capture, pending deep reading

## Core Takeaway

This item was captured from `{source.get('id')}` because it matched the AI/agent source watchlist. The durable capture preserves feed metadata, source URL, article-page extraction when available, and raw evidence. Open `article.md` for the captured text and `source.md` for the feed/page evidence.

## Reusable Principle

Use RSS captures as source radar: they are good for catching official releases and engineering essays early, then promote only the most useful ones into deeper topic notes.
"""

    article = f"""# {title}

---

- Local ID: {local_id}
- Source: {source_label}
- Date: {date}
- URL: {url}
- Feed URL: {feed_url}
- Capture depth: feed metadata + article page extraction

---

## Feed Summary

{summary_text}

## Captured Article Text

{article_body}
"""

    source_doc = f"""# Source Evidence

- Title: {title}
- Source URL: {url}
- Original publisher URL: {url}
- Feed URL: {feed_url}
- Source ID: {source.get('id')}
- Source name: {source.get('name')}
- Published: {entry.get('published', '')}
- Updated: {entry.get('updated', '')}
- Collection date: {collection_date}

## Evidence Notes

- Discovery source: RSS/Atom feed from `knowledge/sources/source-registry.json`.
- Article page extraction error: {page.get('error', '')}
- Capture depth: feed metadata + article page extraction.
"""

    write_text(item_dir / "summary.md", summary)
    write_text(item_dir / "article.md", article)
    write_text(item_dir / "source.md", source_doc)
    write_text(raw_dir / "feed-entry.json", json.dumps(entry, ensure_ascii=False, indent=2) + "\n")
    write_text(raw_dir / "page.html", page.get("html", ""))
    write_text(raw_dir / "page-text.txt", page.get("text", ""))

    return {
        "id": local_id,
        "date": date,
        "title": title,
        "source": source_label,
        "topic": topic,
        "blocks": blocks,
        "status": "RSS metadata + article text captured",
        "url": url,
        "item_dir": str(item_dir.relative_to(ROOT)).replace("\\", "/"),
    }


def promoted_candidate_for_entry(source, entry, feed_url, collection_date, reason, promoted_id, topic_hint=""):
    url = entry_url(entry)
    title = entry.get("title") or url
    if not candidate_is_relevant(title, url):
        return None
    return make_candidate(
        title=title,
        url=url,
        source=source,
        route="rss",
        topic_hint=topic_hint or (source.get("landing_topics") or ["06-frontier-radar"])[0],
        reason=reason,
        evidence_path=f"knowledge/raw/source-candidates/rss feed {source.get('id')} {feed_url}",
        discovered_at=collection_date,
    ) | {"status": "captured", "promoted_id": promoted_id}


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


def ensure_source_article_index():
    if SOURCE_ARTICLE_INDEX_PATH.exists():
        return
    write_text(
        SOURCE_ARTICLE_INDEX_PATH,
        """# Source Article Index

Durable non-BestBlogs captures from official blogs, engineering blogs, newsletters, and community feeds.

Use this as a low-token entry point before opening individual `summary.md` files.

| ID | Date | Title | Source | Topic | Capture |
| --- | --- | --- | --- | --- | --- |
""",
    )


def append_source_article_index(rows):
    if not rows:
        return
    ensure_source_article_index()
    text = read_text(SOURCE_ARTICLE_INDEX_PATH)
    additions = [
        f"| {row['id']} | {md_cell(row['date'])} | {md_cell(row['title'])} | {md_cell(row['source'])} | `{row['topic']}` | RSS + article text |"
        for row in rows
    ]
    if not text.endswith("\n"):
        text += "\n"
    write_text(SOURCE_ARTICLE_INDEX_PATH, text + "\n".join(additions) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Capture RSS/Atom sources as durable knowledge items.")
    parser.add_argument("--ids", nargs="+", required=True, help="Source IDs in source-registry.json.")
    parser.add_argument("--limit", type=int, default=5, help="Max captures per run across all sources.")
    parser.add_argument("--per-source", type=int, default=5, help="Max entries to inspect per source.")
    parser.add_argument("--keywords", nargs="*", default=DEFAULT_KEYWORDS)
    parser.add_argument("--collection-date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--candidate-limit", type=int, default=20, help="Max promoted RSS records to append across this run.")
    parser.add_argument("--no-candidates", action="store_true", help="Do not append RSS captures to knowledge/candidates/promoted.jsonl.")
    args = parser.parse_args()

    sources = load_registry()
    seen = existing_urls()
    captured = []
    candidates = []
    skipped = []
    discovery_report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "rss-capture",
        "source_ids": args.ids,
        "discoveries": [],
    }

    for source_id in args.ids:
        source = sources.get(source_id)
        if not source:
            skipped.append({"source_id": source_id, "reason": "missing_source"})
            continue
        feed_url = source.get("rss")
        if not feed_url:
            skipped.append({"source_id": source_id, "reason": "missing_rss"})
            continue
        try:
            feed_text = fetch_text(feed_url, timeout=60)
            entries = parse_feed(feed_text)
            discovery_report["discoveries"].append({"source_id": source_id, "url": feed_url, "entries": entries[: args.per_source]})
        except Exception as exc:
            skipped.append({"source_id": source_id, "reason": "feed_error", "error": str(exc)})
            continue

        for entry in entries[: args.per_source]:
            url = entry_url(entry)
            normalized = normalize_url(url)
            if not url:
                skipped.append({"source_id": source_id, "title": entry.get("title", ""), "reason": "missing_url"})
                continue
            if normalized in seen:
                skipped.append({"source_id": source_id, "url": url, "title": entry.get("title", ""), "reason": "already_captured"})
                continue
            page = extract_page(url)
            if not is_relevant(entry, page.get("text", ""), args.keywords):
                skipped.append({"source_id": source_id, "url": url, "title": entry.get("title", ""), "reason": "not_relevant"})
                continue
            item_row = write_item(source, entry, feed_url, page, args.collection_date)
            captured.append(item_row)
            if not args.no_candidates and len(candidates) < args.candidate_limit:
                candidate = promoted_candidate_for_entry(source, entry, feed_url, args.collection_date, f"Captured as durable RSS item {item_row.get('id')}.", item_row.get("id"), item_row.get("topic"))
                if candidate:
                    candidates.append(candidate)
            seen.add(normalized)
            if len(captured) >= args.limit:
                break
            time.sleep(0.5)
        if len(captured) >= args.limit:
            break

    RAW_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_CANDIDATES_DIR / f"rss-capture-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    write_text(out_path, json.dumps(discovery_report, ensure_ascii=False, indent=2) + "\n")

    append_index(captured)
    append_source_article_index(captured)
    appended_candidates = append_promoted(candidates) if candidates else []
    print(json.dumps({"captured": captured, "skipped": skipped, "count": len(captured), "candidates": appended_candidates, "candidate_count": len(appended_candidates), "raw_report": str(out_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
