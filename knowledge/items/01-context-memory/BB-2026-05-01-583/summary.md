# BB-2026-05-01-583 Summary

## Article

- Title: QoderWork Skills Development Practice: Exploring the Transition from Traditional Data Science to AI Data Science - My Skills Advancement Journey
- Source: BestBlogs / 大淘宝技术
- URL: https://www.bestblogs.dev/article/35406486
- Date: 06-26
- Topic: `01-context-memory`
- Tags: AI Agent, Prompt Engineering, AI Coding, Domain Knowledge Engineering, LLM

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author, Zi Sui (from the Taobao & Tmall Group Live Streaming Technology Team), details the QoderWork Skills development system and engineering philosophy based on personal practice. The article first identifies the pain points of data science teams repeatedly running data and manually generating reports, introducing the value of Skills as "digital assistants." The core section proposes a four-layer separation architecture: SKILL.md (orchestration layer, solely responsible for process guidance), config.yaml (parameter template layer, avoiding hardcoding business values), scripts/ (implementation layer, solidifying complex logic like statistical tests and field detection), and references/ (knowledge layer, enabling progressive information disclosure). Subsequently, by deconstructing the design concepts of excellent community Skills (Follow Builders, Frontend Slides)—such as Frontend Slides' use of "NON-NEGOTIABLE" tags, anti-pattern lists, and one-shot data collection instructions—it demonstrates the concrete form of this architecture in practice. The author also shares two self-developed Skills: User Insight Report Generation (including RFM segmentation and the PIA insight framework) and AB Testing Analysis (including mandatory SRM checks, automatic method selection, and a conclusion determination matrix), summarizing the development methodology: Description is the soul, provide processes rather than code, templates are more controllable than free-form generation, config is a template not a form, and control the length. Finally, the author compares Idealab's RAG practices with QoderWork Skills, arguing that AI's ceiling depends on the quality of injected domain knowledge, and the core of data science transformation is freeing up human effort to focus on high-value business problems.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
