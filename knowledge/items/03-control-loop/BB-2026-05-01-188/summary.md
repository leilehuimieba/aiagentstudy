# BB-2026-05-01-188 Summary

## Article

- Title: Building a general-purpose accessibility agent—and what we learned in the process
- Source: BestBlogs / The GitHub Blog
- URL: https://www.bestblogs.dev/en/article/1ca8b942
- Date: Yesterday
- Topic: `03-control-loop`
- Tags: Accessibility, AI Agent, LLM, GitHub Copilot, WCAG

## Model Mapping

- Blocks: Goal, Control Loop, Tools/Actions, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details GitHub's experimental general-purpose accessibility agent, designed to provide just-in-time accessibility answers and automatically remediate simple, objective issues before they reach production. The agent has reviewed 3,535 pull requests with a 68% resolution rate, with top issues including structural clarity, interactive control naming, and status messages. Key architectural decisions include using a sub-agent architecture with a passive reviewer and an active implementer, executing instructions in a linear order, and using template schemas for consistent communication. The article emphasizes that the agent is not a silver bullet but an augmentation tool, and that its effectiveness depends on being trained on manually audited and remediated accessibility issues. It also covers critical limitations: evaluating code complexity to avoid unsafe changes, identifying high-risk patterns like drag-and-drop and rich text editors, reducing the LLM's bias toward generating code, and acknowledging that 36% of WCAG A and AA success criteria cannot be detected automatically. The agent's output is periodically manually reviewed to refine instructions.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
