"""
知识库查询封装
- 知识库来源：knowledge/retrieval/articles-meta.json（165篇，内存索引）
- 用户数据来源：product/data/product.sqlite
- 注意：FTS5 trigram 在 SQLite 3.28 下不可用，统一用内存过滤
"""
import json
import os
import sqlite3
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
META_PATH = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
ITEMS_DIR = os.path.join(ROOT, "knowledge", "items")
PRODUCT_DB = os.path.join(ROOT, "product", "data", "product.sqlite")
DOMAINS_PATH = os.path.join(ROOT, "product", "config", "domains.json")

# domain_id -> set of topic IDs that belong to it
_domain_topics: dict = {}

def _load_domains():
    global _domain_topics
    if _domain_topics:
        return
    with open(DOMAINS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    for d in data.get("domains", []):
        _domain_topics[d["id"]] = {st["id"] for st in d.get("subtopics", [])}

def get_topics_for_domain(domain_id: str) -> set:
    _load_domains()
    return _domain_topics.get(domain_id, set())

# 启动时加载全量元数据到内存
_articles = []  # list[dict]

def _load():
    global _articles
    if _articles:
        return
    with open(META_PATH, encoding="utf-8") as f:
        _articles = json.load(f)

def _search_text(item: dict, query: str) -> bool:
    text = " ".join([
        item.get("title", ""),
        item.get("retrieval_text", ""),
        item.get("takeaway", ""),
        item.get("topic", ""),
    ]).lower()
    return query.lower() in text


# ── 主查询函数 ────────────────────────────────────────────────

def search_articles(query: str = "", domain: str = None,
                    days: int = None, limit: int = 10):
    """关键词 + 领域 + 时间过滤，返回文章元数据列表。"""
    _load()
    cutoff = None
    if days:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    allowed_topics = get_topics_for_domain(domain) if domain else None

    results = []
    for item in _articles:
        if allowed_topics is not None and item.get("topic", "") not in allowed_topics:
            continue
        if cutoff and item.get("date", "9999") < cutoff:
            continue
        if query and not _search_text(item, query):
            continue
        results.append(_to_card(item))

    results.sort(key=lambda x: x["date"], reverse=True)
    return results[:limit]


def get_article(article_id: str):
    """返回单篇文章的完整信息（含正文）。"""
    _load()
    for item in _articles:
        if item.get("id") == article_id:
            card = _to_card(item)
            card["full_text"] = _read_article_text(item)
            return card
    return None


def get_recent_articles(days: int = 7, limit: int = 20):
    """最近 N 天的文章，按日期倒序。"""
    return search_articles(days=days, limit=limit)


def get_articles_by_subtopic(subtopic_tag: str, limit: int = 10):
    """按子话题关键词过滤。"""
    return search_articles(query=subtopic_tag, limit=limit)


def get_all_articles(limit: int = 50):
    """返回所有文章（按日期倒序）。"""
    return search_articles(limit=limit)


# ── 用户行为写入 ──────────────────────────────────────────────

def record_event(article_id: str, event_type: str, payload: dict = None) -> None:
    """写入阅读行为事件。"""
    conn = _product_conn()
    conn.execute(
        "INSERT INTO user_events(article_id, event_type, payload) VALUES(?,?,?)",
        (article_id, event_type, json.dumps(payload or {}, ensure_ascii=False))
    )
    conn.commit()
    conn.close()


def save_note(article_id: str, note_text: str, note_type: str = "compression") -> None:
    """保存用户笔记（每篇文章保留最新一条，upsert）。"""
    conn = _product_conn()
    existing = conn.execute(
        "SELECT id FROM user_notes WHERE article_id=?", (article_id,)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE user_notes SET note_text=?, note_type=?, created_at=datetime('now','localtime') WHERE article_id=?",
            (note_text, note_type, article_id)
        )
    else:
        conn.execute(
            "INSERT INTO user_notes(article_id, note_text, note_type) VALUES(?,?,?)",
            (article_id, note_text, note_type)
        )
        conn.execute(
            "UPDATE user_profile SET total_notes=total_notes+1, updated_at=datetime('now','localtime') WHERE id=1"
        )
    conn.commit()
    conn.close()


def get_note_for_article(article_id: str) -> str:
    """返回某篇文章的笔记内容，没有则返回空字符串。"""
    conn = _product_conn()
    row = conn.execute(
        "SELECT note_text FROM user_notes WHERE article_id=?", (article_id,)
    ).fetchone()
    conn.close()
    return row["note_text"] if row else ""


def get_notes(limit: int = 50):
    """获取用户笔记列表（含文章标题）。"""
    conn = _product_conn()
    rows = conn.execute(
        "SELECT id, article_id, note_text, note_type, created_at FROM user_notes ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    notes = [dict(r) for r in rows]
    # 补文章标题
    _load()
    meta_map = {a["id"]: a.get("title", a["id"]) for a in _articles}
    for n in notes:
        n["title"] = meta_map.get(n["article_id"], n["article_id"])
    return notes


def get_user_profile() -> dict:
    """获取用户画像。"""
    conn = _product_conn()
    row = conn.execute("SELECT * FROM user_profile WHERE id=1").fetchone()
    conn.close()
    if not row:
        return {}
    p = dict(row)
    p["active_topics"] = json.loads(p.get("active_topics", "[]"))
    p["weak_topics"] = json.loads(p.get("weak_topics", "[]"))
    return p


def update_read_stats() -> None:
    """阅读完一篇后，更新总读数。"""
    conn = _product_conn()
    conn.execute(
        "UPDATE user_profile SET total_read=total_read+1, updated_at=datetime('now','localtime') WHERE id=1"
    )
    conn.commit()
    conn.close()


# ── 统计 ─────────────────────────────────────────────────────

def get_timeline():
    """
    返回每个 topic 按月的文章数量，用于时间轴视图。
    结果格式：{months: [...], series: [{topic, data: [...]}]}
    """
    _load()
    from collections import defaultdict
    # 收集所有年月
    month_topic = defaultdict(lambda: defaultdict(int))
    for item in _articles:
        d = item.get("date", "")
        if len(d) >= 7:
            ym = d[:7]  # "2025-11"
            t  = item.get("topic", "unknown")
            month_topic[ym][t] += 1

    all_months = sorted(month_topic.keys())
    all_topics = sorted({item.get("topic", "unknown") for item in _articles})

    series = []
    for topic in all_topics:
        series.append({
            "topic": topic,
            "data":  [month_topic[m].get(topic, 0) for m in all_months],
        })

    return {"months": all_months, "series": series}


def get_topic_stats():
    """返回每个 topic 的文章数量和用户读过数量。"""
    _load()
    from collections import Counter
    total_by_topic = Counter(i.get("topic", "unknown") for i in _articles)

    conn = _product_conn()
    read_events = conn.execute(
        "SELECT article_id FROM user_events WHERE event_type='view_end'"
    ).fetchall()
    conn.close()
    read_ids = {r[0] for r in read_events}

    read_by_topic: Counter = Counter()
    for item in _articles:
        if item["id"] in read_ids:
            read_by_topic[item.get("topic", "unknown")] += 1

    return [
        {
            "topic": topic,
            "total": count,
            "read": read_by_topic.get(topic, 0),
            "coverage_pct": round(read_by_topic.get(topic, 0) / count * 100) if count else 0,
        }
        for topic, count in sorted(total_by_topic.items())
    ]


# ── 内部工具 ─────────────────────────────────────────────────

def _to_card(item: dict) -> dict:
    return {
        "id":       item.get("id", ""),
        "date":     item.get("date", ""),
        "title":    item.get("title", ""),
        "source":   item.get("source", ""),
        "topic":    item.get("topic", ""),
        "tags":     item.get("tags", []),
        "summary":  item.get("summary_text", "") or item.get("takeaway", ""),
        "takeaway": item.get("takeaway", ""),
        "url":      item.get("bestblogs_url", ""),
    }


def _read_article_text(item: dict) -> str:
    path = item.get("article_path", "")
    if not path:
        return ""
    full = os.path.abspath(os.path.join(ROOT, path))
    allowed_root = os.path.abspath(ITEMS_DIR)
    try:
        if os.path.commonpath([allowed_root, full]) != allowed_root:
            return ""
    except ValueError:
        return ""
    if not os.path.exists(full):
        return ""
    with open(full, encoding="utf-8") as f:
        return f.read()




def _product_conn():
    conn = sqlite3.connect(PRODUCT_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ── 自测 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("search 'checkpoint':", len(search_articles("checkpoint")), "results")
    print("recent 7d:", len(get_recent_articles(days=7)), "results")
    print("all:", len(get_all_articles(limit=200)), "total")
    art = get_all_articles(limit=1)
    if art:
        detail = get_article(art[0]["id"])
        print("article detail id:", detail["id"])
        print("full_text len:", len(detail.get("full_text", "")))
    stats = get_topic_stats()
    print("topic stats:")
    for s in stats:
        print(f"  {s['topic']}: {s['total']} total, {s['read']} read ({s['coverage_pct']}%)")
