# RAG Is Not Machine Learning， and the ML Toolkit Solves the Wrong Problem

- BestBlogs URL: https://www.bestblogs.dev/article/5265f8ad
- Original publisher URL: https://towardsdatascience.com/rag-is-not-machine-learning-and-the-ml-toolkit-solves-the-wrong-problem/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-02 02:50:03
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 37083

---

A development team dedicated six months to fine-tuning their RAG pipeline.

  
   They ran five Optuna sweeps.

   They added a custom reranker.

   They fine-tuned an embedding model on their own data.

  

  Production accuracy never moved. Pilots kept complaining about the same wrong answers. Six months in, the bug was in the parser.

  The team was lost, not stuck. RAG is not machine learning, and the ML toolkit solves the wrong problem. This is the single most expensive misconception in enterprise RAG today. It costs months of careful work, the wrong people on the wrong tasks, and a quiet erosion of trust in the system.

  RAG looks enough like machine learning that the ML toolkit feels like the natural next step. The instincts (hyperparameter optimization, evaluation datasets, explainability frameworks) are not wrong in isolation. They are imported from the wrong field. The methods that work for training models don’t work for assembling search systems.

  The point is not that ML is bad. The embedding model that powers vector search is itself a deep learning model, but you don’t train it, you consume it. The point is that the system you’re building around it is not a model, and treating it as one wastes time, picks the wrong metrics, hires the wrong people, and hides the real failure modes.

  The “RAG is not ML” position is one piece of Enterprise Document Intelligence Volume 1, which builds enterprise RAG brick by brick. The four bricks (parsing, question parsing, retrieval, generation) are the engineering toolkit this article points to.

  1. Two different problems

  Machine learning solves problems where the true answer is unknown and has to be predicted. Will this customer churn? What’s the probability this transaction is fraud? Is this image a cat? You don’t know the answer in advance. That’s why you train a model. The model learns from labeled examples, generalizes to new inputs, and produces a prediction. Performance is measured in aggregate, across thousands of test cases, because individual predictions can be wrong while the model is still useful overall.

  RAG solves a different problem. The answer to “what is the effective date of this contract?” exists, written on page one of the document, or it doesn’t exist anywhere. There’s nothing to predict. The system either finds the answer in the document and reports it faithfully, or it fails and should say so. Performance is binary at the question level (got it or didn’t) even if you measure aggregate rates across many questions.

  These differences are concrete:

  
   In ML, “the model was wrong on 8% of cases” is a feature of the system. You build redundancy, downstream checks, human review for the borderline cases. In RAG, “the system gave a wrong answer 8% of the time” is a bug. Each of those 8% has a specific cause: the wrong passage was retrieved, the right passage was retrieved but the model paraphrased it badly, the answer wasn’t in the corpus and the system made one up. They aren’t statistical noise to optimize on average. They’re individually fixable failures.

   In ML, you can’t generally tell why the model got a particular case wrong. That’s why explainability is a research field. In RAG, you can always tell. The retrieval logs which passages it returned. The generator saw exactly those passages. If the answer is wrong, you walk the chain backward and find the broken link. There’s nothing hidden.

   In ML, the model improves by training on more data. In RAG, the system improves by indexing better, parsing more carefully, retrieving more precisely, prompting more clearly. None of that is training. It’s engineering.

  

  That difference changes which tools you reach for when something breaks.

  The cases catalogued in Article 2 fall exactly here: negation, exact identifiers, internal acronyms, signal dilution in long context, topical proximity outranking the actual answer. None of those move when you swap embedding models or sweep chunk sizes. They aren’t bugs a model can learn its way out of, because there is no labeled signal saying “this is the right line” for the model to train on. The fix is structural (question parsing, expert keywords, retrieval that knows the document’s structure), and the next sections walk through the three ML reflexes that pick the wrong tool instead.

  2. Three arguments that don’t apply

  Three ML methods get imported into RAG projects by default: hyperparameter optimization, evaluation datasets with train/test splits, and feature-attribution explainability. Each is reasonable inside ML. Each misfires here.

  2.1 The hyperparameter argument

  The most common framing goes something like this: chunk size, overlap, top-k, similarity threshold. These are hyperparameters, and you should optimize them the way you optimize ML models, using tools like Optuna or Ray Tune. Run a sweep, plot the curves, pick the best configuration.

  In these setups, top_k is the number of passages the retriever keeps, and similarity_threshold is the minimum cosine score a passage must reach to qualify. The code below declares all four as numbers to optimize:

  # What teams typically write (and why it's the wrong activity)
