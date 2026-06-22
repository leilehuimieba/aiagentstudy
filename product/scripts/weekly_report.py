"""
周学习报告生成 (M10)
- SQL 聚合本周数据（阅读、笔记、复习、话题变化）
- Jinja2 渲染 HTML
- DeepSeek 把数字转成自然语言叙述段落
- 输出：product/data/reports/weekly_YYYY-WW.html

运行：python product/scripts/weekly_report.py [--week 2026-W20]
"""
import sys
import os
import json
import sqlite3
import argparse
from datetime import datetime, date, timedelta

ROOT        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DIR = os.path.join(ROOT, "product")
REPORTS_DIR = os.path.join(PRODUCT_DIR, "data", "reports")

# ── 环境 ─────────────────────────────────────────────────────

def _load_env():
    env_path = os.path.join(PRODUCT_DIR, ".env")
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
    db_path = os.path.join(PRODUCT_DIR, "data", "product.sqlite")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ── 周范围计算 ────────────────────────────────────────────────

def week_range(week_str: str = None):
    """返回 (start_date, end_date, label) 字符串。week_str 格式: '2026-W20'"""
    if week_str:
        year, w = week_str.split("-W")
        # ISO week: 周一为第一天
        d = datetime.strptime(f"{year} {w} 1", "%G %V %u").date()
    else:
        today = date.today()
        d = today - timedelta(days=today.weekday())   # 本周一

    start = d.isoformat()
    end   = (d + timedelta(days=6)).isoformat()
    label = d.strftime("%Y-W%V")
    return start, end, label


# ── 数据聚合 ─────────────────────────────────────────────────

def aggregate(start: str, end: str) -> dict:
    conn = _conn()

    # 本周阅读事件
    read_ids = [r[0] for r in conn.execute("""
        SELECT DISTINCT article_id FROM user_events
        WHERE event_type='view_end'
          AND created_at >= ? AND created_at <= ?
    """, (start + " 00:00:00", end + " 23:59:59")).fetchall()]

    # 本周笔记
    notes = [dict(r) for r in conn.execute("""
        SELECT article_id, note_text, created_at FROM user_notes
        WHERE created_at >= ? AND created_at <= ?
        ORDER BY created_at DESC
    """, (start + " 00:00:00", end + " 23:59:59")).fetchall()]

    # 本周完成复习
    reviews_done = conn.execute("""
        SELECT COUNT(*) FROM review_queue
        WHERE last_result IS NOT NULL
    """).fetchone()[0]

    # 待复习总数
    due_total = conn.execute(
        "SELECT COUNT(*) FROM review_queue WHERE next_review_at <= ?",
        (end,)
    ).fetchone()[0]

    # 话题阅读分布
    topic_reads = {}
    if read_ids:
        placeholders = ",".join("?" * len(read_ids))
        meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
        with open(meta_path, encoding="utf-8") as f:
            meta_map = {a["id"]: a for a in json.load(f)}
        for aid in read_ids:
            topic = meta_map.get(aid, {}).get("topic", "unknown")
            topic_reads[topic] = topic_reads.get(topic, 0) + 1

    # 历史总量
    total_read  = conn.execute("SELECT total_read  FROM user_profile WHERE id=1").fetchone()
    total_notes = conn.execute("SELECT total_notes FROM user_profile WHERE id=1").fetchone()

    conn.close()

    return {
        "week_read_count":  len(read_ids),
        "week_notes_count": len(notes),
        "week_notes":       notes[:5],   # 最多展示5条
        "week_reviews_done": reviews_done,
        "due_total":        due_total,
        "topic_reads":      topic_reads,
        "total_read":       total_read[0]  if total_read  else 0,
        "total_notes":      total_notes[0] if total_notes else 0,
        "active_topic":     max(topic_reads, key=topic_reads.get) if topic_reads else "—",
    }


# ── LLM 叙述生成 ─────────────────────────────────────────────

