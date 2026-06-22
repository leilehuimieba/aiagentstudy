# BB-2026-05-01-221 Summary

## Article

- Title: What Parameter Golf taught us
- Source: BestBlogs / OpenAI Blog
- URL: https://www.bestblogs.dev/en/article/5499bd5a
- Date: 05-12
- Topic: `04-evaluation-guardrails`
- Tags: Parameter Golf, Machine Learning, AI Coding Agents, OpenAI, Research Competition

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

OpenAI's Parameter Golf challenge invited participants to minimize held-out loss on a FineWeb dataset under strict constraints: a 16 MB artifact limit (model weights + training code) and a 10-minute training budget on 8×H100s. Over eight weeks, more than 1,000 participants submitted over 2,000 entries. The post details standout technical approaches across several themes: training optimization (e.g., Muon weight decay, spectral embedding initialization), quantization (GPTQ-lite, full Hessian GPTQ), test-time training strategies, and novel modeling ideas (CaseOps tokenizer, XSA attention, SmearGate, mini depth recurrence). A key finding was the widespread use of AI coding agents, which lowered the barrier to entry and accelerated the pace of experimentation but also introduced challenges for submission review and scoring. OpenAI developed an internal Codex-based triage bot to manage the high volume of submissions. The challenge also served as a talent discovery surface. The post concludes with OpenAI's intention to run more such challenges in the future.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
