# Codex CLI 0.128.0 新增 /goal 命令

- BestBlogs URL: https://www.bestblogs.dev/article/5de75aba
- Extraction: DOM text from BestBlogs page
- Extracted chars: 487
- Original publisher URL: https://simonwillison.net/2026/Apr/30/codex-goals/#atom-everything

---

30th April 2026 - Link Blog

Codex CLI 0.128.0 adds /goal. The latest version of OpenAI's Codex CLI coding agent adds their own version of the Ralph loop: you can now set a /goal and Codex will keep on looping until it evaluates that the goal has been completed... or the configured token budget has been exhausted.

It looks like the feature is mainly implemented though the goals/continuation.md and goals/budget_limit.md prompts, which are automatically injected at the end of a turn.