import optuna
def objective(trial):
    chunk_size    = trial.suggest_int("chunk_size", 100, 2000)
    chunk_overlap = trial.suggest_int("chunk_overlap", 0, 200)
    top_k         = trial.suggest_int("top_k", 1, 20)
    threshold     = trial.suggest_float("threshold", 0.5, 0.95)
    accuracy = run_rag_pipeline_and_score(
        chunk_size, chunk_overlap, top_k, threshold
    )
    return accuracy
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=200)  # two weeks of compute later...

  There’s a grain of truth here. These variables do affect retrieval quality, and they are worth tuning. The trouble starts with the word “hyperparameter,” which brings in a metaphor with hidden assumptions.

  In machine learning, a hyperparameter controls how a model learns: learning rate, regularization strength, number of layers. The model itself is what changes during training; the hyperparameter shapes that change. In RAG, there is no learning. The chunk size doesn’t control how something learns. It controls how a function splits text, the same way every time, regardless of what you’ve fed it before.

  What looks like a hyperparameter is a configuration choice, the kind you’d make when configuring a search engine. The expertise needed to tune it well isn’t statistical optimization. It’s understanding the structure of your documents and the shape of your questions. Chunk size of 512 tokens may work beautifully on dense academic papers and disastrously on insurance contracts where a single clause spans 800 tokens and breaking it in half loses the conditional that gives the clause its meaning. No grid search will tell you that. You need to read your documents.

  This is why teams who grid-search chunk size often find a “best” value that performs marginally better on the test set and identically on production data. The optimum on the test set was an artifact of the test set, not a genuine improvement in the underlying system. They’ve optimized a number, not solved a problem.

  
   Common pitfall: A team running Optuna over chunk_size, top_k, and similarity_threshold for two weeks, ending up at chunk_size=487 with no idea why. The honest answer to “why 487?” is “because Optuna said so.” That answer doesn’t survive a real production failure, and it doesn’t generalize when the document distribution shifts. A chunk size of 500 chosen because that’s roughly the size of a paragraph in this corpus is more defensible than 487 chosen because a sweep landed there.

  

  The right activity isn’t tuning numbers. It’s deciding structurally how to chunk. By section? By paragraph? By the table of contents entries? By question type, with different chunkers for short lookups vs long clauses? Answered by looking at documents and questions, not by optimization curves.

  There’s a deeper reason chunk size resists optimization: by construction, no single chunk size can serve every question. Take two questions on the same insurance contract:

  
   “What is the effective date?” The answer is one line, somewhere on page one. It wants a chunk small enough to pin down a single line precisely.

   “What are the exclusions of the policy?” The answer might be one page, or three pages, depending on how the insurer wrote it. It wants a chunk large enough to capture an entire section.

  

  There is no number that satisfies both. A chunk size of 200 tokens chops the exclusions section into incoherent fragments. A chunk size of 2000 tokens buries the effective date in surrounding noise.

  Trying to find “the best chunk size” is therefore not a tuning problem. The framing itself is broken: no single number can serve a distribution of questions whose answers have different lengths.

  You could, in principle, make chunk size respond to the question by training a small model that predicts the right chunker from the question’s features: classify the intent, regress over the expected answer length, output a strategy. That would be machine learning applied legitimately, on a problem where something is being learned.

  But you don’t need to. You can write the rule down. Look at a question and you can tell whether it asks for a date, a section, or a comparison. So can a domain expert. So can ten lines of Python with hand-written conditions over keywords. The deeper reason RAG isn’t machine learning is that, for most of the decisions inside the system, you already know the answer, or someone on your team does. Machine learning is the tool for problems where nobody knows the answer in advance.

  The right approach is to stop looking for one chunk size and start routing different question types to different retrieval strategies:

  # What to do instead: route by question type
