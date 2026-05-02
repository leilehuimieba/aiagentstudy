# AI Agent Knowledge Base

Low-token entry point.

## Read Order

1. `knowledge/catalog/README.md`
2. `knowledge/catalog/map.md`
3. `knowledge/catalog/articles-index.md`
4. Relevant `knowledge/items/**/summary.md`
5. Full `article.md` only when needed

## Structure

- `knowledge/catalog/`: small indexes and topic maps.
- `knowledge/items/`: curated entries organized by topic and ID.
- `knowledge/raw/`: raw page states and command outputs.

## Capture Policy

For each collected item, preserve:

- `summary.md`: low-token structured summary and model mapping.
- `article.md`: full text exported from the BestBlogs page when available.
- `source.md`: evidence links, including both the BestBlogs page URL and the original publisher URL when BestBlogs exposes it.
- `raw/`: raw metadata, page state, or extraction output.

Default reading should still use indexes and summaries first. Full text exists for evidence and deep study, not for every routine lookup.
