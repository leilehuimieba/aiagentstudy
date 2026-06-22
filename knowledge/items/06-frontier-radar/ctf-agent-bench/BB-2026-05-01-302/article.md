# Hacking CTFs with Plain Agents

- Extraction: arXiv abstract + result excerpts
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://arxiv.org/abs/2412.02776

---

## Abstract

This paper argues that plain LLM-agent design can nearly saturate a high-school-level hacking benchmark. Using prompting, tool use, and multiple attempts, the authors reach 95% performance on InterCode-CTF.

## Key Evidence

- The paper reports 95% performance (81/85) on InterCode-CTF with ReAct&Plan@5.
- It explicitly compares against earlier results: InterCode baseline 40%, EnIGMA 72%, and a DeepMind result at 29%.
- Category saturation is strongest for general skills, web exploitation, reverse engineering, and binary exploitation.
- The paper notes occasional guessed flags from unrelated tasks, warning that contamination remains a live benchmark risk.

## Extracted Excerpts

> We obtain 95% performance on InterCode-CTF, a popular offensive security benchmark, using prompting, tool use, and multiple attempts.

> Using primarily prompt engineering and function calling, we solved 95% of tasks (81/85) compared to their 72% (72/100).

> We observed the agent occasionally guessing flags from unrelated tasks.
