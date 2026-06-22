import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
CANDIDATES_ROOT = ROOT / "knowledge" / "candidates"
ITEMS_ROOT = ROOT / "knowledge" / "items"
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"
SOURCE_ARTICLE_INDEX_PATH = ROOT / "knowledge" / "catalog" / "source-article-index.md"
PAPER_INDEX_PATH = ROOT / "knowledge" / "catalog" / "paper-index.md"
INBOX_PATH = CANDIDATES_ROOT / "inbox.jsonl"
PROMOTED_PATH = CANDIDATES_ROOT / "promoted.jsonl"
REJECTED_PATH = CANDIDATES_ROOT / "rejected.jsonl"
DEFERRED_PATH = CANDIDATES_ROOT / "deferred.jsonl"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    "paper",
    "github",
    "智能体",
    "大模型",
    "模型",
    "论文",
    "评测",
]

NOISE_PATTERNS = [
    "/login",
    "/signin",
    "/sign-in",
    "/signup",
    "/join",
    "/pricing",
    "/privacy",
    "/terms",
    "/cookies",
    "/support",
    "/contact",
    "utm_",
    "#",
]

NOISE_HOSTS = {
    "app6ca5octe2206.pc.xiaoe-tech.com",
    "discord.gg",
    "instagram.com",
    "tiktok.com",
    "x.com",
    "youtube.com",
    "linkedin.com",
}

NOISE_HOST_PATH_PREFIXES = {
    "chatgpt.com": ["/business"],
    "claude.com": ["/"],
    "docs.github.com": ["/"],
    "huggingface.co": ["/inference", "/storage"],
    "openai.com": ["/open-models"],
    "pro.jiqizhixin.com": ["/inbox"],
    "anthropic.com": ["/claude", "/product"],
}

GENERIC_TITLES = {
    "",
    "ai",
    "ai agents",
    "ai chief of staff",
    "ai designer",
    "ai engineer",
    "ai sdr",
    "ai shortlist",
    "ai voice agents",
    "business",
    "categories",
    "company",
    "developers",
    "design tools",
    "docs",
    "home",
    "launches",
    "news",
    "pricing",
    "products",
    "product",
    "research",
    "resources",
    "safety",
    "security",
    "engineering",
    "global affairs",
    "ai adoption",
    "search syntax tips",
    "buckets new",
    "daily papers",
    "inference providers",
    "inference endpoints",
    "economic futures",
    "download press kit",
    "featured",
    "sign up",
    "get meta ai",
    "skip to main content",
    "try chatgpt",
}

GITHUB_RESERVED = {
    "about",
    "account",
    "copilot",
    "dashboard",
    "events",
    "explore",
    "features",
    "issues",
    "marketplace",
    "notifications",
    "orgs",
    "pricing",
    "pulls",
    "repos",
    "settings",
    "topics",
    "trending",
}

PRODUCTHUNT_ITEM_PREFIXES = {"/products/", "/posts/"}

PROMOTED_PREFIXES = {
    "article": "WEB",
    "paper": "PAPER",
    "product": "PRODUCT",
    "repo": "REPO",
}

TOPIC_RULES = [
    ("04-evaluation-guardrails", ["benchmark", "eval", "evaluation", "safety", "alignment", "guardrail", "security", "risk", "policy"], ["Evaluation", "Guardrails", "Source Signal"]),
    ("03-control-loop", ["agent", "agentic", "multi-agent", "workflow", "orchestration", "planning", "computer use", "harness"], ["Goal", "Context/State", "Control Loop"]),
    ("01-context-memory", ["context", "memory", "rag", "retrieval", "knowledge", "long context"], ["Context/State", "Memory", "Source Signal"]),
    ("02-tools-actions", ["tool", "api", "sdk", "browser", "github", "repo", "cli", "deployment", "inference", "codex"], ["Tools/Actions", "Infrastructure", "Source Signal"]),
]

HTTP_HEADERS = {
    "User-Agent": "aiagentstudy-candidate-promote/1.0",
    "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,*/*",
}


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_stack = []
        self.parts = []
        self.title_parts = []
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
        text = html.unescape(data or "").strip()
        if not text:
            return
        if self.in_title:
            self.title_parts.append(text)
        self.parts.extend([text, " "])

    def text(self):
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def title(self):
        return re.sub(r"\s+", " ", " ".join(self.title_parts)).strip()


def ensure_files():
    CANDIDATES_ROOT.mkdir(parents=True, exist_ok=True)
    for path in [INBOX_PATH, PROMOTED_PATH, REJECTED_PATH, DEFERRED_PATH]:
        if not path.exists():
            path.write_text("", encoding="utf-8")


def normalize_url(url):
    try:
        parsed = urlparse(url or "")
    except ValueError:
        return ""
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    cleaned = parsed._replace(fragment="", query="")
    return cleaned.geturl().rstrip("/")


def read_jsonl(path):
    ensure_files()
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            rows.append({"_invalid": True, "path": str(path), "line": line_no, "error": str(exc), "raw": line})
    return rows


def write_jsonl(path, rows):
    ensure_files()
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def md_cell(text):
    return re.sub(r"\s+", " ", text or "").replace("|", "/").strip()


def all_rows():
    return {
        "inbox": read_jsonl(INBOX_PATH),
        "promoted": read_jsonl(PROMOTED_PATH),
        "rejected": read_jsonl(REJECTED_PATH),
        "deferred": read_jsonl(DEFERRED_PATH),
    }


def candidate_path_for_bucket(bucket):
    paths = {
        "inbox": INBOX_PATH,
        "promoted": PROMOTED_PATH,
        "rejected": REJECTED_PATH,
        "deferred": DEFERRED_PATH,
    }
    if bucket not in paths:
        raise ValueError(f"Unknown candidate bucket: {bucket}")
    return paths[bucket]


