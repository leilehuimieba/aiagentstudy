// AI Agent 情报站 — main app (real API integration, v5 features)
(async function () {

  // ── State ──────────────────────────────────────────────────────────────────
  const state = {
    domain: "ai-agent",
    topics: [],
    topicNameById: {},      // 当前 domain 的话题名（用于 chips）
    allTopicNames: {},      // 所有 domain 的话题名（用于画像等跨域展示）
    filter: "all",
    query: "",
    articles: [],
    selectedId: null,
    angleCache: {},
    angle: "engineer",
    tab: "detail",
    feedbackState: {},
  };

  // ── DOM refs ───────────────────────────────────────────────────────────────
  const $list        = document.getElementById("article-list");
  const $count       = document.getElementById("article-count");
  const $search      = document.getElementById("search");
  const $searchWrap  = document.getElementById("sb-search");
  const $searchClear = document.getElementById("search-clear");
  const $filters     = document.getElementById("filters");
  const $detail      = document.getElementById("article-detail");
  const $tabbar      = document.getElementById("tabbar");
  const $detPane     = document.getElementById("pane-detail");
  const $prog        = document.querySelector("#reading-progress > span");

  const MORE_THRESHOLD = 8;
  const PANE_IDS = ["detail", "qa", "review", "coverage", "timeline", "profile"];
  const TAB_BY_NUM = { "1": "detail", "2": "qa", "3": "review", "4": "coverage", "5": "timeline", "6": "profile" };

  // ── Helpers ────────────────────────────────────────────────────────────────

  function esc(s) {
    return String(s || "").replace(/[&<>"]/g, m =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m])
    );
  }

  // Whitelist-based sanitizer for body/angle content — allows safe inline tags only
  function sanitize(html) {
    const ALLOWED = new Set(["b", "strong", "i", "em", "code", "br"]);
    return String(html || "").replace(
      /<(\/?)([a-z0-9]+)([^>]*)>/gi,
      (match, slash, tag) => {
        const t = tag.toLowerCase();
        if (!ALLOWED.has(t)) return esc(match);
        return `<${slash}${t}>`;
      }
    );
  }

  function topicName(id) {
    return state.allTopicNames[id] || state.topicNameById[id] || id;
  }

  function labelFor(k) {
    return { engineer: "工程师", product: "产品", beginner: "初学者", original: "原文摘要" }[k] || k;
  }

  // ── Article list ───────────────────────────────────────────────────────────

  function getFiltered() {
    const q = state.query.trim().toLowerCase();
    return state.articles.filter(a => {
      if (state.filter !== "all" && a.topic !== state.filter) return false;
      if (!q) return true;
      return (
        (a.title   || "").toLowerCase().includes(q) ||
        (a.summary || "").toLowerCase().includes(q) ||
        (a.topic   || "").toLowerCase().includes(q)
      );
    });
  }

  function renderList() {
    const items = getFiltered();
    $count.textContent = `${items.length} 篇`;
    if (items.length === 0) {
      $list.innerHTML = `
        <div class="empty-list">
          <div class="empty-ico">○</div>
          <div class="empty-msg">${
            state.articles.length === 0
              ? "这个领域还没有入库文章"
              : "本话题下还没有文章"
          }</div>
        </div>`;
      return;
    }
    $list.innerHTML = items.map(a => `
      <div class="article-item${a.id === state.selectedId ? " active" : ""}" data-id="${a.id}" role="listitem">
        <div class="ai-title">${esc(a.title)}</div>
        <div class="ai-meta">
          <span class="tag-topic">${esc(topicName(a.topic))}</span>
          <span class="ai-date">${a.date || ""}</span>
        </div>
        <div class="ai-summary">${esc(a.summary || a.takeaway || "")}</div>
      </div>
    `).join("");
  }

  $list.addEventListener("click", e => {
    const item = e.target.closest(".article-item");
    if (!item) return;
    selectArticle(item.dataset.id);
  });

  // ── Article selection ──────────────────────────────────────────────────────

  async function selectArticle(id) {
    if (state.selectedId === id) return;
    state.selectedId = id;
    state.tab = "detail";
    renderList();
    renderTabs();
    await loadAndRenderDetail(id);
    window.api.recordEvent(id, "view_start").catch(() => {});
    setupViewEndTracking(id);
  }

  // ── Filters / topic chips ──────────────────────────────────────────────────

  async function loadTopicsForDomain(domainId) {
    state.domain = domainId;
    state.filter = "all";

    $filters.setAttribute("aria-busy", "true");
    $filters.innerHTML =
      '<span class="chip-skel"></span>' +
      '<span class="chip-skel" style="width:48px"></span>' +
      '<span class="chip-skel" style="width:40px"></span>' +
      '<span class="chip-skel" style="width:56px"></span>';

    try {
      const { topics, domain_name } = await window.api.getConfigTopics(domainId);
      state.topics = topics;
      state.topicNameById = Object.fromEntries(topics.map(t => [t.id, t.name]));
      renderFilters(topics);
      const titleEl = document.querySelector(".sb-title span:last-child");
      if (titleEl) titleEl.textContent = `${domain_name} 情报站`;
      document.title = `${domain_name} 情报站`;
    } catch {
      $filters.innerHTML = '<button class="chip active" data-filter="all" aria-pressed="true">全部</button>';
    }

    $filters.setAttribute("aria-busy", "false");
    await loadArticles();
  }

  function renderFilters(topics) {
    const showCount = topics.length > MORE_THRESHOLD ? 6 : topics.length;
    const visible  = topics.slice(0, showCount);
    const overflow = topics.slice(showCount);

    const chips =
      '<button class="chip active" data-filter="all" aria-pressed="true">全部</button>' +
      visible.map(t =>
        `<button class="chip" data-filter="${t.id}" aria-pressed="false">${esc(t.name)}</button>`
      ).join("");

    const moreChip = overflow.length
      ? `<div class="chip-more" id="chip-more">
           <button class="chip" data-more-toggle aria-haspopup="true" aria-expanded="false">更多 ▾</button>
           <div class="menu" role="menu">
             ${overflow.map(t =>
               `<button role="menuitem" data-filter="${t.id}" aria-pressed="false">${esc(t.name)}</button>`
             ).join("")}
           </div>
         </div>`
      : "";

    $filters.innerHTML = chips + moreChip;
  }

  $filters.addEventListener("click", e => {
    const more = e.target.closest("[data-more-toggle]");
    if (more) {
      const wrap = document.getElementById("chip-more");
      const isOpen = wrap.classList.toggle("open");
      more.setAttribute("aria-expanded", isOpen ? "true" : "false");
      return;
    }
    const chip = e.target.closest("[data-filter]");
    if (!chip) return;
    state.filter = chip.dataset.filter;
    const moreEl = document.getElementById("chip-more");
    if (moreEl) {
      moreEl.classList.remove("open");
      moreEl.querySelector("[data-more-toggle]")?.setAttribute("aria-expanded", "false");
    }
    $filters.querySelectorAll("[data-filter]").forEach(c => {
      const on = c.dataset.filter === state.filter;
      c.classList.toggle("active", on);
      c.setAttribute("aria-pressed", on ? "true" : "false");
    });
    const trigger = document.querySelector("[data-more-toggle]");
    if (trigger) {
      const inOverflow = state.filter !== "all" &&
        !!document.querySelector(`#chip-more .menu [data-filter="${state.filter}"]`);
      trigger.classList.toggle("active", inOverflow);
    }
    renderList();
  });

  document.addEventListener("click", e => {
    if (!e.target.closest("#chip-more")) {
      const moreEl = document.getElementById("chip-more");
      if (moreEl) {
        moreEl.classList.remove("open");
        moreEl.querySelector("[data-more-toggle]")?.setAttribute("aria-expanded", "false");
      }
    }
  });

  // ── Domain switcher ────────────────────────────────────────────────────────

  document.getElementById("domain-switcher").addEventListener("click", e => {
    const b = e.target.closest(".ds-btn");
    if (!b) return;
    document.querySelectorAll(".ds-btn").forEach(x => {
      const on = x === b;
      x.classList.toggle("active", on);
      x.setAttribute("aria-pressed", on ? "true" : "false");
    });
    loadTopicsForDomain(b.dataset.domain);
  });

  // ── Search (debounced + clear button) ─────────────────────────────────────

  let _searchTimer = null;
  $search.addEventListener("input", e => {
    const v = e.target.value;
    $searchWrap.classList.toggle("has-value", v.length > 0);
    clearTimeout(_searchTimer);
    _searchTimer = setTimeout(() => {
      state.query = v;
      renderList();
    }, 150);
  });

  $searchClear.addEventListener("click", () => {
    $search.value = "";
    state.query = "";
    $searchWrap.classList.remove("has-value");
    clearTimeout(_searchTimer);
    renderList();
    $search.focus();
  });

  // ── Tabs ───────────────────────────────────────────────────────────────────

  function renderTabs() {
    document.querySelectorAll("#tabbar .tab").forEach(t => {
      const on = t.dataset.tab === state.tab;
      t.classList.toggle("active", on);
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.setAttribute("tabindex", on ? "0" : "-1");
    });
    PANE_IDS.forEach(id => {
      const el = document.getElementById("pane-" + id);
      if (id === state.tab) el.removeAttribute("hidden");
      else el.setAttribute("hidden", "");
    });
    if (state.tab === "coverage") renderCoverage();
    if (state.tab === "timeline") renderTimeline();
    if (state.tab === "review")   renderReview();
    if (state.tab === "profile")  renderProfile();
  }

  $tabbar.addEventListener("click", e => {
    const t = e.target.closest(".tab");
    if (!t) return;
    state.tab = t.dataset.tab;
    renderTabs();
  });

  // ── Keyboard shortcuts ─────────────────────────────────────────────────────
  // /    : focus search
  // j/k  : next/prev article in visible list
  // 1-6  : switch tab
  // Esc  : close dropdown / clear search

  document.addEventListener("keydown", e => {
    const target = e.target;
    const inEditable = target && (
      target.tagName === "INPUT" ||
      target.tagName === "TEXTAREA" ||
      target.isContentEditable
    );

    if (e.key === "Escape") {
      const moreEl = document.getElementById("chip-more");
      if (moreEl?.classList.contains("open")) {
        moreEl.classList.remove("open");
        moreEl.querySelector("[data-more-toggle]")?.setAttribute("aria-expanded", "false");
        return;
      }
      if (target === $search && $search.value) {
        $search.value = "";
        state.query = "";
        $searchWrap.classList.remove("has-value");
        clearTimeout(_searchTimer);
        renderList();
        return;
      }
      if (inEditable) target.blur();
      return;
    }

    if (inEditable) return;

    if (e.key === "/") {
      e.preventDefault();
      $search.focus();
      $search.select();
      return;
    }

    if (TAB_BY_NUM[e.key]) {
      state.tab = TAB_BY_NUM[e.key];
      renderTabs();
      return;
    }

    if (e.key === "j" || e.key === "k") {
      const items = getFiltered();
      if (!items.length) return;
      const idx  = Math.max(0, items.findIndex(a => a.id === state.selectedId));
      const next = e.key === "j"
        ? Math.min(items.length - 1, idx + 1)
        : Math.max(0, idx - 1);
      if (items[next].id !== state.selectedId) {
        selectArticle(items[next].id);
        // keep item in view
        const el = $list.querySelector(`.article-item[data-id="${items[next].id}"]`);
        if (el) {
          const top = el.offsetTop, bot = top + el.offsetHeight;
          if (top < $list.scrollTop) $list.scrollTop = top - 8;
          else if (bot > $list.scrollTop + $list.clientHeight)
            $list.scrollTop = bot - $list.clientHeight + 8;
        }
      }
    }
  });

  // ── Load all articles ──────────────────────────────────────────────────────

  async function loadArticles() {
    state.selectedId = null;
    state.articles = [];
    $list.innerHTML =
      '<div class="empty-list"><div class="empty-msg">加载中…</div></div>';
    $detail.innerHTML = "";

    try {
      const data = await window.api.listArticles({ limit: 200, domain: state.domain });
      state.articles = data.articles || [];
      renderList();

      const $qaCount = document.getElementById("qa-count");
      if ($qaCount) $qaCount.textContent = state.articles.length;

      if (state.articles.length > 0) {
        await selectArticle(state.articles[0].id);
      }
    } catch {
      $list.innerHTML =
        '<div class="empty-list"><div class="empty-msg">加载失败，请检查后端服务是否运行</div></div>';
    }
  }

  // ── Article detail ─────────────────────────────────────────────────────────

  async function loadAndRenderDetail(id) {
    $detail.innerHTML =
      '<div style="padding:32px;color:var(--muted)">加载中…</div>';
    try {
      const article = await window.api.getArticle(id);
      const idx = state.articles.findIndex(a => a.id === id);
      if (idx >= 0) state.articles[idx] = { ...state.articles[idx], ...article };
      renderDetailContent(article);
    } catch (e) {
      $detail.innerHTML =
        `<div style="padding:32px;color:#ef4444">加载失败: ${esc(e.message)}</div>`;
    }
  }

  function renderDetailContent(a) {
    if (!a) return;
    const fb       = state.feedbackState[a.id] || new Set();
    const cacheKey = `${a.id}_${state.angle}`;
    const cached   = state.angleCache[cacheKey];

    const angleHtml = state.angle === "original"
      ? `<p>${sanitize(a.summary || a.takeaway || "")}</p>`
      : cached
        ? `<p style="white-space:pre-wrap">${sanitize(cached)}</p>`
        : `<p style="color:var(--muted)">正在生成「${labelFor(state.angle)}」角度解读… ⊙</p>`;

    const bodyHtml = a.full_text ? renderBody(a.full_text) : "";

    $detail.innerHTML = `
      <h1>${esc(a.title)}</h1>
      <div class="meta-row">
        <span>${esc(a.date || "")}</span>
        <span class="dot">·</span>
        <span class="src">${esc(a.source || "")}</span>
        <span class="dot">·</span>
        <span class="tag-topic">${esc(topicName(a.topic))}</span>
        ${a.url ? `<span class="dot">·</span><a class="ext" href="${esc(a.url)}" target="_blank" rel="noopener">原文链接 ↗</a>` : ""}
      </div>

      <div class="takeaway">
        <div class="lbl">核心要点 · Takeaway</div>
        <p>${sanitize(a.takeaway || a.summary || "")}</p>
      </div>

      <div class="angles" id="angles" role="tablist" aria-label="阅读视角">
        <button class="angle${state.angle === "engineer" ? " active" : ""}" data-angle="engineer" role="tab" aria-selected="${state.angle === "engineer"}">工程师</button>
        <button class="angle${state.angle === "product"  ? " active" : ""}" data-angle="product"  role="tab" aria-selected="${state.angle === "product"}">产品</button>
        <button class="angle${state.angle === "beginner" ? " active" : ""}" data-angle="beginner" role="tab" aria-selected="${state.angle === "beginner"}">初学者</button>
        <button class="angle${state.angle === "original" ? " active" : ""}" data-angle="original" role="tab" aria-selected="${state.angle === "original"}">原文摘要</button>
      </div>

      <div class="article-body">
        <p style="color:var(--text)"><b>「${labelFor(state.angle)}」角度:</b></p>
        ${angleHtml}
        ${bodyHtml ? `<hr style="border:none;border-top:1px solid var(--border);margin:20px 0">${bodyHtml}` : ""}
      </div>

      <div class="feedback" id="feedback" role="group" aria-label="反馈">
        <button class="fb-btn${fb.has("useful")  ? " on" : ""}" data-fb="useful"  aria-pressed="${fb.has("useful")}"><span>💡</span> 有用</button>
        <button class="fb-btn${fb.has("known")   ? " on" : ""}" data-fb="known"   aria-pressed="${fb.has("known")}"><span>✓</span> 已知道</button>
        <button class="fb-btn${fb.has("deepen")  ? " on" : ""}" data-fb="deepen"  aria-pressed="${fb.has("deepen")}"><span>🔍</span> 想深入</button>
      </div>

      <div class="note-block">
        <div class="note-header">
          <label for="note-${a.id}">我的笔记</label>
          <span class="note-char" id="note-char-count">0 字</span>
        </div>
        <textarea id="note-${a.id}" placeholder="把这篇文章和你已知道的东西联系起来——你会记得更牢。" rows="4"></textarea>
        <div class="note-actions">
          <button class="btn-secondary" id="clear-note-btn">清除</button>
          <button class="btn-primary" id="save-note-btn">保存笔记</button>
        </div>
      </div>

      <div class="rec-block" id="rec-block">
        <div class="rec-block-title">你可能还想读</div>
        <div id="rec-list-inline" class="rec-list-inline">
          <span style="color:var(--muted);font-size:13px">加载中…</span>
        </div>
      </div>
    `;

    // Angle buttons
    document.getElementById("angles").addEventListener("click", e => {
      const b = e.target.closest(".angle");
      if (!b) return;
      state.angle = b.dataset.angle;
      renderDetailContent(a);
      if (state.angle !== "original" && !state.angleCache[`${a.id}_${state.angle}`]) {
        loadAngleSummary(a.id, state.angle);
      }
    });

    // Feedback — optimized: toggle in-place without full re-render
    document.getElementById("feedback").addEventListener("click", e => {
      const b = e.target.closest(".fb-btn");
      if (!b) return;
      const set = state.feedbackState[a.id] || new Set();
      if (set.has(b.dataset.fb)) set.delete(b.dataset.fb);
      else set.add(b.dataset.fb);
      state.feedbackState[a.id] = set;
      const on = set.has(b.dataset.fb);
      b.classList.toggle("on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
      window.api.recordEvent(a.id, `feedback_${b.dataset.fb}`, { active: on }).catch(() => {});
    });

    // 加载已有笔记
    window.api.getNoteForArticle(a.id).then(({ note }) => {
      const ta = document.getElementById(`note-${a.id}`);
      if (ta && note) {
        ta.value = note;
        const counter = document.getElementById("note-char-count");
        if (counter) counter.textContent = `${note.length} 字`;
      }
    }).catch(() => {});

    // 字数统计
    const noteTa = document.getElementById(`note-${a.id}`);
    if (noteTa) {
      noteTa.addEventListener("input", () => {
        const counter = document.getElementById("note-char-count");
        if (counter) counter.textContent = `${noteTa.value.length} 字`;
      });
    }

    // Note clear
    document.getElementById("clear-note-btn").addEventListener("click", () => {
      const ta = document.getElementById(`note-${a.id}`);
      if (ta) { ta.value = ""; ta.dispatchEvent(new Event("input")); }
    });

    // Note save
    document.getElementById("save-note-btn").addEventListener("click", () => {
      const ta  = document.getElementById(`note-${a.id}`);
      const txt = ta ? ta.value.trim() : "";
      if (!txt) return;
      const btn = document.getElementById("save-note-btn");
      if (btn) { btn.textContent = "保存中…"; btn.disabled = true; }
      window.api.saveNote(a.id, txt)
        .then(() => {
          if (btn) {
            btn.textContent = "已保存 ✓";
            btn.style.background = "#22c55e";
            btn.disabled = false;
            setTimeout(() => {
              if (btn.isConnected) { btn.textContent = "保存笔记"; btn.style.background = ""; }
            }, 2000);
          }
        })
        .catch(() => { if (btn) { btn.textContent = "保存笔记"; btn.disabled = false; } });
    });

    // Reset scroll + progress
    if ($detPane) $detPane.scrollTop = 0;
    if ($prog) $prog.style.width = "0%";

    // Trigger angle load if needed
    if (state.angle !== "original" && !state.angleCache[cacheKey]) {
      loadAngleSummary(a.id, state.angle);
    }

    // 异步加载推荐
    loadInlineRecommendations();
  }

  async function loadInlineRecommendations() {
    const $rec = document.getElementById("rec-list-inline");
    if (!$rec) return;
    try {
      const { recommendations } = await window.api.getRecommendations(4);
      if (!recommendations || !recommendations.length) {
        $rec.innerHTML = '<span style="color:var(--muted);font-size:13px">暂无推荐</span>';
        return;
      }
      $rec.innerHTML = recommendations.map(r => `
        <div class="rec-inline-card" data-id="${esc(r.id)}">
          <div class="rec-inline-topic">${esc(topicName(r.topic))}</div>
          <div class="rec-inline-title">${esc(r.title)}</div>
          <div class="rec-inline-reason">${esc(r.reason)}</div>
        </div>`).join("");
      $rec.querySelectorAll(".rec-inline-card").forEach(card => {
        card.addEventListener("click", () => selectArticle(card.dataset.id));
      });
    } catch {
      $rec.innerHTML = '';
    }
  }

  function renderBody(text) {
    if (!text) return "";
    return text.split(/\n{2,}/).map(block => {
      const t = block.trim();
      if (!t) return "";
      if (/^#{1,3}\s/.test(t)) return `<h3>${esc(t.replace(/^#+\s/, ""))}</h3>`;
      return `<p>${sanitize(t)}</p>`;
    }).join("");
  }

  async function loadAngleSummary(articleId, angle) {
    try {
      const data = await window.api.getAngleSummary(articleId, angle);
      state.angleCache[`${articleId}_${angle}`] = data.summary || "";
      if (state.selectedId === articleId && state.angle === angle) {
        const article = state.articles.find(a => a.id === articleId);
        if (article) renderDetailContent(article);
      }
    } catch (e) {
      console.warn("angle summary failed:", e.message);
    }
  }

  // ── View-end tracking ──────────────────────────────────────────────────────

  function setupViewEndTracking(articleId) {
    if (!$detPane) return;
    let sent = false;

    function check() {
      if (sent) return;
      const max = $detPane.scrollHeight - $detPane.clientHeight;
      const pct = max <= 0 ? 100 : ($detPane.scrollTop / max) * 100;
      if (pct >= 80) {
        sent = true;
        window.api.recordEvent(articleId, "view_end", { pct: Math.round(pct) })
          .then(res => {
            if (res && res.conflict_alert) showConflictBanner(res.conflict_alert);
          })
          .catch(() => {});
      }
    }

    $detPane.addEventListener("scroll", check, { passive: true });
    setTimeout(() => $detPane.removeEventListener("scroll", check), 300_000);
  }

  function showConflictBanner(alert) {
    document.querySelector(".conflict-banner")?.remove();
    const el = document.createElement("div");
    el.className = "conflict-banner";
    el.innerHTML = `
      <span class="ico">⚡</span>
      <div><b>观点冲突</b> — ${esc(alert.description || "")}</div>
      <button class="conflict-dismiss" data-id="${alert.id}">✕</button>`;
    $detail.insertAdjacentElement("afterbegin", el);
    el.querySelector(".conflict-dismiss").addEventListener("click", e => {
      const id = Number(e.target.dataset.id);
      if (id) window.api.dismissConflictAlert(id).catch(() => {});
      el.remove();
    });
  }

  // ── Coverage tab ───────────────────────────────────────────────────────────

  let _coverageLoaded = false;
  async function renderCoverage() {
    if (_coverageLoaded) return;
    const $card = document.getElementById("cov-card");
    $card.innerHTML = '<div style="padding:20px;color:var(--muted)">加载中…</div>';
    try {
      const stats = await window.api.topicStats();
      const ts = (stats || []).slice().sort((a, b) => b.coverage_pct - a.coverage_pct);
      $card.innerHTML = ts.map(t => {
        const pct  = t.coverage_pct || 0;
        const name = topicName(t.topic);
        return `
          <div class="cov-row">
            <div class="cov-top">
              <span class="name">${esc(name)}</span>
              <span class="num">${t.read}/${t.total} 篇</span>
              <span class="pct">${pct}%</span>
            </div>
            <div class="cov-bar"><span style="width:${pct}%"></span></div>
          </div>`;
      }).join("") || '<div style="padding:20px;color:var(--muted)">暂无数据</div>';
      _coverageLoaded = true;
    } catch {
      $card.innerHTML = '<div style="padding:20px;color:#ef4444">加载失败</div>';
    }
  }

  // ── Timeline tab (with year boundary marks) ────────────────────────────────

  let _timelineLoaded = false;
  async function renderTimeline() {
    if (_timelineLoaded) return;
    const $hm = document.getElementById("heatmap");
    $hm.innerHTML =
      '<tr><td colspan="20" style="color:var(--muted);padding:20px">加载中…</td></tr>';
    try {
      const { months, series } = await window.api.getTimeline();
      const max = Math.max(1, ...series.flatMap(s => s.data));

      // Build header with year-boundary marks
      const head = `<thead><tr>
        <th class="topic-col">话题</th>
        ${months.map(m => {
          const [y, mo] = m.split("-");
          const isYearStart = mo === "01";
          const cls      = isYearStart ? ' class="year-mark"' : "";
          const yearTag  = isYearStart ? `<span class="year-tag">${y}</span>` : "";
          return `<th${cls}>${yearTag}${parseInt(mo)}月</th>`;
        }).join("")}
        <th style="padding-left:12px">合计</th>
      </tr></thead>`;

      const body = `<tbody>${series.map(s => {
        const total = s.data.reduce((a, b) => a + b, 0);
        return `<tr>
          <td class="topic">${esc(topicName(s.topic))}</td>
          ${s.data.map((v, i) => {
            const mo = months[i].split("-")[1];
            const cellCls = mo === "01" ? "cell year-mark" : "cell";
            return `<td class="${cellCls}" title="${months[i]} · ${v} 篇"
              style="background:${heatColor(v, max)}"></td>`;
          }).join("")}
          <td class="total">${total}</td>
        </tr>`;
      }).join("")}</tbody>`;

      $hm.innerHTML = head + body;

      const $scale = document.getElementById("legend-scale");
      if ($scale) $scale.innerHTML = [0, 0.25, 0.5, 0.75, 1]
        .map(p => `<span style="background:${heatColor(Math.round(p * max), max)}"></span>`)
        .join("");
      const $lm = document.getElementById("legend-max");
      if ($lm) $lm.textContent = `最大值 ${max} 篇/月`;
      _timelineLoaded = true;
    } catch {
      $hm.innerHTML =
        '<tr><td colspan="20" style="color:#ef4444;padding:20px">加载失败</td></tr>';
    }
  }

  function heatColor(v, max) {
    if (v <= 0) return "#0d1120";
    const a = 0.12 + 0.78 * (v / max);
    return `rgba(59,130,246,${a.toFixed(3)})`;
  }

  // ── Review tab ─────────────────────────────────────────────────────────────

  function _reviewUrgency(nextDateStr) {
    const today = new Date(); today.setHours(0,0,0,0);
    const next  = new Date(nextDateStr); next.setHours(0,0,0,0);
    const diff  = Math.round((next - today) / 86400000);
    if (diff < 0)  return { when: `超期 ${-diff} 天`, cls: "overdue" };
    if (diff === 0) return { when: "今日到期", cls: "due" };
    if (diff === 1) return { when: "明天到期", cls: "upcoming" };
    return { when: `${diff} 天后`, cls: "upcoming" };
  }

  async function renderReview() {
    const $g = document.getElementById("review-grid");
    $g.innerHTML =
      '<div style="padding:20px;color:var(--muted);grid-column:1/-1">加载中…</div>';
    try {
      const { items, stats } = await window.api.getDueReviews(20);

      // 更新页头副标题
      const $sub = document.querySelector("#pane-review .sub");
      if ($sub && stats) {
        $sub.textContent = `队列共 ${stats.total} 张卡片，今日到期 ${stats.due_today} 张，已复习 ${stats.ever_reviewed} 张。`;
      }

      if (!items || items.length === 0) {
        $g.innerHTML = `
          <div class="empty-list" style="grid-column:1/-1">
            <div class="empty-ico">○</div>
            <div class="empty-msg">今日无到期复习，阅读文章后会自动加入队列</div>
          </div>`;
        return;
      }

      $g.innerHTML = items.map(item => {
        const s = _reviewUrgency(item.next_review_at);
        const qid = item.id;  // 后端返回 id 字段
        return `
          <div class="rev-card ${s.cls}" data-qid="${qid}">
            <div class="when">${s.when}</div>
            <h4>${esc(item.title || "")}</h4>
            <div class="q">
              <span class="qmark">Q.</span>${esc(item.review_question || item.title || "")}
            </div>
            <div class="rev-actions">
              <button class="forgot" data-qid="${qid}" data-r="forgot">✗ 忘了</button>
              <button class="hint"   data-qid="${qid}" data-r="hint">💡 提示</button>
              <button class="know"   data-qid="${qid}" data-r="remember">✓ 记得</button>
            </div>
          </div>`;
      }).join("");

      $g.addEventListener("click", async e => {
        const btn = e.target.closest("[data-r]");
        if (!btn) return;
        const qid = Number(btn.dataset.qid);
        try {
          await window.api.submitReview(qid, btn.dataset.r);
          const card = btn.closest(".rev-card");
          if (card) { card.style.opacity = "0.35"; card.style.pointerEvents = "none"; }
        } catch (err) { console.warn(err); }
      });
    } catch (e) {
      console.error(e);
      $g.innerHTML =
        '<div style="padding:20px;color:#ef4444;grid-column:1/-1">加载失败</div>';
    }
  }

  // ── Profile tab ────────────────────────────────────────────────────────────

  const ANGLE_LABEL = { engineer: "工程师视角", product: "产品视角", researcher: "研究者视角", unknown: "—" };

  async function renderProfile() {
    try {
      const profile = await window.api.getProfile();
      const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

      const totalArticles = state.articles.length || profile.total_articles || 165;
      set("pf-total",  `${totalArticles} 篇`);
      set("pf-read",   `${profile.total_read ?? 0} 篇`);
      set("pf-notes",  profile.total_notes ?? 0);
      set("pf-events", profile.events_count ?? 0);

      const active = (profile.active_topics || []).slice(0, 5);
      set("pf-topic",  active.length ? active.map(t => topicName(t)).join("、") : "—");

      const angle = ANGLE_LABEL[profile.primary_angle] || profile.primary_angle || "—";
      const readPct = totalArticles > 0 ? Math.round((profile.total_read || 0) / totalArticles * 100) : 0;
      set("pf-angle", `${angle} · ${readPct}% 阅读率`);

      const $at = document.getElementById("pf-active-topics");
      if ($at) {
        $at.innerHTML = active.length
          ? active.map((t, i) =>
              `<span class="${i === 0 ? "lg" : i < 3 ? "md" : ""}">${esc(topicName(t))}</span>`
            ).join("")
          : '<span style="color:var(--muted)">继续阅读后自动更新</span>';
      }

      const weak = (profile.weak_topics || []).slice(0, 4);
      const $wt = document.getElementById("pf-weak-topics");
      if ($wt) {
        $wt.innerHTML = weak.length
          ? weak.map(t =>
              `<span style="background:rgba(239,68,68,0.12);color:#fca5a5">${esc(topicName(t))}</span>`
            ).join("")
          : '<span style="color:var(--muted)">已全面覆盖</span>';
      }
    } catch (e) {
      console.error(e);
      const el = document.getElementById("pf-total");
      if (el) el.textContent = `${state.articles.length} 篇`;
    }
  }

  // ── QA tab ─────────────────────────────────────────────────────────────────

  const $qaInput   = document.getElementById("qa-input");
  const $qaAsk     = document.getElementById("qa-ask");
  const $qaDeep    = document.getElementById("qa-deep");
  const $qaResults = document.getElementById("qa-results");

  $qaDeep.addEventListener("click", () => {
    const on = $qaDeep.classList.toggle("on");
    $qaDeep.setAttribute("aria-pressed", on ? "true" : "false");
  });
  $qaDeep.setAttribute("aria-pressed", $qaDeep.classList.contains("on") ? "true" : "false");

  async function submitAsk() {
    const q = $qaInput.value.trim();
    if (!q) return;
    const deep = $qaDeep.classList.contains("on");
    $qaInput.value = "";

    const loadId = `qa-load-${Date.now()}`;
    $qaResults.insertAdjacentHTML("afterbegin", `
      <div class="qa-result" id="${loadId}">
        <div class="qa-q">你问</div>
        <div class="qa-question">${esc(q)}</div>
        <div class="qa-answer" style="color:var(--muted)">检索知识库中… ⊙</div>
      </div>`);

    try {
      const result  = await window.api.ask(q, state.domain, deep);
      const refs    = result.articles || [];
      const newHtml = renderQaResult(q, result.answer || "", refs);
      const loader  = document.getElementById(loadId);
      if (loader) loader.outerHTML = newHtml;
    } catch (e) {
      const loader = document.getElementById(loadId);
      if (loader) loader.querySelector(".qa-answer").innerHTML =
        `<span style="color:#ef4444">请求失败: ${esc(e.message)}</span>`;
    }
  }

  function renderQaResult(q, answer, refs) {
    return `
      <div class="qa-result">
        <div class="qa-q">你问</div>
        <div class="qa-question">${esc(q)}</div>
        <div class="qa-answer">${sanitize(answer).replace(/\n/g, "<br>")}</div>
        <div class="qa-sources">
          <div class="lbl">参考文章 · ${refs.length}</div>
          <div class="qa-source-chips">
            ${refs.map((r, i) => `
              <button class="qa-src" data-id="${r.id}">
                <span class="n">${i + 1}</span>
                <span>${esc(r.title || r.id)}</span>
              </button>`).join("")}
          </div>
        </div>
      </div>`;
  }

  $qaAsk.addEventListener("click", submitAsk);
  $qaInput.addEventListener("keydown", e => {
    if (e.key === "Enter") { e.preventDefault(); submitAsk(); }
  });
  $qaResults.addEventListener("click", e => {
    const s = e.target.closest(".qa-src");
    if (!s || !s.dataset.id) return;
    selectArticle(s.dataset.id);
  });

  // ── 采集按钮 ───────────────────────────────────────────────────────────────

  const $collectBtn = document.getElementById("collect-btn");
  if ($collectBtn) {
    $collectBtn.addEventListener("click", async () => {
      if ($collectBtn.classList.contains("loading")) return;
      $collectBtn.classList.add("loading");
      $collectBtn.textContent = "采集中…";
      try {
        await fetch("/api/admin/collect", { method: "POST" });
        $collectBtn.classList.remove("loading");
        $collectBtn.classList.add("done");
        $collectBtn.textContent = "后台运行中";
        setTimeout(async () => {
          $collectBtn.classList.remove("done");
          $collectBtn.textContent = "采集";
          await loadTopicsForDomain(state.domain);
        }, 30000);
      } catch {
        $collectBtn.classList.remove("loading");
        $collectBtn.textContent = "采集";
      }
    });
  }

  // ── Reading progress bar ───────────────────────────────────────────────────

  $detPane.addEventListener("scroll", () => {
    const max = $detPane.scrollHeight - $detPane.clientHeight;
    const pct = max <= 0 ? 0 : Math.min(100, ($detPane.scrollTop / max) * 100);
    if ($prog) $prog.style.width = pct + "%";
  }, { passive: true });

  // ── Init ───────────────────────────────────────────────────────────────────

  // 预加载所有 domain 的话题名，供跨域展示（如画像 Tab）使用
  try {
    const { domains } = await window.api.listDomains();
    await Promise.all(domains.map(async d => {
      const { topics } = await window.api.getConfigTopics(d.id);
      topics.forEach(t => { state.allTopicNames[t.id] = t.name; });
    }));
  } catch {}

  // 处理图谱页跳转传参
  const _jumpTo = sessionStorage.getItem("selectArticle");
  if (_jumpTo) {
    sessionStorage.removeItem("selectArticle");
    await loadTopicsForDomain("ai-agent");
    if (state.articles.find(a => a.id === _jumpTo)) {
      selectArticle(_jumpTo);
    }
  } else {
    await loadTopicsForDomain("ai-agent");
  }

})();
