# Knowledge Items

Curated AI-agent knowledge items live here. Use `knowledge/catalog/` or `.\kb.ps1 search` before opening item folders directly.

## Item Format

Each standard item directory should contain:

- `summary.md`: low-token summary and agent-model mapping.
- `article.md`: full article text when available.
- `source.md`: BestBlogs URL and original publisher URL when exposed.
- `raw/`: extraction evidence and debugging data.

## Topic Directories

- `01-context-memory`: context engineering, memory, RAG, retrieval, and knowledge-base design.
- `02-tools-actions`: tools, browser automation, CLI adapters, APIs, MCP-like surfaces, and execution environments.
- `03-control-loop`: planning, orchestration, agent loops, multi-agent work, and harness patterns.
- `04-evaluation-guardrails`: verification, observability, safety, reliability, and production failure analysis.
- `05-security-techniques`: security techniques and CTF-like agent security materials.
- `06-frontier-radar`: models, products, papers, benchmarks, and ecosystem updates.

## Reading Rule

Open `summary.md` first. Open `article.md` only when you need evidence, detail, or direct source reading.
