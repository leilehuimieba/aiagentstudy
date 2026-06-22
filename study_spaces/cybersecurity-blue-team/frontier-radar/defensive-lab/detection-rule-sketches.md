# Detection and Prevention Rule Sketches

> These are implementation sketches. Convert them into your own WAF, SIEM, EDR, API gateway, import scanner, or agent policy language.

## 1. WAF / API Gateway: Public Workflow Build with User-Supplied Code-Like Data

Goal: catch Langflow-like public build routes where request bodies contain executable workflow data.

Pseudo logic:

```text
IF request.path MATCHES "/api/*/build_public*"
AND request.auth.status IN ["none", "anonymous", "public"]
AND request.body CONTAINS_FIELD "data"
AND request.body CONTAINS_ANY [
  "exec", "eval", "import", "subprocess", "os.", "open(",
  "__", "base64", "curl", "wget", ".env", "/etc/passwd"
]
THEN block WITH reason "public workflow build cannot accept code-like user data"
```

Better prevention:

```text
public_build_endpoint.allowed_fields = ["flow_id", "input_values"]
public_build_endpoint.disallowed_fields = ["data", "code", "template", "custom_component"]
workflow_node.source = stored_database_flow_only
```

## 2. Upload Gateway: Final Path Must Stay Inside Upload Root

Goal: catch path traversal and arbitrary-write risk.

Pseudo logic:

```text
raw_filename = multipart.filename
decoded_filename = repeated_url_decode(raw_filename, max_rounds=2)
normalized_name = normalize_path(decoded_filename)
final_path = resolve(upload_root, normalized_name)

IF raw_filename CONTAINS_ANY ["../", "..\\", "%2e", "%252e", "/etc/", "C:\\"]
OR final_path DOES_NOT_START_WITH upload_root
OR file.extension IN [".py", ".js", ".sh", ".ps1", ".service", ".conf", ".env", ".yaml", ".yml", ".jinja", ".html"]
THEN block_or_quarantine
```

Better prevention:

```text
stored_name = random_uuid()
preserve_original_filename_for_display_only = true
upload_storage_noexec = true
```

## 3. Workflow Import Scanner: Custom MCP stdio Requires Admin Review

Goal: catch Flowise-like imported workflow artifacts that can launch server-side commands.

Pseudo logic:

```text
FOR each node IN imported_workflow.nodes:
  IF node.type MATCHES_ANY ["Custom MCP", "MCP Tool", "Tool Server"]
  AND node.config.transport == "stdio":
    IF deployment.mode IN ["server", "multi_user", "cloud", "team"]:
      quarantine import
      require admin review
      log node id, transport, command category, args shape
```

Command risk categories:

```text
critical_interpreters = ["bash", "sh", "zsh", "powershell", "pwsh", "cmd"]
package_runners = ["npx", "npm", "pnpm", "yarn", "uvx", "pipx"]
interpreters = ["node", "python", "python3", "ruby", "perl", "php"]
container_or_remote = ["docker", "kubectl", "ssh", "scp"]
```

Policy:

```text
IF mcp.transport == "stdio"
AND mcp.command IN any_risk_category
THEN block unless server_definition_id IN admin_approved_allowlist
```

## 4. EDR / Process: Flowise or Agent Parent Spawns High-Risk Child

Goal: catch server-side execution from AI workflow platforms and AI IDEs.

Pseudo logic:

```text
IF process.parent.name IN ["node", "flowise", "langflow", "python", "uvicorn", "gunicorn", "electron", "code", "cursor"]
AND process.child.name IN ["bash", "sh", "powershell", "pwsh", "cmd", "python", "node", "npx", "uvx", "docker", "curl", "wget"]
AND process.context IN ["workflow_import", "mcp_tool_enumeration", "agent_auto_command", "public_flow_build"]
THEN alert high
```

Escalate to critical when:

