# Source Evidence

- Title: Best practices for computer and browser use with Claude | Claude
- BestBlogs URL: https://www.bestblogs.dev/en/article/94694e50
- Original publisher URL: https://www.anthropic.com/news/claude-sonnet-4-6
- Original link text: latest models

## Captured Page Metadata

- Browser title: Best practices for computer and browser use with Claude | Claude
- Description: This blog post from the official Claude blog offers a comprehensive guide for developers building computer use agents with Claude's latest models (4.6 family and Opus 4.7). It identifies the single highest-impact optimization as pre-downscaling screenshots to fit API limits (1568px long edge / 1.15MP for 4.6; 2576px / 3.75MP for Opus 4.7) to prevent silent downscaling and coordinate mismatch. Recommended starting resolutions are 1280x720 for 4.6 models and 1080p for Opus 4.7, with a provided Python function for 'max API fit' per-image scaling. The guide covers diagnosing click issues (consistently offset, near misses, wrong element), model selection (Sonnet 4.6 for mechanical precision, Opus 4.7 for reasoning), handling small targets via zoom and keyboard alternatives, and content ordering (text before image). It also presents detailed recommendations for adaptive thinking effort levels: 'medium' is the sweet spot for 4.6 models, while 'high' is the default for Opus 4.7. Finally, it discusses prompt injection defenses, including training-time robustness, real-time classifiers, and continuous red teaming.
- Date: 05-12

## Evidence Links Captured

- latest models: https://www.anthropic.com/news/claude-sonnet-4-6
- tool configuration: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- adaptive thinking: https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking
- Prompt Injection Classifiers Interest Form.: https://docs.google.com/forms/d/e/1FAIpQLSfXj6rXC-SUQEYHCLabwUe5JuYiYyJ29Ja-KP7EhLIPlyz0tw/viewform?usp=dialog
- approach to prompt injection defenses: https://www.anthropic.com/research/prompt-injection-defenses
- official computer use tool: https://docs.anthropic.com/en/docs/agents-and-tools/computer-use
- fill out this interest form: https://docs.google.com/forms/d/e/1FAIpQLSfXj6rXC-SUQEYHCLabwUe5JuYiYyJ29Ja-KP7EhLIPlyz0tw/viewform?usp=dialog
- context management: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- server-side compaction: https://docs.anthropic.com/en/docs/build-with-claude/compaction
- advisor tool: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
- computer use documentation: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- original computer use research post: https://www.anthropic.com/news/developing-computer-use
