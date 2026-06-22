# Arm Open-Sources Metis， an AI Security Framework Outperforming Traditional SAST Tools

- BestBlogs URL: https://www.bestblogs.dev/article/5877d882
- Original publisher URL: https://www.infoq.com/news/2026/05/arm-metis-agentic-security/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-05-31 03:00:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 3563

---

Arm has open-sourced Metis, an agentic AI security framework designed to autonomously uncover complex software vulnerabilities. Unlike traditional pattern-based tools, Metis applies semantic reasoning to analyze cross-component dependencies and provides clear, natural language explanations for its findings.

   According to Arm, the growing complexity of modern codebases makes it challenging for traditional static application security testing (SAST) tools to detect vulnerabilities across multiple function boundaries or libraries without generating high false-positive rates. Instead of relying on fixed rules and pattern matching, Metis employs "agentic" AI to identify security issues across large-scale codebases:

   
    By combining advanced analysis techniques with AI-enabled workflows, Metis identifies more sophisticated security vulnerabilities that are difficult to detect using existing approaches, as well as identifying them earlier in the process.

   

   Metis uses retrieval-augmented generation (RAG) to enhance a base large language model with project-specific context derived from source code, build files, and documentation, giving it a clearer picture of the system design and intended behavior. With this approach, Arm says, Metis can analyze entire repositories, individual files, pull requests, or recent code changes delivering up to 10x higher true positive rates and approximately 50% fewer false positives compared to leading static analysis tools.

   
    False positives consume valuable engineering time and can reduce trust in automated tooling. By reducing false positives, Metis helps engineering teams focus on the issues that matter most, accelerating remediation and reducing wasted effort during validation and review.

   

   Metis can also operate alongside external SAST tools and validate their findings to help reduce the number of false positives. In Arm's internal benchmarks using GPT-5.5-Cyber as the base model, Metis achieved 98% accuracy in identifying vulnerabilities, compares to just 6% for traditional SAST, according to the company.

   Beyond simply flagging vulnerabilities, Metis can also explain its findings with clear, actionable summaries, giving developers and engineers the context they need to understand and address issues quickly.

   Metis can be used with any OpenAI-compatible LLM and supports a wide range of programming languages, including C, C++, Python, Go, TypeScript, Rust, and others. Its plugin-based architecture also allows developers to easily extend support for additional languages, models, and custom prompts.

   Metis supports both Ollama and vLLM deployments, which are configured in metis.yaml. For example, to use Llama 3.1 with Ollama on a local machine:

   llm_provider:
  name: "ollama"
  base_url: "http://localhost:11434/v1"
  model: "llama3.1:8b"
  code_embedding_model: "nomic-embed-text:v1.5"
  docs_embedding_model: "nomic-embed-text:v1.5"

   For vLLM deployments, Arm recommends using LiteLLM as a frontend for the LLM provider and configuring Metis to route requests through it. A typical setup includes one vLLM instance serving a chat model, another serving the embedding model, and a LiteLLM router to coordinate traffic between them.

   While the current release focuses on vulnerabilities in software system, Arm is working to extend Metis to support hardware vulnerability verification.

   Arm says that Metis is currently monitoring over 130 software projects within the company. The code is available under an Apache 2.0 license on GitHub.
