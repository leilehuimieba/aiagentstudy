# DynoSim: Simulating the Pareto Frontier

- BestBlogs URL: https://www.bestblogs.dev/article/aeb68360
- Original publisher URL: https://developer.nvidia.com/blog/dynosim-simulating-the-pareto-frontier/
- Source: BestBlogs / NVIDIA Technical Blog
- Publish time: 2026-05-30 06:31:38
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 14908

---

Modern LLM serving is hard to tune because each deployment is a stack of interacting choices: model backend, tensor-parallel shape, prefill/decode split, worker counts, scheduler settings, routing policy, KV cache behavior, autoscaling thresholds, and topology. Those choices interact across layers, and a local improvement can shift the bottleneck somewhere else. For larger models, even one realistic experiment can require many GPUs or nodes before we learn whether the idea was worth testing.

  That is the motivation for DynoSim: a Dynamo twin.

  DynoSim is a workload-driven discrete-event simulation of the NVIDIA Dynamo serving stack. It combines measured engine forward-pass timing, Mocker scheduler cores, Router, and Planner behavior, KV cache effects and workload traces on one virtual timeline. The goal is not a purely analytical estimate and not a bit-exact hardware emulator. The goal is a faithful serving simulation at the atomic level of forward passes, while extending up to the full inference stack, which for us is Dynamo (and for many others as well).

  Not only is DynoSim faithful, it is also blazingly fast as a full-stack Rust implementation. On an Apple M4 MacBook Air, the single-threaded Rust offline replay simulated the full 23,608-request Mooncake trace with eight round-robin workers and 512-token trace and engine blocks in 2.41 seconds of wall time. The simulated serving window was 60.1 minutes, about 1,500x faster than real time. 

  
   
    
    
     
      
     
    
    
     Figure 1. DynoSim turns exhaustive deployment search into a fast simulate-then-verify loop, screening thousands of candidates before spending GPU time
    
   
  

  With DynoSim a sweep can map the Pareto frontier for a workload on existing hardware, while an autoresearch-style workflow can propose algorithmic changes to our components: a better Router cost function, Planner heuristic, or cache policy.

  Architecture: Composing Dynamo as events

  A key design choice is composition. DynoSim is not one monolithic model; it is a set of serving components that run on the same simulated timeline. A replay harness drives workload arrivals, single-engine simulations model worker-local scheduling and forward-pass timing, and multi-engine simulations add the system behaviors that only exist across workers: routing, distributed caching, and Planner decisions. 

  
   
    
    
     
      
     
    
    
     Figure 2. DynoSim composes workload replay, engine simulations, Router, Planner, and optional KVBM behavior on a single discrete-event timeline.
    
   
  

  Replay on a virtual clock

  Discrete-event simulation, or DES, gives DynoSim a virtual clock and an event queue. Components do not wait in real time. Instead, they schedule future events with modeled durations: a request arrival, a scheduler step, a forward pass, a KV transfer, a worker startup, or a Planner action. The runtime jumps to the next timestamp, updates system state, and lets the affected components schedule more work.

  A request’s journey through the twin

  
   A load generator, such as Dynamo AIPerf, emits a request from a trace or synthetic workload.

   The router decides where the request should go, or whether it should wait.

   The selected engine scheduler batches the request into a prefill or decode pass.

   Hardware-informed timing, such as timing backed by AI Configurator (AIC), estimates the duration of that pass.

   KV handoff, cache, or offload-related events may be scheduled on the same virtual timeline.

   Decode produces visible output tokens.

   The trace collector records request-level and system-level metrics.

  

  The important part is that every component decision changes future events. A router decision affects the worker’s queue, a Planner scaling decision delays capacity, and a KV movement decision can change when decode begins.

  Replay harness: Driving the twin

  The replay harness connects workload generation to the simulated components and then back to metrics. For fixed traces, arrivals can be scheduled directly from the trace. For feedback-driven workloads, such as multi-turn or agentic traffic, the harness can wait for completions before issuing follow-up requests. The trace collector records throughput, TTFT, TPOT, end-to-end latency, prefix cache reuse, and other request-level or system-level metrics from the simulated timeline.

  Single engine simulation: Scheduler fidelity matters

  A single engine is not just a tokens-per-second estimate. The scheduler decides which requests enter each pass, how prefill and decode work are batched, and how KV pressure changes progress. DynoSim keeps that backend-specific: the vLLM path models a waiting/running scheduler with shared token budget and preemption/recompute, while the SGLang path models radix-cache-aware admission, chunked-prefill budgets, and prefix-preserving decode retraction.

  AIConfigurator (AIC) fits into this picture as engine-side timing: given the model, backend, system, tensor-parallel shape, and pass shape, it estimates how long prefill or decode work should take. The scheduler simulation decides what each pass contains; AIC estimates the duration of that chosen pass. AIC informs pass speed, while the mocker/replay scheduler models the serving behavior around the pass.

  The figure below shows why that scheduler layer matters. AIC gives strong fidelity to real silicon for engine-side performance, especially for throughput and token time. But TTFT is sensitive to how requests wait, batch, chunk, and enter prefill under high concurrency.

  
   
    
    
     
      
     
    
    
     Figure 3. Scheduler-aware replay closes the gap between engine timing estimates and hardware measurements. The model tested is MiniMax-M2.5 FP8 on NVIDIA HGX B200, with TP=4, ISL=1K, OSL=1K, at concurrencies from 8 to 64.
    
   
  

  Multi engine simulation: From workers to systems

  The power of Dynamo comes from components that make online decisions from active system feedback. A Router needs the current cache state and decode load. The Planner needs traffic, worker state, and SLA signals. KVBM needs transfer pressure, tier capacity, and future cache availability. Multi-engine simulation models those feedback loops with the same timestamp-ordered event queue. Each component observes the current simulated state and schedules future decisions or completions back into that queue.

  For the concrete Router and KVBM results below, we use the same baseline replay setup unless noted otherwise: the full 23,608-request Mooncake FAST25 toolagent trace, MiniMax-M2.5 FP8 on NVIDIA HGX B200, vLLM 0.14.0 timing from AIC, TP=4, and offline replay. The Router experiment composes eight aggregated workers; the KVBM experiment uses one worker and toggles the G2 host-memory tier.

  The figure below compares round-robin routing with the KV Router. G2 offload is disabled, so the difference comes from routing and cache placement:

  
   
    
    
     
      
     
    
    
     Figure 4. KV-aware routing improves prefix reuse from about 0.38 to 0.44-0.45, reducing TTFT and lifting throughput compared with round-robin placement across the concurrency sweep, though cache-affine placement can increase decode pressure at high concurrency as reflected in TPOT and TPS/user.
    
   
  

  KVBM manages KV blocks across the serving memory hierarchy: local HBM, host memory, SSD, and distributed or remote cache. Local lower-tier cache behavior can often be modeled as timing and resource pressure: G1 (GPU memory), G2 (host memory), transfer bandwidth, tier capacity, and eventually G3 (disk). Distributed cache is where the simulation becomes more interesting. Offload, onboard, remote read, and placement decisions affect routing, scheduling, queueing, and future cache state, so they need to be registered as events on the same timeline as the rest of the serving harness.

  The KVBM example below shows what the mocker predicts when the G2 host-memory tier is enabled and sized at 32,768 blocks:

  
   
    
    
     
      
     
    
    
     Figure 5. Enabling the KVBM G2 host-memory tier reduces prefill recompute by reusing KV blocks that would otherwise be rebuilt, lowering TTFT across the sweep and shifting the throughput-interactivity Pareto curve upward, with the largest gain at c=32 where mean TTFT improves by 19.3%.
    
   
  

  In the future, Replay can also drive NIXL (NVIDIA Inference tranXfer Library) reads and writes against a real distributed cache target. Those measurements calibrate transfer cost, placement behavior, and contention, then feed back into the distributed cache model.

  Optimization and discovery with DynoSim

  Once DynoSim can run a workload through composed components, replay becomes a scoring function for both optimization and discovery: propose a layout or policy, run the workload, collect metrics, and compare the result against the objective or hypothesis.

  Systematic optimization via Replay

  The optimizer today uses a crude but practical block-coordinate descent over the deployment knobs: choose a TP shape, choose a worker split for that TP shape, then choose the router setting. That works because the current search space is still small and locally smooth enough for coarse coordinate search to find useful candidates. As the search space grows, the same replay scoring loop can be connected to richer black-box optimizers such as Hyperopt-style Bayesian search, genetic algorithms, or Vizier.

  More interestingly, the replay loop is not limited to structured knobs. In the style of Karpathy’s autoresearch, an agentic harness can propose a nontrivial code change, rebuild Dynamo, rerun the same trace, and keep only changes that improve the objective. That turns replay into a bounded research loop for router cost functions, Planner heuristics, and cache policies that are awkward to express as a small parameter grid.

  Discovery examples Beyond the current optimizer

  The same simulation loop can be used for research, not just configuration search. Some experiments tune exposed parameters. Others change the algorithm itself.

  Here we focus the in-depth discovery example on the Planner. Autoscaling fits DynoSim for two reasons. First, the interesting behavior is macro: it emerges from minutes of traffic, delayed worker startup, capacity churn, and feedback between scale decisions, queues, and routing — none of which a small unit test can exercise faithfully. Second, evaluating it the other way — in a full Kubernetes setup — is expensive per policy change, both in GPU-hours and in engineer time. DynoSim lets us aggressively sweep those effects before standing up the full environment: compare static vs dynamic setups, tune Planner parameters, and quantify how much worker startup time matters before deciding whether faster startup, predictive scaling, or pre-warmed capacity is worth the engineering.

  The three experiments below reuse the Mooncake FAST25 toolagent trace introduced above, but switch the simulated engine profile to Qwen3-32B at TP=2 on H200-SXM.

  Experiment 1 setup tradeoffs: We compare static deployments and dynamic deployment with planner using aggregated engines. We sweep static replica counts (no planner; fixed deployments with different number of engine replicas) and overlay one planner run setting SLA to TTFT=1500 ms and ITL=50 ms.

  
   
    
    
     
      
     
    
    
     Figure 6. SLA-targeted Planner finds a better cost-latency operating point than static deployment.
    
   
  

  The dynamic deployment with planner reaches a much better cost-latency point: its p90 TTFT and ITL are far lower than any static deployments while using less GPU-hours at the same time.

  Experiment 2 scaling interval: We sweep the scaling interval from 1 second to 300 seconds, with engine startup set to instant, to see the tradeoff between reacting quickly to traffic changes and scaling too often.

  
   
    
    
     
      
     
    
    
     Figure 7. Load adjustment works best around 5-10 seconds, balancing responsiveness and scaling churn.
    
   
  

  P90 TTFT stays about the same from 1-10 second intervals, but scaling events drop sharply from 1,529 to 233. After about 30 seconds, the Planner reacts too slowly to bursts. GPU-hours stay roughly steady across the sweep, so very short intervals do not cost much more GPU time, but they do cause unnecessary scaling churn. The best range is around 5-10 seconds. 

  Experiment 3 cold-start time: On a real cluster, adding capacity takes time because a new engine pod needs seconds to minutes before it can serve traffic. In the simulation, we model that delay and measure how well the Planner handles it.

  
   
    
    
     
      
     
    
    
     Figure 8. Startup delay produces an SLA cliff once new capacity arrives too late to absorb bursts.
    
   
  

  For Qwen3-32B at TP=2, the Planner meets the SLA until startup delay reaches about 180 seconds. Around 200 seconds, performance drops sharply, and by 300 seconds the system is stuck behind the traffic burst, with p90 TTFT reaching 242 seconds. This suggests users should optimize cold start time to stay below 200 seconds for best performance. 

  These three experiments illustrate how the design space can be explored cheaply. 

  Simulation as the inner loop

  The goal is not to replace real-cluster validation. The goal is to make that validation more focused.

  
   
    
    
     
      
     
    
    
     Figure 9. DynoSim makes simulation the inner loop for deployment tuning: sweep broadly, shortlist Pareto candidates, verify on the cluster, then calibrate from telemetry.
    
   
  

  Simulation becomes the inner loop for design exploration. Real clusters remain the outer loop for validation. Between those loops, Dynamo can test serving algorithms as a system: scheduler behavior, routing policy, Planner control, KV/cache movement, workload shape, and measured engine timing.

  Looking forward, we plan to close this loop in production as well. A smart sweeping algorithm built on top of DynoSim would run periodically against recently-recorded production traffic, search the configuration space under the current workload distribution, and recommend (or directly apply) a reconfiguration when a materially better deployment is found. Because traffic shape drifts over hours and days – different prompt mixes, ISL/OSL distributions, or burst patterns – what was the right TP shape, prefill/decode split, router policy, and Planner setting last week may no longer be optimal today. A continuous DynoSim-driven sweep keeps the live deployment tracking the current optimum instead of relying on a one-shot launch decision.

  Related guides

  
   Mocker trace replay

   Profiler guide

   Router guide

   Planner guide

   KVBM guide
