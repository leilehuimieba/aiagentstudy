# Two Misconfigurations That Caused Spark OOM Failures on Kubernetes

- BestBlogs URL: https://www.bestblogs.dev/article/72544a86
- Original publisher URL: https://www.infoq.com/articles/spark-oom-kubernetes-misconfigurations/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-06-03 17:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 24227

---

Key Takeaways

    
     Setting spark.kubernetes.local.dirs.tmpfs=true backs all scratch directories with node RAM, including shuffle spill, which can exhaust node memory within seconds during shuffle-heavy stages.

      A hard podAffinity rule that forces executor co-location concentrates shuffle-time memory pressure on a single node, which can trigger catastrophic out of memory (OOM) failures during shuffle-heavy stages.

     A one gibibyte (1Gi) scratch volume limit is insufficient for any shuffle-heavy job: size tmp-volume and workdir against your actual production shuffle data profile.

     Compound infrastructure misconfigurations often only surface under production-scale load and are easily misdiagnosed as Spark tuning problems like heap undersizing or data skew.

     Cloud migrations change the infrastructure contract your workloads depend on; explicitly validate storage semantics and scheduling behavior before promoting to production

    

   

   Introduction

   Shortly after migrating several Spark batch pipelines from on-premises infrastructure to Azure Kubernetes Service (AKS), we began seeing repeated executor OOM failures in one of our larger jobs. The failures appeared during shuffle stages and initially looked like a typical Spark memory tuning problem. Executor memory was increased, executor counts were adjusted, and the job was restarted multiple times. None of these changes helped. The puzzling part was that the pipeline had been stable for years before the migration.

   The eventual root cause was not a Spark configuration issue at all. Instead, two infrastructure-level settings introduced during the migration interacted in an unexpected way: RAM-backed local scratch directories (spark.kubernetes.local.dirs.tmpfs=true) and a hard podAffinity rule forced all executors onto the same node. Together, these settings caused shuffle spill to consume node memory rather than disk, leading to repeated OOM kills.

   This article documents the investigation, the root cause, and the configuration changes that resolved the issue.

   System Context and Migration Background

   The Pipeline Environment

   Our data platform manages production batch pipelines supporting large-scale aggregation and transformation of transactional data at a major U.S. financial institution. The workloads in question processed an approximately three gigabytes fixed-width flat file daily. The file contained multiple interleaved record layouts requiring multiple parsing passes and unions, making the job far more shuffle-intensive than its three gigabyte input size suggested. On-premises, these pipelines had run reliably for more than three years with stable execution profiles and no comparable OOM pattern.

   AKS Cluster Configuration

   A view of the environment where the incident occurred:

   
    
     
      Parameter
      Before (broken)
      After (fixed)
     

     
      Node RAM
      64GB
      64GB
     

     
      Executors per job
      4
      4
     

     
      Executor memory
      8g → 10g during diagnosis
      10g
     

     
      Dynamic allocation
      Disabled
      Disabled
     

     
      Spark version
      3.4.0
      3.4.0
     

     
      Language
      Scala
      Scala
     

     
      spark.kubernetes.local.dirs.tmpfs
      true ❌
      false ✅
     

     
      spark.sql.shuffle.partitions
      not set (default 200)
      200 (explicitly set)
     

     
      tmp-volume size
      1Gi (RAM-backed) ❌
      10Gi (disk-backed) ✅
     

     
      workdir size
      1Gi (RAM-backed) ❌
      10Gi (disk-backed) ✅
     

     
      Pod placement rule
      podAffinity required ❌
      podAntiAffinity preferred ✅
     

    
   

   Migration Context

   The migration to AKS was part of a broader cloud modernization effort. These workloads were treated as lift-and-shift candidates , with the assumption that matching CPU and RAM would preserve runtime behavior without application changes. That assumption proved incorrect: two infrastructure settings introduced during migration changed how Kubernetes handled executor placement and local storage, and neither was flagged during review.

   Incident Timeline

   Week One Post-Migration

   Initial runs appeared stable. Smaller jobs completed without issue. The first OOM failures appeared in the fixed-width multi-layout batch job during its shuffle-heavy union stages. This job read the same three gigabyte file multiple times with different layout parsers before merging the results.

   Days Two to Three

   OOM failures were initially treated as transient. Jobs were restarted manually and temporarily recovered. The issue was logged as intermittent and attributed to possible resource contention at the cluster level.

   Days Three to Four: First Hypothesis and Heap Misconfiguration

   The initial diagnosis focused on executor heap sizing. We increased spark.executor.memory from eight gigabytes (8g) to ten gigabytes (10g). Failures persisted under load, ruling out simple heap undersizing as the root cause.

   Day Four: Second Hypothesis and Executor Count

   We increased the number of executors to distribute the workload further, which had no meaningful effect; failures continued during shuffle-heavy stages.

   Days Four to Five Kubernetes Pod Placement Investigation

   We checked Kubernetes pod placement using AKS pod logs and Datadog. Datadog’s Kubernetes Node Overview dashboard showed node memory utilization spiking above ninety percent during shuffle stages. Kubernetes events consistently reported:

   
