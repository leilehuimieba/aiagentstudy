# BB-2026-05-01-579 Summary

## Article

- Title: A Mechanistic Explanation of Prompt Injection (and why you should study roles) — LessWrong
- Source: BestBlogs / LessWrong
- URL: https://www.bestblogs.dev/article/8f187d0e
- Date: 06-22
- Topic: `01-context-memory`
- Tags: LLM, Prompt Injection, AI Safety, AI Security, Role Confusion

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The article presents a mechanistic explanation of prompt injection based on how LLMs internally perceive role tags. The authors develop role probes to measure the LLM's internal belief about which role each token belongs to, and show that role perception is driven by writing style rather than the actual tag. This leads to role confusion: text that sounds like a user command or reasoning style overrides the assigned role tag. They introduce a new attack, CoT Forgery, which places fake reasoning inside a user prompt to trick the model into treating it as its own thinking, achieving ~60% success on jailbreak benchmarks. They also show that standard prompt injections on tool outputs succeed when the injected text sounds user-like (e.g., prepending "User: "). The core finding is that roles are soft boundaries reconstructed from surface features, not hard architectural boundaries, and this enables prompt injection. The article advocates for a new subfield studying the science of roles, and outlines open research directions including subconscious steering and principled role design.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
