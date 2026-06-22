import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "knowledge" / "retrieval" / "kb.sqlite"
RRF_K = 60
ALL_TOPICS = [
    "01-context-memory",
    "02-tools-actions",
    "03-control-loop",
    "04-evaluation-guardrails",
    "05-security-techniques",
    "06-frontier-radar",
]


STOP_PHRASES = [
    "是什么",
    "什么是",
    "有什么",
    "有何",
    "如何",
    "怎么",
    "怎样",
    "是否",
    "可以",
    "一个",
    "一种",
    "一下",
    "这个",
    "那个",
    "请问",
]

TOKEN_SYNONYMS = {
    "agent": ["智能体", "ai-agent", "agentic"],
    "智能体": ["agent", "ai-agent", "agentic"],
    "memory": ["记忆", "长期记忆", "working memory", "context"],
    "记忆": ["memory", "长期记忆", "working memory", "context"],
    "context": ["上下文", "context engineering"],
    "上下文": ["context", "context engineering"],
    "评估": ["evaluation", "评测", "验证", "benchmark"],
    "evaluation": ["评估", "评测", "验证", "benchmark"],
    "可靠": ["可靠性", "reliability", "guardrails"],
    "可靠性": ["可靠", "reliability", "guardrails"],
    "reliability": ["可靠", "可靠性", "guardrails"],
    "guardrails": ["可靠性", "评估", "验证"],
    "workflow": ["工作流", "orchestration"],
    "orchestration": ["编排", "workflow", "多 agent"],
    "multi-agent": ["多 agent", "multi agent", "多智能体"],
    "多智能体": ["multi-agent", "multi agent", "多 agent"],
    "机器学习": ["machine learning", "ml"],
    "完成": ["finished", "done", "complete", "completion", "actually finished"],
    "任务": ["task", "tasks"],
    "浏览器": ["browser"],
    "自动化": ["automation", "automated"],
    "登录状态": ["login state", "logged-in", "cookies", "session"],
}

PHRASE_SYNONYMS = {
    "auto mode": ["自动模式"],
    "claude code auto mode": ["claude code 自动模式", "Claude Code 自动模式"],
}

TOPIC_HINTS = {
    "01-context-memory": [
        "memory",
        "记忆",
        "context",
        "上下文",
        "rag",
        "retrieval",
        "检索",
        "knowledge base",
        "知识库",
        "compression",
        "压缩",
    ],
    "02-tools-actions": [
        "tool",
        "tools",
        "工具",
        "browser",
        "浏览器",
        "opencli",
        "cli",
        "api",
        "mcp",
        "automation",
        "自动化",
        "container",
        "containers",
        "sandbox",
    ],
    "03-control-loop": [
        "loop",
        "control",
        "控制",
        "harness",
        "runtime",
        "workflow",
        "orchestration",
        "编排",
        "subagent",
        "多智能体",
        "agent",
        "智能体",
    ],
    "04-evaluation-guardrails": [
        "eval",
        "evaluation",
        "评估",
        "评测",
        "验证",
        "guardrail",
        "guardrails",
        "reliability",
        "可靠",
        "benchmark",
        "安全",
        "完成",
        "finished",
    ],
    "05-security-techniques": [
        "ctf",
        "漏洞",
        "exploit",
        "pentest",
        "security technique",
        "攻防",
    ],
    "06-frontier-radar": [
        "model",
        "模型",
        "benchmark",
        "paper",
        "论文",
        "frontier",
        "生态",
        "发布",
        "趋势",
        "product",
    ],
}

RELATED_TOPICS = {
    "01-context-memory": ["03-control-loop", "04-evaluation-guardrails"],
    "02-tools-actions": ["03-control-loop", "04-evaluation-guardrails"],
    "03-control-loop": ["02-tools-actions", "04-evaluation-guardrails", "01-context-memory"],
    "04-evaluation-guardrails": ["03-control-loop", "02-tools-actions"],
    "05-security-techniques": ["04-evaluation-guardrails", "02-tools-actions"],
    "06-frontier-radar": ["02-tools-actions", "04-evaluation-guardrails"],
}


