"""
M7 优化：矛盾冲突检测
当用户读完一篇文章后，检查它与已有笔记是否存在明显观点冲突。
检测流程：
  1. 取用户最近 20 条笔记
  2. 取新文章摘要/takeaway
  3. LLM 判断是否存在冲突
  4. 有冲突则写入 contradiction_alerts 表
"""
import os
import json
import sqlite3
from datetime import datetime

ROOT       = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DB = os.path.join(ROOT, "product", "data", "product.sqlite")
META_PATH  = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")


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
    from openai import OpenAI
    return OpenAI(
        api_key=_ENV.get("LLM_API_KEY", ""),
        base_url=_ENV.get("LLM_BASE_URL", "https://api.deepseek.com/v1"),
    )


def _conn():
    conn = sqlite3.connect(PRODUCT_DB)
    conn.row_factory = sqlite3.Row
    return conn


def _get_article_claim(article_id):
    """取文章的核心观点（takeaway / summary）。"""
    with open(META_PATH, encoding="utf-8") as f:
        articles = json.load(f)
    for a in articles:
        if a.get("id") == article_id:
            return a.get("takeaway", "") or a.get("summary_text", "") or a.get("title", "")
    return ""


def _get_recent_notes(limit=20):
    """取用户最近笔记，返回 [{id, article_id, note_text}]。"""
    conn = _conn()
    rows = conn.execute(
        "SELECT id, article_id, note_text FROM user_notes ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _already_alerted(article_id):
    """这篇文章是否已经生成过冲突提醒（避免重复）。"""
    conn = _conn()
    count = conn.execute(
        "SELECT COUNT(*) FROM contradiction_alerts WHERE article_id=?", (article_id,)
    ).fetchone()[0]
    conn.close()
    return count > 0


def _detect_contradiction(new_claim, notes):
    """
    调用 LLM 判断新文章观点与已有笔记是否有冲突。
    返回 None（无冲突）或 (note_index, description) 元组。
    """
    if not new_claim or not notes:
        return None

    notes_text = "\n".join(
        f"[笔记{i+1}] {n['note_text']}" for i, n in enumerate(notes[:10])
    )

    prompt = f"""你是一个知识冲突检测助手。

新文章观点：
{new_claim}

用户已有笔记（最近10条）：
{notes_text}

请判断：新文章观点与上述任意一条笔记是否存在明显的观点矛盾或结论冲突？
（不是角度不同或补充关系，而是真正的"A说X，B说非X"式冲突）

如果有冲突，请输出 JSON：
{{"has_conflict": true, "note_index": <1-10的整数>, "description": "<一句话说明冲突内容，不超过60字>"}}

如果没有冲突，请输出：
{{"has_conflict": false}}

只输出 JSON，不要其他内容。"""

    try:
        client = _client()
        resp = client.chat.completions.create(
            model=_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.1,
        )
        text = resp.choices[0].message.content.strip()
        # 去除可能的 markdown 代码块
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text.strip())
        if data.get("has_conflict"):
            idx = int(data.get("note_index", 1)) - 1
            idx = max(0, min(idx, len(notes) - 1))
            return (idx, data.get("description", "存在观点冲突"))
    except Exception:
        pass
    return None


def check_and_save(article_id):
    """
    对刚读完的文章做矛盾检测。
    有冲突则写入 contradiction_alerts，返回冲突描述；无冲突返回 None。
    """
    if _already_alerted(article_id):
        return None

    claim = _get_article_claim(article_id)
    if not claim:
        return None

    notes = _get_recent_notes(limit=20)
    if not notes:
        return None

    result = _detect_contradiction(claim, notes)
    if not result:
        return None

    note_idx, description = result
    conflicting_note_id = notes[note_idx]["id"]

    conn = _conn()
    conn.execute("""
        INSERT INTO contradiction_alerts(article_id, conflicting_note_id, description)
        VALUES (?, ?, ?)
    """, (article_id, conflicting_note_id, description))
    conn.commit()
    conn.close()

    return {
        "description":          description,
        "conflicting_note_id":  conflicting_note_id,
        "conflicting_note":     notes[note_idx]["note_text"],
    }


def get_undismissed_alerts(limit=10):
    """获取未消除的冲突提醒列表。"""
    conn = _conn()
    rows = conn.execute("""
        SELECT id, article_id, conflicting_note_id, description, created_at
        FROM contradiction_alerts
        WHERE dismissed=0
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def dismiss_alert(alert_id):
    """标记提醒为已处理。"""
    conn = _conn()
    conn.execute("UPDATE contradiction_alerts SET dismissed=1 WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()
