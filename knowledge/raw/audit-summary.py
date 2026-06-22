import argparse
import json
import subprocess
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = ROOT / "knowledge" / "raw" / "audit-kb.js"
BUILD_REPORT_PATH = ROOT / "knowledge" / "retrieval" / "build-report.json"
FTS_REPORT_PATH = ROOT / "knowledge" / "retrieval" / "fts-report.json"


def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run_audit():
    result = subprocess.run(
        ["node", str(AUDIT_PATH.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def count(value):
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return sum(count(item) for item in value.values())
    if isinstance(value, int):
        return value
    return 0


def candidate_file_count(audit, name):
    return audit.get("candidates", {}).get("files", {}).get(name, 0)


def build_summary(audit):
    build_report = read_json(BUILD_REPORT_PATH)
    fts_report = read_json(FTS_REPORT_PATH)
    missing = audit.get("missing", {})
    invalid = audit.get("invalid", {})
    size = audit.get("size", {})
    quality = audit.get("quality", {})
    source_issues = audit.get("sourceIssues", {})
    placeholder_loss = audit.get("placeholderLoss", {})
    retrieval_surface = audit.get("retrievalSurface", {})
    candidates = audit.get("candidates", {})

    checks = {
        "missing_files": count(missing),
        "invalid_item_json": count(invalid.get("itemJson", [])),
        "unresolved_short_articles": count(size.get("articleUnder800", [])),
        "source_issues": count(source_issues),
        "placeholder_loss": count(placeholder_loss),
        "summary_index_mismatches": count(retrieval_surface.get("summaryVsIndexMismatches", [])),
        "candidate_errors": candidates.get("errorCount", 0),
        "quality_override_errors": count(quality.get("articleLengthOverrideErrors", [])),
        "unused_quality_overrides": count(quality.get("unusedArticleLengthOverrides", [])),
    }
    failing = {key: value for key, value in checks.items() if value}
    status = "GREEN" if not failing else "RED"

    return {
        "status": status,
        "failing_checks": failing,
        "checks": checks,
        "totals": audit.get("totals", {}),
        "retrieval": {
            "items": build_report.get("items"),
            "generated_at": build_report.get("generated_at"),
            "chunks": fts_report.get("chunks"),
        },
        "accepted_exceptions": {
            "short_articles": count(size.get("articleUnder800Accepted", [])),
        },
        "candidates": {
            "inbox": candidate_file_count(audit, "inbox.jsonl"),
            "promoted": candidate_file_count(audit, "promoted.jsonl"),
            "deferred": candidate_file_count(audit, "deferred.jsonl"),
            "rejected": candidate_file_count(audit, "rejected.jsonl"),
            "errors": candidates.get("errorCount", 0),
        },
    }


def print_text(summary):
    status = summary["status"]
    symbol = "OK" if status == "GREEN" else "FAIL"
    print(f"Knowledge base health: {status} ({symbol})")
    totals = summary["totals"]
    retrieval = summary["retrieval"]
    print(f"  Items: {totals.get('items', 0)} | Catalog rows: {totals.get('indexRows', 0)}")
    print(
        "  Retrieval: {items} items | {chunks} chunks | generated_at={generated_at}".format(
            items=retrieval.get("items", "n/a"),
            chunks=retrieval.get("chunks", "n/a"),
            generated_at=retrieval.get("generated_at", "n/a"),
        )
    )
    print("")
    print("Blocking checks:")
    if summary["failing_checks"]:
        for key, value in summary["failing_checks"].items():
            print(f"  - {key}: {value}")
    else:
        print("  - none")
    print("")
    accepted = summary["accepted_exceptions"]
    print("Accepted exceptions:")
    print(f"  - short_articles: {accepted['short_articles']}")
    print("")
    candidates = summary["candidates"]
    print(
        "Candidates: inbox={inbox}, promoted={promoted}, deferred={deferred}, rejected={rejected}, errors={errors}".format(
            **candidates
        )
    )
    if summary["status"] == "GREEN" and candidates["inbox"]:
        print(f"Next review queue: .\\kb.ps1 watch --limit {min(candidates['inbox'], 20)}")


def main():
    parser = argparse.ArgumentParser(description="Print a compact health summary for the knowledge base.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    audit = run_audit()
    summary = build_summary(audit)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_text(summary)


if __name__ == "__main__":
    main()
