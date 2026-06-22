import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "knowledge" / "sources" / "source-registry.json"
ITEMS_ROOT = ROOT / "knowledge" / "items"
CANDIDATES_ROOT = ROOT / "knowledge" / "candidates"
PROBES_ROOT = ROOT / "knowledge" / "sources" / "opencli-probes"


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def read_json(path):
    return json.loads(read_text(path))


def read_jsonl(path):
    if not path.exists():
        return []
    rows = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def field(text, label):
    return (re.search(rf"^- {re.escape(label)}: (.+)$", text, re.M) or ["", ""])[1].strip()


def load_sources():
    registry = read_json(REGISTRY_PATH)
    sources = []
    for group in registry.get("groups", []):
        for source in group.get("sources", []):
            row = dict(source)
            row["group_id"] = group.get("id", "")
            row["group_name"] = group.get("name", "")
            row["group_priority"] = group.get("priority", 99)
            sources.append(row)
    return sources, registry


def item_stats():
    stats = defaultdict(lambda: {"items": 0, "browser_snapshots": 0, "rss_items": 0, "candidate_promotions": 0, "latest_collection_date": ""})
    for item_json_path in ITEMS_ROOT.glob("**/item.json"):
        try:
            metadata = read_json(item_json_path)
        except json.JSONDecodeError:
            continue
        local_id = metadata.get("id") or item_json_path.parent.name
        source_id = metadata.get("source_id", "")
        if not source_id:
            continue
        item_type = metadata.get("type", "")
        row = stats[source_id]
        row["items"] += 1
        if item_type == "browser_snapshot" or local_id.startswith("BROWSER-"):
            row["browser_snapshots"] += 1
        if item_type == "rss_article" or local_id.startswith("RSS-"):
            row["rss_items"] += 1
        if local_id.startswith(("WEB-", "PAPER-", "PRODUCT-", "REPO-")):
            row["candidate_promotions"] += 1
        collection_date = (metadata.get("capture") or {}).get("collection_date", "")
        if collection_date and collection_date > row["latest_collection_date"]:
            row["latest_collection_date"] = collection_date
    return stats


def candidate_stats():
    stats = defaultdict(Counter)
    for bucket in ["inbox", "promoted", "deferred", "rejected"]:
        for row in read_jsonl(CANDIDATES_ROOT / f"{bucket}.jsonl"):
            source_id = row.get("source_id", "")
            if source_id:
                stats[source_id][bucket] += 1
    return stats


def probe_stats():
    latest = {}
    if not PROBES_ROOT.exists():
        return latest
    for probe_path in sorted(PROBES_ROOT.glob("source-probe-*.json")):
        try:
            probe = read_json(probe_path)
        except json.JSONDecodeError:
            continue
        generated_at = probe.get("generated_at", "")
        for result in probe.get("results", []):
            source_id = result.get("source_id", "")
            if not source_id:
                continue
            current = latest.get(source_id)
            if current and current.get("generated_at", "") >= generated_at:
                continue
            latest[source_id] = {
                "generated_at": generated_at,
                "profile": probe.get("profile", ""),
                "status": result.get("status", ""),
                "requested_url": result.get("requested_url", ""),
                "final_url": ((result.get("eval") or {}).get("page_state") or {}).get("url", ""),
                "text_length": ((result.get("eval") or {}).get("page_state") or {}).get("textLength", 0),
                "probe_path": str(probe_path.relative_to(ROOT)).replace("\\", "/"),
            }
    return latest


def health_status(source, item_row, candidate_row, probe_row):
    inbox = candidate_row.get("inbox", 0)
    if inbox:
        return "backlog"
    if probe_row and probe_row.get("status") and probe_row.get("status") != "browser_readable":
        return "probe_attention"
    if item_row.get("items", 0) or (probe_row and probe_row.get("status") == "browser_readable"):
        return "active"
    if source.get("rss") or source.get("api"):
        return "needs_capture"
    return "unseen"


