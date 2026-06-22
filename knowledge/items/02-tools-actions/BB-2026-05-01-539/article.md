# The Pulse: Antigravity 2.0 takes ‘IDE’ out of its new IDE

- BestBlogs URL: https://www.bestblogs.dev/article/bca3a4c2
- Original publisher URL: https://blog.pragmaticengineer.com/the-pulse-antigravity-2-0-takes-ide-out-of-its-new-ide/
- Source: BestBlogs / The Pragmatic Engineer
- Publish time: 2026-06-12 00:22:16
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 7891

---

Hi, this is Gergely with a bonus, free issue of the Pragmatic Engineer Newsletter. In every issue, I cover Big Tech and startups through the lens of senior engineers and engineering leaders. Today, we cover one out of four topics from The Pulse issue from 21 May 2026. Full subscribers received the article below three weeks days ago. If you’ve been forwarded this email, you can subscribe here.

  Yesterday, Google launched a full redesign of its flagship AI IDE, Antigravity 2.0. The “original” Antigravity came out in November 2025, as pretty much a clone of Windsurf, the IDE whose team Google acquired for $2.4B last July.

  Google has turned Antigravity into two distinct applications, “Antigravity IDE” (its former incarnation) and “Antigravity 2.0”. This new version itself resembles a clone of Codex’s desktop app. When you install Antigravity 2.0, there are two different applications. From Google’s launch post:

  “If you already have installed the Antigravity IDE, when that application next updates, it will automatically update to Antigravity 2.0. At this point, you will be asked if you would like to still keep the Antigravity IDE, which is recommended for developers:

  

  
   
  
  My sense is that the team at Google may have struggled to decide whether to keep supporting “original” Antigravity while investing in the Codex-like experience, and so kept both. Whatever the reasoning, it has created confusing naming, and it feels to me like the team’s true focus is 2.0.

  
   
   
    Big change: Antigravity 2.0 throws out the IDE and adds a conversational interface
   
  
  The upgrade feels rushed, sloppy, and poorly thought out. I had Antigravity on my machine, and installed Antigravity 2.0 separately. I wanted to use them side-by-side, but when I tapped “Restart to update” on Antigravity 1.0, it upgraded itself to Antigravity 2.0 (the non-IDE version). Suddenly, I had two applications with different names, but neither is an IDE:

  
   
   
    Testing times: Two apps but no IDE version on my machine, due to lack of testing
   
  
  Google has introduced an “Agent Manager” concept that feels unintuitive, and perhaps suitably, its creator struggles to explain it (emphasis mine:)

  
   “When we launched the Google Antigravity IDE in November 2025, there was no agent-first GUI surface in the market. We wanted to prove that such a surface worked, at least for software development. So, while the core of the Antigravity IDE was a familiar agent-powered IDE, we introduced the Agent Manager, a second surface that stripped away much of the “IDE” UI. This allowed users to focus on the agent conversations themselves, the artifacts the agents produced, and multi-agent management.
   

   

   Even without this separation, we have been pleasantly surprised how many people have adopted the Agent Manager in the Antigravity IDE for such non-development tasks, but it is not particularly intuitive”.
  

  The “Agent Manager” is basically a way to launch several agents, and the most intuitive interfaces for doing so are inside Claude and Codex desktop apps and Claude CoWork. Antigravity 2.0 copies them by starting new agent tasks on the right hand of the UI, and keeping track of them.

  Google looks indecisive about what to do with the IDE part of Antigravity. The release announcement suggests they’ll keep on confusing users (emphasis mine:)

  
   “Although Antigravity 2.0 is the future, we won’t disrupt your workflows right away. For now, both the Antigravity IDE application itself and the Agent Manager in the Antigravity IDE will remain available. In an upcoming release, we will remove the Agent Manager from the Antigravity IDE, turning the IDE into a purely agent-powered IDE.”
  

  Basically, the Antigravity IDE (not “the future” in Google’s vision) will become more limited over time. It’s unclear what a “purely” agent-powered IDE will be once agentic functionality is removed, especially as Antigravity IDE is not the future, as per Google.

  Not only that, but the announcement also encourages devs to use Antigravity 2.0 with other IDEs! From the launch post (emphasis mine):

  
   “We recommend dual-wielding Antigravity 2.0 with your IDE of choice, whether it is the Antigravity IDE or otherwise. Googlers have already been dual wielding Antigravity 2.0 with a whole host of IDEs! We will have compatible extensions and plugins into other popular IDEs shortly”.
  

  To me, this suggests Google will retire Antigravity IDE and recommend VS Code, JetBrains, Cursor, or Zed, with Antigravity. Then again, why would Cursor or Zed support Antigravity? The messaging is extremely confusing: Google’s still the king of opacity.

  Feedback on Antigravity 2.0 has been negative due to bugs, poor UX and model support, more bugs, and eating up Gemini token quotas rapidly. Antigravity does not support state-of-the-art Anthropic or OpenAI models (no Opus 4.7 or GPT 5.5). Not supporting OpenAI’s models like this is sensible as they’re competitors, but Google is an investor in Anthropic, so not supporting Opus 4.7 (while supporting the legacy 4.6 model) is a bit odd.

  
   
   
    Models which Antigravity 2.0 supports
   
  
  Gemini 3.5 Flash is Google’s cutting-edge model, but it gets lots of complaints from devs for editing files without asking, and seems like an inefficient model. Another common complaint is that Antigravity uses up the $100/month Ultra subscription daily quota in minutes. Basically, it seems like a poor-quality product that wasn’t polished due to lack of time or inclination.

  In context, it’s embarrassing for there to be a “Codex” folder in the launch video if it suggests that Google’s own Antigravity devs are using Codex for day-to-day work. It also suggests that the launch video was not reviewed properly, otherwise this obvious detail would presumably have been caught and fixed:

  
   
   
    Codex folder in Documents suggests Antigravity devs are users of it. Source: Antigravity 2.0 launch video
   
  
  To upset devs even more, Google is replacing its open source Gemini CLI with the closed source Antigravity CLI. There are a few issues with this move:

  
   Antigravity CLI does not support Google’s own Agent Client Protocol (ACP), used for programmatic control, primarily for IDE and other developer tool integrations. This is protocol which IDEs like JetBrains and Zed have adopted, so Antigravity CLI becomes incompatible with them

   Google offers no migration path from Gemini CLI settings/skills/MCPs into Antigravity. Figure it out on your own!

   Devs using Gemini models are forced to move as Google has removed support for Gemini 3.5 Flash model from Gemini CLI. It can only be used from Antigravity CLI. Clearly, this was done to force a move. Why not offer a migration path?

  

  My sense is the Antigravity team is moving fast, breaking things, and shipping a broken product. It feels like the Antigravity 2.0 and Antigravity CLI products have been rushed to meet the annual Google conference (Google I/O) deadline, this week. Google deprecates existing products to attempt to get users to switch to the new version. But the new one is broken.

  
   
   
    What’s changed? Manu Cornet penned this cartoon in 2011
   
  
  And this is a big reason why I don’t believe Google will become a serious player in the dev tools space – not even with AI dev tools. Every six to twelve months they remind devs who onboarded to their dev tools that it was a mistake to do so. I would expect the majority of Google CLI and Antigravity users to go and try products from other vendors – be that Cursor, Anthropic, OpenAI, GitHub, or others – and for few to stick around after their workflows are broken.

  Subscribe to my weekly newsletter to get articles like this in your inbox. It's a pretty good read - and the #1 software engineering newsletter on Substack.
