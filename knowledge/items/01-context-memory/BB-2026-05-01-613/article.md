# How to Build Memory into AI Agents

- BestBlogs URL: https://www.bestblogs.dev/article/35c6d909
- Original publisher URL: https://www.langchain.com/blog/how-to-give-your-agent-memory
- Source: BestBlogs / LangChain Blog
- Publish time: 2026-06-24 08:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 7648

---

Building a loop so that your agent can learn from previous actions allows you to create delightful agentic experiences that learn with the user. This is often called memory. Memory can be the difference between your users having to constantly repeat corrections instead of the agent remembering how to do something correctly after the first time it is told.

   The implementations are still evolving, but the abstractions are simple. In order to implement memory, you’ll want to run some process in the background that looks for places the agent made a mistake or could have learned new information, and extract/generalize that information into a data structure. There are a lot of details yet to be figured out there. This post walks through a concrete implementation of this process. It will use:

   
    LangSmith Observability as a trace store

    LangSmith Engine as a process that analyzes traces

    LangSmith Context Hub as a memory store

   

   
    
     
    

   
   What is memory?

   Memory is durable context that an agent can retrieve across runs to guide its behavior. It may include facts, preferences, past interactions, instructions, skills, examples, and learned patterns.

   A trace, transcript, or log is useful evidence of what happened. It becomes memory only when the relevant lesson is converted into context the agent can retrieve on a later run and use to change its behavior.

   To decide what belongs where, it helps to separate memory into two scopes: short-term (or ‘working’) memory and long-term memory.

   Short-term memory is the context available while the agent is doing the task in front of it: the current thread, recent messages, tool results, retrieved documents, intermediate reasoning artifacts, and temporary files or state the agent needs to finish the current job.

   Long-term memory is context that persists beyond the current run: facts, preferences, examples, workflows, policies, instructions, and skills that should be available later to shape the agent’s behavior over time.

   The relationship between the two is a read-and-write cycle. During a run, the agent benefits from long-term memory once the harness makes the relevant context available. That might happen through prompt assembly, retrieval from a store, tool access, files, runtime state, or some other context-loading mechanism. As the run unfolds, working memory changes. After the run, the trace gives us evidence of what happened. Most of that evidence should remain history, but some of it may contain useful signal: a preference the agent should remember, an instruction that needs to be clarified, a tool-use pattern that should become a rule, or a skill that should be updated.

   A useful way to think about long-term memory is to separate it into semantic, episodic, and procedural memory, a taxonomy borrowed from cognitive science and commonly mapped onto language-agent systems.

   
    Semantic memory is what the agent knows: facts, preferences, and general knowledge.

    Episodic memory is what the agent has experienced: past interactions, examples, actions, and outcomes.

    Procedural memory is how the agent should behave: instructions, workflows, policies, skills, and tool-use rules.

   

   
    
     
    

   
   Many of the most visible improvements in agent behavior come from procedural memory. When an agent repeatedly formats answers incorrectly, calls tools in the wrong order, delegates to the wrong subagent, or ignores a tone rule, the fix is often procedural: make the rule clearer, change the steps the agent follows, or move the behavior into a more specific skill that owns that task.

   The high-level memory process

   At a high level, a well-functioning agent memory loop has three parts: capture traces, analyze traces, and update memory.

   1. Capture traces

   Traces are the evidence layer. A well-instrumented trace records the path an agent took through a task: the user input, model calls, tool inputs and outputs, retrieved documents, routing decisions, latency, errors, and often user feedback.

   This is important because, unlike traditional deterministic software, you often do not know how an agent behaved until you inspect its trajectory. Unexpected behavior might be caused by a weak prompt, a missing tool, a confusing tool schema, poor retrieval, stale context, an overly broad instruction, or a routing decision that quietly sent the work to the wrong place. Inspecting a trace allows you to isolate these causes.

   2. Analyze traces

   Once traces are captured, the next step is to find useful signal. Some signal comes from explicit feedback or eval failures. Some comes from recurring patterns: the same bad output, the same invalid tool call, the same routing mistake, or the same ignored instruction.

   The tricky part is diagnosis. The same symptom can point to different fixes. If the agent ignores a tone rule, the rule might be too vague, in the wrong place, missing from the relevant skill, or contradicted by another instruction.

   3. Update memory

   Once the signal is understood, the system should decide whether future context needs to change. That might mean fixing an issue, like clarifying an instruction or changing a routing rule, but it can also mean remembering something useful, like a user preference, a successful example, or a pattern the agent should reuse later.

   
    
     
    

   
   How to do this with LangSmith

   You can do this whole agent memory loop with LangSmith:

   
    Capture traces: LangSmith Observability

    Analyze traces: LangSmith Engine

    Update Memory: LangSmith Context Hub

   

   In LangSmith, tracing gives you the capture step. Tracing projects give you a rich store of the trajectories that your agent took so that you can inspect and understand why the agent behaved the way it did.

   LangSmith Engine is the background process that turns those traces into improvement signal. Instead of requiring you to inspect every run manually, Engine analyzes traces for recurring issues, diagnoses likely root causes, and surfaces concrete changes that could improve future behavior - it might add a rule, move an instruction closer to the relevant workflow, create a new example, update a skill or change a routing policy.

   Context Hub is where those changes can become durable agent context. It gives you a versioned place to manage the instructions, tools, and skills your agents use, so memory is not just an ad hoc prompt edit sitting in application code.

   Once the context is updated, future runs load it back into the agent. That closes the loop - traces are captured, Engine extracts improvement signal, Context Hub stores the memory, and the next run starts with updated context.

   
    
     
    

   
   Design principles for useful memory (from experience)

   A few principles to help make this loop reliable:

   
    Not everything should be a memory update. Most trace data should remain history. Some should become dataset examples, evals, code changes, or tool-schema fixes. Only a small subset should become durable context.

    Make sure future runs actually read the update! If the runtime caches prompts, tools, or skills, memory commits need a refresh path. Otherwise the system may store the right update while continuing to run with stale context.

    Protect important behavior with evals. If a memory update matters enough to shape future behavior, it is usually worth having a way to detect when that behavior regresses.

   

   Acknowledgements

   Thanks to Sydney Runkle and Harrison Chase for their thoughtful review and feedback.
