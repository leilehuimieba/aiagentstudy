import argparse
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = ROOT / "knowledge" / "raw"
CANDIDATES_ROOT = ROOT / "knowledge" / "candidates"


def load_script(filename, module_name):
    script_path = RAW_ROOT / filename
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_jsonl(path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def run_json_command(args):
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def summarize_candidates(root=ROOT):
    candidates_root = root / "knowledge" / "candidates"
    buckets = {}
    inbox = read_jsonl(candidates_root / "inbox.jsonl")
    for name in ["inbox", "promoted", "deferred", "rejected"]:
        buckets[name] = len(read_jsonl(candidates_root / f"{name}.jsonl"))
    return {
        **buckets,
        "top_sources": Counter(row.get("source_id", "") for row in inbox if row.get("source_id")).most_common(5),
        "top_topics": Counter((row.get("topic") or row.get("topic_hint") or "") for row in inbox if (row.get("topic") or row.get("topic_hint"))).most_common(5),
    }


def collect_report(root=ROOT, include_eval=False):
    coverage_module = load_script("generate-current-coverage.py", "generate_current_coverage")
    coverage = coverage_module.collect_snapshot(root)
    health = run_json_command(["python", "knowledge/raw/audit-summary.py", "--json"])
    source_health = run_json_command(["python", "knowledge/raw/source-health.py", "--json"])
    focus = []
    for row in source_health.get("sources", [])[:10]:
        focus.append(
            {
                "source_id": row.get("source_id", ""),
                "status": row.get("status", ""),
                "candidate_inbox": row.get("candidate_inbox", 0),
                "next_action": row.get("next_action", ""),
            }
        )
    report = {
        "coverage": coverage,
        "health": {
            "status": health.get("status", "UNKNOWN"),
            "failing_checks": health.get("failing_checks", {}),
            "accepted_short_articles": (health.get("accepted_exceptions") or {}).get("short_articles", 0),
        },
        "candidates": summarize_candidates(root),
        "source_health": {
            "status_counts": source_health.get("status_counts", {}),
            "focus": focus,
        },
    }
    if include_eval:
        result = subprocess.run(
            ["python", "knowledge/raw/eval-search.py"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=True,
        )
        report["eval_output"] = "\n".join(result.stdout.splitlines()[:8])
    return report


def table_from_pairs(pairs, empty_label):
    if not pairs:
        return f"_No {empty_label}._\n"
    lines = ["| Name | Count |", "| --- | ---: |"]
    for name, count in pairs:
        lines.append(f"| {name} | {count} |")
    return "\n".join(lines) + "\n"


def render_report(report, review_date):
    coverage = report["coverage"]
    health = report["health"]
    candidates = report["candidates"]
    source_health = report["source_health"]
    source_status = ", ".join(f"{key}={value}" for key, value in sorted(source_health.get("status_counts", {}).items())) or "none"

    focus_lines = ["| Source | Status | Inbox | Next action |", "| --- | --- | ---: | --- |"]
    for row in source_health.get("focus", []):
        focus_lines.append(
            "| {source_id} | {status} | {candidate_inbox} | `{next_action}` |".format(**row)
        )

    failing = health.get("failing_checks") or {}
    failing_text = "none" if not failing else ", ".join(f"{key}={value}" for key, value in sorted(failing.items()))
    eval_section = ""
    if report.get("eval_output"):
        eval_section = f"""
## Search Eval

```text
{report['eval_output']}
```
"""

    return f"""# Weekly Project Review - {review_date}

## Snapshot

- Catalog rows: {coverage['total_rows']}
- BestBlogs rows: {coverage['bestblogs_rows']}
- Latest BestBlogs ID: `{coverage['latest_bestblogs_id']}`
- Retrieval chunks: {coverage['retrieval_chunks']}
- Candidate inbox: {coverage['candidate_inbox']}
- Health: `{health['status']}`
- Blocking checks: {failing_text}
- Accepted short-article exceptions: {health.get('accepted_short_articles', 0)}

## Candidate Queue

| Bucket | Count |
| --- | ---: |
| inbox | {candidates.get('inbox', 0)} |
| promoted | {candidates.get('promoted', 0)} |
| deferred | {candidates.get('deferred', 0)} |
| rejected | {candidates.get('rejected', 0)} |

### Top Candidate Sources

{table_from_pairs(candidates.get('top_sources', []), 'candidate sources')}
### Top Candidate Topics

{table_from_pairs(candidates.get('top_topics', []), 'candidate topics')}
## Source Health Focus

Status counts: {source_status}

{chr(10).join(focus_lines)}
{eval_section}
## Next Actions

1. Keep candidate inbox at or below 50.
2. Promote, defer, or reject the oldest/highest-value candidate batch.
3. Update at least one topic brief before the next capture batch.
4. Refresh coverage after meaningful capture work: `.\\kb.ps1 coverage --write`.

## Management Files

- `PROJECT_BOARD.md`
- `PRODUCT_NOW.md`
- `knowledge/catalog/current-coverage.md`
"""


def write_report(root, markdown, review_date):
    output = root / "product" / "data" / "reports" / f"weekly-project-review-{review_date}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description="Generate a durable weekly project review report.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Review date for the report filename and title.")
    parser.add_argument("--write", action="store_true", help="Write the report under product/data/reports.")
    parser.add_argument("--eval", action="store_true", help="Include the slower search eval summary.")
    args = parser.parse_args()

    report = collect_report(ROOT, include_eval=args.eval)
    markdown = render_report(report, args.date)
    if args.write:
        output = write_report(ROOT, markdown, args.date)
        print(f"Wrote {output.relative_to(ROOT)}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
