# Study Spaces

`study_spaces/` is for non-agent study domains that should live in this repository without polluting the AI-agent knowledge base.

## Rule

- `knowledge/` remains the AI-agent learning KB.
- `study_spaces/<domain>/` is for other long-term study collections, such as exam prep, course notes, interview prep, or unrelated topic archives.
- Do not place non-agent materials under `knowledge/items/` or `knowledge/retrieval/`.

## Suggested Structure

Each study space can follow a lightweight variant of the main KB pattern:

1. `README.md`
2. `catalog/`
3. `items/`
4. `raw/`

Use the agent KB workflow only when that space actually benefits from summaries, retrieval, and evidence tracking.
