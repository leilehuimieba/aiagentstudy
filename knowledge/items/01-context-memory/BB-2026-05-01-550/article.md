# How Box AI built enterprise content agents with Deep Agents

- BestBlogs URL: https://www.bestblogs.dev/article/06adaad3
- Original publisher URL: https://www.langchain.com/blog/building-box-ai-how-an-enterprise-content-platform-went-ai-native-with-deep-agents
- Source: BestBlogs / LangChain Blog
- Publish time: 2026-06-12 08:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 7366

---

‍Box is the intelligent content management platform trusted by 100,000+ enterprises to store, secure, and govern their unstructured data. The Box Agent, part of Box AI, is built on Deep Agents to search across an enterprise's content library, synthesize findings across thousands of documents, and produce reports and analysis, all while respecting Box's existing security and permissions model. 

   From Single-File Q&A to Enterprise-Scale Analysis

   The first iteration of the Box Agent allowed users to ask questions within a single document. From there, the team introduced Knowledge Hubs, a RAG-based layer that let users query across a defined knowledge source. 

   "When we started with agents, we wanted to solve the search problem," explained Sesh Jalagam, Principal AI Architect at Box. "Enterprise search is challenging, because you have duplicate information, outdated information, things that seemingly look the same but every enterprise has its own nomenclature." 

   While valuable capabilities, users began to ask increasingly complex questions across different domains. A bioscience company's researchers might have asked Box AI to synthesize a body of existing research before starting a new study. A legal team might have asked to pull all contracts exceeding a certain value from the past decade and assess them against a risk rubric. For a richer AI-native experience, Box required an agentic architecture that went beyond standard Q&A.

   Choosing Deep Agents for Control, Model Flexibility, and Speed

   Box evaluated multiple frameworks when it set out to build its agent platform. Two requirements shaped the decision.

   
    Complete model agnosticism. Box offers its customers a choice of LLM providers, from OpenAI and Anthropic to Google and others, and that flexibility had to be preserved at the platform level. 

    Speed of iteration. To launch and improve Box Agent for 100,000+ enterprise customers, the Box team needed to focus engineering time on the enterprise-specific problems rather than rebuilding core agent infrastructure. 

   

   Deep Agents satisfied both. The model abstraction layer handled provider-agnostic routing, and the open agent harness unlocked 3x speed of iteration. "We wanted full control of all the pieces, while building on a forward-looking framework," Jalagam said. 

   The Deep Agent Architecture: A Parent Agent That Spawns Its Own Children

   The Box Agent’s architecture uses a parent/child model where both the parent and all children are Deep Agents. The parent (called the Global Agent) receives a request, classifies intent, and decides whether to handle it directly or spawn child agents to distribute the work. Child agents are expressed as tools to the parent, keeping the invocation surface uniform whether the parent is running a keyword search or delegating to a freshly spawned sub-agent.

   This design was a deliberate evolution from an earlier architecture that had hardcoded, specialized sub-agents: a dedicated search agent, a QA agent, and a compose agent—which created unnecessary latency. "If the question was very simple, or the search was very simple, the parent node can just do it," said Shubhro Roy, AI Engineering Leader at Box. "It doesn't even need to come up with a plan."

   For complex tasks, the behavior looks entirely different. If asked, for example, to pull all contracts from the last 10 years with values exceeding a threshold and evaluate them against a risk rubric, the Global Agent produces a plan, then fans out. One child searches for the relevant documents, another retrieves the rubric in parallel, and a third synthesizes and analyzes the results once the first two complete. All 3 agents (or any number of agents, depending on what the task demands) run with isolated context windows, reporting back through the middleware layer.

   Because child agents are spawned dynamically rather than predefined, the system handles tasks that Box's product teams haven't explicitly designed for. The Global Agent decides at runtime what children to create and what tools to give them.

   Both parent and child have access to the same full tool registry, covering BM25 keyword search, vector search, structured Q&A over spreadsheets, file operations, and more. Rather than trying to dynamically select a subset of tools per request, Box found that as use cases expanded, the models were better at deciding which tools to use than any static routing logic. 

   
    
     
    

   
   Middleware: Citations, Caching, and Context Management

   Box uses Deep Agents middleware that intercepts model and tool calls. Middleware lets you customize the agent loop with guardrails, approvals, dynamic context, and other application-specific behavior. Three of its functions for the Box Agent include:

   Citation generation. For complex, multi-document answers, citations run as a parallel process during response streaming. By the time the streamed answer completes, the citations are ready to attach. Embedding-based matching handles source attribution, with built-in logic to ensure citations are distributed appropriately across multiple sources. "The advantage of doing it as middleware is that the streaming of the answer and the citation generation happen in parallel, so you never interrupt the user," explained Roy.

   Prompt caching. Middleware injects caching on multi-turn conversations, reducing both cost and latency as conversation history accumulates.

   Context management. When conversation history exceeds 170,000 tokens, middleware summarizes it automatically, preventing context overflow without requiring changes to agent logic.

   Middleware also functions as the communication channel between parent and child agents. A child that completes a search writes its results through middleware; the parent and other children can read and act on those results. This is how intermediate artifacts flow between agents within a single execution.

   Speed of Iteration: From Months to Weeks

   Building on Deep Agents meaningfully accelerated Box's engineering velocity. "Previously we built Box AI completely from the ground up, which meant more time to get something out in the market,” emphasized Jalagam. With the current stack, the team can ship a new agent in a couple of weeks.

   The acceleration also shows up within the agentic platform itself. The first agent architecture, with hardcoded specialized sub-agents, took roughly 3 months to develop and ship. The recursive parent/child architecture that followed shipped 4x faster. 

   Expanding Box Agent’s Institutional Knowledge

   The Box Agent’s capabilities today—cross-enterprise search, multi-document synthesis, structured report generation—are the foundation for a future agent with the institutional knowledge of a tenured employee. "Imagine an employee who has 10 years' worth of understanding of all the pieces going on," Jalagam said. The roadmap includes richer memory and knowledge composition within agents, the ability to run offline in the background collecting and surfacing information, and deeper communication with both internal teams and external systems.

   Read more about Box’s Agent Architecture: https://blog.box.com/how-box-built-its-ai-agent-langgraph 

   Building agents on top of enterprise content? Learn more about Deep Agents.

   ‍
