import argparse
import json
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ITEMS_ROOT = ROOT / "knowledge" / "items"
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"


def read_text(path):
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def write_text(path, text):
    path.write_text(text, encoding="utf-8")


def md_cells(line):
    return [part.strip() for part in line.split("|")]


def parse_index():
    rows = {}
    for line in read_text(INDEX_PATH).splitlines():
        if not line.startswith("| "):
            continue
        parts = md_cells(line)
        if len(parts) < 8 or not re.match(r"^[A-Z][A-Z0-9-]+-\d{4}", parts[1]):
            continue
        rows[parts[1]] = {
            "id": parts[1],
            "date": parts[2],
            "title": parts[3],
            "source": parts[4],
            "topic": parts[5].replace("`", ""),
            "blocks": [part.strip() for part in parts[6].split(",") if part.strip()],
            "status": parts[7],
        }
    return rows


def field(text, label):
    return (re.search(rf"^- {re.escape(label)}:[ \t]*([^\r\n]*)", text, re.M) or ["", ""])[1].strip()


def split_list(value):
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def extract_urls(text):
    return sorted(set(match.group(0).rstrip(".,):") for match in re.finditer(r"https?://[^\s)]+", text or "")))


def clean_url(value):
    value = (value or "").strip()
    if not value:
        return ""
    lowered = value.lower()
    if "not found" in lowered or "not available" in lowered or lowered in {"n/a", "none", "null"}:
        return ""
    return value if value.startswith(("http://", "https://")) else ""


def any_url_contains(urls, needle):
    return any(needle in (url or "").lower() for url in urls)


def infer_source_id(local_id, source_data, summary_source, urls):
    explicit = source_data["source_id"].strip()
    if explicit:
        return explicit, source_data["source_name"]
    source_name = source_data["source_name"] or summary_source
    haystack = " ".join([source_name, summary_source, *urls]).lower()
    if "internal synthesis" in haystack or "local kb" in haystack or "本地" in haystack or "知识库综合" in haystack:
        return "local-synthesis", source_name or "Local synthesis"
    domain_map = [
        ("bestblogs.dev", "bestblogs", source_name or "BestBlogs"),
        ("arxiv.org", "arxiv", source_name or "arXiv"),
        ("openreview.net", "openreview", source_name or "OpenReview"),
        ("github.com", "github", source_name or "GitHub"),
        ("owasp.org", "owasp", source_name or "OWASP"),
        ("portswigger.net", "portswigger", source_name or "PortSwigger"),
        ("docs.oasis-open.org", "oasis", source_name or "OASIS"),
    ]
    for marker, source_id, default_name in domain_map:
        if marker in haystack:
            return source_id, source_name or default_name
    if local_id.startswith("ARXIV-"):
        return "arxiv", source_name or "arXiv"
    if local_id.startswith("RSS-"):
        return "", source_name
    if local_id.startswith("BROWSER-"):
        return "", source_name
    return "", source_name


def item_type(local_id, source_id="", urls=None, source_name=""):
    urls = urls or []
    source_name = (source_name or "").lower()
    if local_id.startswith("BB-"):
        if source_id == "bestblogs" or any_url_contains(urls, "bestblogs.dev"):
            return "bestblogs_item"
        if source_id in {"arxiv", "openreview"} or any_url_contains(urls, "arxiv.org") or any_url_contains(urls, "openreview.net"):
            return "paper"
        if "internal synthesis" in source_name or "local kb" in source_name or "本地" in source_name or "知识库综合" in source_name:
            return "note"
        if source_id == "github" or any_url_contains(urls, "github.com"):
            return "repo"
        return "web_article"
    if local_id.startswith("ARXIV-"):
        return "paper"
    if local_id.startswith("RSS-"):
        return "rss_article"
    if local_id.startswith("BROWSER-"):
        return "browser_snapshot"
    if local_id.startswith("WEB-"):
        return "web_article"
    if local_id.startswith("PAPER-"):
        return "paper"
    if local_id.startswith("REPO-"):
        return "repo"
    if local_id.startswith("PRODUCT-"):
        return "product"
    return "item"


def list_item_dirs(ids=None):
    allowed = set(ids or [])
    dirs = []
    for summary_path in ITEMS_ROOT.glob("**/summary.md"):
        item_dir = summary_path.parent
        if allowed and item_dir.name not in allowed:
            continue
        dirs.append(item_dir)
    return sorted(dirs)


def raw_files(raw_dir):
    if not raw_dir.exists():
        return []
    return [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted(raw_dir.rglob("*")) if path.is_file()]


def source_fields(source_text):
    return {
        "source_url": clean_url(field(source_text, "Source URL") or field(source_text, "BestBlogs URL")),
        "original_url": clean_url(field(source_text, "Original publisher URL")),
        "requested_url": clean_url(field(source_text, "Requested URL")),
        "feed_url": clean_url(field(source_text, "Feed URL")),
        "pdf_url": clean_url(field(source_text, "PDF URL")),
        "source_id": field(source_text, "Source ID") or field(source_text, "Candidate source ID"),
        "source_name": field(source_text, "Source name") or field(source_text, "Candidate source name"),
        "candidate_id": field(source_text, "Candidate ID"),
        "candidate_url": clean_url(field(source_text, "Candidate URL")),
        "candidate_evidence_path": field(source_text, "Candidate evidence path"),
        "capture_method": field(source_text, "Capture method"),
        "opencli_profile": field(source_text, "OpenCLI profile"),
        "browser_status": field(source_text, "Browser status"),
        "collection_date": field(source_text, "Collection date"),
        "published": field(source_text, "Published"),
        "updated": field(source_text, "Updated"),
        "arxiv_id": field(source_text, "arXiv ID"),
        "doi": field(source_text, "DOI"),
    }


