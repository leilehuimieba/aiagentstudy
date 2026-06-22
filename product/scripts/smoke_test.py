"""
冒烟测试 — 开发前环境验证
运行：python product/scripts/smoke_test.py
全部 PASS 才能开始写业务代码
"""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DIR = os.path.join(ROOT, "product")

passed = []
failed = []

def check(name, fn):
    try:
        fn()
        passed.append(name)
        print(f"  PASS  {name}")
    except Exception as e:
        failed.append(name)
        print(f"  FAIL  {name}: {e}")


# ── 1. Python 依赖 ────────────────────────────────────────────
print("\n[1] Python 依赖")

def check_openai_sdk():
    import openai
    assert openai.__version__

def check_feedparser():
    import feedparser
    assert feedparser.__version__

def check_dateutil():
    from dateutil.parser import parse
    parse("2026-05-19")

def check_flask():
    import flask
    assert flask

def check_requests():
    import requests
    assert requests

check("openai SDK（用于 DeepSeek）", check_openai_sdk)
check("feedparser", check_feedparser)
check("python-dateutil", check_dateutil)
check("flask", check_flask)
check("requests", check_requests)

# ── 2. 数据文件 ───────────────────────────────────────────────
print("\n[2] 数据文件")

def check_kb_sqlite():
    import sqlite3
    db_path = os.path.join(ROOT, "knowledge", "retrieval", "kb.sqlite")
    assert os.path.exists(db_path), f"not found: {db_path}"
    db = sqlite3.connect(db_path)
    count = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    db.close()
    assert count > 100, f"too few items: {count}"

def check_articles_meta():
    import json
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    assert os.path.exists(meta_path), f"not found: {meta_path}"
    with open(meta_path, encoding="utf-8") as f:
        items = json.load(f)
    assert len(items) > 100, f"too few items: {len(items)}"

def check_items_dir():
    items_dir = os.path.join(ROOT, "knowledge", "items")
    assert os.path.isdir(items_dir)
    topics = os.listdir(items_dir)
    assert len(topics) >= 4, f"too few topics: {topics}"

check("kb.sqlite 可访问", check_kb_sqlite)
check("articles-meta.json 可读", check_articles_meta)
check("knowledge/items/ 目录存在", check_items_dir)

# ── 3. 内存搜索能力 ───────────────────────────────────────────
print("\n[3] 搜索能力")

def check_memory_search():
    import json
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    with open(meta_path, encoding="utf-8") as f:
        items = json.load(f)
    results = [i for i in items if "agent" in i.get("retrieval_text", "").lower()]
    assert len(results) > 20, f"search returned too few: {len(results)}"

def check_time_filter():
    import json
    from datetime import datetime, timedelta
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    with open(meta_path, encoding="utf-8") as f:
        items = json.load(f)
    cutoff = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    recent = [i for i in items if i.get("date", "") >= cutoff]
    assert len(recent) > 0, "no recent items found"

check("关键词内存搜索", check_memory_search)
check("时间范围过滤", check_time_filter)

# ── 4. 配置文件 ───────────────────────────────────────────────
print("\n[4] 配置文件")

def check_sources_json():
    import json
    path = os.path.join(PRODUCT_DIR, "config", "sources.json")
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    assert "sources" in cfg
    assert len(cfg["sources"]) > 0

def check_domains_json():
    import json
    path = os.path.join(PRODUCT_DIR, "config", "domains.json")
    assert os.path.exists(path)
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    assert "domains" in cfg
    assert len(cfg["domains"]) > 0
    total_subtopics = 0
    for d in cfg["domains"]:
        assert "subtopics" in d, f"domain missing subtopics: {d.get('id')}"
        total_subtopics += len(d["subtopics"])
    assert total_subtopics >= 5, f"too few subtopics: {total_subtopics}"

check("sources.json 格式正确", check_sources_json)
check("domains.json 格式正确", check_domains_json)

# ── 5. API Key + LLM 连通性 ──────────────────────────────────
print("\n[5] API Key 与 LLM 连通性")

def check_api_key():
    env_path = os.path.join(PRODUCT_DIR, ".env")
    if not os.path.exists(env_path):
        raise Exception(".env 文件不存在，请复制 .env.template 并填入真实 key")
    content = open(env_path, encoding='utf-8').read()
    if "sk-你的真实key" in content:
        raise Exception(".env 中 LLM_API_KEY 是模板占位符，未填入真实值")
    if "LLM_API_KEY=" not in content:
        raise Exception(".env 中未找到 LLM_API_KEY")

def check_llm_connectivity():
    env_path = os.path.join(PRODUCT_DIR, ".env")
    cfg = {}
    for line in open(env_path, encoding='utf-8').read().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    from openai import OpenAI

    client = OpenAI(
        api_key=cfg.get("LLM_API_KEY", ""),
        base_url=cfg.get("LLM_BASE_URL", "https://api.deepseek.com/v1"),
    )
    # 用 flash 做连通测试（快速低成本）
    model = cfg.get("QA_MODEL", "deepseek-v4-flash")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in one word"}],
        max_tokens=500,
    )
    reply = resp.choices[0].message.content.strip()
    assert reply, f"LLM 返回空内容 (model={model})"

check("LLM_API_KEY 已配置", check_api_key)
check("DeepSeek API 连通性（真实调用）", check_llm_connectivity)

# ── 6. product/data 目录 ─────────────────────────────────────
print("\n[6] 目录结构")

def check_product_dirs():
    for d in ["api", "web", "web/js", "scripts", "config", "data"]:
        path = os.path.join(PRODUCT_DIR, d)
        assert os.path.isdir(path), f"missing dir: {path}"

check("product/ 子目录完整", check_product_dirs)

# ── 结果汇总 ─────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"结果：{len(passed)} PASS / {len(failed)} FAIL")
if failed:
    print(f"\n需要修复：")
    for f in failed:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("\n[OK] 所有检查通过，可以开始开发")
