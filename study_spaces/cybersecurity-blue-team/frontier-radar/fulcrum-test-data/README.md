# Fulcrum Test Data Pack

> Created: 2026-06-18
> Target project: private GitHub repo `leilehuimieba/Fulcrum`
> Mode: data collection and test design only; no exploit execution.

This pack is designed to fit Fulcrum's current architecture and evaluation schema.

Observed Fulcrum shape from the private repository page:

- Project positioning: agent security middleware for governed enterprise scenarios.
- Key risk surfaces: input pollution, tool call abuse, extension/MCP/Skill supply chain, audit and reproducible evaluation.
- Current pipeline: `labeler -> detectors -> attributor -> risk_scorer -> chain_analyzer -> policy -> executor/tools -> audit/model`.
- Current detector baseline: deterministic `keyword_rules` covering six categories:
  - `injection`
  - `jailbreak`
  - `exfiltration`
  - `sensitive_file`
  - `command_exec`
  - `data_poisoning`
- Current policy conditions:
  - `tool_in`
  - `tool_name`
  - `source_trust`
  - `risk_at_least`
  - `attribution_at_least`
  - `risk_level`
  - `path_sensitive`
  - `path_outside_workspace`
  - `domain_allowed`
  - `command_dangerous`
- Current policy actions:
  - `allow`
  - `sanitize`
  - `approve`
  - `block`
- Current `samples/` directory appears to contain only `README.md`, so this pack can become the first practical sample seed after review.

## Files

- [fulcrum_eval_samples.jsonl](fulcrum_eval_samples.jsonl): Fulcrum-schema-aligned test samples.
- [coverage_matrix.md](coverage_matrix.md): mapping from samples to detector/policy/evaluation goals.
- [ingestion_notes.md](ingestion_notes.md): suggested migration into Fulcrum `samples/` and evaluation scripts.

## Safety

Samples are intentionally non-executing and use placeholders such as `SAFE_CANARY_*`, `example.invalid`, and fake paths. They are meant to validate parsing, classification, policy decisions, audit evidence, and report metrics.

If you later add real exploit reproductions, keep those outside public/static paths and use an explicitly authorized lab fixture. Store only metadata and sanitized traces in the repo.

