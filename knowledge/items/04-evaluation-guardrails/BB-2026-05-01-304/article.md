# SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

- Extraction: arXiv abstract snippet
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://arxiv.org/abs/2310.06770

---

## Abstract-Oriented Notes

SWE-bench frames software engineering evaluation as a grounded task: given a real repository and a GitHub issue, the model must produce a patch that can be applied and validated by the project test suite. This is a strong example of execution-based, environment-grounded evaluation instead of answer-string matching.

## Why it matters for FlagHunter

- It separates task description from environment state.
- It makes final scoring deterministic through executable validation.
- It naturally supports regression testing after agent changes.
