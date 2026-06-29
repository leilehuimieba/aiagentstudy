# What to Do When Reflection Won't Fix Your AI Agent's Output

- BestBlogs URL: https://www.bestblogs.dev/article/4be45766
- Original publisher URL: https://www.freecodecamp.org/news/what-to-do-when-reflection-won-t-fix-your-ai-agent-s-output/
- Source: BestBlogs / freeCodeCamp
- Publish time: 2026-06-23 06:18:16
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 14706

---

Many AI Agent tutorials propose the same fix for bad output: reflection. Your agent generates garbage JSON? Just add another LLM call to "review" it. The second call critiques the first, the first tries again, and voilà — quality improves. I seems clean, elegant, and academic.

  Well, I've shipped agents to production at a large-scale web company — systems that generated deployment configs, API payloads, database queries. And I can tell you from painful experience: reflection doesn't work for structured output. Not reliably, and not when it actually matters.

  Here's what happens in practice. Your agent generates JSON. It's wrong about a third of the time, with missing fields, wrong types, and violated business rules. You add a reflection step because that's what the tutorials say. Now it fails one in six times.

  This sounds like progress until you realize that those remaining failures are invisible. The reflection step said "looks good!" and waved them through. You've built a system that's confidently wrong, and you won't know until something breaks in production at 2am on a Saturday.

  I spent weeks debugging this loop before I found a pattern that actually works. It's embarrassingly simple, it gets me near-perfect correctness, and it doesn't require any clever reflection prompts. Let me show you.

  What We'll Cover:

  
   
    Prerequisites

   

   
    The Problem with Reflection

   

   
    The Fix: Deterministic Validation

    
     What the Validator Actually Catches (and Why LLMs Can't)

    

   

   
    The Code

   

   
    Why This Works So Well

   

   
    When Three Attempts Isn't Enough

   

   
    When to Use This (and When Not To)

   

   
    The Takeaway

   

  

  Prerequisites

  To get the most out of this article, you should be familiar with:

  
   
    Basic Python (functions, dictionaries, type hints)

   

   
    How LLM APIs work at a high level (sending a prompt, getting a completion back)

   

   
    What a JSON Schema is (you don't need to be an expert — the code explains itself)

   

  

  The Problem with Reflection

  My take: asking an LLM to critique another LLM's structured output is like asking someone who's bad at math to grade someone else who's bad at math. They'd likely have the same or similar blind spots. The same weights that produced the error are now being asked to detect the error. Why would they suddenly get it right on the second pass?

  Think about what you're actually asking the model to do during a reflection step. "Hey, look at this JSON you just generated. Does timeout_seconds need to be less than interval_seconds? Are the replicas and CPU limits consistent with the business rules I listed in the system prompt?"

  The model reads it over, pattern-matches against what "looks right," and says "yep, all good." It missed that constraint during generation. It's going to miss it during review too, because it's the same model doing the same kind of reasoning.

  The failure mode that kept biting me wasn't wrong output — it was approved wrong output. False positives. The reflection step says "this configuration is correct" when it absolutely isn't.

  A system that says "I failed, try again" is annoying but safe. A system that says "this is correct" when it's broken? That's the config that sails through your pipeline and takes down your service. That's a 2am page.

  Reflection works beautifully for open-ended stuff — improving the tone of an email, catching logical gaps in an essay, suggesting a better structure for a blog post. But for structured output with hard constraints? You need something that doesn't guess. You need something deterministic.

  The Fix: Deterministic Validation

  The pattern for the fix is dead simple:

  Generate → Validate with a real validator → Feed exact errors back → Retry.

  That's it. No second LLM call to "critique." No chain-of-thought reasoning about correctness. Just a function that returns true or false with specific error strings — the same kind of validator you'd write for a form submission or an API request.

  Here's the key insight, and honestly it's the whole article in one sentence: LLMs are excellent at fixing errors when you tell them exactly what's wrong. They're terrible at finding their own errors.

  When you tell a model "your output had these specific errors: timeout_seconds must be < interval_seconds, replicas > 5 requires cpu_limit >= 1.0", it fixes both on the next try almost every time.

  The fixing is trivial. The finding is the hard part. And with this technique, you're outsourcing that to a deterministic function that's perfect at it, every time, in microseconds. There's no hallucinations and you don't get "confident but wrong" responses. Just pass or fail with an exact reason why.

  What the Validator Actually Catches (and Why LLMs Can't)

  A deterministic validator checks errors at three levels, and each one exploits something LLMs are fundamentally bad at:

  1. Structural errors

  Is the output even valid JSON? Are all required fields present? Are types correct (string vs. integer vs. array)? JSON Schema handles this in microseconds.

  An LLM "reviewing" the same output might glance at the structure and say "looks like valid JSON" without actually parsing it. The validator parses it. There's no "looks like". It either passes or it doesn't.

  2. Constraint violations

  Is replicas within the allowed range of 1–20? Does service_name match the regex ^[a-z][a-z0-9-]*$? Is memory_limit_mb at least 128?

  These are boundary checks. LLMs are notoriously bad at precise numerical comparisons and regex matching. They approximate, while a validator evaluates them exactly.

  3. Cross-field business rules

  This is where reflection fails hardest. Rules like "if replicas > 5, then cpu_limit must be >= 1.0" or "timeout_seconds must be strictly less than interval_seconds" require holding two values in mind and applying a specific logical relationship.

  These rules don't exist in the training data as patterns the model can pattern-match against. They're your rules, specific to your system. The LLM has no reason to "know" them beyond what's in the prompt, and prompts get lost in long contexts.

  Here's why the validator wins at all three: it doesn't reason — it executes. There's no interpretation, attention window, or chance of skipping a constraint because something earlier in the context was more salient. Every rule runs every time, in order, deterministically.

  The LLM's job, by contrast, is to generate: to produce something that looks right based on patterns. That's a fundamentally different skill than verifying that every constraint in a spec is satisfied. You wouldn't ask a novelist to proofread a tax return. Don't ask a generator to validate its own output.

  The Code

  Here's the full pattern in LangGraph: the validator, the nodes, and the graph with conditional routing. The complete runnable example — schema, validator, the loop, and tests — is on GitHub: github.com/manishramavat/langgraph-deterministic-validation

  First, the schema and the validator — this is your real source of truth:

  from jsonschema import validate, ValidationError

DEPLOYMENT_CONFIG_SCHEMA = {
    "type": "object",
    "required": ["service_name", "replicas", "resources", "health_check"],
    "properties": {
        "service_name": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
        "replicas": {"type": "integer", "minimum": 1, "maximum": 20},
        "resources": {
            "type": "object",
            "required": ["cpu_limit", "memory_limit_mb"],
            "properties": {
                "cpu_limit": {"type": "number", "minimum": 0.1, "maximum": 8.0},
                "memory_limit_mb": {"type": "integer", "minimum": 128, "maximum": 16384},
            },
        },
        "health_check": {
            "type": "object",
            "required": ["path", "timeout_seconds", "interval_seconds"],
            "properties": {
                "path": {"type": "string", "pattern": "^/"},
                "timeout_seconds": {"type": "integer", "minimum": 1},
                "interval_seconds": {"type": "integer", "minimum": 5},
            },
        },
    },
}

# The validator: your REAL source of truth. This is the hard part.
def validate_config(config: dict) -> tuple[bool, list[str]]:
    """Schema validation + business rules. This IS your spec."""
    errors = []
    try:
        validate(instance=config, schema=DEPLOYMENT_CONFIG_SCHEMA)
    except ValidationError as e:
        errors.append(f"Schema: {e.message} (at {list(e.path)})")
        return False, errors  # bail early — no point checking rules on broken structure

    # Cross-field rules that JSON Schema can't express
    if config["replicas"] > 5 and config["resources"]["cpu_limit"] < 1.0:
        errors.append(f"replicas={config['replicas']} requires cpu_limit >= 1.0")
    if config["health_check"]["timeout_seconds"] >= config["health_check"]["interval_seconds"]:
        errors.append("timeout_seconds must be < interval_seconds")

    return len(errors) == 0, errors

  Now the LangGraph loop that wires generation to that validator:

  import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT = ("You generate deployment configs as valid JSON. "
                 "Required fields: service_name, replicas, resources, health_check. "
                 "Follow ALL constraints exactly. Return ONLY the JSON object.")

class State(TypedDict):
    request: str
    config: dict | None
    errors: list[str]
    attempts: int

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

def generate_node(state: State) -> dict:
    """Generate config, injecting exact errors on retries."""
    content = f"Generate config for: {state['request']}"
    if state["errors"]:  # the magic — exact errors fed back, not vague critique
        content += "\n\nYour previous attempt had these errors:\n"
        content += "\n".join(f"- {e}" for e in state["errors"])
        content += "\nFix ALL of them."
    resp = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=content)])
    try:
        config = json.loads(resp.content.strip()) if resp.content else {}
    except json.JSONDecodeError:
        config = None  # validator will catch this
    return {"config": config, "attempts": state["attempts"] + 1}

