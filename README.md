# AI Agent Study Workspace

This folder is a durable context capsule and local knowledge base for studying AI agents.

Read `AGENTS.md`, `AI_AGENT_MEMORY.md`, `AI_AGENT_LEARNING_MODEL.md`, `OPENCLI_NOTES.md`, and `KNOWLEDGE_BASE.md` first.

For the knowledge base, use `knowledge/catalog/` first and read full articles only when needed.

## Working Flow

1. Read the workspace instructions first.
2. Use `knowledge/catalog/` as the low-token entry point.
3. Open `summary.md` before `article.md`.
4. Preserve evidence when capturing new items.
5. Verify each completed batch with `node knowledge\\raw\\verify-batch.js`.

## Knowledge Capture Rule

Each collected item should preserve:

- `summary.md`: low-token summary and agent-model mapping
- `article.md`: full text when available
- `source.md`: BestBlogs URL plus original publisher URL when exposed
- `raw/`: raw extraction data and debugging evidence

Do not claim capture success unless `article.md`, `source.md`, and index updates are actually written.

## Git Notes

- Remote repository: `git@github.com:leilehuimieba/aiagentstudy.git`
- Default branch: `main`
- Line endings are normalized with `.gitattributes`