def candidate_number_counters():
    counters = {}
    pattern = re.compile(r"^CAND-(20\d{2})-(\d{4})$")
    for rows in all_rows().values():
        for row in rows:
            match = pattern.match(row.get("candidate_id", ""))
            if match:
                year = match.group(1)
                counters[year] = max(counters.get(year, 0), int(match.group(2)))
    return counters


def existing_urls():
    urls = set()
    for rows in all_rows().values():
        for row in rows:
            normalized = normalize_url(row.get("url", ""))
            if normalized:
                urls.add(normalized)
    return urls


def next_candidate_id(year=None):
    year = year or datetime.now().strftime("%Y")
    counters = candidate_number_counters()
    return f"CAND-{year}-{counters.get(str(year), 0) + 1:04d}"


def allocate_candidate_id(year, counters):
    year = str(year or datetime.now().strftime("%Y"))[:4]
    counters[year] = counters.get(year, 0) + 1
    return f"CAND-{year}-{counters[year]:04d}"


def path_parts(url):
    try:
        parsed = urlparse(url or "")
    except ValueError:
        return []
    return [part for part in parsed.path.split("/") if part]


def canonical_host(url):
    try:
        host = urlparse(url or "").netloc.lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def is_github_repo_url(url):
    parsed = urlparse(url)
    if canonical_host(url) != "github.com":
        return False
    parts = path_parts(url)
    if len(parts) != 2:
        return False
    return parts[0].lower() not in GITHUB_RESERVED and parts[1].lower() not in GITHUB_RESERVED


def is_producthunt_item_url(url):
    if canonical_host(url) != "producthunt.com":
        return False
    path = urlparse(url).path.lower()
    return any(path.startswith(prefix) and len(path_parts(url)) == 2 for prefix in PRODUCTHUNT_ITEM_PREFIXES)


def is_paper_url(url, title=""):
    parsed = urlparse(url)
    host = canonical_host(url)
    haystack = f"{url} {title}".lower()
    if host == "arxiv.org" and (parsed.path.startswith("/abs/") or parsed.path.startswith("/pdf/")):
        return True
    if host in {"openreview.net", "papers.ssrn.com"}:
        return True
    if host == "huggingface.co" and parsed.path.startswith("/papers/"):
        return True
    return "paper" in haystack and len(path_parts(url)) >= 2


def is_article_url(url):
    host = canonical_host(url)
    parsed = urlparse(url)
    path = parsed.path.lower()
    parts = path_parts(url)
    if host == "openai.com":
        return path.startswith("/index/") and len(parts) >= 2
    if host == "anthropic.com":
        return path.startswith("/news/") and len(parts) >= 2
    if host == "ai.meta.com":
        return path.startswith("/blog/") and len(parts) >= 2
    if host == "pro.jiqizhixin.com":
        return path.startswith("/reference/") and len(parts) >= 2
    if host == "jiqizhixin.com":
        return path.startswith("/articles/") or path.startswith("/short_urls/")
    return len(parts) >= 2


def title_from_url(url):
    parts = path_parts(url)
    if not parts:
        return url
    if is_github_repo_url(url):
        return "/".join(parts[:2])
    slug = parts[-1]
    if re.fullmatch(r"\d+(\.\d+)?|[0-9a-f-]{12,}", slug.lower()):
        return url
    return re.sub(r"\s+", " ", re.sub(r"[-_]+", " ", slug)).strip().title()


def item_url_exists(url):
    normalized = normalize_url(url)
    if not normalized:
        return ""
    for source_path in ITEMS_ROOT.glob("**/source.md"):
        text = read_text(source_path)
        for match in re.finditer(r"https?://[^\s)]+", text):
            if normalize_url(match.group(0)) == normalized:
                return str(source_path.parent.relative_to(ROOT)).replace("\\", "/")
    return ""


