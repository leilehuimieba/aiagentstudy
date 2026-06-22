# Server-side template injection

- Extraction: Web Security Academy topic page excerpts
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://portswigger.net/web-security/server-side-template-injection

---

## Key Evidence

The Academy page operationalizes SSTI methodology into a practical workflow: detect, identify the engine, exploit, explore objects, and create custom attacks. It also links to realistic labs, which makes it particularly suitable for converting into automated strategy steps.

## Extracted Excerpts

- Try fuzzing the template with special characters before deeper probing.
- If fuzzing is inconclusive, still test context-specific approaches for plaintext and code context.
- For plaintext context, arithmetic payloads such as ${7*7} provide a clean proof-of-concept when the output renders as 49.
