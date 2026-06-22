# Architecting Cloud-Native Kafka: From Tiered Storage Towards a Diskless Future

- BestBlogs URL: https://www.bestblogs.dev/article/519d67f3
- Original publisher URL: https://www.infoq.com/articles/architecting-cloud-native-kafka/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-05-26 17:00:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 32046

---

Key Takeaways

    
     Storage disaggregation changes Kafka economics by shifting costs from infrastructure provisioning to cloud API usage, making inefficient consumer access patterns a potentially major source of operational expense.

     When storage costs shift from shared infrastructure to per-request API charges, platform teams need client-level visibility to attribute expenses; without it, a single replay job can produce major bill spikes with little visibility into their origin.

     Kafka's legacy rebalancing protocol made dynamic consumer scaling operationally disruptive because scale events triggered group-wide processing pauses. The next-generation protocol greatly reduces this barrier, making Kubernetes-native autoscaling significantly more practical.

     Multi-tenancy in Kafka has historically forced a costly trade-off: either run a dedicated cluster per team or accept weak isolation on a shared one; virtual clusters propose a middle path that delivers strict tenant boundaries without infrastructure duplication.

     Kafka has traditionally coupled partition count to consumer parallelism. Share Groups break this constraint, letting teams scale consumers independently without costly re-partitioning of topics.

    

   

   Introduction: The Cloud-Native Transition and the "Economic OS"

   To understand the current architectural trajectory of Apache Kafka, it helps to establish what it fundamentally is. Kafka is a distributed event streaming platform designed to publish, subscribe to, store, and process streams of records in real-time. Its evolution is driven by the open-source community through Kafka Improvement Proposals (KIPs) formal design documents that outline major architectural changes and operational features.

   For years, Kafka relied on a strict "shared-nothing" design optimized for bare-metal deployments. It achieved its legendary single-digit millisecond latency by writing sequential, append-only logs directly to local broker disks and serving reads directly from the operating system's page cache. This approach kept latency low and throughput high. However, executing a "lift and shift" of this hardware-bound setup into modern cloud environments introduced punishing new financial realities.

   Consider the modernization journey of Discover Financial Services. Operating out of Riverwoods, Illinois, Discover facilitates millions of daily transactions across its global network. To improve engineering velocity and support data science initiatives, Discover migrated its legacy card settlement environment to a cloud-native architecture built on Apache Kafka as the central event backbone, streaming card-settlement transactions in real time to downstream processing layers including Amazon EMR and Apache Spark for fraud detection and risk scoring. This migration drastically reduced the time required to adopt pricing changes from six months down to just three weeks so that the platform could process four million transaction records in a mere nine minutes (AWS Customer Case Study, AWS re:Invent 2021 Presentation).

   
   Within this modernized stack, Kafka serves a distinct role: its event streaming architecture provides the real-time backbone for risk analysis and fraud detection, continuously feeding downstream models while EMR and Spark handle batch settlement processing.

   However, moving a massive, multitenant platform to the cloud exposes the realities of cloud unit economics. Mirroring transaction data three times across Availability Zones (AZs) creates massive network egress fees. Furthermore, storing petabytes of audit logs or historical event streams on premium cloud block storage rapidly becomes prohibitively expensive.

   To survive the cloud, Kafka is maturing from a strictly hardware-bound system into a highly disaggregated architecture governed by strict financial controls. While this architecture is often referred to as an "economic operating system", the term is not merely a metaphor; it represents a concrete operational reality where platform teams must actively build telemetry-driven chargeback pipelines, enforce cost-aware replay governance workflows, and selectively apply queue semantics to manage highly variable cloud expenses.

   The following decision matrix illustrates how architects should map specific workloads to these evolving capabilities:

   

   Figure 1. Decision matrix for mapping workloads to tiered storage capabilities (Source: author).

   As shown in Figure 1, architects should map specific workloads to these evolving capabilities based on ordering requirements, latency sensitivity, and retention needs.

   Throughout this article, we will thread real-world operational challenges through each architectural evolution from tiered storage to the diskless future showing exactly how architects and platform teams must adapt their deployment strategies.

   Decoupling Compute and Capacity: The Realities of Tiered Storage

   KIP-405: Kafka Tiered Storage alters the broker's relationship with state by dividing data retention into two distinct layers: a latency-optimized local tier utilizing block storage and a capacity-optimized remote tier leveraging object storage, such as Amazon S3. An internal broker component known as the Remote Log Manager acts as an orchestrator, asynchronously moving rolled log segments from the local disk to external storage once they breach specific size or time thresholds.

   Actionable Guidance: When to Enable Tiered Storage

   Platform teams should not enable Kafka Tiered Storage blindly across all clusters. Architects must evaluate the disk-versus-object storage tradeoff based on three factors: retention duration, read patterns, and the cost profile of their current block storage volumes. Clusters that retain data well beyond their active processing window typically more than seven days are the strongest candidates, because the majority of stored data is cold and can be offloaded to object storage at a fraction of the block storage cost. However, clusters with short retention windows or latency-sensitive hot-read patterns may see negligible benefit, or even increased costs from object storage API overhead (refer to request amplification below). Various criteria help determine when the tradeoff is favorable.

   Compliance and Audit Needs

   Your workload requires long retention (e.g., seven-year audit logs for SOX or PCI-DSS compliance). Consider a financial institution storing fifty terabytes of audit logs per Kafka broker on EBS gp3 volumes ($0.08/GB-month, per the AWS EBS pricing page). With a Kafka replication factor of 3, block storage alone costs approximately $12,288 per month per broker (50 TB × 1,024 GB/TB × $0.08 × 3). Offloading cold segments to S3 Standard ($0.023/GB-month, per the AWS S3 pricing page) reduces the retained data cost to roughly $1,178 per month, a savings of approximately ninety percent. For clusters using higher-performance io2 volumes ($0.125/GB-month) with provisioned IOPS, the savings can exceed ninety-three percent. These figures use US East (N. Virginia) list prices as of 2025; actual costs vary by region, negotiated discounts, and retrieval patterns. Readers can verify and customize these estimates using the AWS Pricing Calculator.

   Replay-Heavy Analytics

   Machine learning pipelines and data science teams frequently need to rebuild state stores by scanning years of historical transaction data. Tiered storage serves these reads from the remote tier, isolating the heavy I/O impact from latency-sensitive, real-time transaction processing on the local disks.

   Think Twice for Short Retention Windows

   Your workload is primarily real-time with less than seven days of retention. The added architectural complexity and potential API overhead will not yield a positive return on investment.

   The FinOps Risk: Request Amplification

   While Tiered Storage heavily reduces block storage expenditures, the introduction of cloud object storage APIs creates a severe FinOps risk. Cloud infrastructure providers bill for object storage based not only on gigabytes at rest but also on the volume of API interactions (e.g., charging per thousand GET requests).

   Because Kafka consumers inherently perform sequential fetches, a misconfigured consumer pulling years of history can trigger request amplification, generating thousands of individual S3 GET requests per second and severely spiking the API bill.

   Architectural Action: To reduce request amplification risk, platform engineers should evaluate aligning the consumer's max.partition.fetch.bytes with the broker's remote segment size. The intuition is straightforward: If a consumer's fetch window closely matches the size of a remote object, the broker issues fewer individual GET calls per fetch, reducing both tail latency and API cost exposure. However, this remains an optimization pattern rather than a universal prescription; the actual number of object storage API calls depends on segment size, fetch cadence, consumer parallelism, and access locality.

   Notably, the community recognizes this tuning gap: KIP-1178 proposes introducing a dedicated remote.max.partition.fetch.bytes consumer configuration to decouple remote fetch sizing from local fetch behavior, acknowledging that the current default of 1 MB is misaligned with typical cloud connector chunk sizes of four megabytes. Until KIP-1178 or a similar proposal reaches production, teams should treat fetch-size tuning as an empirical exercise and validate its impact against their specific workload using remote fetch metrics, rather than assuming it will universally eliminate API cost exposure.

   Closing the Visibility Gap: FinOps and Cost Attribution

   Tiered Storage initially left platform engineering teams financially blind. If an internal development team launched a heavy batch job scanning five years of transaction history, the cloud bill spiked — but operators had no way to attribute the cost to a specific application, because traditional Kafka metrics only aggregate data at the broker or topic level. This governance gap is the motivation behind KIP-1267: Tiered Storage Cost Attribution Metrics, which proposes introducing client-level JMX telemetry including metrics such as RemoteFetchBytesPerSec and RemoteFetchRequestsPerSec to activate granular cost attribution per consuming application.

   Important: KIP-1267 is currently under community discussion and has not yet been accepted or merged into an Apache Kafka release. The telemetry pipeline described below using Prometheus to scrape these metrics and Grafana to visualize per-client cost attribution represents the intended architectural pattern once the KIP reaches production, not a capability available in upstream Kafka today. Organizations that need cost attribution before KIP-1267 ships can approximate it using broker-level metrics combined with consumer group lag tracking, though this approach lacks the per-client granularity the KIP proposes.

   KIP-1267 fixes this critical visibility gap. It introduces granular JMX telemetry specifically designed for remote storage operations and ties it directly to the client ID. This enhancement allows operators to properly attribute remote fetch costs to specific consumers for strict chargeback and FinOps governance.

   Implementing a Telemetry-Driven Chargeback Pipeline

   Platform teams must translate these metrics into a concrete governance workflow. Here is a practical implementation path using Prometheus and Grafana:

   
    Metric Exposure and Centralized Scraping

   

   Configure the broker nodes with a Prometheus JMX exporter agent. Define YAML rules to capture the new metrics (e.g., RemoteFetchBytesPerSec and RemoteFetchRequestsPerSec) and expose them via a centralized scraping server.

   
    Cost Attribution Dashboards (PromQL)

   

   Platform engineers can use PromQL in Grafana to build dashboards that calculate the estimated hourly cost per client. Using a multidimensional cost formula, you multiply the egress byte count by the cloud provider's gigabyte transfer rate, and the request count by the API pricing tier:

   # NOTE: Metric names below follow JMX-to-Prometheus naming conventions 
