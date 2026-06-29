# 3 Agents. 3 LLMs. 1 Aging GPU: Engineering Parallel Inference on Bare Metal

- BestBlogs URL: https://www.bestblogs.dev/article/0807a4a4
- Original publisher URL: https://towardsdatascience.com/3-agents-3-llms-1-aging-gpu-engineering-parallel-inference-on-bare-metal/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-25 23:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 28710

---

You have three AI agents using three different LLMs. You have one ancient GPU and you are too poor to upgrade. You need to run these agents in parallel, but on this old GPU, exactly one survives and the other two crash. Here is the small C++ daemon that fixes that, and the true story of how they all survive together.

  
  The problem you actually have

  Let me describe a situation with which you can relate very easily.

  You have a few AI agents: Agent A generates the raw code, Agent B actively reviews it for security flaws as it is being written, and Agent C simultaneously drafts the documentation. To achieve a seamless, real-time developer experience without massive lag spikes, all three must be resident in memory at the same time. They each work best with a different small instruct LLM — a SmolLM here, a Qwen there, a small Llama somewhere else. You point them at your machine, which has one very old GPU. You can’t upgrade it this quarter, or this year, or possibly this lifetime (yes, you are that poor!). It is an NVIDIA GTX 1080 with only 8 GB of VRAM, and you have spent years quietly being told that it should still be enough for “small” models.

  So you do the obvious thing. You open three terminals to launch these agents in parallel via three llama-completion processes. And then you wait to see this:

  
   You: “OK, even though the GPU is old, three small models should be working fine.”

   llama-completion (Agent 1, Llama 3.2 1B): “Loading backend. Reserving KV cache up front for n_ctx=172032, n_batch=8192, -ngl 99.” GPU memory jumps to 6,536 MiB out of 8,192.

   You: “Cool. Now Agent 2 — Qwen2 0.5B.”

   llama-completion (Agent 2): “Allocating 1,536 MiB on device 0…” cudaMalloc: “❌ out of memory.”

   llama-completion (Agent 2): “qwen process ended.” 🫡

   You: “Fine. SmolLM2 360M, then. That one is tiny.”

   llama-completion (Agent 3): “Allocating 5,120 MiB on device 0…” cudaMalloc: “❌ out of memory.”

   llama-completion (Agent 3): “smol process ended.”

  

  Your nvidia-smi: still shows only one process at 6,512 MiB. Your three-agent demo: is in fact a one-agent demo with two crash logs.

  If this looks familiar, you are not doing anything wrong. You are doing exactly what every “multi-agent on a single GPU” tutorial tells you to do. The problem is that the tutorial is being optimistic about the silicon. However, don’t worry, I got a solution for you, and that is what this article is about.

  The rest of this article is two things: a one-minute explanation of why the second and third process die, and a small C++ daemon called lmxd that admits all three on the same card without the OOM lottery. There is exactly one prior post you might want as background, Warpgroup-backend, and even that is optional.

  
  Why the 3 LLMs can’t run in parallel (the one-minute version)

  llama.cpp‘s llama-completion (and friends) reserve the KV cache (per-token memory the attention layers use during decoding) for the full configured context window, up front, when the llama_context is created. Yes, it is up front, not as you go type, to ensure the decoding process runs smoothly without any hiccups. With -c 172032 and -ngl 99, the first process happily eats 6,536 MiB / 8,192 MiB of your card before it has decoded a single token, and almost none of that is the model weights. It is the KV reservation.

  At that time, when the second process tries to build its own context and gets exactly this in its log:

  0.00.592.688 E ggml_backend_cuda_buffer_type_alloc_buffer: allocating 1536.00 MiB
              on device 0: cudaMalloc failed: out of memory
