import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"
COVERAGE_PATH = ROOT / "knowledge" / "catalog" / "current-coverage.md"
FTS_REPORT_PATH = ROOT / "knowledge" / "retrieval" / "fts-report.json"
CANDIDATES_ROOT = ROOT / "knowledge" / "candidates"


def read_text(path):
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def count_jsonl(path):
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip())


def parse_index_rows(index_text):
    rows = []
    for line in index_text.splitlines():
        if not line.startswith("| "):
            continue
        if line.startswith("| ---") or line.startswith("| ID "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        local_id = cells[0]
        if not re.match(r"^[A-Z][A-Z0-9-]+-", local_id):
            continue
        rows.append(
            {
                "id": local_id,
                "date": cells[1],
                "title": cells[2],
                "source": cells[3],
                "topic": cells[4].strip("`"),
                "blocks": cells[5],
                "status": cells[6],
            }
        )
    return rows


def latest_bestblogs_id(rows):
    nums = []
    for row in rows:
        match = re.match(r"BB-2026-05-01-(\d{3})$", row["id"])
        if match:
            nums.append(int(match.group(1)))
    if not nums:
        return "none"
    return f"BB-2026-05-01-{max(nums):03d}"


def collect_snapshot(root=ROOT):
    index_path = root / "knowledge" / "catalog" / "articles-index.md"
    fts_report_path = root / "knowledge" / "retrieval" / "fts-report.json"
    candidates_root = root / "knowledge" / "candidates"
    rows = parse_index_rows(read_text(index_path))
    by_prefix = Counter(row["id"].split("-", 1)[0] for row in rows)
    topic_counts = Counter(row["topic"] for row in rows if row["topic"])
    fts_report = read_json(fts_report_path)

    return {
        "total_rows": len(rows),
        "bestblogs_rows": by_prefix.get("BB", 0),
        "arxiv_rows": by_prefix.get("ARXIV", 0),
        "rss_rows": by_prefix.get("RSS", 0),
        "browser_rows": by_prefix.get("BROWSER", 0),
        "web_rows": by_prefix.get("WEB", 0),
        "latest_bestblogs_id": latest_bestblogs_id(rows),
        "retrieval_chunks": fts_report.get("chunks", 0),
        "candidate_inbox": count_jsonl(candidates_root / "inbox.jsonl"),
        "candidate_promoted": count_jsonl(candidates_root / "promoted.jsonl"),
        "candidate_deferred": count_jsonl(candidates_root / "deferred.jsonl"),
        "candidate_rejected": count_jsonl(candidates_root / "rejected.jsonl"),
        "topic_counts": dict(sorted(topic_counts.items())),
    }


def render_topic_distribution(topic_counts):
    if not topic_counts:
        return "_No topic rows found._\n"
    lines = ["| Topic | Count |", "| --- | ---: |"]
    for topic, count in topic_counts.items():
        lines.append(f"| `{topic}` | {count} |")
    return "\n".join(lines) + "\n"


def render_markdown(snapshot, organized_date):
    return f"""# Current Knowledge Coverage

Last organized: {organized_date}

Use this page to understand what is already in the AI-agent knowledge base before starting another collection pass.

## Snapshot

| Area | Count | Notes |
| --- | ---: | --- |
| BestBlogs full captures | {snapshot['bestblogs_rows']} | Main curated article corpus. Latest ID: `{snapshot['latest_bestblogs_id']}`. |
| arXiv paper captures | {snapshot['arxiv_rows']} | Paper metadata and abstracts, indexed in `paper-index.md`. |
| RSS article captures | {snapshot['rss_rows']} | Official/engineering/newsletter captures, indexed in `source-article-index.md`. |
| Browser source snapshots | {snapshot['browser_rows']} | OpenCLI Browser Bridge rendered source radar pages. |
| Candidate promotions | {snapshot['web_rows']} | Durable items promoted from candidate radar. |
| Total catalog rows | {snapshot['total_rows']} | Retrieval should be rebuilt after meaningful collection. |
| Retrieval chunks | {snapshot['retrieval_chunks']} | SQLite FTS chunks generated from `articles-meta.jsonl`. |
| Candidate inbox | {snapshot['candidate_inbox']} | Radar candidates waiting for promote/defer/reject review. |

## Candidate Queue

| Bucket | Count |
| --- | ---: |
| inbox | {snapshot['candidate_inbox']} |
| promoted | {snapshot['candidate_promoted']} |
| deferred | {snapshot['candidate_deferred']} |
| rejected | {snapshot['candidate_rejected']} |

## Topic Distribution

{render_topic_distribution(snapshot['topic_counts'])}
## Reading Order

1. Use `articles-index.md` for the complete corpus.
2. Use `paper-index.md` for paper-only lookup.
3. Use `source-article-index.md` for RSS and browser-captured source items.
4. Open only the matching `summary.md` first.
5. Open `article.md` when evidence, exact wording, or deeper reading is needed.

## Capture Routes

| Need | Command |
| --- | --- |
| Latest BestBlogs articles | `.\\kb.ps1 capture --profile qmvqcrb8 --page 1 --page-size 20 --discovery-date {organized_date}` |
| Latest arXiv candidates | `.\\kb.ps1 capture-arxiv --latest-candidates --limit 5` |
| RSS sources | `.\\kb.ps1 capture-rss --ids langchain-blog simon-willison latent-space --limit 5` |
| Browser-rendered source radar | `.\\kb.ps1 capture-browser --ids openai-news jiqizhixin github-trending huggingface-papers --profile qmvqcrb8 --limit 4` |
| Check source health | `.\\kb.ps1 source-health --limit 20` |
| Watch candidate radar | `.\\kb.ps1 watch --limit 20` |
| Rebuild search | `.\\kb.ps1 rebuild` |
| Verify search quality | `.\\kb.ps1 eval` |
| Review project management | `PROJECT_BOARD.md` and `PRODUCT_NOW.md` |

## Current Project Management Notes

- Capture throughput is now strong; synthesis and productization are the bottlenecks.
- Use `PROJECT_BOARD.md` for the radar/capture/synthesis/product workstreams.
- Use `PRODUCT_NOW.md` for the current two-week execution cycle.
- Keep candidate inbox below 50 and promote/defer/reject candidates within 7 days when possible.
- After each meaningful capture batch, run `verify`, `audit`, `rebuild`, and `eval`.

## Known Source Notes

- Browser snapshots are discovery radar, not final article-level evidence.
- Promote important linked articles or papers into deeper items after relevance checks.
- Use `source-health` before adding another source-specific capture path.
- Keep `knowledge/` scoped to AI-agent learning; put unrelated domains under `study_spaces/`.
"""


def main():
    parser = argparse.ArgumentParser(description="Generate knowledge/catalog/current-coverage.md from repository state.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Coverage date to write in the document.")
    parser.add_argument("--write", action="store_true", help="Write knowledge/catalog/current-coverage.md instead of printing.")
    args = parser.parse_args()

    snapshot = collect_snapshot(ROOT)
    markdown = render_markdown(snapshot, args.date)
    if args.write:
        COVERAGE_PATH.write_text(markdown, encoding="utf-8")
        print(f"Wrote {COVERAGE_PATH.relative_to(ROOT)}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
