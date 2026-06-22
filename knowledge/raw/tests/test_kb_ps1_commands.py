import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class KbPs1CommandTest(unittest.TestCase):
    def test_kb_ps1_exposes_coverage_weekly_review_and_obsidian_card_commands(self):
        text = (ROOT / "kb.ps1").read_text(encoding="utf-8-sig")

        self.assertIn('"coverage"', text)
        self.assertIn('"weekly-review"', text)
        self.assertIn('"obsidian-card"', text)
        self.assertIn('generate-current-coverage.py', text)
        self.assertIn('generate-weekly-review.py', text)
        self.assertIn('generate-obsidian-card.py', text)
        self.assertIn('Weekly project review', text)
        self.assertIn('.\\kb.ps1 coverage --write', text)
        self.assertIn('.\\kb.ps1 weekly-review --write', text)
        self.assertIn('.\\kb.ps1 obsidian-card BB-2026-05-01-564', text)
        self.assertIn('--register-existing', text)


if __name__ == "__main__":
    unittest.main()
