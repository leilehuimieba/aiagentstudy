import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
AUDIT_SCRIPT = REPO_ROOT / "knowledge" / "raw" / "audit-kb.js"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class AuditKbTests(unittest.TestCase):
    def test_reports_duplicate_catalog_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            raw_dir = root / "raw"
            raw_dir.mkdir(parents=True)
            shutil.copy(AUDIT_SCRIPT, raw_dir / "audit-kb.js")

            for name in ["inbox", "promoted", "deferred", "rejected"]:
                write_text(root / "candidates" / f"{name}.jsonl", "")
            write_text(root / "quality" / "article-length-overrides.json", '{"accepted_short_articles": {}}\n')

            item_dir = root / "items" / "04-evaluation-guardrails" / "TEST-2026-001"
            write_text(
                item_dir / "summary.md",
                "\n".join(
                    [
                        "# TEST-2026-001 Summary",
                        "",
                        "- Title: First title",
                        "- Source: Test Source",
                        "",
                    ]
                ),
            )
            write_text(item_dir / "article.md", "x" * 1000)
            write_text(item_dir / "source.md", "- Original publisher URL: https://example.com/first\n")
            write_text(item_dir / "item.json", json.dumps({"id": "TEST-2026-001"}))
            write_text(item_dir / "raw" / "source.json", "{}\n")

            write_text(
                root / "catalog" / "articles-index.md",
                "\n".join(
                    [
                        "# Articles Index",
                        "",
                        "| ID | Date | Title | Source | Topic | Blocks | Status |",
                        "| --- | --- | --- | --- | --- | --- | --- |",
                        "| TEST-2026-001 | 2026-06-18 | First title | Test Source | `04-evaluation-guardrails` | Evaluation | Captured |",
                        "| TEST-2026-001 | 2026-06-18 | Second title | Other Source | `04-evaluation-guardrails` | Evaluation | Captured |",
                        "",
                    ]
                ),
            )

            result = subprocess.run(
                ["node", str(raw_dir / "audit-kb.js")],
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            )
            report = json.loads(result.stdout)

        self.assertEqual(
            [{"id": "TEST-2026-001", "count": 2}],
            report["retrievalSurface"]["duplicateIndexIds"],
        )


if __name__ == "__main__":
    unittest.main()
