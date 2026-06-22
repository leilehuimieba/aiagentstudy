"""
数据库初始化 — 创建 product.sqlite 的所有表
运行：python product/scripts/migrate_db.py
幂等：可重复运行，不会破坏已有数据
"""
import sqlite3
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(ROOT, "product", "data", "product.sqlite")


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


SCHEMA = """
-- 阅读行为事件
CREATE TABLE IF NOT EXISTS user_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT    NOT NULL,
    event_type  TEXT    NOT NULL,
    payload     TEXT    DEFAULT '{}',
    created_at  TEXT    DEFAULT (datetime('now','localtime'))
);
CREATE INDEX IF NOT EXISTS idx_events_article ON user_events(article_id);
CREATE INDEX IF NOT EXISTS idx_events_type    ON user_events(event_type);

-- 用户笔记（一句话压缩）
CREATE TABLE IF NOT EXISTS user_notes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT    NOT NULL,
    note_text   TEXT    NOT NULL,
    note_type   TEXT    DEFAULT 'compression',
    created_at  TEXT    DEFAULT (datetime('now','localtime'))
);
CREATE INDEX IF NOT EXISTS idx_notes_article ON user_notes(article_id);

-- 间隔复习队列
CREATE TABLE IF NOT EXISTS review_queue (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      TEXT    NOT NULL UNIQUE,
    review_question TEXT    NOT NULL,
    next_review_at  TEXT    NOT NULL,
    ease_factor     REAL    DEFAULT 2.5,
    review_count    INTEGER DEFAULT 0,
    last_result     TEXT    DEFAULT NULL,
    created_at      TEXT    DEFAULT (datetime('now','localtime'))
);
CREATE INDEX IF NOT EXISTS idx_review_next ON review_queue(next_review_at);

-- 多角度摘要缓存
CREATE TABLE IF NOT EXISTS article_summaries (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id  TEXT    NOT NULL,
    angle       TEXT    NOT NULL,
    summary     TEXT    NOT NULL,
    created_at  TEXT    DEFAULT (datetime('now','localtime')),
    UNIQUE(article_id, angle)
);
CREATE INDEX IF NOT EXISTS idx_summaries_article ON article_summaries(article_id);

-- 矛盾冲突提醒
CREATE TABLE IF NOT EXISTS contradiction_alerts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      TEXT    NOT NULL,
    conflicting_note_id INTEGER,
    description     TEXT    NOT NULL,
    dismissed       INTEGER DEFAULT 0,
    created_at      TEXT    DEFAULT (datetime('now','localtime'))
);
CREATE INDEX IF NOT EXISTS idx_alerts_article ON contradiction_alerts(article_id);
CREATE INDEX IF NOT EXISTS idx_alerts_dismissed ON contradiction_alerts(dismissed);

-- 用户画像（单行，upsert 更新）
CREATE TABLE IF NOT EXISTS user_profile (
    id               INTEGER PRIMARY KEY DEFAULT 1,
    expertise_level  TEXT    DEFAULT 'unknown',
    primary_angle    TEXT    DEFAULT 'unknown',
    active_topics    TEXT    DEFAULT '[]',
    weak_topics      TEXT    DEFAULT '[]',
    total_read       INTEGER DEFAULT 0,
    total_notes      INTEGER DEFAULT 0,
    updated_at       TEXT    DEFAULT (datetime('now','localtime'))
);
INSERT OR IGNORE INTO user_profile(id) VALUES(1);
"""


def migrate():
    conn = get_conn()
    for stmt in SCHEMA.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            conn.execute(stmt)
    conn.commit()

    # 验证
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()]
    conn.close()

    expected = {"article_summaries", "contradiction_alerts", "review_queue", "user_events", "user_notes", "user_profile"}
    missing = expected - set(tables)
    if missing:
        raise RuntimeError(f"建表失败，缺少：{missing}")

    print(f"[OK] product.sqlite 初始化完成")
    print(f"     路径：{DB_PATH}")
    print(f"     表：{', '.join(sorted(tables))}")


if __name__ == "__main__":
    migrate()