def build_metadata(item_dir, index_row):
    local_id = item_dir.name
    summary_path = item_dir / "summary.md"
    article_path = item_dir / "article.md"
    source_path = item_dir / "source.md"
    raw_dir = item_dir / "raw"
    summary_text = read_text(summary_path)
    source_text = read_text(source_path)
    summary_title = field(summary_text, "Title")
    summary_source = field(summary_text, "Source")
    summary_date = field(summary_text, "Date")
    summary_topic = field(summary_text, "Topic").replace("`", "")
    summary_tags = split_list(field(summary_text, "Tags"))
    summary_blocks = split_list(field(summary_text, "Blocks"))
    source_data = source_fields(source_text)
    all_source_urls = extract_urls(source_text)
    for key in ["source_url", "original_url", "requested_url", "feed_url", "pdf_url", "candidate_url"]:
        if source_data[key] and source_data[key] not in all_source_urls:
            all_source_urls.append(source_data[key])
    all_source_urls = sorted(set(all_source_urls))
    source_id, source_name = infer_source_id(local_id, source_data, summary_source, all_source_urls)

    return {
        "schema_version": 1,
        "id": local_id,
        "type": item_type(local_id, source_id, all_source_urls, source_name or summary_source),
        "date": summary_date or (index_row or {}).get("date", ""),
        "title": summary_title or (index_row or {}).get("title", ""),
        "source": summary_source or (index_row or {}).get("source", ""),
        "topic": summary_topic or (index_row or {}).get("topic", item_dir.parent.name),
        "blocks": summary_blocks or (index_row or {}).get("blocks", []),
        "tags": summary_tags,
        "status": (index_row or {}).get("status", ""),
        "source_id": source_id,
        "source_name": source_name,
        "urls": {
            "source_url": source_data["source_url"],
            "original_url": source_data["original_url"],
            "requested_url": source_data["requested_url"],
            "feed_url": source_data["feed_url"],
            "pdf_url": source_data["pdf_url"],
            "candidate_url": source_data["candidate_url"],
            "all_source_urls": all_source_urls,
        },
        "capture": {
            "collection_date": source_data["collection_date"],
            "capture_method": source_data["capture_method"],
            "opencli_profile": source_data["opencli_profile"],
            "browser_status": source_data["browser_status"],
            "published": source_data["published"],
            "updated": source_data["updated"],
        },
        "candidate": {
            "candidate_id": source_data["candidate_id"],
            "evidence_path": source_data["candidate_evidence_path"],
        },
        "paper": {
            "arxiv_id": source_data["arxiv_id"],
            "doi": source_data["doi"],
        },
        "paths": {
            "item_dir": str(item_dir.relative_to(ROOT)).replace("\\", "/"),
            "summary": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
            "article": str(article_path.relative_to(ROOT)).replace("\\", "/"),
            "source": str(source_path.relative_to(ROOT)).replace("\\", "/"),
            "raw_dir": str(raw_dir.relative_to(ROOT)).replace("\\", "/"),
            "raw_files": raw_files(raw_dir),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Build stable item.json metadata sidecars for knowledge items.")
    parser.add_argument("--ids", nargs="*", help="Optional local item IDs to build.")
    parser.add_argument("--limit", type=int, default=0, help="Optional max items to process.")
    parser.add_argument("--execute", action="store_true", help="Write item.json files. Default is preview only.")
    parser.add_argument("--json", action="store_true", help="Emit full JSON report.")
    args = parser.parse_args()

    index_rows = parse_index()
    item_dirs = list_item_dirs(args.ids)
    if args.limit:
        item_dirs = item_dirs[: args.limit]

    planned = []
    changed = []
    unchanged = []
    missing_index = []
    for item_dir in item_dirs:
        local_id = item_dir.name
        index_row = index_rows.get(local_id)
        if not index_row:
            missing_index.append(local_id)
        metadata = build_metadata(item_dir, index_row)
        out_path = item_dir / "item.json"
        new_text = json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        old_text = read_text(out_path)
        entry = {
            "id": local_id,
            "path": str(out_path.relative_to(ROOT)).replace("\\", "/"),
            "type": metadata["type"],
            "source_id": metadata["source_id"],
            "topic": metadata["topic"],
            "would_change": old_text != new_text,
        }
        planned.append(entry)
        if old_text == new_text:
            unchanged.append(entry)
            continue
        if args.execute:
            write_text(out_path, new_text)
            changed.append(entry)

    report = {
        "execute": args.execute,
        "selected": len(item_dirs),
        "would_change": sum(1 for row in planned if row["would_change"]),
        "changed": len(changed),
        "unchanged": len(unchanged),
        "missing_index": missing_index,
        "planned": planned,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Item metadata build")
        print(f"  Execute: {args.execute}")
        print(f"  Selected: {report['selected']}")
        print(f"  Would change: {report['would_change']}")
        print(f"  Changed: {report['changed']}")
        print(f"  Unchanged: {report['unchanged']}")
        print(f"  Missing index rows: {len(missing_index)}")
        for row in planned[:20]:
            mark = "write" if row["would_change"] else "skip"
            print(f"  - {mark}: {row['id']} [{row['type']}] source={row['source_id']} -> {row['path']}")


if __name__ == "__main__":
    main()
