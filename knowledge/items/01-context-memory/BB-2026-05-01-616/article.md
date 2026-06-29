# Vector RAG Isn’t Enough — I Built a Context Graph Layer for Multi-Agent Memory

- BestBlogs URL: https://www.bestblogs.dev/article/0b2a6406
- Original publisher URL: https://towardsdatascience.com/vector-rag-isnt-enough-i-built-a-context-graph-layer-for-multi-agent-memory/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-26 02:37:56
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 26764

---

TL;DR

  
   I wasn’t trying to build a new memory architecture. I was trying to understand why one agent kept forgetting decisions made by another. The benchmark came later.

   Multi-agent systems lose cross-agent decisions because flat transcripts and vector search both have a structural blind spot — not just a noise problem.

   A context graph stores facts as entities and relationships instead of text chunks, so it can answer questions that need two facts combined.

   This is not a concept. Three memory architectures, five scripted scenarios, 18 graded queries, fully deterministic, zero LLM calls.

   Context graph: 88.9% accuracy at 26.9 tokens/query. Raw history dump: 61.1% accuracy at 490.9 tokens/query. Vector-only RAG: 50.0% accuracy at 75.9 tokens/query.

   I found two real bugs building this — stale-fact retrieval and an entity-matching gap. Both are in the article.

  

  The Problem That Made Me Build This

  I built a three-agent pipeline that worked great for short tasks. But the moment the conversation dragged on and an agent needed to recall a past decision, the whole thing fell apart.

  Here is exactly how it broke: Agent_Planner would decide the project should use PostgreSQL. Then, twenty turns of “sounds good” and “I’ll get to it” would pass. Eventually, Agent_Reviewer would pipe up and ask what storage technology we were using. Even with the entire raw transcript sitting right there in the context window, the agent couldn’t answer reliably.

  I was running this pipeline locally as a side project for EmiTechLogic just to see how far I could push multi-agent coordination before it hit a wall. Turns out, it didn’t take very long.

  Initially, I assumed this was just a model limitation. It isn’t. It is a memory architecture problem that usually triggers one of two massive headaches depending on how you try to fix it.

  The Alternative Fix: Vector Search and the Relational Trap

  If you switch to vector search, you fix the noise problem but immediately create a different one. A vector store retrieves chunks that look similar to your query; it doesn’t retrieve relationships between facts.

  If a key decision lives in one chunk and a critical dependency note about that decision lives in another, a similarity search has no way to combine them—no matter how good your embedding model is.

  Both approaches hit different structural ceilings. Instead of guessing which compromise was “good enough,” I decided to measure them both.

  What This Problem Actually Is

  To be clear about what this article is not: this isn’t a token-compression problem, and it’s not a staleness problem. It’s a structural retrieval problem. Some questions can only be answered by combining two separately-stated facts, and neither a growing context window nor a vector index has a mechanism to do that. That is a completely different failure mode than the ones I’ve written about before, and it needed a different benchmark.

  The Test Setup

  To test this, I built five deterministic scenarios containing 18 graded queries and ran all three memory architectures against the exact same conversations.

  All the results below come from real runs of that benchmark using a localized setup:

  
   Environment: Python 3.12, CPU-only (no GPU needed)

   API Calls: Zero

   Consistency: Reproduced identically across two separate machines

  

  
   Code Repo: You can find the complete implementation and run the tests yourself here: https://github.com/Emmimal/context-graph-benchmark/

  

  What “Context Graph” Means Here

  A flat memory store (whether it is a raw chat transcript or a vector index) treats every single turn as an independent unit of text. To retrieve something, you just find the unit that best matches your query.

  A context graph changes the underlying structure entirely. It treats memory as distinct entities with typed relationships connecting them:

  
   AuthModule —–> DEPENDS_ON —–> RateLimiter

   Agent_Implementer —–> ASSIGNED_TO —–> AuthModule

  

  Retrieval in this model means traversing these relationships instead of just matching keywords or semantic vectors.

  That structural difference only matters for one specific class of questions: anything that requires you to combine two separately-stated facts.

  Consider a question like: “Which team owns the component that depends on the service that X chose?”

  There is no single answer chunk sitting anywhere in the raw conversation history. The answer does not exist as a block of text. It only exists as a path through multiple facts. A flat store cannot construct that path on the fly. A graph walks right through it.

  Who This Is For

  This approach is worth building if you run multi-agent pipelines where one agent’s decision must be correctly retrieved by a different agent many turns later. It is built for systems where questions routinely require combining two or more separately-stated facts, or any long-running agent conversation where the token cost of re-sending history is becoming a real line item.

  You should skip it for single-agent, single-turn tasks because there is no cross-agent state to lose. Skip it if your queries are always single-fact lookups with no joins. Vector RAG gets you most of the accuracy there at a fraction of the engineering cost. Finally, skip it if your team has no tolerance for an extra moving part. A graph needs an extraction step (which is rule-based in this benchmark, but requires an LLM call in production) that a flat store avoids.

  If your multi-agent system finishes its work in a single exchange, plain context passing works fine. This problem shows up specifically when conversations run long and decisions need to survive past the turn they were made in.

  The Three Architectures

  
   
    
     
      Architecture
      What it stores
      What it costs
      What it’s good at
     

    
    
     
      Raw History Dump
      Every turn, verbatim
      Grows with conversation length, resent every query
      Nothing it doesn’t get for free from having everything
     

     
      Vector-Only RAG
      Every turn, embedded (TF-IDF)
      Flat per query, loses relational structure
      Finding semantically similar single facts
     

     
      Context Graph
      Structured triples in a NetworkX graph
      Flat and small per query
      Questions that need two facts combined
     

    
   

  
  Why There Are No LLM Calls in the Benchmark

  I purposely left out LLM calls from every stage of this benchmark: no LLMs for extraction, none for query answering, and none for grading.

  If a real LLM handled the extraction, the benchmark would measure LLM variance as much as actual architectural differences. Using deterministic, rule-based stand-ins ensures that every single run produces the exact same numbers.

  I ran this test independently on two different machines while writing this piece. The output matched byte-for-byte, maintaining accuracy to four decimal places and token counts down to the exact integer.

  Building a Benchmark That Doesn’t Secretly Favor the Graph

  The easiest way to make a graph win a benchmark is to only ask it clean, single-fact questions. That proves nothing. To keep the testing fair, every scenario follows four strict rules:

  
   Distractors outnumber facts: Every scenario contains far more “sounds good,” “I’ll check that,” and “no blockers on my end” turns than actual concrete decisions.

   Queries span physical distance: Some queries are asked right after a fact is stated (direct), some are asked many turns later (distant), and some require stitching two separate facts together (join). An example of a join query is: “Which component does the module owned by Agent_Implementer depend on?”

   Some queries are easy on purpose: Direct, single-fact lookups are included specifically to give the flat architectures a fair shot.

   Grading is completely deterministic: The benchmark uses substring matching against a hand-written ground truth rather than relying on an LLM judge.

  

  @dataclass
