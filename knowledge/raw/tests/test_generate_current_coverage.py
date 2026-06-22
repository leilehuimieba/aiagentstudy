import importlib.util
import json
import unittest
from pathlib import Path


def load_module():
    script_path = Path(__file__).resolve().parents[1] / "generate-current-coverage.py"
    spec = importlib.util.spec_from_file_location("generate_current_coverage", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class GenerateCurrentCoverageTest(unittest.TestCase):
    def test_current_coverage_uses_repository_counts(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "knowledge/catalog/articles-index.md",
                "\n".join(
                    [
                        "# Articles Index",
                        "",
                        "| ID | Date | Title | Source | Topic | Blocks | Status |",
                        "| --- | --- | --- | --- | --- | --- | --- |",
                        "| BB-2026-05-01-573 | 06-17 | Latest BestBlogs | BestBlogs / Source | `01-context-memory` | Context/State | Full text + source captured |",
                        "| BB-2026-05-01-001 | 05-01 | First BestBlogs | BestBlogs / Source | `02-tools-actions` | Tools/Actions | Full text + source captured |",
                        "| ARXIV-2026-001 | 2026-06-08 | Paper | arXiv | `04-evaluation-guardrails` | Evaluation | Paper metadata + abstract captured |",
                        "| RSS-2026-001 | 2026-06-05 | RSS | RSS / Blog | `03-control-loop` | Goal | RSS metadata + article text captured |",
                        "| BROWSER-2026-001 | 2026-06-09 | Browser | Browser / Source | `06-frontier-radar` | Model | Browser snapshot captured |",
                    ]
                )
                + "\n",
            )
            write(root / "knowledge/retrieval/fts-report.json", json.dumps({"chunks": 123}))
            write(root / "knowledge/candidates/inbox.jsonl", "{}\n{}\n")
            write(root / "knowledge/candidates/promoted.jsonl", "{}\n")

            module = load_module()
            snapshot = module.collect_snapshot(root)
            markdown = module.render_markdown(snapshot, "2026-06-18")

            self.assertEqual(snapshot["total_rows"], 5)
            self.assertEqual(snapshot["bestblogs_rows"], 2)
            self.assertEqual(snapshot["latest_bestblogs_id"], "BB-2026-05-01-573")
            self.assertEqual(snapshot["candidate_inbox"], 2)
            self.assertIn(
                "| BestBlogs full captures | 2 | Main curated article corpus. Latest ID: `BB-2026-05-01-573`. |",
                markdown,
            )
            self.assertIn(
                "| Retrieval chunks | 123 | SQLite FTS chunks generated from `articles-meta.jsonl`. |",
                markdown,
            )
            self.assertIn("PROJECT_BOARD.md", markdown)
            self.assertNotIn("BB-2026-05-01-514", markdown)
            self.assertNotIn("Total catalog rows | 532", markdown)


if __name__ == "__main__":
    unittest.main()
