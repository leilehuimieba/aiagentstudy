# ReproRepo: Scaling Reproducibility Audits with GitHub Repository Issues

---

- Local ID: ARXIV-2026-007
- Source: arXiv
- arXiv ID: 2606.18237v1
- Date: 2026-06-16
- Authors: Shanda Li, Qiuhong Anna Wei, Jingwu Tang, Valerie Chen, Nihar B Shah, Tim Dettmers, Yiming Yang, Ameet Talwalkar
- Categories: cs.CL, cs.AI, cs.LG
- URL: https://arxiv.org/abs/2606.18237v1
- PDF: https://arxiv.org/pdf/2606.18237v1
- Capture depth: metadata + abstract

---

## Abstract

Reproducing research results from papers and released code is central to scientific progress. Existing works have introduced benchmarks to evaluate whether LLM agents can assist with reproducibility, but they are difficult to scale due to their reliance on substantial manual effort for data curation and evaluation. We introduce ReproRepo, a scalable framework for reproducibility evaluation that leverages human-raised GitHub issues as naturally occurring supervision on realistic reproduction blockers. We instantiate ReproRepo on 1,149 recent machine learning papers from major conferences and evaluate four frontier model-agent configurations. Our results show that LLM agents, even without executing code, can identify many real-world reproducibility problems from paper-repository pairs: the best agent in our study, namely Codex with GPT-5.5, surfaces at least one semantically related human-reported blocker for ~90% of papers in the study. Further analysis shows that agents are particularly effective for surfacing visible failures and identifying the right semantic region, but may still be insufficient in exact localization. ReproRepo can serve as a reusable, scalable framework for future evaluations of LLM agents on real-world reproducibility auditing. Our code is released at https://github.com/LithiumDA/ReproRepo.

## Capture Notes

This is an abstract-level paper capture from the arXiv API. The PDF URL is preserved for full-text reading and later deep extraction.
