"""
推荐层 (M9) + 知识图谱数据 (M8)
M9：基于知识盲点的规则推荐，每次返回 3 篇，带推荐理由
M8：从文章 topic/tags 共现关系生成 Cytoscape.js 节点/边数据
"""
import os
import json
from datetime import date, timedelta

ROOT       = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
META_PATH  = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
PRODUCT_DB = os.path.join(ROOT, "product", "data", "product.sqlite")

def _load_meta():
    with open(META_PATH, encoding="utf-8") as f:
        return json.load(f)

def _conn():
    import sqlite3
    conn = sqlite3.connect(PRODUCT_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ════════════════════════════════════════════════════════════
# M9 — 推荐
# ════════════════════════════════════════════════════════════

def _get_read_ids() -> set:
    conn = _conn()
    rows = conn.execute(
        "SELECT DISTINCT article_id FROM user_events WHERE event_type='view_end'"
    ).fetchall()
    conn.close()
    return {r[0] for r in rows}


def _get_dismissed_ids() -> set:
    """用 feedback_known 事件作为"不感兴趣"信号。"""
    conn = _conn()
    rows = conn.execute(
        "SELECT DISTINCT article_id FROM user_events WHERE event_type='feedback_known'"
    ).fetchall()
    conn.close()
    return {r[0] for r in rows}


def get_recommendations(top_n: int = 3) -> list:
    """
    推荐逻辑（纯规则）：
    1. 统计各 topic 覆盖率（已读/总量）
    2. 覆盖率最低的 topic → 优先推荐
    3. 在这些 topic 中取最新、未读、未 dismiss 的文章
    4. 返回附带推荐理由的文章列表
    """
    articles   = _load_meta()
    read_ids   = _get_read_ids()
    dismiss_ids = _get_dismissed_ids()
    today      = date.today().isoformat()

    # ── 统计每个 topic 的文章数和已读数 ─────────────────────
    topic_total = {}
    topic_read  = {}
    for a in articles:
        t = a.get("topic", "unknown")
        topic_total[t] = topic_total.get(t, 0) + 1
        if a["id"] in read_ids:
            topic_read[t] = topic_read.get(t, 0) + 1

    # 覆盖率
    coverage = {
        t: topic_read.get(t, 0) / topic_total[t]
        for t in topic_total
    }

    # ── 按覆盖率升序排 topic ─────────────────────────────────
    weak_topics = sorted(coverage, key=lambda t: coverage[t])

    # ── 候选文章：未读、未 dismiss、按日期倒序 ───────────────
    candidates = [
        a for a in articles
        if a["id"] not in read_ids
        and a["id"] not in dismiss_ids
    ]
    candidates.sort(key=lambda a: a.get("date", ""), reverse=True)

    # ── 从最弱 topic 里挑文章 ────────────────────────────────
    result = []
    used_topics = set()

    for topic in weak_topics:
        if len(result) >= top_n:
            break
        topic_candidates = [a for a in candidates if a.get("topic") == topic]
        if not topic_candidates:
            continue

        pick = topic_candidates[0]
        cov_pct = round(coverage[topic] * 100)
        total   = topic_total[topic]
        read_n  = topic_read.get(topic, 0)

        result.append({
            "id":      pick["id"],
            "title":   pick["title"],
            "date":    pick.get("date", ""),
            "topic":   pick.get("topic", ""),
            "summary": pick.get("summary_text", "") or pick.get("takeaway", ""),
            "url":     pick.get("bestblogs_url", ""),
            "reason":  (
                f"你在「{topic}」话题只读过 {read_n}/{total} 篇（覆盖率 {cov_pct}%），"
                f"这是该话题中最新的未读文章。"
            ),
        })
        used_topics.add(topic)

    # 不足时从其他候选补足
    if len(result) < top_n:
        seen = {r["id"] for r in result}
        for a in candidates:
            if len(result) >= top_n:
                break
            if a["id"] not in seen:
                result.append({
                    "id":      a["id"],
                    "title":   a["title"],
                    "date":    a.get("date", ""),
                    "topic":   a.get("topic", ""),
                    "summary": a.get("summary_text", "") or a.get("takeaway", ""),
                    "url":     a.get("bestblogs_url", ""),
                    "reason":  "你还没读过这篇，它是知识库中较新的文章。",
                })

    return result


# ════════════════════════════════════════════════════════════
# M8 — 知识图谱数据
# ════════════════════════════════════════════════════════════

def _load_topic_names() -> dict:
    """从 domains.json 读取 topic ID → 中文名映射。"""
    import json as _json
    path = os.path.join(ROOT, "product", "config", "domains.json")
    names = {}
    try:
        with open(path, encoding="utf-8") as f:
            data = _json.load(f)
        for d in data.get("domains", []):
            for st in d.get("subtopics", []):
                names[st["id"]] = st["name"]
    except Exception:
        pass
    return names


def get_graph_data() -> dict:
    """
    生成 Cytoscape.js 格式的节点/边数据。
    节点 = topic，边 = tag 共现（同一篇文章有相同 tag 的 topic 之间连边）。
    节点大小 = 文章数，颜色深浅 = 用户覆盖率。
    """
    articles    = _load_meta()
    read_ids    = _get_read_ids()
    topic_names = _load_topic_names()

    topic_total = {}
    topic_read  = {}
    topic_tags  = {}   # topic → Counter of tags

    for a in articles:
        t    = a.get("topic", "unknown")
        tags = a.get("tags", [])
        topic_total[t] = topic_total.get(t, 0) + 1
        if a["id"] in read_ids:
            topic_read[t] = topic_read.get(t, 0) + 1
        for tag in tags:
            if tag:
                topic_tags.setdefault(t, {})
                topic_tags[t][tag] = topic_tags[t].get(tag, 0) + 1

    # ── 节点 ─────────────────────────────────────────────────
    nodes = []
    for topic, total in topic_total.items():
        read    = topic_read.get(topic, 0)
        cov_pct = round(read / total * 100) if total else 0
        nodes.append({
            "data": {
                "id":       topic,
                "label":    topic_names.get(topic, topic.split("-", 1)[-1] if "-" in topic else topic),
                "total":    total,
                "read":     read,
                "cov_pct":  cov_pct,
                "size":     max(30, min(80, total * 1.5)),
            }
        })

    # ── 边：topic 间的 tag 共现 ────────────────────────────────
    topic_list = list(topic_tags.keys())
    edges = []
    seen_edges = set()

    for i, t1 in enumerate(topic_list):
        for t2 in topic_list[i+1:]:
            tags1 = set(topic_tags.get(t1, {}).keys())
            tags2 = set(topic_tags.get(t2, {}).keys())
            common = tags1 & tags2
            if len(common) >= 2:   # 至少 2 个共同 tag 才连边
                edge_id = f"{t1}__{t2}"
                if edge_id not in seen_edges:
                    seen_edges.add(edge_id)
                    edges.append({
                        "data": {
                            "id":     edge_id,
                            "source": t1,
                            "target": t2,
                            "weight": len(common),
                            "common_tags": list(common)[:5],
                        }
                    })

    return {
        "nodes":       nodes,
        "edges":       edges,
        "topic_stats": [
            {
                "topic":       t,
                "name":        topic_names.get(t, t),
                "total":       topic_total[t],
                "read":        topic_read.get(t, 0),
                "cov_pct":     round(topic_read.get(t, 0) / topic_total[t] * 100) if topic_total[t] else 0,
            }
            for t in sorted(topic_total)
        ],
    }


# ── 自测 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    recs = get_recommendations()
    print(f"推荐 {len(recs)} 篇:")
    for r in recs:
        print(f"  [{r['topic']}] {r['title'][:50]}")
        print(f"    理由: {r['reason']}")

    print()
    graph = get_graph_data()
    print(f"图谱: {len(graph['nodes'])} 节点, {len(graph['edges'])} 边")
    for n in graph["nodes"]:
        d = n["data"]
        print(f"  {d['id']}: {d['total']}篇, 覆盖{d['cov_pct']}%")
