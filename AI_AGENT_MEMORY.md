# AI Agent Study Memory

## User Context

- The user is learning AI agents and wants a structured cognitive model.
- The user often studies frontier AI agent information from https://www.bestblogs.dev/.
- The user wants OpenCLI used to read logged-in websites and build a local knowledge base.
- The user wants multi-level directory management to avoid reading the whole knowledge base and wasting tokens.

## Local Environment Notes

- Workspace path: `E:\document\aiagentstudy`.
- Preferred language/runtime location: `E:\yuyan`.
- Plain `npm` works after `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- OpenCLI was installed globally via npm and `opencli doctor -v` succeeded.
- OpenCLI paths include `E:\yuyan\npm-global\opencli.cmd`.
- BestBlogs browser session can be opened through OpenCLI, but list/detail rendering has been intermittently slow or stuck; summary-level metadata has been prioritized first.
- On 2026-05-01, BestBlogs `/explore` rendered successfully through OpenCLI and additional article metadata was collected from page links and detail-page meta tags.

## Knowledge Base Rule

- Read `knowledge/catalog/` first.
- Read summaries second.
- Read full article exports only when needed.
- When collecting items, capture full article text when available, but keep normal lookup catalog-first to save tokens.
- Each item should record two evidence links when possible: the BestBlogs page URL and the original publisher URL exposed by BestBlogs.

## Learning Notes

- Agent loop: `Goal -> Context/State -> Reasoning/Planning -> Tool Action -> Observation -> Update -> Deliverable`.
- Treat knowledge as a first-class deliverable.
- Current knowledge base uses multi-level indexes: catalog first, item summaries second, full article exports only when needed.
- BestBlogs items currently indexed: BB-2026-05-01-001 through BB-2026-05-01-009.
- Continued collection added BestBlogs items BB-2026-05-01-010 through BB-2026-05-01-014 from the "文章 + 最新" filter.
- Particularly relevant new items: Codex CLI `/goal` command, GPT-5.5 cyber capability evaluation, and a GenAI domain-evaluation case about color theory.
- Continued collection added BestBlogs items BB-2026-05-01-015 through BB-2026-05-01-022 from video, podcast, brief, newsletter, and topic pages.
- Particularly relevant new items: Karpathy on Software 3.0/Agentic Engineering, Claude Code prompt caching, WorkOS MCP Cross-App Access, Agent technical history, Harness discussion, Agent Memory topic, AI coding tools comparison, and Harness Engineering guide.
- User clarified that article full text should be captured; the low-token catalog is for later search and selective reading, not a reason to skip full-text capture.
- Priority full-text captures completed for BB-2026-05-01-007, 010, 016, 020, and 022. Each has `article.md` and `source.md` where possible.
- Evidence policy: record both the BestBlogs page URL and the original publisher URL when available; for BestBlogs topic pages, record the topic page and captured reference links.

- Batch capture target: continue in batches of 20 successful full-text captures. A successful capture should include `article.md` and `source.md`; short posts may be accepted if the page itself is short.
- Added BB-2026-05-01-023: Claude/MCP production systems article, full text and source captured.
- Continued BestBlogs batch capture on 2026-05-01 added BB-2026-05-01-024 through BB-2026-05-01-045.
- Batch 024-045 verification: 22 new `article.md` files, all above 800 bytes after newsletter augmentation; global verification now reports 43 article files above 800 bytes and 45 source files.
- Batch 024-045 included long-running agents, Greg Brockman interview, DeepSeek vision test, JD GRAM recommendation architecture, China AI/Agent podcast, GPT-5.5 and DeepSeek/Claude/Frontier model topics, Boris Cherny/Claude Code, AI-native product teams, ChatGPT Images 2.0, small-model training, and newsletter issues 83-85/89-92.
- Newsletter detail pages exposed only short DOM text through OpenCLI, so their full article text was recovered from `knowledge/raw/candidates-2.json` and preserved as `raw/discovery-fulltext.json` with notes in `source.md`.
- Next BestBlogs capture batch should start at BB-2026-05-01-046 unless the index already contains newer IDs.
- Continued BestBlogs batch capture on 2026-05-01 added BB-2026-05-01-046 through BB-2026-05-01-065.
- Batch 046-065 verification: 20 new captures completed; global verification now reports 61 article files above 800 bytes and 65 source files.
- Batch 046-065 included Apple / HN / Meta / color-theory articles plus 5 agent-heavy podcasts and 10 agent/tool/video items, including Agent technical history, Karpathy, GPT-5/Claude/Gemini infrastructure, DeepMind AGI, DeepSeek V4, Codex Virgin Atlantic, AssemblyAI update, Claude Design, Gemini Conversational Agents, GitHub reliability, and AGI-era engineering identity.
- Short items in the batch were still captured and indexed because the page itself was short; do not treat the short length as a miss.
- Continued BestBlogs batch capture on 2026-05-02 added BB-2026-05-01-066 through BB-2026-05-01-085 after the user fixed the OpenCLI browser extension and logged into BestBlogs.
- Batch 066-085 verification: 20 new full-text captures completed; global verification now reports 81 article files above 800 bytes and 85 source files.
- Batch 066-085 included agent stack architecture, Google engineering lessons, Martin Fowler/Kent Beck, IDE future, Claude Opus 4.7, Boris Cherny/Claude Code, Claude Code best practices and handbook, OpenAI workspace agents, Shopify AI workflow, Tencent AI-native engineering, product design for agents, Codex, and Responses API WebSockets.
- Three attempted candidates were skipped because their rendered content was too short: `video/5d4cc2f`, `video/6ff088c`, and `article/44277004`.
- OpenCLI health on 2026-05-02: `opencli doctor -v` reported daemon running, extension connected v1.0.2, connectivity OK. If future captures redirect to `signin`, ask the user to login in the same OpenCLI-connected Edge session before running batches.
- Continued BestBlogs capture attempt on 2026-05-02 added BB-2026-05-01-086 through BB-2026-05-01-103 before OpenCLI browser bridge disconnected during the run.
- Partial batch 086-103 verification: 18 new full-text captures completed; global verification reported 99 article files above 800 bytes and 103 source files.
- Partial batch 086-103 included Harness Engineering implementation, Agentic Engineering first principles, Replit CEO / AI platform, app-less interfaces, API open wave, global model/coding podcast, GPT-5.5, Project Glasswing, Claude advisor strategy, Muse Spark, GLM-5.1 long-horizon model, VimRAG, MMX-CLI, hosted agents, DHH programming style, OpenAI token-heavy engineering practice, continuous learning agents, and coding agent components.
- The attempted run timed out while opening `https://www.bestblogs.dev/video/d4d2d42`; the stuck capture process was stopped manually. OpenCLI later reported extension not connected.
- Next BestBlogs capture batch should first complete BB-2026-05-01-104 through BB-2026-05-01-105 to finish the 20-item batch, then continue from BB-2026-05-01-106 unless the index already contains newer IDs.
- On 2026-05-02 the user reported the OpenCLI plugin was installed. `opencli doctor -v` reported daemon running and extension connected, but `opencli browser open` / `browser tab new` did not reliably navigate BestBlogs pages; test evals saw `about:blank`, and direct HTTP requests to BestBlogs also timed out. Avoid declaring new captures successful unless files and index entries are actually written.
- Installed official BestBlogs CLI globally into the preferred `E:\yuyan\npm-global` environment: `@bestblogs/cli` v2.0.8. `bestblogs auth status --json` currently reports `loggedIn: false`; `bestblogs discover/search/read` require an API key and return `AUTH_REQUIRED` until `bestblogs auth login --api-key <key>` or `BESTBLOGS_API_KEY` is configured.
- BestBlogs CLI is probably the best long-term capture path once authenticated. Useful commands: `bestblogs discover search "<query>" --json`, `bestblogs read deep <resourceId> --json`, and `bestblogs read deep <resourceId> --markdown-only`. Store results in the existing `summary.md`, `article.md`, `source.md`, and `raw/` structure.
- On 2026-05-02 the user added the OpenCLI extension to Google Chrome and logged into BestBlogs there. `opencli doctor -v` reported extension connected; `browser tab new https://www.bestblogs.dev/explore` reached `https://www.bestblogs.dev/en/explore` with content cards, so future browser captures can use the Chrome-connected OpenCLI session.
- Continued BestBlogs capture on 2026-05-02 added BB-2026-05-01-104 through BB-2026-05-01-123 using the Chrome OpenCLI browser bridge. Batch 104-123 verification: 20 new full-text captures completed; global verification reported 119 article files above 800 bytes and 123 source files.
- Batch 104-123 included Claude Code source/deep dives, AI tool practice spending, sandboxing AI-generated code, Sonnet/Gemini/Nano Banana/model updates, GLM-5 technical report, MiniMax M2.5, Seed model coverage, Boris Cherny/Claude Code, skill-writing design, OpenAI/Codex engineering observations, context-to-long-term-memory architecture, Vibe Coding practice, AI Coding explosion podcast, Anthropic programming trend report, and a comprehensive agent article. During cleanup, original publisher URLs for 104-123 were corrected from the BestBlogs Sources navigation link to each page's captured `View Source` link.
- On 2026-05-03 an attempted continuation initially wrote duplicate entries BB-2026-05-01-124 through BB-2026-05-01-143 because `capture-batch-066-085.js` only deduplicated `https://www.bestblogs.dev/article/...` URLs and missed already-captured `https://www.bestblogs.dev/en/article/...` forms. The duplicate batch was deleted, `articles-index.md` was rolled back to BB-2026-05-01-123, and the script was fixed to normalize `/en/`, query strings, and fragments before deduplication.
- Continued BestBlogs capture on 2026-05-03 then added the real BB-2026-05-01-124 through BB-2026-05-01-143. Batch 124-143 verification: 20 new full-text captures completed; global verification reported 139 article files above 800 bytes and 143 source files.
- Batch 124-143 included Codex intro, Clawdbot architecture, AI-native doc-driven development, Claude Code internal tips, v0/Git workflow, several agent/product podcasts, Showboat/Rodney, Lenny agent engineering notes, GPT-5.4 mini/nano economics, ChatGPT Images 2.0 video, StrongDM AI team workflow, Pragmatic Summit agent engineering notes, and Claude Code auto mode.
