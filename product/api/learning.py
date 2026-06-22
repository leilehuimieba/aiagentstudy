"""
学习机制层 (M7)
- 间隔复习：supermemo2 库实现 SM-2 算法
- 复习问题：文章入库时 LLM 生成，存入 review_queue.review_question
- 复习动作：记录结果，更新 next_review_at / ease_factor
- 读完压缩：user_notes 已在 db.py 实现，本模块补充复习队列管理
"""
import os
import json
import sqlite3
from datetime import datetime, date, timedelta

from supermemo2 import first_review as sm2_first, review as sm2_review
from openai import OpenAI

ROOT       = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DB = os.path.join(ROOT, "product", "data", "product.sqlite")

# ── 配置 ─────────────────────────────────────────────────────

def _load_env():
    env_path = os.path.join(ROOT, "product", ".env")
    cfg = {}
    if not os.path.exists(env_path):
        return cfg
    for line in open(env_path, encoding="utf-8").read().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg

_ENV   = _load_env()
_MODEL = _ENV.get("QA_MODEL", "deepseek-v4-flash")

def _client():
    return OpenAI(
        api_key=_ENV.get("LLM_API_KEY", ""),
        base_url=_ENV.get("LLM_BASE_URL", "https://api.deepseek.com/v1"),
    )

def _conn():
    conn = sqlite3.connect(PRODUCT_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ── 复习问题生成 ───────────────────────────────────────────────

def generate_review_question(article_id: str, article_text: str, title: str = "") -> str:
    """用 LLM 针对文章生成一个核心考查问题。"""
    prompt = f"""根据以下文章，生成一个能考查核心理解的简短问题（不超过30字）。
问题应该是开放式的，需要读过文章才能回答，不能只靠常识。
只输出问题本身，不要其他内容。

文章标题：{title}
文章内容：{article_text[:2000]}"""

    client = _client()
    resp = client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


# ── 入队 ─────────────────────────────────────────────────────

def enqueue_review(article_id: str, article_text: str = "", title: str = "") -> dict:
    """
    将文章加入复习队列（3天后首次复习）。
    如果已在队列中则忽略。
    返回队列条目。
    """
    conn = _conn()
    existing = conn.execute(
        "SELECT id FROM review_queue WHERE article_id=?", (article_id,)
    ).fetchone()

    if existing:
        conn.close()
        return {"status": "already_queued", "article_id": article_id}

    # 生成复习问题
    question = f"《{title}》的核心观点是什么？"  # 默认兜底
    if article_text:
        try:
            question = generate_review_question(article_id, article_text, title)
        except Exception:
            pass  # 保留默认问题

    next_review = (date.today() + timedelta(days=3)).isoformat()

    conn.execute("""
        INSERT INTO review_queue(article_id, review_question, next_review_at, ease_factor, review_count)
        VALUES (?, ?, ?, 2.5, 0)
    """, (article_id, question, next_review))
    conn.commit()
    conn.close()

    return {
        "status": "queued",
        "article_id": article_id,
        "review_question": question,
        "next_review_at": next_review,
    }


# ── 获取今日待复习 ─────────────────────────────────────────────

def get_due_reviews(limit: int = 10) -> list:
    """返回今天到期的复习条目，带文章元数据。"""
    today = date.today().isoformat()
    conn  = _conn()
    rows  = conn.execute("""
        SELECT r.id, r.article_id, r.review_question,
               r.next_review_at, r.ease_factor, r.review_count, r.last_result
        FROM review_queue r
        WHERE r.next_review_at <= ?
        ORDER BY r.next_review_at ASC
        LIMIT ?
    """, (today, limit)).fetchall()
    conn.close()

    # 补文章标题
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    with open(meta_path, encoding="utf-8") as f:
        meta_map = {a["id"]: a for a in json.load(f)}

    items = []
    for r in rows:
        meta = meta_map.get(r["article_id"], {})
        items.append({
            "id":              r["id"],
            "article_id":      r["article_id"],
            "title":           meta.get("title", r["article_id"]),
            "date":            meta.get("date", ""),
            "review_question": r["review_question"],
            "next_review_at":  r["next_review_at"],
            "ease_factor":     r["ease_factor"],
            "review_count":    r["review_count"],
            "last_result":     r["last_result"],
        })
    return items


def get_review_stats() -> dict:
    """复习队列统计。"""
    today = date.today().isoformat()
    conn  = _conn()
    total   = conn.execute("SELECT COUNT(*) FROM review_queue").fetchone()[0]
    due     = conn.execute(
        "SELECT COUNT(*) FROM review_queue WHERE next_review_at <= ?", (today,)
    ).fetchone()[0]
    done    = conn.execute(
        "SELECT COUNT(*) FROM review_queue WHERE last_result IS NOT NULL"
    ).fetchone()[0]
    conn.close()
    return {"total": total, "due_today": due, "ever_reviewed": done}


# ── 提交复习结果 ───────────────────────────────────────────────

# quality 映射：remember=5, hint=3, forgot=1
_QUALITY = {"remember": 5, "hint": 3, "forgot": 1}

def submit_review(queue_id: int, result: str) -> dict:
    """
    result: "remember" | "hint" | "forgot"
    用 supermemo2 计算下次复习时间。
    返回更新后的条目。
    """
    quality = _QUALITY.get(result, 3)

    conn = _conn()
    row  = conn.execute(
        "SELECT * FROM review_queue WHERE id=?", (queue_id,)
    ).fetchone()
    if not row:
        conn.close()
        raise ValueError(f"review_queue id={queue_id} 不存在")

    ease      = row["ease_factor"]
    reps      = row["review_count"]
    interval  = max(1, reps * 3)  # 首次 interval 估算

    if reps == 0:
        sm = sm2_first(quality)
    else:
        sm = sm2_review(quality, ease, interval, reps)

    interval_days = sm["interval"]
    new_ease      = sm["easiness"]
    next_date     = (date.today() + timedelta(days=interval_days)).isoformat()

    conn.execute("""
        UPDATE review_queue SET
            ease_factor    = ?,
            review_count   = review_count + 1,
            next_review_at = ?,
            last_result    = ?
        WHERE id = ?
    """, (new_ease, next_date, result, queue_id))
    conn.commit()
    conn.close()

    return {
        "queue_id":       queue_id,
        "result":         result,
        "next_review_at": next_date,
        "interval_days":  interval_days,
        "new_easiness":   new_ease,
    }


# ── 自测 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import db
    db._load()

    stats = get_review_stats()
    print(f"复习队列: {stats}")

    # 取一篇文章入队测试
    arts = db.get_all_articles(limit=1)
    if arts:
        a    = arts[0]
        full = db.get_article(a["id"])
        text = full.get("full_text", "") or a.get("summary", "")
        result = enqueue_review(a["id"], text, a["title"])
        print(f"入队: {result}")

    due = get_due_reviews()
    print(f"今日待复习: {len(due)} 条")
    for d in due[:2]:
        print(f"  [{d['article_id']}] {d['review_question'][:60]}")
