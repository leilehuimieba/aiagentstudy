import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module():
    script_path = Path(__file__).resolve().parents[1] / "generate-weekly-review.py"
    spec = importlib.util.spec_from_file_location("generate_weekly_review", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GenerateWeeklyReviewTest(unittest.TestCase):
    def test_render_report_summarizes_project_state_and_next_actions(self):
        module = load_module()
        report = {
            "coverage": {
                "total_rows": 592,
                "latest_bestblogs_id": "BB-2026-05-01-573",
                "bestblogs_rows": 561,
                "retrieval_chunks": 6888,
                "candidate_inbox": 39,
            },
            "health": {
                "status": "GREEN",
                "failing_checks": {},
                "accepted_short_articles": 19,
            },
            "candidates": {
                "inbox": 39,
                "promoted": 1,
                "deferred": 1,
                "rejected": 1,
                "top_sources": [("huggingface-papers", 9), ("anthropic-news", 8)],
                "top_topics": [("04-evaluation-guardrails", 22)],
            },
            "source_health": {
                "status_counts": {"active": 9, "backlog": 6, "needs_capture": 4},
                "focus": [
                    {
                        "source_id": "anthropic-news",
                        "status": "backlog",
                        "candidate_inbox": 8,
                        "next_action": ".\\kb.ps1 watch --ids anthropic-news",
                    }
                ],
            },
        }

        markdown = module.render_report(report, "2026-06-18")

        self.assertIn("# Weekly Project Review - 2026-06-18", markdown)
        self.assertIn("Latest BestBlogs ID: `BB-2026-05-01-573`", markdown)
        self.assertIn("Health: `GREEN`", markdown)
        self.assertIn("| huggingface-papers | 9 |", markdown)
        self.assertIn("| anthropic-news | backlog | 8 | `.\\kb.ps1 watch --ids anthropic-news` |", markdown)
        self.assertIn("PROJECT_BOARD.md", markdown)
        self.assertIn("PRODUCT_NOW.md", markdown)

    def test_write_report_uses_product_reports_directory(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = module.write_report(root, "# Report\n", "2026-06-18")

            self.assertEqual(output, root / "product/data/reports/weekly-project-review-2026-06-18.md")
            self.assertEqual(output.read_text(encoding="utf-8"), "# Report\n")

    def test_summarize_candidates_uses_topic_hint(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            inbox = root / "knowledge/candidates/inbox.jsonl"
            inbox.parent.mkdir(parents=True)
            inbox.write_text(
                '{"source_id":"openai-news","topic_hint":"04-evaluation-guardrails"}\n'
                '{"source_id":"anthropic-news","topic_hint":"04-evaluation-guardrails"}\n',
                encoding="utf-8",
            )

            summary = module.summarize_candidates(root)

            self.assertEqual(summary["top_topics"], [("04-evaluation-guardrails", 2)])


if __name__ == "__main__":
    unittest.main()
