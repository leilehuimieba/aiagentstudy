# AI Source Watchlist

This catalog points to the source registry used to expand collection beyond BestBlogs.

Read:

1. `knowledge/sources/README.md`
2. `knowledge/sources/source-registry.json`
3. `knowledge/sources/capture-strategy.md`
4. `knowledge/sources/paper-sources.md`
5. `knowledge/catalog/current-coverage.md`
6. `knowledge/catalog/paper-index.md`
7. `knowledge/catalog/source-article-index.md`

## Priority Source Groups

1. `papers-primary`: arXiv, OpenReview, Hugging Face Papers, Semantic Scholar, ACL Anthology.
2. `official-labs`: OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft Research, NVIDIA, Hugging Face, Mistral, Qwen, DeepSeek.
3. `agent-engineering`: LangChain, LlamaIndex, Vercel AI SDK, Simon Willison, Latent Space, The Gradient, Ahead of AI.
4. `model-optimization`: Hugging Face, vLLM, Unsloth, Together AI, Databricks/Mosaic, Modal, NVIDIA Technical Blog.
5. `chinese-ai`: 机器之心, 量子位, PaperWeekly, Datawhale, InfoQ 中文, 阿里云开发者, 腾讯技术工程.
6. `community-signals`: Hacker News, Reddit, GitHub Trending, Product Hunt.

## Capture Rule

New sources should first be registered in `source-registry.json`.
Only then should capture scripts create durable items under `knowledge/items/**`.

Current captured coverage is summarized in `current-coverage.md`.

For arXiv, use:

```powershell
.\kb.ps1 discover-sources --max-results 10
.\kb.ps1 capture-arxiv --latest-candidates --limit 5
```

For RSS/official/engineering sources, use:

```powershell
.\kb.ps1 capture-rss --ids langchain-blog simon-willison latent-space --limit 5
```

For dynamic pages and logged-in/browser-rendered discovery, use:

```powershell
.\kb.ps1 capture-browser --ids openai-news jiqizhixin github-trending huggingface-papers --profile qmvqcrb8 --limit 4
```

Browser snapshots should be treated as daily radar. Deep-capture the best linked articles or papers separately when they become important.
