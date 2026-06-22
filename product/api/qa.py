"""
问答核心逻辑
- 时间感知：检测"最近N天/周/月"自动换算 days 参数
- 检索：从 db.py 拿文章列表，截取 top-K 摘要拼入 prompt
- LLM：deepseek-v4-flash（快速低成本），复杂推理切 deepseek-v4-pro
- 引用格式：[标题](url) 内联引用
"""
import os
import re
import json
from datetime import datetime

from openai import OpenAI
from db import search_articles, get_article

# ── 环境配置 ─────────────────────────────────────────────────

def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
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

def _client():
    return OpenAI(
        api_key=_ENV.get("LLM_API_KEY", ""),
        base_url=_ENV.get("LLM_BASE_URL", "https://api.deepseek.com/v1"),
    )

QA_MODEL      = _ENV.get("QA_MODEL", "deepseek-v4-flash")
REASON_MODEL  = _ENV.get("REASONING_MODEL", "deepseek-v4-pro")


# ── 时间意图解析 ──────────────────────────────────────────────

_TIME_PATTERNS = [
    (r"最近\s*(\d+)\s*天",   lambda m: int(m.group(1))),
    (r"过去\s*(\d+)\s*天",   lambda m: int(m.group(1))),
    (r"最近\s*(\d+)\s*周",   lambda m: int(m.group(1)) * 7),
    (r"过去\s*(\d+)\s*周",   lambda m: int(m.group(1)) * 7),
    (r"最近\s*(\d+)\s*个月", lambda m: int(m.group(1)) * 30),
    (r"过去\s*(\d+)\s*个月", lambda m: int(m.group(1)) * 30),
    (r"本周",  lambda m: 7),
    (r"本月",  lambda m: 30),
    (r"近期",  lambda m: 30),
]

def _detect_days(question: str):
    """返回 int(天数) 或 None。"""
    for pattern, fn in _TIME_PATTERNS:
        m = re.search(pattern, question)
        if m:
            return fn(m)
    return None


# ── 关键词提取（简单版） ───────────────────────────────────────

_STOPWORDS = {"的", "了", "是", "在", "有", "和", "与", "或", "等", "这", "那", "中",
              "什么", "怎么", "为什么", "如何", "哪些", "哪个", "能", "会", "吗", "呢"}

def _extract_keywords(question: str) -> str:
    """把问题拆成空格分隔的关键词字符串，用于 search_articles。"""
    # 去标点、去停用词，保留长度>=2的词
    tokens = re.findall(r'[一-鿿A-Za-z0-9_\-\.]+', question)
    kws = [t for t in tokens if t not in _STOPWORDS and len(t) >= 2]
    return " ".join(kws[:5]) if kws else question[:20]


# ── 检索 ─────────────────────────────────────────────────────

def _retrieve(question: str, domain: str = "ai-agent", top_k: int = 8):
    """返回与问题最相关的文章列表（card 格式）。"""
    days = _detect_days(question)
    kw   = _extract_keywords(question)

    # 先精准检索
    results = search_articles(query=kw, domain=domain, days=days, limit=top_k)

    # 如果结果不足，补充近期文章
    if len(results) < 3 and days is None:
        recent = search_articles(days=90, limit=top_k - len(results))
        seen = {r["id"] for r in results}
        results += [r for r in recent if r["id"] not in seen]

    return results[:top_k]


# ── Prompt 构建 ───────────────────────────────────────────────

_SYSTEM = """你是一个 AI Agent 领域情报分析师，帮助用户从知识库中获取洞察。

规则：
1. 只基于【参考文章】中的内容回答，不要编造信息。
2. 每个关键观点后附上引用，格式：[文章标题](url)
3. 如果参考文章不能回答问题，明确说明"知识库中暂无相关内容"。
4. 时间相关问题要明确说明文章的发布日期范围。
5. 回答简洁，用中文，重点突出。"""

def _build_prompt(question: str, articles: list) -> str:
    refs = []
    for i, a in enumerate(articles, 1):
        date    = a.get("date", "")
        title   = a.get("title", "")
        url     = a.get("url", "")
        summary = a.get("summary", "") or a.get("takeaway", "")
        refs.append(f"[{i}] ({date}) {title}\n    URL: {url}\n    摘要: {summary}")

    refs_text = "\n\n".join(refs) if refs else "（无相关文章）"
    return f"【参考文章】\n{refs_text}\n\n【问题】\n{question}"


# ── 主入口 ────────────────────────────────────────────────────

def answer_question(question: str, domain: str = "ai-agent",
                    use_reasoning: bool = False) -> dict:
    """
    返回：
    {
        "answer": str,          # markdown 格式回答
        "articles": list[dict], # 引用的文章列表
        "days_detected": int | None,
        "model": str
    }
    """
    articles = _retrieve(question, domain=domain)
    prompt   = _build_prompt(question, articles)
    model    = REASON_MODEL if use_reasoning else QA_MODEL

    client = _client()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )
    answer = resp.choices[0].message.content.strip()

    return {
        "answer":       answer,
        "articles":     articles,
        "days_detected": _detect_days(question),
        "model":        model,
    }


# ── 自测 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    questions = [
        "AI Agent 的 memory 机制有哪些主流方案？",
        "最近30天 Agent 评测方面有什么新进展？",
        "MCP 协议是什么，有哪些实践案例？",
    ]
    for q in questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        result = answer_question(q)
        print(f"检索到 {len(result['articles'])} 篇文章，时间过滤: {result['days_detected']} 天")
        print(f"模型: {result['model']}")
        print(f"\nA: {result['answer'][:300]}...")