0.00.593.132 E llama_init_from_model: failed to initialize the context:
              failed to allocate buffer for kv cache

  This isn’t a bug. It is llama.cpp doing the safe thing for one process: pre-reserve KV so decoding never stalls mid-stream. It happens to be a deeply unsafe thing when three independent processes do it on the same 8 GB card, because the card has no queue and there is no shared accounting. There is only cudaMalloc which becomes literally a coin flip the moment the card is past ~80 % full.

  The fix is not “a better algorithm.” It is the simplest of all: bookkeeping. Someone has to look at the card, decide whether the next agent will actually fit, and refuse the request before the next process tries to allocate. I know, right! Let’s build it. And in case you need help, please find the github repo at the end of this article.

  
  The solution: a small C++ daemon that does the bookkeeping

  We needed a bookkeeper, so let’s build that bookkeeper. lmxd is one long-lived process (about 1,500 lines of C++17 only) that owns the GPU on behalf of the agents. Agents do not spawn their own llama-completion binaries anymore, they just talk to the daemon over a tiny Unix-socket text protocol (HELP, STATUS, LIST, REGISTER, UNREGISTER), and the daemon decides whether the new agent fits, and only then loads the model.

  The whole policy lives in one number: 90 % of the card’s total VRAM, and one rule: admit a new agent only if currently_used + new_estimate ≤ 90 % cap. Everything below is just an honest implementation of that rule.

  The ledger that enforces the cap is small enough to read in one sitting. From src/vram_ledger.cpp:

  bool VramLedger::try_reserve(uint64_t model_table_bytes) {
  // Single critical section covers compare-and-bump so parallel REGISTERs cannot overcommit.
  std::lock_guard<std::mutex> lock(mu_);
  if (!initialized_) {
    return false;
  }
  uint64_t projected = 0;
  if (!add_u64(allocated_bytes_, model_table_bytes, &projected)) {
    return false;
  }
  if (projected > max_vram_bytes_) {
    return false;
  }
  allocated_bytes_ = projected;
  return true;
}

  Only a few lines of real, enforcing policy. Check that the sum doesn’t silently overflow + the projected total stays under the cap, and then only commit. The mutex matters: if two agents call REGISTER at the same time, you cannot have both of them pass the check on stale state and overcommit by a model. I know I speak on behalf of everyone when I say that we have all debugged that race and none of us enjoyed it.

  The handler that decides what to do with an incoming REGISTER line is even shorter — and the order of operations is the whole game. From src/daemon_app.cpp:

  uint64_t v_new = 0;
    if (!table_.lookup(model_key, &v_new)) {
      return std::string("ERR unknown model_key for VRAM table lookup\n");
    }
    if (!ledger_.try_reserve(v_new)) {
      const VramLedger::Snapshot st = ledger_.snapshot();
      std::ostringstream os;
      os << "ERR VRAM_LEDGER_DENY code=CAP ledger_max_bytes=" << st.max_bytes
         << " ledger_allocated_bytes=" << st.allocated_bytes << " requested_table_bytes=" << v_new
         << "\n";
      return os.str();
    }
    std::string lerr;
    if (!llama_.acquire_model(model_key, &lerr)) {
      ledger_.release(v_new);
      return std::string("ERR llama acquire failed: ") + lerr + "\n";
    }
    // Record the agent's per-context slot so subsequent DECODE calls can drive the KV-swap
    // dance via LlamaContextManager. Slot creation is recorded-only -- no context built yet.
    std::string cerr;
    if (!ctx_mgr_.create_slot(agent_id, model_key, &cerr)) {
      // Unwind: release the model refcount + ledger bytes so the failed REGISTER leaves no trace.
      llama_.release_model(model_key);
      ledger_.release(v_new);
      return std::string("ERR ctx_mgr create_slot failed: ") + cerr + "\n";
    }
    agent_to_model_[agent_id] = model_key;
    std::ostringstream os;
    os << "OK registered agent=" << agent_id << " model=" << model_key << "\n";

  AT this point, it’ll be great if we take a few minutes to look at those lines closely. They follow the simple order of operation: look up the byte estimate, reserve in the ledger, then load the model. If the ledger refuses, the daemon returns a structured ERR VRAM_LEDGER_DENY code=CAP line and never touches the GPU. If the ledger accepts but the model load fails for some other reason — disk I/O, corrupt file, whatever — the reservation is released on the same path. Either the agent ends up registered with its bytes booked, or absolutely nothing happens.

  This is probably the bit that goes wrong in almost every “naive” version. If you load the model first and check the budget second, you have already paid the disk I/O for a model you are about to refuse, and you are one race away from successfully loading a model whose bytes you can never charge anywhere. Book before you build. Always.

  The model loader itself is doing one more boring-but-important thing: one process, one llama_backend_init, one refcounted map of GGUF paths to loaded models. From src/llama_single_service.cpp:

  bool LlamaSingleService::acquire_model(const std::string& path, std::string* err_out) {
  // Guard every llama entry point so multi-agent registration never races the runtime.
  std::lock_guard<std::mutex> lock(mu_);

  if (!backend_inited_) {
    // Bring up CPU/GPU backends once; subsequent calls are cheap refcount bumps only.
    llama_backend_init();
    backend_inited_ = true;
  }

  const auto it = models_.find(path);
  if (it != models_.end()) {
    // Reuse an already-mapped GGUF and bump refcount for the new agent tenant.
    it->second.refcount += 1;
    return true;
  }

  // Fresh path: load default params then map weights from disk through llama.cpp parsers.
  llama_model_params params = llama_model_default_params();
  llama_model* model = llama_model_load_from_file(path.c_str(), params);
  if (model == nullptr) {
    if (err_out != nullptr) {
      *err_out = "llama_model_load_from_file failed for path: " + path;
    }
    return false;
  }

  ModelSlot slot{};
  slot.model = model;
  slot.refcount = 1;
  models_.emplace(path, std::move(slot));
  return true;
}

  The daemon calls llama_backend_init exactly once. The naive “three terminals” approach spawns three independent CUDA primary contexts on the same card, each burning hundreds of megabytes in silent driver overhead before a single tensor is even touched. The daemon refuses to do that—one backend per GPU. Furthermore, if two agents request the exact same GGUF, it maps the weights into VRAM just once and simply bumps a reference counter.

  That is the entire system: a number (90 %), an honest ledger, a strict order of operations, and one shared backend. It is not new computer science. It is bookkeeping, written down in C++ and exposed over a Unix socket so a tired engineer at 2 AM can nc -U /tmp/lmxd.sock and just talk to it.

  
  The receipts (i.e., one ugly table and five screenshots)

  The whole demo can be packed in one shell script (although not provided currently in the repo, as I focused on the solution part, not the demo part): that runs the naive stack and the daemon stack back-to-back and dumps the PNG + transcript pairs. Same hardware, same three GGUFs (SmolLM2-360M-Instruct-Q4_K_M, Qwen2-0.5B-Instruct-Q4_K_M, Llama-3.2-1B-Instruct-Q4_K_M — combined ~1.4 GiB on disk, all from the bartowski Hugging Face account), same -ngl 99 -c 172032. The card is an NVIDIA GTX 1080 (8 GB, Pascal), driver 535.309.01, with llama.cpp pinned at tag b9724.

  Track A — three terminals, three llama-completion binaries

  Baseline, before anything: 22 MiB used on the card.

  
   
  
  Launch Llama 3.2 1B first. One process, immediately 6,536 MiB:

  
   
  
  Try to add Qwen2 0.5B. The transcript ends with qwen process ended and a cudaMalloc failed: out of memory while allocating a 1,536 MiB KV buffer:

  
   
  
  Try SmolLM2 360M — the smallest of the three. Same outcome:

  
   
  
  Final score: one process resident, two crash logs. The “three-agent demo” is, in fact, a one-agent demo with two error traces.

  Track B — lmxd admits all three

  Same card. Same three models. Bring up the daemon with a small text table that maps each GGUF to its on-disk size, point it at a --admission-percent 90 budget, and fire three sequential REGISTER lines through nc -U. The final STATUS + LIST exchange is the entire headline of this post:

  
   
  
  Three different small instruct models, three distinct agent ids, 1.58 GB booked against a 7.73 GB ceiling, on the same hardware that gave Track A only one survivor.

  The headline is not “the daemon is faster.” It is the daemon succeeds in placeing three where the naive stack succeeds in only one. And when it eventually does refuse a request, it returns a single wire line — ERR VRAM_LEDGER_DENY code=CAP ledger_max_bytes=... ledger_allocated_bytes=... requested_table_bytes=... — with the exact three numbers an operator needs to debug it. Failure that explains itself is the most beautiful thing, isn’t it?

  Track B continued — registered agents that actually decode

  Admitting agents is only half of the story. If those agents can’t function in parallel, then the entire of this post is lost. The other half is deciding which one gets the live llama_context right now, because at any given millisecond only one of them is multiplying tensors. The daemon ships that half too: per-agent context lifecycle in lmx::LlamaContextManager, real llama.cpp decode in lmx::AgentRuntime, KV-cache eviction to host RAM via lmx::KvSwapHelper on every agent switch, all behind one extra IPC verb — DECODE.

  Same socket. Two registered agents (smol, qwen). We fire three sequential DECODE calls to cycle between them: a cold start, a swap that pages the active agent’s KV cache out to host memory, and a final swap that pages it back into a fresh context. At every step, the wire response explicitly reports exactly what the daemon had to move:

  
   
  
  Three calls, three different KV-swap states, in ~440 ms total wall clock on the same GTX 1080:

  
   
    
     
      Call
      KV_swap_evicted
      KV_swap_restored
      What happened
     

    
    
     
      DECODE smol …
      none
      false
      Cold start. Manager built smol’s llama_context fresh.
     

     
      DECODE qwen …
      smol
      false
      Manager serialized smol’s full context state to a host scratch buffer, freed smol’s context, built qwen’s fresh.
     

     
      DECODE smol …
      qwen
      true
      Manager evicted qwen the same way, then restored smol’s saved KV from host scratch into a brand-new context so the conversation continues.
     

    
   

  
  What’s actually on the GPU at the steady state where both models are registered and DECODEs are flying through:

  
   
  
  926 MiB for two registered small models with a live context — well under the 7.7 GiB budget. The lmxd process is the only CUDA tenant on the card. Suspended agents pay zero VRAM bytes; their KV state lives in host RAM until they get the live slot back. That is how “register many, decode any” stays cheap.

  The shape of one DECODE response, for the wire-level skeptics:

  OK schema=lmx-daemon/1
