# Pinterest Uses Content Fingerprints for URL Deduplication Across Millions of Domains

- BestBlogs URL: https://www.bestblogs.dev/article/a3d45d78
- Original publisher URL: https://www.infoq.com/news/2026/06/pinterest-miqps-url-dedup/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-06-08 22:37:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 3815

---

Pinterest engineers have developed a URL normalization system called Minimal Important Query Param Set (MIQPS) to improve content deduplication across its large-scale ingestion pipeline. The system is used to determine which URL query parameters affect page identity and should be retained, and which are considered non-essential and can be safely removed. The goal is to reduce duplicate-content processing across millions of domains while maintaining the accuracy of ingested data.

   The system is used within Pinterest's content ingestion infrastructure, which processes URLs from a wide variety of merchant and publisher websites. Many of these URLs point to the same underlying page but differ due to tracking parameters, campaign identifiers, session tokens, and other query string variations. Although downstream systems can eventually detect duplicates, each URL variant still incurs separate fetch, render, and indexing costs, increasing infrastructure overhead at scale.

   

   Multiple URLs with different query parameters all point to the same underlying product (Source: Pinterest Blog Post)

   Shanhai Liao, a Software Engineer at Pinterest, highlighted the scale of the problem in a LinkedIn post.

   
    This is the kind of problem that sounds trivial until you're operating at Pinterest scale, across millions of merchant domains with wildly different URL conventions. Static allowlists work for the top platforms. For the long tail, we needed something smarter.

   

   To address this, MIQPS replaces traditional rule-based URL normalization approaches that rely on manually maintained allowlists, denylists, or domain-specific heuristics. These approaches are difficult to scale across a long tail of heterogeneous domains with inconsistent URL structures. Instead, MIQPS uses a data-driven approach that evaluates whether removing a query parameter changes the rendered content of a page. If content changes exceed a defined threshold, the parameter is classified as important and retained; otherwise, it is considered noise and removed during normalization.

   The system operates by first collecting a large corpus of URLs from Pinterest's ingestion pipelines and grouping them based on query parameter patterns. It then renders pages and generates content fingerprints to compare the effect of removing individual parameters. This allows the system to infer parameter importance based on observed content behavior rather than predefined rules or metadata such as canonical tags. Pinterest noted that canonical tags are often missing, inconsistent, or polluted with tracking parameters, making them unreliable for large-scale deduplication.

   

   End-to-end system architecture (Source: Pinterest Blog Post)

   MIQPS uses a small set of tunable parameters that control mismatch thresholds and minimum sample sizes. To improve efficiency, it applies early exit logic that stops evaluation once mismatch rates exceed a threshold after limited tests, avoiding unnecessary page renders. It also uses a conservative default that treats parameters as non-neutral when data is insufficient. The output is a parameter importance map stored in a configuration service and applied at runtime alongside static rules. MIQPS is protected by anomaly detection that rejects updates where important parameters are downgraded, while safely allowing additions to the non-neutral set.

   The architecture separates offline analysis from runtime processing. Expensive content rendering and parameter evaluation are performed offline, while runtime systems apply precomputed rules during URL processing. Pinterest stated that URL structures tend to evolve slowly, making offline computation a practical tradeoff between freshness, cost, and operational complexity for large-scale ingestion systems.
