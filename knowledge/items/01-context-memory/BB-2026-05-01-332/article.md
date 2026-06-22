# Embeddings Aren’t Magic: The Predictable Failure Modes of RAG Retrieval

- BestBlogs URL: https://www.bestblogs.dev/article/47f5946d
- Original publisher URL: https://towardsdatascience.com/embeddings-arent-magic-the-predictable-failure-modes-of-rag-retrieval-enterprise-document-intelligence-vol-1-2/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-05-30 23:00:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 57588

---

Two scenes, both familiar.

  Scene 1: A RAG system over a few hundred pages of policy documents goes live for a small team.

  
   The first thing that impresses everyone: it handles paraphrase. Someone asks “how do I cancel?”, the document never uses the word cancel, it uses termination procedures, and the system finds it anyway.

   Another user asks in French while the policy is in English, and the right page comes back. A typo here, a phonetic spelling there, no problem. After a few days the team is genuinely impressed. The closest thing RAG has to magic is sitting in front of them, and it didn’t take any hand-coded synonym table to make it work.

  

  Scene 2: The same system, two weeks later.

  
   The user asks “what’s the rule on contractor overtime?” The system answers “I couldn’t find that information.” The user, who happens to be the business expert who wrote half this manual, frowns, opens the PDF, types non-employee labor into Ctrl-F, and lands on the exact paragraph in three seconds. The right keyword wasn’t overtime. It was the term the document actually uses. The expert knew that; the embedding didn’t.

   Pretty quickly, more cases like this surface. Negation breaks. Exact contract reference numbers break. An internal product code returns the wrong tier. None of it is fixable by swapping the embedding provider.

  

  The position of the series, stated up front: most enterprise reliability gains come from strong upstream filtering (expert keywords, document structure), not from a reranker stacked on top of weak retrieval.

  The classical stack ranks the layers by cost:

  
   cheap embedding similarity at the bottom,

   an optional cross-encoder reranker between,

   the chat-completion LLM on top.

  

  None of them is magic; each breaks in specific ways.

  This article is one piece of the broader Entreprise Document Intelligence Vol. 1 series, which builds enterprise RAG brick by brick from a baseline pipeline to corpus-scale architecture.

  1. What embeddings nail

  Before the failures, what embeddings actually impress at. The failures only make sense in contrast.

  An embedding turns a piece of text into a vector. Texts with similar terms end up close in vector space.

  An embedding is a list of numbers that captures the meaning of a piece of text: a longer list can carry more nuance. Embeddings have improved with each generation. Every case below runs on the same four models, weakest to strongest:

  
   GloVe-avg (2014): averaged 300-dim word vectors. No contextualization. Heavily biased toward literal token overlap. Apache 2.0, declared on the HuggingFace model card.

   all-MiniLM-L6-v2 (2021): small open-source contextual sentence encoder, 22M parameters, 384-dim. Apache 2.0, declared on the HuggingFace model card.

   text-embedding-ada-002 (OpenAI 2022): 1536-dim. Proprietary; governed by OpenAI’s Terms of Use.

   text-embedding-3-large (OpenAI 2024): 3072-dim. Proprietary; governed by OpenAI’s Terms of Use.

  

  Loading each is a one-liner. The two local models come from sentence-transformers (HuggingFace weights pulled to disk on first call); the two OpenAI models go through the API client. Same call shape across all four, returning a vector.

  from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Local models: weights downloaded from HuggingFace, run in-process.
glove  = SentenceTransformer("average_word_embeddings_glove.6B.300d")  # 2014, 300-dim
minilm = SentenceTransformer("all-MiniLM-L6-v2")                       # 2021, 384-dim

# OpenAI models: called through the API.
client = OpenAI()
def openai_embed(text: str, model: str) -> list[float]:
    return client.embeddings.create(input=text, model=model).data[0].embedding

# Same call shape across all four; each returns a vector of its own dimension.
v_glove  = glove.encode("policy renewal")
v_minilm = minilm.encode("policy renewal")
v_ada    = openai_embed("policy renewal", "text-embedding-ada-002")   # 2022, 1536-dim
v_large  = openai_embed("policy renewal", "text-embedding-3-large")   # 2024, 3072-dim

  Each model lives in its own vector space with its own cosine distribution, so raw scores across columns are not comparable. What is meaningful is the separation within a column: does the target win against the decoys, and by how much? Watching the gap widen across the gradient is the empirical evidence that embeddings really did get better.

  The primitive every comparison table below uses is the same: embed the query and each candidate with the four models, score with cosine similarity, return a row per candidate:

  def _cos(u, v):
    """Cosine similarity : dot-product of two vectors, normalised by their lengths."""
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

