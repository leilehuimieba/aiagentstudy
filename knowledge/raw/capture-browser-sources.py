import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from manage_candidates import append_candidates, candidate_is_relevant, make_candidate


ROOT = Path(__file__).resolve().parents[2]
ITEMS_ROOT = ROOT / "knowledge" / "items"
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"
SOURCE_ARTICLE_INDEX_PATH = ROOT / "knowledge" / "catalog" / "source-article-index.md"
REGISTRY_PATH = ROOT / "knowledge" / "sources" / "source-registry.json"
RAW_CANDIDATES_DIR = ROOT / "knowledge" / "raw" / "source-candidates"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOPIC_RULES = [
    (
        "04-evaluation-guardrails",
        ["benchmark", "eval", "evaluation", "safety", "alignment", "guardrail", "security", "reliability", "risk"],
        ["Evaluation", "Guardrails", "Source Signal"],
    ),
    (
        "03-control-loop",
        ["agent", "agentic", "multi-agent", "workflow", "orchestration", "planning", "deep research", "computer use"],
        ["Goal", "Context/State", "Control Loop", "Source Signal"],
    ),
    (
        "01-context-memory",
        ["context", "memory", "rag", "retrieval", "knowledge", "long context"],
        ["Context/State", "Memory", "Source Signal"],
    ),
    (
        "02-tools-actions",
        ["tool", "api", "sdk", "browser", "github", "repo", "cli", "deployment", "inference"],
        ["Tools/Actions", "Infrastructure", "Source Signal"],
    ),
]

KEYWORDS = [
    "ai",
    "agent",
    "agentic",
    "llm",
    "large language model",
    "model",
    "openai",
    "anthropic",
    "claude",
    "gemini",
    "chatgpt",
    "codex",
    "rag",
    "retrieval",
    "inference",
    "training",
    "post-training",
    "benchmark",
    "eval",
    "tool",
    "browser",
    "智能体",
    "大模型",
    "模型",
    "论文",
    "评测",
]


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def md_cell(text):
    return re.sub(r"\s+", " ", text or "").replace("|", "/").strip()


def normalize_url(url):
    try:
        parsed = urlparse(url or "")
    except ValueError:
        return ""
    return parsed._replace(fragment="", query="").geturl().rstrip("/")


def comparable_host(url):
    try:
        host = urlparse(url or "").netloc.lower()
    except ValueError:
        return ""
    if host.startswith("www."):
        host = host[4:]
    return host


def final_url_matches_source(source, page_state):
    requested_host = comparable_host(source.get("url", ""))
    final_host = comparable_host((page_state or {}).get("url", ""))
    return bool(requested_host and final_host and requested_host == final_host)


def looks_like_security_challenge(page_state):
    text = ((page_state or {}).get("text") or "").lower()
    challenge_markers = [
        "performing security verification",
        "protect against malicious bots",
        "verifies you are not a bot",
        "performance and security by cloudflare",
        "ray id:",
    ]
    return any(marker in text for marker in challenge_markers)


def looks_like_error_page(page_state):
    text = ((page_state or {}).get("text") or "").lower()
    error_markers = [
        "404 we seem to have lost this page",
        "page not found",
        "the page you requested could not be found",
    ]
    return any(marker in text for marker in error_markers)


def extract_json_object(output):
    decoder = json.JSONDecoder()
    for i, ch in enumerate(output or ""):
        if ch in "[{":
            try:
                obj, _ = decoder.raw_decode(output[i:])
                return obj
            except json.JSONDecodeError:
                continue
    return None