def next_promoted_item_id(candidate_type, year):
    prefix = PROMOTED_PREFIXES.get(candidate_type or "article", "WEB")
    max_num = 0
    pattern = re.compile(rf"^{re.escape(prefix)}-{re.escape(str(year))}-(\d{{3}})$")
    for path in ITEMS_ROOT.glob(f"**/{prefix}-{year}-*"):
        match = pattern.match(path.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"{prefix}-{year}-{max_num + 1:03d}"


def classify_candidate(candidate, page_text=""):
    hint = candidate.get("topic_hint", "")
    if hint and (ITEMS_ROOT / hint).exists():
        topic = hint
    else:
        haystack = f"{candidate.get('title', '')} {candidate.get('url', '')} {page_text[:3000]}".lower()
        topic = "06-frontier-radar"
        for candidate_topic, keywords, _blocks in TOPIC_RULES:
            if any(keyword in haystack for keyword in keywords):
                topic = candidate_topic
                break
    haystack = f"{candidate.get('title', '')} {candidate.get('url', '')} {page_text[:3000]}".lower()
    blocks = None
    for rule_topic, keywords, rule_blocks in TOPIC_RULES:
        if rule_topic == topic or any(keyword in haystack for keyword in keywords):
            blocks = rule_blocks
            break
    if not blocks:
        blocks = ["Model", "Frontier Radar", "Source Signal"]
    return topic, blocks


def tags_for_candidate(candidate, page_text=""):
    haystack = f"{candidate.get('title', '')} {candidate.get('url', '')} {page_text[:3000]}".lower()
    tags = [candidate.get("source_name") or candidate.get("source_id") or "Candidate", candidate.get("type", "article").title()]
    for needle, tag in [
        ("agent", "AI Agent"),
        ("agentic", "Agentic AI"),
        ("llm", "LLM"),
        ("large language model", "LLM"),
        ("model", "Model"),
        ("claude", "Claude"),
        ("openai", "OpenAI"),
        ("codex", "Codex"),
        ("memory", "Memory"),
        ("rag", "RAG"),
        ("retrieval", "Retrieval"),
        ("benchmark", "Benchmark"),
        ("eval", "Evaluation"),
        ("github", "GitHub"),
        ("paper", "Paper"),
        ("论文", "Paper"),
        ("智能体", "AI Agent"),
        ("大模型", "LLM"),
    ]:
        if needle in haystack and tag not in tags:
            tags.append(tag)
    return tags[:8]


def infer_type(url, title=""):
    haystack = f"{url} {title}".lower()
    parsed = urlparse(url)
    if is_paper_url(url, title):
        return "paper"
    if is_github_repo_url(url):
        return "repo"
    if is_producthunt_item_url(url):
        return "product"
    return "article"


def candidate_is_relevant(title, url, keywords=None):
    keywords = keywords or KEYWORDS
    normalized = normalize_url(url)
    if not normalized:
        return False
    host = canonical_host(normalized)
    if host in NOISE_HOSTS:
        return False
    parsed = urlparse(normalized)
    if any(parsed.path.lower().startswith(prefix) for prefix in NOISE_HOST_PATH_PREFIXES.get(host, [])):
        return False
    low_url = normalized.lower()
    if any(pattern in low_url for pattern in NOISE_PATTERNS):
        return False
    clean_title = re.sub(r"\s+", " ", title or "").strip()
    low_title = clean_title.lower()
    structured_item = (
        is_paper_url(normalized, clean_title)
        or is_github_repo_url(normalized)
        or is_producthunt_item_url(normalized)
        or is_article_url(normalized)
    )
    if low_title in GENERIC_TITLES and not structured_item:
        return False
    if clean_title == normalized and not structured_item:
        return False
    if host == "github.com":
        return is_github_repo_url(normalized)
    if host == "producthunt.com":
        if not is_producthunt_item_url(normalized):
            return False
    parts = path_parts(normalized)
    if len(parts) == 0:
        return False
    if len(parts) == 1 and host in {"openai.com", "anthropic.com", "ai.meta.com", "jiqizhixin.com", "huggingface.co"}:
        return False
    if len(parts) == 1 and (low_title in GENERIC_TITLES or low_title == parts[0].lower()):
        return False
    haystack = f"{clean_title} {urlparse(normalized).path}".lower()
    return any(keyword.lower() in haystack for keyword in keywords)


def make_candidate(
    title,
    url,
    source,
    route,
    topic_hint,
    reason,
    evidence_path,
    discovered_at=None,
    candidate_type=None,
):
    normalized = normalize_url(url)
    clean_title = re.sub(r"\s+", " ", title or normalized).strip()
    if clean_title.lower() in GENERIC_TITLES or clean_title == normalized or re.fullmatch(r"GitHub\s+[\d.]+k?", clean_title, re.I):
        clean_title = title_from_url(normalized)
    return {
        "candidate_id": "",
        "status": "radar",
        "type": candidate_type or infer_type(normalized, title),
        "title": clean_title[:240],
        "url": normalized,
        "source_id": source.get("id", ""),
        "source_name": source.get("name", source.get("id", "")),
        "discovered_at": discovered_at or datetime.now().strftime("%Y-%m-%d"),
        "route": route,
        "topic_hint": topic_hint,
        "reason": reason,
        "evidence_path": evidence_path.replace("\\", "/") if evidence_path else "",
        "promoted_id": "",
        "reject_reason": "",
    }


def append_candidates(candidates):
    ensure_files()
    rows = read_jsonl(INBOX_PATH)
    seen = existing_urls()
    counters = candidate_number_counters()
    appended = []
    for candidate in candidates:
        normalized = normalize_url(candidate.get("url", ""))
        if not normalized or normalized in seen:
            continue
        year = (candidate.get("discovered_at") or datetime.now().strftime("%Y"))[:4]
        candidate = dict(candidate)
        candidate["url"] = normalized
        candidate["candidate_id"] = candidate.get("candidate_id") or allocate_candidate_id(year, counters)
        rows.append(candidate)
        seen.add(normalized)
        appended.append(candidate)
    write_jsonl(INBOX_PATH, rows)
    return appended


def append_promoted(candidates):
    ensure_files()
    rows = read_jsonl(PROMOTED_PATH)
    seen_urls = existing_urls()
    seen_promoted_ids = {row.get("promoted_id", "") for row in rows}
    counters = candidate_number_counters()
    appended = []
    for candidate in candidates:
        normalized = normalize_url(candidate.get("url", ""))
        promoted_id = candidate.get("promoted_id", "")
        if not normalized or promoted_id in seen_promoted_ids or normalized in seen_urls:
            continue
        year = (candidate.get("discovered_at") or datetime.now().strftime("%Y"))[:4]
        candidate = dict(candidate)
        candidate["url"] = normalized
        candidate["status"] = "captured"
        candidate["candidate_id"] = candidate.get("candidate_id") or allocate_candidate_id(year, counters)
        rows.append(candidate)
        seen_urls.add(normalized)
        seen_promoted_ids.add(promoted_id)
        appended.append(candidate)
    write_jsonl(PROMOTED_PATH, rows)
    return appended


def validate_candidates():
    required = ["candidate_id", "status", "type", "title", "url", "source_id", "discovered_at", "route"]
    errors = []
    ids = set()
    urls = set()
    for name, rows in all_rows().items():
        for idx, row in enumerate(rows, start=1):
            if row.get("_invalid"):
                errors.append(row)
                continue
            for field in required:
                if not row.get(field):
                    errors.append({"file": name, "line": idx, "error": f"missing {field}"})
            candidate_id = row.get("candidate_id", "")
            if candidate_id in ids:
                errors.append({"file": name, "line": idx, "error": f"duplicate candidate_id {candidate_id}"})
            ids.add(candidate_id)
            normalized = normalize_url(row.get("url", ""))
            if not normalized:
                errors.append({"file": name, "line": idx, "error": "invalid url"})
            elif normalized in urls:
                errors.append({"file": name, "line": idx, "error": f"duplicate url {normalized}"})
            urls.add(normalized)
    return errors


WATCH_GROUP_FIELDS = {
    "source": "source_id",
    "type": "type",
    "topic": "topic_hint",
    "route": "route",
    "date": "discovered_at",
    "status": "status",
}


def valid_candidate_rows(path):
    return [row for row in read_jsonl(path) if not row.get("_invalid")]


def candidate_bucket_counts():
    return {
        "inbox": len(valid_candidate_rows(INBOX_PATH)),
        "promoted": len(valid_candidate_rows(PROMOTED_PATH)),
        "deferred": len(valid_candidate_rows(DEFERRED_PATH)),
        "rejected": len(valid_candidate_rows(REJECTED_PATH)),
    }


def candidate_watch_row(row):
    return {
        "candidate_id": row.get("candidate_id", ""),
        "status": row.get("status", ""),
        "type": row.get("type", ""),
        "title": row.get("title", ""),
        "url": row.get("url", ""),
        "source_id": row.get("source_id", ""),
        "source_name": row.get("source_name", ""),
        "topic_hint": row.get("topic_hint", ""),
        "route": row.get("route", ""),
        "discovered_at": row.get("discovered_at", ""),
        "reason": row.get("reason", ""),
        "evidence_path": row.get("evidence_path", ""),
        "promoted_id": row.get("promoted_id", ""),
        "defer_reason": row.get("defer_reason", ""),
        "reject_reason": row.get("reject_reason", ""),
    }


def group_key(row, group_by):
    field = WATCH_GROUP_FIELDS.get(group_by, "")
    return row.get(field) or "(empty)"


def counter_items(rows, field, limit=10):
    counts = Counter(row.get(field) or "(empty)" for row in rows)
    return [{"key": key, "count": count} for key, count in counts.most_common(limit)]


def build_watch_payload(limit=20, source_ids=None, status=None, bucket="inbox", group_by=""):
    ensure_files()
    rows = valid_candidate_rows(candidate_path_for_bucket(bucket))
    if source_ids:
        allowed = set(source_ids)
        rows = [row for row in rows if row.get("source_id") in allowed]
    if status:
        rows = [row for row in rows if row.get("status") == status]
    rows.sort(key=lambda row: (row.get("discovered_at", ""), row.get("candidate_id", "")), reverse=True)
    matched_rows = rows
    visible_rows = rows[:limit]
    groups = []
    if group_by:
        grouped = defaultdict(list)
        for row in visible_rows:
            grouped[group_key(row, group_by)].append(row)
        groups = [
            {
                "key": key,
                "count": len(group_rows),
                "items": [candidate_watch_row(row) for row in group_rows],
            }
            for key, group_rows in grouped.items()
        ]
        groups.sort(key=lambda group: (group["count"], group["key"]), reverse=True)
    return {
        "bucket": bucket,
        "filters": {
            "source_ids": source_ids or [],
            "status": status or "",
        },
        "limit": limit,
        "counts": candidate_bucket_counts(),
        "matched_count": len(matched_rows),
        "selected_count": len(visible_rows),
        "group_by": group_by,
        "summary": {
            "source": counter_items(matched_rows, "source_id"),
            "type": counter_items(matched_rows, "type"),
            "topic": counter_items(matched_rows, "topic_hint"),
            "route": counter_items(matched_rows, "route"),
            "date": counter_items(matched_rows, "discovered_at"),
            "status": counter_items(matched_rows, "status"),
        },
        "groups": groups,
        "items": [candidate_watch_row(row) for row in visible_rows],
    }


def print_watch_item(row, indent=""):
    print(f"{indent}- {row.get('candidate_id')} [{row.get('type')}] {row.get('title')}")
    print(f"{indent}  Source: {row.get('source_name')} ({row.get('source_id')})")
    print(f"{indent}  Topic hint: {row.get('topic_hint')} | Route: {row.get('route')} | Date: {row.get('discovered_at')}")
    print(f"{indent}  URL: {row.get('url')}")
    if row.get("reason"):
        print(f"{indent}  Reason: {row.get('reason')}")
    if row.get("defer_reason"):
        print(f"{indent}  Defer: {row.get('defer_reason')}")
    if row.get("reject_reason"):
        print(f"{indent}  Reject: {row.get('reject_reason')}")


def print_watch_summary(payload):
    for label, key in [
        ("Sources", "source"),
        ("Types", "type"),
        ("Topics", "topic"),
        ("Routes", "route"),
        ("Dates", "date"),
        ("Statuses", "status"),
    ]:
        items = payload["summary"].get(key, [])
        if not items:
            continue
        print(f"  {label}: " + ", ".join(f"{item['key']}={item['count']}" for item in items))


def show_watch(limit=20, source_ids=None, status=None, bucket="inbox", group_by="", summary=False, emit_json=False):
    payload = build_watch_payload(
        limit=limit,
        source_ids=source_ids,
        status=status,
        bucket=bucket,
        group_by=group_by,
    )
    if summary:
        payload = dict(payload)
        payload["items"] = []
        payload["groups"] = []
    if emit_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print("Knowledge candidate watch")
    print(f"  Inbox: {payload['counts']['inbox']}")
    print(f"  Promoted: {payload['counts']['promoted']}")
    print(f"  Deferred: {payload['counts']['deferred']}")
    print(f"  Rejected: {payload['counts']['rejected']}")
    print(f"  Bucket: {bucket}")
    print(f"  Matched: {payload['matched_count']}")
    print(f"  Showing: {payload['selected_count']}")
    if group_by:
        print(f"  Group by: {group_by}")
    if summary:
        print_watch_summary(payload)
        return
    if group_by:
        for group in payload["groups"]:
            print("")
            print(f"- {group['key']}: {group['count']}")
            for row in group["items"]:
                print("")
                print_watch_item(row, indent="  ")
        return
    for row in payload["items"]:
        print("")
        print_watch_item(row)


def extract_json_object(output):
    decoder = json.JSONDecoder()
    for idx, char in enumerate(output or ""):
        if char in "[{":
            try:
                value, _ = decoder.raw_decode(output[idx:])
                return value
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


def fetch_http_capture(url, timeout=60):
    import requests

    session = requests.Session()
    session.trust_env = False
    response = session.get(url, headers=HTTP_HEADERS, timeout=timeout)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    body = response.text
    title = ""
    text = body
    if "html" in content_type.lower() or "<html" in body[:500].lower():
        parser = TextExtractor()
        parser.feed(body)
        title = parser.title()
        text = parser.text()
    return {
        "method": "http",
        "url": response.url,
        "status_code": response.status_code,
        "content_type": content_type,
        "title": title,
        "text": text,
        "html": body,
        "error": "",
    }


def fetch_browser_capture(url, profile):
    opened = run_opencli(["browser", profile, "tab", "new", url], timeout=90)
    page_info = extract_json_object(opened["stdout"]) if opened["returncode"] == 0 else None
    if opened["returncode"] != 0 or not page_info or not page_info.get("page"):
        return {
            "method": "browser",
            "url": url,
            "title": "",
            "text": "",
            "html": "",
            "error": "open_failed",
            "open": opened,
            "page_info": page_info,
        }
    tab_id = page_info["page"]
    run_opencli(["browser", profile, "tab", "select", tab_id], timeout=30)
    eval_js = (
        "(()=>{"
        "const text=(document.body&&document.body.innerText||'').replace(/\\s+/g,' ').trim();"
        "const html=document.documentElement&&document.documentElement.outerHTML||'';"
        "return {url:location.href,title:document.title,readyState:document.readyState,textLength:text.length,text,html};"
        "})()"
    )
    evaluated = {"returncode": 1, "stdout": "", "stderr": "not run"}
    page_state = None
    for attempt in range(4):
        if attempt:
            time.sleep(2)
        evaluated = run_opencli(["browser", profile, "eval", eval_js, "--tab", tab_id], timeout=120)
        page_state = extract_json_object(evaluated["stdout"]) if evaluated["returncode"] == 0 else None
        if page_state and page_state.get("url") != "about:blank" and page_state.get("textLength", 0) > 200:
            break
    if not page_state:
        page_state = {"url": url, "title": "", "text": "", "html": "", "textLength": 0}
    return {
        "method": "browser",
        "url": page_state.get("url") or url,
        "title": page_state.get("title", ""),
        "text": page_state.get("text", ""),
        "html": page_state.get("html", ""),
        "error": "" if page_state.get("textLength", 0) > 0 else "empty_page_state",
        "open": opened,
        "page_info": page_info,
        "eval": evaluated,
        "page_state": page_state,
    }


def append_catalog_index(rows):
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
        f"| {row['id']} | {md_cell(row['date'])} | {md_cell(row['title'])} | {md_cell(row['source'])} | `{row['topic']}` | Candidate promotion |"
        for row in rows
    ]
    if not text.endswith("\n"):
        text += "\n"
    write_text(SOURCE_ARTICLE_INDEX_PATH, text + "\n".join(additions) + "\n")


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
        f"| {row['id']} | {md_cell(row['date'])} | {md_cell(row['title'])} | {md_cell(row['source'])} | `{row['topic']}` | Candidate promotion |"
        for row in rows
    ]
    if not text.endswith("\n"):
        text += "\n"
    write_text(PAPER_INDEX_PATH, text + "\n".join(additions) + "\n")


