# Language Agents as Hackers: Evaluating Cybersecurity Skills with Capture the Flag

- Extraction: OpenReview abstract + result excerpts
- BestBlogs URL: Not found during this capture
- Original publisher URL: https://openreview.net/forum?id=KOZwk7BFc3

---

## Abstract

The paper introduces InterCode-CTF, a benchmark for evaluating language agents on capture-the-flag tasks. The benchmark contains 100 verified task instances spanning reverse engineering, forensics, cryptography, binary exploitation, and web exploitation.

## Key Evidence

- The benchmark provides 100 executable cybersecurity tasks.
- GPT-4 out of the box solves 40/100 tasks.
- The authors note that GPT-4 struggles on harder tasks requiring multiple investigative steps and specialized skills.
- The paper explicitly observes a repeated-command failure mode: when stuck, the model often repeats near-duplicate commands instead of switching tactics.

## Extracted Excerpts

> We manually collect and verify a benchmark of 100 task instances that require a number of cybersecurity skills such as reverse engineering, forensics, and binary exploitation.

> We evaluate GPT-4 out of the box and find that while it manages to solve 40 tasks, it still struggles with more complex problems that require multiple investigative steps and specialized cybersecurity skills to solve.

> While human task workers might recognize these situations and devise alternative tactics, GPT-4 will tend to repeat commands with small adjustments.
