# Why Vector Search Alone Isn't Enough: Hybrid Retrieval for RAG

- BestBlogs URL: https://www.bestblogs.dev/article/1986e257
- Original publisher URL: https://www.infoq.com/articles/vector-search-hybrid-retrieval-rag/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-06-02 17:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 24781

---

Key Takeaways

    
     Vector embeddings are approximation engines that are excellent at finding semantically similar content, but systematically weak at distinguishing specific entities like version numbers, error codes, and feature flag names.

     Production queries rarely fall cleanly into purely semantic or purely lexical categories; most are hybrid queries requiring both meaning and exact-match, which is where single-method retrieval fails.

     BM25 (short for Best Matching 25) is a ranking function that provides the precision that embeddings can't. It uses three mechanisms: inverse document frequency (IDF), which is a weighting of rare distinguishing tokens; term-frequency saturation; and document length normalization.

     Reciprocal Rank Fusion (RRF) combines BM25 and vector results without the pain of score normalization. It operates on rank position alone, rewarding documents that both retrievers agree on.

     A production retrieval stack is layered. BM25 plus vector search is fused with RRF and is optionally followed by a cross-encoder reranking stage for final relevance gains on a small candidate set.

    

   

   Your company recently launched an internal omni-search, a single system, developed using Retrieval Augmented Generation (RAG), spanning the company's backlog issues, design documents, launch documents, runbooks, and correction of errors (COEs). Engineers, PMs, and managers query it through an LLM-powered chat UI. Teams also wrap it as an MCP tool, so that their AI coding assistants can pull context directly.

   Then an on-call team member in the production support group types: "runbook to enable the payment_v2_enforce feature flag in production" and the chat assistant tells them to disable it instead. Internally, the system ranks documents by embedding similarity.

   To the embedding model, the two runbooks look almost identical. They have the same flag name, same service, same vocabulary, and a similar surrounding context. The on-call engineer doesn't see this ranking directly. They see the chat assistant's answer generated from the top-K results the retriever returned (and sometimes the right runbook isn't even in the top-K). The answer is at best diluted and at worst confidently wrong.

   
   If you have built a search system using embeddings, this situation might feel familiar. The system gets the big idea right but misses the small, specific details that actually mattered.

   The query above demanded two things: a semantic understanding of "feature flag runbook" and an exact match on the operation (enable versus disable). Vector search only handled the first.

   This is not a flaw in your embedding model; it is how vector similarity works. Embeddings find things similar to your query, not things that match it exactly. Because retrieval feeds the top-K results into the LLM as context, ranking matters as much as recall.

   The right answer being present in the top-K is not enough if the wrong answer is ranked above it. The fix isn't to replace embeddings, but to pair them with classical keyword matching on the actual text so that conceptual relevance and exact term matching both contribute to the final ranking.

   Where Vector-Only RAG Pipelines Break

   To understand why this situation happens, it helps to zoom out and look at the full pipeline. A RAG pipeline has three stages, as shown in Figure 1.

   

   Figure 1. A typical RAG pipeline has three stages: chunking, retrieval, and generation. (Source: created by author)

   The elements in Figure 1 can be defined as follows:

   
    Chunking breaks the source corpus into indexable units. 

    Retrieval takes the user's query, searches over those chunks and returns the top-K most relevant ones. 

    Generation hands those chunks to an LLM as context and asks it to produce an answer.

   

   Assume the first and third stages work correctly. Documents are split at sensible boundaries and the LLM grounds its answers in the provided context without hallucinating. The retrieval stage is where the failure from the introduction occurs. The retriever embeds the query, compares it to the indexed document vectors, and returns whichever documents sit closest in embedding space. Closeness in embedding space means semantic similarity, not identity. Two runbooks for the same feature flag, one for enable and one for disable, sit very close together in an embedding space. Their wording differs in only one word out of many and the embedding model produces nearly identical vectors for nearly identical text. The retriever cannot reliably distinguish them. So when the user asks for the runbook to enable the flag, the runbook to disable it is sometimes the closer document and the retriever surfaces it with the same confidence it would retrieve the right one. That is the breaking point, where the same vector space and the same scoring mechanism retrieves the wrong document at the top.

   The Problem Is That Embeddings Are Approximation Engines

   Embedding models like BERT convert text into fixed-dimensional numerical vectors that capture the semantic meaning of text. Text with similar meanings produces similar vectors. "Feature flag", "kill switch", "rollout gate", and "config toggle" all cluster close together in vector space. This clustering is extremely useful when a user searches for an idea. It becomes a precision problem when a user needs an exact entity, a specific feature flag name, a specific error code, or a specific deployment version.

   The same approximation behavior shows up across different failure patterns. When someone searches for ERR_PAYMENT_GATEWAY_TIMEOUT, related codes like ERR_PAYMENT_GATEWAY_REJECTED and ERR_PAYMENT_GATEWAY_UNAUTHORIZED end up close to the query because they share the ERR_PAYMENT_GATEWAY prefix and appear in similar troubleshooting documents. The trailing word that distinguishes them carries little weight on its own. The embedding model behaves exactly as designed. It is built to find similar, not identical things. When the distinguishing element is small relative to the surrounding text, embeddings collapse the distinction.

   Figure 2 shows an embedding space, in which semantically similar items cluster together. Within a cluster, distinguishing between specific entities (e.g., the runbook to enable vs. disable a feature flag) becomes difficult. This is the precision failure that hybrid search addresses.

   

   Figure 2. Semantically similar items cluster together. Not Every Query Has the Same Problem. (Source: created by author)

   Search queries fall into three broad categories based on which retrieval method handles them best.

   Semantic Queries

   A user asking "What's our protocol when a region goes offline?" is asking about a concept. Documents titled "Disaster recovery architecture", "Active-active replication strategy", and "Failover runbook" should all rank well even though they share no words with the query. Embeddings handle this situation naturally because they capture meaning rather than literal word matches.

   Exact-Match Queries

   These queries are also called lexical queries in the IR literature. A user pasting an error code from a stack trace or log into the search bar, like "ERR_PAYMENT_GATEWAY_TIMEOUT", already knows the identifier they want. For these queries, semantic similarity is exactly what the user doesn't want. Vector embeddings can actively hurt by surfacing semantically adjacent but identifier-distinct documents (the runbook for ERR_PAYMENT_GATEWAY_REJECTED instead of TIMEOUT). Keyword search handles these queries efficiently and correctly.

   Hybrid Queries

   A user searching "rollback runbook for v3.2 deployment" needs a semantic understanding (i.e., a runbook for the deployment-rollback operation) and exact matches on the distinguishing tokens: "v3.2" to pick the right version and "rollback" to distinguish from "rollout". A user searching for "Outlook 2019 sync error 0x80004005 troubleshooting" needs a semantic match on the symptom, plus exact matches on the version and the error code. These queries demand both. In my experience with production RAG systems, they are the majority. The rest of this article is about how to handle them.

   BM25 Provides Precision Where Embeddings Approximate

   Vector search needs a partner and the partner is BM25, the probabilistic ranking function at the heart of classical information retrieval. It is the default scorer in Elasticsearch, OpenSearch, and most lexical search engines, as well as the dominant keyword-search algorithm for the better part of three decades. It succeeds precisely where vector search fails. It relies on probabilistic information retrieval theory with three built-in mechanisms that directly address the exact-match problem.

   Inverse document frequency (IDF) measures how rare a term is across the corpus. Common words like "service" or "deployment" receive low weight, while rare distinguishing tokens like "v3.2", "ERR_PAYMENT_GATEWAY_TIMEOUT" or "payment_v2_enforce" receive high weight. This approach is precisely why BM25 outperforms embeddings on exact-match queries. Rare tokens that distinguish one document from another are the tokens BM25 weights most heavily.

   Term frequency (TF) saturation controls the impact of repeated terms. The first mention of a term significantly impacts the score, but subsequent mentions yield diminishing returns. The score approaches a limit rather than growing linearly. This situation prevents keyword-stuffed documents from gaming the ranking.

   Length normalization addresses another bias in text retrieval. Longer documents tend to score higher simply because they contain more words, giving them more opportunities to match query terms. Length normalization corrects for this scenario by factoring in document length when computing relevance scores, factoring in not just how many times a term appears, but how often relative to the document's length. This point is especially important in RAG systems with variable-length chunks, where larger chunks would consistently outrank smaller ones without this adjustment.

   Hybrid Search with Reciprocal Rank Fusion

   Looking at Figure 3, hybrid retrieval runs BM25 and vector search in parallel, fuses their ranked lists with RRF and optionally reranks with a cross-encoder before passing the top-K chunks to the LLM.

   

   Figure 3. Hybrid retrieval. (Source: created by author)

   At this point, we have two retrievers with complementary strengths, vector search and BM25. Vector search captures semantic meaning, while BM25 matches exact tokens. Each produces its own ranked list. To handle hybrid queries, those two lists need to be combined into one.

   The combination itself is the hard part. Vector cosine similarity is bounded between -1 and 1. BM25 scores are unbounded. Normalizing them onto a common scale is tricky. The correct weights are query-dependent: for one query, the right weight on BM25 might be 0.7, for another 0.3. Calibrating these weights per-query at production scale is impractical. This situation is where Reciprocal Rank Fusion (RRF) helps.

   Deep Dive into How RRF Helps Combine Scores

   RRF sidesteps the normalization problem entirely by ignoring raw scores from either retriever. It operates on rank position alone:

   RRF_Score(d) = Σ 1 / (k + rank_r(d))

   The constant k, which is typically 60 (Cormack, Clarke, and Buettcher 2009), smooths the contribution of each rank position. A document at rank 1 contributes 1/61 ≈ 0.0164. A document at rank 10 contributes 1/70 ≈ 0.0143. A document missing from a retriever's top-K contributes 0 from that retriever.

   The mechanism is straightforward. Documents that both retrievers rank in their top results get the highest fused scores, because they receive non-zero contributions from each. Documents that only one retriever finds get demoted, even if that retriever ranks them at the top. RRF rewards consensus.

   The three tables below walk through this situation on three query types, which include a semantic query, an exact-match query, and a hybrid query. Together they show where RRF clearly wins, where it preserves a correct result with a narrower margin and where the article's argument actually lands.

   When considering the rank columns, each retriever is searching over the full corpus of thousands of documents. The BM25 and Vector ranks shown are positions within those full retrieval outputs, not within the four documents displayed in each table. So a BM25 rank of 12 means the document was the twelfth-ranked result out of the entire corpus.

   All three queries in the walkthrough below are runnable end-to-end against a local Elasticsearch instance. The sample application code and dataset can be found in this GitHub demo.

   A Semantic Query

   Query: "How Does Our Auth System Handle Expired Tokens?"?"

   This is a conceptual question. The right document is a runbook titled "Token refresh and expiration handling in auth service". It shares several query terms ("token", "expiration"/"expired", "handling"/"handle", "auth"), so BM25 does find it, but a less relevant document with higher term frequency on "system" and "token" outranks it on the BM25 side.

   
    
     
      Document
      BM25 Rank
      Vector Rank
      RRF Score
     

     
      Token refresh and expiration handling in auth service
      3
      1
      1/63 + 1/61 = 0.0323
     

     
      OAuth flow design doc
      6
      2
      1/66 + 1/62 = 0.0313
     

     
      System token rotation runbook
      1
      8
      1/61 + 1/68 = 0.0311
     

     
      Auth service architecture overview
      2
      11
      1/62 + 1/71 = 0.0302
     

    
   

   BM25 finds the right document, just not as confidently as it finds System token rotation runbook, which has multiple matches on common terms but is about a different operation. Vector search ranks the right document at the top because it captures the conceptual alignment between the query and the document's content. RRF rewards the document both retrievers rank highly, surfacing it at the top of the fused list. The next two RRF results ("OAuth flow design doc" and "System token rotation runbook") are both reasonable supporting contexts for an LLM consuming this top-K.

   An Exact-Match Query

   Query: "ERR_PAYMENT_GATEWAY_TIMEOUT"

   The user has pasted an error code from a stack trace. BM25 finds the right runbook because the identifier string is unique and matches verbatim. A vector search struggles because the query has minimal semantic content beyond "an error from the payment service", and the embedding model can't reliably distinguish ERR_PAYMENT_GATEWAY_TIMEOUT from sibling error codes in the same service.

   
    
     
      Document
      BM25 Rank
      Vector Rank
      RRF Score
     

     
      Runbook: ERR_PAYMENT_GATEWAY_TIMEOUT (payment-svc)
      1
      6
      1/61 + 1/66 = 0.0316
     

     
      Runbook: ERR_PAYMENT_GATEWAY_REJECTED (payment-svc)
      12
      1
      1/72 + 1/61 = 0.0303
     

     
      Runbook: ERR_PAYMENT_GATEWAY_UNAUTHORIZED (payment-svc)
      15
      2
      1/75 + 1/62 = 0.0295
     

     
      Payment service general error handling guide
      -
      3
      0 + 1/63 = 0.0159
     

    
   

   Considering plausibility, the adjacent error code runbooks appear in BM25 results because related runbooks typically cross-reference each other in their troubleshooting steps ("If you see ERR_PAYMENT_GATEWAY_REJECTED instead, see this runbook"). The query token matches those cross-references. Without those cross-references, BM25 would return only the TIMEOUT runbook itself and the adjacent-runbook rows would be missing from BM25 entirely.

   RRF puts the correct runbook at the top, but the margin over the rejected runbook is narrow and the second and third RRF results are wrong error code runbooks. For a pure-identifier query like this one, BM25 alone produces a cleaner top-K than the hybrid result. BM25's #2 and #3 would be unrelated documents the LLM can ignore, whereas RRF's #2 and #3 are similar-looking error runbooks that risk confusing the LLM about which error code the user actually pasted. This is the honest case where hybrid retrieval is a distribution-level improvement, not a strict improvement on every query.

   A Hybrid Query

   Query: "Rollback Runbook for v3.2 Deployment"

   
    
     
      Document
      BM25 Rank
      Vector Rank
      RRF Score
     

     
      Rollback runbook v3.2 deployment
      1
      3
      1/61 + 1/63 = 0.0323
     

     
      Rollout runbook v3.2 deployment
      4
      1
      1/64 + 1/61 = 0.0320
     

     
      v3.2 deployment postmortem
      6
      2
      1/66 + 1/62 = 0.0313
     

     
      Rollback runbook v3.1 deployment
      2
      7
      1/62 + 1/67 = 0.0311
     

    
   

   BM25 ranks the right document at the top because "rollback" + "v3.2" + "deployment" + "runbook" all match. Vector search ranks the rollout runbook for v3.2 at the top, not because the embedding model believes rollout is more relevant than rollback to a rollback query, but because cosine similarity between the query and the two runbooks is within roughly 0.01 to 0.02 of each other. Which one lands at rank 1 in vector search is closer to noise than signal. On a different day or against a different embedding model, the order could flip.

   That noise-level uncertainty on the most operationally important distinction in the query, which operation the user actually wants to perform, is exactly the failure mode that hybrid retrieval addresses. BM25's preference for the rollback runbook breaks the tie in favor of the operation the user asked for. RRF promotes the document that both retrievers rank within their top three, the correct rollback runbook for v3.2.

   What the Three Queries Demonstrate Together

   Across the three query types, the pattern is consistent. On the semantic query, vector search finds the right document and RRF preserves it at the top while adding a consensus signal from BM25. On the exact-match query, BM25 finds the right document and RRF preserves it at the top, though the runners-up are noisier than they would be with BM25 alone. On the hybrid query, each retriever alone has a different failure mode. BM25's top-1 is correct, but its runner-up is the wrong version. Vector search's top-1 is the wrong operation. RRF's combination produces a top-1 that is correct and a runner-up that is wrong, but related, which is the cleanest of the three.

   In my experience, production query distributions are dominated by the third case. Most real-world queries combine semantic intent with specific identifiers, version numbers, error codes, or other tokens that demand exact matching. Hybrid retrieval is the engineering response to that distribution.

   Hybrid Retrieval in Production

   Production RAG systems have converged on hybrid retrieval. Perplexity fuses lexical and embedding-based scorers across hundreds of billions of URLs on Vespa, with a multi-stage ranking that ends in cross-encoder reranking. Glean layers, lexical retrieval and dense embeddings over a proprietary knowledge graph for enterprise search. Two different domains, the same architectural pattern.

   Production Implementation of Elasticsearch

   Elasticsearch and OpenSearch both support hybrid retrieval natively through the retriever API (Elasticsearch 8.13+ with OpenSearch following). Native support means the fusion happens inside the search engine in a single query, with no application-level merging logic. The examples below use Elasticsearch syntax; OpenSearch syntax is nearly identical.

   Index Mapping

   Your index requires a standard text field for BM25 and a dense vector field for embeddings:

   PUT /rag_knowledge_base
{
  "mappings": {
    "properties": {
      "title":   { "type": "text" },
      "content": { "type": "text", "analyzer": "standard" },
      "content_vector": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}

   Figure 4. Elasticsearch index mapping defining a text field for BM25 alongside a 768-dimensional dense vector field for semantic retrieval.

   Hybrid Query with RRF

   The query structure runs both retrievers and fuses them in a single request:

   POST /rag_knowledge_base/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": { "match": { "content": "rollback runbook for v3.2 deployment" } }
          }
        },
        {
          "knn": {
            "field": "content_vector",
            "query_vector": [0.12, -0.45, ...],
            "k": 50,
            "num_candidates": 100
          }
        }
      ],
      "rank_constant": 60
    }
  }
}

   Figure 5. Hybrid retrieval query using Elasticsearch's RRF retriever to run BM25 and kNN searches in parallel and fuse their rankings in a single request.

   Tuning for Production

   The default configuration above is a reasonable starting point, but production systems almost always need tuning. Three parameters in particular drive most of the relevance and latency tradeoffs you will encounter.

   Rank Constant (k)

   The rank constant is the smoothing parameter in the RRF formula that controls how steeply rank contributions decay; a document at rank r contributes 1/(k + r) to its fused score. The default of 60 works for general-purpose retrieval. Lowering it to 20-30 biases the contribution in favor of top-ranked results, which is useful when BM25 hits are highly precise, like error codes, version strings, or feature flag names. Increasing it to 80-100 flattens the rank contribution curve, favoring documents that appear in both lists over documents that rank highly in just one. The right value depends on whether you want high precision (lower k) or recall (higher k).

   kNN Candidates

   The num_candidates parameter sets how many vectors the HNSW graph traversal explores before returning the top-K, controlling the recall-latency tradeoff in approximate nearest neighbor search. A setting of k=50 with num_candidates=100 is a strong baseline. If you observe that vector search recall is low (relevant documents consistently appear outside the top 50), increasing num_candidates to 200-300 typically improves recall with modest latency impact, since the additional computation happens locally within the vector index rather than as additional network roundtrips.

   Reranking with Cross-Encoders

   Hybrid retrieval with RRF gets you a strong candidate set, but a cross-encoder re-ranking stage can meaningfully improve final relevance. Unlike bi-encoders, which produce embeddings independently for query and document, cross-encoders process the full query-document pair through the transformer jointly, enabling token-level interaction between query terms and document content. This architectural difference is why cross-encoders consistently outperform bi-encoders on relevance: They can model nuanced relationships that independent embeddings cannot capture.

   In practice, the pattern is to have RRF retrieve twenty to fifty candidates, then pass them through a cross-encoder like ms-marco-MiniLM-L-6-v2 for final ordering. Cross-encoders are too slow for first-stage retrieval (they require a forward pass per query-document pair), but for re-ranking a small candidate set, the latency is usually acceptable, typically under one hundred milliseconds for fifty candidates on a GPU. Cross-encoders consistently outperform bi-encoders on standard retrieval benchmarks like BEIR, with larger models showing the largest gains on out-of-domain queries and even lightweight models providing meaningful gains in-domain. For production systems where every percentage point of relevance matters, this final stage is worth the investment.

   Conclusion

   Dense embeddings solve the generalization problem in retrieval since they find conceptually relevant documents even when query terms do not match document terms. BM25 solves the precision problem where it finds exact matches based on rare, distinguishing tokens. But neither alone is sufficient for the production RAG.

   Embeddings are approximation engines, which is their strength and their limitation. Hybrid search with RRF is not a workaround for a temporary gap in model quality; it is the architecturally correct approach for systems that must handle both conceptual and exact-match queries.

   If you are running a RAG pipeline on embeddings alone, you are leaving retrieval quality on the table. Add BM25, fuse with RRF, and consider a cross-encoder re-ranking stage.
