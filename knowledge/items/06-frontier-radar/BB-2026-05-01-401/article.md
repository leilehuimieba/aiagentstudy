# NVIDIA Dynamo Snapshot: Fast Startup for Inference Workloads on Kubernetes

- BestBlogs URL: https://www.bestblogs.dev/article/2c1ca519
- Original publisher URL: https://developer.nvidia.com/blog/nvidia-dynamo-snapshot-fast-startup-for-inference-workloads-on-kubernetes/
- Source: BestBlogs / NVIDIA Technical Blog
- Publish time: 2026-05-28 07:10:20
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 18724

---

The cold-start problem

  In production inference deployments, demand fluctuates over time, requiring inference replicas to scale elastically. However, cold-starting inference workloads on Kubernetes can take several minutes. During that time, GPUs are allocated but idle, generating no tokens and serving no requests.

  This delay increases the risk of service level agreement (SLA) violations during traffic spikes, as the system cannot scale quickly enough to absorb sudden increases in demand.

  For a single-GPU vLLM (v0.20.0) workload, the cold-start latency breaks down as follows:

  
   
    
    
     
      
     
    
    
     Figure 1. Cold-Start Latency Breakdown for a Single-GPU Inference Worker
    
   
  

  To significantly reduce startup time, we are introducing NVIDIA Dynamo Snapshot, our checkpoint/restore approach for AI inference workloads on Kubernetes. In this post, we describe the design choices and optimizations behind our early prototype, which achieves startup times close to the speed of light for single-GPU workloads.

  This is the first post in a series on fast startup in Dynamo.

  CRIU and cuda-checkpoint

  A running inference worker’s checkpointable state has two components:

  
   Device state (GPU-side): CUDA contexts, streams, device memory, virtual address mappings, etc. This is not visible to the host. To serialize this state, we use the checkpointing capability of the CUDA driver (which is also exposed by the cuda-checkpoint command line tool) to dump the device state to CPU memory of the process owning each CUDA context.

   Host state (CPU-side): CPU memory, threads, file descriptors, namespaces, etc. The Linux kernel has all the bookkeeping necessary to be able to serialize this state. We use an open-source tool, CRIU (Checkpoint/Restore in Userspace) to walk the Linux kernel’s bookkeeping and serialize the process tree’s state to disk.

  

  These two tools compose cleanly to allow checkpoint/restore of the full inference worker state. When checkpointing:

  
   cuda-checkpoint dumps all device state into CPU memory.

   CRIU dumps all host-side process tree state to a folder in storage.

  

  When restoring (same or different node):

  
   CRIU restores the process tree according to the serialized state from distributed storage like NFS/SMB, allowing us to fetch the checkpointed artifact from a different node.

   cuda-checkpoint restores the GPU state from what is serialized in CPU memory onto the new GPUs.

  

  CRIU is fundamentally a freeze-and-thaw mechanism. When a process is restored, execution resumes at the exact instruction where it was checkpointed, completely unaware that checkpointing or restoration occurred.

  Because of this, any coordination required before checkpointing, such as quiescing the workload, or after restoration, such as re-establishing external state, must be handled externally through an orchestrator or workload-specific hooks. We describe these mechanisms in the following sections.

  In Kubernetes, workloads run inside containers inside pods. Because CRIU checkpoints contain references to the container’s writable filesystem layer, we checkpoint at the container level so the process tree state and filesystem travel together.

  We provide a privileged DaemonSet, snapshot-agent, installable through a Helm chart. An agent runs on every node and handles checkpoint and restore for runc-managed containers without requiring modifications to runc itself.

  On checkpoint, the agent waits for the workload’s readiness probe, then invokes cuda-checkpoint and CRIU from the host side before writing the artifact to shared storage. The workload may have created/deleted files local to the container (i.e. the overlay filesystem), which the agent also checkpoints after the CRIU stage. 

  On restore, the agent launches a lightweight placeholder pod, restores the overlay filesystem, and restores the CRIU/CUDA checkpoint into its namespaces. The restored worker then takes over execution.

  Each agent operates independently on its local node, allowing checkpoints and restores to parallelize naturally across the cluster. We built this instead of relying on Kubernetes native checkpoint/restore support in runc, which also delegates to CRIU. The DaemonSet approach is fully portable and does not depend on cloud-provider support for checkpoint/restore feature gates.

  It also gives us tighter control over CRIU for performance tuning and allows checkpoint artifacts to live in flexible storage backends instead of being embedded into OCI images.

  
   
    
    
     
      
     
    
    
     Figure 2. Kubernetes checkpoint and restore lifecycle with Dynamo Snapshot
    
   
  

  Dynamo Snapshot: The workload

  A Dynamo inference worker comes up in two phases:

  
   Engine initialization: The configured inference engine is started: communicators are initialized, weights are loaded, kernels are warmed up, graphs are compiled/captured, etc. By the end of this phase the worker is fully warm. It could serve a request, but is not yet discoverable to anything outside its own pod.

   Distributed runtime startup: The worker connects to the Dynamo control plane and registers itself with the discovery backend, so the router and the rest of the graph can find it. From this point on, the worker is “live” — there are open connections to the control plane, and other components in the cluster are aware of this worker’s pod identity.

  

  If we were to implement checkpoint/restore naively, without the workload knowing it was being checkpointed, the readiness probe of the checkpoint job would correspond to a fully initialized distributed runtime that is registered to the discovery plane, which means there are active TCP connections that cannot be captured by CRIU.

  The general pattern that solves this is quiesce/resume hooks: the workload ensures it is in a quiescent state and blocks on an external signal that fires when the restore is complete. This is a powerful abstraction for checkpoint/restore because:

  
   It lets the workload clean up its resources before being checkpointed, which optimizes the final checkpoint size (and thereby decreases restore time).

   It allows the workload to recreate resources that aren’t checkpointable post-resume. This is especially important for multi-GPU and multi-node checkpoints (planned for a future release): outbound TCP connections used for RPC cannot be checkpointed in an established state since the pod IP changes between checkpoint and restore, and RDMA registrations and NIC state also need to be recreated post-restore.

  

  In Dynamo Snapshot, we implement these hooks by defining the readiness probe as the presence of a “ready for checkpoint” signal file. The worker writes this file after the engine initializes but before distributed runtime startup.

  At that point, the worker enters a polling loop waiting for a separate “restore complete” signal file while the snapshot agent checkpoints it externally. The checkpoint can occur at any instruction within that polling loop.

  Because CRIU restores execution at the exact instruction where checkpointing occurred, the worker resumes directly inside the polling loop, detects the signal file, and proceeds with distributed runtime initialization without requiring additional synchronization.

  Optimization #1: KV cache unmap and release

  One optimization to reduce the checkpoint size is to deallocate the KV cache memory before checkpointing. After measuring the peak GPU memory usage while weights, CUDA graphs, and other buffers/activations are allocated, inference engines allocate the remainder of the GPU memory as a large KV cache buffer.

  However, since our checkpoint is taken in a quiescent state before the replica has served any requests, this KV cache buffer does not need to be checkpointed at all. But we need to keep the virtual address of this KV cache stable since it is baked into the CUDA graph. This means we allocate the KV cache buffer via the CUDA Virtual Memory Management API (cuMemCreate and cuMemMap); then deallocating the underlying physical allocation while keeping the virtual address stable is as simple as calling cuMemUnmap and cuMemRelease, but not cuMemAddressFree. Luckily, this functionality is already natively available in vLLM (via sleep() and wake_up()) and SGLang (via torch_memory_saver).

  Unmap and release of the KV cache reduces the total artifact size of Qwen3-0.6B on a B200 from ~190 GiB to ~6 GiB. The wins are most pronounced for large KV cache sizes (i.e. smaller model weights relative to GPU size).

  
   
    
    
     
      
     
    
    
     Figure 3. KV cache unmap and release reduces checkpoint size
    
   
  

  Optimization #2: Speeding up CRIU

  At this point, restore times are still far from acceptable. And or larger models, the restore time actually exceeds that of a cold start, defeating the entire purpose of checkpoint/restore.

  
   
    
    
     
      
     
    
    
     Figure 4. Restore time with upstream CRIU exceeds cold-start time
    
   
  

  The primary reason is, CRIU and cuda-checkpoint do not copy memory at speed-of-light (SOL) speeds. In a Linux process, there are two types of memory: anonymous memory (the heap, stack, etc. of a process) and shared memory (shared between processes). CRIU is responsible for restoring both types of memory, and both become significant bottlenecks for large models. In this section, we outline the optimizations to CRIU that we developed to significantly speed up restoration of process memory.

  Note: These CRIU optimizations are not yet shipped as part of Dynamo Snapshot, and will be available once they have been merged into upstream CRIU.

  Note #2: The overlay filesystem for our benchmarked workloads was very small (<100 MiB) and is negligible in restore timing, so it is omitted.

  Optimization #2.1: Parallel memfd restore

  vLLM’s sleep()/wake_up() path and SGLang’s torch_memory_saver (which we call in the quiesce/resume hooks) move weight-tagged GPU allocations into pinned CPU shadow buffers. This is common practice for high-bandwidth host-to-device/device-to-host (H2D/D2H) memory copies. CUDA backs these allocations with shared anonymous memory, which is then pinned through the NVIDIA driver. Inside the Linux kernel, these appear as memfds: anonymous, RAM-backed files that can be mapped with MAP_SHARED.

  For gpt-oss-120b, these buffers consumed more than 120 GiB, split across many independent 2 GiB-or-smaller buffers. Upstream CRIU restores those buffers serially: it creates one shmem-backed object, resizes it, maps it, reads its contents from the checkpoint image, and only then moves on to the next object.

  We modified CRIU to first enumerate all unique shmem-backed objects, then launch a thread pool to restore them in parallel. Each worker allocates its buffer and reads from the checkpoint independently, allowing restore to use the available storage bandwidth and CPU parallelism instead of processing buffers one at a time.

  Optimization #2.2: Linux native AIO for anonymous memory

  After CRIU has restored the shared resources (files, sockets, shmem objects, memfds, etc.), it still has to fill in each process’s private memory: heap pages, stacks, anonymous mappings, and copy-on-write private file mappings. These pages are not shared; they belong to one process and need to land at the exact virtual addresses they had before checkpoint.

  In upstream CRIU, that fill path is a synchronous preadv loop. The restorer pulls one job from the list, hands it to preadv, and waits. The kernel issues that single read to the storage device, the device DMAs the bytes into the destination VMA pages, and preadv returns. Only then does the restorer move on to the next job. There is exactly one read in flight at any moment, which leaves the storage device idle between requests. A single blocking stream cannot saturate fast NVMe bandwidth, and on network-attached storage each read also pays a round trip before the next one can start.

  
   
    
    
     
      
     
    
    
     Figure 5. Serial preadv Memory Restore (one read in flight at a time)
    
   
  

  We replaced the preadv loop with Linux native AIO. CRIU builds a list of read jobs ahead of time. Each job is an iocb describing a file offset, a byte count, and an iovec pointing at the destination VMA pages. The restorer creates an AIO context, which holds many distinct read transactions simultaneously, allowing the storage device to run them concurrently across its internal channels. The restorer creates an AIO context, submits a batch of iocbs with io_submit, and keeps a window of up to 128 reads in flight. As completions come back via io_getevents, new submissions backfill the window until every job is done.

  
   
    
    
     
      
     
    
    
     Figure 6. Linux Native AIO Memory Restore (up to 128 reads in flight concurrently)
    
   
  

  Direct I/O and the page cache

  Where the storage backend supports it, both anonymous and shared memory reads use O_DIRECT. Restore is mostly a one-pass stream from checkpoint files into destination memory, so caching the input pages in the kernel page cache is usually wasteful. Without direct I/O, a large restore can temporarily fill the page cache with checkpoint data while also allocating the destination shmem pages, increasing memory pressure and evicting useful data for other workloads.

  Even more importantly, Linux native AIO is only truly asynchronous on files opened with O_DIRECT. On filesystems where O_DIRECT is unavailable or unreliable, such as some NFS deployments, restore falls back to buffered I/O with sequential readahead so the kernel still sees a predictable streaming access pattern, but the gains from AIO are significantly reduced.

  Results

  On the same setup, we saw a massive improvement in CRIU restore time, and it is now significantly faster to restore from checkpoint than to cold start an inference worker:

  
   
    
     
      Model
      Checkpoint size
      CRIU (upstream)
      CRIU (AIO)
      CRIU (AIO + parallel memfd)
      Speedup over upstream
      SOL
     

    
    
     
      Qwen3-0.6B
      6.2 GiB
      6.8 s
      2.9 s
      2.4 s
      2.8x
      0.95 s
     

     
      Qwen3-8B
      26 GiB
      24 s
      11 s
      4.7 s
      5.1x
      1.8 s
     

     
      gpt-oss-120b
      129 GiB
      119 s
      54 s
      15 s
      7.9x
      11 s
     

    
   

   
    Table 1. Restore-time comparison for upstream CRIU and optimized restore paths. Linux native AIO and parallel memfd restore significantly reduce restore latency and approach speed-of-light (SOL) performance across model sizes.
   
  
  

  
   
    
    
     
      
     
    
    
     Figure 7. CRIU restore time after Linux native AIO and parallel memfd optimizations
    
   
  

  At this point the CRIU restore time is much closer to SOL, but the end-to-end restore time is still dominated by moving large model weights sequentially from PVC, through host memory, and onto the GPU. This process is fundamentally serial: cuda-checkpoint cannot restore GPU memory until CRIU materializes the weights in host memory. Because these weights dominate the checkpoint size, keeping them inside the CRIU image creates a hard ceiling on restore speeds and blocks faster, direct-to-GPU transfer channels.

  Optimization #3: GPU memory service

  To eliminate this bottleneck, we developed the GPU Memory Service (GMS). GMS uses the CUDA Virtual Memory Management (VMM) API to decouple large model weights from the inference worker’s process lifetime, offloading the majority of the process memory into a separate GMS artifact.

  By removing weights from the core CRIU checkpoint, GMS allows us to perform process state restoration  and weight restoration concurrently utilizing different memory bandwidth channels, rather than serially. Weight restoration can now also use the fastest available paths such as GPUDirect Storage (GDS) or peer-GPU RDMA/NVLink. The CRIU checkpoint is also drastically shrunk, containing only the host-side state of the container’s process tree and a few double-buffered miscellaneous buffers, while the GMS weight artifact now holds the majority of process memory that can be restored much faster.

  
   
    
     
      Model
      CRIU checkpoint size (baseline)
      CRIU checkpoint size (with GMS)
      GMS weight artifact
     

    
    
     
      Qwen3-0.6B
      6.2 GiB
      4.3 GiB
      1.2 GiB
     

     
      Qwen3-8B
      26 GiB
      4.8 GiB
      15 GiB
     

     
      gpt-oss-120B
      129 GiB
      6.7 GiB
      74 GiB
     

    
   

   
    Table 2. Breakdown of checkpoint artifact sizes for each model after decoupling weights into GMS
   
  
  Even with weight restoration going through NFS, we see significant restore time speedup:

  
   
    
    
     
      
     
    
    
     Figure 8. End-to-End Restore Time with GMS Weight Decoupling over NFS. Restore times are measured from a common restore trigger timestamp, excluding container startup time.
    
   
  

  When the weights are restored over another independent channel is where we see the decoupling approach truly shine – weight restoration can complete in parallel, before CRIU restore even completes (assuming a sufficiently fast weight transfer mechanism). Below are results from a proof-of-concept weight restoration backend that stripes the weights across 8 local NVMe SSDs – the restore process completes in under 5 seconds. The final result is a start-time reduction of 21x for gpt-oss-120b.

  
   
    
    
     
      
     
    
    
     Figure 9. Sub-5-second restore with GMS and striped local NVMe SSDs
     

     

     Note: The full architecture and detailed features of GMS that apply to other use cases (such as resiliency) will be described in a subsequent blog post.
    
   
  

  Availability and roadmap

  We now have early proof that fast startup for inference workloads on Kubernetes is practical, and we are working to stabilize the implementation and expand support to a wider range of workloads. Dynamo Snapshot will roll out incrementally over the coming months.

  Today, the experimental release supports single-GPU vLLM and SGLang workloads through the non-GMS checkpoint/restore path.

  We are currently working on integrating the following features:

  
   GMS restore path with pluggable backends (GDS, UCX, etc), currently gated on pending CUDA driver patch

   TensorRT-LLM support

   Multi-GPU and multi-node support via quiesce/resume hooks for PyTorch, NCCL, NIXL, etc.
