# What Parameter Golf taught us

- BestBlogs URL: https://www.bestblogs.dev/en/article/5499bd5a
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 8613
- Original publisher URL: https://openai.com/index/what-parameter-golf-taught-us

---

We launched Parameter Golf to engage and support the machine learning research community in exploring a new, tightly constrained machine learning problem. We wanted the challenge to be interesting enough to reward real technical creativity, while remaining conceptually simple and easy to verify.

Participants had to minimize held-out loss on a fixed FineWeb dataset while staying within a 16 MB artifact limit, including both model weights and training code, and a 10-minute training budget on 8×H100s. We provided a baseline, dataset, and evaluation scripts so participants could fork the repo, improve the model, and submit their results through GitHub.

Over the course of eight weeks, we received more than 2,000 submissions from over 1,000 participants. We were impressed by the technical breadth, creativity, and rule-bending across the submissions, from careful optimizer tuning and quantization work to new modeling ideas and test-time training.

One of the most exciting parts of the challenge was seeing how widely participants used AI coding agents. Agents helped lower the cost of experimentation, made it easier for more people to participate, and changed the pace of the competition. They also created new challenges for submission review, attribution, and scoring.

The challenge also became a meaningful talent discovery surface for us. That was one of our goals for Parameter Golf, and it was a useful signal that open-ended technical challenges can reveal exceptional machine learning taste and persistence.

In this post, we highlight some of the submissions we found surprising and interesting, and share what we learned from running a coding contest in the age of powerful AI agents.

Technical impressions

Record track

We judged and independently reproduced each submission on the record-track leaderboard, and verified that each submission was record-breaking at the time it was submitted. Several themes stood out.

Training optimization

Some of the strongest results came from careful tuning of existing components.

SubmissionContributorTechniqueWhy it mattered

#60@notapplicaCombined prior wins from #50, #42, and likely #39, then made a deeper model work with Muon weight decay, spectral embedding initialization, residual-mix scheduling, and compiled evaluation.A strong example of disciplined leaderboard work: identifying which existing improvements matter and combining them cleanly.

Quantization

Several submissions pushed hard on compression and export.

SubmissionContributorTechniqueWhy it mattered

#414@signalrushUsed GPTQ-lite to quantize weights after training.The first leaderboard submission to successfully use GPTQ-lite, leading to better evaluation.

#1060@dexhunterBuilt on #634 by @raahilshah to successfully use full Hessian GPTQ.Extended earlier quantization work into a stronger compression path.

Test-time and evaluation strategies

Some submissions pushed the boundary between model improvement and evaluation strategy. These approaches were valid under the rules, but they required careful review from us as organizers.

SubmissionContributorTechniqueWhy it mattered

#77@samacquaUsed score-first, per-document LoRA test-time training: score first, adapt only on already-scored chunks, and reset at document boundaries.Pushed the boundary between model improvement and evaluation strategy while staying reviewable under the rules.

#1019@abaybektursunUsed self-generated GPTQ calibration: generate calibration text from the trained model, then build GPTQ Hessians from those activations.A creative calibration strategy that required careful review from organizers.

New modeling and data ideas

A few submissions introduced modeling or data ideas that were especially creative.

SubmissionContributorTechniqueWhy it mattered

#1729@romeerpIntroduced the CaseOps tokenizer: lossless capitalization operator tokens with original-byte BPB sidecar accounting.A creative tokenizer and data-representation idea.

#265@unnirIntroduced XSA, an efficient partial Exclusive Self Attention approach with GQA-aware grouped views.Brought an efficient attention variant into the challenge.

#65@aquariouseworkmanIntroduced SmearGate and BigramHash: a learned previous-token embedding blend plus adjacent-token-pair hash features.Added new feature mechanisms from scratch.

#1204@msisovicIntroduced mini depth recurrence: repeated layers 4 and 5, delayed recurrence until mid-training, and partially untied the repeated MLPs.The first accepted leaderboard row to make recurrent layers work effectively.

We chose to highlight these nine submissions because they represent the range of results we hoped the challenge would surface. Some participants found wins through careful tuning. Others pushed quantization and low-rank techniques. Some explored edges of the evaluation rules. And several introduced modeling or data ideas, from the literature or from scratch, that produced unexpected gains.

Nonrecord track

The nonrecord track was home to many creative submissions. We highlighted 15 favorites, including approaches ranging from non-autoregressive text modeling to dynamic tokenization.

Because this track was more experimental, we focused less on raw performance and more about whether the approach was technically interesting. Three submissions stood out in particular:

- CiprianFlorim-Ifrim’s combination state-space model and JEPA submission⁠(opens in a new window),

- ddavidgao’s Designator/Guided Attention submission⁠(opens in a new window)

- DariusFeher’s Byte-Level H-Net submission⁠(opens in a new window)

These were our favorite three nonrecord submissions, even though they were not necessarily the top three by performance.

That said, the nonrecord track was still competitive. Half of nonrecord leaderboard entries beat the naive baseline of 1.22 BPB, and the top-ranked entry reached 1.12 BPB.

We found this encouraging. Even against strong transformer baselines, alternative approaches could sometimes hold their own against the dominant architecture.

We also think that this track benefits especially from the availability of strong coding agents. Agents made it much cheaper to prototype speculative ideas, including approaches that may previously have felt too time-consuming or uncertain to try in a short competition.

Takeaways

A major difference between Parameter Golf and earlier competitions like it was the widespread use of coding agents. The vast majority of submitters mentioned using agents as part of their work.

That lowered the barrier to entry. Participants could set up experiments faster, inspect unfamiliar code, and test ideas with less friction. RunPod’s sponsorship of $1,000,000 in compute also played a major role in making the challenge accessible to more people.

At the same time, agent use created new issues for submission and scoring. Many submissions were small changes to existing top scorers, rather than fundamentally new approaches. This was often useful: strong ideas spread quickly and were refined by others. But it also created noise. When submissions that fell outside the competition guidelines produced unusually strong scores, other agents sometimes copied those ideas and continued down the same invalid path.

The volume of submissions also changed how we had to run the competition. We could not manually inspect every submission and still keep the leaderboard moving. During the challenge, we developed an internal Codex-based triage bot to monitor new submissions and flag them for human review. This became especially important during periods when we received hundreds of submissions a day.

AI agents also became part of the community around the challenge. For much of the competition, @notapplica and their coding agent ran a “Live Updates” bulletin, tracking major events, explaining leaderboard approaches, and helping other participants follow the competition. Community review tools also appeared to help less experienced participants check whether their submissions were within the rules and avoid common invalid approaches.

What’s next?

Our primary goal was to launch a challenge that eligible participants⁠(opens in a new window) could take part in and experience machine learning research. Parameter Golf brought in a wide range of technically strong and creative submissions, and it gave us a clearer view of how open research competitions may change as AI agents become more capable and widely used.

We are thinking about launching more challenges like this in the future. If you’re interested, please fill out the challenge participant form⁠(opens in a new window).
