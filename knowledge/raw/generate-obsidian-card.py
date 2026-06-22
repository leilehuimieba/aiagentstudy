from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VAULT_ROOT = Path(r"D:\webstudy\Notes\obsidian\黑曜石")


MODULE_PATHS = {
    "01-context-memory": Path("学习笔记/AI-Agent/01-上下文与记忆"),
    "02-tools-actions": Path("学习笔记/AI-Agent/02-工具调用与动作"),
    "03-control-loop": Path("学习笔记/AI-Agent/03-控制循环与编排"),
    "04-evaluation-guardrails": Path("学习笔记/AI-Agent/04-评估与护栏"),
    "06-frontier-radar": Path("学习笔记/AI-Agent/06-前沿模型与产品雷达"),
    "context": Path("学习笔记/AI-Agent/01-上下文与记忆"),
    "tools": Path("学习笔记/AI-Agent/02-工具调用与动作"),
    "control-loop": Path("学习笔记/AI-Agent/03-控制循环与编排"),
    "eval": Path("学习笔记/AI-Agent/04-评估与护栏"),
    "security": Path("学习笔记/AI-Agent/05-Agent安全"),
    "frontier": Path("学习笔记/AI-Agent/06-前沿模型与产品雷达"),
    "project": Path("学习笔记/AI-Agent/90-项目方法论"),
    "workflow": Path("学习笔记/AI-Agent/91-提示词与工作流"),
    "case": Path("学习笔记/AI-Agent/92-案例拆解"),
    "reading": Path("学习笔记/AI-Agent/99-阅读记录"),
}


class DuplicateCardError(RuntimeError):
    pass


def find_item_dir(root: Path, item_id: str) -> Path:
    items_root = root / "knowledge" / "items"
    matches = sorted(items_root.glob(f"*/{item_id}"))
    if not matches:
        raise FileNotFoundError(f"Item not found under knowledge/items: {item_id}")
    return matches[0]


def parse_bullet_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^- ([^:]+):\s*(.*)$", line.strip())
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip().strip("`")
            fields[key] = value
    return fields


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def first_sentence(text: str) -> str:
    compact = " ".join(text.split())
    if not compact:
        return "待补充。"
    match = re.search(r"(.+?[.!?。！？])\s", compact + " ")
    if match:
        return match.group(1).strip()
    return compact[:180].rstrip()


def split_tags(value: str) -> list[str]:
    return [tag.strip() for tag in value.split(",") if tag.strip()]


def load_item(root: Path, item_id: str) -> dict:
    item_dir = find_item_dir(root, item_id)
    summary_path = item_dir / "summary.md"
    source_path = item_dir / "source.md"
    summary = summary_path.read_text(encoding="utf-8")
    source = source_path.read_text(encoding="utf-8") if source_path.exists() else ""

    summary_fields = parse_bullet_fields(summary)
    source_fields = parse_bullet_fields(source)
    core_takeaway = extract_section(summary, "Core Takeaway")

    return {
        "id": item_id,
        "item_dir": item_dir,
        "title": summary_fields.get("title") or source_fields.get("title") or item_id,
        "source": summary_fields.get("source") or source_fields.get("bestblogs source label") or "",
        "summary_url": summary_fields.get("url", ""),
        "date": summary_fields.get("date", ""),
        "topic": summary_fields.get("topic", item_dir.parent.name).strip("`"),
        "tags": split_tags(summary_fields.get("tags", "")),
        "blocks": summary_fields.get("blocks", ""),
        "core_takeaway": core_takeaway,
        "bestblogs_url": source_fields.get("bestblogs url") or summary_fields.get("url", ""),
        "original_url": source_fields.get("original publisher url", ""),
        "source_label": source_fields.get("bestblogs source label", ""),
        "word_count": source_fields.get("word count", ""),
    }


def frontmatter_tags(item: dict) -> str:
    tags = ["AI-Agent"]
    for tag in item.get("tags", []):
        cleaned = re.sub(r"\s+", "", tag)
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
    return "[" + ", ".join(tags[:8]) + "]"


def relative_item_path(item: dict) -> str:
    try:
        return str(item["item_dir"].relative_to(ROOT)).replace("/", "\\")
    except ValueError:
        return str(item["item_dir"]).replace("/", "\\")


def render_card(item: dict, card_date: str) -> str:
    title = item["title"]
    takeaway = item.get("core_takeaway", "")
    local_path = relative_item_path(item)
    original_url = item.get("original_url") or "未记录"
    bestblogs_url = item.get("bestblogs_url") or item.get("summary_url") or "未记录"

    return f"""---
title: {title}
date: {card_date}
source: BestBlogs
kb_id: {item["id"]}
tags: {frontmatter_tags(item)}
---

# {title}

## 一句话结论

{first_sentence(takeaway)}

## 原文摘要

{takeaway or "待补充。"}

## 待整理成个人理解

- 这篇解决了什么问题：
- 它属于 Agent 模型的哪一层：
- 可以复用到我的哪个项目：
- 需要补充验证的点：

## Agent 模型映射

- Topic: `{item.get("topic", "")}`
- Blocks: {item.get("blocks", "") or "待补充"}
- Source: {item.get("source", "") or item.get("source_label", "") or "待补充"}

## 关联笔记

- [[00-模块索引]]

## 来源

- BestBlogs: {bestblogs_url}
- 原文: {original_url}
- 本地知识库: `{local_path}`
"""


