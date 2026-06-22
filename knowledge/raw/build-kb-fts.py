import json
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IN_PATH = ROOT / "knowledge" / "retrieval" / "articles-meta.jsonl"
DB_PATH = ROOT / "knowledge" / "retrieval" / "kb.sqlite"
REPORT_PATH = ROOT / "knowledge" / "retrieval" / "fts-report.json"
CHUNK_TARGET_CHARS = 1400
CHUNK_OVERLAP_CHARS = 220


def load_rows():
    rows = []
    with IN_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def article_body(article_text):
    parts = article_text.split("\n---\n")
    return (parts[1] if len(parts) > 1 else article_text).strip()


def clean_markdown(text):
    text = text.replace("\r", "")
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def article_chunks(row):
    article_path = ROOT / row["article_path"]
    if not article_path.exists():
        return []

    article_text = clean_markdown(article_body(article_path.read_text(encoding="utf-8")))
    if not article_text:
        return []

    sections = []
    current_heading = "Article"
    current_lines = []
    raw_text = article_path.read_text(encoding="utf-8").replace("\r", "")
    for line in article_body(raw_text).split("\n"):
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match:
            if current_lines:
                sections.append((current_heading, clean_markdown("\n".join(current_lines))))
            current_heading = heading_match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_heading, clean_markdown("\n".join(current_lines))))

    if not sections:
        sections = [("Article", article_text)]

    chunks = []
    ordinal = 0
    for heading, section_text in sections:
        section_text = re.sub(r"\s+", " ", section_text).strip()
        if not section_text:
            continue
        start = 0
        while start < len(section_text):
            end = min(start + CHUNK_TARGET_CHARS, len(section_text))
            chunk_text = section_text[start:end].strip()
            if len(chunk_text) >= 120:
                chunks.append(
                    {
                        "item_id": row["id"],
                        "ordinal": ordinal,
                        "heading": heading,
                        "chunk_text": chunk_text,
                        "contextual_text": "\n".join(
                            [
                                f"Article: {row['title']}",
                                f"Topic: {row['topic']}",
                                f"Source: {row['source']}",
                                f"Section: {heading}",
                                "",
                                chunk_text,
                            ]
                        ),
                    }
                )
                ordinal += 1
            if end >= len(section_text):
                break
            start = max(end - CHUNK_OVERLAP_CHARS, start + 1)
    return chunks


def main():
    rows = load_rows()
    all_chunks = []
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("PRAGMA journal_mode=DELETE")
    cur.execute("PRAGMA synchronous=NORMAL")

    cur.execute(
        """
        CREATE TABLE items (
            rowid INTEGER PRIMARY KEY,
            id TEXT UNIQUE NOT NULL,
            date TEXT,
            title TEXT,
            source TEXT,
            topic TEXT,
            blocks_json TEXT,
            tags_json TEXT,
            aliases_json TEXT,
            status TEXT,
            index_title TEXT,
            index_source TEXT,
            bestblogs_url TEXT,
            original_url TEXT,
            summary_path TEXT,
            article_path TEXT,
            source_path TEXT,
            raw_dir TEXT,
            takeaway TEXT,
            reusable_principle TEXT,
            summary_text TEXT,
            article_preview TEXT,
            retrieval_text TEXT,
            article_chars INTEGER,
            article_size INTEGER
        )
        """
    )

    cur.execute(
        """
        CREATE VIRTUAL TABLE items_fts USING fts5(
            id UNINDEXED,
            title,
            source,
            topic,
            blocks,
            tags,
            aliases,
            takeaway,
            reusable_principle,
            summary_text,
            article_preview,
            retrieval_text,
            tokenize = 'trigram'
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE chunks (
            rowid INTEGER PRIMARY KEY,
            item_id TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            topic TEXT,
            title TEXT,
            source TEXT,
            heading TEXT,
            chunk_text TEXT,
            contextual_text TEXT,
            summary_path TEXT,
            article_path TEXT,
            source_path TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            item_id UNINDEXED,
            title,
            topic,
            heading,
            contextual_text,
            chunk_text,
            tokenize = 'trigram'
        )
        """
    )

    for row in rows:
        cur.execute(
            """
            INSERT INTO items (
                id, date, title, source, topic, blocks_json, tags_json, aliases_json, status,
                index_title, index_source, bestblogs_url, original_url,
                summary_path, article_path, source_path, raw_dir,
                takeaway, reusable_principle, summary_text, article_preview,
                retrieval_text, article_chars, article_size
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["date"],
                row["title"],
                row["source"],
                row["topic"],
                json.dumps(row["blocks"], ensure_ascii=False),
                json.dumps(row["tags"], ensure_ascii=False),
                json.dumps(row.get("aliases", []), ensure_ascii=False),
                row["status"],
                row["index_title"],
                row["index_source"],
                row["bestblogs_url"],
                row["original_url"],
                row["summary_path"],
                row["article_path"],
                row["source_path"],
                row["raw_dir"],
                row["takeaway"],
                row["reusable_principle"],
                row["summary_text"],
                row["article_preview"],
                row["retrieval_text"],
                row["article_chars"],
                row["article_size"],
            ),
        )
        rowid = cur.lastrowid
        cur.execute(
            """
            INSERT INTO items_fts (
                rowid, id, title, source, topic, blocks, tags, aliases, takeaway,
                reusable_principle, summary_text, article_preview, retrieval_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rowid,
                row["id"],
                row["title"],
                row["source"],
                row["topic"],
                ", ".join(row["blocks"]),
                ", ".join(row["tags"]),
                ", ".join(row.get("aliases", [])),
                row["takeaway"],
                row["reusable_principle"],
                row["summary_text"],
                row["article_preview"],
                row["retrieval_text"],
            ),
        )
        for chunk in article_chunks(row):
            all_chunks.append(chunk)
            cur.execute(
                """
                INSERT INTO chunks (
                    item_id, ordinal, topic, title, source, heading, chunk_text,
                    contextual_text, summary_path, article_path, source_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["id"],
                    chunk["ordinal"],
                    row["topic"],
                    row["title"],
                    row["source"],
                    chunk["heading"],
                    chunk["chunk_text"],
                    chunk["contextual_text"],
                    row["summary_path"],
                    row["article_path"],
                    row["source_path"],
                ),
            )
            chunk_rowid = cur.lastrowid
            cur.execute(
                """
                INSERT INTO chunks_fts (
                    rowid, item_id, title, topic, heading, contextual_text, chunk_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    chunk_rowid,
                    row["id"],
                    row["title"],
                    row["topic"],
                    chunk["heading"],
                    chunk["contextual_text"],
                    chunk["chunk_text"],
                ),
            )

    cur.execute("CREATE INDEX idx_items_topic ON items(topic)")
    cur.execute("CREATE INDEX idx_items_date ON items(date)")
    cur.execute("CREATE INDEX idx_chunks_item_id ON chunks(item_id)")
    cur.execute("CREATE INDEX idx_chunks_topic ON chunks(topic)")
    con.commit()
    cur.execute("VACUUM")
    con.close()

    report = {
        "generated_from": str(IN_PATH.relative_to(ROOT)).replace("\\", "/"),
        "db": str(DB_PATH.relative_to(ROOT)).replace("\\", "/"),
        "items": len(rows),
        "chunks": len(all_chunks),
        "chunk_target_chars": CHUNK_TARGET_CHARS,
        "chunk_overlap_chars": CHUNK_OVERLAP_CHARS,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
