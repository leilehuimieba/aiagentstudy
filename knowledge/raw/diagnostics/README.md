# diagnostics/

Historical one-off scripts and debug data, moved out of `knowledge/raw/` root.

**These are provenance, not tooling.** Many of the scripts hardcode a stale
absolute repo root (e.g. `D:\newwork\aiagentstudy`, missing `AI-Agents`) and no
longer run as-is. Do NOT use them as a capture path — the active pipeline is the
stable scripts at the `knowledge/raw/` root, driven by `kb.ps1`. Keep these only to
understand how a past batch was produced or to copy a technique.

Contents:

- One-off scripts: `add-*.js`, `capture-batch-*.js`, `capture-edge-*.py`,
  `capture-latest-live.js`, `capture-opencli-latest-page5.py`, `*-page5*.py`,
  `process-*.js`, `rebuild-index.js`, `update-index-full.js`, `filter-discovery.js`,
  `finalize-fulltext-priority.js`, `fix-duplicate-170.py`, `discover-candidates-2.js`,
  `audit-relevance.js`, `tmp-opencli-fetch-page5.js`
- Debug data: `cdp-smoke-test*.json/js`, `b71c47ef-*.json`, `test-*-direct.json`,
  `opencli-*-debug.json`, `opencli-login-test-*.json`, `http-test-*.html`,
  `page5-titles.txt`
