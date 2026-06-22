# Source Evidence

- Title: Claw Code：一个对齐 Claude Code 产品表面的开源 Rust Agent Harness
- Canonical URL: https://github.com/ultraworkers/claw-code
- Evidence date: 2026-05-26

## Primary public sources

- Repository root: https://github.com/ultraworkers/claw-code
- Repository README: https://github.com/ultraworkers/claw-code/blob/main/README.md
- Rust workspace README: https://github.com/ultraworkers/claw-code/blob/main/rust/README.md
- Parity document: https://github.com/ultraworkers/claw-code/blob/main/PARITY.md
- Concept document: https://github.com/ultraworkers/claw-code/blob/main/concept.md
- Conversation runtime: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/runtime/src/conversation.rs
- Tools registry / executor: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/tools/src/lib.rs
- Permission enforcer: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/runtime/src/permission_enforcer.rs
- Task registry: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/runtime/src/task_registry.rs
- MCP bridge: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/runtime/src/mcp_tool_bridge.rs
- LSP registry: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/runtime/src/lsp_client.rs
- CLI entrypoint: https://github.com/ultraworkers/claw-code/blob/main/rust/crates/rusty-claude-cli/src/main.rs

## Captured local artifacts

- Local repo clone: `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code`
- Repo HEAD at capture: `d4494a8aeb8446164e1a7260def1d4e77cef243c`
- Key files inspected:
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\README.md`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\PARITY.md`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\concept.md`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\conversation.rs`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\tools\src\lib.rs`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\permission_enforcer.rs`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\task_registry.rs`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\mcp_tool_bridge.rs`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\runtime\src\lsp_client.rs`
  - `D:\newwork\aiagentstudy\knowledge\raw\external\claw-code\rust\crates\rusty-claude-cli\src\main.rs`

## Local verification runs

- `cargo check -p runtime --lib` ✅
- `cargo test -p tools agent_tool_subset_mapping_is_expected` ✅
- `cargo test -p tools enter_and_exit_plan_mode_round_trip_existing_local_override` ✅
- `cargo test -p tools run_task_packet_creates_packet_backed_task` ✅
- `cargo test -p runtime run_turn_errors_when_max_iterations_is_exceeded -- --exact` ❌ on Windows test build due Unix-only `std::os::unix::fs::PermissionsExt` usage inside runtime test modules (`mcp_stdio.rs`, `mcp_tool_bridge.rs`)

## Evidence note

This repository explicitly describes itself as a **public Rust implementation** of the `claw` CLI harness and states that it is **not affiliated with, endorsed by, or maintained by Anthropic**. It should be used as a comparative, open-source Claude Code-style harness — not as proof that Anthropic has open-sourced the current Claude Code core runtime.