class Turn:
    turn_id: int
    turn_type: TurnType          # FACT, DISTRACTOR, or QUERY
    speaker: str
    text: str
    subject: str | None = None    # structured triple, FACT turns only
    predicate: str | None = None
    object: str | None = None
    fact_id: str | None = None
    query_type: str | None = None # "direct", "distant", "join"
    required_fact_ids: tuple = ()
    ground_truth: str | None = None

  The benchmark covers five distinct scenarios across different domains: software planning, a research pipeline, incident response, customer support escalation, and a data pipeline.

  Across these five setups, there are 18 total queries split into three specific categories:

  
   6 Direct queries: Lookups asked immediately after the fact is stated.

   7 Distant queries: Lookups asked many turns after the fact is stated.

   5 Join queries: Questions that require combining two separately-stated facts to get the answer.

  

  Architecture 1: Raw History Dump

  Every single turn gets appended to a flat transcript, and the entire transcript gets resent on every query. This is exactly what you get by default when you do not design a memory system on purpose.

  I built this to serve as a genuinely fair baseline. It gets the full, perfect transcript with nothing hidden from it. The answer extraction uses keyword overlap with light stemming, searched from the most recent turn backward. This setup closely mirrors how a context-stuffed prompt tends to weight recency anyway.

  class RawHistoryDump:
    def ingest(self, turn: Turn) -> None:
        self.transcript.append(f"{turn.speaker}: {turn.text}")

    def answer_query(self, query_turn: Turn) -> tuple[str, int]:
        prompt = self._build_prompt(query_turn)   # the ENTIRE transcript
        tokens = count_tokens(prompt)
        answer = self._extract_answer(query_turn)
        return answer, tokens

  The cost model matches exactly what you see in production: every query resends the entire growing conversation history.

  Architecture 2: Vector-Only RAG

  Every turn, fact and distractor alike, gets embedded and stored as a chunk. A real vector store does not know in advance which turns will matter later. On a query, the top-K most similar chunks are retrieved.

  I used TF-IDF instead of a neural embedding API for the same reason I avoided LLM calls elsewhere. TfidfVectorizer has no random state, making it deterministic by construction. It is also not a toy stand-in. TF-IDF is a real sparse-retrieval method used in production RAG, often paired with dense embeddings in a hybrid setup.

  class VectorOnlyRAG:
    def _retrieve(self, query_text: str) -> list[str]:
        if not self.chunks:
            return []
        corpus = self.chunks + [query_text]
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(corpus)
        sims = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
        top_idx = sims.argsort()[::-1][:self.top_k]
        return [self.chunks[i] for i in top_idx if sims[i] > 0]

  (The actual implementation wraps fit_transform in a try/except block to handle the rare edge case of a query containing only stop words. I skipped that here for space, but it is in the repository.)

  The structural ceiling remains clear: a join query requires combining two distinct facts. When those facts are stated across two different turns, no single chunk contains both pieces of information. No embedding model can fix that limitation on its own.

  Architecture 3: The Context Graph

  Facts get written as (subject, predicate, object) triples into a NetworkX directed multigraph. Distractor turns never get written at all. This is the one place this architecture gets an advantage the other two do not: filtering data before it ever hits storage.

  In production, that filtering step is an LLM call performing entity extraction. In this benchmark, it is deterministic because the scenario setup already tags which turns are facts. I am isolating exactly what the storage and retrieval architecture does on its own, with extraction held constant as a stated assumption. I am not claiming to have solved extraction for free.

  class ContextGraph:
    def ingest(self, turn: Turn) -> None:
        if turn.subject is None:
            return  # distractors carry no structured triple; not stored
        self.graph.add_node(turn.subject)
        self.graph.add_node(turn.object)
        self.graph.add_edge(turn.subject, turn.object,
                             predicate=turn.predicate, fact_id=turn.fact_id)

  The join-query traversal is the part doing the real work. It performs a two-hop walk across the graph nodes instead of searching for a single text chunk that happens to contain both facts.

  def _answer_join(self, query_turn, mentioned):
    for entity in mentioned:
        out_edges, in_edges = self._edges_touching(entity)
        intermediates = [v for _, v, _ in out_edges] + [u for u, _, _ in in_edges]
        for intermediate in intermediates:
            further_out, _ = self._edges_touching(intermediate)
            for _, target, data in further_out:
                if target != entity:
                    # score candidates by predicate relevance
                    ...

  Here’s the difference in search space across all three:

  
   
   Raw history and vector search retrieve text. A context graph retrieves relationships. By traversing connected entities, the system can answer multi-hop questions that similarity search alone may miss.
  
  What Actually Happened When I First Ran It

  The first full run, with all three architectures built, scored the context graph at 0% accuracy.

  I’m including this because it’s the part most “I built X” posts skip. I could have rewritten the scenarios to be friendlier instead of debugging the code. That would have given me a fake result. I traced it instead.

  Bug 1: Entity Vocabulary Mismatch

  Graph nodes were named things like Project_Alpha or AuthModule. The queries, written the way an agent would actually phrase them, said “this project” or “the authentication module.” A literal substring match between the query text and the node name found absolutely nothing.

  This is the exact same vocabulary-mismatch problem people criticize vector search for. It just hits the graph at write time instead of query time.

  The fix was a small alias table standing in for a real entity-linking step, which would usually be handled by an LLM call in production. Using a graph does not get you out of this problem. It simply moves the problem from query-time retrieval to write-time resolution. That is an ongoing engineering cost, not a one-time fix.

  Bug 2: Returning Stale Facts With Full Confidence

  This is the exact issue I would flag first to anyone shipping this pattern in a production environment.

  One scenario features a support ticket that starts at a priority level of “high” and gets reclassified to “critical” mid-conversation. When querying “what is the current priority?”, the graph returned “high”—the stale value, with the exact same confidence it would have given the current one.

  The cause was simple: my first ingest() implementation just added every new edge and never removed the old one. The graph held two HAS_PRIORITY edges originating from the same node. Whichever edge happened to be visited first in the iteration order won the lookup, completely ignoring which fact was actually current.

  # the bug
