# How CockroachDB Built Vector Indexing at Scale

- BestBlogs URL: https://www.bestblogs.dev/article/155cf24c
- Original publisher URL: https://blog.bytebytego.com/p/how-cockroachdb-built-vector-indexing
- Source: BestBlogs / ByteByteGo Newsletter
- Publish time: 2026-05-25 23:30:38
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 17803

---

The CockroachDB team wanted to add vector search to their distributed database, and dozens of well-known algorithms already existed.

   To facilitate the decision-making process, they wrote down a list of architectural requirements, including a refusal to depend on any central coordinator, a refusal to allocate large in-memory caches, a need for real-time updates, an intolerance for hot spots, and a requirement to support sharding. Then they checked the list against the popular options.

   Most failed at least one requirement, and some failed several. The team’s response was to build something new, called C-SPANN, that satisfied every constraint by treating the index as ordinary table data inside CockroachDB rather than as a separate system.

   In this article, we will look at how the CockroachDB engineering team built this index and the challenges they faced.

   Disclaimer: This post is based on publicly shared details from the CockroachDB Engineering Team. Please comment if you notice any inaccuracies.

   Vectors and Approximate Nearest Neighbor Search
    
     
      
       
        
       
      
     

    

   A vector is a long list of numbers that captures the meaning of something.

   Modern neural networks like the ones behind ChatGPT can take an image, a document, or a snippet of audio and convert it into a vector of floating-point numbers, typically a few hundred to a few thousand dimensions long.

   The useful property of these vectors, often called embeddings, is that similar things produce similar vectors. For example, two photos of beaches end up close to each other in this multi-dimensional space, and a photo of a beach and the word “beach” end up in roughly the same neighborhood, which is what makes semantic search possible.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   The trick is finding those neighbors quickly when you have billions of vectors to search through.

   Traditional database indexes work because numbers and strings have a natural ordering. We can sort them, store them in a B-tree, and walk that tree to find what you want.

   Vectors do not have that property. Should beach photos come before or after food photos? What about photos of food at the beach? There is no answer, because the data has no inherent sequence, which means a B-tree cannot help you.

   The brute-force alternative is to compare your query vector against every stored vector and return the closest matches. This works fine for a few thousand vectors, but falls apart somewhere in the tens of thousands, and becomes hopeless once you reach the millions.

   Vector indexes solve this by giving up on exact answers. They find approximate nearest neighbors, accepting a small loss of accuracy in exchange for orders of magnitude better performance. The results are usually close enough that real users cannot tell the difference, and the search runs fast enough to feel instant. That tradeoff between accuracy and speed is the foundation of every vector index, and the interesting engineering question is how you make the rest of the system work around it.

   Even with a good algorithm for finding nearest neighbors, plugging it into a distributed transactional database is its own problem. That is where the CockroachDB story actually begins.

   Architectural Constraints in a Distributed SQL Database
    
     
      
       
        
       
      
     

    

   CockroachDB is a distributed SQL database. This means that the data lives across multiple machines, often across regions, and the system is designed to scale linearly. It guarantees transactional consistency and supports real-time updates, and all of this has to keep working when machines die, disks fail, or networks partition.

   These properties impose a set of architectural constraints on any new feature, and a vector index is no exception. The CockroachDB team wrote down six requirements that any candidate algorithm had to satisfy.

   
    
     The first requirement is that no single node can act as a central coordinator. Any node in the cluster should be able to serve reads and writes, because relying on a single leader to direct traffic creates a bottleneck and a single point of failure.

    

    
     The second requirement is that the index cannot rely on large in-memory structures. Index state has to live in persistent storage, since the team could not assume every node has gigabytes of RAM available for caching vectors. They also wanted to avoid the long warm-up times that come with rebuilding in-memory caches after a restart, which matters especially for serverless deployments where nodes spin up and down on demand.

    

    
     The third requirement is that network hops have to stay minimal. Round-trips between nodes are expensive, and any algorithm that requires sequential traversal across the cluster will accumulate latency unpredictably.

    

    
     The fourth requirement is that the index data layout has to be sharding-compatible. Index data has to map naturally to CockroachDB’s key-value storage so that it can be split, merged, and rebalanced like any other table.

    

    
     The fifth requirement is that the index must avoid creating hot spots. As inserts and queries scale up, the load has to spread across the cluster, because concentrating traffic on a single node defeats the point of running a distributed system in the first place.

    

    
     The sixth requirement is that the index has to support incremental updates. Inserts and deletes need to be applied in real time without blocking queries, requiring batch rebuilds, or degrading search quality over time.

    

    

   

   This list rules out the most popular vector indexes.

   HNSW, the graph-based algorithm that powers pgvector, Weaviate, and many other systems, is excellent on accuracy benchmarks but builds its graph in memory and resists sharding. Classic IVF is closer in spirit but assumes a single-node deployment and struggles with dynamic updates. Specialized vector databases like Pinecone solve these problems by being separate systems entirely, which works fine if you are willing to keep your vectors in one database and your transactional data in another.

   CockroachDB needed something that handled both inside the same system, with the same guarantees.

   Faced with this list, the team built something new. They called it C-SPANN, and the design choices that make it work are mostly about what it does not try to do.

   The C-SPANN Architecture
    
     
      
       
        
       
      
     

    

   C-SPANN borrows ideas from three places.

   Microsoft’s SPANN paper contributed the tree structure for partitioning vectors, the follow-up SPFresh paper contributed techniques for incremental updates, and Google’s ScaNN project contributed ideas around quantization.

   The CockroachDB team combined these with their distributed SQL architecture to produce something none of the source papers describe directly.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   At the core is a hierarchical K-means tree. Vectors are grouped into partitions based on similarity, where each partition typically contains dozens to hundreds of vectors and has a centroid that represents the average of the vectors it contains. Think of the centroid as the partition’s center of mass. Those centroids are themselves grouped into higher-level partitions with their own centroids, and that process repeats until you reach a single root partition at the top.

   The result is a wide, shallow tree. With a fanout of around 100, an index of one million vectors needs only three levels, and an index of ten billion vectors needs only five. Searching the tree means starting at the root, comparing the query vector to the centroids at that level, descending into the closest partition, and repeating until you reach the leaves. At each level, partitions can be processed in parallel, which keeps latency low and predictable. At the leaves, the system scans a few hundred candidate vectors using SIMD CPU instructions for speed.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   That much describes the algorithm. The interesting part is what happens to the data structure once it is built.

   Each partition is stored as a self-contained set of key-value rows inside CockroachDB. Partition data lives in CockroachDB ranges, which are the same units of storage that hold every other table in the database. Therefore, the index is not a parallel structure attached to the database. It is table data with extra meaning.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   This decision pays dividends. CockroachDB already knows how to split a range when it grows too large, how to rebalance ranges across nodes when load shifts, and how to cache frequently accessed rows in its block cache.

   All of this setup applies to vector index data automatically, without writing a single line of new infrastructure code. When a new node joins the cluster, ranges containing index partitions get distributed to it the same way ranges containing user tables do. When a node restarts, the index is immediately ready to serve queries because it lives on disk, rather than in some warm-up cache that has to be rebuilt.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   However, building the index is one thing. Keeping it healthy as data flows in and out is harder, especially when the index needs to be compressed aggressively to stay affordable.

   Index Maintenance, Quantization, and Multi-Tenant Partitioning
    
     
      
       
        
       
      
     

    

   A K-means tree is not static. Partitions grow as vectors are inserted and shrink as vectors are deleted, so the system needs background machinery to keep partitions at a reasonable size and to keep vectors grouped with their nearest centroids.

   When a partition grows too large, C-SPANN splits it. A balanced variant of the K-means algorithm divides the vectors into two roughly equal groups, each with its own new centroid, and the tree is updated so that future inserts route to whichever new partition is closer. When a partition shrinks too small, the system merges it away and reassigns its vectors to neighboring partitions. Both operations happen in the background to avoid interfering with foreground transactions.

   There is one point worth noting.

   After a split, some vectors in the original partition might actually be closer to a neighboring partition’s centroid than to either of the two new centroids, and they get reassigned. Likewise, a vector in a neighboring partition might now be closer to one of the new centroids and migrate in. This idea, called nearest partition assignment, comes from the SPFresh paper and is what keeps the index accurate over time.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   The consequence is that you can start with an empty table, insert millions of vectors, and end up with an accurate, well-balanced index without ever rebuilding it. The maintenance setup handles everything incrementally.

   The other operational factor is size. An OpenAI embedding has 1,536 dimensions stored as 2-byte floats, which works out to about 3 KB per vector. A billion vectors at full precision is 3 TB just for the embeddings, before any indexing overhead is counted. Storing and scanning that much data is expensive both in disk space and in the CPU and memory used during search.

   C-SPANN compresses vectors using a technique called RaBitQ, which reduces each dimension to a single bit. The compressed representation is roughly 200 bytes per vector, a 94 percent size reduction. The math behind the compression involves a random orthogonal transform that preserves distances while spreading data evenly across dimensions

   What matters for the system is that quantization is lossy, so distance estimates from compressed vectors are only approximate. C-SPANN compensates with a reranking step, where the system scans quantized vectors to assemble a candidate set, then fetches the original full-precision vectors for those candidates to compute exact distances. By fetching candidates, the system can absorb quantization error and still return accurate results. The pattern of cheap approximate filtering followed by precise refinement on a small candidate set shows up in many other systems too, and recognizing it here makes it easier to spot elsewhere.

   The third operational reality is multi-tenancy. In most real applications, vectors belong to someone, whether a user, a customer, or an organization, and most queries are scoped to a single owner. Mixing one user’s vectors with another’s during search is wasteful, and it is also a security problem.

   CockroachDB handles this through prefix columns on the vector index. Here is what the schema looks like.

   
    
     
      CREATE TABLE photos (
  id UUID PRIMARY KEY,
  user_id UUID,
  embedding VECTOR(1536),
  VECTOR INDEX (user_id, embedding)
);

     

     
      
       
        
       
      

      
       
        
       
      

     
    

   

   A query for one user’s nearest matches uses pgvector-compatible syntax.

   
    
     
      SELECT id
