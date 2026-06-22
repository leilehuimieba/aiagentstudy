# The Pulse: a trend of trying to cut back on AI spend within eng departments?

- BestBlogs URL: https://www.bestblogs.dev/article/3d0b654a
- Original publisher URL: https://blog.pragmaticengineer.com/the-pulse-a-trend-of-trying-to-cut-back-on-ai-spend-within-eng-departments/
- Source: BestBlogs / The Pragmatic Engineer
- Publish time: 2026-06-12 00:32:50
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 6483

---

Hi, this is Gergely with a bonus, free issue of the Pragmatic Engineer Newsletter. In every issue, I cover Big Tech and startups through the lens of senior engineers and engineering leaders. Today, we cover one out of four topics from The Pulse issue from two weeks ago. Full subscribers received the article below fourteen days ago. If you’ve been forwarded this email, you can subscribe here.

  The below The Pulse is interesting, as a week after the original was sent it out, OpenAI CEO Sam Altman also said how AI budgeting is a huge issue for some companies – echoing findings from this analysis.

  
  In mid-May, Uber president, Andrew McDonald, was on the Rapid Response podcast for a conversation about the ridesharing giant with host Bob Safian, who raised the lack of hoped-for efficiency leverage from AI, citing the language learning app, Duolingo.

  
   “When you hear companies talking about 25% of code commits over the last quarter were AI-driven, or how their token usage went from X to Y percentage of employees: all these numbers are amazing. I think it’s a massive transformation of society”, McDonald said.
   

   

   “But, then you go and you talk to your senior engineering leaders, and you’re asking: “how many projects that were “on the cutting room floor” got moved above the line [of being done] because of the productivity gains? Because 25% of our code commits were via Claude Code last quarter.”
   

   

   That link [of improved productivity thanks to AI] is not there yet. I mean, maybe implicitly there’s more that is getting shipped, but it’s very hard to draw a line between one of those stats and more useful consumer features.
   

   

   Over the coming quarters and years, maybe that will become clearer. But today it’s hard, even if some of the underlying metrics are trending in a really astronomical direction.
   

   

   Our CTO, Praveen, went viral because he said in an interview that we had blown through our AI budget for 2026 and it was the middle of March. We’re going to have to start talking about token consumption and the associated cost versus headcount, and making tradesoffs on that as an engineering organization.
   

   

   If you’re not able to draw a direct line to [how many] useful features and functionality you’re shipping to your users, that tradeoff [on AI spend] becomes harder to justify because AI is not free.
   

   

   If you’re just a user [of AI tools] sitting there and coming up with interesting use cases, and you don’t pay the bill, it can feel [like AI is free]. But somebody’s paying the bill”.
  

  My hunch is that pretty much every company is starting to, or will do soon, ask questions about the massive growth in AI spend; starting with AI coding tools. I talked with a few folks at larger and smaller companies about it:

  
   OpenCode: customer demand for optimizing spend is spiking. Yesterday, on the podcast episode with OpenCode creator, Dax Raad, he said demand for OpenCode’s hosted inference service (OpenCode Zen) surpassed all expectations because larger companies want cheaper, but still capable, AI models. He revealed that over the past month, every single inbound enterprise request was about optimizing spend. So, there’s some widespread concern about AI bills.

   Companies with cutting-edge AI bite the bullet with model routing. I talked with a CTO and a Head of Engineering at two cutting-edge tech companies. They also do not have an obvious return on investment (ROI) as yet. Still, they feel they have no choice but to pay the “intelligence premium” for state-of-the-art models or increase the number of bugs shipped. To reduce costs, both are considering “smart” model routing based on use case and prompt. These places pay top-of-market for the best engineers, so similarly, there are expectations of access to the best tools and models.

   DoorDash: More knowledge-sharing sessions and responsibility for devs. The leading food delivery company gives responsibility for spending to devs: everyone has a high monthly token usage limit. To exceed it, you need to justify why, and also share the plan for being more efficient next month. Many regular in-house knowledge-sharing sessions are about efficient AI use.

   Traditional company: monthly limits and dumb-model downgrades. One month ago, one of the largest retirement-savings companies in the US updated its AI usage policy for all devs, a current engineer told me, imposing a monthly GitHub Copilot token limit. Once gone, devs must use the less capable “0x” models on Copilot, which are not charged extra: GPT‑5 mini, GPT‑4.1, and Grok Code Fast 1.

   Startups: signing up for multiple Claude / Codex Max subscriptions. I talked with several smaller startups that are generating meaningful revenue, and don’t want to pay expensive API prices. So, they’ve made it a practice for devs to get subsidized Claude Code Max or Codex Max subscriptions.

  

  There’s a new bottom-up focus on AI efficiency. Most tech companies do a variety of internal knowledge-sharing things like regular team demos, lunch-and-learn sessions, and engineering all-hands. I’ve been noticing more AI efficiency-focused sessions in the past couple of months, coming from engineers: no top-down mandate!

  Engineering all-hands, CTOs, and even CEOs have started to raise concerns about increasing AI token costs, and now more engineers are experimenting with cheaper models for simpler tasks, model routing, more efficient token usage, etc.

  I’d expect that during the next performance review and promotion cycles, engineers who helped save on token costs might be rewarded, like two years ago, when engineering teams were rewarded for saving on third-party vendor bills.

  For an engineer, the best way to show impact in your work is to translate it to money: revenue generated, or costs saved. With AI spending as high as (or higher than) on observability, it should be straightforward to show massive savings with smart optimizations. There’s a touch of irony in how any savings – for which there might be promotions and pay rises – will come from the places that actually did the rocketing spending.

  
  Read the full issue in the previous The Pulse. Or check out this week's The Pulse: Did Anthropic’s new model just boost rival Codex’s market share?

  Subscribe to my weekly newsletter to get articles like this in your inbox. It's a pretty good read - and the #1 software engineering newsletter on Substack.
