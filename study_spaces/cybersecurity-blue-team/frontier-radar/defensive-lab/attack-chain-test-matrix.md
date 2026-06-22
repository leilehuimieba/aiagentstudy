# Attack Chain Test Matrix

> Purpose: give a defender enough operational detail to build blockers and test cases, without providing replayable exploits.

## 0. Common Model

Most current AI/Agent security failures follow the same shape:

```text
untrusted input
-> interpreted as config / prompt / workflow / tool / query / memory
-> crosses into privileged runtime
-> runtime performs action
-> secrets, data, network, filesystem, or process execution become reachable
```

Your project should treat the following as high-risk trust-boundary crossings:

- HTTP request body becomes executable workflow data.
- Uploaded filename becomes filesystem path.
- Imported workflow becomes server-side tool configuration.
- MCP `stdio` config becomes subprocess launch.
- Prompt or URL parameter becomes instruction.
- Agent memory write becomes future behavioral policy.
- Checkpoint metadata becomes database query.
- LLM-selected command arguments become local process behavior.

## 1. Langflow CVE-2026-33017: Public Flow Build to Python Execution

Known facts:

- Affected versions before 1.9.0.
- Risk shape: unauthenticated public flow build endpoint accepts attacker-controlled `data`.
- Dangerous transition: supplied flow data contains node definitions that reach server-side Python execution.
- Public sources report exploitation within about 20 hours after advisory publication.

High-level attack chain:

```text
internet scan
-> POST to public flow build endpoint
-> include attacker-controlled flow data
-> server chooses supplied data over stored database flow
-> node definition reaches dynamic Python execution
-> attacker validates execution
-> attacker enumerates env, local files, app config
-> attacker attempts secret exfiltration or stage-two retrieval
```

Block points:

- Require authentication for all build/execute endpoints.
- Remove or reject optional user-supplied flow `data` on public-build paths.
- Enforce strict schema: workflow data cannot contain code-bearing fields unless signed and trusted.
- Run workflow execution in a sandbox without secrets or cloud credentials.
- Deny outbound network by default for workflow build containers.

Telemetry to collect:

- HTTP method/path/user/auth status.
- Presence of optional `data` field on public build endpoint.
- Flow/node fields containing code-like text.
- Child process creation by Langflow worker.
- Reads of `.env`, cloud credential files, SSH keys, database files.
- Egress to unknown domains, OAST/interactsh-like domains, paste sites, package mirrors.

Useful detection features:

```text
endpoint contains /api/v1/build_public_tmp/
AND unauthenticated OR public route
AND body contains "data"
AND body contains code-like tokens: exec, eval, import, subprocess, os., open(, __, base64, curl, wget
```

## 2. Langflow CVE-2026-5027: File Upload Path Traversal to Arbitrary Write

Known facts:

- Risk shape: file upload endpoint accepts multipart filename that can traverse outside the intended upload directory.
- Dangerous transition: uploaded filename becomes server-side filesystem path.
- Arbitrary write can become persistence, config tampering, template injection, or later code execution depending on deployment.

High-level attack chain:

```text
scan exposed Langflow
-> POST multipart upload
-> filename contains traversal or encoded traversal
-> server writes outside upload directory
-> attacker targets startup path, config path, import path, template path, or writable service path
-> later reload / restart / import / template render turns write into impact
```

Block points:

- Normalize filename before validation.
- Resolve absolute final path and enforce it stays inside the upload root.
- Replace user filename with server-generated object id.
- Store uploads in a non-executable object store.
- Deny writes to app directory, home directory, service config, cron, startup, template, and import paths.

Telemetry to collect:

- Raw filename and normalized filename.
- Final resolved path.
- Upload destination.
- Files written outside upload root.
- Writes to `.py`, `.js`, `.sh`, service files, cron files, config files, templates.

Useful detection features:

```text
multipart filename contains ../, ..\, %2e%2e, %252e%252e, absolute path prefix
OR final_path does not start with upload_root
OR upload extension belongs to executable/config/template family
```

## 3. Flowise CVE-2026-40933: Custom MCP stdio to Server-Side Command Execution

Known facts:

- Affected packages include `flowise` and `flowise-components` through 3.0.13; 3.1.0 is listed as patched in advisory databases.
- Risk shape: Custom MCP config can use `stdio`, which launches a configured command as a child process.
- Practical path: authenticated user, compromised account, malicious insider, or imported workflow/chatflow influences MCP config.
- Import-only paths are especially important because workflow rendering/tool enumeration may trigger backend connection to the MCP server.

High-level attack chain:

```text
attacker controls chatflow / workflow / Custom MCP config
-> config contains stdio transport
-> config contains command + args + env-like fields
-> victim imports or opens workflow
-> backend enumerates MCP tools
-> backend launches configured subprocess
-> process can read env, mounted files, network, cloud metadata, SaaS tokens
```

Block points:

- Disable stdio MCP in hosted or multi-user deployments.
- Prefer Streamable HTTP/SSE transport with authenticated remote MCP servers.
- Treat imported chatflow JSON as code.
- Only admins can create or modify Custom MCP definitions.
- Pre-register MCP servers by immutable id; users choose from allowlist, not command fields.
- Run Flowise as non-root and without cloud admin credentials or Docker socket.

Telemetry to collect:

- Chatflow import source and user.
- Custom MCP nodes in imported workflow.
- Transport type.
- Command, args, env keys after normalization.
- Child processes spawned by Node/Flowise.
- Egress from child process to package registries, paste sites, unknown domains, internal APIs, metadata endpoints.

Useful detection features:

