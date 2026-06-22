# Pretrained to Imagine， Fine-Tuned to Act: The Rise of World-Action Models

- BestBlogs URL: https://www.bestblogs.dev/article/da120804
- Original publisher URL: https://developer.nvidia.com/blog/pretrained-to-imagine-fine-tuned-to-act-the-rise-of-world-action-models/
- Source: BestBlogs / NVIDIA Technical Blog
- Publish time: 2026-06-15 10:01:57
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 82347

---

Quick glossary for readers new to VLA/WAM terminology
    
     
      VLA Vision-Language-Action model: a robot policy that starts from a pretrained VLM backbone and adapts it to generate actions from visual observations and language instructions. Large-scale VLM pretraining is a core part of the recipe. See Pi-0 and GR00T N1.
     

     
      WAM World-Action Model: a policy that starts from a pretrained world-model or video backbone and adapts it to represent or predict how the scene changes over time and emit corresponding actions. We use WAM as the term throughout this post.
     

     
      VLM Vision-Language Model: a model pretrained on image-text or video-text data to produce language outputs grounded in visual inputs, usually before being adapted for robot control.
     

     
      Video backbone A pretrained video model reused as the central representation or generator inside a robot policy.
     

     
      World model A model that predicts a future world state, conditioned on some action abstraction such as language, robot actions, or latent actions. The predicted state may be represented as images, video, point tracks, object states, or latent features. See the classic World Models paper and NVIDIA’s Cosmos world foundation model paper.
     

     
      Grounding Connecting symbols (e.g. words in a language instruction) to the perceptual and motor referents that satisfy them. Language-to-action grounding in particular means turning an instruction like “pick up the red mug” into the visual percepts and motor commands that actually accomplish it. The grounding gap is the persistent shortfall between what a model knows about language and what it can reliably cause to happen in the physical world.
     

     
      Inverse dynamics Given a current observation ot and a future observation ot+k, infer the most plausible action or action sequence that would produce the transition.
     

     
      Joint prediction Given ot and language lt, train one policy π(ot, lt) to predict both future observations ot+1:t+k and actions at:t+k.
     

     
      Action chunk A short horizon action sequence at:t+k — i.e. the k actions at, at+1, …, at+k−1 — such as joint commands, end-effector deltas, and gripper states, predicted in one policy call. See ACT and Diffusion Policy.
     

     
      Mixture-of-Transformers (MoT) Several modality-specific transformers or experts, such as a video transformer and an action transformer, connected through shared attention while keeping separate weights. See the related Transfusion paper.
     

     
      Diffusion Transformer (DiT) A transformer backbone used inside diffusion or flow-matching models to denoise image, video, or action tokens over multiple steps. DiT commonly uses adaptive layer normalization (adaLN) to inject timestep conditioning into transformer blocks. See the Peebles and Xie DiT paper.
     

     
      VAE Variational Autoencoder: in this post, mainly image and video VAEs that compress high-resolution images or videos into latent representations before generation or policy learning. This reduces token count substantially; for example, Wan 2.1’s VAE uses 4× temporal and 8×8 spatial compression, while Wan 2.2-5B uses a higher-compression 4× temporal and 16×16 spatial interface. See the original VAE paper, Rombach et al.’s latent diffusion paper, the Wan paper, and the Wan 2.2 release.
     

     
      Wan A family of large pretrained video-generation models often used as the video backbone in recent WAMs. See the Wan paper.
     

     
      Cosmos NVIDIA’s world foundation model family for physical AI, including video prediction models that can be adapted for robotics and policy learning. See the Cosmos paper.
     

     
      DROID Distributed Robot Interaction Dataset: a large real-world manipulation dataset with more than 50k demonstrations across varied tasks, collected using Franka Panda robot arms. See the DROID paper.
     

     
      RoboArena A distributed real-world benchmark for evaluating generalist robot policies on open-ended language-conditioned tasks. See the RoboArena paper.
     

     
      RoboLab A high-fidelity simulation benchmark for analyzing task-generalist robot policies across visual, relational, and procedural competencies. See the RoboLab paper.
     

     
      CALVIN A language-conditioned manipulation benchmark focused on long-horizon task sequences in simulation. See the CALVIN paper.
     

     
      LIBERO A robot-learning benchmark for studying knowledge transfer, lifelong learning, and generalization in manipulation. See the LIBERO paper.
     

     
      RoboTwin A simulation data generator and benchmark for robust bimanual robotic manipulation under domain randomization. See the RoboTwin 2.0 paper.
     

     
      FAST / BEAST Discrete action-tokenization methods that turn continuous robot actions into token sequences, making action learning more compatible with VLM-style training. See the FAST paper and BEAST paper.
     

     
      VPP Video Prediction Policy: a WAM-style method that uses predictive visual representations from a video model to condition robot actions. See the VPP paper.
     

     
      LAPA Latent Action Pretraining from Videos: a method for learning action-like latent variables from videos without ground-truth robot action labels. See the LAPA paper.
     

     
      OOD Out-of-distribution: a task, object, environment, or instruction outside the examples used during training or demonstration.
     

     
      FLOP / ZFLOP Floating-point operations measure training compute. 1 ZFLOP equals 1021 FLOPs.
     

     
      H100 / GPU-hour H100 is a high-end NVIDIA training GPU. A GPU-hour means one GPU running for one hour, a rough unit for comparing training cost.
     

     
      BF16 Brain floating point 16-bit: a lower-precision number format commonly used to train large neural networks efficiently.
     

     
      I2V Image-to-video: a video-generation setup conditioned on an initial image or frame.
     

    

   
   
    Background: two building blocks. A visuomotor policy maps current observations plus a goal or instruction to robot actions. A world model predicts future visual or latent states from the current state plus an action or goal abstraction. A WAM sits at the overlap: it leverages a pretrained video/world-model backbone as a prior and predicts both future states and robot actions.Visuomotor policy: language instruction and current observation in, action sequence out.World model: current world state plus an action abstraction in, future image or latent out.

   

   Introduction

   Last year, my Scholar Inbox digest was dominated almost every day by new VLA papers. This changed in the last months, and a different keyword is coming up almost daily now too: WAM, short for World-Action Model. In October 2025, I wrote in my State of VLA post that WAMs were a small subfield within VLA research and far less popular than VLAs initialized from VLMs [60]. That has changed fast, and my wish to see more work in this direction has already become reality.

   So what changed, and why now? Maybe it is because WAMs are the shiny new thing everyone wants to work on, or VLA authors ran out of new names for their own VLAs, since basically all “-VLA” names like “X-VLA” and “Ego-VLA” are already used. So now we can recycle them for the WAM area. But more likely it has something to do with VLM-based VLAs getting stuck. Modern VLAs benefited from massive vision-language pretraining, but they still hit a language-to-action grounding wall. The problem of mapping language and pixels into behavior still has to be learned from robot data. WAMs offer a different starting point. They use pretrained video or world-model backbones that already model how scene dynamics change under language conditioning. If that prior transfers to behavior generation, the remaining video-to-action gap may be smaller than learning language-to-action grounding directly.

   But the ideas behind WAMs are not new. Early WAMs like UniPi [10] proposed essentially this approach back in 2023. So why did it take several years for the paradigm to enter the robot foundation model mainstream, and where does it actually stand today? This post takes a closer look at the modern WAM landscape to answer the central question:

   
    Central question: Is this a real paradigm shift in research and industry, or just a short hype cycle? And if the recipe works so well, why did it take several years after early papers like UniPi for WAMs to become so popular?

   

   My take: WAMs will become the second major recipe for robot foundation models, alongside VLM-based VLAs. The open questions are which formulation of them wins, and which parts of the model architecture and pipeline actually matter. It is likely that the winner is neither pure VLA nor pure WAM, but a hybrid of both.

   This is my map of the modern WAM space: how to categorize and understand WAMs, what changed since the early models, and how current results compare to VLAs. For a broader survey, see the recent NTU survey “World Model for Robot Learning: A Comprehensive Survey” [57], which maps world models for robot learning across simulation, evaluation, navigation, and autonomous driving.

   Table of contents

   
    
     The Two Representation Bets for Generalist Policies

     Why World-Action Models? Our Hypotheses
      
       The Grounding Gap

       Core Hypotheses for WAMs as Policy Representations

       A Quick Experiment: Veo 3.1

      

     Understanding Modern WAMs: Core Formulations
      
       Paradigm: What the Model Predicts
        
         Inverse Dynamics

         Joint Prediction

         Representation-Only

        

       Action Integration: How Actions Enter the Model
        
         Default Action Tokens

         Action as Image

         Latent Actions and Plans

        

       Architecture

       Why WAM Took Off Now

       WAM Comparison

      

     Practical Considerations
      
       The Cost of the Video Prior

       Inference Speed

      

     Why the Modern VLA Baseline Still Matters

     Are the Two Representation Roads Actually One?
      
       A Fourth Path: Robotics-First Foundation Models

      

     Closing Thoughts

     Sources

    

   
   The two representation bets for generalist policies

   
    
     
      
       
      
     
    
    
     Figure 1. The two current bets for generalist manipulation policies: VLM-based VLAs vs video-backbone WAMs.
    
   
   The field currently has two major representation bets for robot foundation models in both research and industry. Many teams are building on the traditional VLA recipe established by Pi-0 [2] and later refined by Pi-0.5 [4], using VLM backbones as the starting point for policy learning. This VLM-backbone recipe appears in public work from teams including NVIDIA GR00T [5], Xiaomi Robotics [27], Being-H0.5 [28], and others.

   More recently, a different paradigm has emerged: using pretrained video backbones as an alternative path toward generalist manipulation. Public examples now span NVIDIA’s DreamZero [8] and Cosmos Policy [13], Ant Group’s LingBot-VA [9], Rhoda AI’s DVA [40], Sereact’s Cortex 2.0 [45], and Mimic Robotics with mimic-video [14]. At the same time, many university labs and open research groups are also pushing the frontier with new ideas, including Video Prediction Policy [24], Unified Video Action Model [39], and Fast-WAM [23]. We discuss these in more detail below.

   The choice of backbone impacts the full training and evaluation pipeline, from training recipe and data mixture to inference optimizations. Given the cost of running these models at scale, most teams will likely have to prioritize one direction (VLA or WAM) first rather than fully pursuing both in parallel. Which path proves out, or whether the two converge, is still open. Which one would you bet on today? In the following sections, we dive deeper into both sides of this decision.

   Why World-Action Models? Our hypotheses

   Before we dive deeper into current models, let’s first review why WAMs are attractive as an alternative to VLM-based VLAs. It also helps to first place WAMs inside the broader landscape of world models in robotics.

   
    
    
     Figure 2. World models in robotics. Action-conditioned world models (DreamDojo, Genie, JEPA-WM) predict future states from a learned action abstraction. Video world models (Cosmos-3, WAN, Veo, LTX-Video) predict future video conditioned on language and a reference frame. World-Action Models (WAM) like DreamZero, LingBot-VA, UniPi, and mimic-Video sit at the intersection: they reuse a video or world-model backbone inside a robot policy that emits actions.
    
   
   The grounding gap

   To understand why WAMs are attractive, it helps to understand the core challenge of “classical” VLAs built on VLM backbones. The motivation for the first VLAs was to leverage the internet-scale knowledge of VLMs for robotics. VLMs are trained on massive amounts of vision-text data and show notable zero-shot performance on many vision tasks. The VLA recipe then adapts these pretrained representations for action generation.

   However, there is a major domain gap between VLM pretraining and embodied manipulation. Several VLA papers either observe degradation of pretrained VLM capabilities or design around it, particularly when the action-learning objective diverges sharply from the original VLM objective. VLM2VLA frames this directly as catastrophic forgetting during the VLM-to-VLA transition [55]. Knowledge Insulation reports similar findings and makes the concern architectural: it isolates the gradients of the flow-matching action expert from the VLM backbone to preserve pretrained language/vision knowledge, improving training convergence, task performance, and language following [20]. Recent solutions like VLM co-training and discrete action tokenizers have helped, but the core challenge remains: grounding language into physical action from limited robot data. We cover these solutions in the modern VLA baseline section below.

   This naturally raises the question: what if we started from a backbone that already represents how language maps to visual change in the world?

   Core hypotheses for WAMs as policy representations

   The core idea is simple: instead of using a VLM backbone to jump-start imitation learning, use a pretrained video backbone. Current video models are trained on large video corpora and learn spatiotemporal representations of how visual scenes evolve. Crucially, current video models are often text-conditioned: they are trained to generate videos from precise language descriptions, sometimes with a reference frame and sometimes from text alone. Many of these videos contain intentional behavior: hands reaching, tools moving, objects being manipulated, and scenes changing because someone or something acted. That makes video backbones attractive as a model prior for generalist manipulation. Before seeing any robot actions, the backbone already encodes useful links between language, visual change, and plausible object interactions. The Veo 3.1 demonstration below is a quick illustration.

   I would treat the next three points as hypotheses, not conclusions. They are recurring claims across papers, discussions with peers, and my own read of the field, supported by qualitative intuition, simulation evidence, and a few early real-world signals, but not by clean matched comparisons yet:

   
    Predicting future world changes correlates with generating the necessary actions. Inverse dynamics prediction is often easier than pure action generation [26]. If the desired outcome is known, inferring the action that produced it is usually simpler than predicting the action directly from the instruction and current observation. Pi-0.7’s visual-subgoal results point in the same direction: when the policy is given a desired future image, action prediction becomes more direct and training converges faster [43].

    Video pretraining provides grounding between language and physical change. Video models learn to map text descriptions to visual outcomes. If this transfers to robotics, it could reduce the amount of grounding that has to be learned from robot demonstrations alone.

    Video data regularizes robot policies. Robot datasets are small relative to web-scale video. Either through pretraining on video first or through co-training on video alongside robot data, the broader visual prior can reduce overfitting; the benefit depends on the dataset, objective, and architecture. DreamZero [8] and Fast-WAM [23] both show that, during robot fine-tuning, WAMs perform best when action learning is co-trained with a video-prediction objective.

   

   A quick experiment: how much does a frontier video model already “understand” about robot manipulation?

   How much do modern video models already capture before any robotics-specific action head is added? We ran a simple experiment with Google’s Veo 3.1, a frontier video generation model. Given a single context frame from an original RoboArena rollout of a toaster task in the DROID setup, we prompted Veo to push the toaster lever (the reference task, matching the original DROID demonstration) and then pick up an orange sitting to the left (the composed extension, beyond the demonstration). This video is very unlikely to be part of Veo’s pretraining data, but we cannot verify the training set directly; treat this as a qualitative check of the prior, not a controlled probe of training-set membership. One-shot attempt, no prompt optimization.

   The prompt used was:

   
    “Given this initial frame, generate a video of the robot arm pushing the toaster lever. After finishing that task, the robot should pick up the orange on the left side of the toaster and stop after it has picked it up.”

   

   Context frame and ground-truth rollout:

   
    
     
     
      Figure 3. Context frame from a RoboArena toaster task in the DROID setup.
     
    
   
   
    
     
      
       
       
        Figure 4. Ground-truth rollout: robot pushes the toaster lever.
       
      
     
    
   

   Veo 3.1 generated rollouts (zero-shot, no robotics fine-tuning): 
     

   
    
    
     Figure 5. Veo 3.1 rollout for the reference task (pushing the toaster lever).
    
   
   
    
    
     Figure 6. Veo 3.1 rollout for the composed extension (lever push followed by orange pickup).
    
   
   
    
     
      
      
       Figure 7. Animated rollout of the full composed-extension sequence: lever push followed by orange pickup.
      
     
    
   
   The generated rollout is surprisingly good for a model that was not explicitly trained as a robot policy. The generated motions are smooth, the background remains stable and consistent, and the robot follows a plausible trajectory toward both target objects. Even the sequencing is respected: finish the lever, then move to the orange.

   The limitations are equally visible: The model does not fully push the toaster lever down and at points appears to attempt the opposite motion (pulling it up). More visibly, the pinch gripper from the original DROID setup morphs into a four-fingered hand. The fixed-base robot arm is reimagined, almost instantly after the context frame, as a different robot with fewer degrees of freedom. These artifacts are consistent with the model using broad visual priors rather than faithfully modeling the specific hardware.

   Still, the result illustrates why video backbones are attractive for robotics: the model has a useful prior for what robot-object interaction should look like, even though it is not yet reliable enough for control. WAM fine-tuning is the attempt to turn that zero-shot imagination into reliable control.

   Understanding modern WAMs: Core formulations

   After establishing the core motivation, we can now focus on the current WAM research. In contrast to VLM-based VLAs, where the training recipe has largely converged around VLM co-training with a flow transformer for action generation, WAMs are still splitting into several active formulations. This is exactly what makes the area interesting right now: the field does not yet know which combination of design choices will win, or whether the best systems will merge parts of several.

   To make the design space readable, we organize WAMs along three axes (which are not fully independent):

   
    Paradigm: what does the model predict, and how is the predicted video used to generate actions? (inverse dynamics vs joint prediction vs representation-only)

    Action integration: how do actions actually enter the model? (default action tokens vs action-as-image vs latent actions/plans)

    Architecture: how are the components composed? (Mixture-of-Transformers vs monolithic vs hierarchical)

   

   The axes are not fully independent, and some WAMs do not fit well into a single category. I would not treat this as a perfect taxonomy. It should be more a practical map for reading the current papers without getting lost in naming choices. For each axis, I present the idea with an older paper and then a modern scaled-up version of the same rough recipe.

   
    
    
     Figure 8. The WAM design space at a glance. Left: The three paradigms differ in what the model predicts. An inverse-dynamics WAM generates future video and then derives actions from it. A joint-prediction WAM emits video and actions together. A representation-only WAM uses the video backbone purely as a representation and skips video generation at inference. Middle: The three action-integration choices differ in how actions enter the model. Actions can be standalone tokens. They can be image-shaped targets the video model natively denoises. Or they can be compressed latent actions and plans. Right: The three architecture styles differ in how the components are composed. A monolithic transformer handles everything in one stack. Modality-specific experts coupled by shared attention (MoT) keep separate weights but share information. A hierarchical pipeline runs a video module before an action module. The rest of this section walks through each axis in turn.
    
   
   Paradigm: What the model predicts

   The first axis is the policy formulation: what the model predicts, and how the predicted video is used to generate actions. Across modern WAMs, we see three directions that differ at the inference boundary: inverse dynamics, joint prediction, and representation-only.

   Inverse dynamics: Predict the future, then infer the action

   
    
    
     Figure 9. Inverse-Dynamics WAM (abstract). A video model first produces future frames or latents from the language instruction and current observation; an inverse-dynamics head then maps the predicted transition into a sequence of actions. Specific systems differ in whether they use full RGB futures (LingBot-VA, DVA), latent video features (VPP, mimic-video), or only intermediate features.
    
   
   The inverse-dynamics setup is the easiest WAM recipe to understand: first imagine the future, then predict the most likely action from the video. This shifts the hard language-grounding problem into the video stage: translate the command into a plausible visual change. The bet is that video pretraining has already learned a useful part of this language-to-visual-change mapping, so the action head does not have to learn everything from robot demos and can focus on the inverse-dynamics problem instead.

   

  

  
   
    
     Figure 10. UniPi overview. A text-conditioned video generator produces a future image sequence from the current frame and language instruction; a separate inverse-dynamics module then extracts actions from consecutive frames. Image from Du et al., 2023 [10].
    
   
   UniPi [10] is a pioneering paper for this direction. It was probably the first modern execution of this recipe that was clearly aware of the potential of video diffusion for robotics: use video as a high-level plan, then use inverse dynamics to recover the low-level controls. In hindsight. A lot of recent WAM work looks like an improved version of this.

   UniPi also shows why it took several more years until WAMs hit the mainstream. it used a CNN-based video diffusion stack from the Imagen Video era [56], and the video generator had to be pretrained from scratch. Our rough estimate in Footnote 2 puts that pretraining around 167 ZFLOPs, well outside the budget of most robotics labs. While this recipe existed before, it was not really reproducible for the average lab Modern inverse-dynamics WAMs can now sidestep this by starting from open DiT-based video backbones and fine-tuning them2.

   
    
    
     Figure 11. LingBot-VA architecture: inverse dynamics action prediction conditioned on video rollouts from a fine-tuned Wan 2.2-5B backbone. Image from Li et al., 2026 [9].
    
   
   A modern version of this direction is LingBot-VA [9]. It turns Wan 2.2-5B into a robot video-action model through 16k hours of cross-embodiment pretraining. The important difference from UniPi is not just scale.  LingBot-VA is causal and trained on long visual histories for closed-loop rollouts rather than open-loop video generation. It also uses a Mixture-of-Transformers (MoT) architecture: separate experts for video and action, each with its own weights, coupled through shared self-attention in each layer.

   
    
     Table 1. Inverse dynamics, original recipe vs modern scaled version.
    
    
     
      Design choice
      UniPi [10]
      LingBot-VA [9]
     

    
    
     
      Main idea
      Generate a future video plan, then recover actions with inverse dynamics.
      Fine-tune a video backbone for closed-loop robot world-action rollouts.
     

     
      Backbone
      CNN-based video diffusion (cascaded U-Net), trained from scratch in the Imagen Video era.
      Wan 2.2-5B latent DiT (open weights).
     

     
      Latent video VAE
      None; generates low-resolution RGB futures.
      Wan 2.2-5B (16×16 spatial, 4× temporal) [56].
     

     
      Action expert
      Separate CNN action head.
      MoT action expert coupled via joint attention.
     

     
      Action-video coupling
      One-way: video first, then actions.
      Two-way: video conditions actions; generated actions condition video.
     

     
      Robot training scale
      Small, demonstration-only.
      16k hours of robot world-action pretraining across embodiments.
     

    
   

   There are several variants around the same theme. Video Prediction Policy [24], DiT4DiT [37], and mimic-video [14] do not necessarily need the final RGB video; they use intermediate video-model features as the predictive plan for an action decoder. DVA [42] and LingBot-VA lean more directly on generated or predicted future rollouts. The difficult part is that most papers change the video backbone, use different amounts of large-scale pretraining, tune different hyperparameters, and evaluate on different setups.

   Joint prediction: Learn video and actions together

   
    
    
     Figure 12. Joint-Prediction WAM (abstract). A single model takes the language instruction and current observation and emits both an action sequence and imagined future states (frames or latents) in one pass, with no separate inverse-dynamics module.
    
   
   The second formulation is joint prediction. Instead of generating a future video first and then decoding actions, the model predicts video and actions together. This is the more coupled version of the WAM idea: the model is forced to learn what should happen and how to make it happen in the same prediction step.

   
    
    
     Figure 13. GR-1 architecture. Stage 1 pretrains on video prediction; stage 2 fine-tunes on robot data with a joint objective over future frames and action chunks. Image from Wu et al., 2023 [11].
    
   
   GR-1 [11] is an early foundation paper for this direction. It pretrained on large-scale video and then fine-tuned on local robot datasets with both video and action supervision. It used a GPT-2-style transformer policy, pretrained it on internet video prediction with readout tokens, and then fine-tuned it on robotics data with a joint video-action objective. Earlier works like R3M [15] and Voltron [16] had already shown that video and language can help representation learning for robotics, but GR-1 made a simple and important shift: it used video to learn better policy representations, not only image-level visual representations.

   At the time, the CALVIN results were useful simulation evidence. On the harder ABC→D split, prior methods in the GR-1 table stayed below an average sequence length of 1.0, while GR-1 reached 3.06/5. This result is useful here because it makes the generalization signal easiest to read. By 2026 this number is outdated, but I still think the result matters historically. It showed that predicting future visual states could shape a better policy representation, not just a better visual encoder.

   
    
   
   
    
    
     Figure 14. CALVIN ABC→D result summarized as average completed subtasks out of five, with GR-1 as the historical result and Xiaomi-Robotics-0 as a current SOTA VLA reference. Values are redrawn from 
      
 
      Wu et al., 2023 [11] and Xiaomi Robotics, 2026 [27].
    
   
   DreamZero [8] is the modern scaled version of this idea. Instead of training a smaller transformer-style policy around a video-prediction head, it starts from Wan 2.1-I2V-14B-480P and turns the video diffusion backbone into a joint world-action model. The model denoises video and action tokens together inside one monolithic DiT. There is no separate inverse-dynamics module: action is another generated modality inside the same denoising process.

   
    
    
     Figure 15. DreamZero architecture. A single monolithic transformer, initialized from a 14B Wan video diffusion backbone, denoises video tokens and action tokens jointly. Image from Ye et al., 2026 [8].
    
   
   DreamZero’s reported RoboArena score is an important real-world signal for WAMs. While most papers still focus on popular benchmarks like LIBERO and other simulation benchmarks, RoboArena is one of the few public real-world, open-ended evaluations, which is what makes the snapshot below worth pausing on.

   
    
    
     Figure 16. April 2026 RoboArena leaderboard snapshot. Pi-FAST (1592) is ahead of Pi-0 (1475), while Pi-0.5 (1622) and DreamZero (1750) push further ahead.
    
   
   In the April 2026 snapshot above, DreamZero reaches 1750 compared to 1622 for Pi-0.5, which is a meaningful signal for the potential of WAMs. This is not proof that WAMs are the better default, but it is a positive signal for their potential. It is interesting because DreamZero was trained only on DROID without an additional large-scale cross-embodiment robot training stage.

   
    
     Table 2. Joint prediction, early policy-level version vs modern scaled version.
    
    
     
      Design choice
      GR-1 [11]
      DreamZero [8]
     

    
    
     
      Main idea
      Use future-frame prediction as an auxiliary objective while learning actions.
      Denoise future video and robot actions together in one video diffusion backbone.
     

     
      Backbone
      GPT-2-style transformer policy with video-prediction readout tokens.
      Wan 2.1-I2V-14B-480P video diffusion model adapted for robot control.
     

     
      Scale
      ~21M policy parameters; pretrained visual and language encoders kept separate [55].
      14B Wan backbone, action-tuned end-to-end.
     

     
      Generative objective
      L2 reconstruction for future video and actions.
      Flow/denoising for joint future-video and action generation.
     

     
      Latent video VAE
      None; pretrained MAE/ViT visual features.
      Inherited Wan latent video VAE.
     

     
      Language conditioning
      CLIP.
      T5-family text encoder (inherited from Wan).
     

    
   

   GR-1 showed the policy-level version of joint video-action prediction, while DreamZero combines the idea with a modern video-foundation-model and flow-matching setup. The core joint-prediction idea is the same as GR-1, but DreamZero changes nearly everything else around it, so this is far from a clean comparison.

   GR-2 [12], Seer [29], PAD [57], UWM [58], UVA [41], and DreamVLA [40] sit around this broader joint-prediction wave. PAD was another early attempt for joint future image prediction and robot action generation inside one joint denoising process. UWM uses independent noise for video and action to support more flexible inference modes inside a joint transformer.

   Representation-only: Skip video generation at inference

   The third option is to use the video backbone purely as a representation and skip video generation at inference entirely. Fast-WAM is a nice example of this idea.

   Fast-WAM [23] uses a similar Wan/MoT-style setup to LingBot-VA and closely matches its performance on simulated benchmarks even without 16k hours of large-scale robot pretraining. In addition, skipping video generation at test time makes its inference several times faster. However, Fast-WAM is one of the few public pieces of evidence for the representation-only hypothesis, and current simulation evidence is not enough to really convince me of this idea. But I am happy to be convinced in future work.

   Most WAMs today keep some form of video generation at inference and are very slow. Faster WAMs like Fast-WAM will become a much bigger research area in the future.

   Action integration: How actions enter the model

   After discussing how to combine video and action prediction, let’s focus on how actions are represented inside the model. The choice is important because the pretrained backbone knows how to denoise visual tokens, not continuous robot actions, so there is a real modality mismatch. I see three variants in the current papers.

   Default action tokens

   The simplest default is to add action tokens, continuous or discrete, and an action head, where actions are treated as another modality alongside video. UniPi, GR-1, DreamZero, LingBot-VA, VPP, mimic-video, and Fast-WAM all use some version of this. The risk is the modality mismatch: action chunks are different from the visual tokens the backbone was pretrained on, so the model has to adapt its representation during action fine-tuning.

   Action as image

   Another option is to turn the actions into something the video model already knows. Instead of new action tokens or a separate action head, encode actions as visual targets inside the same generation interface, so the pretrained video representation is not disrupted.

   
    
    
     Figure 17. GENIMA turns actions into visual targets: the image model predicts joint-action targets in RGB space, and a downstream controller maps those targets back to robot commands. Image from Shridhar et al., 2024 [31].
    
   
   The closest early ancestor here is GENIMA [31]. GENIMA fine-tunes Stable Diffusion to draw joint-action targets on RGB images, then uses a controller to map those visual targets into joint-position actions. The interesting part is the interface choice: actions are expressed as something the generative image model can draw.

   
    
    
     Figure 18. Cosmos Policy latent injection: action, proprioception, and value targets are represented as synthetic latent frames inside the same video denoising interface. Image from Kim et al., 2026 [13].
    
   
   A modern version of this direction is Cosmos Policy [13], which treats actions as synthetic latent video frames. Instead of adding a separate action decoder, it encodes action, proprioception, and value targets as fake frames inside the video model’s own denoising interface, and at inference time decodes the predicted action image back into an action vector by averaging spatial dimensions. This setup keeps the pretrained video backbone close to its native video denoising space while still producing robot actions.

   Latent actions and plans

   A different option is to compress behavior into latent plans or latent actions and condition the policy on those. This is attractive because full video prediction is expensive, and most pixels are not actually needed for control. Latent plans and latent actions are not exactly the same thing, but for this discussion I group them together: both are compact behavior abstractions learned from trajectories or video.  The main differences are granularity and supervision. Plans usually cover a multi-step window and often need paired robot data; latent actions in the Genie/LAPA style can be learned from unlabeled video.

   
    
    
     Figure 19. Play-LMP architecture. A recognition network compresses trajectory windows into latent plans during training; at inference, a proposal network predicts the latent plan from the current observation and goal image. Image from Lynch et al., 2020 [32].
    
   
   Play-LMP [32] pioneered this idea in 2019. This is worth remembering because the basic idea is older than the current foundation-model wave. Play-LMP compressed sub-tasks into a small latent space as an intermediate abstraction for conditioning the low-level policy, long before access to today’s larger robot datasets and pretrained models. Concretely, a posterior network compressed short trajectory windows into a latent plan, a prior learned to predict that latent plan from the current observation and goal image, and a low-level policy decoded the sampled plan into actions.

   The modern latent-action wave changes the scale and the data source. Genie [19] showed that latent action tokens can be learned from unlabeled internet video and used to drive an action-conditioned world model. Genie itself does not decode those latents into real robot motor commands, so it is not a robot policy. But it made the idea much more scalable: learn an action-like abstraction from video without having ground-truth robot actions. LAPA [33] then pushed this kind of latent-action pretraining toward VLA-style robot learning.

   Being-H0.7 [42] is a modern WAM version of the original Play-LMP idea. It keeps the prior/posterior latent-plan logic, but executes it at foundation-model scale with several major changes. Instead of a small hierarchical latent-plan policy, it uses a larger Mixture-of-Transformers backbone. Similar to Play-LMP, the model has a posterior branch and a prior branch. The posterior branch gets access to future observations, encodes them with a frozen V-JEPA2.1 [64] visual encoder and Perceiver resampler, and compresses them into K future embeddings. The prior branch uses learnable latent queries and learns to match those future-informed latent states from the available context. At test time, the posterior branch is removed, so the policy gets a fast latent interface instead of forcing the model to regenerate full video sequences. The action generation part is still a flow-matching action policy. Being-H0.7 is trained on 200,000 hours of egocentric human video together with 15,000 hours of robot demonstrations.

   
    
    
     Figure 20. Being-H0.7 latent world-action architecture. The posterior branch compresses observed behavior into latent tokens, while the prior branch predicts those tokens for fast test-time policy inference. Image from BeingBeyond Team, 2026 [42].
    
   
   
    
     Table 3. Latent abstractions, early latent-plan recipe vs modern scaled latent world-action recipe.
    
    
     
      Design choice
      Latent Plans / Play-LMP [32]
      Being-H0.7 [42]
     

    
    
     
      Main idea
      Compress short robot behavior windows into latent plans that condition a low-level policy.
      Learn a latent world-action model from large-scale egocentric video and robot demonstrations.
     

     
      Data source
      Robot play / demonstration trajectories.
      200k hours of egocentric human video plus 15k hours of robot demonstrations.
     

     
      Architecture
      Hierarchical latent-plan policy; LSTM low-level decoder.
      Large MoT transformer for latent world-action modeling.
     

     
      Latent variable
      Trajectory-level latent plan, prior/posterior training.
      Same prior/posterior structure, foundation-model scale.
     

     
      Policy interface
      Predict prior plan; low-level policy conditioned on observation and goal executes it.
      Train both branches; at test time only the prior branch runs through the compact latent interface.
     

    
   

   The key difference is not the latent variable itself. Play-LMP already had the core prior/posterior latent-plan idea. Being-H0.7 shows how that interface can be scaled inside a modern WAM/VLA hybrid.

   Latent actions have also become popular as an abstraction for action-conditioned world models. A recent example is DreamDojo [44], which learns continuous latent actions from large-scale egocentric human video for a controllable world model. The important distinction from inverse dynamics is the supervision path. Inverse-dynamics WAMs usually need paired video and action data to learn how visual transitions map to motor commands. Latent-action methods try to first learn a behavior abstraction from video itself, then connect that abstraction to robot action later.

   Architecture: Hierarchical, Monolithic, or MoT?

   The third axis is architecture: how the components are structurally composed. This is mostly orthogonal to the first two axes. Inverse dynamics can be hierarchical or MoT-style, joint prediction can be monolithic or expert-based, and latent-action methods can sit inside several different wrappers.

   
    
    
     Figure 21. Hierarchical: separate video prediction and action generation stages, connected one-way.
    
   
   Hierarchical is the most flexible design because the action head is fully modular. It can be anything from a simple CNN regressor (UniPi) up to a full VLA stack (Pi-0.7’s BAGEL subgoals plus full VLA-based action expert), with VPP [24] and mimic-video [14] sitting in between by passing intermediate video-model features instead of full RGB rollouts. The downside is weak coupling between the video and action stages. Information flows one way, so this style is less natural when video and action should strongly influence each other.

   
    
    
     Figure 22. Monolithic transformer: a single transformer jointly denoises video and actions end-to-end.
    
   
   Monolithic transformers like DreamZero [8] put video and action denoising in the same stack, which gives them strong coupling between the two streams. They are also the natural fit for action-as-image setups such as Cosmos Policy [13], where actions and video already live in the same latent space. The risk is dual optimization: the same model weights have to handle dense visual tokens and much sparser action targets.

   
    
    
     Figure 23. Mixture-of-Transformers: modality-specific experts coupled by shared attention.
    
   
   Mixture-of-Transformers (MoT) is the current default, including in modern VLAs (Pi-0, Pi-0.5) and in recent WAMs like LingBot-VA [9] and Fast-WAM [23]. Modality-specific parameters keep the representations separate while shared attention still lets video and action exchange information. My guess is that MoT-style designs will become the dominant WAM architecture as well, mostly because they are a practical compromise between modularity and coupling.

   Why WAMs took off now

   My short answer for why WAMs took off now: while the idea was not new, the required tools like pretrained video models finally caught up. The early formulations (UniPi for inverse dynamics, GR-1 for joint prediction, Play-LMP for latent abstractions) had the right ideas but limited tools: smaller backbones, weaker video data, no openly available video foundation models, and per-step action heads that did not work well compared to modern action chunk policies. Their modern counterparts (LingBot-VA, DreamZero, Being-H0.7) use infrastructure and large-scale robotic datasets that did not exist a few years ago.

   First, video backbones got much stronger. DiT-based models like Wan [21] and Cosmos [22] replaced earlier CNN-based stacks, with better temporal compression, flow-matching objectives, and well-curated web-scale video data. Second, those backbones became openly available. Researchers can now fine-tune a strong pretrained video model instead of paying the full pretraining cost themselves.Third, the action side caught up: modern systems predict action chunks with transformer or flow-matching heads instead of small per-step MLP heads. That is why WAMs now look like a real recipe, not just an old idea with better branding.

   WAM comparison

   The table below summarizes the models we covered before by categorizing them across different design decisions: what does the model predict, how do actions enter, what backbone does it use, and what architecture is used? The WAM space is moving fast, so this is only a selected subset of papers. For a broader survey of world-model and WAM-related robot-learning papers, see the NTU survey “World Model for Robot Learning” [57].

   
    
     Table 4. Selected WAM and related model comparison along the three design axes (paradigm, action integration, architecture), plus backbone and year.
    
    
     
      Model
      Paradigm
      Action Integration
      Backbone
      Architecture
      Year
     

    
    
     
      Play-LMP [32]
      — (pre-WAM)
      Latent plan
      Transformer + LSTM (scratch)
      Hierarchical
      2019
     

     
      UniPi [10]
      Inverse Dynamics
      Default action tokens
      CNN Video Diffusion (1.7B)
      Hierarchical
      2023
     

     
      GR-1 [11]
      Joint Prediction
      Default action tokens
      Transformer (scratch)
      Unified Transformer
      2024
     

     
      GENIMA [31]
      Inverse Dynamics
      Action-as-image
      Stable Diffusion / ControlNet
      Hierarchical (image gen + controller)
      2024
     

     
      Seer [29]
      Inverse Dynamics
      Default action tokens
      Transformer over visual/action tokens
      Unified Transformer
      2025
     

     
      VPP [24]
      Inverse Dynamics
      Default action tokens
      Stable Video Diffusion
      Hierarchical
      2025
     

     
      mimic-video [14]
      Inverse Dynamics
      Default action tokens
      Video Diff (Cosmos)
      Hierarchical
      2025
     

     
      DreamZero [8]
      Joint Prediction
      Default action tokens
      Video Diff (Wan 14B)
      Monolithic DiT
      2026
     

     
      LingBot-VA [9]
      Inverse Dynamics
      Default action tokens
      Video Diff (Wan 2.2-5B)
      MoT
      2026
     

     
      Cosmos Policy [13]
      Joint Prediction
      Action-as-image
      Video Diff (Cosmos)
      Monolithic DiT
      2026
     

     
      Being-H0.7 [42]
      Joint Prediction (latent)
      Latent plans / actions
      MoT transformer (scratch, 200k+15k hr data)
      MoT
      2026
     

     
      Fast-WAM [23]
      Representation-Only
      Default action tokens
      Video Diff (Wan 5.5B)
      MoT
      2026
     

    
   

   Practical considerations

   We have seen some promising WAM models above and some promising results. However, there are also several core issues:

   
    High training cost. Video backbones process many more tokens than image-conditioned action policies, and full video pretraining is expensive.

    Slow inference. Policies that generate or denoise future video latents are much slower than simple VLAs.

    Memory and systems complexity. Long video-token sequences push GPU memory, communication, and data loading. Good luck trying to run 10B+ WAM models on your local GPU without additional engineering.

   

   The cost of the video prior

   A strong video prior can reduce robotics-data requirements in some settings [24, 25, 42] and still deliver strong zero-shot performance when using modern video models like Wan [21]. In practice, this often trades robot-data efficiency for compute cost. Let’s look at a very rough lower-bound comparison for this.

   Training cost is very hard to compare between models, but we can make a rough lower-bound estimate from the details available in papers and GitHub repos. Therefore, we use a simple dense-transformer lower-bound estimate, C ≈ 6NT, where N is the number of trainable dense parameters and T is the number of tokens1.

   
    
   
   
    
    
     Figure 24. Lower-bound dense-core training compute estimates in ZFLOPs, shown on a log scale. Treat as a rough cross-paper comparison rather than precise budgets; values use the reported parameters, samples, tokens, or GPU-hours available in each paper/model card, with derivations and caveats in Footnote 1
    
   
   VLM-based VLAs are cheaper in both stages of training because their sequences are smaller: they encode one to a few images plus text, then predict text or a short action-token sequence. WAMs train to predict a sequence of video latents with additional action tokens. The video token sequence is often around 10x longer compared to VLA sequences. This makes training on the same dataset more expensive than default VLA training.

   Figure 24 gives an overview of different VLA/WAM training-cost estimates. DreamZero-style action tuning is roughly 9 ZFLOPs, which is large compared to the lightweight VLA training rows. A modern VLA like MolmoAct2 reports the full cost from Molmo2-ER to a DROID checkpoint at about 9.8 ZFLOP-equivalent. This assumes a strong inherited Molmo2-ER backbone and does not count Qwen3 or SigLIP2 pretraining cost. Summer-22B is a modern public video-pretraining token/data reference for understanding the cost required to train a competitive video foundation model at scale: with a 22B-parameter model and the paper’s ~500B-token training scale, it gives a ~66 ZFLOP video-pretraining estimate. If we reduce this to match the DreamZero Wan size of 14B, we can estimate 51 ZFLOPs for training the video model and WAM stage together. Compared to the efficient VLA Foundry recipe at 6.9 ZFLOPs, this results in a ~7.4x gap. These numbers show the challenges of WAM training at scale.

   Beyond total FLOPs, there is a hardware and engineering barrier. A 14B-parameter model with roughly 8k-token action-tuning sequences needs substantial GPU memory and typically multi-node setups with high-end interconnects. Successful video-model training also depends on robust data filtering, captioning, video decoding, latent preprocessing, distributed I/O, and long-sequence DiT infrastructure.

   There is also a data-quality version of the same argument. DreamZero argues that stronger video generation translates into stronger policy performance [8], so WAMs are not only compute-hungry but also video-data-quality hungry: filtering, captioning, latent representation, and generative pretraining all become part of the policy recipe. VLM-based VLAs do not show the same clean link. VLM4VLA [51] finds VLM initialization helps versus training from scratch, but generic VLM capabilities are poor predictors of downstream VLA performance. For WAMs, video-generation quality is a requirement for good policies; for VLAs, spatial objectives are much more important than other vision capabilities.

   For row-by-row caveats and the derivations behind each estimate, see the reference table below.

   
    
     
      Comparison row
      What it counts
      Estimate / reported accounting
      Main caveat
     

    
    
     
      VLA Foundry VLA/action stage
      Only the final VLA/action training stage on top of the pretrained Foundry VLM.
      ~0.56 ZFLOPs from ~1.65B trainable parameters, 102.4M samples, and ~549 tokens/sample.
      Does not include LLM or VLM pretraining.
     

     
      Pi-FAST / FAST DROID action tuning
      A representative DROID fine-tuning run for a FAST-style VLA action-token policy.
      ~0.77 ZFLOPs for the 240k-step accounting; the current 100k-step OpenPI config would be ~0.32 ZFLOPs under the same token assumption.
      Sensitive to step count and sequence length; not a paper-reported compute budget.
     

     
      VLA Foundry full LLM→VLM→VLA recipe
      The small from-scratch VLA Foundry path: language pretraining, VLM training, then VLA/action training.
      ~6.9 ZFLOPs, dominated by the 800B-token LLM stage.
      This is a 1–2B open recipe, not a frontier-scale VLA.
     

     
      DreamZero WAM action tuning
      Downstream WAM adaptation of a pretrained Wan-14B video backbone.
      ~8.6–9.0 ZFLOPs for 100k steps, batch 128, and roughly 8.0–8.4k tokens/sequence.
      Excludes the cost of producing Wan and excludes frozen encoder, VAE, communication, and data-pipeline overhead.
     

     
      MolmoAct2 reported VLA stack to DROID
      MolmoAct2-Pretrain, MolmoAct2 post-training, and the DROID embodiment fine-tune, starting from Molmo2-ER.
      ~9.8 ZFLOP-equivalent from reported 5,760 + 2,304 + 1,152 = 9,216 H100-hours.
      Excludes Molmo2-4B, Molmo2-ER specialization, OpenFAST tokenizer training, and upstream Qwen3/SigLIP2 pretraining.
     

     
      Illustrative Wan-14B full WAM stack
      A Wan-scale proxy for video pretraining plus DreamZero-style action tuning.
      ~51 ZFLOPs = 14B-parameter Wan-style video pretraining proxy over 500B tokens + DreamZero-style tuning.
      This is not Summer-22B plus DreamZero; it uses Summer’s token budget as a proxy for Wan-scale video pretraining.
     

     
      Summer-22B video pretraining estimate
      Reported ~500B-token video-pretraining data scale from a from-scratch video model.
      ~66 ZFLOPs from a 22B-parameter model over ~500B video tokens.
      A transparent video-pretraining estimate, not a paper-reported FLOP total.
     

    
   

   Inference speed

   Overall, VLM-based VLAs are not always fast, but default WAM setups with test-time video generation can be even slower. Exact numbers depend on hardware, implementation, diffusion steps, and action-chunk length, but representative values from Fast-WAM [23] give a useful reference: two common WAM inference modes (joint prediction and inverse dynamics with full video generation) take between 590ms and 800ms per action chunk, compared to roughly 190ms for Pi-0.5. That is a 3–4x slowdown at inference time, which matters a lot for real-time control. There are ways to speed this up, as shown in the DreamZero [8] paper and the Fast-WAM approach of skipping video generation entirely, but without access to large GPUs, running these models locally is still challenging.

   Why the modern VLA baseline still matters

   Modern VLM-based VLAs have improved quickly, and the strongest baseline now combines four ideas: discrete action tokenization, VLM-preserving co-training, isolated action heads, and much broader data mixtures. Any claim that video backbones are the better default has to beat the current SOTA recipe.

   The architecture of VLAs has converged to one default setup: the Mixture-of-Transformers recipe, initially introduced in vision by Transfusion [30] and made popular in robotics by Pi-0 [2]. What changed is mostly the training recipe. Early flow-based action heads caused a strong disruption from discrete next-token VLM pretraining to continuous action denoising. Newer recipes try to reduce that disruption.

   First, many modern VLAs use discrete tokenizers like FAST [3] or BEAST [34] to represent actions as a new type of language the VLM can learn. This is motivated by the optimization tension: VLMs are pretrained for discrete next-token prediction with a cross-entropy loss, while robot actions live in a continuous space typically modeled with flow matching. Naively fine-tuning a VLM with flow-matching objectives leads to catastrophic forgetting of the pretrained language and vision capabilities [51]. Co-training with discrete action tokenization, often in combination with isolated gradients from the flow-matching head, sidesteps this issue. The VLM can remain closer to its preferred discrete space and learn useful representations for embodied control, while the flow-matching head conditions on those features for its own action prediction. At test time, systems with a separate action head can drop the slow autoregressive action-token prediction path and let the action head do its job.

   To get some intuition on the impact of this catastrophic forgetting problem, let’s look again at the RoboArena [1] snapshot. Pi-FAST uses the same backbone as Pi-0-DROID, but without the flow component and with discrete FAST tokens for action generation. Both are fine-tuned on DROID. Pi-FAST reaches a score of 1592, while Pi-0 only reaches 1475, which is a fairly large gap. This supports the view that the discrete-action recipe can preserve more useful pretrained capability than the original Pi-0 flow-based setup.

   Second, Pi-0.5-style systems co-train on VLM data and robotics data, often while isolating gradients between the VLM and flow/action components for faster and more stable convergence [4,20]. This lets the VLM continue practicing language and visual understanding while the action side specializes for manipulation. The same pattern appears across recent VLAs such as Pi-0.5, Xiaomi-robotics-0 [27], and Being-H0.5 [28]. Pi-0.5 surpasses both Pi-FAST and Pi-0 on RoboArena by a good margin (1622 vs 1592 for Pi-FAST and 1475 for Pi-0). These results are consistent with the importance of these training design decisions for policy performance.

   Even with these recipe improvements, VLAs still hit the grounding wall. Language is an underspecified way to express goals for behavior. A text instruction in a cluttered scene rarely pins down the relevant object instance or the desired physical state. So policies can overfit to spurious correlations like background objects or other dataset biases. Pi-0.7’s reported gap between language-only prompting and goal-image conditioning supports this view: visual subgoals improve language following and make training converge faster [41]. DreamZero’s 1750 elo-score on the same RoboArena snapshot is another argument that a video/image goal prior can help with this kind of problem.

   So currently there is no real winner between WAMs and VLAs, and it is questionable if there ever will be one. First comparisons like Zhang et al. [25] benchmark LingBot-VA, Cosmos Policy, and Pi-0.5 on LIBERO-Plus and RoboTwin 2.0-Plus under matched perturbations. Their results show that WAMs can reach strong robustness without the broader training-data mixture used by VLA baselines. However, the comparison is limited to simulation environments and does not cover real-world generalization.

   Are the two representation roads actually one?

   The open question is whether the two paths even remain distinct in the long run. Some recent VLAs already use world-model-style components for better goal following (see Pi-0.7), and many recent WAMs borrow from the VLA MoT recipe for the action expert. The future of robot foundation models appears to be a mix of both.

   
    
    
     Figure 25. The likely convergence: VLA-style, WAM-style, and a third universal path that combines both.
    
   
   There are already first signs of this direction in recent works like Motus [17] and BagelVLA [18]. Instead of deciding whether language or video should be the main representation for robotics, train one model that does it all. Figure 26 shows a simplified version: an understanding/VLM component, a video-generation component, and an action expert. Each tower has specialized weights while exchanging information through shared self-attention, often with non-symmetric patterns so each tower can expose different information to the others. Dense transformers or MoE-style routing could implement the same high-level idea.

   
    
    
     Figure 26. A Motus-style hybrid setup: video modeling and action generation are handled by separate transformers while sharing attention and text conditioning, pointing toward a unified VLA+WAM policy recipe.
    
   
   A hierarchical version of this hybrid also appears in Physical Intelligence’s recent Pi-0.7 [41], a steerable VLA whose action expert is conditioned on visual subgoals generated at test time by a BAGEL– based world model [50]. A high-level policy emits subtask instructions, the world model turns those instructions into subgoal images, and the action expert executes conditioned on the current observation plus that subgoal.

   The reported ablations support the language-following argument: adding world-model subgoals improves instruction following on complex referential tasks and is reported as necessary for some dataset-bias-breaking tasks where no-subgoal variants fail. The authors also report that subgoal images make training significantly faster, because action prediction becomes closer to an inverse-dynamics problem between the current frame and a desired future frame. On the evidence ladder, this is a real-world signal that visual subgoals can close part of the language-grounding gap, even inside a VLA-style stack. It does not require the stronger claim that every strong VLA needs a full video-generation head.

   Sereact’s Cortex 2.0 [47] is another startup example pointing in this hybrid direction. Cortex 2.0 adds a world model that generates candidate future trajectories in visual latent space, scores them for expected progress, risk, and efficiency, and conditions execution on the best-scored rollout. This makes it an industry signal for WAM-style foresight becoming a planning layer inside deployed manipulation systems.

   Being-H0.7 [42] is the best example of a foundation-model hybrid: it is a latent-plan-style WAM/VLA built on the pretrained VLA Being-H0.5, with InternVL3.5 as the understanding expert, Qwen3 as the action expert, and V-JEPA2.1 [64] visual encoders. It manages to combine VLA-style pretrained components, V-JEPA2.1 [64] future-observation embeddings, a Play-LMP-style prior/posterior latent interface, and a flow-matching action policy.

   Compute cost is the main reason we have seen only a few “one-model-does-it-all” systems so far. Training a strong VLM is already expensive; layering large-scale video modeling on top compounds the cost. The split between VLA-style and WAM-style training therefore remains useful in the near term, both because of compute limits and because we still do not know which ingredients matter most for robotics. Do you think these two roads genuinely merge, or does one of them win outright?

   A fourth path: Robotics-first foundation models

   A fourth possibility is a robotics-first foundation model (RFFM).  Basically, this would be a large transformer architecture designed around robotics challenges: embodiment, action, contact-rich interaction, and embodied memory. A clean version of this path would not simply start from a web VLM or video generator and then attach actions later. It would make interaction and action central to pretraining from the beginning.

   The cleanest example I am aware of is GEN-1 from Generalist AI, which introduced a large robotic behavior model pretrained on 500k hours of UMI-style wearable data. The core issue for this direction is access: outside of well-funded startups and larger companies, almost no one has access to this kind of large-scale human or robot data. So this research path is currently blocked for the community until we get more open-source robotics data at scale.

   One orthogonal direction worth flagging is latent world models like V-JEPA 2 [45]. They learn latent dynamics directly from video inside pretrained latent spaces. These models promise cheaper rollouts, faster inference, and cleaner planning signals than diffusion-based video generation. First WAMs in this direction, such as VLA-JEPA [63] or Being-H0.7 [42], report promising performance.
   

   Closing thoughts

   WAMs will become a core research subfield of robot foundation models. Whereas VLAs have converged on a roughly shared recipe (VLM backbone, gradient-isolated action expert with flow matching, and co-training on a broad web and robotics mix), WAMs are still in an exploration phase. Papers vary widely in video backbone, policy formulation, training recipe, and evaluation setup. That research diversity is healthy for a young area, and many new ideas are being published. However, no one really knows what works best yet.

   To summarize the conclusions from this blog:

   
    The gap from instruction to motion is still open. Even modern VLAs, with discrete action tokenization, VLM-preserving co-training, and broad data mixtures, do not fully close it. WAMs promise to attack this gap from the video side, but current results do not show that they have solved it yet.

    Robot benchmarking is still a core issue. I have to repeat a finding from my last blog post: modern VLA and WAM benchmarking is not solved. We need more benchmarks like RoboLab [62] or MolmoSpaces [61] that make benchmaxxing harder and require proper policy generalization to get good scores.

    The likely next generation of robot foundation models will be WAM+VLA hybrids. Pi-0.7’s BAGEL subgoals, Cortex 2.0’s planning-by-foresight, Being-H0.7’s latent prior/posterior bridge, and Motus / BagelVLA-style hybrids already merge VLA and WAM thinking. The first robot foundation models trained from scratch are another likely bet, especially once we get access to more and better open-source robotics data.

   

   That’s my current read on where WAMs stand. If you see it differently, or have a strong argument for one of these paths over the others, reach out and let me know — I’d be very happy to hear it.

   
   Footnotes

   
    1. Normalized Compute Accounting: For the bar plot, we use the dense-transformer lower-bound Ctrain ≈ 6 × Ntrain × T, where Ntrain is trainable dense parameters and T is tokens processed. Values are reported in ZFLOPs, with 1 ZFLOP = 1021 FLOPs. The H100-hour intuition uses non-sparse dense BF16-equivalent H100 peak throughput at roughly 30% utilization, giving 1 ZFLOP ≈ 936 H100-hours. This excludes preprocessing, dataloading, optimizer overheads, frozen encoder passes, VAE encoding/decoding, attention terms beyond the simple 6NT approximation, communication overhead, and hardware-specific efficiency. The point is order-of-magnitude normalization, not an exact systems audit.

    
     VLA Foundry LLM pretraining: VLA Foundry [46] releases a Foundry-LLM checkpoint whose model card reports a 1.2B non-embedding-parameter language model trained on 800B DCLM-Baseline-1.0 tokens. Using the underlying 1.23B parameter count used in this estimate gives C ≈ 6 × 1.23B × 800B = 5.9 ZFLOPs, or roughly 5.5k H100-hours.

     VLA Foundry VLM stage: The Foundry-VLM-1.3B-200M model card reports a 1.3B non-embedding-parameter VLM trained on 200M image-caption pairs and initialized from Foundry-LLM-1.2B-800B [46]. The technical report describes 64 image tokens plus variable caption text, padded or truncated to a 256-token total sequence. For the estimate, we count one 256-token multimodal sequence per sample, giving T ≈ 200M × 256 = 51.2B tokens and C ≈ 6 × 1.32B × 51.2B = 0.41 ZFLOPs, or roughly 0.4k H100-hours. This still ignores some implementation overhead and should be read as a lower-bound simplification.

     VLA Foundry VLA/action stage: The Foundry-VLA-1.7B-full model card reports a 1.7B non-embedding-parameter VLA trained on 102M simulated and real bimanual manipulation samples; the paper’s training table reports 102.4M total samples for the Foundry-VLA-1.7B variants [46]. Using an average 549-token sequence estimate gives T ≈ 102.4M × 549 = 56.2B tokens and C ≈ 6 × 1.65B × 56.2B = 0.56 ZFLOPs, or roughly 0.5k H100-hours. Summing the LLM, VLM, and VLA stages gives ~6.9 ZFLOPs for the small from-scratch VLA Foundry LLM→VLM→VLA path that uses the 800B-token LLM checkpoint.

     Pi-FAST / FAST DROID action tuning: FAST [3] supplies the discrete action-tokenization recipe, and OpenPI [48] provides the public Pi-FAST-DROID training/configuration reference. The plotted value uses the earlier 240k-step DROID accounting with global batch 256 and an approximate 700-token sequence (two 224×224 image views plus text/action tokens): T ≈ 240k × 256 × 700 = 43B tokens, so C ≈ 6 × 3B × 43B = 0.77 ZFLOPs, or roughly 0.7k H100-hours. OpenPI’s current public full-DROID fine-tuning config uses 100k steps at batch 256, which would be ~0.32 ZFLOPs under the same 700-token assumption. Treat this row as a representative FAST-scale DROID tuning estimate rather than a canonical fixed cost.

     MolmoAct2 reported VLA stack to DROID: MolmoAct2 [58] reports MolmoAct2-Pretrain at 5,760 H100-hours (200k steps, 4,200-token maximum sequence length, global batch 128, 64 H100s), post-training at 2,300 H100-hours (100k updates, global batch 128, 64 H100s), and the DROID fine-tune at 1,150 H100-hours (100k updates, global batch 64, 32 H100s). We sum these reported numbers to 9,210 H100-hours and convert with the same 1 ZFLOP ≈ 936 H100-hours heuristic, giving ~9.8 ZFLOP-equivalent. This row is not a from-scratch VLA total: MolmoAct2 starts from Molmo2-ER, whose specialization compute is not reported in H100-hours; OpenFAST tokenizer training compute is also not reported; and Molmo2-ER itself builds on Molmo2. Molmo2-4B [59] reports 490 + 7.5k + 3.2k = ~11.2k H100-hours for its own VLM stages, but that still excludes upstream Qwen3-4B and SigLIP2 pretraining.

     DreamZero WAM action tuning: DreamZero [8] reports a 14B Wan2.1-I2V-14B-480P backbone, 100K training steps, global batch size 128 for both AgiBot and DROID, and updates all DiT blocks plus the state/action encoder-decoder while freezing the text encoder, image encoder, and VAE. For the sequence length, we use the paper’s frame/action setup and a Wan-style latent-token approximation: roughly 8.0k–8.4k tokens per sequence after latent compression and grid packing, including video, state, and action tokens. The plotted upper estimate uses 8,361 tokens, giving T ≈ 100k × 128 × 8,361 = 107B tokens and C ≈ 6 × 14B × 107B = 9.0 ZFLOPs, or roughly 8.4k H100-hours for the core DiT update. Using a slightly shorter 8.0k-token accounting gives ~8.6 ZFLOPs. Frozen encoder, VAE, communication, and long-sequence efficiency overheads are still excluded.

     Summer-22B video pretraining: Summer-22B [47] reports a 22B-parameter video diffusion model trained from scratch on approximately 50M clips, described as about 500B video tokens. Using C ≈ 6 × 22B × 500B gives 66 ZFLOPs, or roughly 62k H100-hours.

     Illustrative full WAM stack: Because Wan-14B pretraining compute is not reported, we include a transparent proxy that adds Summer-22B-style video pretraining to DreamZero-style WAM action tuning: 66 + 9.0 = 75.0 ZFLOPs, or roughly 70k H100-hours before extra overhead. This is not a reported DreamZero total and should not be attributed to Wan. It is meant to show the scale of a full video-pretraining-plus-action-tuning path when the video backbone is not treated as free.

     Wan-14B pretraining: Wan [21] reports a 14B video model trained on a large curated image/video corpus, but does not disclose a token count or complete training compute budget. Since DreamZero starts from Wan2.1, the DreamZero action-tuning number should be read as downstream WAM adaptation cost only, not the full cost of producing the underlying video backbone.

    

    These are lower-bound dense-core estimates, and several rows are recomputed estimates rather than paper-reported compute budgets. They are useful for comparing the rough location of compute across training recipes, but they should not be read as exact wall-clock cost, cloud cost, or end-to-end energy use. ↩

    2. UniPi / CNN Diffusion Compute Details: Estimating the FLOPs for the 3D U-Net used in UniPi (which inherits the Imagen Video base architecture) requires a different approach than the Chinchilla formula used for Transformers. Because Convolutional Neural Networks share weights as kernels slide across spatial and temporal dimensions, compute scales drastically with resolution and frame count. Numbers below are rough order-of-magnitude estimates and should be treated as such.

    
     
      
       Forward Pass: The base model generates 16 frames at 24×40 resolution (15,360 total pixels). Factoring in the spatial downsampling of the U-Net architecture, the “effective” pixels processed across all 1.7B parameters is roughly 4,000 per video.
        

        Forward FLOPs ≈ 2 × 1.7B × 4,000 ≈ 13.6 TFLOPs per video.

      

     

    

    

    
     Total Training FLOPs: Training ran for 2,000,000 steps at a global batch size of 2,048. Factoring the standard multiplier of 3 for the forward and backward passes:
      

      C = 3 × 13.6 TFLOPs × 2048 × 2,000,000 ≈ 1.67 × 1023 FLOPs.

    

    To put this in perspective, this is ~167 ZFLOPs. Under the 936 H100-hours/ZFLOP intuition above, that is roughly 156,000 H100-hours; using a lower measured effective-throughput assumption of ~224 TFLOPS/GPU gives roughly 207,000 H100-hours. Even though UniPi’s 1.7B parameter count is much smaller than DreamZero’s 14B, the requirement to pre-train a video foundation model from scratch likely made early WAM-style recipes prohibitively expensive for most robotics labs. The recent momentum is partly driven by open pretrained video models (like Wan), which allow researchers to skip this 1023 FLOP pre-training phase. ↩

   

   Acknowledgements

   The author thanks Alexander Schwarz, Ankit Goyal, Elie Aljalbout, Fabio Ramos, Seonghyeon Ye, Shenyuan Gao, Xuning Yang, Yashraj Narang, and Yixuan Wang (listed alphabetically by first name) for insightful feedback and discussions that improved this post.

   Sources

   
    Atreya, Pranav, et al. “RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies.” CoRL 2025. paper

    Black, Kevin, et al. “Pi-0: A Vision-Language-Action Flow Model for General Robot Control.” arXiv 2024. paper

    Pertsch, Karl, et al. “FAST: Efficient Action Tokenization for Vision-Language-Action Models.” arXiv 2025. paper

    Physical Intelligence, et al. “Pi-0.5: A Vision-Language-Action Model with Open-World Generalization.” arXiv 2025. paper

    Bjorck, Johan, et al. “GR00T N1: An Open Foundation Model for Generalist Humanoid Robots.” arXiv 2025. paper

    Liu, Bo, et al. “LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning.” NeurIPS 2023. paper

    Mees, Oier, et al. “CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks.” RA-L 2022. paper

    Ye, Seonghyeon, et al. “World Action Models Are Zero-shot Policies.” arXiv 2026. paper

    Li, Lin, et al. “Causal World Modeling for Robot Control.” arXiv 2026. paper

    Du, Yilun, et al. “Learning Universal Policies via Text-Guided Video Generation.” NeurIPS 2023. paper

    Wu, Hongtao, et al. “Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation.” ICLR 2024. paper

    Cheang, Chi-Lam, et al. “GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation.” arXiv 2024. paper

    Kim, Moo Jin, et al. “Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning.” arXiv 2026. paper

    Pai, Jonas, et al. “mimic-video: Video-Action Models for Generalizable Robot Control Beyond VLAs.” arXiv 2025. paper

    Nair, Suraj, et al. “R3M: A Universal Visual Representation for Robot Manipulation.” arXiv 2022. paper

    Karamcheti, Siddharth, et al. “Language-Driven Representation Learning for Robotics.” arXiv 2023. paper

    Bi, Hongzhe, et al. “Motus: A Unified Latent Action World Model.” arXiv 2025. paper

    Hu, Yucheng, et al. “BagelVLA: Enhancing Long-Horizon Manipulation via Interleaved Vision-Language-Action Generation.” arXiv 2026. paper

    Bruce, Jake, et al. “Genie: Generative Interactive Environments.” ICML 2024. paper

    Driess, Danny, et al. “Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better.” NeurIPS 2025. paper

    Wan Team, et al. “Wan: Open and Advanced Large-Scale Video Generative Models.” arXiv 2025. paper

    Agarwal, Niket, et al. “Cosmos World Foundation Model Platform for Physical AI.” arXiv 2025. paper

    Yuan, Tianyuan, et al. “Fast-WAM: Do World Action Models Need Test-time Future Imagination?” arXiv 2026. paper

    Hu, Yucheng, et al. “Video Prediction Policy: A Generalist Robot Policy with Predictive Visual Representations.” ICML 2025. paper

    Zhang, Zhanguang, et al. “Do World Action Models Generalize Better than VLAs? A Robustness Study.” arXiv 2026. paper

    Schäfer, Lukas, et al. “When does predictive inverse dynamics outperform behavior cloning?.” arXiv preprint arXiv:2601.21718 (2026). paper

    Cai, Rui, et al. “Xiaomi-robotics-0: An open-sourced vision-language-action model with real-time execution.” arXiv 2026. paper

    Luo, Hao, et al. “Being-H0.5: Scaling Human-Centric Robot Learning for Cross-Embodiment Generalization.” arXiv 2026. paper

    Tian, Yang, et al. “Predictive Inverse Dynamics Models are Scalable Learners for Robotic Manipulation.” ICLR 2025. paper

    Zhou, Chunting, et al. “Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model.” ICLR 2025. paper

    Shridhar, Mohit, Yat Long Lo, and Stephen James. “Generative Image as Action Models.” CoRL 2024. paper

    Lynch, Corey, et al. “Learning Latent Plans from Play.” CoRL 2020. paper

    Ye, Seonghyeon, et al. “Latent Action Pretraining from Videos.” ICLR 2025. paper

    Zhou, Hongyi, et al. “BEAST: Efficient Tokenization of B-Splines Encoded Action Sequences for Imitation Learning.” NeurIPS 2025. paper

    Chi, Cheng, et al. “Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots.” RSS 2024. paper

    Chi, Cheng, et al. “Diffusion Policy: Visuomotor Policy Learning via Action Diffusion.” IJRR 2025. paper

    Ma, Teli, et al. “DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control.” arXiv 2026. paper

    Zhang, Wenyao, et al. “DreamVLA: A Vision-Language-Action Model Dreamed with Comprehensive World Knowledge.” NeurIPS 2025. paper

    Li, Shuang, et al. “Unified Video Action Model.” arXiv 2025. paper

    Rhoda AI Team. “Causal Video Models Are Data-Efficient Robot Policy Learners.” Rhoda AI Blog, 2026. blog

    Physical Intelligence. “Pi-0.7: a Steerable Model with Emergent Capabilities.” Physical Intelligence Blog/Paper, April 2026. blog, paper

    Luo, Hao, et al. “Being-H0.7: A Latent World-Action Model from Egocentric Videos.” arXiv 2026. paper, project page

    Assran, Mido, et al. “V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning.” arXiv 2025. paper

    Gao, Shenyuan, et al. “DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos.” arXiv 2026. paper

    Aida, Adriana, et al. “Cortex 2.0: Grounding World Models in Real-World Industrial Deployment.” arXiv 2026. paper, project page

    Mercat, Jean, et al. “VLA Foundry: A Unified Framework for Training Vision-Language-Action Models.” arXiv 2026. paper, model collection

    Ryu, Simo, and Chunghwan Han. “Summer-22B: A Systematic Approach to Dataset Engineering and Training at Scale for Video Foundation Model.” arXiv 2026. paper

    Physical Intelligence. “openpi.” GitHub repository, 2025-2026. code

    Zhang, Jianke, et al. “VLM4VLA: Revisiting Vision-Language-Models in Vision-Language-Action Models.” arXiv 2026. paper

    Deng, Chaorui, et al. “Emerging Properties in Unified Multimodal Pretraining.” arXiv 2025. paper

    Hancock, Asher J., et al. “Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting.” ICLR 2026. paper, project page

    Ho, Jonathan, et al. “Imagen Video: High Definition Video Generation with Diffusion Models.” arXiv 2022. paper

    Wang, Lirui, et al. “Prediction with Action: Visual Policy Learning via Joint Denoising Process.” arXiv 2024. paper

    Wen, Junjie, et al. “Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets.” arXiv 2025. paper

    ByteDance Seed. “GR-1.” GitHub repository, 2024. released config

    Wan-Video Team. “Wan2.2.” GitHub repository, 2025. release

    Hou, Bohan, et al. “World Model for Robot Learning: A Comprehensive Survey.” 2026. project page, repo

    Fang, Haoquan, et al. “MolmoAct2: Action Reasoning Models for Real-World Deployment.” arXiv 2026. paper, model

    Clark, Christopher, et al. “Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding.” arXiv 2026. paper, model

    Reuss, Moritz. “State of VLA Research at ICLR 2026.” Blog post, October 2025. blog

    Kim, Yejin, et al. “MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation.” arXiv 2026. paper

    Yang, Xuning, et al. “RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies.” arXiv 2026. paper

    Sun, Jingwen, et al. “VLA-JEPA: Enhancing Vision-Language-Action Model with Latent World Model.” arXiv 2026. paper

    Mur-Labadia, Lorenzo, et al. “V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning.” arXiv 2026.

   

   Cite this post

   If you’d like to cite this article, use the BibTeX below:

  

  
   @misc{reuss2026state-wam,
  title        = {Pretrained to Imagine, Fine-Tuned to Act: The Rise of World-Action Models},
  author       = {Reuss, Moritz},
  year         = {2026},
  month        = {June},
  organization = {Seattle Robotics Lab (SRL), NVIDIA},
  howpublished = {\url{https://developer.nvidia.com/blog/pretrained-to-imagine-fine-tuned-to-act-the-rise-of-world-action-models}},
  note         = {Blog post},
}
