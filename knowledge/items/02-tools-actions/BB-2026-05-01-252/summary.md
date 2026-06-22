# BB-2026-05-01-252 Summary

## Article

- Title: Best practices for computer and browser use with Claude / Claude
- Source: BestBlogs / Claude Blog
- URL: https://www.bestblogs.dev/en/article/94694e50
- Date: 05-12
- Topic: `02-tools-actions`
- Tags: Claude, Computer Use, Browser Automation, Best Practices, Screenshot Scaling

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This blog post from the official Claude blog offers a comprehensive guide for developers building computer use agents with Claude's latest models (4.6 family and Opus 4.7). It identifies the single highest-impact optimization as pre-downscaling screenshots to fit API limits (1568px long edge / 1.15MP for 4.6; 2576px / 3.75MP for Opus 4.7) to prevent silent downscaling and coordinate mismatch. Recommended starting resolutions are 1280x720 for 4.6 models and 1080p for Opus 4.7, with a provided Python function for 'max API fit' per-image scaling. The guide covers diagnosing click issues (consistently offset, near misses, wrong element), model selection (Sonnet 4.6 for mechanical precision, Opus 4.7 for reasoning), handling small targets via zoom and keyboard alternatives, and content ordering (text before image). It also presents detailed recommendations for adaptive thinking effort levels: 'medium' is the sweet spot for 4.6 models, while 'high' is the default for Opus 4.7. Finally, it discusses prompt injection defenses, including training-time robustness, real-time classifiers, and continuous red teaming.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