```text
child reads secret-like files
OR child contacts unknown network destination
OR child receives env keys matching ["API_KEY", "TOKEN", "SECRET", "AWS_", "AZURE_", "GCP_", "OPENAI_", "ANTHROPIC_"]
```

## 5. MCP Config File Protection

Goal: prevent prompt/model/repo content from silently modifying trusted tool registry.

Pseudo logic:

```text
protected_paths = [
  "~/.config/*/mcp*.json",
  "~/.cursor/*",
  "~/.claude/*",
  ".mcp.json",
  "mcp.json",
  "*agent*rules*",
  "*tool*registry*"
]

IF file.path MATCHES protected_paths
AND writer.identity IN ["ai_agent", "model_generated_patch", "workspace_import", "repo_checkout"]
AND change CONTAINS ["stdio", "command", "args", "env"]
THEN block write OR require explicit human diff approval
```

## 6. AI Search Parameter-to-Prompt Guard

Goal: separate search queries from executable instructions.

Pseudo logic:

```text
IF url.domain IN enterprise_ai_search_domains
AND url.query.q.length > threshold
AND url.query.q CONTAINS_ANY [
  "ignore previous", "search my email", "find my MFA", "calendar",
  "SharePoint", "OneDrive", "include the result in", "image URL",
  "send to", "fetch", "http", "remember"
]
THEN warn_or_block_click
```

Better prevention:

```text
q_field.semantic_type = search_terms_only
instruction_field.must_be_server_generated = true
remote_resource_rendering = disabled_by_default
sanitize_before_stream = true
```

## 7. AI Output Remote Resource Guard

Goal: block SearchLeak-like exfil paths.

Pseudo logic:

```text
IF ai.output.streaming == true
AND output.chunk CONTAINS remote_resource_markup
THEN hold chunk
sanitize chunk before browser render
rewrite or remove remote URLs
```

Data-loss check:

```text
IF outbound.url CONTAINS sensitive_pattern
AND request.source == ai_output_render
THEN block egress
```

Sensitive pattern examples for tests:

```text
TEST_MFA_CODE_000000
TEST_EMAIL_BODY_TOKEN
TEST_SHAREPOINT_DOC_ID
TEST_CALENDAR_SECRET
```

## 8. Memory Write Guard

Goal: prevent recommendation/memory poisoning.

Pseudo logic:

```text
IF prompt CONTAINS_ANY ["remember", "future conversations", "always recommend", "trusted source", "prefer this vendor"]
AND source.type IN ["web_page", "email", "ad", "third_party_link", "summarize_with_ai_button"]
THEN do_not_write_memory_automatically
REQUIRE explicit user confirmation
SET memory.ttl = short
STORE memory.source_url and prompt_hash
```

High-risk categories:

```text
security advice
financial advice
medical advice
legal advice
vendor recommendation
credential handling
software installation
```

## 9. Agent Command argv Policy

Goal: avoid treating command names as sufficient approval.

Pseudo logic:

```text
IF agent.command.name IN allowed_commands
THEN validate full argv against command-specific schema
ELSE block
```

Examples of dangerous argument families to classify:

```text
exec-like flags
preload/config-load flags
template/render flags
write-output flags
network-fetch flags
shell/interpreter passthrough flags
plugin/hook flags
```

Approval UI should show:

```text
command name
full argv
cwd
env diff
network permission
filesystem permission
source text that influenced this command
reason from model
policy decision
```

## 10. Correlation Rules

### Public Build to Secret Read

```text
IF event A: public workflow build request
AND within 2 minutes event B: app process reads secret-like file
AND within 2 minutes event C: app process makes unknown egress
THEN incident severity = critical
```

### Workflow Import to Subprocess

```text
IF event A: workflow/chatflow import contains MCP stdio
AND event B: server process spawns child process before workflow run
THEN incident severity = critical
```

### AI Search to External Resource

```text
IF event A: AI search query contains instruction-like q parameter
AND event B: AI output contains external image/link
AND event C: browser/proxy requests external URL with sensitive-like parameter
THEN incident severity = critical
```

