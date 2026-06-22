"""
用户模型推断层 (M5)
- 从 user_events 读取行为信号，更新 user_profile
- 推断维度：expertise_level / primary_angle / active_topics / weak_topics
- 全规则式，无 ML
"""
import json
import sqlite3
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DB = os.path.join(ROOT, "product", "data", "product.sqlite")

# 子话题关键词映射（和 domains.json 对齐）
TOPIC_KEYWORDS = {
    "control-flow":  ["control", "loop", "orchestration", "flow", "langgraph", "编排", "控制流"],
    "memory-context":["memory", "context", "recall", "rag", "retrieval", "记忆", "上下文"],
    "tools-mcp":     ["tool", "mcp", "function call", "plugin", "工具", "插件"],
    "multi-agent":   ["multi-agent", "swarm", "collaboration", "协作", "多智能体"],
    "evaluation":    ["evaluation", "benchmark", "reliability", "评测", "评估", "可靠性"],
    "safety":        ["safety", "security", "permission", "guardrail", "安全", "权限"],
    "product-biz":   ["product", "business", "startup", "commercial", "产品", "商业"],
}

# 角度关键词（文章 topic/tags 中判断）
ANGLE_TOPICS = {
    "engineer": ["01-context-memory", "02-tools-actions", "03-control-loop", "04-evaluation-guardrails"],
    "product":  ["06-frontier-radar"],
    "researcher":["04-evaluation-guardrails", "06-frontier-radar"],
}


def _conn():
    conn = sqlite3.connect(PRODUCT_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ── 核心推断函数 ──────────────────────────────────────────────

def infer_and_update():
    """
    从行为数据推断用户画像，写回 user_profile。
    在以下时机调用：
      - POST /api/events 收到 view_end 时（含停留时长）
      - POST /api/events 收到 feedback_* 时
    """
    conn = _conn()

    # ── 读取所有事件 ──────────────────────────────────────────
    events = conn.execute(
        "SELECT article_id, event_type, payload FROM user_events ORDER BY created_at"
    ).fetchall()

    # ── 读取文章元数据（用于反查 topic/tags）────────────────
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    with open(meta_path, encoding="utf-8") as f:
        articles_meta = {a["id"]: a for a in json.load(f)}

    # ── 信号聚合 ──────────────────────────────────────────────
    deep_reads     = set()  # article_id → 有效阅读（pct>=80）
    known_clicks   = set()
    useful_clicks  = set()
    dive_clicks    = set()
    topic_reads    = {}   # topic → 篇数

    for e in events:
        aid   = e["article_id"]
        etype = e["event_type"]
        try:
            payload = json.loads(e["payload"] or "{}")
        except Exception:
            payload = {}

        if etype == "view_end":
            # 前端发 pct（滚动百分比），>=80 算有效阅读
            pct = payload.get("pct", payload.get("seconds", 0))
            if pct >= 80 or payload.get("seconds", 0) >= 30:
                deep_reads.add(aid)
        elif etype == "feedback_known":
            known_clicks.add(aid)
        elif etype == "feedback_useful":
            useful_clicks.add(aid)
        elif etype == "feedback_dive":
            dive_clicks.add(aid)

    for aid in deep_reads:
        meta = articles_meta.get(aid, {})
        topic = meta.get("topic", "")
        if topic:
            topic_reads[topic] = topic_reads.get(topic, 0) + 1

    total_events = len(events)

    # ── 推断 expertise_level ─────────────────────────────────
    # "已知道"比例高 → expert
    if total_events > 10 and len(known_clicks) / max(len(deep_reads), 1) > 0.4:
        expertise = "expert"
    elif total_events > 5 and len(known_clicks) / max(len(deep_reads), 1) < 0.1:
        expertise = "beginner"
    else:
        expertise = "intermediate"

    # ── 推断 primary_angle ───────────────────────────────────
    angle_score = {"engineer": 0, "product": 0, "researcher": 0}
    for topic, count in topic_reads.items():
        for angle, topics in ANGLE_TOPICS.items():
            if topic in topics:
                angle_score[angle] += count
    primary_angle = max(angle_score, key=lambda k: angle_score[k]) if any(angle_score.values()) else "unknown"

    # ── active_topics（至少读过 1 篇的 topic，按阅读量排序）──
    active_topics = sorted(topic_reads, key=lambda t: topic_reads[t], reverse=True)

    # ── weak_topics（完全没读过的 topic）──────────────────────
    all_topics = set()
    for meta in articles_meta.values():
        t = meta.get("topic", "")
        if t:
            all_topics.add(t)
    weak_topics = [t for t in all_topics if topic_reads.get(t, 0) == 0]

    # ── 写回 user_profile ────────────────────────────────────
    conn.execute("""
        UPDATE user_profile SET
            expertise_level = ?,
            primary_angle   = ?,
            active_topics   = ?,
            weak_topics     = ?,
            updated_at      = datetime('now','localtime')
        WHERE id = 1
    """, (
        expertise,
        primary_angle,
        json.dumps(active_topics, ensure_ascii=False),
        json.dumps(weak_topics,   ensure_ascii=False),
    ))
    conn.commit()
    conn.close()

    return {
        "expertise_level": expertise,
        "primary_angle":   primary_angle,
        "active_topics":   active_topics,
        "weak_topics":     weak_topics,
        "deep_reads":      len(deep_reads),
        "known_clicks":    len(known_clicks),
    }


def get_profile_summary() -> dict:
    """返回用户画像 + 行为统计摘要。"""
    conn = _conn()
    row = conn.execute("SELECT * FROM user_profile WHERE id=1").fetchone()
    events_count = conn.execute("SELECT COUNT(*) FROM user_events").fetchone()[0]
    notes_count  = conn.execute("SELECT COUNT(*) FROM user_notes").fetchone()[0]
    conn.close()

    if not row:
        return {}
    p = dict(row)
    p["active_topics"] = json.loads(p.get("active_topics", "[]"))
    p["weak_topics"]   = json.loads(p.get("weak_topics",   "[]"))
    p["events_count"]  = events_count
    p["notes_count"]   = notes_count
    return p


# ── 自测 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    result = infer_and_update()
    print("推断结果:")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print()
    profile = get_profile_summary()
    print("用户画像:")
    for k, v in profile.items():
        print(f"  {k}: {v}")
