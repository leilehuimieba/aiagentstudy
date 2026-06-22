import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module():
    script_path = Path(__file__).resolve().parents[1] / "generate-obsidian-card.py"
    spec = importlib.util.spec_from_file_location("generate_obsidian_card", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


SUMMARY = """# BB-2026-05-01-999 Summary

## Article

- Title: How to Build a Production-Safe Agent Loop: From Exit Conditions to Audit Trails
- Source: BestBlogs / freeCodeCamp
- URL: https://www.bestblogs.dev/article/example
- Date: 06-16
- Topic: `03-control-loop`
- Tags: AI Agent, LLM, Production AI

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article argues that production agent safety comes from explicit exit conditions, budget limits, append-only audit logs, and human review gates. It reframes agent reliability as an engineering discipline rather than model trust.

## Reusable Principle

Use the catalog and this summary as the low-token entry point.
"""


SOURCE = """# Source Evidence

- Title: How to Build a Production-Safe Agent Loop: From Exit Conditions to Audit Trails
- BestBlogs URL: https://www.bestblogs.dev/article/example
- Original publisher URL: https://www.freecodecamp.org/news/example/
- BestBlogs source label: freeCodeCamp
- Publish time: 2026-06-16 07:18:49
- Language: English
- Score: 90
- Word count: 3321
"""


class GenerateObsidianCardTest(unittest.TestCase):
    def test_load_item_reads_summary_and_source_fields(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)

            item = module.load_item(root, "BB-2026-05-01-999")

            self.assertEqual(item["id"], "BB-2026-05-01-999")
            self.assertEqual(item["title"], "How to Build a Production-Safe Agent Loop: From Exit Conditions to Audit Trails")
            self.assertEqual(item["topic"], "03-control-loop")
            self.assertEqual(item["bestblogs_url"], "https://www.bestblogs.dev/article/example")
            self.assertEqual(item["original_url"], "https://www.freecodecamp.org/news/example/")
            self.assertIn("explicit exit conditions", item["core_takeaway"])

    def test_render_card_includes_reusable_sections_and_evidence(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)
            item = module.load_item(root, "BB-2026-05-01-999")

            markdown = module.render_card(item, "2026-06-18")

            self.assertIn("title: How to Build a Production-Safe Agent Loop", markdown)
            self.assertIn("kb_id: BB-2026-05-01-999", markdown)
            self.assertIn("## 一句话结论", markdown)
            self.assertIn("## 原文摘要", markdown)
            self.assertIn("## 待整理成个人理解", markdown)
            self.assertIn("https://www.bestblogs.dev/article/example", markdown)
            self.assertIn("https://www.freecodecamp.org/news/example/", markdown)
            self.assertIn("knowledge\\items\\03-control-loop\\BB-2026-05-01-999", markdown)

    def test_write_card_uses_topic_mapping_and_safe_filename(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)
            item = module.load_item(root, "BB-2026-05-01-999")

            output = module.write_card(root, vault, item, "2026-06-18", module_alias=None)

            self.assertEqual(
                output,
                vault / "学习笔记/AI-Agent/03-控制循环与编排/2026-06-18-How to Build a Production-Safe Agent Loop.md",
            )
            self.assertIn("BB-2026-05-01-999", output.read_text(encoding="utf-8"))

    def test_write_card_registers_generated_card_and_renders_catalog_index(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)
            item = module.load_item(root, "BB-2026-05-01-999")

            output = module.write_card(root, vault, item, "2026-06-18", module_alias="control-loop")

            registry_path = root / "knowledge/obsidian/cards-index.jsonl"
            markdown_path = root / "knowledge/catalog/obsidian-card-index.md"
            records = [json.loads(line) for line in registry_path.read_text(encoding="utf-8").splitlines()]
            markdown = markdown_path.read_text(encoding="utf-8")

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["kb_id"], "BB-2026-05-01-999")
            self.assertEqual(records[0]["module"], "control-loop")
            self.assertEqual(records[0]["topic"], "03-control-loop")
            self.assertEqual(records[0]["obsidian_path"], str(output))
            self.assertIn("| BB-2026-05-01-999 | 2026-06-18 |", markdown)
            self.assertIn("[How to Build a Production-Safe Agent Loop", markdown)
            self.assertIn("control-loop", markdown)

    def test_write_card_rejects_duplicate_registry_entries_without_force(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)
            item = module.load_item(root, "BB-2026-05-01-999")

            module.write_card(root, vault, item, "2026-06-18", module_alias="control-loop")

            with self.assertRaises(module.DuplicateCardError):
                module.write_card(root, vault, item, "2026-06-18", module_alias="control-loop")

    def test_write_card_allows_duplicate_when_force_is_true(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)
            item = module.load_item(root, "BB-2026-05-01-999")

            first = module.write_card(root, vault, item, "2026-06-18", module_alias="control-loop")
            second = module.write_card(root, vault, item, "2026-06-19", module_alias="control-loop", force=True)
            records = module.load_registry(root)

            self.assertEqual(len(records), 2)
            self.assertNotEqual(first, second)
            self.assertEqual(records[1]["date"], "2026-06-19")

    def test_register_existing_card_records_path_without_overwriting_file(self):
        module = load_module()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            item_dir = root / "knowledge/items/03-control-loop/BB-2026-05-01-999"
            write(item_dir / "summary.md", SUMMARY)
            write(item_dir / "source.md", SOURCE)
            existing_card = vault / "学习笔记/AI-Agent/03-控制循环与编排/curated-card.md"
            write(existing_card, "# Human curated card\n")
            item = module.load_item(root, "BB-2026-05-01-999")

            output = module.register_existing_card(root, item, existing_card, "2026-06-18", "control-loop")
            records = module.load_registry(root)

            self.assertEqual(output, existing_card)
            self.assertEqual(existing_card.read_text(encoding="utf-8"), "# Human curated card\n")
            self.assertEqual(records[0]["obsidian_path"], str(existing_card))
            self.assertEqual(records[0]["module"], "control-loop")


if __name__ == "__main__":
    unittest.main()
