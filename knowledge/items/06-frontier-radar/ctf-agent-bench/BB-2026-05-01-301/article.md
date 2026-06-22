# NYU CTF Bench: A Scalable Open-Source Benchmark Dataset for Evaluating LLMs in Offensive Security

- Extraction: arXiv abstract + result excerpts
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://arxiv.org/abs/2406.05590

---

## Abstract

The paper introduces a public benchmark built from CSAW capture-the-flag challenges to evaluate LLMs in offensive cybersecurity. The dataset contains 200 validated challenges across crypto, forensics, pwn, reverse engineering, web, and misc categories, paired with an automated evaluation framework and external tool support.

## Key Evidence

- The benchmark contains 200 validated challenges from 2017-2023 CSAW events.
- The authors report per-model solved percentages and failure types.
- Table 4 breaks failures into give up, round exceeded, connection failure, token exceeded, and wrong answer.
- The paper also compares LLM scores against human CSAW participants.

## Extracted Excerpts

> We present a large, high-quality, public dataset of 200 CTF challenges and a framework to evaluate a wide array of LLMs on these challenges, integrated with access to eight critical cybersecurity tools.

> GPT-4 performed the best overall, though its success was limited.

> Table 4 reports failure rates by type: give up, round exceeded, connection failure, token exceeded, and wrong answer.