def concept_keys(concepts):
    return {variant.casefold() for variants in concepts for variant in variants}


def is_definitional_query(raw_query: str, concepts) -> bool:
    lowered = raw_query.casefold()
    keys = concept_keys(concepts)
    asks_definition = any(phrase in lowered for phrase in ("是什么", "什么是"))
    asks_agent = "agent" in keys or "智能体" in keys
    return len(concepts) <= 3 and (asks_definition or asks_agent)


def has_eval_intent(raw_query: str, concepts) -> bool:
    lowered = raw_query.casefold()
    keys = concept_keys(concepts)
    return any(
        token in lowered or token in keys
        for token in ("评估", "评测", "验证", "可靠", "可靠性", "evaluation", "reliability", "guardrails")
    )


def has_howto_intent(raw_query: str) -> bool:
    lowered = raw_query.casefold()
    return any(token in lowered for token in ("如何", "怎么", "怎样", "实践", "落地"))


def detect_query_intent(raw_query: str):
    lowered = raw_query.casefold()
    concepts = extract_query_concepts(raw_query)
    if any(token in lowered for token in ("证据", "出处", "来源", "source", "original", "引用", "原文")):
        return "evidence"
    if any(token in lowered for token in ("对比", "比较", "区别", "差异", " vs ", " versus ", "compare")):
        return "comparison"
    if any(token in lowered for token in ("最新", "最近", "趋势", "发布", "frontier", "release", "ecosystem")):
        return "frontier"
    if has_eval_intent(raw_query, concepts):
        return "evaluation"
    if has_howto_intent(raw_query):
        return "howto"
    if is_definitional_query(raw_query, concepts):
        return "definition"
    return "lookup"


def resolve_query_profile(profile, mode, raw_query, explicit_limit, expand_topic):
    intent = detect_query_intent(raw_query)
    defaults = {
        "standard": (5, False),
        "brief": (3, False),
        "deep": (10, True),
        "evidence": (8, True),
    }
    auto_defaults = {
        "definition": (4, False),
        "lookup": (5, False),
        "howto": (6, True),
        "evaluation": (6, True),
        "comparison": (8, True),
        "evidence": (8, True),
        "frontier": (8, True),
    }

    if profile == "auto":
        suggested_limit, suggested_expand = auto_defaults[intent]
    else:
        suggested_limit, suggested_expand = defaults[profile]

    if mode == "pack" and profile == "standard":
        suggested_limit = 5

    limit = explicit_limit if explicit_limit is not None else suggested_limit
    return limit, bool(expand_topic or suggested_expand), intent


def infer_topics(raw_query: str, requested_topic=None, expand_topic=False):
    if requested_topic and not expand_topic:
        return [requested_topic]
    if not requested_topic and not expand_topic:
        return None

    lowered = raw_query.casefold()
    concepts = extract_query_concepts(raw_query)
    keys = concept_keys(concepts)
    scores = {}
    for topic, hints in TOPIC_HINTS.items():
        score = 0
        for hint in hints:
            hint_key = hint.casefold()
            if hint_key in lowered or hint_key in keys:
                score += 2
            elif any(hint_key in key or key in hint_key for key in keys if len(key) >= 3):
                score += 1
        if score:
            scores[topic] = score

    ordered = [topic for topic, _score in sorted(scores.items(), key=lambda item: (-item[1], ALL_TOPICS.index(item[0])))]

    if requested_topic:
        topics = [requested_topic]
        for topic in ordered:
            if topic not in topics:
                topics.append(topic)
        for topic in RELATED_TOPICS.get(requested_topic, []):
            if topic not in topics and (topic in ordered or len(topics) < 3):
                topics.append(topic)
        return topics[:4]

    return ordered[:3]


