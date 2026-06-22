# BB-2026-05-01-549 Summary

## Article

- Title: Who Is the Strongest Goalkeeper for Agents? The First Agent Skill Security Evaluation Benchmark, SkillTrustBench, Officially Released
- Source: BestBlogs / 腾讯技术工程
- URL: https://www.bestblogs.dev/article/15507569
- Date: 06-16
- Topic: `02-tools-actions`
- Tags: AI Agent, AI Security, LLM, Agent Security, Security Evaluation

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article, jointly released by Tencent朱雀Lab and The Chinese University of Hong Kong, Shenzhen, officially introduces SkillTrustBench—the first dual-purpose benchmark for evaluating both the security and trustworthiness of Agent skills in real-world deployment scenarios and the detection effectiveness of external scanning solutions. The article first outlines the severe state of Agent skill security threats: the ClawHavoc incident in early 2026 led to 1,184 malicious skills being listed; a Snyk report showed 36.82% of skills had security issues; Tencent朱雀Lab's full scan revealed that 74.6% of 50,000 skills declared network request permissions, with highly decentralized external communication channels. It then points out the shortcomings of current scanning solutions: the maximum overlap of positive samples between different tools is only 10.4%, 81.9% of flagged samples are detected by only a single solution, and attackers have begun using input truncation, file type blind spots, social engineering, and other methods to bypass detection. SkillTrustBench distills 5,520 evaluation cases from 62,652 real skills, covering nine threat categories (T01-T09), with a special introduction of 'T09 Unsafe Coding Behavior' to assess skills that are non-malicious but have security flaws. The initial evaluation compared three open-source solutions—Skill Vetter, Cisco Skill Scanner, and NVIDIA SkillSpector—along with model backbones like Claude Opus 4.6, GLM 5.1, and DeepSeek V4 Flash. It found that high recall often comes with high false positives, and a truly deployable solution needs to balance recall and false positives.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
