# BB-2026-05-01-331 Source References

## Primary Sources

### FlagHunter/PentestAgent Source Code
- `D:\webstudy\FlagHunter\pentestagent\agents\base_agent.py` — ReAct loop (`_run_loop`), tool execution path
- `D:\webstudy\FlagHunter\pentestagent\tools\registry.py` — Tool registry, ToolSchema, Tool class
- `D:\webstudy\FlagHunter\pentestagent\tools\executor.py` — ToolExecutor with flag scanning, stealth delays
- `D:\webstudy\FlagHunter\pentestagent\llm\memory.py` — ConversationMemory, token counting, summarization
- `D:\webstudy\FlagHunter\CLAUDE.md` — Project overview, architecture documentation

### Claw Code Source (Rust rewrite of Claude Code)
- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\conversation.rs` — ConversationRuntime, run_turn(), AssistantEvent, TurnSummary
- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\permission_enforcer.rs` — PermissionEnforcer, PermissionMode, check_bash(), check_file_write()
- `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\tools\src\lib.rs` — ToolSpec, execute_tool_with_enforcer(), classify_bash_permission(), allowed_tools_for_subagent(), execute_agent()

### Knowledge Base Synthesis Materials
- `BB-2026-05-01-325` — Claude Code official surface + npm package + historical reverse-engineering analysis
- `BB-2026-05-01-326` — Hello-Agents foundation: agent definition, memory, context, protocols, evaluation
- `BB-2026-05-01-327` — Claw Code: open-source Rust agent harness aligned with Claude Code surface
- `BB-2026-05-01-328` — Claude Code-style agent implementation map
- `BB-2026-05-01-329` — Minimal Claude Code-style open-source implementation blueprint
- `BB-2026-05-01-330` — FlagHunter vs Claw Code gap analysis and improvement roadmap

## Key Evidence Mapping

| Claim | Evidence Source |
|-------|----------------|
| 7 design principles | Synthesized from BB-325/326/327/328 + claw-code source analysis |
| Principle 1 (engineered ReAct) | claw-code `conversation.rs:run_turn()` |
| Principle 2 (unified tool contract) | claw-code `tools/lib.rs:ToolSpec`, `execute_tool_with_enforcer()` |
| Principle 3 (permission as hard gate) | claw-code `permission_enforcer.rs:PermissionEnforcer` |
| Principle 4 (subagent as first-class) | claw-code `tools/lib.rs:execute_agent()`, `allowed_tools_for_subagent()` |
| Principle 5 (externalized memory) | Official docs + CLAUDE.md system + Hello-Agents memory model |
| Principle 6 (GSSC pipeline) | Hello-Agents (BB-326) context engineering framework |
| Principle 7 (evolvable ecosystem) | Official plugin marketplace + MCP protocol |
| FlagHunter gap assessment | FlagHunter source + claw-code comparison (BB-330 evidence) |
| 4-Phase plan code sketches | Derived from claw-code architecture patterns, adapted to Python |
