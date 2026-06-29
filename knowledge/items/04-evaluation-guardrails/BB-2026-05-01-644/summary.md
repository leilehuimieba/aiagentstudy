# BB-2026-05-01-644 Summary

## Article

- Title: Fintech Engineering Handbook
- Source: BestBlogs / Hacker News
- URL: https://www.bestblogs.dev/article/9b7ac3e7
- Date: 06-27
- Topic: `04-evaluation-guardrails`
- Tags: Fintech, Financial Systems, Engineering Practices, Double-Entry Bookkeeping, Event Sourcing

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The Fintech Engineering Handbook is a living document aimed at software engineers building systems where money is the primary focus. It is structured around three core principles: no invented data, no lost data, and no trust. The handbook begins with representing money, covering precision handling (floating-point, arbitrary precision, minor-units, rational numbers), rounding strategies, currency handling (packaging amount and currency, no cross-currency arithmetic, controlled currency set), and FX rates (directionality, time, transactional vs reference rates). It then moves to recording money via the ledger, explaining double-entry bookkeeping, distinction between value time, booking time, and settlement time, audit trails, event sourcing, immutability, reversals and corrections, and GDPR considerations. Finally, it introduces executing money flows with invariants. The content is practical, with clear trade-offs and principles touched for each pattern.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