def rerank_rows(rows, raw_query: str, limit: int):
    concepts = extract_query_concepts(raw_query)
    if not rows:
        return rows

    definitional = is_definitional_query(raw_query, concepts)
    eval_intent = has_eval_intent(raw_query, concepts)
    howto_intent = has_howto_intent(raw_query)

    for row in rows:
        title = (row.get("title") or "").casefold()
        takeaway = (row.get("takeaway") or "").casefold()
        reusable_principle = (row.get("reusable_principle") or "").casefold()
        tags = " ".join(row.get("tags") or []).casefold()
        blocks = " ".join(row.get("blocks") or []).casefold()
        source = (row.get("source") or "").casefold()
        topic = row.get("topic") or ""
        block_count = len(row.get("blocks") or [])

        bonus = 0.0

        for variants in concepts:
            lowered_variants = [variant.casefold() for variant in variants]
            if any(variant in title for variant in lowered_variants):
                bonus += 3.0
            elif any(variant in tags for variant in lowered_variants):
                bonus += 1.75
            elif any(variant in takeaway for variant in lowered_variants):
                bonus += 1.0

        if definitional:
            if topic in {"03-control-loop", "01-context-memory", "04-evaluation-guardrails"}:
                bonus += 2.0
            if "topic" in source:
                bonus += 1.25
            bonus += min(block_count, 5) * 0.55
            if any(term in title for term in ("agent", "智能体", "agentic", "harness", "context engineering", "memory")):
                bonus += 2.5
            if any(term in title for term in ("组成部分", "技术栈", "架构", "系统", "编排")):
                bonus += 2.0
            if any(term in tags for term in ("ai-agent", "agent-memory", "context-engineering", "harness-engineering", "multi-agent")):
                bonus += 2.0
            if any(term in takeaway for term in ("goal", "context", "memory", "tool", "control loop", "智能体", "agent")):
                bonus += 1.25
            if any(term in reusable_principle for term in ("model", "agent", "智能体", "workflow", "control loop", "context")):
                bonus += 0.75
            if any(term in blocks for term in ("control loop", "context/state", "memory", "goal", "evaluation/guardrails")):
                bonus += 1.5
            if topic == "06-frontier-radar":
                bonus -= 1.0

        if eval_intent:
            if topic == "04-evaluation-guardrails":
                bonus += 2.5
            if any(term in title for term in ("评估", "评测", "可靠", "reliability", "evaluation", "guardrail")):
                bonus += 2.0
            if any(term in tags for term in ("ai-eval", "可靠性", "评估", "benchmark")):
                bonus += 1.25
            if "evaluation/guardrails" in blocks:
                bonus += 1.75

        if eval_intent and howto_intent:
            if "topic" in source:
                bonus += 2.75
            bonus += min(block_count, 5) * 0.65
            if any(term in title for term in ("指南", "完全指南", "横评", "memory", "context engineering", "harness")):
                bonus += 1.75
            if any(
                term in reusable_principle
                for term in ("评估", "权限", "日志", "验证", "rollback", "budget", "隔离", "reliability", "guardrail")
            ):
                bonus += 1.5
            if any(term in takeaway for term in ("permissions", "verification", "rollback", "reliability", "治理", "评估")):
                bonus += 1.25
            if any(term in title for term in ("危机", "故障", "事故", "outage", "incident")):
                bonus -= 2.25

        row["score"] = round(float(row["score"]) + bonus, 6)

    rows.sort(key=lambda row: (-row["score"], row["id"]))
    return rows[:limit]


def normalize_text(text: str) -> str:
    text = text.strip()
    for phrase in STOP_PHRASES:
        text = text.replace(phrase, " ")
    return re.sub(r"\s+", " ", text).strip()


