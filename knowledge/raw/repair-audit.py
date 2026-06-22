import argparse
import json
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
ITEMS_ROOT = ROOT / "knowledge" / "items"
INDEX_PATH = ROOT / "knowledge" / "catalog" / "articles-index.md"


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\ufeff", "")


def write_text(path, text):
    path.write_text(text, encoding="utf-8")


def md_cells(line):
    return [part.strip() for part in line.split("|")]


def parse_index():
    rows = {}
    for line in read_text(INDEX_PATH).splitlines():
        if not line.startswith("| "):
            continue
        parts = md_cells(line)
        if len(parts) < 8 or not re.match(r"^[A-Z][A-Z0-9-]+-\d{4}", parts[1]):
            continue
        rows[parts[1]] = {
            "id": parts[1],
            "date": parts[2],
            "title": parts[3],
            "source": parts[4],
            "topic": parts[5].replace("`", ""),
            "raw_line": line,
        }
    return rows


def list_item_dirs():
    dirs = []
    for summary_path in ITEMS_ROOT.glob("**/summary.md"):
        dirs.append(summary_path.parent)
    return sorted(dirs)


def summary_fields(summary_text):
    return {
        "title": (re.search(r"^- Title: (.+)$", summary_text, re.M) or ["", ""])[1],
        "source": (re.search(r"^- Source: (.+)$", summary_text, re.M) or ["", ""])[1],
    }


def normalize_equivalent(value):
    value = (value or "").replace("|", "/")
    value = re.sub(r"\s*/\s*", " / ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def replace_summary_field(summary_text, field, value):
    label = "Title" if field == "title" else "Source"
    pattern = re.compile(rf"^- {label}: .+$", re.M)
    replacement = f"- {label}: {value}"
    if not pattern.search(summary_text):
        return summary_text
    return pattern.sub(replacement, summary_text, count=1)


def classify_summary_index(index_rows):
    safe = []
    unsafe = []
    missing = []
    for item_dir in list_item_dirs():
        item_id = item_dir.name
        index = index_rows.get(item_id)
        if not index:
            missing.append(item_id)
            continue
        summary_path = item_dir / "summary.md"
        summary_text = read_text(summary_path)
        fields = summary_fields(summary_text)
        fixes = {}
        notes = []
        unsafe_notes = []
        for field in ["title", "source"]:
            summary_value = fields[field]
            index_value = index[field]
            if summary_value == index_value:
                continue
            if normalize_equivalent(summary_value) == normalize_equivalent(index_value):
                fixes[field] = index_value
                notes.append(f"{field}: delimiter-equivalent")
            else:
                unsafe_notes.append(f"{field}: summary differs from index")
        if fixes:
            safe.append(
                {
                    "id": item_id,
                    "summary_path": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
                    "fixes": fixes,
                    "notes": notes,
                }
            )
        if unsafe_notes:
            unsafe.append(
                {
                    "id": item_id,
                    "summary_path": str(summary_path.relative_to(ROOT)).replace("\\", "/"),
                    "notes": unsafe_notes,
                    "index_title": index["title"],
                    "summary_title": fields["title"],
                    "index_source": index["source"],
                    "summary_source": fields["source"],
                }
            )
    return safe, unsafe, missing


def apply_summary_index_fixes(safe_fixes):
    changed = []
    for fix in safe_fixes:
        summary_path = ROOT / fix["summary_path"]
        text = read_text(summary_path)
        original = text
        for field, value in fix["fixes"].items():
            text = replace_summary_field(text, field, value)
        if text != original:
            write_text(summary_path, text)
            changed.append(fix)
    return changed


def main():
    parser = argparse.ArgumentParser(description="Preview or apply low-risk audit repairs.")
    parser.add_argument("--fix", choices=["summary-index"], default="summary-index")
    parser.add_argument("--execute", action="store_true", help="Apply safe repairs. Default is preview only.")
    parser.add_argument("--report-path", default="", help="Optional JSON report output path.")
    args = parser.parse_args()

    index_rows = parse_index()
    safe, unsafe, missing = classify_summary_index(index_rows)
    changed = apply_summary_index_fixes(safe) if args.execute else []
    report = {
        "fix": args.fix,
        "execute": args.execute,
        "safe_fix_count": len(safe),
        "changed_count": len(changed),
        "unsafe_mismatch_count": len(unsafe),
        "missing_index_count": len(missing),
        "safe_fixes": safe,
        "unsafe_mismatches": unsafe,
        "missing_index_rows": missing,
    }
    if args.report_path:
        report_path = ROOT / args.report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        write_text(report_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