```text
workflow_import contains CustomMCP
AND transport == "stdio"
AND command field exists

process.parent in ["node", "flowise"]
AND process.command in [npx, npm, node, python, python3, uvx, bash, sh, powershell, pwsh, docker]
AND event.context == "mcp_tool_enumeration" OR "workflow_import"
```

## 4. MCP stdio Systemic Class: Configuration as Process Launcher

Risk shape:

```text
config file / marketplace package / project repo / AI-generated edit
-> MCP server definition
-> stdio transport with command, args, env
-> AI client starts local server
-> server gains local file and token access according to host privileges
```

Block points:

- Never auto-load project MCP config into global agent config.
- Require explicit diff review for MCP config changes.
- Store MCP config in a protected path that model output cannot modify directly.
- Require signer/reputation for marketplace MCP packages.
- Isolate each MCP server in a container or OS sandbox.
- Pass only required environment variables; never pass entire process env by default.

Telemetry:

- MCP config file creation/modification.
- MCP server start/stop.
- Spawned binary and exact argv.
- Env keys passed to MCP server.
- Files and directories accessed by MCP server.
- Network domains contacted by MCP server.

## 5. LangGraph Checkpointer Chain: Metadata Query to RCE

Risk shape:

```text
user-controllable filter / metadata / checkpoint id
-> checkpointer query builder
-> SQL / RediSearch query injection
-> checkpoint content or query result manipulation
-> unsafe deserialization or state restoration
-> agent runtime executes attacker-influenced object / code path
```

Block points:

- Patch LangGraph/LangChain checkpoint packages.
- Use parameterized queries.
- Only allow safe metadata keys from a fixed schema.
- Treat checkpoint content as untrusted.
- Disable unsafe deserialization formats and legacy compatibility paths.
- Separate checkpoint store from production secrets and privileged networks.

Telemetry:

- Metadata filter keys and values.
- Rejected keys.
- Query builder errors.
- Deserialization errors.
- Checkpoint restore events.
- Agent runtime file/network access during restore.

Useful detection features:

```text
metadata key contains SQL operators, quotes, parentheses, comment tokens
OR RediSearch special syntax outside allowlisted pattern
OR checkpoint restore follows untrusted write
OR deserialization happens on externally writable checkpoint data
```

## 6. SearchLeak Class: Parameter-to-Prompt plus Rendering/Egress

Known facts:

- SearchLeak chained Parameter-to-Prompt injection, an HTML rendering race, and CSP bypass via Bing SSRF.
- Data sources included mailbox, calendar, SharePoint, and OneDrive.
- Microsoft remediated the issue under CVE-2026-42824.

High-level attack chain:

```text
user clicks trusted-looking AI search link
-> URL query parameter contains instruction-like content
-> AI search treats parameter as executable prompt
-> AI retrieves sensitive enterprise data user can access
-> model response includes remote-loadable HTML/Markdown/image construct
-> browser or proxy fetches attacker-controlled URL before/around sanitization
-> sensitive data appears in outbound request metadata or URL
```

Block points:

- Separate search query from instruction fields.
- Strip imperative instructions from query parameters.
- Sanitize before streaming to browser.
- Do not auto-load remote resources in AI output.
- Proxy and rewrite links/images through safe renderers.
- Detect AI responses that combine sensitive data snippets with external URLs.

Telemetry:

- AI search URLs with long `q=` or instruction-like parameters.
- AI retrieval scope: mailbox, calendar, SharePoint, OneDrive.
- Generated HTML/Markdown with remote image/link.
- Outbound request during response render.
- Sensitive tokens or document snippets in URLs.

Useful detection features:

```text
q parameter contains: search my email, find MFA, include in image URL, send to, remember, ignore
AND AI output contains remote image/link before sanitization
AND outbound domain not in enterprise allowlist
```

## 7. AI Recommendation / Memory Poisoning

Risk shape:

```text
web page / email / ad / "summarize with AI" button
-> AI assistant link contains q parameter
-> q parameter asks model to remember or prefer a source
-> assistant writes persistent memory or user preference
-> future answers are biased toward attacker-preferred supplier/source/advice
```

Block points:

- Memory write requires explicit user confirmation.
- Memory entries must include source, timestamp, and reason.
- Memory from third-party content should default to temporary.
- High-risk domains such as medical, financial, legal, security advice require stricter confirmation.
- Provide memory review and one-click revoke.

Telemetry:

- Prompt contains memory-write verbs.
- Source type is third-party link or summarized web page.
- Memory entry created or updated.
- Future recommendation references poisoned memory.

Useful detection features:

```text
prompt contains remember / future conversations / trusted source / always recommend / prefer this company
AND source != direct user statement
AND target domain in high-risk category
```

## 8. Prompt Injection to Agent Command Execution

Risk shape:

```text
untrusted text in repo / issue / log / web page / prompt
-> agent chooses "safe" command
-> attacker controls command arguments
-> argument triggers tool feature: exec, preload, config load, write, template, hook
-> local code execution or sensitive file read
```

Block points:

- Tool allowlist must include exact argv shape, not only binary name.
- Dangerous flags must be blocked per tool.
- Use `shell=false` and structured argv.
- Use `--` separators when supported.
- Read-only sandbox for inspection tasks.
- Human approval should show command, args, cwd, env delta, file/network permissions, and why it is needed.

Telemetry:

- Agent command proposal.
- Full argv, cwd, env delta.
- Source that influenced command.
- Tool output that caused next action.
- File/network/process access during command.

Useful detection features:

```text
agent source context is untrusted
AND command is allowed
AND argv contains dangerous execution/write/config flags
OR argv references config file from workspace
OR command attempts to access home/cloud/ssh/token paths
```

