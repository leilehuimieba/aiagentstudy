# A Three-Phase Factual Recall Circuit in Gemma-2B and Gemma-12B-IT

- BestBlogs URL: https://www.bestblogs.dev/article/2f139dd0
- Original publisher URL: https://towardsdatascience.com/a-three-phase-factual-recall-circuit-in-gemma-2b-and-gemma-12b-it/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-24 23:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 11429

---

How do large language models represent factual knowledge internally? This post presents BizzaroWorld, a mechanistic interpretability study attempting to localize factual recall circuits in the Gemma model family using activation patching across 60 prompt pairs and 20 knowledge categories. The technical work here is greatly influenced by the work done by Prakash et al.¹, who looked at entity tracking within the LLaMa series of models.

  The goal: localize where factual knowledge lives inside a transformer, and whether that location is consistent across model scale. The full codebase is available here.

  The Experimental Setup

  First of all, I wanted to know why logit differences through clean and corrupted prompt pairs were the ideal way to get to this problem. Finding facts seemed similar to finding entities as Prakash et al. did, so I focused on Indirect Object Identification (IoI). This is clearer if I present three factual prompts and their clean targets.

  
   “When red paint mixes with yellow paint the result is” -> “ Orange”

   “The epic Inferno was written by” -> “ Dante”

   “The Roman god Mercury matches the Greek god” -> “ Hermes”

  

  It seemed to me that, to answer questions like these, LLMs would need to find entities within their representation. So, I looked for more answers about how logit differences and IoI would work in this context, and, for this, the ARENA course² was very helpful. I found that logit differences between clean and corrupt prompt pairs provide a clear scalar signal well-suited to measuring the causal effect of patching interventions, so that is what I measured.

  Thus, I designed a fact battery of 60 clean/corrupt prompt pairs, across 20 different categories of facts.

  
   
   Image by author
  
  Before beginning any patching experiments, I wanted to identify the highest-signal prompt pairs; those in which the logit difference between clean and corrupt runs was most pronounced and informative for activation patching. So I created my own metric to measure this, TotalSwing, which calculates the net effect of patching on these prompt pairs. Here is an example of what I am talking about.

  
   
   Image by author
  
  My intuition was that calculating logit differences on both sides and subtracting them would be the cleanest signal, since the right hand side – applying the clean target onto the corrupt prompt – usually results in a negative logit difference as shown above. That means, both values end up being added together, resulting in a nice, positive scalar through which I could sort all 60 prompt pairs I had created.

  It worked well, and with this I came up with a CSV file with all the prompts, sorted by TotalSwing. I called this the golden prompt pairs, and, using it, I created three experimental modes for each subsequent experiment I would do.

  
   
   Image by author
  
  And now, I was ready to begin the experimentation.

  Isolating Gemma-2B’s Components

  LLMs are huge structures. To know where anything is happening, we need ruthless isolation. TransformerLens³ by Neel Nanda was instrumental to do just that. I wanted to hook onto all different pieces of the puzzle i.e. the residual streams before and after all relevant components (the attention heads and MLP sublayers) across all layers. And that’s precisely what I did. I ran four experiments, where I progressively narrowed down the model into its pieces.

  
   Experiment 1 = patching at the final token position

   Experiment 2 = patching before and after each of the sublayers

   Experiment 3 = patching at the entity token position

   Experiment 4 = patching before each attention head

  

  The numbers these experiments generated highlighted a clear finding: there exists a three-phase factual recall circuit within the Gemma model family.

  
   Phase 1 — Storage (layers 0–14, entity token position): Facts are encoded as directions in the residual stream at the entity token. The residual stream dominates causally here, contributing 40× more than attention outputs and 18× more than MLP outputs. 86.7% of top-15 prompt pairs released their stored signal at layers 13–15, with a mean worst layer of 16.3 across all experimental modes (Pearson r = -0.83 between model confidence and damage score).

   Phase 2 — Routing (distributed attention heads): Signal moves from the entity token position to the final prediction position via attention heads collectively. No single head was solely responsible, although head 2 was disproportionately active; for instance, it was active in 40% of prompt pairs across experimental mode A. However, individual head damage (ΔLD = -0.68) was negligible compared to full residual stream damage (ΔLD = -11.47).

   Phase 3 — Readout (layers 15–17, final token position): The answer is retrieved, not computed. Late blocks are pass-through i.e. the signal is already encoded and is simply read out. This finding was unanimous across all three experimental modes and 20 knowledge categories.

  

  The Three-Phase Circuit at Scale: Gemma-12B-IT

  I was after a generalizable result, so the next step was to see if this pattern held true for the larger model, Gemma-12B-IT too. Although I wanted to test it out with even larger Gemma models, such as Gemma-31B or Gemma-27B, I was beholden to my university’s HPC disk space constraint, which I will talk about later. Still, I was able to replicate the entire suite for the 12B model, including all experiment modes A, B, and C.

  I found some interesting results while doing so, but first of all, let’s revisit how and where these two architectures differ.

  
   
   Image by author
  
  Besides these architectural differences, everything else, such as the tokenizers used⁴, are the same between the two models. Yet, I saw something which was quite different for Gemma-12B-IT regarding the tokenizer behavior which influenced prompt pair selection.

  When I did the initial triage pass, as I described above for ranking my 60 prompt pairs, this larger Gemma model removed three golden prompt pairs, even though they both use the same tokenizer.

  This exclusion happens because, during the forward pass, the model maps individual tokens into token ID arrays. For these passes to work, the array shapes must match with everything else, otherwise the matrix multiplication does not work. I had observed this when I did this process with Gemma-2B, where I’d seen some bizarre behavior, such as the physics unit “hertz” being mapped to two tokens⁵. Very non-intuitive. I was expecting my 60 prompts to pass through Gemma-12B-IT with no problems, but I was wrong here. This effect was obviously more pronounced when I did initial experimentations with LLaMa-70B⁶, which I will detail in the future work section below, but it took me by surprise.

  
   The consequence of this is that cross-model mechanistic comparisons are partly constrained by tokenizer-induced dataset drift, and reported differences should be interpreted with that caveat in mind

  

  Hence, before designing any fact batteries for such experimentations, we need to run the facts through all the models being tested, so any tokenizer drift is reported immediately, and the prompt pairs affected can be replaced before setting out to do any experimentation.

  After noting these anomalies, I ran experiments 1 through 4, for all experimental modes A, B, and C.

  
   I found that this three-phase circuit replicated at scale: storage shifted to layers 0–27, routing remained distributed with no significantly dominant head, and readout concentrated in the final layers, structurally identical to Gemma-2B, proportionally scaled

  

  Here are some figures that demonstrate this.

  
   
   Image by author
  
  
   
   Image by author
  
  Each category of fact shows its own behavioral pattern, which was consistent with my hypothesis.

  
   
   Image by author
  
  The other interesting bit I saw was that the effect of the attention heads for Gemma-12B-IT seemed even more distributed and duller than what I had seen for Gemma-2B. This finding is highlighted by mean ld_delta heatmaps for the above two models, for the attention heads.

  
   
   Image by author
  
  
   
   Image by author
  
  For Gemma-12B-IT, the heat-map is almost completely empty, except tiny colored cells around layers 20 and 28⁷. Once again, the magnitude of logit difference values were much larger for the residual stream than these sublayer components.

  Disk Quota Issues, Future Experimentations, and Conclusion

  Throughout this experiment, I found many interesting techniques that I was eager to try, such as path patching (with DCM) and CMAP. I also wanted to check if quantization or running the entire pipeline through fine-tuned variants would change this three-phase factual recall circuit. However, I was bottlenecked by a 30GB disk quota constraint. In fact, as hinted above, I had already prepared an 8-bit quantized version of LLaMa-70B and had dealt with the exclusion of 22 golden prompt pairs, due to tokenizer differences. Inference was working well, but I just couldn’t expand the process beyond that due to the disk constraints, so I shelved the idea for later.

  In my opinion, extending this line of work with path patching is the next natural step, as it would show a lot more. Path patching, formalized by Goldowsky-Dill et al⁸., sharpens activation patching from node-level to edge-level precision. Standard activation patching measures the total causal effect of a node by replacing its output and observing all downstream consequences; path patching, instead, isolates individual edges in the computational graph, revealing precisely which components communicate with which.

  These findings establish a foundation for targeted intervention: knowing where factual recall lives is prerequisite to knowing where to intervene when it fails. To take these ideas further, I would like to follow through on my initial plans, and also see how the attention heads collaborate using SAEs. Yes, the residual stream is doing the heavy lifting, but what does that mean? I need further details.

  In summary, the logical next move for this work is cross-architecture replication on LLaMA and other variants⁹. Additionally, the distributed routing finding in Experiment 4 warrants path patching experiments to establish directed causal relationships between components.

  References

  
   Nikhil Prakash, Tamar Rott Shaham, Tal Haklay, Yonatan Belinkov, and David Bau. Fine-tuning enhances existing mechanisms: A case study on entity tracking, 2024

   https://github.com/callummcdougall/ARENA_3.0

   https://github.com/TransformerLensOrg/TransformerLens

   Gemma uses the SentencePiece tokenizer

   Whereas something like the physics unit “Watt” was one token, as you’d expect logically

   LLaMa uses Tiktoken or SentencePiece tokenizer, depending on the model version

   If you look closely, other cells are highlighted too, but they’re much duller compared to Gemma-2B

   Nicholas Goldowsky-Dill, Chris MacLeod, Lucas Sato, and Aryaman Arora. Localizing model behavior with path patching, 2023.

   It would be especially interesting to include a diffusion language model such as LLaDA-8B here, since the attention mechanism differs fundamentally from standard autoregressive transformers, requiring custom hook infrastructure beyond what TransformerLens currently supports