def compare_models(query, candidates, target=None):
    qg = glove.encode(query)
    qm = minilm.encode(query)
    qa = openai_embed(query, "text-embedding-ada-002")
    ql = openai_embed(query, "text-embedding-3-large")
    rows = []
    for c in candidates:
        rows.append({
            "candidate": c,
            "GloVe-avg":  _cos(qg, glove.encode(c)),
            "MiniLM":     _cos(qm, minilm.encode(c)),
            "ada-002":    _cos(qa, openai_embed(c, "text-embedding-ada-002")),
            "3-large":    _cos(ql, openai_embed(c, "text-embedding-3-large")),
        })
    return pd.DataFrame(rows).set_index("candidate")

  1.1 Conceptual proximity

  car matches passages about vehicles, automobiles, motor vehicles. fire damage finds passages on smoke damage and scorching. manager approval matches a clause about executive approval. The model captures the semantic field, not just the surface words. This is what makes embeddings feel powerful: the user does not have to guess the document’s vocabulary; the embedding bridges the rest.

  
   
   
    Casual query bridges to formal paraphrase. All four models pick TARGET; bigger models widen the margin – Image by author
   
  
  1.2 Synonyms and paraphrase

  Phone number matches telephone. Policy cancellation matches a section titled termination procedures. Fee matches charge. Monthly cost matches premium. Expiration matches policy end date. Doctor matches physician, lawyer matches attorney, car matches vehicle. Single words and multi-word compounds alike. The model has learned that two vocabularies say the same thing, including the gap between casual user phrasing and the formal language documents are written in. Nobody coded that mapping by hand.

  The test: query what is the monthly fee against a synonym TARGET (A flat charge of $9.99...), a literal-overlap decoy (Premium payments are due monthly..., which shares the literal monthly token), and two off-topic decoys.

  
   
   
    Query monthly fee. Three models bridge fee ↔︎ charge; GloVe picks the literal-overlap decoy – Image by author
   
  
  Only GloVe-avg falls for the literal-overlap decoy. Sentence-encoder training (already in 2021’s MiniLM) is what gives real synonym handling. Without it, a candidate that just repeats the query’s tokens in any order wins. With it, the model bridges fee ↔︎ charge even though the two words share no letters. The query is also phrased as a question (what is the monthly fee) and the TARGET as an assertion (A flat charge of $9.99...). The synonym handling is what wins here. But the actual answer (the bare number $9.99 alone, or Yes for a yes/no question) would not necessarily win regardless of model strength. Section 2.2 demonstrates that directly.

  1.3 Typos and misspellings

  insurence still embeds close to insurance. polciy still finds the policy section. deductable with the wrong vowel still lands on the deductible page. Diacritics dropped on French terms (resiliation without the accent) still match the canonical form. Modern embedding models were trained on a web-scraped soup of text where these typos are constant, and they have learned to absorb the noise.

  
   
   
    Typoed query. GloVe collapses to negative cosines; margin to TARGET grows from MiniLM to 3-large – Image by author
   
  
  Look at the score gaps, not the absolute scores. GloVe-avg has no notion of typos. Misspelled tokens are out of vocabulary, so the embeddings collapse and the cosines go negative. The ordering is basically random. The OpenAI models absorb the typos cleanly. Character-level robustness is real, and it scales with model capacity.

  1.4 Cross-lingual matching

  Multilingual embeddings place premium, prime and Prämie in nearby regions of the space. Same for deductible / franchise / Selbstbeteiligung, for claim / sinistre / Schadensfall. A French keyword retrieves an English passage about the same concept. For enterprises with mixed-language corpora (French contracts, English correspondence, German policy schedules), this is genuinely useful when it works, and on modern models it usually does.

  
   
   
    French query against English candidates. GloVe and MiniLM struggle; ada-002 and 3-large bridge languages cleanly – Image by author
   
  
  GloVe fails outright: it picks Coverage limit: $50,000 per year. over Annual premium: $1,200. because the French annuelle lexically associates with year in its averaged word space, and it has no idea that prime means premium. MiniLM technically picks TARGET, but the cosines sit around 0.12, basically noise. ada-002 and 3-large are multilingual by training, like BGE-M3 and multilingual-e5, and they bridge French to English cleanly. The choice is not “vector vs keyword”, it is “multilingual vector model vs English-only one”.

  1.5 Compound polysemy

  Polysemic words have multiple meanings that the context disambiguates:

  
   bank (financial institution / river edge),

   claim (insurance event / assertion),

   store (verb: put away / noun: retail outlet),

   green card (immigration document / a card colored green),

   hot dog (food / a dog that is hot).

  

  When a candidate uses the literal word in the wrong sense, a strong embedding should still pick the semantically right one. This is also where the literal-token bias of weak models shows clearest: GloVe-avg cannot distinguish the two readings of a compound and picks whichever candidate shares the most tokens with the query. Sentence encoders progressively recover the right sense, but how progressively depends on how known the compound is in training data.

  We test two compounds, easy first, then hard.

  First, green card, the easy case. The immigration sense is so heavily attested in training corpora (news, legal text, Wikipedia) that even MiniLM resolves the compound. The test: query green card, three candidates. A paraphrase of the immigration document (TARGET, zero shared tokens), a gaming-context sentence that contains both green and card in literal senses (the trap), and one off-topic decoy.

  
   
   
    green card against immigration paraphrase vs gaming trap. Only GloVe falls in the trap – Image by author
   
  
  Only GloVe falls in the trap. Word-averaging models have no notion that “green card” as a compound refers to immigration. They see two tokens, look for candidates sharing those tokens, and the gaming trap wins. MiniLM is already enough to flip it, because sentence-level training captures the institutional sense. ada-002 picks TARGET by a comfortable margin; 3-large by a wide one. This is the kind of polysemy embeddings handle well, because the public web teaches the compound everywhere.

  Now hot dog, the hard case. Same structural setup (a compound that also reads literally), but the literal reading (a dog that is hot) is also heavily attested in training text. The model has seen plenty of sentences about hot weather and dogs in it. The food sense and the literal sense compete on near-equal footing, and the literal-token bias of weak and mid models wins.

  
   
   
    hot dog against food paraphrase vs literal-token trap. Only 3-large flips the polysemy cleanly – Image by author
   
  
  This is the section 1 case where the model gradient helps the most. GloVe-avg, MiniLM, and ada-002 all fall in the trap. They latch onto the shared hot + dog tokens despite the wrong sense. The same effect was already visible on GloVe in section 1.2 (literal monthly token beating the fee ↔︎ charge synonym). Compound polysemy is the worst case of it: the literal tokens of the query appear in the decoy, so even ada-002 cannot tell the two senses apart. 3-large is the first model that recovers: it picks the food paraphrase by a wide margin even though TARGET shares zero tokens with the query.

  So the practical question for your corpus is not “is there polysemy” but “how institutional is the polysemy I have”. An insurance corpus has plenty of compound polysemy that is not in the public training distribution (claim handling as a verb in a workflow, pool as a risk-sharing instrument). On those, even ada-002 behaves like GloVe behaves on hot dog. The 2024-class model is the realistic fix; the rest of the series goes after the structural one.

  1.6 What these wins really show, and don’t

  The vocabulary in this section has one thing in common: it is public. The model saw green card ↔︎ permanent resident card, prime ↔︎ premium, polciy → policy in millions of training documents. Embeddings handle them well because the equivalence is baked into the weights. What the literature calls the parametric memory of the model (the part that “knows” things from training, without any retrieval) is doing most of the work.

  Two consequences worth naming before we move on.

  1. For these cases, you might not need RAG at all. Ask GPT-4 “what is another name for green card?” and you get the answer without retrieval. The parametric part of the model already knows. RAG earns its place exactly where the parametric part does not: facts that are not on the public web, contract clauses that do not generalise, internal product codes the model never saw. Section 1 used well-known vocabulary so the demos are reproducible and read cleanly. Production RAG is not used to answer these questions.

  2. The section 1 wins do not transfer to enterprise vocabulary. An insurance company has ShieldPro Elite (a product tier), pool (a risk-sharing instrument, not a swimming pool), non-employee labor (the contract’s word for contractor), regulatory citations like Solvency II Article 7. None of this is in the model’s training distribution. On enterprise terms, embeddings fail the same way GloVe fails on hot dog, because the institutional sense the embedding would need to recover is not institutionalised anywhere outside that company.

  The fix is not a bigger embedding model. The fix is the expert who knows the vocabulary, codified as a keyword dictionary (section 3.3 develops this). Section 2.1 makes the failure concrete on the pool example.

  Section 2 catalogues the structural failures. Read them with this in mind: every one of them is the rule, not the exception, on enterprise corpora.

  2. Where they break, and why

  The abilities in section 1 are real; the failures below are equally real, equally reproducible, and persist across all four models. A larger model does not move the ranking. The fix is architectural, not “pick a stronger embedding”.

  Section 1.6 already raised the obvious counter (“for these cases, just ask the LLM directly”). At corpus scale that does not scale: a 200k-document corpus cannot be passed through an LLM on every query. Some retrieval step has to come first. The mainstream pipeline stacks a reranker between embeddings and the LLM; the series’s answer is upstream filtering through expert keywords and document structure (articles 6, 7, 9). Either way, the failures catalogued below apply to the embedding stage. None of these layers is magic.

  2.1 The simplest break: the term isn’t in the model

  Before the structural failures, the most basic one. Section 1.6 said it in words. Here is the demo.

  Take pool. In an insurance contract, pool is a risk-sharing instrument: a group of insureds that collectively absorb losses through aggregated premiums. In general English, pool is a body of water you swim in. Two senses of the same word, with one stark difference: the swimming sense is everywhere on the public web; the risk-pool sense is buried in actuarial textbooks, regulatory filings, and reinsurance treaties that the model barely saw at training time.

  The test mirrors the hot-dog setup from section 1.5, with one twist. Query the bare word pool. Three candidates: a swimming paraphrase (the public sense, no pool token in the sentence), a reinsurance paraphrase using real industry jargon (the specialist sense, also no pool token), and a random control sentence about a train departure (no pool token, no insurance connection, no swimming).

  
   
   
    Query pool. The reinsurance sense ranks below a random control on three of four models – Image by author
   
  
  The swim paraphrase wins on every model, by a wide margin (0.353 to 0.843 cosine, depending on the model). The reinsurance paraphrase, written in genuine industry vocabulary, ranks below the random train-departure control on three of the four models. Even ada-002, the workhorse of most enterprise RAG deployments, puts the train timetable 0.010 ahead of the specialist sentence. Only 3-large gives the specialist sense a 0.006 lift over the control, well inside the noise of the measurement.

  This is the most direct failure mode there is: the embedding space simply does not encode the specialist sense of pool. A reranker stacked on top would not help, because the candidate scores it would re-evaluate are themselves noise. A bigger embedding model would not help, because the model that saw the swimming pool a million times and the reinsurance pool maybe a hundred times will keep weighting the swimming sense.

  pool is in fact a soft OOV case: the swim sense and the risk sense share a register and 3-large catches some signal. The harder cases are strict OOV terms: ShieldPro Elite (a fictional product tier), Solvency II Article 7 (a real regulatory citation), ZRX-2025 (an internal product code). For these the embedding has no anchor at all. The model treats them as random byte strings; ranking them against any other text is a coin flip biased by tokenization quirks.

  The fix is the expert who knows the vocabulary, codified as a keyword dictionary. Section 3.3 develops the workflow.

  The rest of section 2 walks through the structural failures that show up even when the term is in the model. The pool case is the simpler break that comes first.

  2.2 The structural break: term similarity, not answer relevance

  Section 2.1 covered the case where the term simply isn’t in the model. The rest of section 2 covers the case where the term is in the model, and the embedding still gives the wrong answer. Those failures share one structural root. An embedding sees text and ranks it by term similarity. It does not represent the question-to-answer relation at all. Two of the simplest queries you can ask make this concrete. They aren’t enterprise edge cases, they’re the most general questions in the world.

  
   
   
    Yes/no question. The bare keyword Termination beats the actual Yes answer on every model – Image by author
   
  
  “Yes” is the right answer to a yes/no question. It never wins. The literal copy of the query’s noun does. On every model from 2014 to 2024.

  A subtlety worth naming. This particular failure is less harmful in practice than it looks. For a yes/no question, what we actually want from retrieval is not the literal word yes. We want the evidence about the topic: the page where the rule lives. The answer-phase LLM produces yes/no from that evidence. So retrieval pulling Termination or Termination may be required. (the topical matches) rather than Yes, it is possible. is closer to the right behaviour than the demo’s verdict suggests. The principle the article keeps surfacing is here too: the retrieval phase is not the answer phase, and they have to be separated and optimised as two distinct steps. Articles 6, 7, and 8 develop the separation.

  The failure is sharper on the next example, where retrieval actually needs to find the answer-bearing line.

  Now the cleanest factoid in the world: “What is the capital of France?” The internet has seen “Paris is the capital of France” millions of times. If question-answer mapping showed up anywhere in any embedding space, this is where it would show up.

  
   
   
    Query Capital of France. Paris never wins; topic-decoys sharing Capital of or France always do – Image by author
   
  
  Paris is never #1. On three of the four models (GloVe, ada-002, 3-large) the winner is Capital of Italy, the candidate that shares the literal phrase Capital of with the query. On MiniLM a different decoy wins: France is in Europe., because it shares the token France. Different decoys, same root cause: topic similarity, not answer relevance. Going from a 300-dim 2014 bag-of-word-vectors model to a 3072-dim 2024 OpenAI model does not flip the trap. For a factoid question, retrieval should fetch the line that contains the answer. Instead, every model picks the line that matches the query’s vocabulary topically.

  A second nuance worth naming. Modern embedding models train on question-passage pairs (MS MARCO, Natural Questions, BEIR). This does push answer-bearing passages a little closer to the questions they answer. The bias exists. It is weak. On very general factoids it sometimes flips the decision. On specialised vocabulary the model never saw at training (internal product codes, expert terminology, contract jargon), the bias vanishes. Topic similarity dominates again.

  The sections below catalogue this root cause in four concrete failure shapes (negation, magnitudes, topical proximity, signal dilution) plus a survey of the obvious cases. Each is the same mechanism applied to a different query type.

  2.3 Negation

  A negation question turns the logical relation upside down: the user wants the candidate that is the complement of the topic, not the candidate that is closest to the topic. Embeddings can’t do that. They measure topical proximity, not logical complementation. The starker the test, the clearer the failure.

  Query: “What is NOT a city?” Four candidates: three are real entities (two specific cities + the literal word City), and one is Table, a mundane object that happens to be the only candidate that answers the question correctly.

  
   
   
    Query What is NOT a city?. Every model ranks the correct answer last; negation is invisible – Image by author
   
  
  Every model fails the same way. The candidates that match the topic (City, Paris, New York) sit on top, and Table, the one candidate that actually answers the question, lands last. The query word NOT carries almost no signal in the embedding space: the embedding sees a bag containing “city” and ranks anything city-related higher than anything that isn’t. The fix isn’t a stronger embedding model. It’s a step that detects the negation at question-parsing time and inverts the retrieval (Article 6).

  “Sure, but no real user writes a negation query.” A reasonable objection that holds for a moment and then breaks in production. Users do not pose “what is NOT a city?” They pose “what is the premium amount on this policy?” The system returns the deductible by mistake. The user, frustrated, naturally tries to correct: “I want the premium amount, not the deductible.” That second query is a negation, and it is exactly the moment a real enterprise user writes one.

  The instinct is reasonable: a human reader treats not as an exclusion. The embedding does the opposite. By adding deductible to the query, even prefixed with not, the embedding pulls deductible-bearing lines closer, not further. The user’s correction makes the failure strictly worse than the original query.

  This is the larger principle the section keeps surfacing: the raw question is never the right input to the retriever. The fix is upstream, in question parsing: negation gets detected, lifted out of the prose, encoded as a structured exclude-filter, and applied after retrieval, not embedded with the rest of the query. Sections 3.2 and 3.3 return to this point with a positive version: what the retriever actually consumes is a structured representation (keywords, filters, exclusions), not the user’s free-form sentence.

  2.4 Magnitudes and thresholds

  Numerical comparisons, dates, contract amounts, account balances. Anything where the answer depends on the value itself. Take a stripped-down version: query find value greater than 1M, four candidates that are bare amounts.

  
   
   
    Query asks for value > 1M. 1M wins everywhere; 3B, the only correct answer, ranks last – Image by author
   
  
  Every model picks 1M, the candidate that equals the threshold but does not strictly exceed it. The win is pure lexical match: the literal 1M token sits in the query. 3B, the one candidate that actually answers the question, lands at #4 (dead last) on both ada-002 and 3-large. The embedding has no concept of magnitude. It sees 1M next to 1M and that wins.

  This generalizes to any value-comparison or threshold question: monetary thresholds, dates (“after 2020”), durations (“longer than 30 days”), counts. Embeddings are bad at this almost by design: they compress meaning into dense vectors, and the discriminating signal (the value itself, or the operator that picks among values) is exactly what compression destroys. The fix is well known: BM25 / full-text indexing for the lexical match, plus a question-parsing step that lifts the operator and the threshold out as structured fields (Article 6) so a downstream filter can do the comparison.

  2.5 Topical proximity vs answer relevance

  User question: “Who signed the contract?” The corpus has one passage describing how contracts must be signed (authorized representative, signature requirements) and one passage with the actual signature (“Signed: John Smith, Marketing Director, dated 2025-03-15”). The first passage talks about signing; the second is the signature. Which one wins?

  
   
   
    Who signed the contract?. The procedural passage about signing outranks the actual signature line – Image by author
   
  
  This is the structural failure that the model gradient does not fix. Embedding similarity measures topical proximity, not question-to-answer relationship. A page that talks about a topic will often score higher than a page that answers a question about the topic. Definitions outscore values. Background sections outscore conclusions. Procedures outscore the concrete instances they describe.

  Three of four models confirm the pattern here (GloVe, ada-002, 3-large). MiniLM is the exception: its sentence-pair training pushes the concrete-answer phrasing slightly higher than the procedural-density phrasing. The pattern is stable on the other three, and reproduces across most factoid-against-procedure pairs we have tried.

  2.6 Signal dilution in long context

  The previous tests used candidates roughly the length of the query. Real corpus pages are not. A real page is 300-500 words, dense with details, with the answer to a specific question buried in one sentence somewhere in the middle. When you embed the whole page as a single vector, the signal of that one answer-bearing line gets averaged with everything else, and the page-level embedding drifts toward the centroid of the surrounding noise.

  The cleanest way to see this is a one-variable experiment. Keep the answer sentence fixed. Prepend it with an increasing number of unrelated office-life sentences (office hours, parking rules, HR boilerplate, nothing about deductibles or water damage). Score against a fixed control candidate that shares no specific term with the query, just lives in the same broad insurance/claims vocabulary.

  
   Query: deductible for water damage claims

   Answer (varied): For water damage claims, the standard deductible is $500. prepended with N ∈ {0, 1, 2, 4, 8, 16} unrelated sentences

   Control (constant across N): Claims must include photographs, repair estimates, and police reports where applicable.

  

  
   
   
    Answer signal vs noise: prepending unrelated sentences makes the answer score collapse on every model – Image by author
   
  
  Each model fails in its own time, but they all fail. GloVe collapses immediately because bag-of-words averaging drags the embedding toward the noise after a single sentence. MiniLM holds out for four sentences before its sentence-encoder representation gives up. ada-002 and 3-large, both 2022+ OpenAI models trained on question-passage pairs, last the longest, but by the time the candidate is 144 words (eight unrelated sentences), the right answer ranks below a candidate that does not contain the words deductible, water, or damage at all. Embedding a 300-word page is the production version of “answer + 16 noise sentences”.

  This is why production pipelines that embed at the page level frequently miss the right page even when the answer is genuinely on it. The page-vector averages 300-500 words of topical noise around one or two answer-bearing lines. Section 3.1 is the architectural fix: embed line by line, not page by page. Only aggregate up to the page when generation needs the surrounding context. The right line on a noisy page becomes findable again because its embedding is not averaged with everything else.

  2.7 The obvious cases (no demo needed)

  Some query types break embeddings so plainly that a four-model comparison would just repeat the same result. They are listed here for completeness, and to make a broader point: no embedding upgrade rescues them. The fix is upstream (question parsing, Article 6) or in a different tool entirely (BM25, metadata filter, aggregation pipeline).

  
   OOV identifiers and internal jargon: contract references (Section 4.2.1), regulatory citations (GDPR Art. 17.3), invoice numbers, ticket IDs, internal product names (ShieldPro Elite, SAP-MRP, KPI-Q4-V3). The embedding treats them as opaque sequences and cannot rank them semantically. Fix: BM25 or an exact-match index for the lookup, plus a glossary that maps aliases to canonical terms (ShieldPro Elite → top-tier homeowners plan) maintained as expert keywords (Article 6).

   Boolean composition: “documents reviewed by Alice but not by Bob”, “claims with damage and witness”. Bag-of-words averaging erases the logical operators. Fix: parse the question into a structured filter (Article 6) and apply it after retrieval.

   Counting and aggregation: “How many contracts did Alice sign?”, “List all open claims”. Embeddings return one most-similar passage; a counting answer needs a full scan or a SQL-style query over an index. Fix: route these to an aggregation pipeline (Articles 15-20).

   Temporal predicates: “the latest version”, “claims filed after 2020”, “policies expiring before December”. Embeddings do not represent temporal order. Fix: extract the temporal filter at question-parsing time and apply it as a metadata filter on the index.

   Multi-hop reasoning: “Who is the manager of the person who signed contract X?” Each hop is a separate retrieval; the embedding gives you one shot. Fix: an agentic chain, or a graph traversal over a properly indexed corpus.

  

  The pattern is consistent. When an embedding fails clearly, the answer is rarely “buy a bigger embedding model”. It is “lift the query out of the embedding lane and into the right tool”.

  2.8 Same cracks at page scale (real document)

  The four failures above were demonstrated on hand-written candidates. They show up identically when retrieval runs page-by-page on a real document. We embed every page of Attention Is All You Need (Vaswani et al. 2017; arXiv non-exclusive distribution license, declared on the arXiv abstract page; 15 pages) and run three questions; each surfaces a different ranking pathology at page granularity.

  What each result shows.

  
   Q1, barely wins. Three pages within 0.01 of each other; the right page (page 7, where the Adam learning-rate formula lives) wins by 0.007. That’s the margin of luck, not retrieval. A variant of section 2.5 (topical proximity) compounded with general ranking fragility.

   Q2, top-3 saves us. Page 8 outranks page 9, but the answer (Table 3, the d_k row of the ablation) lives on page 9. Top-3 is enough; top-1 would have failed silently. Same flavour as section 2.4 (exact values inside a numeric table).

   Q3, total failure. The answer page (page 8, ε_ls = 0.1) falls out of the top-3 entirely. Page 15 (with example sentences full of ε symbols in formulas) sneaks in instead. This is section 1.5 (compound polysemy) firing on ε: the embedding can’t tell the ε of the Adam optimizer (page 7), the ε_ls of label smoothing (page 8), and the ε of unrelated formulas (page 15) apart.

  

  Same failure categories, scaled up to a real document. The fix is the same one section 3 develops.

  3. How to actually use them

  Section 1 showed what embeddings impress at. Section 2 showed where they break, with two distinct roots: when the term simply isn’t in the model (section 2.1) and when the term is in the model but term similarity isn’t answer relevance (sections 2.2 onward). The natural next question: given that, how do we actually use them in production?

  Four sections. Section 3.1: the right mental model (line-level synonym-tolerant search). Section 3.2: the trick that bridges the question-to-answer gap is not really about embeddings, it’s about extracting the keywords the answer would contain. Section 3.3: the production workflow that makes both work, by discovering the corpus’s vocabulary with experts, codifying it into a keyword dictionary, then running targeted retrieval on top. Section 3.4: the special case of sentiment-heavy corpora (HR feedback, customer surveys, support tickets), where the same discovery mechanism applies to emotional vocabulary.

  3.1 The reframing: line-level synonym-tolerant search

  The simplest way to hold what embeddings are: vector search is keyword search that handles synonyms, typos, and other languages, applied line by line. It is not magic. It is not “page-level semantic understanding”. On a single line, the model treats cancel and terminate as close. It absorbs polciy as policy. It bridges prime and premium across languages. Every match that worked in section 1 worked for this reason.

  When you embed a whole page into a single vector (section 2.6 showed it directly), the signal of one good line gets averaged with the rest, and the right line hides inside a page that mostly talks about other things. So embed line by line. Only aggregate up to the page when generation needs the surrounding context.

  Page-level embedding still earns its place in a few cases: when no single line carries the keyword (the page is about car insurance but never uses that phrase), when the topic is implied by surrounding vocabulary (medical page mentioning A1C / insulin / blood sugar but never diabetes), when style or register matters, when the heading is generic (“Notes”, “Section 5”). Outside those cases, line-level wins almost every time.

  The demo below makes it concrete on a real paper. The previous sections embedded short hand-written candidates. Here we embed every line of the Attention Is All You Need paper (15 pages, ~1000 lines) and search by a short keyword anchor. The top-K results are lines, with their page and line number. You can read each match and see why it matched: the anchor’s keyword or a clear paraphrase is right there in the text.

  Five operations on top of pandas and numpy: encode the query, stack the line embeddings into a matrix, batch-compute cosine in one matmul, sort by similarity, return the top-k. No vector database, no framework, no infra. The “vector store” is a DataFrame column plus a numpy dot product.

  def top_lines_for(question: str, line_df: pd.DataFrame, k: int = 10) -> pd.DataFrame:
    """Rank every line by cosine similarity to `question`. Return the top-k."""
    q_vec = get_embedding(question, client=client)
    line_matrix = np.vstack(line_df["embedding"].values)
    sims = line_matrix @ q_vec / (
        np.linalg.norm(line_matrix, axis=1) * np.linalg.norm(q_vec)
    )
    return (
        line_df.assign(similarity=sims)
        .nlargest(k, "similarity")[["page_num", "line_num", "similarity", "text"]]
        .reset_index(drop=True)
    )

  
   
   
    Top 10 lines for multi-head attention: paraphrases and literal matches from pages 1, 4, 5, 10 – Image by author
   
  
  Two things to take away from the line-level demo.

  1. The matched lines literally show why each one matched. No magic, no ranking opacity. Every top result contains either the anchor’s keyword or a clear paraphrase of it. That is line-level embedding in one phrase: a fuzzy, synonym-tolerant Ctrl-F over the document.

  2. The matched line is an anchor, not the passage you send to generation. The line is a small thing the retriever can confidently locate. The passage that goes to the LLM is usually larger: the surrounding paragraph, the section, sometimes the whole page. Article 7 develops this as a two-step pattern: detect anchors first (line-level, keyword-level, structure-level), then choose a passage around each anchor based on what the question needs. Targeted retrieval = small N around a sharp anchor, not 30 fuzzy pages thrown at the LLM.

  3.2 HyDE: search what the answer would contain, not the question

  Section 2.2 showed that embeddings don’t see questions; they see term similarity. The natural response: stop feeding the question into the retriever. Feed it text that looks like the answer instead. That’s the idea behind HyDE (Hypothetical Document Embeddings). Write (or have an LLM write) a sentence that plausibly answers the question, in the vocabulary the document would use, and embed that. The retriever compares the hypothetical-answer vector to the corpus.

  The point everyone makes about HyDE is the embedding side: “the rewritten query lands in the document’s neighbourhood instead of the user’s”. That’s true and it helps. But the real value of HyDE, especially in enterprise contexts, is on a different layer. Writing a hypothetical answer is also an extraction step: it surfaces the keywords the answer would contain. “Termination procedures”, “rights of rescission”, “cancellation fee”. These are the words that anchor the search, whether the retriever is vector-based or keyword-based.

  
   
   
    Raw query ranks target #4; HyDE rewrite injects doc vocabulary, target climbs to #1 – Image by author
   
  
  Why HyDE worked here, and what actually did the work. The raw query says cancel. The target line says rescission and terminate. Zero shared content tokens. Three lexical decoys in the candidate pool each repeat cancel/cancellation several times, and together they push the formal target down to rank #4. The HyDE rewrite is a fictional answer that happens to contain rescission, terminate, written notice, renewal, the exact vocabulary the target uses. Once those tokens enter the query side, the ranking flips and the target climbs to #1.

  The dominant factor is the keywords the rewrite contains. Register matching (the rewrite’s formal declarative tone aligning with the document’s register) and latent semantic associations from the LLM’s training contribute smaller second-order effects (Article 6 decomposes them in depth); in enterprise vocab-bounded corpora, those do not move the result. Run keyword search on the term set {rescission, terminate, written notice, renewal} and you get the same target with no embedding pass at all.

  HyDE is implicit keyword expansion routed through an embedding step. The LLM writes a full hypothetical answer, the system embeds it, the retriever runs cosine over the corpus. All of that work to inject a handful of keywords into the query. Two simpler paths do the same vocabulary lift, explicitly:

  
   Ask the LLM for the keywords directly. One prompt: “What terms would the answer to this question contain in a typical insurance contract?” Output: rescission, terminate, written notice, renewal. Use them in keyword search. No fictional document, no embed, no cosine.

   Have the expert hand you the dictionary. Lawyers, claims adjusters, compliance officers already know that cancellation in user vocabulary equals rescission in contract vocabulary. Codifying that mapping once is durable; asking the LLM to rediscover it on every query is wasteful.

  

  Both paths beat the HyDE pipeline on three fronts. Auditability: the matched keywords are visible to the team and to a regulator; a 0.83 cosine score is not. Latency: one LLM call, no embed round-trip per query. Durability: the keywords persist in a dictionary, reusable across queries; HyDE regenerates the hypothesis from scratch every time. Article 6 (Question Parsing) formalises this as the explicit expert keyword dictionary that grows with the corpus.

  Consumer vs enterprise. On consumer-shaped corpora (general insurance FAQs, e-commerce help, public-service forms), the LLM has seen plenty of training text in the right register, so its keyword guess is usually decent. HyDE works without an expert in the loop. On enterprise corpora (internal product codes, regulatory citations, contract jargon, custom acronyms), the LLM falls back on generic legalese (“…will be outlined in the terms and conditions…”) and misses the doc’s actual vocabulary. The expert already knows that vocabulary. Asking the LLM to guess what the expert can hand you, on every single query, is the slow path.

  3.3 The production answer: discover keywords with experts

  The standard advice (“use embeddings for semantic retrieval”) is too vague. A sharper question is when do they actually earn their slot in the pipeline? Four answers, each pointing somewhere different.

  Already know the right keywords? Use keyword search. It is faster, cheaper, auditable, and not opaque the way a vector match is. If a regulator asks why a particular passage was retrieved, “the line contains force majeure and pandemic” is a defensible answer. “The cosine similarity was 0.83” is not.

  Typos in the query? Fix the query. A single LLM call corrects polciy to policy and you’re back to clean keyword search. No embedding pipeline required.

  Typos in the documents? Now embeddings genuinely earn their place. OCR’d contracts, scanned forms, hand-typed notes. Keyword search literally cannot match a misspelled token, but a line-level embedding still lands in the right neighbourhood. This is the case where vector search is structurally irreplaceable.

  Multilingual corpus? Same answer, different mechanism. Contracts in French, correspondence in English, regulatory annexes in German. A multilingual embedding lets the user query in one language and surface lines from the others. prime annuelle finds Annual premium: $1,200. (section 1.4 showed it). Maintaining bilingual keyword dictionaries by hand is possible but expensive; the multilingual embedding bridges the languages for free, and the expert keeps the dictionary working in one language with embeddings as the cross-language fallback. Requires a multilingual model: ada-002, 3-large, BGE-M3 work; GloVe and English-only sentence encoders do not.

  Synonyms specific to your enterprise that you don’t know yet? This is the most production-relevant case, and where embeddings are most useful: as a discovery mechanism, not as the retriever itself.

  The reason matters. In legal, medical, insurance, financial corpora, the meaningful synonyms aren’t dictionary synonyms. Force majeure and act of God mean the same thing in a contract, but the embedding model doesn’t know that. They’re not lexical neighbours and not embedding-space neighbours either. They’re business-specific equivalences that only experts (lawyers, claims adjusters, compliance officers) know.

  Concrete pairs across domains. What “domain synonyms” looks like in practice:

  
   Insurance contracts: cancellation ↔︎ rescission, termination, lapse of cover, surrender of the policy. deductible ↔︎ excess (UK), franchise (FR). claim ↔︎ loss notification, incident report. policyholder ↔︎ insured, assured, named party.

   Medical records: blood sugar ↔︎ glycemia, A1C, HbA1c, fasting plasma glucose. heart attack ↔︎ myocardial infarction, MI, acute coronary event. high blood pressure ↔︎ hypertension, elevated BP reading.

   Legal and contract clauses: force majeure ↔︎ act of God, unforeseeable circumstances, events beyond reasonable control. non-compete ↔︎ restrictive covenant, restraint of trade clause. confidentiality ↔︎ non-disclosure, NDA, proprietary information clause.

   HR and employment: dismissal ↔︎ termination of employment, separation, severance event. salary ↔︎ compensation, base pay, gross remuneration. harassment ↔︎ unwanted conduct, hostile environment, inappropriate behaviour.

  

  None of these aliases are dictionary synonyms in the usual sense. They are domain-specific equivalences validated by an insurance underwriter, a clinician, a contract lawyer, an HR professional. The embedding finds them as candidates; the expert says yes or no. Force majeure equals act of God only if you know it does.

  HyDE makes this implicit (the LLM invents the document’s likely vocabulary on the fly, section 3.2 showed where it falls short). The series makes it explicit: a curated keyword dictionary maintained by domain experts.

  # Discovery loop. One corpus, seed terms the expert already knows.