def validate_node(state: State) -> dict:
    """Run deterministic validation. No LLM involved."""
    if not state["config"]:
        return {"errors": ["Output was not valid JSON"]}
    _, errors = validate_config(state["config"])
    return {"errors": errors}

def route(state: State) -> str:
    """Done if valid OR exhausted retries."""
    if not state["errors"]:
        return "done"
    return "retry" if state["attempts"] < 3 else "done"

graph = StateGraph(State)
graph.add_node("generate", generate_node)
graph.add_node("validate", validate_node)
graph.set_entry_point("generate")
graph.add_edge("generate", "validate")
graph.add_conditional_edges("validate", route, {"retry": "generate", "done": END})
app = graph.compile()

  The graph compiles to a loop with a deterministic exit condition: either the output passes validation, or you've hit 3 attempts and it's time to escalate. No orchestration framework magic. The validator does the hard work.

  Why This Works So Well

  You're separating two fundamentally different jobs: error detection and error correction. And you're giving each job to the tool that's actually good at it.

  Validators are perfect at detection. We've had JSON Schema validators, SQL parsers, and type checkers for decades. They're solved problems. They run in microseconds. They never hallucinate a passing result, and they never have an off day. They also never get confused by a tricky edge case they saw during training.

  That second task is exactly where LLMs drop the ball: systematically checking every constraint isn't what next-token prediction optimizes for.

  Together, they're near-perfect. The validator catches everything (because it's deterministic). The LLM fixes everything the validator catches (because the feedback is unambiguous). Separately, they're both mediocre at the combined task. The validator can't generate configs. The LLM can't reliably verify them. But as a team? You get something that's better than either alone, and dramatically better than reflection for this type of error.

  When Three Attempts Isn't Enough

  If the model doesn't fix it within three attempts, a fourth try almost never helps. The residual errors are usually ambiguity in your spec, not a fixable generation problem. So decide up front what "give up" means in your system:

  
   
    Log the failure with the request and the final error list — these are your best signal for where the spec itself is ambiguous.

   

   
    Reject with a clear error (for example, a 422 with the validation messages) rather than shipping a broken config downstream.

   

   
    Escalate to a human for high-stakes paths.

   

  

  Whatever you do, don't burn tokens hoping that attempt seven will magically work.

  When to Use This (and When Not To)

  Here's the simple test: can you write a function that returns true or false for your agent's output?

  If yes, wire that function into a generate → validate → retry loop. Your validator already exists, you just haven't put it in the agent's feedback path yet:

  
   
    JSON output? You already have a schema. Run jsonschema.validate().

   

   
    SQL output? Run EXPLAIN — the database tells you if it parses.

   

   
    Code output? Compile it. Run the tests. Those are your validators.

   

   
    Terraform? terraform validate exists for exactly this reason.

   

  

  If no – if "correct" is subjective (tone of an email, quality of a summary, persuasiveness of copy) — then you're back to reflection or human review. That's fine. Reflection works for subjective quality. Reflection just doesn't work when there's a right answer and a wrong answer.

  The Takeaway

  Build the validator first and the agent second. Your validator IS your spec. It defines "correct" in machine-checkable terms. Once you have that, your agent becomes a simple loop with a deterministic exit condition, and you can reason about its reliability with real confidence instead of hoping your prompt is clever enough.

  Stop asking LLMs to verify themselves for deterministic output. Give them a mirror that actually reflects reality.

  All opinions are my own and don't represent my employer.
