"""
Flask API 服务
端点：
  GET  /api/articles                    ?query=&domain=&days=&limit=
  GET  /api/articles/<id>
  GET  /api/articles/<id>/summary       ?angle=engineer|product|beginner
  POST /api/qa                          body: {question, domain?, use_reasoning?}
  POST /api/events                      body: {article_id, event_type, payload?}
  GET  /api/notes
  POST /api/notes
  GET  /api/profile
  POST /api/profile/infer               （触发用户模型推断）
  GET  /api/stats/topics

运行：python product/api/app.py
"""
import sys
import os
import hmac
import ipaddress
from urllib.parse import urlparse

# 确保 product/api/ 在 import 路径里
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, send_from_directory
import db
import qa
import user_model
import personalize
import learning
import recommend
import contradiction

# ── 读取 .env 配置 ────────────────────────────────────────────

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

_ENV = _load_env()

WEB_DIR = os.path.join(ROOT, "product", "web")

app = Flask(__name__, static_folder=None)
app.json.ensure_ascii = False  # 允许 JSON 直接输出中文
app.config["MAX_CONTENT_LENGTH"] = int(_ENV.get("MAX_REQUEST_BYTES", 1024 * 1024))


# ── 前端静态文件服务（解决 ES module file:// CORS 问题）────────

@app.get("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")

@app.get("/graph")
def graph_page():
    return send_from_directory(WEB_DIR, "graph.html")

@app.get("/<path:filename>")
def static_files(filename):
    # 只服务 web 目录下的静态资源，不拦截 /api/ 路由
    import pathlib
    target = pathlib.Path(WEB_DIR) / filename
    if target.exists() and target.is_file():
        return send_from_directory(WEB_DIR, filename)
    return jsonify({"ok": False, "error": "not found"}), 404


# ── 工具 ─────────────────────────────────────────────────────

def ok(data):
    return jsonify({"ok": True, "data": data})

def err(msg, code=400):
    return jsonify({"ok": False, "error": msg}), code


def _bounded_text(value, field_name: str, max_len: int):
    value = (value or "").strip()
    if len(value) > max_len:
        raise ValueError(f"{field_name} 不能超过 {max_len} 字符")
    return value


def _is_loopback_remote() -> bool:
    try:
        return ipaddress.ip_address(request.remote_addr or "").is_loopback
    except ValueError:
        return False


def _same_origin_header() -> bool:
    """Block browser cross-site POSTs while still allowing local scripts without Origin."""
    origin = request.headers.get("Origin") or request.headers.get("Referer")
    if not origin:
        return True
    parsed = urlparse(origin)
    expected = urlparse(request.host_url)
    return (parsed.scheme, parsed.netloc) == (expected.scheme, expected.netloc)


def _require_admin():
    configured = _ENV.get("ADMIN_TOKEN", "").strip()
    supplied = request.headers.get("X-Admin-Token", "")
    if configured:
        if hmac.compare_digest(supplied, configured):
            return None
        return err("admin token 无效或缺失", 403)

    # Development fallback: only loopback + same-origin/no-origin clients.
    if _is_loopback_remote() and _same_origin_header():
        return None
    return err("admin endpoint 需要 ADMIN_TOKEN", 403)


@app.before_request
def request_guard():
    if request.method in ("POST", "PUT", "PATCH", "DELETE") and not _same_origin_header():
        return err("跨站请求被拒绝", 403)


# ── 管理 ──────────────────────────────────────────────────────

@app.post("/api/admin/reload")
def admin_reload():
    denied = _require_admin()
    if denied:
        return denied
    db._articles.clear()
    db._load()
    return ok({"reloaded": len(db._articles)})


@app.post("/api/admin/collect")
def admin_collect():
    """异步触发 daily_collect.py，立刻返回，结果写入日志。"""
    denied = _require_admin()
    if denied:
        return denied
    import subprocess, threading, sys
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "daily_collect.py")

    def _run():
        subprocess.run([sys.executable, script], capture_output=True, text=True)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return ok({"started": True, "message": "采集任务已在后台启动，约 30 秒后完成"})


# ── 文章相关 ──────────────────────────────────────────────────

