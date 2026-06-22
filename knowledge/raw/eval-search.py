import argparse
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVALS = ROOT / "knowledge" / "retrieval" / "evals" / "search-queries.jsonl"
QUERY_SCRIPT = ROOT / "knowledge" / "raw" / "query-kb.py"


def load_cases(path):
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            if not case.get("query") or not case.get("relevant_ids"):
                raise SystemExit(f"Invalid eval case at {path}:{line_no}")
            cases.append(case)
    return cases


def run_query(case, limit):
    cmd = [
        sys.executable,
        str(QUERY_SCRIPT),
        case["query"],
        "--limit",
        str(limit),
        "--json",
    ]
    if case.get("topic"):
        cmd.extend(["--topic", case["topic"]])
    if case.get("profile"):
        cmd.extend(["--profile", case["profile"]])
    if case.get("expand_topic"):
        cmd.append("--expand-topic")
    result = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True)
    return json.loads(result.stdout)


def reciprocal_rank(ids, relevant):
    for index, item_id in enumerate(ids, start=1):
        if item_id in relevant:
            return 1.0 / index
    return 0.0


def dcg(ids, relevant, k):
    score = 0.0
    for index, item_id in enumerate(ids[:k], start=1):
        if item_id in relevant:
            score += 1.0 / math.log2(index + 1)
    return score


def ndcg(ids, relevant, k):
    ideal_hits = min(len(relevant), k)
    if ideal_hits == 0:
        return 0.0
    ideal = sum(1.0 / math.log2(index + 1) for index in range(1, ideal_hits + 1))
    return dcg(ids, relevant, k) / ideal


def main():
    parser = argparse.ArgumentParser(description="Evaluate local knowledge-base retrieval quality.")
    parser.add_argument("--cases", default=str(DEFAULT_EVALS), help="JSONL eval cases")
    parser.add_argument("--limit", type=int, default=10, help="Query limit for each case")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    cases_path = Path(args.cases)
    if not cases_path.is_absolute():
        cases_path = ROOT / cases_path

    cases = load_cases(cases_path)
    details = []
    totals = {"hit@5": 0.0, "recall@10": 0.0, "mrr": 0.0, "ndcg@10": 0.0}

    for case in cases:
        rows = run_query(case, args.limit)
        ids = [row["id"] for row in rows]
        relevant = set(case["relevant_ids"])
        hit_at_5 = 1.0 if any(item_id in relevant for item_id in ids[:5]) else 0.0
        recall_at_10 = len([item_id for item_id in ids[:10] if item_id in relevant]) / len(relevant)
        mrr = reciprocal_rank(ids, relevant)
        ndcg_at_10 = ndcg(ids, relevant, 10)

        detail = {
            "query": case["query"],
            "topic": case.get("topic"),
            "profile": case.get("profile", "standard"),
            "expand_topic": bool(case.get("expand_topic")),
            "relevant_ids": case["relevant_ids"],
            "returned_ids": ids,
            "hit@5": hit_at_5,
            "recall@10": recall_at_10,
            "mrr": mrr,
            "ndcg@10": ndcg_at_10,
        }
        details.append(detail)
        for key, value in (("hit@5", hit_at_5), ("recall@10", recall_at_10), ("mrr", mrr), ("ndcg@10", ndcg_at_10)):
            totals[key] += value

    summary = {
        "cases": len(cases),
        "limit": args.limit,
        "metrics": {key: round(value / len(cases), 4) for key, value in totals.items()},
        "details": details,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    print("Knowledge search eval")
    print(f"Cases: {summary['cases']}")
    print(f"Limit: {summary['limit']}")
    for key, value in summary["metrics"].items():
        print(f"{key}: {value}")
    print("")
    for detail in details:
        print(f"- {detail['query']}")
        if detail.get("topic"):
            suffix = " expanded" if detail.get("expand_topic") else " strict"
            print(f"  topic: {detail['topic']}{suffix}")
        if detail.get("profile") != "standard":
            print(f"  profile: {detail['profile']}")
        print(f"  relevant: {', '.join(detail['relevant_ids'])}")
        print(f"  returned: {', '.join(detail['returned_ids'][:5])}")
        print(
            "  metrics: "
            f"hit@5={detail['hit@5']:.1f}, "
            f"recall@10={detail['recall@10']:.2f}, "
            f"mrr={detail['mrr']:.2f}, "
            f"ndcg@10={detail['ndcg@10']:.2f}"
        )


if __name__ == "__main__":
    main()
