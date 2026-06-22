# Source Evidence

- Title: Build Long-running AI agents that pause， resume， and never lose context with ADK
- BestBlogs URL: https://www.bestblogs.dev/en/article/7be5372c
- Original publisher URL: https://adk.dev/
- Original link text: Agent Development Kit (ADK)

## Captured Page Metadata

- Browser title: Build Long-running AI agents that pause， resume， and never lose context with ADK
- Description: This article from the Google Developers Blog presents a comprehensive architectural guide for building long-running AI agents that can survive idle periods, server restarts, and multi-day workflows. Using a New Hire Onboarding Coordinator Agent as a concrete example, the author walks through three key architectural shifts that separate production agents from stateless demo chatbots: implementing durable memory schemas via explicit state machines instead of relying on raw conversation history, using event-driven dormancy gates with webhooks instead of active polling, and employing multi-agent delegation for specialized sub-tasks. The tutorial provides complete Python code examples using the ADK framework, including state schema definition, persistent SQLite session storage, webhook endpoints for external event handling, and a resume handler that hydrates sessions and applies state transitions atomically. It also covers golden evaluation tests for validating multi-day flows and deployment to Google's Agent Runtime. The core insight is that stateless agents fail on real enterprise workflows due to prompt context pollution, token cost explosion, and reasoning hallucinations over idle time, and the solution is a fundamentally different architecture where agent state is explicit, durable, and decoupled from raw chat history.
- Date: 05-12

## Evidence Links Captured

- Agent Development Kit (ADK): https://adk.dev/
- GitHub: https://github.com/GoogleCloudPlatform/generative-ai/tree/main/agents/adk/new-hire-onboarding
- Agents CLI: https://github.com/google/agents-cli
- Cloud Run: https://cloud.google.com/run?e=48754805
- new-hire-onboarding repo: https://github.com/GoogleCloudPlatform/generative-ai/tree/main/agents/adk/new-hire-onboarding
- ADK documentation: https://adk.dev/
- Agents CLI: https://google.github.io/agents-cli/