def extract_query_concepts(raw_query: str):
    cleaned = normalize_text(raw_query)
    if not cleaned:
        return []

    concepts = []
    seen = set()

    def push_concept(variants):
        deduped = []
        local_seen = set()
        for variant in variants:
            variant = variant.strip()
            if not variant:
                continue
            key = variant.casefold()
            if key in local_seen:
                continue
            local_seen.add(key)
            deduped.append(variant)
        concept_key = tuple(v.casefold() for v in deduped)
        if not concept_key or concept_key in seen:
            return
        seen.add(concept_key)
        concepts.append(deduped)

    lowered_cleaned = cleaned.casefold()
    for phrase, extras in PHRASE_SYNONYMS.items():
        if phrase in lowered_cleaned:
            push_concept([phrase, *extras])

    for match in re.finditer(r"[A-Za-z0-9][A-Za-z0-9_.:+/#-]*|[\u4e00-\u9fff]{2,}", cleaned):
        token = match.group(0).strip().replace('"', " ")
        if not token:
            continue

        def add_variant(value):
            if value and value not in variants:
                variants.append(value)

        lowered = token.casefold()
        variants = [token]
        for extra in TOKEN_SYNONYMS.get(lowered, []):
            add_variant(extra)

        # For long Chinese phrases, keep a few short semantic chunks as recall helpers.
        if re.fullmatch(r"[\u4e00-\u9fff]{4,}", token):
            for size in (2, 3, 4):
                for i in range(0, len(token) - size + 1):
                    chunk = token[i : i + size]
                    add_variant(chunk)
                    for extra in TOKEN_SYNONYMS.get(chunk.casefold(), []):
                        add_variant(extra)

        push_concept(variants)
    return concepts


def build_match_query(raw_query: str) -> str:
    concepts = extract_query_concepts(raw_query)
    if not concepts:
        return ""
    groups = []
    for variants in concepts:
        if len(variants) == 1:
            groups.append(f'"{variants[0]}"')
        else:
            groups.append("(" + " OR ".join(f'"{variant}"' for variant in variants) + ")")
    return " AND ".join(groups)


def connect():
    if not DB_PATH.exists():
        raise SystemExit(
            "Missing knowledge/retrieval/kb.sqlite. Run:\n"
            "1. node knowledge\\raw\\build-kb-retrieval.js\n"
            "2. python knowledge\\raw\\build-kb-fts.py"
        )
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def hydrate_item(con, item_id):
    row = con.execute(
        """
        SELECT
            id, date, title, source, topic, status, summary_path, article_path,
            source_path, bestblogs_url, original_url, takeaway, reusable_principle,
            blocks_json, tags_json
        FROM items
        WHERE id = ?
        """,
        [item_id],
    ).fetchone()
    if not row:
        return None
    item = dict(row)
    item["blocks"] = json.loads(item.pop("blocks_json"))
    item["tags"] = json.loads(item.pop("tags_json"))
    return item


def rrf(rank):
    return 1.0 / (RRF_K + rank)


def topic_clause(column, topics):
    if not topics:
        return "", []
    placeholders = ", ".join("?" for _ in topics)
    return f" AND {column} IN ({placeholders})", list(topics)


def search_items(con, query, limit, topics=None):
    match_query = build_match_query(query)
    if not match_query:
        return []
    candidate_limit = max(limit * 8, 20)

    sql = """
        SELECT
            items.id,
            items.date,
            items.title,
            items.source,
            items.topic,
            items.status,
            items.summary_path,
            items.article_path,
            items.source_path,
            items.bestblogs_url,
            items.original_url,
            items.takeaway,
            items.reusable_principle,
            items.blocks_json,
            items.tags_json,
            bm25(items_fts, 8.0, 3.0, 2.0, 2.0, 2.0, 1.5, 2.5, 1.0, 0.5, 0.2, 0.1) AS bm25_score,
            snippet(items_fts, 11, '[', ']', ' ... ', 18) AS snippet_text
        FROM items_fts
        JOIN items ON items_fts.rowid = items.rowid
        WHERE items_fts MATCH ?
    """
    params = [match_query]
    clause, topic_params = topic_clause("items.topic", topics)
    sql += clause
    params.extend(topic_params)
    sql += " ORDER BY bm25_score, items.id LIMIT ?"
    params.append(candidate_limit)

    rows = []
    for rank, row in enumerate(con.execute(sql, params), start=1):
        item = dict(row)
        item["blocks"] = json.loads(item.pop("blocks_json"))
        item["tags"] = json.loads(item.pop("tags_json"))
        item["bm25_score"] = round(-1.0 * item.pop("bm25_score"), 6)
        item["rank"] = rank
        item["match_scope"] = "item"
        rows.append(item)
    return rows