Reason: OOMKilled
Exit Code: 137

   We also observed a clear executor churn pattern in AKS pod logs. Instead of the job completing with the original four executors, it repeatedly replaced OOM-killed executors and eventually reached the fiftieth executor before failing. Datadog node-level memory usage climbed from approximately forty-two gigabytes to over fifty-eight gigabytes within seconds during shuffle stages, immediately preceding each termination event. This was a clear signal that the problem was not heap sizing but node-level memory exhaustion causing the Kubernetes kernel OOM killer to terminate executor processes.

   Day Five: Root Cause Confirmed

   A review of the Spark and Kubernetes configuration revealed that spark.kubernetes.local.dirs.tmpfs had been set to true during migration, causing all local scratch directories, including shuffle spill paths, to be backed by RAM rather than disk. The scratch volumes (tmp-volume and workdir) were also sized at only one gibibyte each, which was far too small for the shuffle data this job generated. On-premises, local disk space had been used for shuffle spill and volumes were appropriately sized. Neither difference had been documented during migration review.

   Day Five: Resolution Deployed

   The podAffinity colocation rule was replaced with podAntiAffinity using preferredDuringSchedulingIgnoredDuringExecution. Also, spark.kubernetes.local.dirs.tmpfs was set to false, and tmp-volume and workdir size limits were increased from one to ten gibibytes. OOM failures stopped immediately. The fix has held for six months with zero recurrence.

   Root Cause Analysis

   Three contributing factors were identified for the failures, which only appeared when the second and third interacted under shuffle-heavy load.

   Factor 1: Shuffle-Driven Memory Pressure in Large Data Jobs

   Large shuffle stages in data-intensive jobs triggered sharp executor memory spikes. This is expected behavior in Spark; shuffle operations require holding intermediate data in memory before spilling to disk. In isolation, this data retention is manageable with appropriate resource configuration. It became catastrophic in combination with the other factors below.

   Although the source file was only about three gigabytes, the repeated parsing passes required by the multi-layout, fixed-width format, the intermediate Spark DataFrame materializations for each layout, the union operations combining them, and the downstream shuffle stages amplified memory pressure well beyond what raw input size would suggest. A three gigabyte input file might seem modest for a 4-executor job (i.e., a Spark cluster configuration with 4 worker processes, each allocated a fixed share of CPU cores and memory, collectively responsible for processing the data in parallel across partitions), but the multi-pass processing amplified the effective working set well beyond raw input size.

   Factor 2: Affinity Misconfiguration Forcing Executor Colocation

   The executor placement rule had effectively become a hard colocation constraint. A podAffinity rule using requiredDuringSchedulingIgnoredDuringExecution was present in the configuration. Rather than distributing executor pods across nodes, it forced them onto the same node. This was not default bin packing behavior; Kubernetes was obeying an explicit hard placement rule.

   Kubernetes scheduling combined with this misconfigured placement rule forced all four executor pods onto the same sixty-four gigabyte node. That concentrated shuffle-time memory and I/O pressure on a single machine. Once tmpfs-backed spill was added to the picture, node memory was exhausted and the kernel OOM killer began terminating executors.

   On-premises, the cluster scheduler had been configured with explicit placement constraints that naturally distributed executors. This constraint was not carried over during migration. We corrected this issue by replacing the colocation behavior with podAntiAffinity using preferredDuringSchedulingIgnoredDuringExecution.

   Factor 3: RAM-Backed Local Scratch Directories (spark.kubernetes.local.dirs.tmpfs=true)

   This was the most impactful misconfiguration. During migration, the Spark configuration included:

   