def generate_narrative(data: dict, start: str, end: str) -> str:
    """把聚合数据转成自然语言学习总结段落。"""
    notes_text = "\n".join(f"  · {n['note_text']}" for n in data["week_notes"]) or "  （本周未写笔记）"
    topic_text = "、".join(f"{t}（{n}篇）" for t, n in data["topic_reads"].items()) or "无"

    prompt = f"""你是学习教练，根据以下数据为学习者生成一段本周学习总结（150字以内，中文，鼓励为主，指出一个可改进点）：

本周（{start} 至 {end}）数据：
- 深度阅读：{data['week_read_count']} 篇
- 写了笔记：{data['week_notes_count']} 条
- 最活跃话题：{data['active_topic']}（{data['topic_reads'].get(data['active_topic'], 0)} 篇）
- 复习队列中：{data['due_total']} 条待复习
- 本周写的句子：
{notes_text}

只输出总结段落，不加标题。"""

    try:
        client = _client()
        resp = client.chat.completions.create(
            model=_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"（AI 叙述生成失败：{e}）"


# ── Jinja2 模板渲染 ───────────────────────────────────────────

REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{{ label }} 学习周报</title>
<style>
  body { font-family: -apple-system, sans-serif; background:#0f1117; color:#e2e8f0;
         max-width:700px; margin:40px auto; padding:0 24px; line-height:1.7; }
  h1 { font-size:24px; color:#fff; margin-bottom:4px; }
  .sub { color:#64748b; font-size:13px; margin-bottom:32px; }
  .section { margin-bottom:28px; }
  .section h2 { font-size:14px; color:#94a3b8; text-transform:uppercase;
                letter-spacing:.08em; margin-bottom:12px; }
  .stat-row { display:flex; gap:24px; flex-wrap:wrap; margin-bottom:20px; }
  .stat { background:#1a2035; border-radius:10px; padding:16px 20px; flex:1; min-width:120px; }
  .stat .n { font-size:28px; font-weight:700; color:#3b82f6; }
  .stat .l { font-size:12px; color:#64748b; margin-top:4px; }
  .narrative { background:#1e2535; border-left:3px solid #3b82f6; padding:16px 20px;
               border-radius:4px; font-size:14px; color:#cbd5e1; }
  .note-item { padding:10px 0; border-bottom:1px solid #1e2535; font-size:13px; color:#94a3b8; }
  .note-item:last-child { border-bottom:none; }
  .topic-bar { margin-bottom:10px; }
  .topic-label { font-size:12px; color:#94a3b8; margin-bottom:4px;
                 display:flex; justify-content:space-between; }
  .bar-bg { background:#1a2035; border-radius:3px; height:5px; }
  .bar-fill { background:#3b82f6; border-radius:3px; height:5px; }
  .footer { color:#334155; font-size:11px; margin-top:40px; text-align:center; }
</style>
</head>
<body>
<h1>{{ label }} 学习周报</h1>
<div class="sub">{{ start }} — {{ end }}</div>

<div class="section">
  <div class="stat-row">
    <div class="stat"><div class="n">{{ data.week_read_count }}</div><div class="l">本周深度阅读</div></div>
    <div class="stat"><div class="n">{{ data.week_notes_count }}</div><div class="l">本周写了笔记</div></div>
    <div class="stat"><div class="n">{{ data.due_total }}</div><div class="l">待复习条目</div></div>
    <div class="stat"><div class="n">{{ data.total_read }}</div><div class="l">累计阅读篇数</div></div>
  </div>
</div>

<div class="section">
  <h2>本周总结</h2>
  <div class="narrative">{{ narrative }}</div>
</div>

{% if data.week_notes %}
<div class="section">
  <h2>本周写的句子</h2>
  {% for note in data.week_notes %}
  <div class="note-item">💬 {{ note.note_text }}</div>
  {% endfor %}
</div>
{% endif %}

{% if data.topic_reads %}
<div class="section">
  <h2>话题阅读分布</h2>
  {% set max_count = data.topic_reads.values() | max %}
  {% for topic, count in data.topic_reads.items() %}
  <div class="topic-bar">
    <div class="topic-label"><span>{{ topic }}</span><span>{{ count }} 篇</span></div>
    <div class="bar-bg"><div class="bar-fill" style="width:{{ (count / max_count * 100) | int }}%"></div></div>
  </div>
  {% endfor %}
</div>
{% endif %}

<div class="footer">生成时间：{{ generated_at }}</div>
</body>
</html>"""


def render_report(label: str, start: str, end: str, data: dict, narrative: str) -> str:
    from flask import render_template_string
    return render_template_string(
        REPORT_TEMPLATE,
        label=label, start=start, end=end,
        data=data, narrative=narrative,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


# ── 主流程 ───────────────────────────────────────────────────

def generate_report(week_str: str = None) -> str:
    """生成周报，返回 HTML 文件路径。"""
    start, end, label = week_range(week_str)
    print(f"[报告] 生成 {label}（{start} ~ {end}）")

    data      = aggregate(start, end)
    narrative = generate_narrative(data, start, end)

    # Jinja2 需要 Flask app context
    import sys
    sys.path.insert(0, os.path.join(ROOT, "product", "api"))
    import app as flask_app

    with flask_app.app.app_context():
        html = render_report(label, start, end, data, narrative)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"weekly_{label.replace(':', '-')}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[报告] 已写入 {out_path}")
    print(f"  本周阅读: {data['week_read_count']} 篇")
    print(f"  本周笔记: {data['week_notes_count']} 条")
    print(f"  最活跃话题: {data['active_topic']}")
    return out_path


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--week", default=None, help="如 2026-W20，默认本周")
    args = p.parse_args()
    generate_report(args.week)