Ticket_4471 --HAS_PRIORITY--> "high"      # stated first
Ticket_4471 --HAS_PRIORITY--> "critical"  # stated later, supersedes the first
# both edges exist at once; nothing tells the graph which one is "now"

  A flat chat dump searched with recency bias tends to surface the newer mention just by scanning backward. In contrast, a graph with no time model hands back either fact with equal structural confidence because graphs do not natively know a relationship has been replaced unless you explicitly tell them.

  That failure mode is worse than a fuzzy search returning a stale chunk. The graph looks completely authoritative even when it is completely wrong.

  The fix: when a new fact restates an existing (subject, predicate) pair, the old edge gets dropped before the new one is written.

  def ingest(self, turn: Turn) -> None:
    if turn.subject is None:
        return
    self.graph.add_node(turn.subject)
    self.graph.add_node(turn.object)

    stale_edges = [
        (u, v, k) for u, v, k, data in self.graph.edges(keys=True, data=True)
        if u == turn.subject and data.get("predicate") == turn.predicate
    ]
    for u, v, k in stale_edges:
        self.graph.remove_edge(u, v, key=k)

    self.graph.add_edge(turn.subject, turn.object,
                         predicate=turn.predicate, fact_id=turn.fact_id)

  If you are shipping anything like this, handling fact supersession is not optional. It is the exact line between building a reliable memory layer and building a major liability.

  Final Benchmark Results

  Five scenarios, 18 queries, fully deterministic, reproduced identically on two separate machines.

  
   
    
     
      Architecture
      Accuracy
      Avg tokens/query
      Direct
      Distant
      Join
     

    
    
     
      Raw History Dump
      61.1%
      490.9
      66.7%
      71.4%
      40.0%
     

     
      Vector-Only RAG
      50.0%
      75.9
      66.7%
      57.1%
      20.0%
     

     
      Context Graph
      88.9%
      26.9
      100%
      85.7%
      80.0%
     

    
   

  
  The context graph wins on accuracy and uses about 18x fewer tokens per query than the raw dump. That is not a tradeoff—it is a win on both axes.

  Vector RAG’s token cost is also low and isn’t the graph’s main differentiator. Both architectures retrieve a bounded number of items, so both stay cheap regardless of conversation length. What separates the graph from vector RAG is the join column: 80% versus 20%. That gap is the structural argument for a graph—vector similarity has no native way to combine two separately-stated facts.

  The raw dump’s accuracy came in higher than I expected at 61.1%, and it earns that. A perfect, lossless transcript with decent keyword matching does fine on single-fact lookups. It falls apart specifically on joins (40%) for the same structural reason as vector RAG, just with a much bigger token bill.

  One limitation was left in on purpose: two queries in the data-pipeline scenario fail because they refer to an entity by description rather than name—”the dataset that currently has an anomaly” instead of naming Upstream_Orders directly. Fixing that requires real semantic understanding of a descriptive clause, not simple alias matching. Extending the alias table to cover my own test queries would mean overfitting the benchmark rather than representing a real limitation, so it stays broken. If your production queries lean toward descriptive references, budget for an LLM-based resolution step instead of an ever-growing static alias table.

  How Token Cost Scales With Conversation Length

  My working assumption going in was that raw-dump token cost scales O(N^2) as conversations grow. I measured it instead of assuming it, because shipping an imprecise complexity claim to an audience that checks it is a fast way to lose credibility.

  The setup: one fact stated once, followed by a growing number of filler turns (ranging from 10 up to 800), followed by a single query asking for that fact. This isolates per-query token cost as a pure function of conversation length, with information content held completely fixed.

  
   
    
     
      Filler turns
      Raw Dump tokens
      Vector RAG tokens
      Context Graph tokens
     

    
    
     
      10
      157
      54
      23
     

     
      50
      659
      54
      23
     

     
      100
      1,287
      54
      23
     

     
      200
      2,542
      54
      23
     

     
      400
      5,052
      54
      23
     

     
      800
      10,072
      54
      23
     

    
   

  
  When the conversation length grew 80x (from 10 to 800 turns), the raw dump’s token count grew 64.15x. Meanwhile, vector RAG and the context graph both grew 1.00x—completely flat.

  The raw dump’s tokens-per-query is O(N), which is linear in conversation length, converging to about 12.6 tokens per filler turn. It is not quadratic. The O(N^2) story only becomes accurate if you sum the cost across an entire multi-query conversation: Q queries, each run against a transcript that has grown linearly, lands around O(N.Q) total cost. That is the real number, just a more precise one than “each query costs O(N^2).”

  Vector RAG and the context graph both hold flat at O(1) per query because both architectures only ever pull a bounded number of items regardless of how long the conversation gets.

  
   
   Token efficiency in LLMs: Comparing the rapid context window scaling of raw chat dumps against the flat, sustainable token usage of Vector RAG and Context Graph architectures.
  
  What I’d Flag Before Taking This to Production

  A few things are worth being direct about before anyone copies this pattern into a real application.

  On latency: Vector RAG is actually the slowest architecture here, not the graph. It refits TF-IDF over the entire corpus on every query call rather than maintaining an incremental index. Averaged across all five scenarios, context graph query answering came in at 0.050ms versus Vector RAG’s 1.764ms.

  That gap closes in a real deployment where you would cache the vectorizer instead of refitting from scratch—the benchmark measured default behavior, not best-case engineered versions. The graph’s occasional spike to 1.9ms comes entirely from join queries walking multiple candidate paths before scoring.

  On what the alias table is actually doing: The entity alias table that lets “the authentication module” resolve to AuthModule is a hardcoded stand-in for real entity linking. In production, that step is an LLM call. The benchmark is deterministic because I hardcoded the aliases I anticipated—it does not mean the vocabulary-mismatch problem is solved for arbitrary query phrasing. It is a real ongoing cost that I am flagging, not hiding.

  On token estimation: I used a ~4-characters-per-token heuristic instead of tiktoken, because tiktoken downloads its BPE rank file from a remote URL on first use—a hidden network dependency in a benchmark built to have none. The heuristic is applied identically across all three architectures, so it cannot bias the comparison between them, but the absolute token numbers are approximations.

  On what this benchmark did not test: Distractor turns here are generic chatter—”no blockers on my end,” “sounds good.” Real production noise is topically close to actual facts. I would expect all three architectures to drop in accuracy under adversarial noise, and I have not measured that, so I won’t claim the lead holds.

  On what is missing for production use: real entity extraction (the ingest() interface already accepts a structured triple, so swapping in an LLM-based extractor is a contained change), incremental vector indexing, graph pruning for long-running conversations that accumulate entities indefinitely, and persistent storage. The repo includes a NetworkX-to-Neo4j export path for anyone who needs durability and concurrent multi-agent writes—but that is an optional step, not a performance upgrade. The reasons to make that jump are transactional guarantees and concurrency, not raw query speed.

  What the Numbers Actually Say

  None of this needed a bigger model or a longer context window. Every single result came from changing how information is represented, not how much data gets crammed into a prompt.

  If you take only one number from this article, take the join-query gap: 80% versus 20–40%. That is the real argument for structured memory, not the token savings.

  While the token savings are real and measurable, they are secondary. In this benchmark, questions requiring two facts from completely different parts of the conversation were where the graph architecture showed its largest advantage. That gap held consistently across all five scenarios, not just the ones that happened to be easy for a graph.

  The full project—five scenarios, three architectures, the test suite that locks these numbers in as regression tests, and the Neo4j export path—is available at the repository below.

  Full source code: https://github.com/Emmimal/context-graph-benchmark/

  References

  [1] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the Middle: How Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics, 12, 157–173. https://doi.org/10.1162/tacl_a_00638

  [2] Zhang, W., Zhou, Y., Qu, H., & Li, H. (2026). Loosely-Structured Software: Engineering Context, Structure, and Evolution Entropy in Runtime-Rewired Multi-Agent Systems (arXiv:2603.15690). arXiv. https://arxiv.org/abs/2603.15690

  [3] A. Kollegger, “Context Graphs & Agentic Decisions,” Neo4j Developer Blog, Jan. 31, 2026. [Online]. Available: https://medium.com/neo4j/context-graphs-agentic-decisions-9a125f22f411

  [4] W. Lyon, “When Your Agents Share a Brain: Building Multi-Agent Memory with Neo4j,” Neo4j Developer Blog, Apr. 13, 2026. [Online]. Available: https://medium.com/neo4j/when-your-agents-share-a-brain-building-multi-agent-memory-with-neo4j-bac609f17b23

  [5] Macklin, N., Zaim, Z., & Erdl, A. (2026). Context Graphs and AI Memory Across the Globe. Neo4j Developer Blog. https://medium.com/neo4j/context-graphs-and-ai-memory-across-the-globe-bb17e293df32

  [6] NetworkX documentation. https://networkx.org/

  [7] Scikit-learn Developers, “TfidfVectorizer,” Scikit-learn Documentation. [Online]. Available: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

  [8] OpenAI. Counting tokens with tiktoken. https://github.com/openai/tiktoken

  [9] Neo4j Python Driver documentation. https://neo4j.com/docs/api/python-driver/current/

  Disclosure

  All code in this article was written by me and is original work, developed and tested on Python 3.12 (Windows, PyCharm). Benchmark numbers are from actual runs of the code in the linked repository and are reproducible by cloning it and running benchmark.py and measure_scaling.py, except where the article explicitly notes a number is a heuristic or estimate rather than a measured result. I have no financial relationship with any tool, library, or company mentioned in this article.