spark.kubernetes.local.dirs.tmpfs: true

   When this property is set to true, Spark instructs Kubernetes to back all local scratch directories including shuffle spill paths with memory-backed empty directory volumes, i.e. the temporary file system (tmpfs). Instead of spilling shuffle data to disk during large shuffles, Spark wrote everything into node RAM. This behavior is documented in Spark's Kubernetes configuration (see reference [1]), but its interaction with volume size limits and executor colocation is less commonly discussed in operational guidance.

   What made this problem especially severe was the combination of tmpfs-backed storage with very small volume size limits. Refer to the original configuration:

   
# BEFORE (broken config)
volumes:
  - emptyDir:
      sizeLimit: 1Gi
    name: tmp-volume       # RAM-backed, capped at 1Gi
  - emptyDir:
      sizeLimit: 1Gi
    name: workdir          # RAM-backed, capped at 1Gi

   With tmpfs=true, these volumes consumed node RAM rather than disk. At only one gibibyte each, they provided minimal headroom for shuffle spill from a multi-pass, multi-union job processing a three gigabyte fixed-width file. Once shuffle spill exceeded the effective capacity of the RAM-backed local scratch volumes, memory pressure escalated rapidly and executor processes began getting terminated by the kernel OOM killer. The on-premises configuration had tmpfs=false and used disk-backed local storage for shuffle spill. This difference was not caught during the migration review.

   The Compounding Effect

   Alone, each factor was manageable:

   
    Shuffle pressure alone: handled by spill-to-disk

    Colocation alone: increased pressure but not catastrophic with disk spill

    Temporary file system (tmpfs) alone: problematic but distributed executors limit per-node impact

   

   Together, all executors were forced onto one node while their shuffle spill consumed node RAM instead of disk, which rapidly exhausted memory under load and triggered repeated OOM kills.

   Why Pre-Migration Testing Did Not Catch This Issue

   Pre-migration validation used smaller or less shuffle-intensive runs. The combined effect of colocation and RAM-backed spill only surfaces under production-scale workload patterns, full-size input files processed through multiple layout passes and union stages. Smaller test runs completed without issue, giving a false signal of stability. Pre-migration validation must simulate production workload volume in a staging environment; representative samples cannot surface compound infrastructure failures that only manifest at scale.

   The Fixes

   The following diagram illustrates the before and after state for executor placement and storage:

   
BEFORE (broken)
┌──────────────────────────────────────────────────────┐
│                   Node A (64GB RAM)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Executor 1│ │Executor 2│ │Executor 3│ │Executor 4│ │
│  │ shuffle  │ │ shuffle  │ │ shuffle  │ │ shuffle  │ │
│  │spill→RAM │ │spill→RAM │ │spill→RAM │ │spill→RAM │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│       podAffinity: required (all on same node)       │
│       spark.kubernetes.local.dirs.tmpfs: true        │
│       tmp-volume: 1Gi (RAM-backed)                   │
└──────────────────────────────────────────────────────┘
  
Executor memory + tmpfs spill → Node memory exhaustion
  → OOMKilled (Exit 137) → executor churn → job fails


AFTER (fixed)
┌──────────────────┐     ┌──────────────────┐
│     Node A       │     │     Node B       │
│  ┌──────────┐    │     │  ┌──────────┐    │
│  │Executor 1│    │     │  │Executor 3│    │
│  │spill→disk│    │     │  │spill→disk│    │
│  └──────────┘    │     │  └──────────┘    │
│  ┌──────────┐    │     │  ┌──────────┐    │
│  │Executor 2│    │     │  │Executor 4│    │
│  │spill→disk│    │     │  │spill→disk│    │
│  └──────────┘    │     │  └──────────┘    │
└──────────────────┘     └──────────────────┘
  