@app.get("/api/articles")
def list_articles():
    try:
        query = _bounded_text(request.args.get("query", ""), "query", 200)
    except ValueError as e:
        return err(str(e))
    domain = request.args.get("domain", None)
    days   = request.args.get("days",  None, type=int)
    limit  = request.args.get("limit", 20,   type=int)
    if days is not None and (days < 1 or days > 3650):
        return err("days 必须在 1 到 3650 之间")
    limit  = min(limit, 100)

    articles = db.search_articles(query=query, domain=domain, days=days, limit=limit)
    return ok({"articles": articles, "total": len(articles)})


@app.get("/api/articles/<article_id>")
def get_article(article_id):
    article = db.get_article(article_id)
    if not article:
        return err("文章不存在", 404)
    db.record_event(article_id, "view_start")
    return ok(article)


@app.get("/api/articles/<article_id>/summary")
def get_article_summary(article_id):
    angle = request.args.get("angle", "engineer")
    if angle not in personalize.ANGLES:
        return err(f"angle 必须是 {personalize.ANGLES} 之一")

    # 需要文章全文 / 摘要作为输入
    article = db.get_article(article_id)
    if not article:
        return err("文章不存在", 404)

    article_text = article.get("full_text", "") or article.get("summary", "")
    summary = personalize.get_summary(article_id, angle, article_text)
    return ok({"article_id": article_id, "angle": angle, "summary": summary})


# ── 问答 ─────────────────────────────────────────────────────

@app.post("/api/qa")
def ask():
    body = request.get_json(silent=True) or {}
    try:
        question = _bounded_text(body.get("question", ""), "question", 2000)
    except ValueError as e:
        return err(str(e))
    if not question:
        return err("question 不能为空")

    domain        = body.get("domain", "ai-agent")
    use_reasoning = body.get("use_reasoning", False)

    result = qa.answer_question(question, domain=domain, use_reasoning=use_reasoning)
    return ok(result)


# ── 事件记录 ─────────────────────────────────────────────────

@app.post("/api/events")
def record_event():
    body = request.get_json(silent=True) or {}
    try:
        article_id = _bounded_text(body.get("article_id", ""), "article_id", 120)
        event_type = _bounded_text(body.get("event_type", ""), "event_type", 80)
    except ValueError as e:
        return err(str(e))
    if not article_id or not event_type:
        return err("article_id 和 event_type 不能为空")

    payload = body.get("payload", {})
    db.record_event(article_id, event_type, payload)

    # 阅读完成或反馈时更新统计 + 重新推断用户模型
    conflict_alert = None
    if event_type == "view_end":
        db.update_read_stats()
        user_model.infer_and_update()
        try:
            conflict_alert = contradiction.check_and_save(article_id)
        except Exception:
            pass
        # 自动将已读文章加入复习队列（后台静默，不阻塞响应）
        try:
            article = db.get_article(article_id)
            if article:
                text = article.get("full_text", "") or article.get("summary", "")
                learning.enqueue_review(article_id, text, article.get("title", ""))
        except Exception:
            pass
    elif event_type.startswith("feedback_"):
        user_model.infer_and_update()

    return ok({"recorded": True, "conflict_alert": conflict_alert})


# ── 笔记 ─────────────────────────────────────────────────────

@app.get("/api/notes")
def get_notes():
    limit = request.args.get("limit", 50, type=int)
    notes = db.get_notes(limit=limit)
    return ok({"notes": notes})


@app.get("/api/notes/<article_id>")
def get_note_for_article(article_id):
    note = db.get_note_for_article(article_id)
    return ok({"note": note})


@app.post("/api/notes")
def save_note():
    body = request.get_json(silent=True) or {}
    try:
        article_id = _bounded_text(body.get("article_id", ""), "article_id", 120)
        note_text = _bounded_text(body.get("note_text", ""), "note_text", 20000)
        note_type = _bounded_text(body.get("note_type", "compression"), "note_type", 40)
    except ValueError as e:
        return err(str(e))
    if not article_id or not note_text:
        return err("article_id 和 note_text 不能为空")

    db.save_note(article_id, note_text, note_type)
    return ok({"saved": True})


# ── 用户画像与统计 ────────────────────────────────────────────

@app.get("/api/profile")
def get_profile():
    profile = user_model.get_profile_summary()
    return ok(profile)


@app.post("/api/profile/infer")
def infer_profile():
    denied = _require_admin()
    if denied:
        return denied
    result = user_model.infer_and_update()
    return ok(result)


@app.get("/api/stats/topics")
def topic_stats():
    stats = db.get_topic_stats()
    return ok({"stats": stats})