def safe_filename_title(title: str) -> str:
    title = title.split(":", 1)[0]
    title = re.sub(r'[<>:"/\\|?*]', "", title)
    title = re.sub(r"\s+", " ", title).strip().rstrip(".")
    if len(title) > 80:
        title = title[:80].rstrip()
    return title or "untitled"


def module_path_for(item: dict, module_alias: str | None) -> Path:
    key = module_alias or item.get("topic") or "reading"
    if key not in MODULE_PATHS:
        raise ValueError(f"Unknown module alias: {key}")
    return MODULE_PATHS[key]


def write_card(
    root: Path,
    vault_root: Path,
    item: dict,
    card_date: str,
    module_alias: str | None = None,
    force: bool = False,
) -> Path:
    existing = find_registry_records(root, item["id"])
    if existing and not force:
        paths = ", ".join(record.get("obsidian_path", "") for record in existing)
        raise DuplicateCardError(f"Obsidian card already registered for {item['id']}: {paths}")

    output_dir = vault_root / module_path_for(item, module_alias)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{card_date}-{safe_filename_title(item['title'])}.md"
    output.write_text(render_card(item, card_date), encoding="utf-8")
    append_registry_record(root, item, output, card_date, module_alias)
    return output


def register_existing_card(
    root: Path,
    item: dict,
    obsidian_path: Path,
    card_date: str,
    module_alias: str | None = None,
    force: bool = False,
) -> Path:
    if not obsidian_path.exists():
        raise FileNotFoundError(f"Existing Obsidian card not found: {obsidian_path}")
    existing = find_registry_records(root, item["id"])
    if existing and not force:
        paths = ", ".join(record.get("obsidian_path", "") for record in existing)
        raise DuplicateCardError(f"Obsidian card already registered for {item['id']}: {paths}")
    append_registry_record(root, item, obsidian_path, card_date, module_alias)
    return obsidian_path


def registry_path(root: Path) -> Path:
    return root / "knowledge" / "obsidian" / "cards-index.jsonl"


def registry_markdown_path(root: Path) -> Path:
    return root / "knowledge" / "catalog" / "obsidian-card-index.md"


def load_registry(root: Path) -> list[dict]:
    path = registry_path(root)
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def find_registry_records(root: Path, item_id: str) -> list[dict]:
    return [record for record in load_registry(root) if record.get("kb_id") == item_id]


def escape_table_cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ").strip()


def render_registry_markdown(records: list[dict]) -> str:
    lines = [
        "# Obsidian Card Index",
        "",
        "Generated bridge records from local knowledge items to Obsidian synthesis cards.",
        "",
        "| KB ID | Date | Card | Module | Topic |",
        "| --- | --- | --- | --- | --- |",
    ]
    for record in records:
        title = escape_table_cell(record.get("title", ""))
        path = record.get("obsidian_path", "")
        lines.append(
            "| {kb_id} | {date} | [{title}]({path}) | {module} | `{topic}` |".format(
                kb_id=escape_table_cell(record.get("kb_id", "")),
                date=escape_table_cell(record.get("date", "")),
                title=title,
                path=path.replace("\\", "/").replace(" ", "%20"),
                module=escape_table_cell(record.get("module", "")),
                topic=escape_table_cell(record.get("topic", "")),
            )
        )
    return "\n".join(lines) + "\n"


def append_registry_record(
    root: Path,
    item: dict,
    output: Path,
    card_date: str,
    module_alias: str | None,
) -> None:
    registry = registry_path(root)
    registry.parent.mkdir(parents=True, exist_ok=True)
    module = module_alias or item.get("topic") or "reading"
    record = {
        "kb_id": item["id"],
        "date": card_date,
        "title": item["title"],
        "module": module,
        "topic": item.get("topic", ""),
        "obsidian_path": str(output),
        "bestblogs_url": item.get("bestblogs_url", ""),
        "original_url": item.get("original_url", ""),
        "local_item_path": relative_item_path(item),
    }
    with registry.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    records = load_registry(root)
    markdown = registry_markdown_path(root)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_registry_markdown(records), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an Obsidian card draft from a local KB item.")
    parser.add_argument("item_id", help="Local knowledge item ID, such as BB-2026-05-01-564.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Card date in YYYY-MM-DD.")
    parser.add_argument("--module", dest="module_alias", help="Target module alias, such as security, eval, case.")
    parser.add_argument("--vault-root", default=str(DEFAULT_VAULT_ROOT), help="Obsidian vault root.")
    parser.add_argument("--write", action="store_true", help="Write the card into the Obsidian vault.")
    parser.add_argument("--register-existing", help="Register an existing Obsidian card path without modifying it.")
    parser.add_argument("--force", action="store_true", help="Allow another card for an already registered item.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    item = load_item(ROOT, args.item_id)
    try:
        if args.register_existing:
            output = register_existing_card(
                ROOT,
                item,
                Path(args.register_existing),
                args.date,
                args.module_alias,
                force=args.force,
            )
            print(f"Registered existing Obsidian card: {output}")
        elif args.write:
            output = write_card(ROOT, Path(args.vault_root), item, args.date, args.module_alias, force=args.force)
            print(f"Wrote Obsidian card: {output}")
        else:
            print(render_card(item, args.date))
        return 0
    except DuplicateCardError as exc:
        print(f"Duplicate Obsidian card: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