podAntiAffinity: preferred (spread across nodes)
spark.kubernetes.local.dirs.tmpfs: false
tmp-volume: 10Gi (disk-backed)
Memory pressure distributed → job completes in 1 hour with 4 executors

   Diagram: original work by author, 2026

   Fix 1: Pod Anti-Affinity for Executor Distribution

   We introduced preferredDuringSchedulingIgnoredDuringExecution anti-affinity to spread executors across nodes:

   
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: spark-role
                operator: In
                values:
                  - executor
          topologyKey: kubernetes.io/hostname

   The term, preferred, rather than required was chosen deliberately. It allows colocation when the cluster is under capacity pressure, avoiding job failures due to unschedulable pods, while strongly preferring distribution under normal conditions.

   Fix 2: Disabling tmpfs and Increasing Volume Size Limits

   Two related changes were made together: tmpfs were disabled and volume size limits were increased:

   Disabling tmpfs

   
# BEFORE: RAM-backed local scratch dirs
spark.kubernetes.local.dirs.tmpfs: true

# AFTER: Disk-backed local scratch dirs
spark.kubernetes.local.dirs.tmpfs: false

   Increasing volume size limits

   
# BEFORE: 1Gi RAM-backed volumes
volumes:
  - emptyDir:
      sizeLimit: 1Gi
    name: tmp-volume
  - emptyDir:
      sizeLimit: 1Gi
    name: workdir

# AFTER: 10Gi disk-backed volumes
volumes:
  - emptyDir:
      sizeLimit: 10Gi
    name: tmp-volume
  - emptyDir:
      sizeLimit: 10Gi
    name: workdir

   Setting spark.kubernetes.local.dirs.tmpfs to false instructs Spark to use disk-backed emptyDir volumes for all local scratch directories, including shuffle spill paths. Kubernetes writes the data to node ephemeral storage backed by the node filesystem rather than memory. Increasing the volume size limits from one gibibyte to ten gibibytes was equally important; the original one gibibyte limit was far too small to absorb shuffle spill from a multi-pass, multi-union job, even if it had been disk-backed. Both changes were required together.

   We also validated spark.sql.shuffle.partitions at two hundred, which balanced parallelism appropriately for our workload without generating excessive small shuffle files. We retained the ten gigabyte executor memory setting after the fix, but the storage and scheduling corrections were the decisive changes. Increasing executor memory alone had not resolved the failures.

   Fix 3: Node Memory Headroom Validation

   While nodes were provisioned with sixty-four gigabytes of RAM, OS and kubelet overhead reduced usable memory available to workloads. We validated that executor memory requests plus overhead left sufficient headroom. With four executors now distributed across nodes under the preferred anti-affinity rule, each node hosted at most one to two executors under normal scheduling, keeping peak memory usage well within safe thresholds even during the most shuffle-intensive stages of the multi-layout union job.

   Running kubectl describe node on the Standard_D16a_v4 node confirms the effective memory budget after kubelet and OS overhead:

   
# kubectl describe node (Standard_D16a_v4)
Capacity:
  memory:             65937008Ki   (~62.8 GB)
  ephemeral-storage:  129886128Ki  (~124 GB)
Allocatable:
  memory:             63530608Ki   (~60.6 GB)
  ephemeral-storage:  119703055367 (~111 GB)
 