def run_opencli(args, timeout=90):
    opencli_bin = shutil.which("opencli") or shutil.which("opencli.cmd") or "opencli.cmd"
    proc = subprocess.run(
        [opencli_bin, *args],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def load_sources():
    registry = json.loads(read_text(REGISTRY_PATH))
    by_id = {}
    for group in registry.get("groups", []):
        for source in group.get("sources", []):
            row = dict(source)
            row["group_id"] = group.get("id", "")
            row["group_name"] = group.get("name", "")
            by_id[row["id"]] = row
    return by_id


def existing_browser_snapshots(collection_date):
    seen = set()
    for source_path in ITEMS_ROOT.glob("**/BROWSER-*/source.md"):
        text = read_text(source_path)
        source_id = (re.search(r"^- Source ID: (.+)$", text, re.M) or ["", ""])[1].strip()
        date = (re.search(r"^- Collection date: (.+)$", text, re.M) or ["", ""])[1].strip()
        if source_id and date:
            seen.add((source_id, date))
    return seen


def next_local_id(year):
    max_num = 0
    pattern = re.compile(rf"^BROWSER-{re.escape(str(year))}-(\d{{3}})$")
    for path in ITEMS_ROOT.glob(f"**/BROWSER-{year}-*"):
        match = pattern.match(path.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"BROWSER-{year}-{max_num + 1:03d}"


def is_relevant(text, links):
    haystack = (text + " " + " ".join(link.get("text", "") for link in links)).lower()
    return any(keyword.lower() in haystack for keyword in KEYWORDS)


def classify(source, text):
    haystack = text.lower()
    for topic, keywords, blocks in TOPIC_RULES:
        if any(keyword in haystack for keyword in keywords):
            return topic, blocks
    landing = source.get("landing_topics") or ["06-frontier-radar"]
    return landing[0], ["Model", "Frontier Radar", "Source Signal"]


def tags_for(source, text):
    haystack = text.lower()
    tags = [source.get("name", source["id"]), "Browser Snapshot"]
    for needle, tag in [
        ("agent", "AI Agent"),
        ("agentic", "Agentic AI"),
        ("智能体", "AI Agent"),
        ("llm", "LLM"),
        ("大模型", "LLM"),
        ("benchmark", "Benchmark"),
        ("eval", "Evaluation"),
        ("评测", "Evaluation"),
        ("github", "GitHub"),
        ("trending", "Trending"),
        ("paper", "Paper"),
        ("论文", "Paper"),
        ("openai", "OpenAI"),
        ("hugging face", "Hugging Face"),
        ("机器之心", "Chinese AI"),
    ]:
        if needle in haystack and tag not in tags:
            tags.append(tag)
    return tags[:8]


def browser_page_state(profile, source):
    opened = run_opencli(["browser", profile, "tab", "new", source["url"]], timeout=90)
    page_info = extract_json_object(opened["stdout"]) if opened["returncode"] == 0 else None
    if opened["returncode"] != 0 or not page_info or not page_info.get("page"):
        return {
            "status": "open_failed",
            "open": opened,
            "page_info": page_info,
            "page_state": None,
        }

    tab_id = page_info["page"]
    run_opencli(["browser", profile, "tab", "select", tab_id], timeout=30)
    eval_js = (
        "(()=>{"
        "const text=(document.body&&document.body.innerText||'').replace(/\\s+/g,' ').trim();"
        "const links=[...document.querySelectorAll('a[href]')].map(a=>({"
        "text:(a.innerText||a.ariaLabel||'').replace(/\\s+/g,' ').trim().slice(0,160),"
        "href:a.href"
        "})).filter(x=>x.href).slice(0,80);"
        "return {url:location.href,title:document.title,readyState:document.readyState,textLength:text.length,text,links};"
        "})()"
    )
    eval_args = ["browser", profile, "eval", eval_js, "--tab", tab_id]
    evaluated = {"returncode": 1, "stdout": "", "stderr": "not run"}
    page_state = None
    for attempt in range(4):
        if attempt:
            time.sleep(2)
        evaluated = run_opencli(eval_args, timeout=120)
        page_state = extract_json_object(evaluated["stdout"]) if evaluated["returncode"] == 0 else None
        if page_state and page_state.get("url") != "about:blank" and page_state.get("textLength", 0) > 500:
            break

    return {
        "status": "browser_readable" if page_state and page_state.get("textLength", 0) > 500 else "low_text",
        "open": opened,
        "page_info": page_info,
        "eval": evaluated,
        "page_state": page_state,
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
        f"| {row['id']} | {md_cell(row['date'])} | {md_cell(row['title'])} | {md_cell(row['source'])} | `{row['topic']}` | Browser snapshot |"
        for row in rows
    ]
    if not text.endswith("\n"):
        text += "\n"
    write_text(SOURCE_ARTICLE_INDEX_PATH, text + "\n".join(additions) + "\n")


def write_item(source, profile, page_result, collection_date):
    page_state = page_result["page_state"]
    text = page_state.get("text", "")
    links = page_state.get("links", [])
    date = collection_date
    local_id = next_local_id(date[:4])
    source_label = f"Browser / {source.get('name', source['id'])}"
    title = f"{source.get('name', source['id'])} browser snapshot - {date}"
    topic, blocks = classify(source, text)
    tags = tags_for(source, text)
    item_dir = ITEMS_ROOT / topic / local_id
    raw_dir = item_dir / "raw"

    link_lines = "\n".join(
        f"- [{link.get('text') or link.get('href')}]({link.get('href')})"
        for link in links[:40]
    )

    summary = f"""# {local_id} Summary

## Article

- Title: {title}
- Source: {source_label}
- URL: {page_state.get('url')}
- Date: {date}
- Topic: `{topic}`
- Tags: {", ".join(tags)}

## Model Mapping

- Blocks: {", ".join(blocks)}
- Layer: browser source radar snapshot

## Core Takeaway

This is a browser-rendered source snapshot captured through OpenCLI Browser Bridge profile `{profile}`. It preserves the visible text and key links from `{source.get('id')}` so the knowledge base can track dynamic sources that are not reliably exposed through RSS/API. Use it as a candidate source for later single-article deep capture.

## Reusable Principle

Use browser snapshots for discovery, not final truth. Promote individual linked articles or papers to durable deep notes only after checking source quality and relevance.
"""

    article = f"""# {title}

---

- Local ID: {local_id}
- Source: {source_label}
- Source ID: {source.get('id')}
- URL: {page_state.get('url')}
- Original requested URL: {source.get('url')}
- Collection date: {date}
- Capture depth: browser-rendered page snapshot

---

## Page Text

{text}

## Candidate Links

{link_lines}
"""

    source_doc = f"""# Source Evidence

- Title: {title}
- Source URL: {page_state.get('url')}
- Original publisher URL: {page_state.get('url')}
- Requested URL: {source.get('url')}
- Source ID: {source.get('id')}
- Source name: {source.get('name')}
- OpenCLI profile: {profile}
- Collection date: {date}
- Browser status: {page_result.get('status')}
- Text length: {page_state.get('textLength')}

## Evidence Notes

- Discovery source: OpenCLI Browser Bridge via `knowledge/sources/source-registry.json`.
- This is a source snapshot, not a claim that every linked item has been deeply read.
- Raw page state and full extracted text are stored under `raw/`.
"""

    write_text(item_dir / "summary.md", summary)
    write_text(item_dir / "article.md", article)
    write_text(item_dir / "source.md", source_doc)
    write_text(raw_dir / "page-state.json", json.dumps(page_state, ensure_ascii=False, indent=2) + "\n")
    write_text(raw_dir / "page-text.txt", text)
    write_text(raw_dir / "opencli-result.json", json.dumps(page_result, ensure_ascii=False, indent=2) + "\n")

    return {
        "id": local_id,
        "date": date,
        "title": title,
        "source": source_label,
        "topic": topic,
        "blocks": blocks,
        "status": "Browser snapshot captured",
        "url": page_state.get("url"),
        "item_dir": str(item_dir.relative_to(ROOT)).replace("\\", "/"),
    }


def candidate_links_for_snapshot(source, item_row, page_state, limit):
    candidates = []
    topic_hint = item_row.get("topic", "")
    evidence_path = f"{item_row.get('item_dir', '')}/raw/page-state.json"
    page_url = normalize_url(page_state.get("url", ""))
    seen = {page_url}
    for link in page_state.get("links", []):
        href = normalize_url(link.get("href", ""))
        title = link.get("text") or href
        if not href or href in seen:
            continue
        seen.add(href)
        if not candidate_is_relevant(title, href):
            continue
        candidates.append(
            make_candidate(
                title=title,
                url=href,
                source=source,
                route="browser",
                topic_hint=topic_hint,
                reason=f"Discovered in browser snapshot {item_row.get('id')} from {source.get('id')}.",
                evidence_path=evidence_path,
                discovered_at=item_row.get("date"),
            )
        )
        if len(candidates) >= limit:
            break
    return candidates


def main():
    parser = argparse.ArgumentParser(description="Capture browser-rendered source snapshots through OpenCLI Browser Bridge.")
    parser.add_argument("--ids", nargs="+", required=True, help="Source IDs in knowledge/sources/source-registry.json.")
    parser.add_argument("--profile", default="qmvqcrb8")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--collection-date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--force", action="store_true", help="Allow recapturing the same source on the same collection date.")
    parser.add_argument("--candidate-limit", type=int, default=20, help="Max candidate links to emit per captured source snapshot.")
    parser.add_argument("--no-candidates", action="store_true", help="Do not append discovered links to knowledge/candidates/inbox.jsonl.")
    args = parser.parse_args()

    sources = load_sources()
    seen = existing_browser_snapshots(args.collection_date)
    captured = []
    candidates = []
    skipped = []
    raw_report = {"generated_at": datetime.now().isoformat(timespec="seconds"), "mode": "browser-snapshot", "results": []}

    for source_id in args.ids:
        if len(captured) >= args.limit:
            break
        source = sources.get(source_id)
        if not source:
            skipped.append({"source_id": source_id, "reason": "missing_source"})
            continue
        if not args.force and (source_id, args.collection_date) in seen:
            skipped.append({"source_id": source_id, "reason": "already_captured_today"})
            continue
        page_result = browser_page_state(args.profile, source)
        raw_report["results"].append({"source_id": source_id, "result": page_result})
        page_state = page_result.get("page_state") or {}
        links = page_state.get("links") or []
        if page_result.get("status") != "browser_readable":
            skipped.append({"source_id": source_id, "reason": page_result.get("status"), "url": page_state.get("url")})
            continue
        if not final_url_matches_source(source, page_state):
            skipped.append(
                {
                    "source_id": source_id,
                    "reason": "final_url_host_mismatch",
                    "requested_url": source.get("url"),
                    "url": page_state.get("url"),
                }
            )
            continue
        if looks_like_security_challenge(page_state):
            skipped.append({"source_id": source_id, "reason": "security_challenge_page", "url": page_state.get("url")})
            continue
        if looks_like_error_page(page_state):
            skipped.append({"source_id": source_id, "reason": "error_page", "url": page_state.get("url")})
            continue
        if not is_relevant(page_state.get("text", ""), links):
            skipped.append({"source_id": source_id, "reason": "not_relevant", "url": page_state.get("url")})
            continue
        item_row = write_item(source, args.profile, page_result, args.collection_date)
        captured.append(item_row)
        if not args.no_candidates and args.candidate_limit > 0:
            candidates.extend(candidate_links_for_snapshot(source, item_row, page_state, args.candidate_limit))
        seen.add((source_id, args.collection_date))

    RAW_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_CANDIDATES_DIR / f"browser-snapshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    write_text(out_path, json.dumps(raw_report, ensure_ascii=False, indent=2) + "\n")

    append_index(captured)
    append_source_article_index(captured)
    appended_candidates = append_candidates(candidates) if candidates else []
    print(json.dumps({"captured": captured, "skipped": skipped, "count": len(captured), "candidates": appended_candidates, "candidate_count": len(appended_candidates), "raw_report": str(out_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
