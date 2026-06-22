"""
个性化摘要生成层 (M6)
- 三种角度：engineer / product / beginner
- 预生成并缓存到 article_summaries 表
- 展示时按 user_profile.primary_angle 自动选角度
"""
import os
import json
import sqlite3

from openai import OpenAI

ROOT        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT_DB  = os.path.join(ROOT, "product", "data", "product.sqlite")

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

_ENV    = _load_env()
_MODEL  = _ENV.get("SUMMARY_MODEL", "deepseek-v4-flash")

def _client():
    return OpenAI(
        api_key=_ENV.get("LLM_API_KEY", ""),
        base_url=_ENV.get("LLM_BASE_URL", "https://api.deepseek.com/v1"),
    )

def _conn():
    conn = sqlite3.connect(PRODUCT_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ── 角度 Prompt 定义 ──────────────────────────────────────────

ANGLE_PROMPTS = {
    "engineer": """你是技术工程师，请用3句话总结这篇文章的技术要点：
1. 核心技术方案或实现细节是什么？
2. 与现有方案相比，技术上有什么不同或改进？
3. 有什么坑、限制或值得注意的工程细节？
只输出3句话，不需要标序号，语言简洁专业。""",

    "product": """你是产品经理，请用3句话总结这篇文章的产品洞察：
1. 解决了什么用户/市场问题？
2. 对竞争格局或行业趋势有什么影响？
3. 产品决策者可以从中得到什么 takeaway？
只输出3句话，不需要标序号，面向业务和决策。""",

    "beginner": """你面对的是刚入门的学习者，请用3句简单的语言解释这篇文章：
1. 这篇文章在讲一个什么问题？用生活中的类比帮助理解。
2. 它提出的解决思路是什么？
3. 读完这篇，应该记住哪一件最重要的事？
只输出3句话，避免术语，用类比和比喻。""",
}

ANGLES = list(ANGLE_PROMPTS.keys())


# ── 生成单篇文章的某个角度摘要 ────────────────────────────────

def generate_summary(article_id: str, article_text: str, angle: str) -> str:
    """调用 LLM 生成指定角度摘要，返回摘要文本。"""
    if angle not in ANGLE_PROMPTS:
        raise ValueError(f"未知 angle: {angle}，支持: {ANGLES}")

    system_prompt = ANGLE_PROMPTS[angle]
    user_content  = f"文章内容：\n\n{article_text[:3000]}"  # 截断防 token 超限

    client = _client()
    resp = client.chat.completions.create(
        model=_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_content},
        ],
        max_tokens=400,
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()


# ── 读缓存 / 写缓存 ───────────────────────────────────────────

def get_cached_summary(article_id: str, angle: str):
    """从 article_summaries 读取缓存，没有则返回 None。"""
    conn = _conn()
    row = conn.execute(
        "SELECT summary FROM article_summaries WHERE article_id=? AND angle=?",
        (article_id, angle)
    ).fetchone()
    conn.close()
    return row["summary"] if row else None


def cache_summary(article_id: str, angle: str, summary: str):
    """写入缓存（INSERT OR REPLACE）。"""
    conn = _conn()
    conn.execute(
        "INSERT OR REPLACE INTO article_summaries(article_id, angle, summary) VALUES(?,?,?)",
        (article_id, angle, summary)
    )
    conn.commit()
    conn.close()


# ── 主要接口 ──────────────────────────────────────────────────

def get_summary(article_id: str, angle: str, article_text: str = "") -> str:
    """
    返回指定角度的摘要。
    先查缓存，没有则实时生成并缓存。
    """
    cached = get_cached_summary(article_id, angle)
    if cached:
        return cached

    if not article_text:
        # 尝试从 articles-meta.json 读摘要作为输入
        meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
        with open(meta_path, encoding="utf-8") as f:
            for item in json.load(f):
                if item.get("id") == article_id:
                    article_text = item.get("retrieval_text", "") or item.get("takeaway", "") or item.get("summary_text", "")
                    break

    if not article_text:
        return "（文章内容不足，无法生成摘要）"

    summary = generate_summary(article_id, article_text, angle)
    cache_summary(article_id, angle, summary)
    return summary


def get_all_angles(article_id: str, article_text: str = "") -> dict:
    """返回三种角度的摘要字典（均先查缓存）。"""
    result = {}
    for angle in ANGLES:
        result[angle] = get_summary(article_id, angle, article_text)
    return result


def pregenerate_for_article(article_id: str, article_text: str) -> dict:
    """
    预生成并缓存所有角度摘要。
    在文章采集入库后异步调用。
    返回各角度摘要的字典。
    """
    results = {}
    for angle in ANGLES:
        # 跳过已有缓存
        if get_cached_summary(article_id, angle):
            results[angle] = "[cached]"
            continue
        try:
            s = generate_summary(article_id, article_text, angle)
            cache_summary(article_id, angle, s)
            results[angle] = s
        except Exception as e:
            results[angle] = f"[error: {e}]"
    return results


# ── 自测 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    # 取知识库第一篇文章做测试
    meta_path = os.path.join(ROOT, "knowledge", "retrieval", "articles-meta.json")
    with open(meta_path, encoding="utf-8") as f:
        items = json.load(f)

    if not items:
        print("没有文章")
    else:
        item = items[0]
        aid  = item["id"]
        text = item.get("retrieval_text", "") or item.get("takeaway", "")
        print(f"文章: {item['title'][:60]}")
        print(f"ID: {aid}")
        print()

        for angle in ANGLES:
            print(f"--- [{angle}] ---")
            s = get_summary(aid, angle, text)
            print(s)
            print()