OK invoke=DECODE agent_id=smol
OK prompt_tokens=4 generated_tokens=24 stopped_on_eos=false
OK elapsed_ms=125.495
OK kv_swap_evicted=qwen kv_swap_restored=true
BEGIN_RESPONSE
 [Weather]. I'm looking forward to seeing you all. I'm [Your Name] and I'm a [Your
END_RESPONSE

  The kv_swap_evicted / kv_swap_restored lines are the entire operational flow. If a DECODE finishes in 125 ms and the line reads kv_swap_restored=true, you know exactly two things: the daemon paid one PCIe round-trip to bring the conversation back, and the agent you just talked to had been suspended (not killed, not OOM’d) before the call.

  
  Honest Confession

  I should confess at this point: I am not a “GPU person” by training. I came up through telecom — 5G with a foot creeping into 6G research — and every “infrastructure” problem in agentic AI keeps looking like something we already solved at the radio layer years ago.

  The very short version: when your phone wants to set up a new call (or a new data session) on a cell, the base station does not just say “sure, you’re on the air.” It runs Connection Admission Control (CAC) — can the cell honor this new session without breaking the SLAs of every session already admitted? If yes, admit. If no, reject at setup with a clear cause code. Never silently drop a live call to make room for a new one.

  Look at this side by side and tell me with a straight face these are different problems:

  
   
    
     
      5G cell tower (Connection Admission Control)
      lmxd on a GPU (VRAM ledger)
     

    
    
     
      Cell capacity = available radio resources
      Device capacity = 90 % of vram_total_bytes
     

     
      Admitted sessions consume known resource budget
      Admitted agents consume known ledger_allocated_bytes
     

     
      New session arrives with an estimated ask
      New agent arrives with table_bytes from the VRAM table
     

     
      Admit iff existing + new ≤ cell budget
      Admit iff allocated + new ≤ ledger_max_bytes
     

     
      Decision is before the bearer is established
      Decision is before any GGUF gets loaded
     

     
      Reject path leaves existing calls unharmed
      Reject path leaves existing agents unharmed
     

     
      Skip CAC → cell collapses, everyone admitted, nobody served
      Skip the ledger → everyone races cudaMalloc, one survives
     

    
   

  
  The MAC scheduler at every cell tower since 3G has been making exactly this call. If you proposed an LTE system where every phone got admitted on arrival and the scheduler “figured it out later,” you would be politely escorted out of the 3GPP meeting. And yet that is exactly what every “spawn three llama-cli processes and hope” demo does on an 8 GB GPU. Same animal in a new zoo.

  
  The last trick — only load the layer you actually need

  Let’s take a moment and think about the numbers. Three agents wanting three different LLMs — say, ~4 GB each, in 4-bit quantization — adds up to ~12 GB on disk. Your card has only 8 GB. Naively loading “all three models, fully resident, all the time” was always going to lose. But that is not what a forward pass actually needs at any one millisecond. A transformer decode step touches one layer at a time. So if you only ever put one transformer layer in VRAM (~1.5 GB), plus the CUDA context (~500 MB), plus the active KV cache chunk, your footprint at any single millisecond never goes above 3–4 GB, and the other 14 GB of weights live in pinned host RAM, waiting their turn.

  The catch is that “waiting their turn” can’t mean “stalling the CUDA cores while we go fetch the next layer over PCIe.” On a GTX 1080’s PCIe 3.0 ×16 (~12 GB/s real-world), reading a single 1.5 GB layer takes ~125 ms. If you wait for it serially, you have built the world’s slowest LLM. The trick — and it is genuinely the only trick — is to make the compute on Layer N overlap with the transfer of Layer N+1, on two different CUDA streams, so by the time the cores finish multiplying you already have the next layer’s weights sitting in a pre-allocated swap slot. Pointer swap. Repeat. Forever.

  One pinned page-locked host arena (cudaHostAlloc), two device-side ping-pong buffers, two CUDA streams, per-layer cudaEvent timings, and the hot loop:

  for (int i = 0; i < cfg_.n_layers; ++i) {
    // Step 1: cudaMemcpyAsync host->device on transfer_stream, then synchronize. No overlap.
    check_cuda("cudaEventRecord(transfer_start.serial)",
               cudaEventRecord(impl_->ev_transfer_start[i], impl_->transfer_stream));
    check_cuda(
        "cudaMemcpyAsync(serial)",
        cudaMemcpyAsync(d_curr, impl_->pool.slot_ptr(static_cast<std::size_t>(i)),
                        cfg_.bytes_per_layer, cudaMemcpyHostToDevice, impl_->transfer_stream));
    check_cuda("cudaEventRecord(transfer_end.serial)",
               cudaEventRecord(impl_->ev_transfer_end[i], impl_->transfer_stream));
    check_cuda("cudaStreamSynchronize(transfer.serial)",
               cudaStreamSynchronize(impl_->transfer_stream));

    // Step 2: launch compute kernel on compute_stream and synchronize before next iter.
    check_cuda("cudaEventRecord(compute_start.serial)",
               cudaEventRecord(impl_->ev_compute_start[i], impl_->compute_stream));
    layer_compute_kernel<<<n_blocks, kBlock, 0, impl_->compute_stream>>>(
        static_cast<const float*>(d_curr), static_cast<float*>(impl_->d_output),
        impl_->elements_per_layer, cfg_.compute_iters);
    check_cuda("kernel launch error (serial)", cudaGetLastError());
    check_cuda("cudaEventRecord(compute_end.serial)",
               cudaEventRecord(impl_->ev_compute_end[i], impl_->compute_stream));
    check_cuda("cudaStreamSynchronize(compute.serial)",
               cudaStreamSynchronize(impl_->compute_stream));
  }

  Stream A (compute) is sweating from all the hard work; Stream B (transfer) is quietly shuttling the next layer in behind its back; nobody on the GPU is ever idle waiting for the bus. The two cudaStreamSynchronize calls are the only true serial points per layer, and on a well-tuned pipeline they are no-ops — Stream B finished its transfer ~30 ms ago and has been waiting for Stream A to catch up.

  A standalone CLI, layer_stream_demo, runs this loop alongside a strictly serial baseline (transfer-then-compute, one stream at a time) on the same hardware, same allocations, same synthetic weights and prints the two wall clocks side by side. On the GTX 1080 reference box at the default config (8 layers × 64 MiB × 64 FMA iters per element), it reports:

  HEADLINE: serial=151.41 ms, overlapped=117.85 ms, savings=22.17%, speedup=1.285x

  Push the configuration toward a bandwidth-bound extreme (--n-layers 16 --bytes-per-layer 67108864 --compute-iters 64), and the savings climb to ~32% (a 1.47× speedup). To be fully transparent, the per-layer kernel tested here is a representative-cost FMA sweep. The honest scope is proving that the asynchronous overlap pattern works on real silicon, not claiming we have rewritten llama.cpp‘s entire decode graph. Swapping this synthetic kernel for a full transformer forward pass is a multi-month undertaking; what this repository ships is the bare-metal C++ primitive that makes that future undertaking possible.

  There is a second half to the trick, owed directly to the architecture of SwarmKV. When you switch from Model 1 to Model 2, the KV cache geometry changes entirely—different head counts, different dimensions, different data types. To survive, the orchestrator must serialize the active KV chunk back to host RAM the moment Model 1’s forward pass retires, freeing VRAM for Model 2.

  It is the exact same llama_state_get_data → host buffer → llama_state_set_data dance, just running between distinct models instead of branches of the same model. We ship this primitive as lmx::KvSwapHelper, a stateless wrapper over llama.cpp‘s state-serialization API. When the context manager executes this on every cross-agent DECODE, it produces the exact kv_swap_evicted and kv_swap_restored logs you saw above. That is what makes those numbers a mechanical reality, not just an aspiration.

  
  How to try it, what’s within scope, and what isn’t

  Okay, now is the time we discuss how you can actually use this solution in your daily life.

  
   
    Link to the github repo: https://github.com/AnubhabBanerjee/VRAM-Conductor

   

  
  I called it “VRAM Conductor” because it acts exactly like a bus conductor during rush hour: it checks the tickets, organizes who gets to board the GPU, and actively tells the next passenger, “Sorry, the bus is full,” before the whole vehicle tips over. Also, my alternate option “Bouncer That Stops Three AI Agents From Stabbing Each Other Over the Last Megabyte of Memory” was too long for a GitHub URL.

  If you want to reproduce this on your own card:

  git clone <repo> && cd <repo-dir>
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DLMX_WITH_LLAMA_CUDA=ON
cmake --build build -j"$(nproc)"

