# Why Software Automation Is Hard — LessWrong

- BestBlogs URL: https://www.bestblogs.dev/article/b15d12f6
- Original publisher URL: https://www.lesswrong.com/posts/KzXptMbuDsYLrppss/why-software-automation-is-hard
- Source: BestBlogs / LessWrong
- Publish time: 2026-06-06 16:56:05
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 29623

---

Originally intended as a quick take, but got a bit longer, so why not turn it into a post. Just sharing my observations & assumptions here about the state of software automation. Happy to hear thoughts on where you think I'm off. I'm sure none of the thoughts in this post are totally original, many have been proposed in similar form elsewhere, and I'm[1] far from the first person to speak of the bottlenecks that AI progress and adoption are facing. It still seemed useful to compile my current views on the situation and summarize them to those with only an outside view on the impact of AI on the software industry.

    
     

    

    
     
     
      

     
     
      by nanobanana 2

     
    
    
     

    

    The software world is trying hard to automate itself. Undoubtedly, coding agents have made a step change since last November and now enable more and more use cases that were unthinkable a year ago. And yet it seems to me that there's still a big disconnect between how many people think coding agents should be affecting the software industry and what's really going on so far in most places.

    Please feel encouraged share your views and disagreements about any of these in the comments.

    First, I do think the following things are all true:

    
     coding agents have become much more capable recently and have unlocked many, many new use cases

     coding agents are better than almost all humans at a huge amount of coding-related activities and allow practically any individual to do work far beyond the scope of what they were able to do 1-2 years ago

     coding agents will become better and better and almost every "intuitive" attempt to predict what they'll be like in a few years will likely underestimate them in all kinds of ways

     the space of things individuals can create has expanded immensely; non-technical people are now able to build pretty useful and sometimes impressive things[2]

    

    But it's easy to extrapolate this too far, assuming that much of software engineering can now be automated and that the same number of engineers can now get done 10x as much as before. My impression is that this is partially true for very small teams, but gets less and less true the larger an organization is and the more dependencies and constraints they have. In particular, I think that it takes a lot of very deliberate effort to find the right ways to use current AI to actually become considerably faster at actually-useful work, and most naive / locally-optimizing approaches at doing so may not work out and even be detrimental.

    Problems and Bottlenecks

    
     The biggest issue I see is context. Meaning both the limited size of context windows, and how context windows are filled.
      
       Humans have vast amounts of context, only a little part of which is actively utilized for any given task (but you can't easily tell ahead of time which part will be relevant). But it's all there in the background and can be used on demand. Often, we don't know ahead of time what context will be needed, but it's all ready to be used without the human having to search for it. It just automatically appears in our brains when we need it (for the most part). Sometimes the human does not even consciously notice they're relying on some piece of context, it's just kind of passively there, informing their actions and decisions[3].

       LLM context is written in words. Human context is closer to embedding vectors[4]. Words are not a great representation. Words can be misunderstood. Words don't come with integrated dimensions of importance, recency, risk, interrelations, and so on. All of these can, to some degree, be phrased in words, but the word count explodes the more nuance you want to represent in your context.

       One might naively assume that an experienced human worker can just write down everything they know, and so the LLM will have the same knowledge. But I don't think that's feasible. Because the human would have to write many millions of words, still wouldn't capture everything they know (much of their knowledge may be "unknown knowns" that they never explicitly thought about, but that would still come up once they need it for some particular task), and would not be expressed in a way that the LLM would understand/interpret in the same way.

       Another assumption could be that coding agents (now or eventually) will be able to just understand code so well that they don't need much human input at all. But a lot of information is just not represented in code. That may include certain reasons why something was implemented in a particular way, or product decisions that happened during an in-person meeting, or all kinds of random constraints of the software that human workers may just organically learn over time and remember, but that are not stored in some central place. Maybe more advanced AI will have sufficient 'truesight' to guess many of these things from the code alone. Especially if it doesn't just take the current state of the code into account (as today's coding agents typically do) but the entire git history of how the code was produced, including ticket descriptions, etc. But I think we're still pretty far away from that.

       People typically include the functional requirements in their prompts when they want a coding agent to do something, i.e. they explain the desired final behavior/output. It's much harder and/or less obvious (and hence often omitted) to explain the non-functional requirements (such as performance, load, accessibility, UX, certain security constraints...). First, these may always kind of exist "in the background", and employees pick them up over time but they are often not written down anywhere. Second, while functional requirements are often binary in some sense (so you can explain them easily, verify that they work, and write tests that ensure they keep working), non-functional requirements can be much more fuzzy. You often have to make trade-offs. Does it make sense to go with a simpler implementation that causes slightly longer loading times? Such questions were until now often subject to the judgment of developers, and now get more and more dropped under the bus, as the coding agent doesn't have enough context or persistence on its own to know all these side constraints, let alone be able to make good decisions about such trade-offs. And while the agent could ask the developer for clarification, this would increase communication overhead and slow things down overall (whereas an informed developer would often make such decisions on the fly).

       Humans also often have a decent grasp of which changes are going to happen in the future, that may be way out of scope for the current task. But they can still inform how to implement something. Coding agents typically don't have such background information, and hence cannot take this information into account, leading to lower-quality implementations.

      

     Coding agents tend to often rely on assumptions they cannot know for sure, and this property cannot be straightforwardly fixed
      
       Developers often complain about coding agents just assuming things and going with these assumptions, which ultimately turn out to be wrong. They often claim to have found some solution or fixed something, and later have to admit their conclusions were misguided. A lot of time can be wasted on such cases.

       One might assume this is just a flaw of coding agents that labs will eventually fix. But my view is that this is a fundamental trade-off with no perfect solution: coding agents have to make many assumptions, as otherwise they would be unwieldy and annoying. If they constantly asked for clarification on everything and always made really sure they understood things thoroughly, they wouldn't get anything done[5]. Them jumping to (usually-but-not-always right) conclusions is a feature, not a bug, and most of the time this makes them highly useful. But it also causes these issues in other cases where their propensity to "make assumptions and solve things based on these assumptions" has undesired consequences.

      

     Relying a lot on low-context coding agents accumulates tech debt and causes engineers to lose their theory of the code
      
       Due to the context + "working on assumptions" points above, coding agents have to solve many problems through guesswork and an incomplete picture of the software they work with. This is often good enough for them to find a solution. But often this just means applying isolated patches rather than finding clean, wholesome solutions, which degrades the flexibility, robustness and maintainability of the code while overfitting on the very specific thing they happen to be working on at any given time.

       I think it's pretty clear that many different people working on the same code base usually cause the code quality to be lower than if one (skilled) engineer, or a small team, maintains the same code fully. The more people work on the code, the less will the average contributor know about it, and the more you end up with duplication, greedy patchwork, incorrect usage of interfaces, and parts of the system working together in sub-optimal ways. Current coding agents make this problem worse, because every developer now sends many different instances of coding agents to work on the code base, where these different instances all separately contribute to this problem.

      

     Incentives & laziness
      
       Giving developers tools that let them do their work faster certainly seems that it would lead to more work getting done. But another thing that may happen is that they aim for a similar level of output, which now requires less effort.

       This would naturally not affect individuals who work on passion projects, so they understandably get very excited about the technology. But if you work to pay the bills and you're not super excited to do work, but rather work in a way that allows you to not feel guilty about your lack of visible output (which I imagine is the case for a non-negligible share of software people out there), then your output may remain about the same, while you just have to expand less effort than before.

       Alternatively, people who do optimize for more output, may end up paying less attention to their code quality, contributing more to the accumulating technical debt.

      

     Cognitive decline
      
       In the past, solving hard technical problems required thinking hard, understanding problems fully, and you typically only came up with working code once you had a good grasp of what you were doing. This is no longer the case. The easiest and often fastest (at least in the short term) way to solve any difficult problem is to ask a coding agent to solve it. You then look at the solution, read its explanation, think "yeah makes sense" and push a commit. It now takes a lot of agency to understand things, because you don't have to anymore. People can solve hard problems without understanding them, and many do. Some have reported a feeling of brain fog when they suddenly have to work on a problem without the aid of a coding agent. I've experienced this as well. I find it very concerning.

       One might argue that the time of humans having to understand complex problems is just over, at least in software engineering. Understanding code just isn't relevant anymore. Coding agents will improve fast enough that the skill of orchestrating coding agents becomes much more important than being able to understand code as a human. Perhaps this is true. But it's still a risk. The software world is currently betting the minds of millions of engineers on the continued progress of coding agents. And if this goes badly, e.g. because AI ends up taking much longer to progress than currently anticipated, the software world could end up in a pretty sticky situation, where its staff (the part that wasn't laid off due to expected AI acceleration) not only doesn't understand the code base anymore, but also has lost the skill[6] to understand and solve problems on their own.

      

     Coordination bottlenecks
      
       Imagine two people carrying a heavy object down a flight of stairs. Often, they do this very slowly and deliberately. Not because they wouldn't individually be able to move faster even while carrying the weight, but because on top of that, they need to ensure they stay in sync. I have the impression that coordinated software development is somewhat similar. There are many processes involved - not just coding, but also code review, testing, product decisions, legal requirements, marketing, general strategy considerations, dealing with regressions, and much more. Big parts of coding and testing can now be accelerated, but some other parts of this complicated web of creation cannot. You can't just accelerate isolated aspects of this system by 10x and assume this benignly translates to an overall acceleration. These systems grew over decades into a shape that kind of works, adjusting to the past reality of software creation. Now, a few parts of these system get greatly accelerated, while the rest has to catch up. This can work to some degree when your organization evolves accordingly and you have good feedback mechanisms & incentives. But the default (in my experience) is that this just leads to a lot more lower-quality code (dare I say slop) getting shipped, with much less good oversight & judgment being involved.

       Increased output tends to cause certain amounts of work for others. Every feature shipped has a risk of creating new bugs that eventually get reported and have to get fixed. Code needs to get reviewed. Support & marketing staff needs to stay on top of the state of the software. Product managers need to know what's there and how it works to prioritize next steps. Different features need to remain compatible to each other, and the more you have, the harder it gets. Often you need backward compatibility. Providing different configuration options for users leads to combinatorial explosions of possible states. Users need to find and use the new features and will, in one way or another, cause feedback to make its way to the company that then has to react to it. The more code is added, the less other engineers understand the code base or the more work they have to do to stay on top of things. Shipping things more quickly comes with all these hidden costs, and the speed advantage is not necessarily worth it.

       The increase in coordination overhead also affects software developers directly. Most of the deep work we used to do is now getting done by machines. Tech leaders love to frame this as a chance to focus on even more meaningful tasks, like providing our human judgment for making important decisions. But the reality so far rather seems to be that this leads to a huge amount of context switching. And to working on 5 tasks in parallel, trying to keep your coding agents on track who often run into walls or get to wrong conclusions or come up with sub-optimal solutions due to lack of sufficient context and/or judgment. And then it's up to you whether you lower your standards and ship bad and unmaintainable code, or put a lot of effort into providing these agents with the concrete context & judgment they need in order to do better work. Fixing a bug nowadays involves less direct interaction with the intricacies and dynamics of code, but instead involves reading pages and pages of highly verbose LLM analysis and trying to extract the actually relevant bits out of it and eventually steering the LLM in the right direction.

      

     Diminishing returns
      
       Many people in tech seem to think that speed is essential. Sometimes it surely is. But I also think this can be overestimated a lot. For instance, it's not at all clear that a tech company with $20M ARR[7], speeding up their development efforts by 5x, would be able to translate this to anything close to 5x the ARR. I'd argue it's not even clear if this would lead to any rise of ARR at all. People within a company may see many cases where a particular feature is requested, and having that feature would in some sense help convince some customer to buy the software or service. And looking at these, it becomes appealing to think "if only we were faster, we could win over so many more customers!" But I don't think this holds true in many cases[8].

       Increased speed may lower the quality of strategic insight and decisions. If you have to make way more decisions per time span, while your software evolves at a much faster pace than before, and you get about the same amount of feedback from the outside world, then your strategic decisions will almost necessarily be much less informed and thought-through. This alone, arguably, could more than offset any potential ARR increases from the acceleration itself[9].

      

    

    
     

    

    I don't know how AI will develop, if progress will continue at about its current pace, and how such progress will affect tech orgs. But I do think many of them are playing with fire and are betting a lot on the assumption that coding agents will become much more capable quickly, at a rate where they somehow manage to outpace the problems that are currently being caused. If progress gets delayed significantly - perhaps due to hardware bottlenecks, headwinds against data-center construction in the US, a Taiwan crisis, a cascade of investors losing trust in AI and pulling out their investments - then my current take is that many existing tech orgs will face considerable challenges caused by their current strategies of hasty automation.

    The Bull Case

    It seems to me that what many people in software are betting on is that coding agents keep getting better at recent rates (or even accelerate), and this will allow them to eventually surpass pretty much all the problems mentioned above. If their capabilities grow faster than the problems accumulate, then it's a good thing to ride this wave as early as possible.

    The problems I listed are not insurmountable, just difficult. For instance, the context issues could to some degree get solved. Coding agents may get much larger context windows, or continual learning gets solved or greatly improved. While the code itself does not contain all the relevant context, agents may eventually process not only entire code bases, but also the full history of company-internal communication tools, knowledge bases, and chat & thought process history of prior coding agents, and have all of these either in their context[10] or even their weights, allowing them to know pretty much all functional + non-functional requirements, reasons why certain decisions were made, and so on.

    Similarly, while technical debt may accumulate, one can also argue that the viability of refactoring and rewriting code from scratch is increasing rapidly. At some point, technical debt may just be a non-issue because a fleet of coding agents can rewrite almost any piece of software overnight, if necessary.

    Another argument I find compelling is that, perhaps, some startups will just figure out how to integrate coding agents properly without running into many of these issues, which for established larger orgs is much harder to do. I believe this could either happen by finding very suitable organizational structures and processes, or by finding particular use cases that are well-suited for AI automation. And these better-prepared and hence much more rapidly executing startups may, over the next years, just outcompete many of the established organizations that are failing to properly adapt. If, from the start, you establish rules and norms around standardized documentation, test coverage, centralized LLM-friendly communication channels, and focus your acceleration attempts to those areas where they have a good chance of working without causing too much trouble elsewhere, then maybe you really can achieve much higher velocity than other companies of similar size throughout the growth phase in a way that leads to a higher market share.

    Even then I'd think that in most domains, quality of strategic judgment is likely more important than speed. A company being 10x as fast at developing new stuff compared to another one may still lose if they just hastily follow the weak signals they pick up from the market.

    What Now?

    All of the above is not to say that the world will not look very strange in five or ten years. I just see a lot of reasons why software automation in particular may not be as straightforward to accomplish as it may look on the surface. None of the challenges I mentioned are insurmountable, but they exist, and solving them will likely take some time.

    Even when we reach a point where some fully automated AI-only companies exist that do not involve any human employees as potential bottlenecks, I would expect these to not have that much of an immediate advantage. At least as long as they still cater to humans. Because, as humans are (initially) both the likely end users and those that hold most of the capital, the signals such companies get from the market will still mostly reach them at human time scales. Being able to develop software 1000x as quickly may not be all that useful when the market feedback still comes in at 1x speed.

    To be clear, I'm not meaning to imply much about the alignment problem or existential risk here. Clearly, once we have fully AI-driven companies without human involvement, and they actually manage to be competitive, then we're deep in singularity territory, and I'd be very happy about internationally coordinated efforts to delay or prevent us from reaching that state of affairs anytime soon. For the most part, I'm arguing that AI automation really seems way trickier than I would have expected a few years ago. I was confused for some time why coding agents seem so incredible during personal use and yet don't seem to have that much of an impact on the productivity of most larger organizations yet[11]. This post is my attempt to make sense of this.

    
     ^
      
       For context, I've been working as a programmer for close to 15 years and have been working a lot with Github Copilot agents and (since the Opus 4.5 release) with Claude Code, both privately and professionally.

      

     ^
      
       This is another reason I found it worthwhile to write such a post - people who have no close ties to the tech world may primarily know coding agents from messy public debates as well as their own experiences, which on an individual level are often overwhelmingly positive. As individuals, we get empowered to solve all kinds of problems we couldn't solve before, and this makes coding agents seem almost magical. But I argue that these magical properties don't transfer that well to the software industry, at least currently.

      

     ^
      
       What I mean by this is that there are many very intangible things, like what kind of experience you strive for with your software, how "dangerous" certain modules are (maybe some particular part of the code requires adjustments, but the three times somebody tried that in the past, it always spectacularly failed, so you learned to not touch that part of the code and just live with its limitations), or knowing that a particular change that would be useful will lead to some conflict with another team that has strong views on doing things differently; things like that, which you don't necessarily think about deliberately, but they still steer your behavior in meaningful ways.

      

     ^
      
       Well, not all of it. There are certainly different types of context humans work with. Some context is in form of written documents (that live outside the code) - these could be processed equally well, or better even, by coding agents, given they have access to them and know they exist and when to query them. However, humans also have a constantly growing theory of the code, of the product, and of the organization as a whole, and know which things they need when. They know how many users their software has (if any), how consequential bugs of different types are and how much effort is warranted to prevent them, how severe an outage would be, broadly what future plans may exist, how much time pressure there is, and so on, and so on. All these things are like very particular glasses through which the human sees their work. The coding agent (of today) has almost none of that. Once coding agents get continual learning, they may be able to persist such things on their own, without having to rely on lossy text representations - but even then, they'll first have to build that context, which would require help from the humans who, until then, are the only ones who have all that context. So even once we have such capable coding agents, they could still take months to build a similar amount of context as a capable human software engineer.

      

     ^
      
       I often observe this when watching others prompt an LLM. In such situations, my impression is often "Wow, this prompt is so vague and just uses terms that are never explained, no way the LLM will be able to work with that", but in most cases, the LLM will just correctly infer what they are talking about and give a pretty solid answer. They just have learned to make usually correct assumptions when working with highly incomplete information. But this comes at the cost of sometimes making wrong assumptions without questioning them, and I don't think they have a way, even in principle, to distinguish right from wrong assumptions reliably.

      

     ^
      
       To state this more clearly, I don't necessarily think that the skill itself degrades that quickly. But once you're high on the drug of "just type the problem into a chat box and hope for it to magically get solved", it's very hard to go back to the old world of expending serious cognitive effort for 8 hours a day.

      

     ^
      
       annual recurring revenue, one way to quantify the revenue of a company which is particularly popular among tech orgs.

      

     ^
      
       Some reasons why I think the link between development velocity and revenue is weaker than one might think:

       
        If your leads end up not buying your service, mentioning some missing features in the process, it's not a given that these missing features were actually load-bearing for their decision. It could be they decided for a variety of fuzzy reasons, or reasons they are not comfortable admitting, and just point out one thing that is easy to explain.

        Similar to the difference of stated and revealed preferences, people may claim (and even believe) that some thing is important to them, but the claim will not be well aligned with actual real-world behavior.

        People may wish a certain problem was solved, but do not end up liking the particular way in which you solved it. Or they will realize that the solution actually does not help them as much as they thought to begin with.

        While some users may be impressed by some new features, others may get overwhelmed if there are too many functionalities and too much change is happening all the time, and would prefer a simpler, cleaner solution without countless bells and whistles.

        Focusing on shipping much more quickly may lower overall quality of the things you do ship, lowering the users' trust in your solution.

       

      

     ^
      
       Naturally, when I make a claim like "an acceleration may counterintuitively lead to a decrease in a company's performance", I should ensure to check whether this would imply that artificially slowing down a company would be good for it. This would seem like a pretty wild claim. And I doubt it is typically true. But if slowing down is bad, then shouldn't speeding up be good, after all? Or why would pre-coding-agent tech orgs be at some optimum where neither a speed-up nor a slow-down would improve things? Well, firstly, they might be close to such an optimum, for the "they evolved over decades into the shape they have today" reason. Accelerating parts of the system without the rest of the system being able to catch up may indeed have an overall negative effect. Secondly, it could be that some (well-dosed) acceleration would be good, but "everyone use coding agents and get 10x as fast" + "even non-tech people should start shipping things to prod" does not seem, to me, like the kind of acceleration with such positive properties.

      

     ^
      
       Seems unlikely in the current paradigm, as this could easily reach tens of billions of tokens or so.

      

     ^
      
       Some exceptions exist, like Anthropic itself, which does seem to possibly have reached much higher development velocity in some areas, although I'd still say it's unclear a) how sustainable this practice will turn out to be or them, b) how big a part this plays in their extreme revenue growth, and c) to what degree their development model could be applied to other tech companies or is pretty specific to their use case (e.g. my understanding is that the rapid development cycles mostly apply to Claude Code, which is a very new piece of software which they likely already started as something to eventually be developed mostly by AI - an advantage that most established companies with their legacy code don't share).