def next_action(source, status, item_row, candidate_row, probe_row):
    if status == "backlog":
        return f"review candidates: .\\kb.ps1 watch --ids {source['id']}"
    if status == "probe_attention":
        return f"retry probe or use browser capture: .\\kb.ps1 probe-sources --ids {source['id']}"
    if status == "needs_capture":
        if source.get("rss"):
            return f"try RSS capture: .\\kb.ps1 capture-rss --ids {source['id']} --limit 3"
        if source.get("api") or "api" in source.get("capture_route", ""):
            return f"try API route: .\\kb.ps1 capture-arxiv or source-specific capture for {source['id']}"
    if source.get("browser_needed") and not probe_row:
        return f"probe browser route: .\\kb.ps1 probe-sources --ids {source['id']} --profile qmvqcrb8"
    if not item_row.get("items", 0):
        return f"consider capture route: {source.get('capture_route', '')}"
    return "monitor"


def build_report(ids=None):
    sources, registry = load_sources()
    allowed = set(ids or [])
    items = item_stats()
    candidates = candidate_stats()
    probes = probe_stats()
    rows = []
    for source in sources:
        if allowed and source["id"] not in allowed:
            continue
        item_row = items[source["id"]]
        candidate_row = candidates[source["id"]]
        probe_row = probes.get(source["id"], {})
        status = health_status(source, item_row, candidate_row, probe_row)
        rows.append(
            {
                "source_id": source["id"],
                "name": source.get("name", source["id"]),
                "group_id": source.get("group_id", ""),
                "priority": source.get("group_priority", 99),
                "capture_route": source.get("capture_route", ""),
                "browser_needed": bool(source.get("browser_needed")),
                "has_rss": bool(source.get("rss")),
                "has_api": bool(source.get("api")),
                "status": status,
                "items": item_row.get("items", 0),
                "browser_snapshots": item_row.get("browser_snapshots", 0),
                "rss_items": item_row.get("rss_items", 0),
                "candidate_promotions": item_row.get("candidate_promotions", 0),
                "candidate_inbox": candidate_row.get("inbox", 0),
                "candidate_promoted": candidate_row.get("promoted", 0),
                "candidate_deferred": candidate_row.get("deferred", 0),
                "candidate_rejected": candidate_row.get("rejected", 0),
                "latest_collection_date": item_row.get("latest_collection_date", ""),
                "latest_probe": probe_row,
                "next_action": next_action(source, status, item_row, candidate_row, probe_row),
            }
        )
    status_counts = Counter(row["status"] for row in rows)
    rows.sort(key=lambda row: (row["priority"], row["status"] == "unseen", -row["candidate_inbox"], -row["items"], row["source_id"]))
    return {
        "generated_from": str(REGISTRY_PATH.relative_to(ROOT)).replace("\\", "/"),
        "default_browser_profile": registry.get("default_browser_profile", "qmvqcrb8"),
        "source_count": len(rows),
        "status_counts": dict(status_counts),
        "sources": rows,
    }


def print_text(report, limit):
    print("Source health")
    print(f"  Sources: {report['source_count']}")
    print(f"  Default browser profile: {report['default_browser_profile']}")
    if report["status_counts"]:
        print("  Status counts: " + ", ".join(f"{key}={value}" for key, value in sorted(report["status_counts"].items())))
    print("")
    for row in report["sources"][:limit]:
        probe = row.get("latest_probe") or {}
        print(f"- {row['source_id']} [{row['status']}] {row['name']}")
        print(f"  Group: {row['group_id']} | Route: {row['capture_route']} | Browser: {row['browser_needed']}")
        print(
            "  Items: {items} | RSS: {rss_items} | Browser snapshots: {browser_snapshots} | Candidate promotions: {candidate_promotions}".format(
                **row
            )
        )
        print(
            "  Candidates: inbox={candidate_inbox}, promoted={candidate_promoted}, deferred={candidate_deferred}, rejected={candidate_rejected}".format(
                **row
            )
        )
        if row["latest_collection_date"]:
            print(f"  Latest collection: {row['latest_collection_date']}")
        if probe:
            print(f"  Latest probe: {probe.get('status')} at {probe.get('generated_at')} text={probe.get('text_length')} path={probe.get('probe_path')}")
        print(f"  Next: {row['next_action']}")
        print("")


def main():
    parser = argparse.ArgumentParser(description="Summarize local source coverage, backlog, and probe health.")
    parser.add_argument("--ids", nargs="*", help="Optional source IDs to show.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report(args.ids)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report, args.limit)


if __name__ == "__main__":
    main()
