# Anatomy of a high-performance EP kernel

- BestBlogs URL: https://www.bestblogs.dev/article/f5ca4d76
- Original publisher URL: https://fergusfinn.com/blog/anatomy-of-a-high-performance-ep-kernel/
- Source: BestBlogs / Hacker News
- Publish time: 2026-06-11 00:04:11
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 22926

---

10 Jun 2026  · 19 min read ·  Cover: "Estación telefónica central en Paris," from El mundo físico (1882), via Wikimedia Commons. 
     

    

    
     Large language models are large. Because they’re large, we need lots of GPUs to run them. It would be nice if LLM inference were ‘embarrassingly parallel’ and we could just always compute independent things on different GPUs. But alas, to use lots of GPUs on LLM inference, we need to get those GPUs talking to one another.

     There are lots of different ways to get different GPUs working together: Tensor Parallelism, Pipeline Parallelism, Context Parallelism, Expert Parallelism, etc. All have their place. But for MoE models, in the MoE layers, when you want to serve at large scale, ‘wide Expert Parallelism’ (wideEP) is kingSee vLLM’s original DeepSeek large-scale serving post for a demonstration at production scale: DeepSeek at 2.2k tokens/s per GPU on an H200 cluster, served with wideEP and data parallel attention..

     The other kinds of parallelism all require communication between GPUs, but their patterns are fixed by the architecture: who sends, who receives, and how much, are all known before the forward pass begins, and are the same on every step. The comms can run as standard collectives.

     Expert parallelism is different. Which tokens need to reach which GPUs is decided by the router, from the data, at runtime, fresh in every MoE layer. And the tokens have somewhere to be reached from: we’ll assume the ‘data parallel attention’ arrangement DeepSeek serves with, where each token lives on exactly one rank (a rank being one GPU somewhere in our cluster). The experts are spread across those same ranks, so a token and the experts it’s routed to will generally not be in the same place. Here’s an example, with 8 GPUs split across 2 nodes, two experts per GPU, 1 token per rank, and 2 routed experts per token:

     Hover a rank chip for its token’s round trip, or an expert for everything routed to it. Four of the sixteen experts drew no tokens at all this step: the routing is lumpy.

     
      
       
        
         
        
       
       DISPATCHEXPERTSCOMBINENODE 0 · NVLINKNODE 1 · NVLINKcrossing = RDMA · within a node = NVLinkGPU 0GPU 1GPU 2GPU 3GPU 4GPU 5GPU 6GPU 7
       
        Expert 0
       
       
        Expert 1
       
       
        Expert 2
       
       
        Expert 3
       
       
        Expert 4
       
       
        Expert 5
       
       
        Expert 6
       
       
        Expert 7
       
       
        Expert 8
       
       
        Expert 9
       
       
        Expert 10
       
       
        Expert 11
       
       
        Expert 12
       
       
        Expert 13
       
       
        Expert 14
       
       
        Expert 15
       
       
        r0
       
       
        r0
       
       
        r1
       
       
        r1
       
       
        r2
       
       
        r2
       
       
        r3
       
       
        r3
       
       
        r4
       
       
        r4
       
       
        r5
       
       
        r5
       
       
        r6
       
       
        r6
       
       
        r7
       
       
        r7
       
       
      
     
     When it comes time to run our MoE layers, our tokens have to go and meet their experts, wherever they might be in the network fabric. It’s the job of the EP communication kernel to make that happen.

     The modern shape of these kernels was set by DeepSeek’s DeepEP library. In this post we’ll build up the anatomy of a DeepEP-style dispatch and combine kernel: the high-throughput shape first, then the low-latency one.

     The job we have to do§

     Let’s make the setup concrete. We have 8 GPUs, split across 2 nodes, connected with RDMA, and each data parallel rank owns a single GPU. Attention runs on each GPU over a batch of  
        
         
          Bi
         
         B_i
         
        tokens, where  
        
         
          Bi
         
         B_i
         
        can vary between GPUs. We’re doing expert parallel with  
        
         E=16E=16
         
        experts, two per GPU, of which  
        
         K=2K=2
         
        are routed for each token.

     At each rank  
        
         
          ri
         
         r_i
         
       , at the entrance to the EP layer, we have a tensor of shape  
        
         
          (Bi,H)
         
         (B_i, H)
         
        
          
           HH
           
          is the hidden size.. The routing layer will run locally, and give us expert assignments for each token. We’re routing 2-out-of-16: for each token, the router gives us a set of logits of length  
        
         1616
         
        (i.e. a tensor of shape  
        
         
          (Bi,16)
         
         (B_i, 16)
         
       ), from which we’ll take the indices of the top 2, to get a tensor of shape  
        
         
          (Bi,2)
         
         (B_i, 2)
         
       . For example, if token  
        
         kk
         
        is routed to experts  
        
         33
         
        and  
        
         1313
         
       , then row  
        
         kk
         
        will be  
        
         [3,13][3, 13]
         
       .

     So at the entrance to the EP layer each rank holds two things: the activation rows it produced, and, after the local routing pass, the top-2 expert assignment for each of those rows.

     
      
       
        
         
        
       
       activations(Bᵢ, H)routerexpert logits(Bᵢ, E=16)assignment(Bᵢ, K=2)0123456789101112131415E:Wᵣ xH→Et0
       
        
       
       
        
       
       −1.20.3−0.42.10.1−0.80.5−0.20.9−0.60.2−1.00.41.7−0.30.6313t1
       
        
       
       
        
       
       2.40.2−0.50.9−1.10.31.9−0.20.7−0.90.10.5−0.70.2−0.1−0.406t2
       
        
       
       
        
       
       0.12.2−0.30.4−0.90.2−0.60.80.31.8−0.20.6−1.10.10.5−0.819t3
       
        
       
       
        
       
       −0.60.32.00.1−0.20.7−1.00.4−0.50.20.8−0.30.61.6−0.70.1213
      
     
     Not all of the experts live locally. Some live next door, on neighbouring NVLink peers, and some live far away, on nodes reachable only over RDMA. The goal of the expert parallelism kernels is to get the activations where they need to go, run the expert GEMMs when they get there, and then bring them back home.

     We’re doing communications here, and with communications it’s handy to specialise on what we care about most: throughput, or latency. The split maps onto the two phases of inference: prefill brings big, compute-bound batches with plenty of other work to hide communication behind, while at decode there is hardly anything else to do, so the transfer itself is what we wait on. We’ll start with the throughput-optimised standard EP shape, then discuss the latency-optimised shape.

     High throughput: ask, then send§

     Dispatch§

     The point of dispatch is to feed a grouped GEMMA grouped GEMM is one kernel launch running a separate matrix multiply per expert, each over a different number of rows. Routing produces exactly this raggedness: each expert’s group is however many tokens it drew.. After routing, every expert has to run a matrix multiply over exactly the tokens assigned to it. Before routing, those tokens are scattered across every rank in the cluster.

     So on each rank, dispatch has to gather the tokens bound for the local experts into a single dense buffer that a grouped GEMM can consume in one go.

     The difficulty is that we don’t know the shape of that buffer ahead of time. Which token goes to which expert is decided by the router at runtime, and the distribution is lumpy and changes every step. An expert might draw a thousand tokens now and none next time. We can’t know how many our local experts will receive until every other rank has run its router. So neither the size of the local activation buffer nor the slot in that buffer into which any particular token lands is known in advance.

     There are two ways to cope with not knowing the size.

     
      We can reserve enough room for the worst case, by allocating a fixed rectangle with a padded slot per expert.

      We can find out the real counts first and then allocate exactly what we need.

     

     The fixed rectangle is simpler, but it has to be sized for the worst case. The worst case doesn’t scale with the tokens you actually receive: all the peers might route their whole batches at the same expert, so every padded slot has to be big enough for everyone at once. At prefill batch sizes that means far more HBM holding emptiness than data, and spare HBM is exactly the resource we want back, because it becomes KV cache, which is what keeps sequences in flight. The price of exactness, meanwhile, is affordable here: when batches are large and the GEMMs are compute bound, the extra communication it takes to learn the real counts can hide behind computeServing stacks manufacture room to hide it in: with two-batch overlap, the step is split into two microbatches, so that while one microbatch’s tokens are on the wire, the other’s GEMMs keep the SMs busy. See SGLang’s large-scale EP writeup.. So the throughput path allocates a ragged buffer,  
        
         
          (
          
           Nlocal
          
          ,H)
         
         (N_\mathrm{local}, H)
         
       , sized to the tokens we’ll actually receive. The fixed rectangle is the low-latency story, which we’ll come to.

     
      
       
        
         
        
       
       High throughputpacked buffer (N_local, H)E0E1E2E3034810no padding, but the layoutdepends on everyone’s counts.Low latencyfixed buffer (E_local, max_tokens, H)cap = 5 tokens per expertE0E1E2E3padded to the cap, but everyaddress is known up front.
      
     
     If we want to allocate only what we need, we have to learn the counts before any activations move. We can do so by running a coordination pass. Every rank already knows from its own routing how many tokens it’s sending to each peer. If everyone trades those numbers, each rank can add up how much it’s about to receiveThe exchange mirrors the fabric: counts cross between nodes over RDMA, then between GPUs within a node over NVLink, gathering as they go, so the coordination costs the same two hops the real dispatch will..

     The coordination pass is cheap in bytes, only a handful of integers per peer rather than megabytes of hidden state. Once a rank knows how many tokens are coming from each source, a write-safe layout of the buffer comes naturally as a prefix sum: the first source’s tokens start at zero, the next source’s start where those end, and so on. The counts hand us both of the things we were missing: how big to make the buffer, and where every block sits inside it.

     
      
       
        
         
        
       
       GPU 0 assembles its counts columnmineNVLinkRDMARDMA to a peer, then NVLink012345678/64All-GatherRDMA over rails0123456716/64All-GatherNVLink0123456764/64dst01234567srcrecv
       
        
       
       
        
       
       21031201prefix sumoffset02336799
      
     
     With the layout fixed, we can actually send the activations. The sender never writes to the final buffer directly. It couldn’t if it wanted to: RDMA writes can only land in memory that was registered with the NIC ahead of time, and the compact buffer is allocated fresh each step, at a size we only just learned. So the sender streams its tokens into a small fixed-size queue on the destination, carved out of pre-registered memory, and the receiver, which owns the compact buffer, drains that queue and copies each token into the slot the prefix sum assigned it. The queue also lets the two sides run at their own pace, with its depth bounding how far ahead the sender can get before it has to wait for the receiver to catch up. The queue is fixed-size too, but fixed at a constant.

     For the queues that cross nodes there’s one more hop hiding in the picture. A token never travels point-to-point to an arbitrary remote GPU: it goes over RDMA to the GPU with the same index on the destination node, and that GPU forwards it over NVLink to its final host. Each GPU then only ever talks to its own counterparts across nodes, which keeps every RDMA flow on its own rail of the fabric and caps the number of connections each NIC has to keep fed.

     What lands in the compact buffer is grouped by where it came from, not by which expert it’s for: the transfer is coarser than the routingA token is sent to a peer once if any of that peer’s experts want it, even if two do, with the per-token expert assignment carried alongside. That is what makes the transfer coarser than the routing.. The grouped GEMM wants contiguous per-expert blocks, so the last step of dispatch is a local permute, from by-source order into by-expert order. In DeepEP this last step is the caller’s: dispatch hands back the by-source buffer along with per-expert counts, and the serving framework does the reordering, or feeds the indices straight to a GEMM that can consume them.

     
      
       
        
         
        
        
         
        
        
         
        
       
       Drain by source rank, then permute into per-expert groupspeer 0tailheadpeer 1peer 2by source rankper-expertE0E1E2E3permute
      
     
     Combine§

     The point of combine is to un-run the dispatch kernel, and add up the contributions for each token.

     The GEMM left its outputs grouped by expert, so the first thing we have to do is to undo the permutation we did on the way in. The inverse permutation puts the outputs back into the by-source-rank layout that dispatch delivered tokens in.

     From there the transport runs in reverse. The rank that hosted the expert is now the sender, streaming its outputs back through the home rank’s per-peer queues into the positions the tokens came from.

     
      
       
        
         
        
       
       Combine, send side: unpermute, then write each group homeE0E1E2E3per-expertunpermuteby dest rankover the fabricpeer 0peer 1peer 2
      
     
     We don’t need to do the coordination pass, since combine is handed the same routing information dispatch produced, so it already knows where everything needs to return to.

     Each token was routed to  
        
         KK
         
        experts, and those experts can sit on different ranks, so several partial outputs converge on the token’s home rank. There they are summed, weighted by the router’s gate weights, into the single vector that is the layer’s output for that tokenThe transport itself just adds the returning contributions together. The gate weights are applied separately, either folded into the activations before the expert GEMM or in the reduction step, so the kernel moving bytes doesn’t have to know about them..

     
      
       
        
         
        
        
         
        
        
         
        
       
       Combine, a receiver rank: sum each position across peersper-peer bufferssumactivationspeer 0013tailheadpeer 112peer 2023Σ0Σ1Σ2Σ3
      
     
     So combine mirrors dispatch at every step. The permute becomes an unpermute, the coordination pass is replaced by reusing dispatch’s routing, and where dispatch compacted arriving tokens into contiguous positions, combine sums them into slots.

     Low latency: send without asking§

     The reason to optimise the kernel for latency is the decode regime. Each rank holds only a handful of tokens, often one per sequence in the batch. The coordination pass was cheap in bytes, but it’s a full network round trip with barriers, and it has to finish before any activations move. At decode there is little to overlap it with, and it becomes a large fraction of the layerA second important penalty: dynamic shapes like the ones in the high-throughput kernels are tough to push into CUDA graphs, which are more important during decode..

     So we want to figure out how to skip it. The coordination pass only ever existed to turn counts into write offsets, and that was only needed because the compact buffer made each sender’s offset depend on what every other sender did. If we’re willing to give up compactness, we can prearrange space for each peer rank to write into. Instead of one packed buffer we pre-reserve a fixed, private region for every (source rank, expert) pair. This is the fixed rectangle from the dispatch fork, with one refinement: the padding is per (source rank, expert) rather than per expert, so no two senders ever write into the same region.

     The address a sender writes to is now a formula, the region for its (source, expert) plus a local slot, and every rank can compute it alone:

      
        
         
          addr=base+(e⋅R+r)⋅chunk+slot
         
         \mathrm{addr} = \mathrm{base} + (e \cdot R + r) \cdot \mathrm{chunk} + \mathrm{slot}
         
       
     with  
        
         ee
         
        the local expert,  
        
         rr
         
        the source rank,  
        
         RR
         
        the number of ranks, and  
        
         chunk\mathrm{chunk}
         
        the per-region cap. The dynamic prefix sum over real counts becomes a static stride times a fixed maximum, and the first thing that happens in the layer is the data send itself.

     Since the transfer is now the thing we wait on, the bytes are the latency, and DeepEP’s low-latency dispatch shrinks them by quantising the payload to FP8 on the wire by default. The return path stays in BF16: combine’s sums are where precision matters.

     The catch is that each private region has to be big enough for whatever its source might send, sized for the worst case rather than the actual count. Left unbounded that worst case is enormousWithout a cap, each region would have to hold the most tokens any rank could ever present, and there is one region per source rank, so the receive buffer would grow with the total number of tokens in flight across the system rather than with a fixed budget. The cap replaces that with a constant., so we need to cap how many tokens a rank may dispatch in one call to a fixed chunk size, and microbatch anything larger. With the cap each region is one chunk tall, and a receiver’s buffer is  
        
         
          
           Elocal
          
          ×R×chunk×H
         
         E_\mathrm{local} \times R \times \mathrm{chunk} \times H
         
       . Each slab is sized for a source dumping its whole chunk into one expert, but routing spreads those tokens across all the experts, so the slabs sit mostly empty.

     Mostly empty means the receiver cannot just hand the buffer to the GEMM, because most of it is uninitialised. It needs to know how many rows each source actually wrote, and it needs to learn that without reintroducing the round trip we just removed. So when a sender finishes filling its region, it writes one more value, into a fixed slot on the receiver: the count of tokens it put there. The count does double duty: the slot starts empty, so its arrival is also the signal that the region’s data has landedTwo things make this safe. The count is written in a form the receiver can tell apart from the empty initial value, so even a source that sends zero tokens produces a signal distinguishable from one that simply has not arrived yet. And the count is ordered after the data it vouches for: it’s issued on the same ordered channel (the same RDMA queue pair, or behind a memory fence over NVLink), so by the time the count shows up, the data is already in place.. The receiver watches the counts and learns the valid range of every region as it fills; the grouped GEMM masks the padded rows.

     
      
       
        
         
        
        
         
        
       
       Low latency: one expert’s private region per source, no coordinationsourcecountchunk = 6 slotsr02r10r21r33r41r5r62r71zero: signals completeno count yet:not readable
      
     
     Combine works the same way. It never needed a coordination pass, but the throughput path still staged its returns through queues; here even those go away. Dispatch delivered each token tagged with where it came from, so the expert’s host can compute a return address directly: a private slot on the token’s home rank, indexed by the token’s position there and which of its  
        
         KK
         
        experts this one was. The sender writes the output into that slot, raises the same kind of flag, and the home rank does the weighted sum once all  
        
         KK
         
        contributions have landed.

     In sum: low latency inverts the throughput tradeoff. Throughput spends a round trip to keep memory tight; low latency spends memory, in the form of mostly-empty worst-case buffers, to remove the round trip.

     Coming home§

     That’s the story. If you open DeepEP’s codebase you should recognise the shape, though you’ll now find these kernels under legacy/: the recent V2 rewrite rebuilds the library on top of NCCL’s new device-side communication API. What the anatomy looks like after that rewrite is worth a post of its own.

     DeepEP itself is built for NVIDIA’s stack: Hopper and Blackwell GPUs, NVLink within the node, InfiniBand-class RDMA between nodes. The UCCL project reimplements the same primitives for lots more: AMD as well as NVIDIA GPUs, and any RDMA NIC, AWS’s EFA, Broadcom’s, at comparable performance.

     There’s a growing stack of optimisations on top. Expert load balancing (EPLB) computes replication and placement plans for hot experts, which serving systems apply periodically: placement is only an indirection the kernel consults, so it’s free to change. vLLM’s elastic EP grows and shrinks the deployment: the world size only enters through  
        
         RR
         
       , in the counts and the regions, so ranks can join and leave. And the routing statistics are observable at exactly this layer: at Doubleword we found that similar requests co-activate similar experts, so you can use EPLB to gather co-activated experts into domains with good networking, and steer the requests that light them up to those domains.

     Work is ongoing to fuse these kinds of comms primitives into the compute kernels themselves (mKernel, ParallelKittens), so we can do fine-grained overlap and better pipelining: one SM can be receiving data while the GEMM tiles start firing off of it.

     However those boundaries move, the job stays the one we started with: the tokens have to go and meet their experts, and then come home.

    

    
      
      
       
        
       
       Suggest an edit 
     
     Last modified: 10 Jun 2026
