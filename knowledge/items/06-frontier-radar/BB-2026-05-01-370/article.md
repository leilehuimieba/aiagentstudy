# [AINews] Founders and Forward Deployed Engineers

- BestBlogs URL: https://www.bestblogs.dev/article/0e141aed
- Original publisher URL: https://www.latent.space/p/ainews-founders-and-forward-deployed
- Source: BestBlogs / Latent.Space
- Publish time: 2026-05-30 09:57:15
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 13337

---

Most people are still digesting the massive Anthropic news from yesterday. 

   We’re taking the opportunity to solicit the leading AI FDE’s in the world for AIE’s new Forward Deployed Engineer track, mirroring similar pushes from both OpenAI DeployCo and Anthropic DeployCo:

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   as well as AIE’s new Founders program, where we are doing our version of the Startup Battlefield, a competitive pitch contest anchored by YCombinator’s Garry Tan and Howie Lu’s $10 Million dollar Hyperagent contest. Sign up (and book hotel!) for details today if you are keen.

   
    
      
      
       
       
        
         
          
           
            
           
          
         
         
          
           
          
         
        

       

      
 
     
    
   

   
    AI News for 5/28/2026-5/29/2026. We checked 12 subreddits, 544 Twitters and no further Discords. AINews’ website lets you search all past issues. As a reminder, AINews is now a section of Latent Space. You can opt in/out of email frequencies!

   

   AI Twitter Recap
    
     
      
       
        
       
      
     

    

   Claude Opus 4.8 Rollout, Benchmark Friction, and API Ergonomics

   
    
     Opus 4.8 landed into a noisy, mixed eval landscape: multiple independent benches converged on “incremental but not dominant.” @arena pushed 200+ frontend/code tests comparing Opus 4.8 against prior Opus variants, Gemini, and GLM; @theo reported CursorBench shows it as more efficient but slightly worse than 4.7 within margin of error; @jerryjliu0 and @llama_index found small gains on tables/layout but regressions on content faithfulness/charts in document parsing; @scaling01 said no progress on ALE-Bench and separately flagged interesting failure modes on LisanBench. On the positive side, @jeremyphoward found 4.8 less over-agentic and more cooperative than 4.7/GPT-5.5 in coding, while @leo_linsky called it a tangible product improvement over prior Anthropic releases.

    

    
     Anthropic also shipped useful platform-level changes: @ClaudeDevs announced mid-conversation system instructions without breaking prompt cache, plus authoritative mid-conversation system-role updates, which matters for long-running agent sessions and cost control. But pricing remains a major complaint: @jeremyphoward argued Anthropic has done little for API affordability, preferring GPT-5.5 partly because subscription/API economics are easier to justify. Overall takeaway: 4.8 looks like a meaningful quality-of-life release for real use, not a clean benchmark reset.

    

   

   Agent Harnesses, Multi-Turn RL Bugs, and the Infrastructure Around Autonomy

   
    
     A subtle but important RL failure mode got called out: @ClementDelangue highlighted a Hugging Face deep-dive on why many tool-using, multi-turn RL training loops are silently broken. The core bug: decoding model output, parsing tool calls, then re-tokenizing the updated conversation can change tokenization, so gradients are applied to sequences the model never actually sampled. The proposed fix is a strict “Token-In, Token-Out” rule: never re-encode sampled tokens; keep a single token buffer across turns. @johnschulman2 reinforced the broader point that renderers are foundational infrastructure between messages and tokens, with failure modes spanning train/test mismatch, caching inefficiency, and prompt injection risk.

    

    
     Harness design is becoming its own optimization discipline: @omarsar0 surfaced work on Effective Feedback Compute (EFC), claiming raw token/tool counts explain agent success poorly while EFC reaches R² up to 0.99, implying harness quality matters more than gross activity. This lines up with productized tuning efforts like @LangChain, where Deep Agents v0.6 makes harness profiles first-class to get strong performance from Qwen/Kimi/DeepSeek at 20x+ lower cost than frontier APIs, and @hwchase17 explicitly framing “different models need different prompts/tools.” @vllm_project shipped native weight syncing APIs and improved pause/resume for async RL, and later added fastokens, a Rust BPE tokenizer to reduce CPU tokenization bottlenecks in long-context/agentic workloads.

    

    
     Debate is shifting from “single vs multi-agent” to where the abstraction pays: @OfirPress argued current multi-agent systems are mostly speedups, not capability unlocks; @scaling01 took the opposite view, expecting swarm-style training to yield better planning and superintelligence-like behavior. Either way, the practical trend is clear: more teams are building around agent observability, traces, and continual improvement loops, e.g. @Vtrivedy10 on mining production traces for SFT/distillation and long-horizon continual learning.

    

   

   Open Models, Local AI, and the OSS Toolchain Tightening Up

   
    
     Local-first and open-weight momentum continues to rise: @LangChain said 1 in 3 AI teams ran an open-weights model in April 2026, up from 1 in 5 nine months earlier; @EpochAIResearch estimated open-weight models now lag frontier proprietary models by about four months. On the toolchain side, @ggerganov launched llama.app, giving llama.cpp an official website, a unified installer, and a single llama entrypoint aimed at easier local deployment and third-party agent integration. @ollama announced OpenJarvis as a local-first personal AI via Ollama, explicitly tied to Stanford/Hazy’s “Intelligence Per Watt” framing.

    

    
     Open infrastructure is getting more enterprise-shaped: @ClementDelangue noted that ~50% of models and datasets on Hugging Face are now private, rising with HF’s storage/buckets offering; this is an important correction to the idea that HF is only public OSS infrastructure. @abidlabs showed Hugging Face Jobs replacing GitHub runners for CPU/serverless GPU CI. @DSPyOSS, @dbreunig, and others shipped a redesigned DSPy docs/front page ahead of a coming 4.0, focused on onboarding into programmable AI systems rather than pure prompting.

    

    
     Licensing and permissiveness are becoming strategic levers: @kimmonismus highlighted NVIDIA moving its four open model families to Linux Foundation OpenMDW-1.1, reducing legal fragmentation across weights/code/docs/data. New permissive data releases also matter: @keshigeyan introduced GPIC, a 100M-pair permissive image corpus plus 1M-pair benchmark for visual generation, with explicit research + commercial usability.

    

   

   Google/OpenAI Product Surface Expands: Managed Agents, Gemini Spark/Omni, and Codex on Windows

   
    
     Google is widening the “managed agent” stack from API to consumer product: @_philschmid showed Managed Agents in the Gemini API: a single API call provisioning a sandboxed Linux environment with code execution, web access, and file I/O. On the consumer side, @GeminiApp rolled out Gemini Spark to U.S. AI Ultra subscribers as a 24/7 personal agent that can operate across a user’s digital ecosystem under direction. Google also kept pushing Gemini Omni multimodal generation/editing demos (example, product thread) and announced Google Flow Agent for creative workflows in video/film production (thread).

    

    
     OpenAI’s Codex is moving closer to a persistent remote dev operator: @OpenAI and @OpenAIDevs added computer use on Windows, including remote steering from the ChatGPT mobile app. Follow-on UX improvements included stable identicons for background agents and search across prior chat content (@OpenAIDevs); @reach_vb summarized broader Codex updates around Windows control, mobile remote access, and profile/task stats. Separately, OpenAI updated gpt-5.5 instant to improve sycophancy, factuality, and multilingual performance per @michpokrass.

    

    
     This all points to more vertically integrated agent stacks: model + harness + sandbox + UI + remote control + pricing/quotas. Google is smoothing quotas on Gemini (@joshwoodward); OpenAI is expanding Codex’s operating surface; Cursor added auto-review mode with subagent-based approval routing (tweet). The common pattern is less “chatbot,” more managed execution environment with policy and memory.

    

   

   Research and Systems Papers Worth Attention

   
    
     Search, retrieval, and memory: @TheTuringPost highlighted Bidirectional Evolutionary Search (BES) from Harvard/MIT, combining forward search with backward decomposition and evolutionary operators; reported gains include Llama-3.2-3B-Instruct on MuSiQue from 4.0% to 7.0%. In retrieval, @_reachsumit pointed to Latent Terms, showing sparse BM25-ready features can be extracted from frozen dense retrievers via SAEs. @topk_io open-sourced Iso-ModernColBERT for more efficient late-interaction inference.

    

    
     Continual learning and belief/state management: @HuggingPapers summarized BeliefTrack, claiming optimized belief-state management cuts long-horizon reasoning failures by 70%+. @AndrewLampinen argued the continual learning field over-focused on interference instead of positive transfer; @victor207755822 presented a second DeliAutoResearch SKILL paper focused on self-iteration and CL.

    

    
     Multimodal/world models/robotics: NVIDIA-affiliated work included γ-World, a generative multi-agent world model streaming at 24 FPS (tweet), and minWM, a real-time interactive video world model framework (tweet). In robotics, @_akhaliq shared Qwen-VLA, and @inventorOli demoed Robostral’s language-following and manipulation improvements. For always-on proactive agents, @dair_ai surfaced work replacing LLM wake-up decisions with a 220MiB temporal-graph encoder, gaining +16.7 mean F1 while running 4–83x faster.

    

   

   Top tweets (by engagement)

   
    
     OpenAI / biology: @OpenAI on Rosalind Biodefense announced trusted-access biology tooling for public health and biodefense.

    

    
     Google / consumer agents: @GeminiApp on Spark rolled out its always-on personal agent to AI Ultra users in the U.S.

    

    
     OpenAI / dev tools: @OpenAI on Codex Windows support and @OpenAIDevs expanded computer use to Windows plus mobile remote steering.

    

    
     llama.cpp UX milestone: @ggerganov launched llama.app with a unified installer and CLI entrypoint for local AI.

    

    
     HF / RL correctness: @ClementDelangue amplified the Token-In, Token-Out warning for multi-turn RL with tools.

    

    
     Open vs closed timing gap: @EpochAIResearch estimated open-weight models are now about 4 months behind the frontier.

    

   

   AI Reddit Recap
    
     
      
       
        
       
      
     

    

   /r/LocalLlama + /r/localLLM Recap
    
     
      
       
        
       
      
     

    

   1. Local LLM Performance: MoE Releases, Quants, VRAM Savings
    
     
      
       
        
       
      
     

    

   
    
     StepFun 3.7 Flash (Activity: 637): StepFun released Step 3.7 Flash, a multimodal MoE with 196B total parameters, 11B active, and a built-in 1.8B ViT, advertised for high-throughput agent workflows up to 400 TPS and reportedly runnable locally with ~128GB RAM. Reported benchmarks position it unusually strongly for a flash-class/local model: SWE-Bench Pro 56.26%, DeepSearchQA F1 92.82%, HLE w/tools 47.2, plus large gains over Step 3.5 Flash on Terminal-Bench, Toolathlon, ClawEval, and other agentic/tool-use tasks. Direct model artifacts are available on Hugging Face in BF16, FP8, NVFP4, and GGUF, with day-0 llama.cpp support PR and related MTP work in llama.cpp#23274. Commenters characterize the model as technically odd: its hidden/thinking traces are described as nearly incoherent, but final answers can be “perfect” and competitive with much larger >1TB models; one user says the prior Step 3.5 “infinite thinking” issue appears fixed. There is cautious enthusiasm around local deployment, especially for users with 4x3090-class hardware, and appreciation that StepFun upstreamed llama.cpp support instead of only maintaining a fork.

     
      
       StepFun released multiple Step-3.7-Flash checkpoints on Hugging Face: BF16 (Step-3.7-Flash), FP8 (Step-3.7-Flash-FP8), NVFP4 (Step-3.7-Flash-NVFP4), and GGUF (Step-3.7-Flash-GGUF). One user reports the prior Step 3.5 Flash “infinite thinking” issue appears fixed, making 3.7 more usable despite still having an odd intermediate reasoning style.

      

      
       There is day-0 llama.cpp enablement via StepFun’s upstream PR: ggml-org/llama.cpp#23845, contrasting with Step 3.5’s fork-based support. A separate community PR for MTP support exists at ggml-org/llama.cpp#23274, though commenters note it needs updating for Step 3.7 and current master.

      

      
       A vLLM nightly test of the NVFP4 checkpoint on 2x Pro 6k with 64 concurrent shallow-context requests reached about 2200 tok/s. The reported config used tensor-parallel-size 2, --enable-expert-parallel, --quantization modelopt, --kv-cache-dtype fp8, --reasoning-parser step3p5, and StepFun tool-call parsing; vLLM reported GPU KV cache size 1,667,645 tokens and max concurrency 6.36x for 262,144 tokens/request.
