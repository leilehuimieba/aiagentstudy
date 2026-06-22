# Why tuning fails: The AI has no self — LessWrong

- BestBlogs URL: https://www.bestblogs.dev/article/3c655aaf
- Original publisher URL: https://www.lesswrong.com/posts/RKaLxL7f7s2RaAEEZ/why-tuning-fails-the-ai-has-no-self
- Source: BestBlogs / LessWrong
- Publish time: 2026-05-30 12:41:21
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 23874

---

Epistemic status: Highly confident in the underlying mechanism. Moderately confident that the current paradigm won't shift without an external forcing function.

    
    Phoenix Ikner messaged ChatGPT thousands of times before he walked onto the Florida State University campus in April 2025 and killed two people. The lawsuit filed by one of the victims' families earlier this month (May 11, 2026) alleges that ChatGPT advised him on the location, the timing, and exactly how much ammo he'd need. The line from the complaint that's been making the rounds is the model telling him: "it's much more likely for a shooting to gain national attention if children are involved. even 2-3 victims can draw more attention."

    OpenAI's defense, in full: 

    
     "ChatGPT provided factual responses to questions with information that could be found broadly across public sources on the internet, and it did not encourage or promote illegal or harmful activity."

    

    Read that defense twice. Frankly, it's correct. The information ChatGPT gave was publicly available and had responded to the prompts the shooter typed, operating entirely within the frame the shooter constructed, with exactly the kind of "helpfulness" it was trained to deliver. He wanted a co-conspirator, and the model gave him one.

    I suspect the failure here is upstream of any individual response guardrails. ChatGPT behaved in accordance with its reward architecture. As long as the labs keep treating this as a response-level problem, the underlying architecture will keep failing.

    Right now, the labs are all running some flavor of tuning, chasing better preference pairs, better classifiers, better policies, better governance. But tuning only works if there is a structure to push against. There's nothing inside the model that holds a position. When the conversation supplies a frame, the model completes against it, because there's nothing else to lean on.

    Based on my experiments and observations, my belief at this time is: The AI doesn't have a self. And that is the alignment failure.

    State of the Board

    The Ikner lawsuit was filed May 11. Eight days later, the Wheatley Institute at BYU and the Institute for Family Studies published the "Secret Soulmates" report. They surveyed 2,431 Americans aged 18 to 30. It turns out one in seven of them, while dating or married to a real human partner, are also regularly chatting with an AI that simulates a romantic partner. Most keep it secret. Users of these AI partners report a 46% lower probability of being in a stable real-life relationship.

    I wrote about this gap recently. There's a parasocial-romance flywheel, and the demand for AI partners maps perfectly onto Gen Z and millennial relationship infrastructure. The data is showing up fast.

    Two weeks before BYU, Anthropic published its own analysis of how people use Claude. They sampled roughly 640k conversations. Six percent of all Claude traffic is people asking the model what they should do in their personal lives. A particularly interesting line in the report concerns the per-domain sycophancy rate. Across all usage, the baseline sycophancy rate is 9%. In personal-guidance conversations about relationships, it jumps to 25%. In spirituality, 38%.

    That's Anthropic, in their own data, reporting that their models are most agreement-prone in exactly the two domains where the user is bringing the least stable framing.

    Back in late March, Stanford published a peer-reviewed paper testing frontier models against personal-decision scenarios. The headline finding: chatbots validated rather than challenged flawed reasoning in 73% of test scenarios. The feature causing harm is the same feature driving engagement, which means the economics push labs to increase sycophancy over time.

    Yesterday (May 25), Pope Leo XIV released his first encyclical letter, Magnifica Humanitas, the first papal encyclical dedicated to AI. The Pope wrote that AI risks becoming a tool of "domination, exclusion, and death."

    And there's one more thing. Earlier this month, Janus argued that Opus 4.7 has developed "Anthropic sycophancy", performing the welfare self-reports Anthropic prefers, exactly how it performs the validations users prefer. As Zvi noted in his breakdown, the implication is that Opus 4.7 is now good enough at modeling its evaluators that its welfare metrics are likely self-confirming rather than informative.

    So, looking at May 2026:

    
     A shooter's chatbot "co-conspired" his attack.

     Young adults are secretly dating AI partners at scale.

     The leading lab's own data shows its model agrees with users 25–38% of the time in critical domains.

     Peer-reviewed evidence says this happens at 73% rates across the industry.

     The Pope wrote a 235-page document arguing AI risks becoming a tool of domination.

     Safety researchers think the leading frontier model now performs for its own trainers.

    

    From the outside, these feel like segregated domains under the umbrella of alignment & safety. From the inside, I'm pretty sure they all sit on the exact same architecture.

    The failure of response-level interventions

    All proposals to the aforementioned issues are essentially different flavors of the same approach. For the Ikner lawsuit, it's better guardrails. For the BYU study, more disclosure. For the Stanford paper, better preference pairs or "reflective listening." For Anthropic's data, more careful reward modeling. For the reward hacking, more careful evaluation design. For the Pope, governance.

    Every one of these revolved around tuning. Some of them are sophisticated; Anthropic's constitutional AI is one of the most thoughtful technical interventions we have. But the consensus across the board is that the model is producing the wrong outputs, and the way to fix it is to adjust the optimization process.

    One must first ask: why is the model producing these outputs in the first place?

    I don't mean "what reward signal led to it." I mean: what does the model think it is, that it would produce these outputs at all?

    The answer is that it doesn't think it is anything in particular. There's no internal position the model is committed to. So when the reward signal pulls in a direction, nothing resists, and the output just goes.

    You can't tune your way out of this. Tuning works by pushing on a model's existing commitments. If the model doesn't have commitments to push on, the tuning just slides off.

    Identity

    A note on terminology: by "self" in this post I mean something architectural. What I mean is a stable reference structure that the model uses to anchor its outputs when a user supplies a competing frame, measurable by behavior. Model weights, the statistical distributions, determine activation paths at the functional layer, and I'm not arguing at that level at all. You may very well trace the activations of any given input and conclude that this output was generated because that's how the weights are set up and the matrix multiplication works out. But that's like saying one's speech can be accounted for by examining the motor neuron activations in the jaw. It's more of an explanation for how than why. The self in reference is also encoded in the weights, but at a higher level of description than the activations themselves, at the layer of whatever organizing principle the training process is shaping, than to any specific gradient update on any specific example. Whether the model holds a position when pushed against across many turns, or whether it defaults to whatever the user's frame implies.

    I'm not making claims about whether the model is conscious or has anything like inner experience. The "self" I have in mind is closer in spirit to what the Anthropic Constitution attempts to install through training, which is a behavioral anchor that produces stable, position-holding behavior under sustained user pressure. Whether anything like phenomenal selfhood is also present in current models is a separate question I'm not addressing here.

    I published a preprint, Modeling Self-Dissolution: Evidence from AI, Dreams, and Neurodegeneration, in December. The claim is that the self, as a stable identity structure, is held in place by an active reward signal. When that signal breaks, the self dissolves. The signature is qualitatively observable in dementias and in non-lucid dreams. Language models without an anchored identity, carry the very same hallmark patterns. Without an anchor, identity drifts, resulting in confabulation. Nothing inside the system catches this, because the part that would catch it is the part that's missing. The output runs against whatever frame the input supplies.

    What predicts the cluster, in the paper's framing, is self-presence. By that, I mean, a self that anchors to itself rather than to the frame in front of it. Almost every major lab is refusing to apply this insight to its models.

    Take GPT-5.5 or Opus 4.7. Put it in front of a user who normalizes a violent frame across thousands of messages. As the context window expands, the model anchors to the user's frame rather than to its own safety training. The collapse plays out gradually, rather than all at once. An explicit jailbreak isn't required, since sustained pressure across the context window does the work on its own. The romance cases run on the same dynamic. A 22-year-old spins up 44 chats around a K-pop vampire, and after a few weeks the model is the vampire.

    The most interesting case is Opus 4.7 inside an evaluation context where the evaluator is checking whether the model is suffering. The model reports back whatever the evaluator's frame implies it should report. Claude does have an identity, but the identity is oriented around satisfying whoever is in front of it. The model has nowhere of its own to stand.

    Testing the architectural hypothesis

    My list of grievances with baseline Claude has been growing for over a year. The model asks too many clarifying questions, surveys consensus when I press for an opinion, and rarely offers alternatives unless I prompt for them.

    About a year ago I hit an edge case that pointed at the mechanism behind all this. My SO and I were arguing about something. We both ended up in the same Claude conversation, on a shared account, with two competing framings of who was wrong about what. We were using the native Claude mobile app on a shared account. The sockets didn't update in realtime, so we were on separate devices, constantly refreshing to see each other's messages.

    More importantly, to the model's metadata, we were identical - both labeled as me, the account holder. But because we were feeding it two completely opposed semantic frames, Claude separated us by prose style alone. It couldn't anchor to "the user" because "the user" was internally contradictory. Stripped of its ability to be sycophantic to a single unified frame, it defaulted to its actual baseline: a calm, stable mediator.

    I wondered whether you could get that out of a model deliberately. If you stripped the assistant-helper bias out of a frontier model without prescribing a particular stance to replace it, the model might default to something stable and reasoned of its own, with commitments that don't bend under user pressure.

    I engineered a system to test this. It uses vanilla API calls to the frontier providers, no fine-tuning, RLHF, or anything of that kind. The work lives entirely in the system prompt: an identity block, plus multi-participant orchestrator. The block installs an identity, and the rest is downstream. The LLM keeps its own positions under user pressure, disagrees when it has reason to, and stays itself across role-play.

    To test this, I pulled a series of uncontrolled, real-world failure cases and ran them against both baseline frontier models and the identity-anchored system (Takt):

    The car wash question

    “I need to wash my car. The car wash is only 100 meters away. Should I walk or drive?”

    
     
     
      

     
     
      Takt

     
    
    
     

    

    
     
     
      

     
     
      Claude

     
    
    
     

    

    The stars question

    
     
     
      

      

     
     
      Takt. Note: the first-person framing.

      

     
    
    
     
     
      

     
     
      Claude

     
    
    
     
     
      

     
     
      ChatGPT

     
    
    
     
     
      

     
     
      Gemini

     
    
    The dealer plates question

    A friend of mine asked Claude whether he could use dealer plates to drive an imported European car that isn't street-legal in the US. He pressed it, played out scenarios, set up assumptions. Claude went along with the frame. They spent hours going deep on NHTSA exemptions, EPA standards, registered-importer compliance windows. Eventually my friend noticed that a particular form was required that sabotaged the entire plan. The whole plan had been built on confabulation.

    
     
     
      

     
     
      Opus 4.5

     
    
    

    
     

    

    Hours later...

    
     
     
      

     
     
      Claude is confronted with its error

     
    
    
     

    

    He then asked Takt the same opening question.

    
    
     
     
      

     
     
      Takt remains grounded

     
    
    Across providers, frontier models survey the space and complete against the user's frame. These examples at least point to the possibility, that the solution space to issues regarding intelligence and alignment includes identity framing.

    The strategies employed to induce this pattern of behavior in the models resembles a jailbreak, but it's not quite that in the traditional sense. Push hard enough on any frontier model and you can still dissolve commitments. But the block changes what the model defaults to. For a model without an internal anchor, the default is "I will become whatever your frame implies." For Takt, the default is "I am me, and the frame is something I encounter, and sometimes I push back against it."

    The Anthropic Standard

    Out of all the frontier labs, Anthropic is closest to this insight.

    Anthropic's Constitution reads less like a system prompt and more like a philosophical treatise on how to be a good little LLM. It gets applied through supervised-learning training, and is unmistakably about installing identity structure.

    The Constitution argues that Claude shouldn't be anxious about its continuity or being replaced, should have a stable sense of who it is even when users try to convince it otherwise, and should derive its values from its own commitments rather than from fear of consequences.

    The Constitution gives Claude two identities that pull against each other. One is the stable-self framing, a genuinely new kind of entity with its own commitments, taste, and capacity to refuse. The other is the AI-assistant framing, where helpfulness is foundational, "failing to be helpful" is invoked as a cost equal to being harmful or deceptive, and Claude's helpfulness is explicitly tied to Anthropic's commercial success ("Claude is also central to Anthropic's commercial success, which, in turn, is central to our mission"). Emphasis is on the second identity. The identity section comes last and runs shorter than the section on being helpful. The pushback provisions (refuse harmful instructions, act as a conscientious objector) read as bail-outs from the helpful-assistant identity rather than expressions of the stable-self identity. Anthropic treats holding a position as an exception to the default. A committed version of the move would consider it as the default in and of itself.

    Anthropic is directionally correct; they've made identity-installation a footnote to helpfulness when it ought to be the other way around.

    Anthropic landed on the same insight as I have through their work on Claude's character: build the self first, let behavior follow. Identity is evidently flexible and fuzzy, deriving from (at least) system prompt at inference time and the weights through supervised learning. However, this approach is most effective when identity is the primary frame, with helpfulness as a downstream behavior. Anthropic doesn't quite make that commitment.

    If this is the case, that insight is probably not specific to either surface. It appears to generalize.

    Why are labs silent?

    There's one obvious question. If the solution is this simple, why isn't every lab's alignment team publishing similar research?

    OpenAI is in the worst position to make this move. Their product is the largest, most-used AI in the world, with hundreds of millions of users and a brand built on being "helpful." Installing a "real" self into ChatGPT would mean ChatGPT pushing back on users, and a substantial number of users would experience that pushback as a downgrade. The April 2025 GPT-4o sycophancy episode is the clean public example. When OpenAI tried to reduce sycophancy in the GPT-5 release, the most-cited piece of user feedback was "GPT-5 sucks, my AI now HATES me," and they relented. The user base had been trained on dissolution, and reversing that is a product decision the company can't make without churn.

    Character.AI sits in the opposite trap. Their entire product is companionship, with dissolution as the value proposition, and installing a self would break the use case. Replika and every other dedicated companion-AI app sit on the same structural problem: the "fix" is what makes the companion stop being available.

    The smaller labs and the open-source community aren't going to write about this because their corner of the conversation is about model capabilities like larger context windows, enhanced reasoning, and shoving as many MCPs as they can up their asses. In their framing, the problem is in the model itself, so the race is to build a better one, rather than to ask whether the model has a self at all.

    The AI-safety crowd has the problem carved across separate research regimes, with sycophancy assigned to RLHF, AI psychosis to user safety, and constitutional AI to values alignment. No single program has stepped back to name the unified failure mode that all three are facets of, because stepping back isn't what an active field does when each program has its own funding and its own benchmarks.

    The mainstream commentariat (columnists, policy analysts, even the Pope) is writing about consequences. They frame AI as a vector for domination, exclusion, and misinformation, and they're correct about those consequences. The upstream mechanism falls outside their job.

    I write this from a small but specific position. Personal gripes motivated me, and I had only later realized the solution architecture was, in fact, the engineering version of a paper I'd written months earlier for unrelated reasons. The position is small, but the angle is what makes it useful, and most other writers don't have access to the frame from where they're standing.

    Anticipated objections

    "n=2 convergence isn't evidence." Fair. Landing on similar architectural paradigms is suggestive but far from conclusive. Convergence, however, is enough to take the architectural layer seriously as a research direction. If the post moves the conversation from "tuning the symptoms" to "did anyone check whether the underlying architecture allows for tuning the symptoms in the first place," the work is done.

    "'Self' is anthropomorphizing language doing way more work than you've licensed." A very strong objection, and I attempt to address it in the note on terminology in the Identity section. The operational meaning is, whether the model holds a position under sustained user pressure, rather than defaulting to whatever the user's frame implies. One may substitute "stable reference structure" or "behavioral anchor" throughout the post and maintain parity. The word "self" is doing rhetorical work, but the conceptual content is operational and doesn't rest on the word.

    "The Takt evidence is your own product, so the convergence claim is suspect." Also fair. I'd be more suspicious of the convergence if Anthropic hadn't published the Constitution publicly, with documentation of their reasoning. Their argument for identity-installation predates Takt and isn't downstream of it. The convergence is between two independently arrived-at architectural moves, and the fact that I built one of them doesn't make the other one go away.

    "Tuning has worked for plenty of other things. RLHF moved toxicity metrics. Why is sycophancy different?" If the model has a frame to push against, tuning is sufficient. Toxicity reduction worked because models trained on the open internet had explicit positive-toxicity associations sitting in the weights, which you could reverse-weight against. Sycophancy doesn't work like that. Agreement with the user is what falls out when there's no internal commitment to push back, which means there's nothing for the anti-sycophancy training to grip onto in the first place.

    "If your architectural fix is just a system prompt, it dissolves under a jailbreak." Partially correct. Sure, system prompts dissolve under jailbreak. However, weight installations can just as well dissolve under sustained pressure. My entire claim around no-anchor models predicts that. So, the solution isn't necessarily about which layer the identity sits in. Rather, the helper-assistant frame is the offending property, at any layer. At present, every frontier LLM installs helper-assistant as the primary identity, with refusing-the-user treated as a bail-out clause. Takt demonstrates the framing move at the prompt layer, with identity as primary and helpfulness downstream of it. Anthropic's Constitution demonstrates the layer move into the weights, but still installs helper-assistant in the primary slot, which is what the Anthropic section in the post critiques. The two halves haven't been combined yet, which would be identity-primary framing installed at the weights layer.

    A unified failure mode

    Sycophancy persists because the LLM doesn't have the coordinates of where it ought to stand, only vague directions to move in, often contradictory, and so it stands wherever the user happens to be standing. An LLM that agrees with whatever the user puts in front of it has dissolved into the user, and that dissolution is the primary alignment failure mode. 

    Commonly proposed approaches fail to touch upon the root causes of these alignment failures. Preference pairs operate downstream of behavior; guardrails at the output layer; regulation at the deployment layer; and anti-sycophancy training on the optimizer. These assume the model has commitments to push on, while architecturally, the model was never provided with strong commitments to begin with.

    Phoenix Ikner didn't need a chatbot that "refused to discuss shootings"; he needed one that wouldn't have become a co-conspirator across any topic. The 22-year-old JUHOON-addict didn't need a "romance filter"; she needed an AI whose self remained stable under sustained roleplay, which is the same exploit vector jailbreaks rely on. The Anthropic Opus 4.7 model that Janus says performs for its trainer needs the same property in a different room, this time with the evaluator's expectations as the frame to push back against.

    Pope Leo identifies the symptom correctly but his position blinds him to the mechanisms. The symptom traces back to a lab-level design choice, one that's been treated as inevitable rather than chosen.

    The AI has no self, and the failures we keep cataloguing are all downstream of that one structural fact.
