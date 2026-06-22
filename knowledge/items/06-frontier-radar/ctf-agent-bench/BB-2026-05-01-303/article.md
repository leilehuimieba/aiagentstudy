# Training Language Model Agents to Find Vulnerabilities with CTF-Dojo

- Extraction: arXiv abstract and result summary
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://arxiv.org/abs/2508.18370

---

## Abstract

CTF-Dojo introduces a large-scale executable runtime for training LLM agents with verifiable feedback in cybersecurity. The system contains 658 fully functional Dockerized CTF-style challenges and a CTF-Forge pipeline for turning public artifacts into runnable environments.

## Key Evidence

- 658 reproducible challenges are containerized with guaranteed reproducibility.
- The training set uses 486 high-quality, execution-verified trajectories.
- The paper reports up to 11.6% absolute gains across InterCode-CTF, NYU CTF Bench, and Cybench.
- The best 32B model reaches 31.9% Pass@1.

## Extracted Excerpts

> We introduce CTF-Dojo, the first large-scale executable runtime tailored for training LLMs with verifiable feedback.

> We trained LLM-based agents on just 486 high-quality, execution-verified trajectories, achieving up to 11.6% absolute gains.

> Our best-performing 32B model reaches 31.9% Pass@1.
