import argparse
import html
import json
import re
import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlsplit, urlunsplit

import requests
from requests.exceptions import RequestException

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "knowledge" / "catalog" / "articles-index.md"
MEMORY = ROOT / "AI_AGENT_MEMORY.md"
REPORT_DIR = ROOT / "knowledge" / "raw"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json,text/plain,*/*",
    "Connection": "close",
}

TOPIC_RULES = [
    (re.compile(r"context|memory|rag|retrieval|embedding|search|knowledge", re.I), ("01-context-memory", "Context/State, Memory, Tools/Actions")),
    (re.compile(r"tool|browser|mcp|api|codex|cursor|claude code|copilot|github|workflow|cli|skill", re.I), ("02-tools-actions", "Tools/Actions, Control Loop, Deliverable")),
    (re.compile(r"agent|orchestrat|harness|planning|multi-agent|react|loop", re.I), ("03-control-loop", "Goal, Context/State, Control Loop, Evaluation")),
    (re.compile(r"eval|benchmark|guardrail|security|privacy|safety|risk|observability|gdpr|trust", re.I), ("04-evaluation-guardrails", "Evaluation, Guardrails, Tools/Actions")),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_bestblogs(url: str) -> str:
    return str(url or "").replace("https://www.bestblogs.dev/en/", "https://www.bestblogs.dev/").split("?", 1)[0].split("#", 1)[0]


def normalize_original(url: str) -> str:
    if not url or url == "Not found":
        return str(url or "")
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def existing_sources():
    urls = set()
    originals = set()
    titles = set()
    for p in (ROOT / "knowledge" / "items").rglob("source.md"):
        txt = p.read_text(encoding="utf-8-sig", errors="ignore")
        m = re.search(r"^- BestBlogs URL:\s*(https://www\.bestblogs\.dev/(?:en/)?(?:article|video|podcast|status|explore/topics)/\S+)\s*$", txt, re.M)
        if m:
            urls.add(normalize_bestblogs(m.group(1)))
        m = re.search(r"^- Original publisher URL:\s*(.+?)\s*$", txt, re.M)
        if m:
            originals.add(normalize_original(m.group(1).strip()))
        m = re.search(r"^- Title:\s*(.+?)\s*$", txt, re.M)
        if m:
            titles.add(m.group(1).strip())
    return urls, originals, titles


def next_id_base() -> int:
    nums = [int(x) for x in re.findall(r"BB-2026-05-01-(\d{3})", read_text(INDEX))]
    return (max(nums) if nums else 0) + 1


def md_cell(text: str) -> str:
    return str(text or "").replace("|", "/").replace("\r", " ").replace("\n", " ").strip()


def stable_date(value: str, discovery_date: str) -> str:
    value = str(value or "").strip()
    try:
        base = datetime.strptime(discovery_date, "%Y-%m-%d").date()
    except ValueError:
        base = None
    if base and value.lower() == "today":
        return base.strftime("%m-%d")
    if base and value.lower() == "yesterday":
        return (base - timedelta(days=1)).strftime("%m-%d")
    return value


def strip_html(doc: str) -> str:
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "\n", doc or "")
    text = re.sub(r"(?i)</(p|div|section|article|h1|h2|h3|h4|h5|h6|li|ul|ol|blockquote|pre|table|tr)>", "\n", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\xa0", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def fetch_json(session: requests.Session, url: str, referer: str, retries: int = 5):
    headers = dict(HEADERS)
    headers["Referer"] = referer
    last = None
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, headers=headers, timeout=90)
            r.raise_for_status()
            return r.json(), r.content
        except RequestException as e:
            last = e
            time.sleep(min(2 * attempt, 10))
    raise last


def extract_json_object(output: str):
    decoder = json.JSONDecoder()
    for i, ch in enumerate(output):
        if ch in "[{":
            try:
                obj, _ = decoder.raw_decode(output[i:])
                return obj
            except json.JSONDecodeError:
                continue
    raise ValueError("No JSON object found in opencli output")


def opencli_fetch_list(profile: str, page: int, page_size: int):
    js = (
        "(()=>{"
        f"const q=new URLSearchParams({{page:'{page}',pageSize:'{page_size}',timeFilter:'1w',language:'all',sortType:'latest',type:'ARTICLE',qualifiedFilter:'false',uiLang:'en'}});"
        "return fetch('/api/proxy/resources?'+q.toString(),{credentials:'include'}).then(r=>r.json())"
        "})()"
    )
    opencli_bin = shutil.which("opencli") or shutil.which("opencli.cmd") or "opencli.cmd"
    proc = subprocess.run(
        [opencli_bin, "browser", profile, "eval", js],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or "").strip() or (proc.stdout or "").strip())
    return extract_json_object(proc.stdout)


def classify(title: str, summary: str):
    text = f"{title}\n{summary}"
    for pattern, result in TOPIC_RULES:
        if pattern.search(text):
            return result
    return "06-frontier-radar", "Model, Frontier Radar, Product Workflow"


def append_memory(lines):
    old = read_text(MEMORY).rstrip() + "\n"
    write_text(MEMORY, old + "".join(f"- {line}\n" for line in lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="qmvqcrb8")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--discovery-date", default="2026-06-08")
    args = parser.parse_args()

    raw = opencli_fetch_list(args.profile, args.page, args.page_size)
    list_path = REPORT_DIR / f"current-opencli-latest-page{args.page}-{args.discovery_date.replace('-', '')}.json"
    write_text(list_path, json.dumps(raw, ensure_ascii=False, indent=2) + "\n")

    entries = raw["data"]["dataList"]
    seen_urls, seen_originals, seen_titles = existing_sources()
    start = next_id_base()
    session = requests.Session()
    session.trust_env = False

    results = []
    errors = []
    skipped = []
    index_append = []
    memory_notes = []

    for item in entries:
        read_url = item["readUrl"]
        norm = normalize_bestblogs(read_url)
        if norm in seen_urls:
            skipped.append({"readUrl": read_url, "reason": "bestblogs_url_exists"})
            continue

        slug = norm.rsplit("/", 1)[-1]
        bbid = f"BB-2026-05-01-{start + len(results):03d}"
        referer = read_url.replace("https://www.bestblogs.dev/article/", "https://www.bestblogs.dev/en/article/")

        try:
            page_json, page_bytes = fetch_json(session, f"https://www.bestblogs.dev/api/proxy/resources/{slug}/page?language=en", referer)
            time.sleep(1)
            content_json, content_bytes = fetch_json(session, f"https://www.bestblogs.dev/api/proxy/resources/{slug}/content?language=en", referer)
        except Exception as e:
            errors.append({"planned_id": bbid, "slug": slug, "readUrl": read_url, "error": str(e)})
            continue

        md = page_json["data"]["metaData"]
        content_data = content_json["data"]["contentData"]
        plain = strip_html(content_data.get("displayDocument") or "")
        title = md.get("title") or item.get("title") or slug
        original_url = md.get("url") or "Not found"
        original_norm = normalize_original(original_url)
        if title in seen_titles or (original_norm and original_norm in seen_originals):
            skipped.append({"readUrl": read_url, "title": title, "original_url": original_url, "reason": "title_or_original_exists"})
            continue

        topic, blocks = classify(title, md.get("summary") or md.get("oneSentenceSummary") or "")
        source = f"BestBlogs / {md.get('sourceName') or item.get('sourceName') or 'Unknown source'}"
        date = stable_date(md.get("publishDateStr") or item.get("publishDateStr") or md.get("publishDateTimeStr", "")[:10], args.discovery_date)
        published_full = md.get("publishDateTimeStr") or ""
        tags = md.get("tags") or []

        item_dir = ROOT / "knowledge" / "items" / topic / bbid
        raw_dir = item_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "page.json").write_bytes(page_bytes)
        (raw_dir / "content.json").write_bytes(content_bytes)
        write_text(raw_dir / "discovery.json", json.dumps(item, ensure_ascii=False, indent=2) + "\n")

        write_text(item_dir / "article.md", (
            f"# {title}\n\n"
            f"- BestBlogs URL: {read_url}\n"
            f"- Original publisher URL: {original_url}\n"
            f"- Source: {source}\n"
            f"- Publish time: {published_full}\n"
            f"- Capture route: article discovered from OpenCLI Browser Bridge profile `{args.profile}` latest article feed page {args.page}; page/content captured from BestBlogs resource APIs\n"
            f"- Extracted chars: {len(plain)}\n\n"
            f"---\n\n{plain}"
        ))
        write_text(item_dir / "source.md", (
            f"# Source Evidence\n\n"
            f"- Title: {md_cell(title)}\n"
            f"- BestBlogs URL: {read_url}\n"
            f"- Original publisher URL: {original_url}\n"
            f"- BestBlogs source label: {md.get('sourceName') or item.get('sourceName') or ''}\n"
            f"- Publish time: {published_full}\n"
            f"- Language: {md.get('languageDesc') or md.get('language') or ''}\n"
            f"- Score: {md.get('score')}\n"
            f"- Word count: {md.get('wordCount')}\n\n"
            f"## Evidence Notes\n\n"
            f"- Discovery source: OpenCLI Browser Bridge profile `{args.profile}` latest list endpoint page {args.page} (`/api/proxy/resources?page={args.page}&pageSize={args.page_size}&timeFilter=1w&language=all&sortType=latest&type=ARTICLE&qualifiedFilter=false&uiLang=en`).\n"
            f"- Detail source: BestBlogs resource page/content endpoints for slug `{slug}`.\n"
        ))
        write_text(item_dir / "summary.md", (
            f"# {bbid} Summary\n\n"
            f"## Article\n\n"
            f"- Title: {title}\n"
            f"- Source: {source}\n"
            f"- URL: {read_url}\n"
            f"- Date: {date}\n"
            f"- Topic: `{topic}`\n"
            f"- Tags: {', '.join(tags) if tags else ''}\n\n"
            f"## Model Mapping\n\n"
            f"- Blocks: {blocks}\n"
            f"- Layer: captured frontier material, pending deep reading\n\n"
            f"## Core Takeaway\n\n"
            f"{md.get('summary') or md.get('oneSentenceSummary') or 'Full text captured for later selective reading and synthesis.'}\n\n"
            f"## Reusable Principle\n\n"
            f"{md.get('featuredReason') or 'Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.'}\n"
        ))

        status = "Full text + source captured" if len(plain) > 800 else "Short page captured"
        index_append.append(f"| {bbid} | {md_cell(date)} | {md_cell(title)} | {md_cell(source)} | `{topic}` | {md_cell(blocks)} | {status} |")
        results.append((bbid, slug, title, topic, len(plain)))
        memory_notes.append(f"On {args.discovery_date}, captured {bbid}: {title} ({topic}, slug `{slug}`) from OpenCLI Browser Bridge profile `{args.profile}` latest article page {args.page} feed, with full text, source evidence, and raw page/content JSON saved.")
        seen_urls.add(norm)
        seen_titles.add(title)
        seen_originals.add(original_norm)
        time.sleep(1)

    if index_append:
        write_text(INDEX, read_text(INDEX).rstrip() + "\n" + "\n".join(index_append) + "\n")
        append_memory(memory_notes)

    end = start + max(len(results) - 1, 0)
    report = {
        "profile": args.profile,
        "page_no": args.page,
        "captured_count": len(results),
        "start_id": results[0][0] if results else None,
        "end_id": results[-1][0] if results else None,
        "items": results,
        "errors": errors,
        "skipped": skipped,
        "list_path": str(list_path),
    }
    write_text(REPORT_DIR / f"opencli-latest-batch-{start:03d}-{end:03d}.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