def chunk_for_question(question: str, line_df, toc_df):
    intent = classify_intent(question)
    if intent == "point_lookup":          # "what is the effective date?"
        return chunk_by_line(line_df)
    elif intent == "section_retrieval":   # "what are the exclusions?"
        return chunk_by_toc_section(line_df, toc_df)
    elif intent == "comparison":          # "compare clauses A and B"
        return chunk_by_full_section(line_df, toc_df)

  The two code blocks above are the entire argument of this section. The first runs Optuna over four numbers for two weeks and produces a value nobody can defend. The second makes one structural decision per question type and produces a system whose behavior anyone can explain.

  Later articles develop how to classify intent (Article 6, on question understanding) and how the different retrieval methods and granularities are implemented (Article 7, on retrieval). The point here is just that the activity isn’t tuning, it’s routing.

  2.2 The evaluation dataset argument

  The next ML import is evaluation method. The reasoning goes: RAG, like any ML system, needs a proper evaluation dataset: questions paired with expected answers, split into train and test sets, scored with precision and recall. Frameworks like RAGAS have made this even more tempting, offering metrics for faithfulness, answer relevancy, and context recall that look satisfyingly ML-ish.

  Evaluation is useful. The issue isn’t whether to evaluate. It’s what the metrics mean. In machine learning, evaluation tells you whether a model has generalized from training data to unseen examples. The train/test split exists because you want to detect overfitting: a model that memorized the training set rather than learning a transferable pattern.

  In RAG, there is nothing to generalize. Overfitting (when a model memorizes training examples rather than learning a pattern that transfers to new data) cannot happen here: the system does not change between queries. The retriever computes the same cosine distances every time. The generator follows the same prompt template. There is no model adjusting to data.

  What evaluation measures in RAG is three things, all of which are coverage and quality questions, not statistical generalization:

  
   Does my corpus contain the answer? If not, the system can’t find it. This is a content question, not a model question.

   Does my retriever find the right passage? If the answer is in the corpus but the retriever missed it, the system fails. This is a search question.

   Does my generator stay faithful to what was retrieved? If the right passage was retrieved but the model paraphrased it incorrectly or hallucinated extras, the system fails. This is a generation discipline question.

  

  Each one points to a specific fix. Mixing them up under an aggregate “accuracy” score loses information. A 75% accuracy from “corpus is missing 25% of the documented topics” demands different action than a 75% accuracy from “retriever misses the right passage 25% of the time.” The first calls for ingesting more documents. The second calls for fixing the retriever. An aggregate metric that treats them the same hides the diagnostic.

  This also explains why teams using RAGAS-style frameworks sometimes report great metrics on a held-out test set and then watch the system fail in production. The test set covered topics where the corpus had answers and the retriever happened to find them. Production has questions whose answers are not in the corpus at all, and the system either hallucinates or fails to say “not found.” The metric was high on the test set because the test set was friendly. The system isn’t broken. The evaluation was.

  What you need to evaluate, broken down by question type, takes about ten lines:

  # Retrieval recall, per question, per intent
def evaluate_retrieval(reference_set, retrieve_fn):
    rows = []
    for ref in reference_set:
        retrieved_lines = retrieve_fn(ref.question)
        recall = len(set(retrieved_lines) & set(ref.expected_lines)) / len(ref.expected_lines)
        rows.append({
            "question": ref.question,
            "intent":   ref.intent,
            "recall":   recall,
            "hit":      recall > 0,
        })
    return pd.DataFrame(rows)