# Standalone overlap demonstration (no model file required):
./build/src/layer_stream_demo

# Daemon. Once it is up, every REGISTER admits, every DECODE runs real llama.cpp with the
# KV-swap dance happening transparently on every agent switch:
./build/src/lmxd --socket /tmp/lmxd.sock --vram-table configs/model_vram.example.txt &
nc -U /tmp/lmxd.sock <<EOF
REGISTER smol	/home/you/models/SmolLM2-360M-Instruct-Q4_K_M.gguf
REGISTER qwen	/home/you/models/Qwen2-0.5B-Instruct-Q4_K_M.gguf
EOF
printf 'DECODE smol 24 Hello, my name is\n'        | nc -U /tmp/lmxd.sock
printf 'DECODE qwen 24 The capital of France is\n' | nc -U /tmp/lmxd.sock
printf 'DECODE smol 24 The weather today is\n'     | nc -U /tmp/lmxd.sock

  Requirements are unsurprising: Linux, CUDA toolkit, NVML, an NVIDIA GPU (Pascal or newer). The daemon needs the GGUF paths in your VRAM table to actually exist; the streaming demo runs on synthetic weights and only needs the toolkit.

  Before anyone reaches for the rocks, the honest list of what this repo does not claim:

  
   LayerStreamer‘s per-layer kernel is a representative-cost FMA sweep, not a real transformer-layer forward pass. Replacing it with one that runs llama.cpp‘s quantized matmul kernels under our stream orchestration requires either reimplementing that matmul stack against a streamed weight pointer or doing surgery on llama.cpp’s graph runner — both are multi-month projects and explicitly out of scope for this repo. What is in scope is the engineering primitive demonstration: pinned host + two CUDA streams + double-buffered swap actually overlap on real silicon, with measured wall-clock savings, on the same card three naïve llama-completion processes can’t even share. The DECODE path does run real llama.cpp end-to-end — it just doesn’t drive the streamer inside the decode loop.

   The single-slot context model serializes agents on the GPU. Only one llama_context is live at a time; the others’ KV is in host RAM. Concurrent decode of two agents at once is not in scope — that needs the LayerStreamer-inside-decode work above, which is the multi-month version of this repo.

   The ledger uses operator-supplied byte estimates (here: exact stat(1) sizes scaled 1.5×). With real decode now in the picture, those estimates need to grow to cover KV cache, activations, and CUDA caching margin more precisely — either as a per-model formula or as online measurement after the first DECODE.

   The daemon samples NVML once at boot, then drifts only via its own try_reserve / release. Live NVML is exposed in STATUS for operators but is not used to detect other processes growing during the daemon’s lifetime. Production stacks would re-sync on a timer.

   One GPU, one process, one client at a time. Multi-GPU placement and high-fanout IPC are out of scope.

  

  None of these change the headline, however.

  
  Wrap

  Let’s be honest: most “multi-agent on one GPU” demos in 2026 aren’t doing clever memory scheduling. They are just throwing three processes at a graphics card, closing their eyes, and hoping things just run magically.

  lmxd isn’t some magical new AI algorithm. It is just a bouncer with a clipboard. It takes connection admission control, a concept older than the first flip phone, and wires it up using a C++ daemon, a strict VRAM ledger, and a shared backend. The result? Three different instruct models politely sharing an 8 GB card instead of fighting to the death over it.

  The takeaway is simple: refusing impossible work is worth more than optimizing possible work. You can have the most advanced speculative decoding and MoE routing in the world, but it won’t save you if you blindly admit a third agent that physically cannot fit in memory. Well-engineered systems verify the budget before they do the work.

  Clone the repo. Run the daemon. Then take a hard look at your own pipelines to see how many are quietly surviving on blind luck. If you came here wondering why throwing three LLMs at an old GPU doesn’t work out of the box, congratulations—you now understand hardware constraints better than most people writing these tutorials.

  Now go yell at your allocator. Lovingly.

  
  The admission screenshots (Track A, 01–04) and the daemon STATUS+LIST panel (05) are direct renders of actual nvidia-smi and lmxd transcripts captured on 2026-06-20. The DECODE-with-KV-swap panel (06) and the steady-state nvidia-smi panel (07) (Both in Track B Continued) come from the lmxd daemon running real llama.cpp decode on the same NVIDIA GTX 1080 on 2026-06-22. Panels 06 and 07 add light syntax coloring at render time — green for the kv_swap_* evidence lines, blue for OK, yellow for $ prompts — to make the swap walk easier to follow. Both are PIL renders of the daemon’s actual stdout.