FROM photos
WHERE user_id = $1
ORDER BY embedding <-> $2
LIMIT 10;

     

     
      
       
        
       
      

      
       
        
       
      

     
    

   

   Behind the scenes, the index maintains a separate K-means tree for each distinct user. Performance scales with how many vectors the user owns, rather than with the total size of the index, so a billion vectors split across a million users behaves, from any one user’s perspective, like a million-vector index.

   Combined with CockroachDB’s REGIONAL BY ROW tables, prefix columns can also partition the index by geography. For example, a user in Europe gets their data and their index entries stored in a European region, with fast local access and compliance with data domiciling requirements, while the same table serves a US user with equally low latency from US infrastructure. The combination of region, ownership, and embedding as prefix columns produces an index that is efficient, secure, and locality-aware by default.

   Conclusion
    
     
      
       
        
       
      
     

    

   C-SPANN refused several compromises that most vector databases quietly accept.

   Freshness in CockroachDB is real-time and transactional rather than batched or eventually consistent, which means a vector inserted in a transaction becomes searchable as soon as that transaction commits, with the same consistency guarantees as any other write. Scaling is native to the distributed architecture rather than a feature retrofitted onto a single-node system, and vectors live alongside transactional data in the same database, inside the same queries, under the same operational umbrella. Since the index lives on disk, nodes serve queries immediately after a restart without any warm-up phase.

   In return, the team accepted some real limitations. The 25.2 release is a preview, and several optimizations are still being built, including fuller SIMD usage, root partition caching, and complete merge support. The current implementation supports only Euclidean distance, with cosine and inner product on the roadmap. Filtering on non-prefix columns is limited today, though that scope is expanding. Also, on raw vector search benchmarks against specialized in-memory systems, C-SPANN does not win on pure latency.

   The tradeoff suggests where this design fits and where it does not. CockroachDB’s vector index is a strong choice for applications where vectors and transactional data need to coexist, where multi-tenant isolation matters, and where multi-region deployment with data domiciling is a requirement. Specialized vector databases remain a better fit for pure vector workloads with no transactional component, for read-heavy batch-updated datasets where freshness is not a concern, and for cases where every microsecond of search latency is critical.

   The architectural logic underneath all of this is worth keeping in mind. The CockroachDB team treated the vector index as ordinary table data and inherited their existing distributed machinery for free, so splits, caching, sharding, replication, and multi-region behavior all worked from day one because they already worked for everything else in the database. The algorithm is the part that gets the headlines, but the integration is what makes the system possible.

   References:

   
    
     Real-Time Indexing for Billions of Vectors: How we built fast, fresh vector indexing at scale in CockroachDB

    

    
     Vector databases
