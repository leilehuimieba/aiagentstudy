# A Guide to AI Cold Starts on Cloud Run

- BestBlogs URL: https://www.bestblogs.dev/article/de02b525
- Original publisher URL: https://cloud.google.com/blog/topics/developers-practitioners/a-guide-to-ai-cold-starts-on-cloud-run/
- Source: BestBlogs / Google Cloud Blog
- Publish time: 2026-05-28 08:00:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 13699

---

I saw a developer asking on Reddit if there was any “sane way” to manage Cloud Run cold starts for AI across multiple regions. They were experiencing startup latencies of up to 20 seconds, a frustrating gap where the infrastructure is spinning up while the user waits for a response.

    The discussion was full of developers who had almost given up on serverless GPUs, with some even migrating back to GKE just to escape the latency. I decided it was time to dive deep into the Mechanics of AI Cold Starts and see if we could find that "sane way."

    During my research into hosting models like Gemma 4 on Cloud Run, I had the privilege of co-presenting at Google Cloud Next '26 with Oded Shahar (Senior Engineering Manager for Cloud Run) and our guest speaker Ajay Nair (Global VP of Platform at Elastic). 

    In our session, "Build AI architectures with custom models on Cloud Run," Ajay shared the production-hardened strategies that allow Elastic to serve millions of daily requests across 17+ model variants, all while maintaining the 'scale-to-zero' efficiency of Cloud Run. 

   

  

  
   
    
     
      
      

     

     
      
     

    

    
     Build AI architectures with custom models on Cloud Run

    

   

  

  
   
    Ajay showed us that the secret isn't just in the model, but in treating GPUs as fungible compute rather than infrastructure to manage.

    I realized then that minimizing cold start latency isn't just about the model, it's about the infrastructure patterns and architectural decisions that keep it fast, scalable, and secure.

    The anatomy of an AI cold start

    As the official Google Cloud GPU best practices explain, an AI cold start is a shift from standard web microservices. You aren't just booting code, you're moving gigabytes of weights into a specialized physical accelerator.

    Think of it as a four-phase race. If you don't optimize each step, you're going to lose your users.

    Phase 1: Infrastructure Provisioning (~5s)

    Cloud Run allocates the physical GPU and injects pre-installed NVIDIA drivers. Since Google manages the drivers for you, you don't have to bloat your Dockerfile.

    Phase 2: Block-Level Container Image Streaming (1-2s)

    Cloud Run uses "image streaming," meaning it pulls only the blocks needed to boot. Your 15GB CUDA image can actually start as fast as a tiny Node.js app!

    Phase 3: Engine Initialization (5-15s)

    This is where your inference engine (vLLM, Ollama) warms up. This is a massive CPU-heavy task, and it's where most people get throttled without realizing it.

    Phase 4: Model Loading & VRAM Transfer 

    This is the final hurdle - moving those model weights from storage into the GPU memory. Unlike standard web apps where CPU is king, GPU memory is your primary constraint here. If your model’s weights don’t fit entirely within the GPU memory, performance degrades significantly as it swaps to slower system RAM.

    Best practices to handling AI cold starts

    To build a "sane" production environment, here are a few crucial levers you can pull, informed by the official Google Cloud documentation on AI inference with GPUs.

    Optimize Phase 4

    Pick the Right Deployment Option

    Phase 4 is the "final hurdle" where you move gigabytes of weights from storage into GPU memory. Your choice of storage determines how fast this transfer happens:

    
     
      Cloud Storage (Concurrent Download) - Fastest: Using the Google Cloud CLI (gcloud storage cp)  allows you to download model files in parallel. This is the recommended method for massive weights because it maximizes network throughput and drastically reduces transfer time. 

     

     
      Cloud Storage (FUSE) - Easiest: This provides "zero-code" changes by mounting a bucket as a local file system. However, because it does not parallelize the initial download, it is significantly slower for large model weights

     

     
      Container Image - Best for <10GB: Baking weights into your image is efficient for smaller models thanks to Cloud Run's Image Streaming. For models over 10GB, however, the import and streaming overhead can become a bottleneck.

     

     
      Internet: Avoid this. It is the slowest and least predictable path for production inference.

     

    

    Model Format & Size

    Optimizing your model's format and size is a direct "hack" to shorten Phase 4 (Model Loading & VRAM Transfer). Because this phase is constrained by how fast you can move gigabytes of data into VRAM, smaller and more efficient files are critical.

    
     
       4-bit Quantization: This is the ultimate cold start hack. Smaller weights mean fewer gigabytes to pull from storage, which directly accelerates the download and transfer portion of Phase 4,

     

     
      Fast Formats: Pick a model format with fast load times like GGUF to minimize startup time. For the fastest performance, move away from Python "pickle" files and use Safetensors for zero-copy loading.

     

     
      Ensure VRAM Fit: Use quantized models to ensure the weights fit entirely within the GPU memory. If the model exceeds VRAM, Phase 4 will stall as the system swaps to significantly slower RAM. 

     

    

    Optimize Phases 3 & 4: Infrastructure & Network Levers

    These infrastructure settings provide the necessary resources to accelerate the most demanding parts of the startup process.

    Startup CPU Boost (Accelerates Phase 3)  

    This feature temporarily doubles your CPU power during startup. A 1 vCPU instance boosts to 2 vCPUs for the duration of startup and the first 10 seconds of serving. It is essential for Phase 3, as engine initialization is a massive CPU-heavy task.

    Direct VPC Egress & PGA (Accelerates Phase 4) 

    Utilizing Direct VPC Egress with Private Google Access (PGA) ensures your model weight traffic stays on Google’s internal high-speed backbone. This optimizes the network path to shorten the time spent moving gigabytes of weights into VRAM.

    Concurrency Tuning (Cold Start Avoidance): 

    In Cloud Run, "concurrency" refers to the maximum number of requests a single instance can handle before the platform scales out to start a new one. For AI workloads, you must tune this setting in tandem with your model engine's internal parallelism flags (e.g., --max-num-seqs  for vLLM or OLLAMA_NUM_PARALLEL for Ollama). 

    Use the official Google Cloud formula to find your ideal Cloud Run concurrency:

    (Number of model instances∗parallel queries per model)+(number of model instances∗ideal batch size)

    Example: If your instance loads 3 model instances onto the GPU, and each model instance can handle 4 parallel queries with an ideal batch size of 4, you would set your Cloud Run maximum concurrent requests to 24: (3×4)+(3×4)

    How the math works: The goal is to keep the GPU fully saturated while ensuring users aren't stuck in a long queue. In this example, the total of 24 concurrent requests is split into two functional groups:

    
     
      Active Processing (12 requests): Calculated as (3 instances×4 queries), this represents the total number of requests the GPU can actively process at any given moment.

     

     
      The "Next Batch" Buffer (12 requests): Calculated as (3 instances×4 batch size), these are the requests waiting "on deck" inside the container. As soon as the GPU finishes the first batch, it immediately picks up these waiting requests.

     

    

    By tuning this value as high as your VRAM allows (usually 10-20 users), one warm instance can serve many requests without triggering a new scale-out event and the cold start that comes with it.

    Scaling Controls (Tuning the Threshold)

    While the formula above defines your maximum capacity, you can also tune when Cloud Run decides to start the next instance. Cloud Run's autoscaler typically targets 60% utilization, but for long-running AI cold starts, you can increase this threshold to 80% or 90% via Scaling Controls.

    
     
      Concurrency Target: Increasing this allows you to "pack" more requests into a single warm instance before triggering a scale-out.

     

     
      CPU Target: Increasing the CPU target prevents the platform from starting a new instance just because initialization or high-intensity inference spiked the CPU utilization.

     

    

    Scaling & Reliability Strategies

   

  

  
   
    
     
      
       
      

     
     
      
       Sometimes the best way to handle a cold start is to avoid it entirely or manage it proactively.

      

     

    

   

  

  
   
    The Single-Region "Always-On" Tradeoff

    If you are deploying globally, the cost of keeping minimum instances set to 1 in every region adds up. Instead, consider an 'always-on' service in just one region. A 100ms global network delay is a much better user experience than a 20s local cold start.

    The 15-Minute Grace Period: A common question is 'How long will my instance stay warm after a request?' Cloud Run generally keeps instances alive for 15 minutes after they become idle (processing zero requests). If your traffic is predictable and comes in every 10–12 minutes, you might not even need an 'always-on' service, the platform’s default shutdown policy will keep a warm instance ready for your next user for free

    The "Wake-Up Call" Strategy 

    Sometimes the best way to handle a cold start is to proactively mask it. If your UI can predict an upcoming request, for example, when a user clicks "New Chat" or begins hovering over a text area, you can send a lightweight health check to your service  immediately. By the time the user finishes typing their prompt, the first two phases of the cold start (Infrastructure Provisioning and Container Image Streaming) are already finished in the background. 

    Pro-Tip: Use Non-Inference Endpoints To make this "wake-up call" as fast as possible, always use a non-inference endpoint rather than sending a dummy prompt like "hi". 

    
     
      Why it’s faster: Non-inference endpoints (like /v1/models for vLLM or /api/tags for Ollama) are handled by the container’s web server the moment it starts. They don’t have to wait for the slow "Phase 4" model loading and VRAM transfer to complete before sending a success response.

     

     
      No Chat Pollution: Because these endpoints don't trigger the model's completion logic, they won't interfere with the user's actual chat history or accidentally trigger session creation in your backend.

     

    

    Recommended Endpoints:

    
     
      vLLM: GET /health  or GET GET /v1/models

     

     
      Ollama: GET /api/tags or GET /api/version

     

    

   

  

  
   
    Tune Startup Probes for VRAM 

    AI models take significant time to move gigabytes of weights from storage into GPU memory (Phase 4). If your startup check fails too many times, Cloud Run will assume your container is broken and kill it.

    To prevent this:

    
     
      Increase the Failure Threshold: Use a high failureThreshold (e.g., 60 or more). Since the total allowed startup time is the product of failureThreshold \times periodSeconds, a threshold of 60 with a 5-second period gives your model a healthy 5-minute window to load.

     

     
      Utilize the 30-Minute Maximum: While standard services are limited to 4 minutes, Cloud Run supports a total startup time of up to 30 minutes (1,800 seconds) for intensive workloads.

     

     
      Avoid False Positives (The Ollama Fix): Be careful with engines like Ollama, which may open a TCP port as soon as the service starts, but before the model is actually in VRAM. Always ensure you are preloading models during the container's entrypoint script to ensure the startup probe only passes once the model is truly ready for inference.

     

    

    Lessons from Elastic’s strategy

    In our NEXT ‘26 session, Ajay Nair highlighted three architectural decisions that allowed Elastic to treat GPUs as fungible compute, rather than infrastructure to manage:

    
     
      Bypass the Compilation Tax: By setting enforce_eager=True in vLLM, they traded a tiny bit of throughput for cold starts that finish in less than a minute rather than multiple minutes.

     

     
      Standalone Checkpoints: They avoided the latency of runtime adapter-switching by pre-merging each LoRA variant into a standalone checkpoint.

     

     
      One Workload, One Service: Each independently-scalable workload — defined by model, task adapter, and traffic shape — is deployed as its own Cloud Run service. This produces 30+ services across ~15 model families, with some models split by task (e.g., v5 retrieval vs. clustering) or by query/passage role.

     

    

    Ready to get started?

    Optimizing the cold start process is the difference between a hobby project and a production-ready application. The best part? Cloud Run handles the NVIDIA driver and CUDA installation for you, starting the instance in about 5 seconds.

    For a deeper dive, the official documentation is your best friend:

    
     Best practices: AI inference on Cloud Run with GPUs

     Configure GPU for Cloud Run services

     Startup CPU boost for Cloud Run

    

    For the full technical breakdown, I highly recommend watching the recording of the session from Google Cloud Next '26. It provides the most comprehensive blueprint for hosting high-performance open models on serverless infrastructure."

    Happy building!

    
    Special thanks to Sara Ford and Shane Ouchi from the Cloud Run team and to Zac Li from Elastic for the helpful review and feedback on this article.