@app.get("/api/stats/timeline")
def timeline_stats():
    data = db.get_timeline()
    return ok(data)


# ── 矛盾冲突提醒 (M7+) ──────────────────────────────────────

@app.get("/api/contradiction/alerts")
def get_conflict_alerts():
    limit = request.args.get("limit", 10, type=int)
    alerts = contradiction.get_undismissed_alerts(limit=limit)
    return ok({"alerts": alerts})


@app.post("/api/contradiction/alerts/<int:alert_id>/dismiss")
def dismiss_conflict_alert(alert_id):
    contradiction.dismiss_alert(alert_id)
    return ok({"dismissed": True})


# ── 复习队列 (M7) ────────────────────────────────────────────

@app.get("/api/reviews/due")
def get_due_reviews():
    limit = request.args.get("limit", 10, type=int)
    items = learning.get_due_reviews(limit=limit)
    stats = learning.get_review_stats()
    return ok({"items": items, "stats": stats})


@app.post("/api/reviews/enqueue")
def enqueue_review():
    body       = request.get_json(silent=True) or {}
    article_id = body.get("article_id", "").strip()
    if not article_id:
        return err("article_id 不能为空")

    article = db.get_article(article_id)
    if not article:
        return err("文章不存在", 404)

    text  = article.get("full_text", "") or article.get("summary", "")
    title = article.get("title", "")
    result = learning.enqueue_review(article_id, text, title)
    return ok(result)


@app.post("/api/reviews/<int:queue_id>/submit")
def submit_review(queue_id):
    body   = request.get_json(silent=True) or {}
    result = body.get("result", "")
    if result not in ("remember", "hint", "forgot"):
        return err("result 必须是 remember / hint / forgot")
    try:
        data = learning.submit_review(queue_id, result)
        return ok(data)
    except ValueError as e:
        return err(str(e), 404)


# ── 推荐 (M9) ────────────────────────────────────────────────

@app.get("/api/recommendations")
def get_recommendations():
    top_n = request.args.get("n", 3, type=int)
    recs  = recommend.get_recommendations(top_n=top_n)
    return ok({"recommendations": recs})


# ── 知识图谱数据 (M8) ─────────────────────────────────────────

@app.get("/api/graph")
def get_graph():
    data = recommend.get_graph_data()
    return ok(data)


# ── 周报触发 (M10) ────────────────────────────────────────────

@app.post("/api/report/weekly")
def gen_weekly_report():
    denied = _require_admin()
    if denied:
        return denied
    body     = request.get_json(silent=True) or {}
    week_str = body.get("week", None)   # 如 "2026-W20"，None 则本周
    if week_str is not None:
        try:
            week_str = _bounded_text(week_str, "week", 8)
        except ValueError as e:
            return err(str(e))

    import sys
    sys.path.insert(0, os.path.join(ROOT, "product", "scripts"))
    import weekly_report

    try:
        path = weekly_report.generate_report(week_str)
        fname = os.path.basename(path)
        return ok({"path": path, "filename": fname})
    except Exception as e:
        return err(str(e))


# ── 领域与话题配置 ───────────────────────────────────────────

@app.get("/api/config/domains")
def config_domains():
    import json as _json
    path = os.path.join(ROOT, "product", "config", "domains.json")
    with open(path, encoding="utf-8") as f:
        domains = _json.load(f)["domains"]
    return ok({"domains": [{"id": d["id"], "name": d["name"]} for d in domains]})


@app.get("/api/config/topics")
def config_topics():
    domain_id = request.args.get("domain", "ai-agent")
    import json as _json
    path = os.path.join(ROOT, "product", "config", "domains.json")
    with open(path, encoding="utf-8") as f:
        domains = _json.load(f)["domains"]
    domain = next((d for d in domains if d["id"] == domain_id), domains[0])
    return ok({
        "domain_id":   domain["id"],
        "domain_name": domain["name"],
        "topics":      [{"id": t["id"], "name": t["name"]} for t in domain.get("subtopics", [])]
    })


# ── 健康检查 ─────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return ok({"status": "ok"})


# ── 启动 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    host  = _ENV.get("FLASK_HOST", "127.0.0.1")
    port  = int(_ENV.get("FLASK_PORT", 5000))
    debug = _ENV.get("FLASK_DEBUG", "false").lower() == "true"

    print(f"[API] 启动于 http://{host}:{port}")
    print(f"[API] debug={debug}")
    app.run(host=host, port=port, debug=debug)
