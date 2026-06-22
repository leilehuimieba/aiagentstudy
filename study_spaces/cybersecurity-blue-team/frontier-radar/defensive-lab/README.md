# AI / Agent Threat Defensive Lab

> Created: 2026-06-18
> Scope: defensive samples for testing prevention, blocking, logging, and analysis.

This directory is a defensive test corpus for AI/Agent-era security risks. It intentionally avoids weaponized exploit payloads. Samples are normalized, synthetic, and designed to exercise controls such as WAF, API gateway rules, EDR, process monitoring, workflow import review, MCP allowlists, AI memory controls, and data-loss prevention.

Use this corpus to answer:

1. Can we recognize the risky shape before code runs?
2. Which trust boundary failed: HTTP input, imported workflow, MCP config, agent command, memory write, or AI search rendering?
3. Which control should block it: auth, schema validation, transport policy, command allowlist, sandbox, egress filtering, output sanitizer, memory confirmation, or secret isolation?
4. Which logs prove that the attack reached the dangerous stage?

## Files

- [attack-chain-test-matrix.md](attack-chain-test-matrix.md): case-by-case attack chains, block points, and telemetry goals.
- [synthetic-samples.jsonl](synthetic-samples.jsonl): machine-readable synthetic samples for test harnesses.
- [intel-derived-sample-candidates-2026-06-18.jsonl](intel-derived-sample-candidates-2026-06-18.jsonl): structured sample ideas derived from current AI/Agent threat intelligence.
- [intel-derived-sample-candidates-2026-06-18-04.jsonl](intel-derived-sample-candidates-2026-06-18-04.jsonl): additional candidate samples for AI coding agents, MCP telemetry, CI/CD agents, and package/build supply chain attacks.
- [intel-derived-sample-candidates-2026-06-18-05.jsonl](intel-derived-sample-candidates-2026-06-18-05.jsonl): candidate samples for MCP tool poisoning, malicious MCP servers, AI credential theft, and extension marketplace fail-open cases.
- [intel-derived-sample-candidates-2026-06-18-06.jsonl](intel-derived-sample-candidates-2026-06-18-06.jsonl): candidate samples from social media and developer community intelligence, including privileged support agents, GitHub metadata injection, CI cache poisoning, Codex token theft, GlassWorm-style extension dependencies, and MCP metadata poisoning.
- [intel-derived-sample-candidates-2026-06-18-07.jsonl](intel-derived-sample-candidates-2026-06-18-07.jsonl): candidate samples from logged-in X/community monitoring, covering Mastra/easy-day-js supply-chain poisoning, semver range traps, AI framework mass publish, malicious agent skills, DDIPE-style documentation reuse, and authorized chain anomalies.
- [intel-derived-sample-candidates-2026-06-18-08.jsonl](intel-derived-sample-candidates-2026-06-18-08.jsonl): candidate samples for MCP runtime vulnerabilities, public telemetry as prompt source, SearchLeak-style enterprise AI search exfiltration, RAG poisoning, malicious model repositories, unsafe model loading, and least-privilege tool gating.
- [intel-derived-sample-candidates-2026-06-18-09.jsonl](intel-derived-sample-candidates-2026-06-18-09.jsonl): candidate samples for email/calendar/browser agents, malicious AI browser extensions, OAuth connectors, non-human identity drift, MCP confused deputy, multi-agent delegation, A2A metadata poisoning, auto resource discovery, and agent payments.
- [intel-derived-sample-candidates-2026-06-18-10.jsonl](intel-derived-sample-candidates-2026-06-18-10.jsonl): candidate samples for AI-generated code vulnerabilities, IaC/DevOps agent misconfigurations, Docker/Kubernetes/CI risks, persistent memory poisoning, compressed-context provenance loss, and checkpoint state restoration.
- [intel-derived-sample-candidates-2026-06-18-11.jsonl](intel-derived-sample-candidates-2026-06-18-11.jsonl): candidate samples for recent KEV-style CMS/VPN/SD-WAN risks, install-time supply-chain execution, Agent Skill behavioral mismatch, MCP metadata poisoning, AI scanner prompt injection, cloud logging tampering, and edge-device visibility gaps.
- [intel-derived-sample-candidates-2026-06-18-12.jsonl](intel-derived-sample-candidates-2026-06-18-12.jsonl): candidate samples from non-X sources, covering GitHub advisory provenance gaps, malicious AI SDK import-time behavior, sandbox read-only bypass, VPN auth-cookie indicators, SD-WAN regression chains, DFIR intrusion timelines, delayed webapp code execution, SAML signature wrapping, and scan-signal-driven patch prioritization.
- [intel-derived-sample-candidates-2026-06-18-13.jsonl](intel-derived-sample-candidates-2026-06-18-13.jsonl): candidate samples for PraisonAI MCP path handling, Guardrails Hub manifest execution, ML package compromise, @cap-js self-propagating packages, Mastra postinstall staging, PeopleSoft zero-day extortion, SaaS vishing, agent approval bypass, and VPN-to-LPE intrusion chains.
- [intel-derived-sample-candidates-2026-06-18-14.jsonl](intel-derived-sample-candidates-2026-06-18-14.jsonl): candidate samples for traditional vulnerability collection, including Exim Dead.Letter exposure, HTTP/2 Bomb triage, distro backport ambiguity, HashiCorp go-getter/consul-template/Vault/Boundary issues, MDX SSR RCE, edge VPN priority override, and forum-driven temporary mitigations.
- [detection-rule-sketches.md](detection-rule-sketches.md): detection and prevention logic sketches for WAF, EDR, MCP gateways, AI search, and memory controls.
- [authorized-exploit-testing-playbook.md](authorized-exploit-testing-playbook.md): safe workflow for real exploit validation in owned or explicitly authorized labs.

## Safety Boundary

These samples are for owned lab systems and defensive analysis only.

- Do not replay request-shaped samples against third-party systems.
- Do not turn placeholders into real commands.
- Do not include real secrets, real tenant URLs, real emails, or real cloud credentials in tests.
- Prefer a mock service that records requests and emits synthetic logs.

## Recommended Test Harness Shape

```text
synthetic sample
-> parser / gateway / importer / agent policy layer
-> expected decision: allow, warn, block, quarantine, require approval
-> expected telemetry: normalized event, risk reason, sample id, matched rule
-> regression assertion
```

## Initial Risk Classes

| Class | Example cases | Best blocking layer |
|---|---|---|
| AI workflow RCE | Langflow CVE-2026-33017, Langflow CVE-2026-5027 | Auth, schema validation, no server-side dynamic code, upload path normalization |
| MCP / tool config execution | Flowise CVE-2026-40933, MCP stdio class | Transport policy, command allowlist, workflow import review, sandbox |
| Agent command argument abuse | Prompt injection to RCE | argv policy, sandbox, tool-specific dangerous flag blocking |
| Agent memory poisoning | AI Recommendation Poisoning | memory-write confirmation, source attribution, risk keywords |
| AI search exfiltration | SearchLeak CVE-2026-42824 | P2P separation, output sanitization before streaming, no auto-load remote resources |
| Agent memory/checkpoint injection | LangGraph checkpointer chain | query parameterization, metadata key validation, safe serialization |
