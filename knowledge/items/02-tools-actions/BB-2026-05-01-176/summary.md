# BB-2026-05-01-176 Summary

## Article

- Title: Agent Skill Specifications, Construction, and Design Patterns
- Source: BestBlogs / 阿里云开发者
- URL: https://www.bestblogs.dev/en/article/ad38855c
- Date: 05-12
- Topic: `02-tools-actions`
- Tags: Agent Skill, Skill-Creator, Writing-Skills, Design Patterns, Prompt Engineering

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Starting from the specification standards for Agent Skills, the article details the SKILL.md format proposed by Anthropic, including YAML metadata fields, Markdown instruction body, file reference specifications, and a three-tier progressive loading mechanism (L1 directory layer, L2 instruction layer, L3 resource layer), emphasizing a description-based, model-driven triggering logic. It then delves into two mainstream Skill development paradigms: Anthropic's official Skill-Creator, whose design philosophy introduces ML engineering practices (train/test set splitting, anti-overfitting) into Prompt Engineering, forming a complete evaluation chain through three specialized Agent roles—Grader, Comparator, and Analyzer; and the Writing-Skills within the Superpowers framework, which employs a RED-GREEN-REFACTOR TDD cycle to create and optimize Skills. The article also summarizes the advantages of Skill-Creator (complete methodology, rigorous evaluation system) and its limitations (high token consumption, lengthy process, steep learning curve), and introduces five Skill design patterns summarized by the Google ADK team: Tool Wrapper, Generator, Workflow, Specification, and Meta-Skill.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
