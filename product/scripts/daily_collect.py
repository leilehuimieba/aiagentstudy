"""
每日采集 pipeline
读取 product/config/sources.json，对每个 enabled 源执行抓取 → 质量评分 → 写入知识库。

运行：python product/scripts/daily_collect.py [--dry-run] [--source bestblogs-ai]
"""
import sys
import os
import json
import re
import time
import argparse
import hashlib
from datetime import datetime, date

ROOT        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DIR = os.path.join(ROOT, "product")

# 加载 .env
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

ENV = _load_env()
QUALITY_THRESHOLD = int(ENV.get("COLLECT_QUALITY_THRESHOLD", 6))

# ── 参数解析 ─────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="每日情报采集")
    p.add_argument("--dry-run", action="store_true", help="只打印，不写入")
    p.add_argument("--source",  default=None,        help="只采集指定 source id")
    p.add_argument("--limit",   type=int, default=20, help="每源最多处理条数")
    return p.parse_args()


# ── 配置加载 ─────────────────────────────────────────────────

def load_sources():
    path = os.path.join(PRODUCT_DIR, "config", "sources.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["sources"]

def load_domains():
    path = os.path.join(PRODUCT_DIR, "config", "domains.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["domains"]


# ── 抓取器 ───────────────────────────────────────────────────

def fetch_rss(url: str, limit: int = 20):
    """通用 RSS 抓取，返回 raw item 列表。"""
    import feedparser
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title":   entry.get("title", "").strip(),
            "url":     entry.get("link", ""),
            "summary": entry.get("summary", "") or entry.get("description", ""),
            "date":    _parse_date(entry),
        })
    return items


def fetch_bestblogs(cfg: dict, limit: int = 20):
    """BestBlogs.dev RSS — 直接使用通用 RSS 抓取器。"""
    rss_url = cfg.get("rss_url", "")
    if not rss_url:
        print(f"  [WARN] bestblogs source 缺少 rss_url 配置")
        return []
    return fetch_rss(rss_url, limit=limit)


def fetch_hn(cfg: dict, limit: int = 20):
    """Hacker News Algolia API 按关键词抓取。"""
    import requests
    keywords = cfg.get("keywords", ["AI agent"])
    items = []
    seen = set()
    for kw in keywords:
        url = f"https://hn.algolia.com/api/v1/search?query={kw}&tags=story&hitsPerPage={limit}"
        try:
            resp = requests.get(url, timeout=10)
            hits = resp.json().get("hits", [])
            for h in hits:
                oid = h.get("objectID", "")
                if oid in seen:
                    continue
                seen.add(oid)
                items.append({
                    "title":   h.get("title", "").strip(),
                    "url":     h.get("url", "") or f"https://news.ycombinator.com/item?id={oid}",
                    "summary": h.get("story_text", "") or "",
                    "date":    datetime.utcfromtimestamp(h.get("created_at_i", 0)).strftime("%Y-%m-%d"),
                })
        except Exception as e:
            print(f"  [WARN] HN fetch error for '{kw}': {e}")
    return items[:limit]


FETCHERS = {
    "bestblogs":          fetch_bestblogs,
    "bestblogs_category": fetch_bestblogs,
    "hn":                 fetch_hn,
}

def _parse_date(entry) -> str:
    try:
        from dateutil.parser import parse as dtparse
        published = entry.get("published", "") or entry.get("updated", "")
        if published:
            return dtparse(published).strftime("%Y-%m-%d")
    except Exception:
        pass
    return date.today().strftime("%Y-%m-%d")


# ── 质量评分 ─────────────────────────────────────────────────

def score_article(item: dict) -> int:
    """
    规则评分 0-10，避免 LLM 调用成本。
    超过 QUALITY_THRESHOLD 才写入。
    """
    score = 5  # 基础分
    title   = item.get("title", "")
    summary = item.get("summary", "")
    text    = (title + " " + summary).lower()

    # 加分：AI agent 相关关键词
    hi_value = ["agent", "llm", "mcp", "memory", "reasoning", "benchmark",
                "evaluation", "multi-agent", "tool use", "rag", "context"]
    score += sum(1 for kw in hi_value if kw in text)

    # 减分：低质量信号
    low_value = ["sponsored", "advertisement", "click here", "buy now",
                 "subscribe", "discount", "coupon"]
    score -= sum(1 for kw in low_value if kw in text)

    # 有摘要加分
    if len(summary) > 100:
        score += 1

    return max(0, min(10, score))


# ── 去重 ─────────────────────────────────────────────────────

def _url_fingerprint(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]

