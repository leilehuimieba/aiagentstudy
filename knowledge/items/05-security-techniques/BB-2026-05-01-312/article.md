# Server-Side Template Injection

- Extraction: PortSwigger Research article excerpts
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://portswigger.net/research/server-side-template-injection

---

## Key Evidence

The article introduces a high-level methodology for SSTI: Detect, Identify, Exploit. It distinguishes plaintext context from code context, recommends generic template-agnostic arithmetic payloads for initial detection, and demonstrates engine-specific exploitation and sandbox escapes.

## Extracted Excerpts

- Template injection can be detected by embedding an arithmetic statement and checking whether the server evaluates it.
- Plaintext context and code context require different detection methods.
- The paper demonstrates engine-specific exploitation paths and sandbox escapes across multiple popular template engines.
