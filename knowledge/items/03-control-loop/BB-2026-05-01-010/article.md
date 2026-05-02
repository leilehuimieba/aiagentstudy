# Codex CLI 0.128.0 新增 /goal 命令 | BestBlogs.dev

- BestBlogs URL: https://www.bestblogs.dev/article/5de75aba
- Selector: main
- Extracted chars: 841

---

30th April 2026 - Link Blog

**[Codex CLI 0.128.0 adds /goal](https://github.com/openai/codex/releases/tag/rust-v0.128.0)**. The latest version of OpenAI's Codex CLI coding agent adds their own version of the [Ralph loop](https://ghuntley.com/ralph/): you can now set a `/goal` and Codex will keep on looping until it evaluates that the goal has been completed... or the configured token budget has been exhausted.

It looks like the feature is mainly implemented though the [goals/continuation.md](https://github.com/openai/codex/blob/6014b6679ffbd92eeddffa3ad7b4402be6a7fefe/codex-rs/core/templates/goals/continuation.md) and [goals/budget\_limit.md](https://github.com/openai/codex/blob/6014b6679ffbd92eeddffa3ad7b4402be6a7fefe/codex-rs/core/templates/goals/budget_limit.md) prompts, which are automatically injected at the end of a turn.