# Same `top_lines_for` primitive from section 3.1: no new infrastructure.

SEED_TERMS = ["cancellation", "deductible", "claim", "policyholder"]

draft_aliases = {
    seed: top_lines_for(seed, corpus_lines, k=10)
    for seed in SEED_TERMS
}
# Each draft is the top-k corpus phrasings closest to the seed.
# Hand to the expert: they keep the real aliases, drop the coincidences.

validated_dictionary = {
    "cancellation": ["rescission", "termination", "lapse of cover",
                     "surrender of the policy"],
    "deductible":   ["excess", "franchise"],
    "claim":        ["loss notification", "incident report"],
    "policyholder": ["insured", "assured", "named party"],
}

# Production retrieval hits this dictionary directly. No embedding call
# on the hot path; the embedding only ran once, at discovery time.

  The results, on a small insurance corpus. Run the seed cancellation against seven candidate lines (four real aliases, three off-topic decoys) and the four aliases rise to the top.

  
   
   
    One seed query, seven candidates. The four real aliases rank top-4 on three of four models – Image by author
   
  
  The pattern is the discovery workflow at work. The model lists candidates ranked by similarity. The expert reads them, keeps rescission, termination, lapse of cover, surrender of the policy, drops premium payments and the other off-topic lines, and the dictionary entry for cancellation is built in one review pass. From that point on, retrieval is keyword search on the dictionary.

  The workflow is progressive and runs with the experts, not around them. First few queries on a new corpus, run embeddings line-by-line as in section 3.1. They surface document phrasings nobody anticipated: the contract uses non-employee labor where the user said contractor; the medical record uses A1C where the user said blood sugar level; the procedure manual uses section 4.2 where the user said overtime rule. Capture those phrasings as keyword aliases in a growing dictionary, with the expert validating each one (they know which aliases are real equivalences and which are coincidences).

  Subsequent queries go through keyword search with the enriched dictionary, no embedding call needed. Each retrieval is now auditable (we know which keywords matched), faster (no LLM/embedding latency on the hot path), and the dictionary itself becomes a durable enterprise asset that survives engineering turnover.

  The reframing is sharper than the standard one. Embeddings aren’t the production retriever. They’re the bootstrap that builds the production retriever, one keyword alias at a time, in collaboration with the people who already know the corpus. Article 6 (Understanding the Question) develops the dictionary engineering: domain hints, expert aliases, multiple alternative phrasings, the feedback loop with retrieval results. Article 7 (Retrieval) develops the targeted retrieval architecture that consumes the dictionary.

  3.4 The HR and customer-feedback case

  Most enterprise documents aren’t sentiment-heavy. Contracts, regulatory texts, financial reports, technical specs are factual corpora; sections 3.1 through 3.3 are built for them. A subset of enterprise corpora is different: customer survey verbatims, employee barometer comments, support ticket free-text, brand mentions on social. The vocabulary here is emotional (drained, frustrated, delighted, let down) rather than technical (force majeure, Solvency II, cedent).

  The discovery workflow still applies. An HR analyst building a burnout-signal lexicon types an explicit concept they care about, say feeling overwhelmed. The embedding surfaces phrasings from the corpus in the same emotional cluster. The top match below shares zero content words with the query; all four models, GloVe through 3-large, rank it #1.

  
   
   
    Query feeling overwhelmed against an emotional paraphrase with zero shared tokens. TARGET wins on every model – Image by author
   
  
  No emotional understanding here. Emotional vocabulary clusters in the model’s space the way insurance vocabulary does in section 1.2 (fee ↔︎ charge). TF-IDF + logistic regression hit roughly 88% on IMDB sentiment in 2010, before contextual embeddings, because emotional words carry signal on their own. Embeddings extend that with synonymy: overwhelmed, drained, empty, hollow, on the edge are automatically close in the space, so a query in one term surfaces sentences using any of them. The same mechanism as section 1.2, applied to a different vocabulary.

  A useful split for production. If sentiment classification is the goal (score each feedback entry, aggregate trends, detect crisis spikes), a dedicated sentiment model outperforms a general embedding. The dedicated model is trained for the task; the embedding is trained for similarity. For vocabulary discovery (what phrasings express distress in our corpus?), the embedding remains the right tool. It surfaces the lexicon the expert validates. Two tasks, two tools. Sarcasm (“Oh great, another Monday”) breaks both, and reliability there needs context the verbatim usually doesn’t provide.

  The pattern here is the article’s larger one. First impression: this looks like emergent emotional understanding. Look closer: it is keyword-similarity with a smarter notion of “close”. Apply accordingly: use the model to discover the vocabulary you didn’t have; don’t ask it to understand the intent behind the vocabulary.

  4. Conclusion

  Embeddings are one brick of Enterprise Document Intelligence Volume 1, which builds enterprise RAG brick by brick. The keyword dictionary this article ends on is what production retrieval (Article 7) reads at query time, fast and auditably.

  
   
  
  Embeddings are powerful and limited in specific, predictable ways.

  
   Section 1: what they handle. Synonyms, paraphrase, typos, cross-lingual queries, and polysemy work well, with each generation of model widening the safety margin.

   Section 2: where they break. Two distinct roots. First, sometimes the term simply isn’t in the model.

   Section 2.1 made this concrete with pool: a random train-timetable sentence beat the reinsurance paraphrase on three of four models. Enterprise vocabulary lives here. Second, when the term is in the model, the embedding ranks by term similarity, not by question-to-answer mapping.

   Section 2.2 showed this directly on the simplest queries. From that second root cascade negation (section 2.3), exact values (section 2.4), topical proximity beating answer relevance (section 2.5), and signal dilution in long context (section 2.6). A whole catalog of “obvious” failures (OOV identifiers, Boolean composition, counting, temporal predicates, multi-hop reasoning) needs no demo.

   Section 3: how to use them in production. Use embeddings line by line as a synonym-tolerant Ctrl-F (section 3.1). When you do need to bridge the question-to-answer gap, the load-bearing piece is the keywords that the answer would contain, not the embedding of the rewritten query (section 3.2). The production answer is a curated keyword dictionary, built by experts and bootstrapped by line-level embedding discovery (section 3.3). Embeddings aren’t the production retriever; they’re how you find the keywords that the production retriever then uses, fast, auditably, every time.

  

  A case from real projects. A team built a RAG system over commercial insurance contracts and spent three months chasing recall. They started with OpenAI’s text-embedding-3-small at 71% recall, benchmarked Voyage, Cohere, BGE-M3 (recall moved between 69% and 73%), then fine-tuned BGE on synthetic question-passage pairs. Recall climbed to 76%. Five points after three months. Then they broke the 200 questions down by type: 92% on conceptual, 23% on negation, 31% on exact-reference, 18% on internal-acronym. The aggregate of 76% hid two categories at near-zero performance — no fine-tuning could fix them. Adding BM25 alongside the vector search took two days, lifting exact-reference recall to 88%. Adding a query expansion step for acronyms via a company glossary took another day, lifting internal-acronym recall from 18% to 71%. One week of structural work outweighed three months of embedding fine-tuning.

  Two signals a team has over-invested in embeddings: the roadmap features “fine-tune the embedding model” as the next milestone before anyone has broken down the actual failure cases; retrieval metrics are reported as a single recall number with no per-question-type breakdown, hiding the categories where embeddings are structurally wrong.

  You just watched embeddings fail in predictable, structural ways. The reflex, especially for engineers from an ML background, is to fix the model: more training data, fine-tune, swap providers, run a sweep. Article 3 makes the case that this is the wrong frame. The failures you just saw are not bugs the model can learn its way out of. RAG is not machine learning, and treating it like one is how teams waste six months optimising the part of the system that wasn’t broken.

  5. Further reading

  The empirical pattern in this article (synonyms, typos, polysemy work; negation, exact identifiers, OOV acronyms fail) matches every controlled study of dense retrievers on out-of-domain enterprise corpora. Reimers and Gurevych (Sentence-BERT, 2019) is the reference for what embedding a line means technically. Ravichander et al. (CONDAQA, 2022) document the negation failure cleanly. The article reframes HyDE (Gao et al. 2023): the load-bearing piece is the keywords the hypothetical answer contains, not the embedding step itself; asking the LLM for the keywords directly recovers the same passage with less infrastructure. Fine-tuning embeddings on enterprise corpora is out of scope here and revisited in Article 21 (production).

  Same direction as the article:

  
   Reimers & Gurevych, Sentence-BERT, EMNLP 2019 (arXiv:1908.10084). The reference for what embedding a line means technically.

   Ravichander et al., CONDAQA, EMNLP 2022 (arXiv:2211.00295). Documents that dense models systematically fail on negation. Same direction as the empirical pattern in this article.

   Gao et al., HyDE: Precise Zero-Shot Dense Retrieval without Relevance Labels, ACL 2023 (arXiv:2212.10496). The HyDE technique the article reframes: keywords from the hypothetical answer are what does the work.

   Formal et al., SPLADE, 2021 (arXiv:2107.05720). Learned sparse retrieval; a bridge between keyword and embedding worlds, in the same spirit as the vector search is keyword search framing.

  

  Different angle, different context:

  
   Karpukhin et al., Dense Passage Retrieval for Open-Domain QA, EMNLP 2020 (arXiv:2004.04906). The canonical dense beats BM25 result on open-domain QA benchmarks. The context is in-domain training data; this article looks at out-of-domain enterprise corpora where the result does not transfer cleanly.

   Wang et al., Text Embeddings by Weakly-Supervised Contrastive Pre-training (E5), 2022 (arXiv:2212.03533) and Lee et al., NV-Embed, 2024 (arXiv:2405.17428). The scale-fixes-it line: larger contrastive pre-training corpora close the OOV gap. The article’s claim is that the failures are structural (compression destroys exact-value signal), not data-volume bound.

   Khattab & Zaharia, ColBERT, SIGIR 2020 (arXiv:2004.12832). Late-interaction retrieval as an answer to exact-token matching at the embedding level; relevant to the “exact values, internal acronyms” failure mode.

   Muennighoff et al., MTEB: Massive Text Embedding Benchmark, EACL 2023 (arXiv:2210.07316). The benchmark driving the “pick the highest-scoring embedding” mindset. Useful for shopping models; the article’s claim is that the leaderboard is not the relevant axis for enterprise OOD vocabulary.
