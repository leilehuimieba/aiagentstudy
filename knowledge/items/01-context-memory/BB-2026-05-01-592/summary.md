# BB-2026-05-01-592 Summary

## Article

- Title: GitHub - deeplethe/forkd: Fork() for AI agent microVMs. Spawn 100 children in ~100ms from a warm parent; BRANCH a live VM in ~150ms. KVM-isolated， snapshot CoW.
- Source: BestBlogs / Hacker News - Newest: "AI Agent"
- URL: https://www.bestblogs.dev/article/0ba05e87
- Date: 06-23
- Topic: `01-context-memory`
- Tags: AI Agent, MicroVM, Firecracker, Sandbox, Copy-on-Write

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

forkd is an open-source microVM runtime built on Firecracker, designed for AI agent workloads that need fast, isolated sandbox fan-out. It boots a parent VM once, warms the runtime (e.g., Python + deps), pauses it to disk, and then spawns children by mmap'ing the parent's memory image with MAP_PRIVATE (kernel CoW). This yields per-child KVM isolation with a spawn cost closer to fork(2) than cold boot. The project also introduces BRANCH (live snapshot of a running sandbox in ~150ms) and diff-snapshot chains (stacked layers to avoid duplicating shared base images). Benchmarks show 101ms to spawn 100 sandboxes (vs. 759ms for Firecracker cold-boot, 1.06s for CubeSandbox, and >100s for Docker/gVisor). A demo shows branching an LLM agent mid-ReAct-loop to explore alternate strategies with shared reasoning state. The README includes design documents, detailed benchmarks, and comparisons with other sandbox technologies.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
