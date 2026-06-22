# BB-2026-05-01-219 Summary

## Article

- Title: After Shama and Sima, Another One Goes Viral! OpenHuman Gets to Know Everything About You in 20 Minutes and Stores It in a Karpathy-Style Knowledge Base
- Source: BestBlogs / 量子位
- URL: https://www.bestblogs.dev/en/article/d7d0e59a
- Date: Yesterday
- Topic: `01-context-memory`
- Tags: OpenHuman, Agent, Personal Knowledge Base, Automation, Open Source

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article introduces the open-source project OpenHuman, an Agent tool that requires no active training or configuration from users. Unlike 'Shama'-style Agents that require users to write Prompts and configure workflows, OpenHuman connects over 118 services including Gmail, GitHub, Slack, and Notion with a single authorization, automatically polling and fetching new data every 20 minutes. The fetched data is cleaned, compressed, and structured into a 'memory tree', ultimately stored as a local SQLite database and Markdown files compatible with Obsidian. Additionally, OpenHuman includes the TokenJuice compression mechanism, which reduces Token consumption by 80%, and a virtual avatar called Mascot that can participate in Google Meet meetings. The article argues that OpenHuman solves three major pain points: API key management, data fragmentation, and context bloat. Its core value lies in 'understanding you' rather than just 'being capable'.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