# kubelet + OS overhead: ~2.3 GB
# 4 executors x 10g = 40 GB executor memory
# Remaining headroom: ~20.6 GB

   Node upgrades to a larger SKU can provide additional headroom, but increase infrastructure cost. The configuration fixes described here resolve the issue on the same node footprint at no additional spend.

   Results

   Before

   
    
     
      Metric
      Value
     

     
      OOM incidents
      Daily failures during shuffle-heavy stages
     

     
      Affected job type
      Fixed-width multi-layout batch job with multiple reads and unions
     

     
      Executor behavior
      Job started with 4 executors; each was OOM-killed and replaced, reaching executor-50 before failing
     

     
      Initial remediation
      Executor memory increase (8g → 10g), executor count increase, manual restarts
     

     
      Time to root cause
      ~3-5 days
     

     
      Node memory at peak
      Spiking above 90% during shuffle stages (Datadog)
     

     
      Kubernetes exit signal
      OOMKilled, Exit Code 137
     

     
      On-call escalations
      Daily
     

    
   

   After

   
    
     
      Metric
      Value
     

     
      OOM incidents
      Zero over six months
     

     
      Executor behavior
      Job completes cleanly with original 4 executors; no replacements, no churn
     

     
      Job completion time
      ~1 hour, stable and predictable
     

     
      Cluster size change
      None; same node pool and footprint
     

     
      On-call escalations
      Zero
     

    
   

   The executor churn pattern is the most telling metric. Before the fix, the cluster was spinning up as many as fifty executors per job run in a futile cycle of OOM-kill and replace — burning cluster resources without making progress. After the fix, the same job was completed in one hour with exactly four executors. No additional infrastructure was required.

   Broader Implications for Cloud-Native Spark

   This incident reflects three patterns that appear repeatedly in cloud migrations of Spark workloads.

   Cloud Storage Semantics Are Not Infrastructure-Neutral

   The spark.kubernetes.local.dirs.tmpfs=true misconfiguration was not an obvious error. The property exists for a reason. RAM-backed scratch directories can improve performance for small working datasets that fit comfortably in memory. The problem was applying it to shuffle spill paths in a job with significant intermediate data, combined with scratch volume size limits of only one gibibyte, which is far too small to absorb any real shuffle load.

   Cloud-native storage abstractions, such as emptyDir, PVCs, and instance storage, have different performance and capacity characteristics than on-premises local disks. Teams migrating Spark workloads should explicitly audit spark.kubernetes.local.dirs.tmpfs, validate scratch volume size limits against expected shuffle data volumes, and confirm behavior under load before production promotion.

   Kubernetes Scheduling Is Not Spark-Aware

   Kubernetes optimizes for general-purpose workload placement, not Spark's shuffle and executor memory behavior. In our case, the problem was amplified by a hard podAffinity rule that forced executor colocation on one node. This was not default scheduler behavior but an explicit misconfigured constraint. Executor placement should be treated as an explicit design choice in every Spark-on-Kubernetes deployment, not left implicit or inherited from unrelated workload patterns.

   Configuration Parity Checklists Are Underused

   The two misconfigurations in this incident were introduced not through deliberate decisions but through omission. Configurations that existed on-premises were simply not carried over. We address this issue with a concrete checklist at the end of the article.

   Spark-on-Kubernetes OOM Prevention Checklist

   This checklist is based on the Spark-on-Kubernetes configuration gaps that caused the OOM failures documented in this article. Use it as a starting point when diagnosing or preventing similar failures in your environment.

   Scheduling

   
    Pod anti-affinity configured for executor pods

    Affinity mode chosen deliberately (preferred vs. required)

    Node pool sizing validated for expected executor distribution

   

   Memory

   
    OS and kubelet overhead accounted for in node memory calculations

    Executor memory requests plus limits leave safe headroom per node

    Peak memory validated under shuffle-heavy load

   

   Storage

   
    spark.kubernetes.local.dirs.tmpfs explicitly set to false (disk-backed scratch directories)

    Local volume size provisioned for peak shuffle spill

    Shuffle spill behavior validated with large dataset runs

    spark.local.dir confirmed to point to disk-backed volumes

   

   Configuration Parity

   
    On-premises scheduler constraints documented and reproduced in cloud

    Storage volume configurations explicitly compared between environments

    Network and I/O configurations validated for cloud topology

   

   Monitoring

   
    Executor OOM kill events alerting configured

    Node memory utilization thresholds set

    Job retry rate monitoring in place

    Shuffle read/write volume tracked per job

   

   Conclusion

   This experience is a reminder that cloud migrations do not just move workloads; they also change the infrastructure contract those workloads depend on. The failures documented here were not caused by application bugs, Spark version changes, or simple heap undersizing. They were caused by two infrastructure settings that silently changed runtime behavior during migration and only interacted destructively under production-scale load.

   The cluster has been stable for six months since. The checklist above is a starting point for teams who would rather not retrace the same path. In financial services, where daily batch pipelines feed downstream consumers and stale data triggers user-reported incidents, these failure patterns carry consequences beyond engineering inconvenience. The storage and scheduling misconfigurations documented here are specific to this Spark-on-Kubernetes deployment, but the underlying dynamic, silent configuration drift that only surfaces under production-scale load, is a pattern worth recognizing in any cloud migration.

   References

   
    "Running Spark on Kubernetes – Spark 3.4.0 Documentation." 2026. Apache.org. 2026.

    "Volumes." n.d. Kubernetes.

    "Assigning Pods to Nodes." n.d. Kubernetes.io.

    schaffererin. 2025. "Best Practices for Storage and Backup – Azure Kubernetes Service." Microsoft.com. October 22, 2025.