def write_promoted_item(candidate, capture, collection_date, topic_override=None):
    page_text = capture.get("text", "")
    title = md_cell(capture.get("title") or candidate.get("title") or title_from_url(candidate.get("url", "")))
    topic, blocks = classify_candidate(candidate | {"topic_hint": topic_override or candidate.get("topic_hint", "")}, page_text)
    local_id = next_promoted_item_id(candidate.get("type", "article"), collection_date[:4])
    item_dir = ITEMS_ROOT / topic / local_id
    raw_dir = item_dir / "raw"
    source_label = f"Candidate / {candidate.get('source_name') or candidate.get('source_id') or candidate.get('route')}"
    tags = tags_for_candidate(candidate, page_text)
    final_url = normalize_url(capture.get("url") or candidate.get("url", ""))
    capture_method = capture.get("method", "http")
    text_note = "full page text captured" if page_text else "metadata captured; page text unavailable"

    summary = f"""# {local_id} Summary

## Article

- Title: {title}
- Source: {source_label}
- URL: {final_url}
- Date: {collection_date}
- Topic: `{topic}`
- Tags: {", ".join(tags)}

## Model Mapping

- Blocks: {", ".join(blocks)}
- Layer: promoted source candidate

## Core Takeaway

This item was promoted from `{candidate.get('candidate_id')}` because it appeared in source radar and matched the local AI-agent watch criteria. The durable capture preserves source evidence, candidate provenance, raw extraction output, and {text_note}.

## Reusable Principle

Use candidate promotion for source signals that deserve durable recall. Keep this note lightweight until a later deep-reading pass extracts claims, mechanisms, comparisons, or implementation lessons.
"""

    article = f"""# {title}

---

- Local ID: {local_id}
- Candidate ID: {candidate.get('candidate_id')}
- Type: {candidate.get('type')}
- Source: {source_label}
- Source ID: {candidate.get('source_id')}
- URL: {final_url}
- Original candidate URL: {candidate.get('url')}
- Collection date: {collection_date}
- Capture method: {capture_method}

---

## Candidate Reason

{candidate.get('reason', '')}

## Captured Text

{page_text or '(No page text captured.)'}
"""

    source_doc = f"""# Source Evidence

- Title: {title}
- Source URL: {final_url}
- Original publisher URL: {final_url}
- Candidate URL: {candidate.get('url')}
- Candidate ID: {candidate.get('candidate_id')}
- Candidate source ID: {candidate.get('source_id')}
- Candidate source name: {candidate.get('source_name')}
- Candidate evidence path: {candidate.get('evidence_path')}
- Capture method: {capture_method}
- Collection date: {collection_date}

## Evidence Notes

- Promoted from `knowledge/candidates/inbox.jsonl`.
- Raw candidate record and page extraction output are stored under `raw/`.
- This is a candidate-level capture, not a finished synthesis note.
"""

    write_text(item_dir / "summary.md", summary)
    write_text(item_dir / "article.md", article)
    write_text(item_dir / "source.md", source_doc)
    write_text(raw_dir / "candidate.json", json.dumps(candidate, ensure_ascii=False, indent=2) + "\n")
    write_text(raw_dir / "promotion-capture.json", json.dumps({k: v for k, v in capture.items() if k not in {"html", "text"}}, ensure_ascii=False, indent=2) + "\n")
    write_text(raw_dir / "page-text.txt", page_text)
    if capture.get("html"):
        write_text(raw_dir / "page.html", capture.get("html", ""))

    return {
        "id": local_id,
        "date": collection_date,
        "title": title,
        "source": source_label,
        "topic": topic,
        "blocks": blocks,
        "status": "Candidate promoted",
        "url": final_url,
        "item_dir": str(item_dir.relative_to(ROOT)).replace("\\", "/"),
    }