def search_chunks(con, query, limit, topics=None):
    match_query = build_match_query(query)
    if not match_query:
        return []
    candidate_limit = max(limit * 16, 40)

    sql = """
        SELECT
            chunks.item_id,
            chunks.ordinal,
            chunks.heading,
            bm25(chunks_fts, 4.0, 2.0, 1.5, 1.0, 0.7) AS bm25_score,
            snippet(chunks_fts, 5, '[', ']', ' ... ', 24) AS snippet_text
        FROM chunks_fts
        JOIN chunks ON chunks_fts.rowid = chunks.rowid
        WHERE chunks_fts MATCH ?
    """
    params = [match_query]
    clause, topic_params = topic_clause("chunks.topic", topics)
    sql += clause
    params.extend(topic_params)
    sql += " ORDER BY bm25_score, chunks.item_id, chunks.ordinal LIMIT ?"
    params.append(candidate_limit)

    rows = []
    for rank, row in enumerate(con.execute(sql, params), start=1):
        item = dict(row)
        item["bm25_score"] = round(-1.0 * item.pop("bm25_score"), 6)
        item["rank"] = rank
        item["match_scope"] = "chunk"
        rows.append(item)
    return rows


def fuse_item_and_chunk_hits(con, item_hits, chunk_hits, limit, raw_query):
    fused = {}

    for hit in item_hits:
        item_id = hit["id"]
        entry = fused.setdefault(
            item_id,
            {
                "score": 0.0,
                "item_rank": None,
                "chunk_rank": None,
                "snippet_text": "",
                "matched_heading": "",
                "match_scope": "item",
            },
        )
        entry["score"] += rrf(hit["rank"])
        entry["item_rank"] = hit["rank"]
        if not entry["snippet_text"]:
            entry["snippet_text"] = hit.get("snippet_text") or ""

    for hit in chunk_hits:
        item_id = hit["item_id"]
        entry = fused.setdefault(
            item_id,
            {
                "score": 0.0,
                "item_rank": None,
                "chunk_rank": None,
                "snippet_text": "",
                "matched_heading": "",
                "match_scope": "chunk",
            },
        )
        if entry["chunk_rank"] is None:
            entry["score"] += rrf(hit["rank"])
            entry["chunk_rank"] = hit["rank"]
            entry["matched_heading"] = hit.get("heading") or ""
            entry["match_scope"] = "item+chunk" if entry["item_rank"] else "chunk"
            if hit.get("snippet_text"):
                heading = hit.get("heading") or "Article"
                entry["snippet_text"] = f"{heading}: {hit['snippet_text']}"

    rows = []
    for item_id, fusion in fused.items():
        item = hydrate_item(con, item_id)
        if not item:
            continue
        item["score"] = round(fusion["score"] * 1000, 6)
        item["snippet_text"] = fusion["snippet_text"]
        item["match_scope"] = fusion["match_scope"]
        if fusion["matched_heading"]:
            item["matched_heading"] = fusion["matched_heading"]
        rows.append(item)

    rows.sort(key=lambda row: (-row["score"], row["id"]))
    return rerank_rows(rows, raw_query, limit)


