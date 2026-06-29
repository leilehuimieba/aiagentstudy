# BB-2026-05-01-643 Summary

## Article

- Title: Codex Logs Are Burning Your SSD
- Source: BestBlogs / 浮之静
- URL: https://www.bestblogs.dev/article/58fb6bc9
- Date: 06-22
- Topic: `02-tools-actions`
- Tags: AI Coding, Codex, Logging System, SQLite, Performance Optimization

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article dissects the logging system issue in OpenAI Codex: its persistent SQLite log sink defaults to accepting TRACE-level logs from all targets, bypassing the user-set `RUST_LOG=warn` filter, leading to continuous high-frequency writes to `logs_2.sqlite` and its WAL file during streaming output. From the source code perspective, the article explains the write amplification mechanism (WAL mode, multiple indexes, insert-prune cycle), cites data from open issues on GitHub such as #17320 and #28224 (e.g., 5 MiB/s write rate, extrapolated 640 TB writes per year), and points out that the file size users see may differ dramatically from actual SSD write volume. The author stratifies the risks to avoid over-panicking, while emphasizing that Mac users face higher risk. The article evaluates three mitigation measures circulating online (SQLite trigger to block inserts, symlink to /tmp or a ramdisk, migrating the SQLite directory to an external drive), detailing their limitations and proper usage. Finally, it proposes the truly necessary upstream fixes: narrowing the default filter, sanitizing protocol payloads, and adding a global size cap. The article cites specific code lines and issue links, with rigorous reasoning and practical advice.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