# applied to KIP-1267's proposed metrics (RemoteFetchBytesPerSec,
# RemoteFetchRequestsPerSec). The exact Prometheus metric names depend
# on your JMX exporter mapping configuration. Teams should verify the
# final metric naming against both the accepted KIP specification and
# their exporter setup before applying these queries in production.

# Egress cost component
# Converts bytes/sec rate to GB/hour, then multiplies by provider egress rate
(sum(rate(kafka_server_remote_fetch_bytes_total[1h])) by (client_id)
  * 3600                    # rate is per-second; scale to 1-hour window
  / 1073741824              # convert bytes → gigabytes
  * 0.09)                   # illustrative egress rate verify against your cloud provider
+
# API request cost component
# Converts requests/sec rate to request-count/hour, prices per 1k requests
(sum(rate(kafka_server_remote_fetch_requests_total[1h])) by (client_id)
  * 3600                    # scale to 1-hour window
  / 1000                    # normalize to units of 1,000 requests
  * 0.0004)                 # illustrative S3 GET rate verify against your cloud provider

   
    Rogue Consumer Detection (Alerting)

   

   To enforce cost-aware replay governance, teams should configure Prometheus Alertmanager rules to detect runaway historical scans. For example, if a specific client ID exceeds a predefined threshold (e.g., fifty dollars per hour in remote fetch costs), and alert fires. An automation pipeline can then dynamically invoke the Kafka AdminClient API to apply strict client quotas, throttling the rogue consumer before the monthly invoice arrives.

   Governing Compute: Elasticity and the Next-Generation Consumer

   While governing persistent storage costs is critical, the next phase requires governing compute elasticity. Historically, scaling a Kafka consumer group to handle a burst in traffic was a highly disruptive operational event.

   Under the legacy consumer rebalance protocol, whenever a new consumer instance joined a group, the entire group was forced to halt processing. Every consumer revoked its assigned partitions and waited idly while the group leader recalculated the assignments; a global "stop-the-world" event that severely degraded pipeline throughput.

   The Next-Generation Consumer Rebalance Protocol (KIP-848, General Availability in Kafka 4.0) fundamentally resolves this issue. It shifts the complex assignment logic from thick client-side libraries to the server-side group coordinator. Rebalancing is now executed incrementally and cooperatively. The coordinator instructs Consumer A to revoke a partition, but Consumer B does not acquire it until the revocation is explicitly confirmed. Crucially, neither consumer halts the processing of their other assigned partitions.

   Operational Impact: Safe Kubernetes Autoscaling

   Translating these protocol improvements into deployment decisions fundamentally changes how platform teams manage elasticity. Historically, linking Kubernetes Horizontal Pod Autoscalers (HPA) to Kafka consumer deployments was highly dangerous. Dynamic scaling triggered cascading "rebalance storms" that paralyzed the application. With KIP-848, HPA-based consumer scaling is finally safe, though teams should validate that their specific workload characteristics and lag-metric stability support reliable autoscaling before enabling it in production.

   Rebalance storms are significantly reduced: Server-side coordination (KIP-848) eliminates the stop-the-world pauses that previously made HPA-driven scaling dangerous, though rebalances triggered by broker failures or network partitions still require careful handling for planned scaling events. Platform teams should utilize operators like Kubernetes Event-Driven Autoscaling (KEDA) to scale consumer pods dynamically. By linking the KEDA ScaledObject directly to consumer lag metrics rather than generic CPU utilization, the cluster can elastically expand and contract in direct correlation to the actual backlog.

   To rely on this behavior, minimum version requirements must be strictly adhered to: Brokers must be upgraded to Kafka 4.0 or higher, and client applications must utilize compatible libraries with the group.protocol=consumer configuration explicitly activated.

   Multi-Tenancy at Scale: Virtual Clusters vs. Traditional Isolation

   As enterprise streaming platforms scale, the physical consolidation of clusters becomes an economic necessity. Operating dozens of disparate, isolated Kafka clusters for individual product teams generates massive idle resource waste. KIP-1134 (Virtual Clusters), currently under community discussion and not yet accepted into Apache Kafka, proposes an architectural path toward solving this challenge.

   Most organizations attempt to manage multi-tenancy by enforcing strict topic naming conventions (e.g., domain.entity.event) combined with complex, prefix-based Access Control Lists (ACLs). This approach strains at enterprise scale: managing thousands of bespoke prefix rules across dynamic development teams becomes a configuration burden and prefixing does not natively prevent consumers from accidentally hijacking Consumer Group IDs from other teams.

   KIP-1134 (Virtual Clusters) proposes an alternative model dedicated logical namespaces within a single physical cluster, replacing both weak ACL-based separation and cost-prohibitive cluster-per-team deployments. The design described below reflects the KIP's proposed architecture, not a production-ready capability. Large enterprises acting as internal streaming providers should track this proposal closely and evaluate it as it matures.

   Under the proposed design, virtual entities would map to underlying physical UUIDs, enabling the broker to enforce tenant boundaries at the metadata and namespace level meaning topic names, consumer group IDs, and ACL scopes would be isolated per virtual cluster. Note that the current KIP-1134 proposal focuses primarily on namespace and metadata isolation; storage-level isolation, per-tenant quotas, and scheduling guarantees are not part of the current proposal scope unless later revisions include them.

   For example, a platform team could consolidate eight team-specific Kafka clusters into a single physical deployment, giving compliance, analytics, and fraud detection teams a dedicated virtual namespace where generic topic names like transactions coexist without collision. However, the KIP's current scope focuses primarily on namespace and metadata isolation; whether it extends to storage-level isolation, per-tenant quotas, or scheduling guarantees should be verified against the latest KIP discussion thread before making consolidation decisions.

   Redefining Scalability: Share Groups and Queue Semantics

   Apache Kafka 4.2.0 officially promoted Share Groups (KIP-932) to production-ready status. Traditionally, Kafka tightly coupled a topic's physical partition count directly to its maximum consumer parallelism. If an application required 256 concurrent consumers to handle a massive influx of tasks, the architect had to artificially inflate the partition count to 256, a well-known anti-pattern.

   Share Groups (KIP-932) address this limitation by natively integrating queue-like semantics into the Kafka ecosystem. The number of concurrent consumers is no longer bounded by partition count multiple consumers can process records from a single partition independently, with the broker managing in-flight record tracking and lease-based delivery can concurrently process independent records originating from the exact same physical partition. When a consumer fetches a record, the broker grants it an exclusive acquisition lock for a configurable duration.

   Actionable Guidance: Event Processing vs. Task Distribution

   Practitioners must carefully evaluate when Share Groups should replace traditional partition scaling strategies.

   Task Distribution (Adopt Share Groups)

   For pipelines dispatching promotional emails, resizing independent image uploads, or running background job queues, exact chronological execution order is irrelevant. Here, Share Groups are optimal. If traffic spikes during a retail event, Kubernetes HPA can dynamically scale the consumer deployment to hundreds of pods to burn down the backlog without requiring any physical alterations to the topic's underlying partition topology.

   Event Processing (Retain Classic Groups)

   If a financial data pipeline is sequentially calculating real-time account balances or reconstructing database state via Change Data Capture (CDC), strict chronological ordering is an absolute mandate. Processing an account withdrawal before the preceding deposit violates business logic. Share Groups explicitly sacrifice partition-level ordering guarantees to achieve uncapped horizontal parallelism. For highly ordered event streams, classic consumer groups remain the only correct architectural choice.

   Adoption Risks

   Share Groups (KIP-932) reached production in Kafka 4.2.0, but the broader ecosystem of supporting mechanisms is still evolving. For example, first-class Dead Letter Queue (DLQ) support including automatic routing of unprocessable "poison pill" messages, circuit breaker patterns for DLQ overflow, and standardized error disposition headers is not yet available in upstream Kafka. Community proposals addressing these gaps are under active discussion, but no implementation timeline has been committed. Teams adopting Share Groups for task-distribution workloads today should plan to implement application-level DLQ handling as an interim measure, and monitor the Apache Kafka developer mailing list for updates on DLQ-related KIPs.

   In the interim, teams adopting Share Groups must manually construct application-level mechanisms for the retrieval and archiving of failed messages. Active community work is underway to close this gap: KIP-1191 proposes native Dead Letter Queue routing for Share Groups, while KIP-1316 introduces a circuit breaker mechanism to automatically pause a share group when DLQ overflow thresholds are exceeded, and KIP-1317 enforces mandatory disposition headers for standardized failure tracking on unprocessable records. Teams should monitor these proposals as they mature toward acceptance.

   The Future: The "Diskless" Fork in the Road

   While Tiered Storage addresses capacity limitations, the active write-ahead log remains inextricably bound to expensive local broker disks and subject to the punishing network egress costs of cross-AZ replication. Recognizing that true cloud-native efficiency requires the complete disaggregation of state, the Apache Kafka community officially approved KIP-1150: Diskless Topics.

   Proposed by Aiven, KIP-1150 shifts the durability boundary entirely to cloud object storage. Local broker disks are stripped of their role as the definitive source of truth and are utilized merely as ephemeral caches. Data is pushed directly into the object store as "Shared Log Segments". and a new external Kafka Batch Coordinator assigns definitive offsets.

   The economic potential is significant. By targeting the elimination of cross-AZ replication and block storage spend, Aiven's OpenMessaging Benchmark (OMB) results demonstrated a greater than ninety-four percent infrastructure cost reduction for high-volume ingress workloads though these results reflect a specific benchmark configuration and may not generalize to all production environments. However, the diskless architecture is entering its next phase of community evaluation, and the architectural trade-offs involved mean this is not a simple upgrade but a strategic design choice that requires careful workload-by-workload assessment.

   Actionable Migration Signals: Wait vs. Adopt

   Diskless topics demand immediate architectural foresight. Engineering leadership must implement a rigorous, workload-driven adoption matrix.

   When to Wait (Latency and Data Integrity Constraints)

   Diskless topics should remain strictly experimental for core transactional applications. As of this writing, KIP-1150 remains under active community discussion (KIP-1150 Discussion Thread), and no production-readiness designation has been assigned by the Kafka Project Management Committee. Aiven's own roadmap documentation (KIP-1150 Accepted) confirms that diskless topics are positioned as an evolving capability with unresolved design dependencies, not a production-hardened feature.

   Latency has costs: Bypassing local disk incurs an unavoidable performance tax. P99 end-to-end latencies balloon to approximately 1.5 to 1.6 seconds under the Aiven Open Messaging Benchmark (OMB) configuration; teams should verify these figures against their own workload profiles, because latency will vary with partition count, record size, and throughput rate.

   Garbage collection carries risk: KIP-1150 relies on an "Upload-then-Commit" pattern. Orphaned, invisible segments accumulating in S3 after broker crashes is a known design risk inherent to this pattern not a theoretical concern but a predictable failure mode of any crash-during-upload scenario in object storage architectures. This failure mode is documented in the KIP-1150 mailing list discussion and is a core motivation behind the KIP-1163: Diskless Core proposal. KIP-1163 proposes a periodic reconciliation loop to detect and reclaim orphaned segments, though it remains under community discussion and has not been accepted.

   These orphaned segments silently inflate cloud bills with no native detection mechanism in KIP-1150 itself. KIP-1163: Diskless Core, which is currently under community discussion, proposes a periodic reconciliation loop for safe garbage collection of these orphans. However, KIP-1163 remains an unresolved design dependency; it has not been accepted or implemented in upstream Kafka. The absence of a landed garbage collection mechanism is a current design risk, therefore teams evaluating KIP-1150 today must plan for external monitoring and manual reconciliation processes to detect and purge orphaned segments.

   Data Integrity and Exactly-Once Semantics (EOS):

   A critical unresolved concern within the KIP-1164 design discussion centers on exactly-once semantics. Shifting to a leaderless data plane inherently decentralizes the transaction state machine. If the Diskless Coordinator handles the Last Stable Offset (LSO) calculation for a large number of multiplexed partitions, it risks becoming a severe performance bottleneck — a design risk not yet resolved in the proposal. Without careful design, this architecture could introduce split-brain scenarios or break read_committed isolation.

   One mitigation approach raised during community discussion proposes framing the "_diskless-metadata" topic as an immutable event store. Under this model, the coordinator's embedded SQLite database would act purely as a materialized view (projection) over this event stream, maintaining a continuously updated index of active Producer IDs (PIDs) to dynamically resolve the LSO in O(1) time without scanning unbounded transaction logs. Note that this projection-based SQLite approach originates from the community mailing list discussion and is not part of the formal KIP-1164 specification; its inclusion in the final design remains subject to community consensus. Until these mechanisms are formalized, teams running EOS-sensitive pipelines must treat diskless topics as incompatible with transactional guarantees and wait for the proposal to mature.

   Decide when to adopt high-volume analytics. Architects should actively pilot diskless topics today for latency-tolerant, high-volume workloads, such as aggregating application telemetry, distributed tracing spans, comprehensive audit logging, and massive batch analytics. In these scenarios, trading a latency penalty of 1.6 seconds for a ninety-four percent infrastructure cost reduction is a highly optimal business decision.

   Conclusion

   With production-ready Tiered Storage decoupling retention from disk capacity, server-side consumer rebalancing (KIP-848) enabling safe Kubernetes autoscaling, and Share Groups (KIP-932) unlocking partition-independent parallelism, Kafka has already delivered several foundational pillars of a cloud-native streaming platform. Meanwhile, proposals like KIP-1267 (cost attribution) and KIP-1134 (Virtual Clusters) signal the community's clear intent to address the remaining gaps in financial governance and multi-tenant isolation, though these capabilities are still under active discussion and have not yet reached production.

   The "Economic Operating System" is therefore best understood not as a finished product, but as an emerging architectural pattern, one where cost-awareness, elastic compute, and tenant isolation converge into a unified design philosophy. Where production-ready KIPs exist today, organizations can already construct Prometheus-driven chargeback pipelines, trust Kubernetes autoscalers to absorb traffic spikes, and selectively apply queue semantics to task-distribution workloads.

   For teams prioritizing strict operational stability and upstream data integrity, classic Tiered Storage combined with FinOps governance remains the proven, production-ready path. The diskless proposals (KIP-1150: Diskless Topic Partitions, KIP-1176: Diskless Brokers via Remote-Only Topics, and KIP-1183: Diskless Replication) promise to further redefine the underlying economics of streaming, but their competing designs underscore that the community has not yet converged on a single approach. By carefully mapping workloads to the correct storage and compute paradigms and tracking the maturity of each KIP before adopting it architects can ensure their event-driven architectures withstand both CFO scrutiny and the evolving demands of planetary-scale infrastructure.

   References

   
    Aiven Engineering Blog, "Benchmarking Diskless Topics: Part 1".

    Apache Kafka Confluence, "KIP-405: Kafka Tiered Storage".

    Apache Kafka Confluence, "KIP-1163: Diskless Core".

    Apache Kafka Project Blog, "Apache Kafka 4.2.0 Release Announcement" (February 17, 2026).

    Apache Kafka Confluence, "KIP-1267: Tiered Storage Cost Attribution Metrics".

    Apache Kafka Confluence, "KIP-848: The Next Generation of the Consumer Rebalance Protocol".

    Apache Kafka Confluence, "KIP-1183: Unified Shared Storage".

    Apache Kafka Dev Mailing List, "KIP-1150: Diskless Topics [Discussion Thread]".

    Aiven Engineering Blog, "KIP-1150 Accepted and the Road Ahead".

    Apache Kafka Dev Mailing List, "KIP-1164: Batch Coordinator & Exactly-Once Semantics (EOS) Data Safety" (accessed April 5, 2026).

    AWS Solutions Case Study, "Discover Financial Services Increases Transaction Processing Speed by 66% on AWS".

    Discover Financial Services: Modernizing Card Settlement with Event-Driven Architecture, "Discover Financial Services: Modernizing Card Settlement with Event-Driven Architecture".

    Apache Kafka Confluence, "KIP-1191: Dead-Letter Queues for Share Groups".

    Apache Kafka Confluence, "KIP-1316: Circuit Breaker for Share Group DLQ Overflow".

    Apache Kafka Confluence, "KIP-1317: Mandatory DLQ Disposition Header for Share Groups".

    Apache Kafka Confluence, "KIP-1150: Diskless Topics".

    Apache Kafka Confluence, "KIP-1176: Tiered Storage for Active Log Segment".

    Apache Kafka Confluence, "KIP-1178: Consumer Fetch Configuration for Remote Storage".

    Apache Kafka Confluence, "KIP-1134: Multi-tenancy in Kafka: Virtual Clusters".

    Apache Kafka Confluence, "KIP-932: Queues for Kafka".

    AWS, "Amazon EBS Pricing".

    AWS, "Amazon S3 Pricing".

    AWS, "AWS Pricing Calculator".