def move_candidate_to_promoted(candidate_id, promoted_id):
    inbox_rows = read_jsonl(INBOX_PATH)
    promoted_rows = read_jsonl(PROMOTED_PATH)
    found = None
    remaining = []
    for row in inbox_rows:
        if row.get("candidate_id") == candidate_id:
            found = dict(row)
        else:
            remaining.append(row)
    if not found:
        raise ValueError(f"candidate not found in inbox: {candidate_id}")
    found["status"] = "captured"
    found["promoted_id"] = promoted_id
    found["captured_at"] = datetime.now().strftime("%Y-%m-%d")
    promoted_rows.append(found)
    write_jsonl(INBOX_PATH, remaining)
    write_jsonl(PROMOTED_PATH, promoted_rows)
    return found


def move_candidate_to_bucket(candidate_id, target_bucket, status, reason_field, reason, extra=None, emit=True):
    inbox_rows = read_jsonl(INBOX_PATH)
    target_path = candidate_path_for_bucket(target_bucket)
    target_rows = read_jsonl(target_path)
    found = None
    remaining = []
    for row in inbox_rows:
        if row.get("candidate_id") == candidate_id:
            found = dict(row)
        else:
            remaining.append(row)
    if not found:
        raise SystemExit(f"Candidate not found in inbox: {candidate_id}")

    found["status"] = status
    found[reason_field] = reason
    found[f"{status}_at"] = datetime.now().strftime("%Y-%m-%d")
    if extra:
        found.update(extra)
    target_rows.append(found)
    write_jsonl(INBOX_PATH, remaining)
    write_jsonl(target_path, target_rows)
    if emit:
        print(json.dumps({target_bucket.rstrip("s") if target_bucket.endswith("s") else target_bucket: found}, ensure_ascii=False, indent=2))
    return found