def load_existing_urls() -> set:
    """从 articles-meta.json 读取已存在的 URL 集合。"""
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    if not os.path.exists(meta_path):
        return set()
    with open(meta_path, encoding="utf-8") as f:
        items = json.load(f)
    return {item.get("bestblogs_url", "") for item in items if item.get("bestblogs_url")}


# ── 写入知识库 ────────────────────────────────────────────────

def classify_topic(item: dict, domains: list) -> str:
    """基于关键词把文章分到最匹配的 subtopic。"""
    text = (item.get("title", "") + " " + item.get("summary", "")).lower()
    best_domain   = domains[0] if domains else {}
    best_subtopic = "uncategorized"
    best_score    = 0

    for domain in domains:
        for sub in domain.get("subtopics", []):
            hits = sum(1 for kw in sub.get("keywords", []) if kw.lower() in text)
            if hits > best_score:
                best_score    = hits
                best_subtopic = sub["id"]
                best_domain   = domain

    return best_domain.get("id", "ai-agent"), best_subtopic


def write_article(item: dict, topic: str, dry_run: bool = False) -> str:
    """写入 knowledge/items/<topic>/<id>/ 并更新 articles-meta.json。"""
    today = date.today().strftime("%Y-%m-%d")
    uid   = f"COL-{today}-{_url_fingerprint(item['url'])}"
    items_dir = os.path.join(ROOT, "knowledge", "items", topic)
    article_dir = os.path.join(items_dir, uid)

    if dry_run:
        print(f"    [DRY] 写入 {uid} → {topic}")
        return uid

    os.makedirs(article_dir, exist_ok=True)

    # 写 article.md
    md_path = os.path.join(article_dir, "article.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {item['title']}\n\n")
        f.write(f"> 来源：{item['url']}\n\n")
        f.write(item.get("summary", ""))

    # 更新 articles-meta.json
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    with open(meta_path, encoding="utf-8") as f:
        metas = json.load(f)

    metas.append({
        "id":             uid,
        "date":           item.get("date", today),
        "title":          item["title"],
        "source":         item.get("source_id", "collect"),
        "topic":          topic,
        "tags":           [],
        "summary_text":   item.get("summary", "")[:300],
        "takeaway":       "",
        "retrieval_text": item["title"] + " " + item.get("summary", ""),
        "bestblogs_url":  item["url"],
        "article_path":   os.path.relpath(md_path, ROOT).replace("\\", "/"),
    })

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)

    return uid


# ── 主流程 ───────────────────────────────────────────────────

def run(args):
    sources  = load_sources()
    domains  = load_domains()
    existing = load_existing_urls()

    total_new = 0
    total_skip_dup = 0
    total_skip_quality = 0

    for src in sources:
        if not src.get("enabled", False):
            print(f"[SKIP] {src['id']} (disabled)")
            continue
        if args.source and src["id"] != args.source:
            continue

        print(f"\n[SOURCE] {src['id']} — {src.get('name', '')}")

        # 选抓取器
        fetcher_key = src.get("type", "rss")
        fetcher = FETCHERS.get(fetcher_key) or (lambda c, limit: fetch_rss(c.get("rss_url", ""), limit))
        try:
            items = fetcher(src, args.limit)
        except Exception as e:
            print(f"  [ERROR] 抓取失败: {e}")
            continue

        print(f"  抓取 {len(items)} 条")

        for item in items:
            item["source_id"] = src["id"]

            # 去重
            if item["url"] in existing:
                total_skip_dup += 1
                continue

            # 质量过滤
            q = score_article(item)
            if q < QUALITY_THRESHOLD:
                print(f"  [LOW]  score={q} — {item['title'][:60]}")
                total_skip_quality += 1
                continue

            # 分类
            domain_id, subtopic = classify_topic(item, domains)
            topic = subtopic  # 写入具体 subtopic 目录

            # 写入
            uid = write_article(item, topic, dry_run=args.dry_run)
            existing.add(item["url"])
            total_new += 1
            status = "[DRY]" if args.dry_run else "[NEW]"
            print(f"  {status} score={q} → {uid} | {item['title'][:55]}")

            time.sleep(0.1)  # 友好限速

    print(f"\n{'='*50}")
    print(f"完成: +{total_new} 新增 / {total_skip_dup} 重复 / {total_skip_quality} 低质量")
    if args.dry_run:
        print("[DRY-RUN] 未实际写入任何文件")
        return

    if total_new > 0:
        try:
            import urllib.request
            req = urllib.request.Request(
                "http://127.0.0.1:5000/api/admin/reload",
                method="POST", data=b"{}",
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=3)
            print("Flask 知识库已热重载")
        except Exception:
            print("Flask 未运行，下次启动时自动加载新文章")


if __name__ == "__main__":
    args = parse_args()
    run(args)
