import argparse
import importlib.util
import json
import sys
from collections import Counter
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


def select_rows(query, limit=None, topic=None, expand_topic=False):
    query_kb = load_query_kb()
    resolved_limit, resolved_expand, intent = query_kb.resolve_query_profile(
        "brief",
        "search",
        query,
        limit,
        expand_topic,
    )
    con = query_kb.connect()
    rows, topics = query_kb.select_rows(con, query, resolved_limit, topic, resolved_expand)
    con.close()
    return rows, topics, intent


def top_counts(rows, field, limit=8):
    counter = Counter()
    for row in rows:
        value = row.get(field)
        if isinstance(value, list):
            counter.update(item for item in value if item)
        elif value:
            counter.update([value])
    return counter.most_common(limit)


def brief_record(row):
    return {
        "id": row["id"],
        "date": row["date"],
        "title": row["title"],
        "source": row["source"],
        "topic": row["topic"],
        "blocks": row.get("blocks") or [],
        "tags": row.get("tags") or [],
        "takeaway": row.get("takeaway") or "",
        "reusable_principle": row.get("reusable_principle") or "",
        "summary_path": row["summary_path"],
        "article_path": row["article_path"],
        "source_path": row["source_path"],
        "score": row.get("score"),
    }


def make_brief(query, rows, topics, intent):
    records = [brief_record(row) for row in rows]
    return {
        "query": query,
        "intent": intent,
        "topics": topics or [],
        "hits": len(records),
        "topic_counts": top_counts(records, "topic"),
        "block_counts": top_counts(records, "blocks"),
        "tag_counts": top_counts(records, "tags"),
        "reading_order": records,
    }


def print_text(brief):
    print(f"Brief query: {brief['query']}")
    print(f"Query intent: {brief['intent']}")
    if brief["topics"]:
        print(f"Topic filter: {', '.join(brief['topics'])}")
    print(f"Hits: {brief['hits']}")
    print("")
    if brief["topic_counts"]:
        print("Topic mix:")
        print("  " + ", ".join(f"{name} ({count})" for name, count in brief["topic_counts"]))
    if brief["block_counts"]:
        print("Agent blocks:")
        print("  " + ", ".join(f"{name} ({count})" for name, count in brief["block_counts"][:6]))
    if brief["tag_counts"]:
        print("Frequent tags:")
        print("  " + ", ".join(f"{name} ({count})" for name, count in brief["tag_counts"][:8]))
    print("")
    print("Reading order:")
    for index, row in enumerate(brief["reading_order"], start=1):
        print(f"{index}. {row['id']} [{row['topic']}] score={row['score']}")
        print(f"   Title: {row['title']}")
        print(f"   Source: {row['source']}")
        if row["takeaway"]:
            print(f"   Takeaway: {row['takeaway']}")
        if row["reusable_principle"]:
            print(f"   Principle: {row['reusable_principle']}")
        print(f"   Summary: {row['summary_path']}")
        print(f"   Evidence: {row['source_path']}")
        print("")


def main():
    parser = argparse.ArgumentParser(description="Show a human-readable topic brief from knowledge hits.")
    parser.add_argument("query", help="Brief query")
    parser.add_argument("--limit", type=int, help="Maximum number of hits")
    parser.add_argument("--topic", help="Optional topic directory filter")
    parser.add_argument("--expand-topic", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows, topics, intent = select_rows(args.query, args.limit, args.topic, args.expand_topic)
    brief = make_brief(args.query, rows, topics, intent)
    if args.json:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    else:
        print_text(brief)


if __name__ == "__main__":
    main()