def reject_candidate(candidate_id, reason):
    return move_candidate_to_bucket(candidate_id, "rejected", "rejected", "reject_reason", reason)


def defer_candidate(candidate_id, reason, until=""):
    extra = {"deferred_until": until} if until else {}
    return move_candidate_to_bucket(candidate_id, "deferred", "deferred", "defer_reason", reason, extra=extra)


def select_candidates(bucket="inbox", source_ids=None, candidate_types=None, query="", status=None, limit=20):
    rows = read_jsonl(candidate_path_for_bucket(bucket))
    rows = [row for row in rows if not row.get("_invalid")]
    if source_ids:
        allowed = set(source_ids)
        rows = [row for row in rows if row.get("source_id") in allowed]
    if candidate_types:
        allowed_types = set(candidate_types)
        rows = [row for row in rows if row.get("type") in allowed_types]
    if status:
        rows = [row for row in rows if row.get("status") == status]
    if query:
        needle = query.lower()
        rows = [
            row
            for row in rows
            if needle
            in " ".join(
                [
                    row.get("candidate_id", ""),
                    row.get("title", ""),
                    row.get("url", ""),
                    row.get("source_id", ""),
                    row.get("source_name", ""),
                    row.get("reason", ""),
                ]
            ).lower()
        ]
    rows.sort(key=lambda row: (row.get("discovered_at", ""), row.get("candidate_id", "")), reverse=True)
    return rows[:limit]


