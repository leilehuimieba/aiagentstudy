# Multi-Source Capture Strategy

## Goal

Expand the knowledge base beyond BestBlogs while keeping the same durable item format:

- `summary.md`
- `article.md`
- `source.md`
- `raw/`

## Source Classes

### 1. Official Lab / Company Sources

Use these for factual announcements, model releases, safety notes, product direction, and infrastructure claims.

Default capture route:

1. Prefer RSS/Atom or official JSON endpoints.
2. Fall back to direct HTTP article fetch.
3. Use OpenCLI Browser Bridge only when content is rendered client-side or blocked without browser context.

Examples: OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft Research, NVIDIA, Hugging Face, Mistral, Qwen, DeepSeek, Kimi, Zhipu.

### 2. Research Paper Sources

Use these for latest AI research, model training, architecture, optimization, evals, and safety papers.

Default capture route:

1. Use official APIs first: arXiv API, OpenReview API, Semantic Scholar API, conference proceedings.
2. Store paper metadata, abstract, PDF URL, HTML URL, code URL, and discussion URL.
3. Capture full paper text only when it is highly relevant or needed for deep reading.

Examples: arXiv, OpenReview, ACL Anthology, Semantic Scholar, Hugging Face Papers, alphaXiv, Papers with Code.

Current local arXiv route:

```powershell
.\kb.ps1 discover-sources --max-results 10
.\kb.ps1 capture-arxiv --latest-candidates --limit 5
```

Durable paper captures are indexed in `knowledge/catalog/paper-index.md` and also appended to `knowledge/catalog/articles-index.md` so the normal retrieval layer can find them.

### 3. Engineering / Practitioner Sources

Use these for agent frameworks, RAG, context engineering, inference optimization, deployment, eval harnesses, and production lessons.

Default capture route:

1. Prefer RSS if available.
2. Direct HTTP for static blogs.
3. Browser Bridge for docs/blogs that need JS rendering.

Examples: LangChain, LlamaIndex, Vercel AI SDK, Modal, Together AI, Databricks/Mosaic, Unsloth, vLLM, Simon Willison, Latent Space.

Current local RSS route:

```powershell
.\kb.ps1 capture-rss --ids langchain-blog simon-willison latent-space --limit 5
```

Durable non-BestBlogs web captures are indexed in `knowledge/catalog/source-article-index.md` and also appended to `knowledge/catalog/articles-index.md`.

Current local browser snapshot route:

```powershell
.\kb.ps1 capture-browser --ids openai-news jiqizhixin github-trending huggingface-papers --profile qmvqcrb8 --limit 4
```

Browser snapshots preserve the rendered page text and candidate links. Treat them as source radar for deciding what to deep-capture next, not as final article-level evidence.

### 4. Chinese AI / Engineering Sources

Use these for Chinese AI ecosystem, local model releases, engineering cases, and translated/curated research.

Default capture route:

1. Use BestBlogs if it exposes full text and original publisher links.
2. Use original site RSS/API when available.
3. Use Browser Bridge for WeChat-like dynamic pages or sites requiring logged-in rendering.

Examples: 机器之心, 量子位, PaperWeekly, Datawhale, InfoQ 中文, 阿里云开发者, 腾讯技术工程, 字节跳动技术团队, 美团技术, 得物技术.

### 5. Community / Discussion Sources

Use these for early signals, not as final truth.

Default capture route:

1. Capture title, link, score/comments, and discussion summary.
2. Always link back to the primary source when available.
3. Do not treat community claims as verified until cross-checked.

Examples: Hacker News, Reddit r/MachineLearning, r/LocalLLaMA, r/ClaudeAI, GitHub Trending, Product Hunt.

## Landing Topics

- Agent memory, context, RAG, retrieval: `01-context-memory`
- Tools, APIs, browser/computer use, frameworks: `02-tools-actions`
- Agent loops, orchestration, harness, multi-agent: `03-control-loop`
- Evaluation, benchmarks, safety, governance: `04-evaluation-guardrails`
- Security techniques and AI-enabled security: `05-security-techniques`
- Model releases, papers, ecosystem, business/product frontier: `06-frontier-radar`

## Dedupe Policy

Deduplicate by:

1. Canonical URL
2. Original publisher URL
3. DOI / arXiv ID / OpenReview ID
4. Title similarity
5. BestBlogs URL if the item came through BestBlogs

## Raw Evidence Policy

For each non-BestBlogs source, store:

- `raw/source-list.json` or feed entry
- `raw/page.html` or `raw/page.json`
- `raw/article-text.txt` or extracted markdown
- `raw/probe.json` when OpenCLI Browser Bridge was used

## OpenCLI Browser Bridge Use

Use `qmvqcrb8` by default.

Useful commands:

```powershell
opencli browser qmvqcrb8 tab new "https://example.com"
opencli browser qmvqcrb8 state
opencli browser qmvqcrb8 extract --selector "main" --chunk-size 20000
opencli browser qmvqcrb8 eval "document.body.innerText"
opencli browser qmvqcrb8 network --since 2m
```

Use Browser Bridge when:

- site requires login state,
- content is rendered by JavaScript,
- a search page or dynamic list needs UI state,
- API requests need browser credentials,
- visual or DOM evidence matters.

Prefer RSS/API/direct HTTP when those are stable and complete.
