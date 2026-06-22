# Source Evidence

- Title: "OncoAgent: A Dual-Tier Multi-Agent Framework for Privacy-Preserving Oncology Clinical Decision Support"
- BestBlogs URL: https://www.bestblogs.dev/en/article/da90d61f
- Original publisher URL: https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper
- Original link text: https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper

## Captured Page Metadata

- Browser title: "OncoAgent: A Dual-Tier Multi-Agent Framework for Privacy-Preserving Oncology Clinical Decision Support"
- Description: This technical paper introduces OncoAgent, a comprehensive open-source system designed to assist oncologists with clinical decision-making while preserving patient privacy. The system features a dual-tier architecture that routes simple queries to a 9B parameter model and complex cases to a 27B deep-reasoning model, both fine-tuned via QLoRA on 266,854 oncological cases. A key innovation is the integration of a four-stage Corrective RAG pipeline over 70+ NCCN and ESMO guidelines, combined with a three-layer reflexion safety validator that enforces a strict Zero-PHI policy. The entire stack runs on a single AMD Instinct MI300X instance using ROCm, eliminating cloud API dependencies. The paper reports significant performance achievements, including a 56x throughput acceleration for synthetic data generation (6,800 vs. 120 cases/hour) and full-dataset fine-tuning in approximately 50 minutes. The system architecture decomposes clinical reasoning across eight specialized LangGraph nodes, each with bounded, auditable functions, and includes a mandatory human-in-the-loop gate for high-complexity cases.
- Date: 05-09

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/da90d61f: https://www.bestblogs.dev/en/article/da90d61f
- https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper: https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper
- https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/oncoagent-thumbnail.png: https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/oncoagent-thumbnail.png