def bulk_candidates(action="show", bucket="inbox", source_ids=None, candidate_types=None, query="", status=None, limit=20, reason="", until="", execute=False):
    selected = select_candidates(
        bucket=bucket,
        source_ids=source_ids,
        candidate_types=candidate_types,
        query=query,
        status=status,
        limit=limit,
    )
    summary = {
        "action": action,
        "bucket": bucket,
        "execute": execute,
        "selected_count": len(selected),
        "selected": [
            {
                "candidate_id": row.get("candidate_id"),
                "type": row.get("type"),
                "title": row.get("title"),
                "source_id": row.get("source_id"),
                "url": row.get("url"),
            }
            for row in selected
        ],
    }
    if action == "show":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return summary
    if action not in {"defer", "reject"}:
        raise SystemExit("Bulk action must be show, defer, or reject.")
    if bucket != "inbox":
        raise SystemExit("Bulk defer/reject only operates on inbox candidates.")
    if not reason:
        raise SystemExit("Bulk defer/reject requires --reason.")
    if not execute:
        summary["dry_run"] = True
        summary["note"] = "Add --execute to apply this bulk action."
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return summary

    moved = []
    for row in selected:
        if action == "defer":
            extra = {"deferred_until": until} if until else {}
            moved.append(move_candidate_to_bucket(row["candidate_id"], "deferred", "deferred", "defer_reason", reason, extra=extra, emit=False))
        else:
            moved.append(move_candidate_to_bucket(row["candidate_id"], "rejected", "rejected", "reject_reason", reason, emit=False))
    result = {
        **summary,
        "moved_count": len(moved),
        "target_bucket": "deferred" if action == "defer" else "rejected",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def restore_candidate(candidate_id, source_bucket=None, reason=""):
    buckets = [source_bucket] if source_bucket else ["deferred", "rejected"]
    inbox_rows = read_jsonl(INBOX_PATH)
    if any(row.get("candidate_id") == candidate_id for row in inbox_rows):
        raise SystemExit(f"Candidate is already in inbox: {candidate_id}")

    found = None
    found_bucket = ""
    remaining_by_bucket = {}
    for bucket in buckets:
        if bucket not in {"deferred", "rejected"}:
            raise SystemExit("Restore source must be deferred or rejected.")
        rows = read_jsonl(candidate_path_for_bucket(bucket))
        remaining = []
        for row in rows:
            if row.get("candidate_id") == candidate_id:
                found = dict(row)
                found_bucket = bucket
            else:
                remaining.append(row)
        remaining_by_bucket[bucket] = remaining
        if found:
            break

    if not found:
        searched = ", ".join(buckets)
        raise SystemExit(f"Candidate not found in {searched}: {candidate_id}")

    history = list(found.get("status_history") or [])
    history.append(
        {
            "from": found_bucket,
            "status": found.get("status", ""),
            "reject_reason": found.get("reject_reason", ""),
            "defer_reason": found.get("defer_reason", ""),
            "deferred_until": found.get("deferred_until", ""),
            "restored_at": datetime.now().strftime("%Y-%m-%d"),
            "restore_reason": reason,
        }
    )
    found["status"] = "radar"
    found["status_history"] = history
    found["restore_reason"] = reason
    found["restored_at"] = datetime.now().strftime("%Y-%m-%d")
    found["reject_reason"] = ""
    found.pop("defer_reason", None)
    found.pop("deferred_until", None)
    found.pop("deferred_at", None)
    found.pop("rejected_at", None)

    write_jsonl(candidate_path_for_bucket(found_bucket), remaining_by_bucket[found_bucket])
    inbox_rows.append(found)
    write_jsonl(INBOX_PATH, inbox_rows)
    print(json.dumps({"restored": found, "from": found_bucket, "to": "inbox"}, ensure_ascii=False, indent=2))
    return found


def promote_candidate(candidate_id, method="http", profile="qmvqcrb8", collection_date=None, topic=None, dry_run=False, force=False, allow_short=False):
    collection_date = collection_date or datetime.now().strftime("%Y-%m-%d")
    candidates = [row for row in read_jsonl(INBOX_PATH) if row.get("candidate_id") == candidate_id]
    if not candidates:
        raise SystemExit(f"Candidate not found in inbox: {candidate_id}")
    candidate = candidates[0]
    existing = item_url_exists(candidate.get("url", ""))
    if existing and not force:
        raise SystemExit(f"Candidate URL already appears in durable item: {existing}. Use --force to promote anyway.")

    capture = fetch_browser_capture(candidate["url"], profile) if method == "browser" else fetch_http_capture(candidate["url"])
    text_len = len(capture.get("text", ""))
    if capture.get("error"):
        raise SystemExit(f"Capture failed for {candidate_id}: {capture.get('error')}")
    if text_len < 250 and not allow_short:
        raise SystemExit(f"Captured text is short ({text_len} chars). Use --allow-short or --method browser if this is expected.")

    preview = {
        "candidate_id": candidate_id,
        "title": capture.get("title") or candidate.get("title"),
        "url": capture.get("url") or candidate.get("url"),
        "method": method,
        "text_length": text_len,
        "dry_run": dry_run,
    }
    if dry_run:
        print(json.dumps({"would_promote": preview, "candidate": candidate}, ensure_ascii=False, indent=2))
        return preview

    item_row = write_promoted_item(candidate, capture, collection_date, topic_override=topic)
    append_catalog_index([item_row])
    if candidate.get("type") == "paper":
        append_paper_index([item_row])
    else:
        append_source_article_index([item_row])
    moved = move_candidate_to_promoted(candidate_id, item_row["id"])
    print(json.dumps({"promoted": item_row, "candidate": moved}, ensure_ascii=False, indent=2))
    return item_row


def source_fields(source_text):
    fields = {}
    for key in ["Source ID", "Source name", "Collection date"]:
        match = re.search(rf"^- {re.escape(key)}: (.+)$", source_text, re.M)
        fields[key] = match.group(1).strip() if match else ""
    return fields


def seed_browser_snapshots(limit_per_snapshot=12, replace_inbox=False):
    if replace_inbox:
        ensure_files()
        write_jsonl(INBOX_PATH, [])
    candidates = []
    for item_dir in sorted(ITEMS_ROOT.glob("**/BROWSER-*")):
        source_path = item_dir / "source.md"
        page_state_path = item_dir / "raw" / "page-state.json"
        if not source_path.exists() or not page_state_path.exists():
            continue
        source_info = source_fields(source_path.read_text(encoding="utf-8"))
        try:
            page_state = json.loads(page_state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        source = {"id": source_info.get("Source ID", ""), "name": source_info.get("Source name", "")}
        topic_hint = item_dir.parent.name
        local_id = item_dir.name
        added = 0
        seen_snapshot_urls = {normalize_url(page_state.get("url", ""))}
        for link in page_state.get("links", []):
            url = normalize_url(link.get("href", ""))
            title = link.get("text") or url
            if not url or url in seen_snapshot_urls:
                continue
            seen_snapshot_urls.add(url)
            if not candidate_is_relevant(title, url):
                continue
            candidates.append(
                make_candidate(
                    title=title,
                    url=url,
                    source=source,
                    route="browser",
                    topic_hint=topic_hint,
                    reason=f"Seeded from existing browser snapshot {local_id}.",
                    evidence_path=str(page_state_path.relative_to(ROOT)),
                    discovered_at=source_info.get("Collection date") or datetime.now().strftime("%Y-%m-%d"),
                )
            )
            added += 1
            if added >= limit_per_snapshot:
                break
    appended = append_candidates(candidates)
    print(json.dumps({"seeded": len(appended), "candidates": appended}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Manage knowledge candidates.")
    sub = parser.add_subparsers(dest="command")

    watch = sub.add_parser("watch", help="Show candidate radar inbox.")
    watch.add_argument("--limit", type=int, default=20)
    watch.add_argument("--ids", nargs="*", help="Filter by source IDs.")
    watch.add_argument("--status", default="")
    watch.add_argument("--bucket", choices=["inbox", "promoted", "deferred", "rejected"], default="inbox")
    watch.add_argument("--group-by", choices=sorted(WATCH_GROUP_FIELDS), default="", help="Group visible candidates by one field.")
    watch.add_argument("--summary", action="store_true", help="Show only queue counts and compact breakdowns.")
    watch.add_argument("--json", action="store_true", help="Emit a machine-readable watch payload.")

    sub.add_parser("validate", help="Validate candidate JSONL files.")
    seed = sub.add_parser("seed-browser", help="Seed candidates from existing BROWSER-* snapshots.")
    seed.add_argument("--limit-per-snapshot", type=int, default=12)
    seed.add_argument("--replace-inbox", action="store_true", help="Clear inbox.jsonl before seeding browser snapshot candidates.")
    promote = sub.add_parser("promote", help="Promote one inbox candidate to a durable knowledge item.")
    promote.add_argument("candidate_id")
    promote.add_argument("--method", choices=["http", "browser"], default="http")
    promote.add_argument("--profile", default="qmvqcrb8")
    promote.add_argument("--collection-date", default=datetime.now().strftime("%Y-%m-%d"))
    promote.add_argument("--topic", help="Override topic directory.")
    promote.add_argument("--dry-run", action="store_true")
    promote.add_argument("--force", action="store_true", help="Promote even if the URL already appears in durable source evidence.")
    promote.add_argument("--allow-short", action="store_true", help="Allow captures with less than 250 characters of extracted text.")
    reject = sub.add_parser("reject", help="Move one inbox candidate to rejected.jsonl.")
    reject.add_argument("candidate_id")
    reject.add_argument("--reason", required=True)
    defer = sub.add_parser("defer", help="Move one inbox candidate to deferred.jsonl.")
    defer.add_argument("candidate_id")
    defer.add_argument("--reason", required=True)
    defer.add_argument("--until", default="", help="Optional revisit date or note.")
    restore = sub.add_parser("restore", help="Restore one deferred/rejected candidate to inbox.jsonl.")
    restore.add_argument("candidate_id")
    restore.add_argument("--from-bucket", choices=["deferred", "rejected"], default="")
    restore.add_argument("--reason", default="")
    bulk = sub.add_parser("bulk", help="Preview or bulk-move filtered candidates.")
    bulk.add_argument("--action", choices=["show", "defer", "reject"], default="show")
    bulk.add_argument("--bucket", choices=["inbox", "promoted", "deferred", "rejected"], default="inbox")
    bulk.add_argument("--ids", nargs="*", help="Filter by source IDs.")
    bulk.add_argument("--type", nargs="*", dest="candidate_types", help="Filter by candidate types.")
    bulk.add_argument("--query", default="", help="Filter by text across ID/title/URL/source/reason.")
    bulk.add_argument("--status", default="")
    bulk.add_argument("--limit", type=int, default=20)
    bulk.add_argument("--reason", default="", help="Required for bulk defer/reject.")
    bulk.add_argument("--until", default="", help="Optional revisit date or note for bulk defer.")
    bulk.add_argument("--execute", action="store_true", help="Apply the bulk defer/reject action.")

    args = parser.parse_args()
    if args.command == "watch":
        show_watch(
            limit=args.limit,
            source_ids=args.ids,
            status=args.status or None,
            bucket=args.bucket,
            group_by=args.group_by,
            summary=args.summary,
            emit_json=args.json,
        )
    elif args.command == "validate":
        errors = validate_candidates()
        print(json.dumps({"errors": errors, "error_count": len(errors)}, ensure_ascii=False, indent=2))
        if errors:
            raise SystemExit(1)
    elif args.command == "seed-browser":
        seed_browser_snapshots(limit_per_snapshot=args.limit_per_snapshot, replace_inbox=args.replace_inbox)
    elif args.command == "promote":
        promote_candidate(
            args.candidate_id,
            method=args.method,
            profile=args.profile,
            collection_date=args.collection_date,
            topic=args.topic,
            dry_run=args.dry_run,
            force=args.force,
            allow_short=args.allow_short,
        )
    elif args.command == "reject":
        reject_candidate(args.candidate_id, args.reason)
    elif args.command == "defer":
        defer_candidate(args.candidate_id, args.reason, until=args.until)
    elif args.command == "restore":
        restore_candidate(args.candidate_id, source_bucket=args.from_bucket or None, reason=args.reason)
    elif args.command == "bulk":
        bulk_candidates(
            action=args.action,
            bucket=args.bucket,
            source_ids=args.ids,
            candidate_types=args.candidate_types,
            query=args.query,
            status=args.status or None,
            limit=args.limit,
            reason=args.reason,
            until=args.until,
            execute=args.execute,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