# Always break down by question type, never just an aggregate
df.groupby("intent")["hit"].mean()
# point_lookup        0.92
# section_retrieval   0.41   <-- this is the real problem
# comparison          0.55

  A single aggregate accuracy of 63% would have hidden the catastrophe on section_retrieval. The per-intent breakdown reveals it instantly. Recall here means: on questions where the answer exists in the corpus, did the retriever find the right passage? Grouping by intent (point_lookup, section_retrieval, …) shows which kind of question fails, and therefore which part of the pipeline to fix.

  RAG has two evaluation surfaces with very different shapes.

  The retrieval surface is a search problem: did the right passage land in front of the model? Measuring this means checking, on a reference set of questions, whether the relevant lines or pages were retrieved at all. The metric is recall at the level you care about (recall at line, at page, at section) and it’s specific to your corpus. Nobody else can run this evaluation for you. Your corpus is unique. This is where the bulk of evaluation effort belongs.

  The generation surface is different. Once the right passage has been retrieved, the question becomes: did the model produce a faithful answer, in the right format, with proper citations, and a clean “not found” when the passage didn’t contain the answer? Some of this you do evaluate yourself, but a large part is already evaluated by the LLM vendors. OpenAI, Anthropic, and Mistral spend enormous resources testing whether their models follow JSON schemas, refuse to invent, and respect prompt instructions. Those are the dimensions on which they improve their models. As a RAG builder, you’re not training the generator. You’re consuming it. If the model fails badly at returning structured JSON or stays unfaithful to its inputs, you’ll notice within an hour of integration. That’s not a metric to set up; it’s a sanity check that’s either obvious or fine.

  What this means in practice: most of your evaluation time should go into retrieval (which is corpus-specific and only you can do it), not into generation (which is mostly the vendor’s problem, and which shows obvious failures fast). Teams that spend weeks building elaborate generation evaluation suites are usually putting off the harder retrieval work that would improve the result.

  
   Going further: Evaluating Your System (later in the series) walks through how to build a reference set for your specific corpus, the four metrics that matter, and why per-question-type metrics are essential while aggregate metrics are misleading.

  

  2.3 The explainability argument

  Machine learning has its own toolkit for explainability. SHAP values to attribute predictions to features. LIME for local approximations of complex models. Attention visualization for transformers. When people start asking for RAG explainability (“why did the system give this answer?”) they naturally turn to these tools. They want to score retrieval relevance, weight document contributions, visualize which tokens influenced the output.

  The irony is that RAG is more explainable by design than most ML models. There’s no need for SHAP. There’s no opacity to crack open. The system retrieved these specific passages from these specific sources, and the answer was built on top of them. That is the explanation. It’s documentary, not statistical.

  This points to a deeper asymmetry between machine learning and RAG. In machine learning, the human has intuition but cannot quantify. Ask who survived the Titanic and people say wealth, age, class: none wrong, none precise. The model has no such doubt: fit a decision tree and the root split is sex, the next cut is an exact age threshold nobody would have guessed, then class. Every split is a number intuition alone could not have produced. The model exists to put those numbers down.

  
   
   
    A real sklearn decision tree on Titanic data. Every threshold is a number intuition couldn’t produce – Image by author
   
  
  For text data, the direction reverses. The user can read the source. A lawyer scanning a contract sees the conditions, the exceptions, the dates. A compliance officer reads a policy and knows whether a behavior breaches it. The text doesn’t hide its meaning, and the expert is already a fluent reader.

  There are exceptions: sarcasm and irony are the classic ones, where modern LLMs sometimes catch what a literal reader misses. But in enterprise contexts the user is the domain expert.

  The model isn’t there to explain the text. It’s there to do the reading at corpus scale, and a citation is enough to let the expert verify any answer in seconds.

  When a user asks “why this answer?”, the right response isn’t a heatmap of attention weights or a feature attribution score. It’s: “I looked at pages 12, 47, and 89 of this contract. Here’s the exact text I used. The answer follows from that text.” If the user disagrees with the answer, they can read the source themselves and judge. They don’t need an explainability framework. They need a citation.

  The fifty-line pipeline from Article 1 already showed this. The prompt asked the model to return the start and end line numbers (with their pages) alongside the answer, in a structured JSON; the annotator then highlighted those exact lines on the PDF. No SHAP, no LIME, no attention visualization, no specialized observability platform. The “explanation” was a side product of how the prompt was written. The citation is part of the answer, not an analysis layer added on top.

  The trace is the explanation. Reading it requires no interpretation, just reading.

  Importing ML explainability into RAG is solving a problem that doesn’t exist. SHAP on a retrieval score is using a scalpel to open a mailbox. The retrieval score is already a number you computed on inputs you can read. There’s nothing to attribute that you don’t already see.

  The deeper failure of the ML-explainability framing is that it makes you focus on the wrong thing. You start trying to explain why a particular passage scored higher than another in vector space, a near-impossible question that doesn’t matter. What matters is whether the right passage was retrieved at all, and whether the answer faithfully reflects it. Those are questions you can answer by reading the logs and the source. No tooling needed.

  3. What changes when you see RAG correctly

  Once you stop treating RAG as ML, two things change. The day-to-day tools, metrics and people reorganize around search rather than training. And a deeper question (where the intelligence sits) moves from the model to the team. Both come from the same framing.

  3.1 Tools, metrics, people

  Three concrete things change.

  The tools change: You don’t need PyTorch, or a training cluster, or hyperparameter optimization frameworks for the system itself. You need a good parser, a flexible retriever, careful prompt engineering, and structured logging of everything that happens. The components that are ML (the embedding model, the LLM) you consume as services. They’re commodity inputs, not things you build or train.

  The metrics change: Aggregate accuracy gives way to per-failure-mode metrics: retrieval recall (did we find the right passage?), answer faithfulness (did the model stick to it?), extraction accuracy (when extracting structured data, did the values match?), not-found rate (when the answer isn’t in the corpus, did we say so cleanly?). Each measures something specific, each maps to a specific part of the pipeline you can fix.

  The people change: A pure ML team trying to ship a RAG system often misses what makes it work, and what makes it fail. The skills that matter most are software engineering (the system has many moving parts that need to compose cleanly), domain expertise (someone has to know what a good answer to a domain question even looks like), and information retrieval intuition (someone has to think like a search engine designer, not a model trainer). ML expertise is useful, but it’s not the dominant skill. A team of ML researchers and no domain expert will produce a beautifully tuned system that misses the point. A team with one ML-aware engineer, two software engineers, and one domain expert will usually outperform it.

  3.2 Where the intelligence sits

  The shift in people points to a deeper question: where does the intelligence of the system live?

  In an ML system the intelligence lives in the model. The model holds the patterns. The team feeds it training data and tunes the loss function. In a RAG system the intelligence lives in the team. The lawyer knows which clauses to look at first. The underwriter knows what “deductible” means, and which page usually carries it. The compliance officer knows which regulation applies to which product. None of that lives inside the embedding model. None of it comes out of a hyperparameter sweep. It already lives in the heads of people who have read these documents for years.

  Watch an underwriter open a new policy. She doesn’t read it linearly. She jumps to the exclusions section first because she’s read five hundred of these and knows that’s where the trap usually lives. She checks the schedule of benefits for the deductibles and ceilings. She checks the territory clause. Three minutes in, she has a clearer view of the contract than any embedding model would produce on a thousand of those contracts. That habit is what the system has to amplify.

  3.3 Amplifying the expert, brick by brick

  The job of an enterprise RAG system is to amplify that expertise at scale, not replace it. What that looks like depends on the brick.

  Parsing comes first. If the parser turns a contract’s PDF into scrambled text, no downstream cleverness recovers it. If the document has a working table of contents, the parser has to extract it cleanly, because the TOC is what the expert relies on to navigate. When a document has no TOC at all (scanned faxes, slide decks exported to PDF, old typewritten policies), reconstructing one becomes a job in itself, often more useful than any retrieval tweak.

  Question understanding carries the team’s vocabulary across the gap between how a user phrases a question and how the document writes the answer. The pilot user types kettle, the contract says small electrical appliance. The compliance officer types data breach, the policy says unauthorized disclosure of personal information. The expert knows the mapping. The question parser turns that mapping into a lookup table: translations across languages, spelling variants, plural forms, internal acronyms. None of it is learned from data, it is dictated by the expert and written down.

  Retrieval amplifies what the expert already does by hand. The expert searches keywords; that part is already easy. What the expert cannot do at scale is run regex patterns over thousands of pages, check whether two terms co-occur inside the same paragraph, or combine boolean conditions across the whole corpus. The retriever does that work fast, then hands candidates back so the expert can verify.

  Generation does the two things the expert would otherwise do by hand: cite the exact passage that supports the answer, and format the raw value into something usable. The string 3455434 on the page becomes €3,455,434 in the answer. 20260516 becomes May 16, 2026. thirty days from the date of the loss stays verbatim, with a citation back to the clause so the expert can verify in one click.

  Articles 5, 6, 7, and 8 develop each brick in turn: the parser that extracts TOC structure, the expert dictionary that maps vocabulary, the TOC-aware retriever, the typed-answer generator. Same principle every time: pick up a piece of human expertise and move the repetitive part to the machine.

  This is also why the series is careful with autonomous agents. It prefers keyword retrieval to embedding similarity by default. It treats reranker tuning as a last resort. Each of those defaults assumes there is no expert to consult. In enterprise contexts the expert is always there. The system should listen to them.

  If you work in a setting with no expert, with unbounded questions, with very different documents, this series will not be your best guide. General-purpose retrieval and autonomous agents are a better fit there.

  4. Two parts, two failure modes

  A useful way to picture RAG is as a search engine, plus an LLM that writes the answer. Two parts, each with a clear job, each with its own way of breaking.

  The search engine retrieves passages from documents. Given a question, return the lines, paragraphs, or sections most likely to contain the answer. This is a pure search problem: selectivity, recall, ranking. Decades of information retrieval theory apply. The fact that part of it uses neural embeddings doesn’t change its nature; embedding similarity is just one ranking signal among several.

  The LLM takes a passage and a question and produces a natural-language answer with a citation. The LLM doesn’t find the answer. The search engine already did that. The LLM writes the answer from a passage that’s been placed in front of it. It’s closer to a translator or a scribe than to an oracle.

  Mapping back to the four bricks from Article 1: parsing, question understanding, and retrieval together make up the search engine; generation is the LLM. The brick view is the operational one (one box of code per brick); the two-part view is the mental model you carry in your head when something goes wrong.

  The two parts fail in different ways, and the diagnosis starts at the seam between them. Pull the trace from a failing query: were the retrieved passages in front of the model, and did they contain the answer?

  If the answer wasn’t in the retrieved passages, the search engine is the culprit, and the fix is upstream. Was the right page corrupted by the parser (OCR errors, multi-word terms split across lines, two-column interleaving)? Did the question parser miss a synonym the expert vocabulary should have expanded? Did the retrieval mechanism rank the right page out of top_k, or break on punctuation that needed a regex? Or is the relevant document just not in the corpus? Four very different fixes, all upstream. “Tune the retriever” is meaningless until you’ve localized which one. The same four bricks that amplify the expert when working (section 3.3) break in their own ways here, each with its own deep-dive article (Articles 5, 6, 7).

  If the answer was in the retrieved passages but the response is wrong, the LLM is the culprit, and the fix is downstream. Common patterns: the model paraphrased and lost a conditional, returned the raw 3455434 because the schema left the answer free-form, cited the wrong line numbers, invented a value not in the passage, or produced an answer when it should have said “not found”. Five generation bugs, five different fixes, all in the prompt, schema, or post-validation layer (Article 8). None of them get better by tuning the retriever.

  Here’s what that diagnosis looks like in practice. A user asks “how many heads does the base Transformer use?” (answer: 8, page 5 of the Attention Is All You Need paper, Vaswani et al. 2017; arXiv non-exclusive distribution license, declared on the arXiv abstract page). The system reports “16”. Pull the trace.

  Retrieval returned pages 4, 7, 8. None of them contain the base-model configuration: page 8 describes the big model (which does use 16 heads), pages 4 and 7 describe encoder structure. The generator read the wrong pages and returned the number it found there. The bug is retrieval, not generation.

  Why did retrieval miss page 5? The keywords were ['heads', 'base', 'model']. Page 7 has heads six times; page 5 has it twice. The keyword retriever ranked page 7 higher because it scored by raw term frequency, without checking whether base, model, and heads co-occur on the same line. Five lines of Python in the keyword retriever fix it.

  What didn’t happen: nobody fine-tuned anything. Nobody ran a sweep. Nobody added a reranker. The diagnostic took five minutes; the fix took an afternoon.

  This separation is what makes RAG workable in practice. Each failure has a specific part to fix. There’s no training loop where retrieval and generation get tangled together. They’re independent components, composed cleanly, each replaceable on its own. Production systems gain a lot from this property: you can swap embedding models, swap LLMs, swap parsers, all without retraining anything.

  
   The whole pipeline is configuration, not model.

  

  When something goes wrong, you change a configuration: the retrieval method, the prompt, the schema, a validation rule. You don’t retrain. You change a Python file, you ship, you measure the per-question-type metric for the affected category, and you confirm the fix. Iteration cycle: hours, not weeks.

  Once you see RAG as configuration to assemble rather than behavior to learn, the rest of the series’ choices follow naturally.

  5. Six months on the wrong problem

  A team at a mid-size enterprise is given six months to deliver a RAG system over a few thousand internal documents. They start by building an evaluation dataset of 500 questions, splitting it 70/30 into train and test. They set up Optuna to sweep chunk size, overlap, top-k, and similarity threshold. The first sweep takes a week of compute, comes back with a “best” configuration, and the team ships it for internal testing.

  The pilot users complain immediately. The system answers fluently but is wrong half the time on questions that the evaluators clearly know: questions about specific clauses, specific dates, specific numerical limits. The team’s response is to expand the evaluation dataset, run another sweep, fine-tune the embedding model on synthetic question-document pairs, and add a reranker. Three more months go by. Production accuracy doesn’t move.

  What was wrong: the parser was treating scanned pages with degraded OCR layers as if they were native text. About 30% of the corpus was effectively unreadable, but the team’s evaluation set happened to be drawn from the readable 70%. No amount of chunk size optimization, embedding fine-tuning, or reranker integration could fix it: a third of the documents were producing garbage. A two-day investment in checking each page (the work of Article 5, on parsing) would have caught this on day one.

  The team had spent six months in ML mode (sweeping hyperparameters, growing evaluation sets, fine-tuning models) when the fix was a parser change.

  
   
   
    ix months of ML activity on the TEAM lane; the corpus bug sat untouched on the CORPUS lane – Image by author
   
  
  This story is composite, but every element of it has happened in real projects. The pattern is consistent: ML reflexes drive the team toward optimization activities that feel productive, while the structural problems sit untouched in the parser, the corpus, or the not-found logic. The first instinct on a struggling RAG system shouldn’t be “let’s tune”. It should be “let’s trace what happens to a failing query, end to end, and find the broken link.”

  6. Conclusion

  RAG looks like machine learning. The resemblance is shallow. The answer exists in the document or it does not. There is no statistical generalisation, no learning curve, no train/test split that maps to real failures. The right framing is search engine assembly: a search engine plus an LLM, two parts you can fix independently, with per-failure-mode metrics replacing aggregate accuracy.

  The cost of holding on to the ML framing is not intellectual. It is six months of careful work on the wrong problem. Article 4 turns the right framing into a working diagnostic: RAG problems sit on a grid of document complexity by question control, and each cell calls for a different stack.

  Article 4 is one entry point into Enterprise Document Intelligence Volume 1, which builds enterprise RAG brick by brick across parsing, question parsing, retrieval, and generation: every brick handled with the engineering toolkit, not the ML one.

  
   
  
  7. Sources and further reading

  The article puts RAG in the 50-year IR tradition (Manning, Raghavan, Schütze, Introduction to Information Retrieval, 2008) rather than the ML tradition. The empirical claim that BM25 often beats dense retrievers out-of-distribution comes from Thakur et al. (BEIR, NeurIPS 2021). The per-failure-mode framing is the same direction as Barnett et al. (Seven Failure Points, 2024). The honest concession is that the reranker is a thin learned layer where ML methodology applies. The framing the article uses for explainability is citation as the explanation: a RAG answer carries its source lines, so the explainability tooling ML projects budget for becomes unnecessary.

  Same direction as the article:

  
   Manning, Raghavan, Schütze, Introduction to Information Retrieval (Cambridge, 2008). The 50-year IR tradition the article puts RAG in.

   Thakur et al., BEIR benchmark, NeurIPS 2021 (arXiv:2104.08663). Dense retrievers tuned on MS MARCO often lose to BM25 out-of-distribution. Empirical support for the IR, not ML framing.

   Barnett et al., Seven Failure Points When Engineering a RAG System, 2024 (arXiv:2401.05856). Practitioner taxonomy of where RAG breaks. Same direction as the per-failure-mode framing.

   Kamradt, Needle in a Haystack (2023). The canonical long-context retrieval benchmark. Research-only: tests a single verbatim fact in a long context, not the aggregating questions enterprise users ask. Discussed in Article 1 and developed in Article 7.

  

  Different angle, different context:

  
   Es et al., RAGAS: Automated Evaluation of Retrieval Augmented Generation, EACL 2024 (arXiv:2309.15217). Treats RAG with aggregate ML metrics (faithfulness, answer relevance, context precision / recall) on benchmark datasets. The context is research benchmarks; the article’s framing is per-failure-mode rates on a fixed enterprise corpus.

   Saad-Falcon et al., ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems, NAACL 2024 (arXiv:2311.09476). ML-style RAG evaluation framework with synthetic train / dev / test splits. Same context as RAGAS; the article argues the train / test split paradigm does not fit enterprise RAG where the answer either exists in the document or does not.

   Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, NeurIPS 2020 (arXiv:2005.11401). The paper that named RAG, and the one that trained retriever and generator jointly. A useful borderline reference: the original RAG paper was an ML paper, even though the engineering pattern that inherited the name is not.
