import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
QUERY_KB_PATH = ROOT / "knowledge" / "raw" / "query-kb.py"


def load_query_kb():
    spec = importlib.util.spec_from_file_location("query_kb", QUERY_KB_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_text(relative_path):
    path = ROOT / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def extract_urls(text):
    return sorted(set(match.group(0).rstrip(".,):") for match in re.finditer(r"https?://[^\s)]+", text or "")))


def raw_files(raw_dir, limit=12):
    path = ROOT / raw_dir
    if not path.exists() or not path.is_dir():
        return []
    files = []
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            files.append(str(file_path.relative_to(ROOT)).replace("\\", "/"))
        if len(files) >= limit:
            break
    return files


def evidence_record(row):
    source_text = read_text(row["source_path"])
    source_urls = extract_urls(source_text)
    return {
        "id": row["id"],
        "date": row["date"],
        "title": row["title"],
        "source": row["source"],
        "topic": row["topic"],
        "blocks": row.get("blocks") or [],
        "tags": row.get("tags") or [],
        "score": row.get("score"),
        "match_scope": row.get("match_scope", ""),
        "matched_heading": row.get("matched_heading", ""),
        "snippet": row.get("snippet_text", ""),
        "bestblogs_url": row.get("bestblogs_url", ""),
        "original_url": row.get("original_url", ""),
        "source_urls": source_urls,
        "summary_path": row["summary_path"],
        "article_path": row["article_path"],
        "source_path": row["source_path"],
        "raw_dir": str(Path(row["source_path"]).parent / "raw").replace("\\", "/"),
        "raw_files": raw_files(str(Path(row["source_path"]).parent / "raw").replace("\\", "/")),
    }


def select_evidence(query, limit=None, topic=None, expand_topic=False):
    query_kb = load_query_kb()
    resolved_limit, resolved_expand, intent = query_kb.resolve_query_profile(
        "evidence",
        "search",
        query,
        limit,
        expand_topic,
    )
    con = query_kb.connect()
    rows, topics = query_kb.select_rows(con, query, resolved_limit, topic, resolved_expand)
    con.close()
    return [evidence_record(row) for row in rows], topics, intent


def print_text(query, records, topics=None, intent="evidence"):
    print(f"Evidence query: {query}")
    print(f"Query intent: {intent}")
    if topics:
        print(f"Topic filter: {', '.join(topics)}")
    print(f"Hits: {len(records)}")
    print("")
    for index, record in enumerate(records, start=1):
        print(f"{index}. {record['id']} [{record['topic']}] score={record['score']}")
        print(f"   Title: {record['title']}")
        print(f"   Source: {record['source']}")
        if record["blocks"]:
            print(f"   Blocks: {', '.join(record['blocks'])}")
        if record["tags"]:
            print(f"   Tags: {', '.join(record['tags'])}")
        if record["snippet"]:
            print(f"   Match: {record['snippet']}")
        print(f"   Summary: {record['summary_path']}")
        print(f"   Article: {record['article_path']}")
        print(f"   Source Doc: {record['source_path']}")
        print(f"   Raw Dir: {record['raw_dir']}")
        if record["bestblogs_url"]:
            print(f"   BestBlogs URL: {record['bestblogs_url']}")
        if record["original_url"]:
            print(f"   Original URL: {record['original_url']}")
        extra_urls = [
            url
            for url in record["source_urls"]
            if url not in {record["bestblogs_url"], record["original_url"]}
        ]
        if extra_urls:
            print(f"   Other Source URLs: {', '.join(extra_urls[:4])}")
        if record["raw_files"]:
            print(f"   Raw Files: {', '.join(record['raw_files'][:6])}")
        print("")


def main():
    parser = argparse.ArgumentParser(description="Show evidence paths and source links for knowledge hits.")
    parser.add_argument("query", help="Evidence search query")
    parser.add_argument("--limit", type=int, help="Maximum number of hits")
    parser.add_argument("--topic", help="Optional topic directory filter")
    parser.add_argument("--expand-topic", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    records, topics, intent = select_evidence(args.query, args.limit, args.topic, args.expand_topic)
    if args.json:
        print(json.dumps({"query": args.query, "intent": intent, "topics": topics, "hits": records}, ensure_ascii=False, indent=2))
    else:
        print_text(args.query, records, topics, intent)


if __name__ == "__main__":
    main()