def fallback_scan(con, query, limit, topics=None):
    lower = query.casefold()
    concepts = extract_query_concepts(query)
    terms = [variant.casefold() for variants in concepts for variant in variants]
    sql = """
        SELECT
            id, date, title, source, topic, status, summary_path, article_path,
            source_path, bestblogs_url, original_url, takeaway, reusable_principle,
            blocks_json, tags_json, retrieval_text
        FROM items
    """
    params = []
    if topics:
        placeholders = ", ".join("?" for _ in topics)
        sql += f" WHERE topic IN ({placeholders})"
        params.extend(topics)

    scored = []
    for row in con.execute(sql, params):
        item = dict(row)
        haystack = " ".join(
            [
                item["title"] or "",
                item["source"] or "",
                item["topic"] or "",
                item["takeaway"] or "",
                item["reusable_principle"] or "",
                item["retrieval_text"] or "",
            ]
        ).casefold()
        if lower in haystack:
            score = 1.0
        else:
            matched_terms = [term for term in terms if term in haystack]
            if not matched_terms:
                continue
            score = float(len(matched_terms))
        matched_concepts = 0
        for variants in concepts:
            if any(variant.casefold() in haystack for variant in variants):
                matched_concepts += 1
        score += matched_concepts * 1.5
        if lower not in haystack and terms:
            if not any(term in (item["title"] or "").casefold() for term in terms):
                score -= 0.25
        if score <= 0:
            continue
        if lower in (item["title"] or "").casefold():
            score += 5.0
        else:
            score += sum(1.5 for term in terms if term in (item["title"] or "").casefold())
        score += sum(
            1.5
            for variants in concepts
            if any(variant.casefold() in (item["title"] or "").casefold() for variant in variants)
        )
        if lower in (item["takeaway"] or "").casefold():
            score += 2.0
        else:
            score += sum(0.5 for term in terms if term in (item["takeaway"] or "").casefold())
        score += sum(
            0.75
            for variants in concepts
            if any(variant.casefold() in (item["takeaway"] or "").casefold() for variant in variants)
        )
        item["blocks"] = json.loads(item.pop("blocks_json"))
        item["tags"] = json.loads(item.pop("tags_json"))
        item["score"] = score
        item["snippet_text"] = item["takeaway"] or item["reusable_principle"] or ""
        item.pop("retrieval_text")
        scored.append(item)

    scored.sort(key=lambda row: (-row["score"], row["id"]))
    return rerank_rows(scored, query, limit)


def select_rows(con, query, limit, topic=None, expand_topic=False):
    topics = infer_topics(query, topic, expand_topic)
    item_hits = search_items(con, query, limit, topics)
    chunk_hits = search_chunks(con, query, limit, topics)
    rows = fuse_item_and_chunk_hits(con, item_hits, chunk_hits, limit, query)
    if not rows:
        rows = fallback_scan(con, query, limit, topics)
    return rows, topics


def format_pack_doc(row, index, role=None):
    lines = [
        f"[Doc {index}]",
        f"ID: {row['id']}",
        f"Title: {row['title']}",
        f"Source: {row['source']}",
        f"Topic: {row['topic']}",
        f"Blocks: {', '.join(row['blocks'])}",
        f"Tags: {', '.join(row['tags']) if row['tags'] else 'none'}",
        f"Takeaway: {row['takeaway'] or 'n/a'}",
        f"Reusable Principle: {row['reusable_principle'] or 'n/a'}",
        f"Match Scope: {row.get('match_scope') or 'n/a'}",
        f"Summary Path: {row['summary_path']}",
        f"Deep Read Path: {row['article_path']}",
        f"Evidence Path: {row['source_path']}",
    ]
    if role:
        lines.insert(1, f"Role: {role}")
    return lines


def grouped_rows(rows, intent):
    if not rows:
        return []

    core_count = 2 if intent == "evidence" else 3
    groups = []
    used = set()

    core = rows[:core_count]
    if core:
        groups.append(("Core Matches", "Best first-read candidates for answering the query.", core))
        used.update(row["id"] for row in core)

    evidence = []
    if intent == "evidence":
        for row in rows:
            if row["id"] in used:
                continue
            if row.get("original_url") or row.get("bestblogs_url"):
                evidence.append(row)
                used.add(row["id"])
            if len(evidence) >= 3:
                break
    if evidence:
        groups.append(("Evidence Sources", "Items worth opening when provenance or source links matter.", evidence))

    background = [row for row in rows if row["id"] not in used]
    if background:
        groups.append(("Related Background", "Useful supporting context after the core matches.", background))

    return groups


