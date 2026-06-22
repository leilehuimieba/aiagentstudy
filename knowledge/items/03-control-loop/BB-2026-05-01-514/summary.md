# BB-2026-05-01-514 Summary

## Article

- Title: The crash that vanished: control and emergence in a five-model economy
- Source: BestBlogs / Hugging Face - Blog
- URL: https://www.bestblogs.dev/article/74c97796
- Date: 06-08
- Topic: `03-control-loop`
- Tags: AI Agent, Emergence, Multi-Agent Systems, Simulation, LLM

## Model Mapping

- Blocks: Goal, Context/State, Control Loop, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author recounts a lesson from the Build Small Hackathon. Initially, a single small model running five woodland creatures produced an emergent bank-run-style crash when a rumor triggered a sell-off. However, when the system was rebuilt with a council of five distinct small models from different labs (OpenAI, NVIDIA, OpenBMB, and a fine-tuned model), the same rumor caused the agents to hoard honey instead of dumping it, making the crash disappear. The author describes three failed attempts to force the crash by manipulating economic inputs (rumor, inventory glut, larger short), which worked against a simple test policy but failed against the live heterogeneous agents. The resolution was to author the crash as a deterministic override at the settlement seam, after all agent trading is complete. The key takeaway is that emergent behavior from one agent population is not durable; you cannot reliably control a market of diverse agents by shocking inputs; and cheap simulators can give false confidence. The craft lies in knowing where to let emergence run and where to impose authored control.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
