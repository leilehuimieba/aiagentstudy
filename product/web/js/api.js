// Flask API client — window.api (IIFE, no ES module required)
(function () {
  async function _fetch(path, opts = {}) {
    const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
    const adminToken = window.localStorage && window.localStorage.getItem("ADMIN_TOKEN");
    if (adminToken) headers["X-Admin-Token"] = adminToken;
    const res = await fetch(path, {
      ...opts,
      headers,
    });
    const json = await res.json();
    if (!json.ok) throw new Error(json.error || "API error");
    return json.data;
  }

  window.api = {
    // ── 文章 ──────────────────────────────────────────────────
    listArticles(params = {}) {
      const q = new URLSearchParams(
        Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ""))
      );
      return _fetch(`/api/articles?${q}`);
    },

    getArticle: (id) => _fetch(`/api/articles/${id}`),

    getAngleSummary: (id, angle) =>
      _fetch(`/api/articles/${id}/summary?angle=${angle}`),

    // ── 领域与话题配置 ─────────────────────────────────────────
    getConfigTopics: (domainId = "ai-agent") =>
      _fetch(`/api/config/topics?domain=${domainId}`),

    listDomains: () => _fetch("/api/config/domains"),

    // ── 问答 ──────────────────────────────────────────────────
    ask: (question, domain = "ai-agent", use_reasoning = false) =>
      _fetch("/api/qa", {
        method: "POST",
        body: JSON.stringify({ question, domain, use_reasoning }),
      }),

    // ── 事件 ──────────────────────────────────────────────────
    recordEvent: (article_id, event_type, payload = {}) =>
      _fetch("/api/events", {
        method: "POST",
        body: JSON.stringify({ article_id, event_type, payload }),
      }),

    // ── 笔记 ──────────────────────────────────────────────────
    saveNote: (article_id, note_text) =>
      _fetch("/api/notes", {
        method: "POST",
        body: JSON.stringify({ article_id, note_text }),
      }),

    getNotes: () => _fetch("/api/notes"),
    getNoteForArticle: (article_id) => _fetch(`/api/notes/${article_id}`),

    // ── 统计 ──────────────────────────────────────────────────
    topicStats: () => _fetch("/api/stats/topics"),

    getTimeline: () => _fetch("/api/stats/timeline"),

    // ── 用户画像 ───────────────────────────────────────────────
    getProfile: () => _fetch("/api/profile"),

    inferProfile: () => _fetch("/api/profile/infer", { method: "POST" }),

    // ── 复习 ──────────────────────────────────────────────────
    getDueReviews: (limit = 10) =>
      _fetch(`/api/reviews/due?limit=${limit}`),

    enqueueReview: (article_id) =>
      _fetch("/api/reviews/enqueue", {
        method: "POST",
        body: JSON.stringify({ article_id }),
      }),

    submitReview: (queue_id, result) =>
      _fetch(`/api/reviews/${queue_id}/submit`, {
        method: "POST",
        body: JSON.stringify({ result }),
      }),

    // ── 矛盾冲突 ───────────────────────────────────────────────
    getConflictAlerts: (limit = 10) =>
      _fetch(`/api/contradiction/alerts?limit=${limit}`),

    dismissConflictAlert: (alertId) =>
      _fetch(`/api/contradiction/alerts/${alertId}/dismiss`, { method: "POST" }),

    // ── 推荐 ──────────────────────────────────────────────────
    getRecommendations: (n = 3) => _fetch(`/api/recommendations?n=${n}`),

    // ── 图谱 ──────────────────────────────────────────────────
    getGraph: () => _fetch("/api/graph"),

    // ── 管理 ──────────────────────────────────────────────────
    triggerCollect: () => _fetch("/api/admin/collect", { method: "POST" }),
    reloadKnowledge: () => _fetch("/api/admin/reload", { method: "POST" }),
  };
})();