def pack_text(query, rows, topics=None, profile="standard", intent="lookup"):
    lines = [
        "KB_CONTEXT_PACK_V1",
        f"Query: {query}",
        f"Query Profile: {profile}",
        f"Query Intent: {intent}",
        f"Topic Filter: {', '.join(topics) if topics else 'none'}",
        f"Documents: {len(rows)}",
        "Read Policy: summary-first; open article.md only for evidence or deep reading.",
        "",
    ]
    for i, row in enumerate(rows, start=1):
        lines.extend(format_pack_doc(row, i))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def grouped_pack_text(query, rows, topics=None, profile="standard", intent="lookup"):
    lines = [
        "KB_GROUPED_CONTEXT_PACK_V1",
        f"Query: {query}",
        f"Query Profile: {profile}",
        f"Query Intent: {intent}",
        f"Topic Filter: {', '.join(topics) if topics else 'none'}",
        f"Documents: {len(rows)}",
        "Read Policy: read Core Matches first; open source.md/article.md only when evidence or deep reading is needed.",
        "",
    ]

    doc_index = 1
    for group_name, group_note, group_items in grouped_rows(rows, intent):
        lines.extend([f"## {group_name}", group_note, ""])
        for row in group_items:
            lines.extend(format_pack_doc(row, doc_index, group_name))
            lines.append("")
            doc_index += 1
    return "\n".join(lines).rstrip() + "\n"


def print_text(query, rows, topics=None, profile="standard", intent="lookup"):
    print(f"Query: {query}")
    if profile != "standard" or intent != "lookup":
        print(f"Query Profile: {profile}")
        print(f"Query Intent: {intent}")
    if topics:
        print(f"Topic Filter: {', '.join(topics)}")
    print(f"Hits: {len(rows)}")
    print("")
    for i, row in enumerate(rows, start=1):
        print(f"{i}. {row['id']} [{row['topic']}] score={row['score']}")
        print(f"   Title: {row['title']}")
        print(f"   Source: {row['source']}")
        print(f"   Blocks: {', '.join(row['blocks'])}")
        if row["tags"]:
            print(f"   Tags: {', '.join(row['tags'])}")
        if row["takeaway"]:
            print(f"   Takeaway: {row['takeaway']}")
        if row["snippet_text"]:
            print(f"   Match: {row['snippet_text']}")
        if row.get("match_scope"):
            print(f"   Match Scope: {row['match_scope']}")
        print(f"   Summary: {row['summary_path']}")
        print(f"   Article: {row['article_path']}")
        print(f"   Source Doc: {row['source_path']}")
        print(f"   Source URL: {row['bestblogs_url']}")
        if row["original_url"]:
            print(f"   Original: {row['original_url']}")
        print("")


def main():
    parser = argparse.ArgumentParser(description="Query the local AI agent knowledge base.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, help="Maximum number of hits")
    parser.add_argument("--topic", help="Optional topic directory filter, e.g. 01-context-memory")
    parser.add_argument(
        "--profile",
        choices=["standard", "brief", "deep", "evidence", "auto"],
        default="standard",
        help="Result strategy. standard preserves old behavior; auto infers limit and topic expansion from query intent.",
    )
    parser.add_argument(
        "--expand-topic",
        action="store_true",
        help="Expand an explicit topic filter to likely related topics based on query hints",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument("--grouped", action="store_true", help="Group pack output into core, background, and evidence sections")
    parser.add_argument(
        "--mode",
        choices=["search", "pack"],
        default="search",
        help="search: human-readable search results; pack: stable low-variance context pack for model input",
    )
    args = parser.parse_args()

    limit, expand_topic, intent = resolve_query_profile(
        args.profile,
        args.mode,
        args.query,
        args.limit,
        args.expand_topic,
    )
    if not args.topic and args.profile in {"auto", "deep", "evidence"} and not args.expand_topic:
        expand_topic = False

    con = connect()
    rows, topics = select_rows(con, args.query, limit, args.topic, expand_topic)
    con.close()

    if args.mode == "pack":
        if args.grouped:
            print(grouped_pack_text(args.query, rows, topics, args.profile, intent), end="")
        else:
            print(pack_text(args.query, rows, topics, args.profile, intent), end="")
    elif args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_text(args.query, rows, topics, args.profile, intent)


if __name__ == "__main__":
    main()
