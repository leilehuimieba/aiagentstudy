# Her · हेर — a detective for your Claude Code sessions

- BestBlogs URL: https://www.bestblogs.dev/article/69db4622
- Original publisher URL: https://huggingface.co/blog/build-small-hackathon/her-blog
- Source: BestBlogs / Hugging Face - Blog
- Publish time: 2026-06-07 18:13:41
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 2820

---

Her · हेर — Marathi for “detective.” A detective for your Claude Code sessions.

  

  Try it here: Her on Hugging Face

  Every Claude Code session leaves a trace — a .jsonl file with every turn, tool call, and token. But in practice, that trace is write-only. Rarely anyone reads 4,000 lines of JSON to figure out why the agent reached for production, where the context budget actually went, or which subagent quietly burned half the run.

  Her reads it for you.

  The premise is simple: drop a session file onto the page and let her investigate. She reconstructs what happened in plain English, flags the risky moves — deploys, config and production changes, secrets — and traces each one back to the exact turn where it happened.

  

  She shows where the tokens went, which tools, subagents, skills, and MCP servers were used, and — only when a named, fixable pattern fires — what you could have done better, grounded in Anthropic’s and the community’s best practices. She suggests, never asserts, and stays silent when there’s nothing worth saying.

  There’s also a built-in copilot: Ask Her. Ask “why was this tool used?” and she answers from the trace, cites the turns, and opens the exact tool call. Drop one file for a session view; drop several to build a project view and hunt a question across many sessions at once.

  

  No third-party AI API is ever called. The model — Nemotron-Mini-4B-Instruct — runs on the Space’s own GPU via ZeroGPU. Your session is uploaded only to a private, auto-deleted namespace that belongs to your run, and nothing about it leaves the box.

  The split that makes this trustworthy: the evaluation engine is purely deterministic. The model is used only to write the English and propose softer suggestions. It never asserts a finding. The numbers don’t move when the model changes.

  

  One nice detail: Her doesn’t just list the CLI tools a session used — she identifies them. A database of top tools from Homebrew, npm, and PyPI ships with the Space, so most tools are named offline with a one-line blurb. When deploy tools, database clients, or dev servers are actually executed, Her flags that activity for the second look it deserves.

  It grew over a weekend. It started as an operator’s view — a journey graph where every query is a node sized by cost, the heaviest one glowing — built for a friend.

  

  I showed it to another friend who wanted it simpler, so the graph grew an executive Report that’s now the default. Then the first friend asked why their CLI tool didn’t show up — which is how the tool database was born.

  

  The frontend is a React app served straight off a Gradio server, with the deterministic engine doing the forensics and Nemotron handling the prose.

  When Claude loses his mind, call Her. ;)

  Try it here: Her on Hugging Face
