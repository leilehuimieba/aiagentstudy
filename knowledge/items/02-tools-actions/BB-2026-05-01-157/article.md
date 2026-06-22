# Claude Code for Product Managers

- BestBlogs URL: https://www.bestblogs.dev/en/article/e80b2d9f
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 10687
- Original publisher URL: https://every.to/source-code/claude-code-for-product-managers

---

This piece is an accompaniment to Spiral general manager Marcus Moretti’s guide for product management using Claude. Read the full guide and the essay below to learn how he built a workflow that helps him run a full product as a solo practitioner. When you’re ready to get started yourself, download the plugin.—Kate Lee

Read the AI-native product management guide

As the general manager of Spiral, Every’s AI writing partner, I’m a “two-slice team.” I’m responsible for all aspects of a product: the code, customer support, marketing, and product management. I could not do this job without Claude.

Claude Code has eliminated the drudgery of product management. The busywork that used to happen across 10 different apps now happens in a single chat thread. I’ve come to view the work of product management through the lens of this conversation—the conversation is the work.

These days, I experience what’s left of product management work in flow state—thinking through gnarly design problems, looking at interesting data, and talking to customers. Cat Wu, Claude Code’s head of product, recently said, “As code becomes much cheaper to write, the thing that becomes more valuable is deciding what to write.”

I wrote up the main skills that run my product management workflow in a guide. Below, I trace how I arrived at those skills and reflect on post-AI product management and software.

Write the roadmap and nothing else

In my new role, the only product document I’ve written is the roadmap. Everything else—every PRD and every ticket—has been written by Claude.

Writing is thinking, so as a new general manager, I wanted to take my time drafting Spiral’s roadmap. I spent several days understanding the product, usage trends, user feedback, and the market. I wrote about the problem Spiral can solve, how Spiral can solve it, and the features we’d need to build to deliver on it. I spent hours talking to several people at the company who’d worked on previous versions of Spiral and were current or former users of it themselves. (In the guide, I talk about the new /ce:strategy skill in compound engineering that interviews you to produce this document for your own product.)

After six drafts of the roadmap, I created a GitHub project and added it as the project’s README. I’m already using GitHub to host all my code, so I figured I might as well use it for tickets as well, or as GitHub calls them, “issues.”

From there, I asked Claude to use the GitHub command line interface (CLI) to read the README and give feedback. We went back and forth on a few tweaks, and then I asked it to review the codebase and do a first pass of the tickets required to deliver the roadmap. Within a few minutes, Claude produced about 100 detailed tickets, each with strategic context, supporting data, acceptance criteria, and technical implementation notes.

To be fair, the roadmap I wrote was pretty detailed; Claude wasn’t hallucinating features. And it had access to a library of user feedback and recent usage reports (more on that below). But it was shocking to see something that had previously taken me days or weeks get done by Claude in minutes. It felt like the PM equivalent of vibe coding.

I’d previously prided myself on the absence of ambiguity in the tickets I produced for engineers, but this was next-level. Claude also prioritized the work in an unbiased way. Sometimes, a product manager gets emotionally attached to a certain feature idea for whatever reason. Claude, however, was ruthless in elevating the things that had the best shot at delivering the vision and hitting our 2026 goals.

That doesn’t mean the tickets were all ready to be implemented. When I do pick up a ticket, I do a full review of the requirements before asking Claude to implement it. This is a step where I still add some value. Claude’s first pass gets the feature right in broad strokes, but it struggles with some aspects of data modeling, microinteractions, and edge cases. I often adjust specs to reflect the nuances of real usage patterns, while Claude seems to envision a perfectly rational user reminiscent of pre-Kahnemanian economics.

I don’t do sprints. I have five columns in the GitHub project: later, next, now, in progress, and done. Around once a day, I run a custom command, /prioritize, and Claude does a sweep—checking for stale tickets, confirming that “now” is this week’s work, pulling anything urgent out of the backlog.

If I discover a bug or a user asks for a compelling feature, I tell Claude to create a ticket. It gets a “triage” label and is sorted in the next /prioritize run. If it’s a priority-zero issue, I go straight to fixing it without creating an issue.

Over time, the GitHub project becomes the product’s working memory: a fluid, continuously prioritized picture of where things stand. I’ve claimed to work in an Agile fashion before, but in hindsight, I don’t think Agile was really possible until these new AI tools came out.

Read the AI-native product management guide
Building blocks that help your agents compose elegant backends

Agents right now often write code that needs to be cleaned up because they need three things most infrastructure wasn’t built to provide: immediate feedback, local reasoning, and a thin meta layer. Convex provides immediate feedback, enables local reasoning, and minimizes the meta layer, giving agents a surface layer that’s actually small enough to work with. Scale without breaking or spending a fortune.

Try Convex at convex.link/every
Want to sponsor Every? Click here.
The pulse command

The old way of understanding how customers were using your product was to look at dashboards and run queries. You’d open Amplitude or Mixpanel and get an overview: how many users, how often, how long, what features, what revenue. Setting these up took time; sometimes they required engineering work, competing with product updates for developer bandwidth.

These days, I don’t look at dashboards. I run a custom command, /pulse that delivers something closer to an analyst’s briefing than a chart. The pulse command surfaces a range of metrics, including active users, chats/messages/drafts created, response times of key aspects of the system, conversations graded one to five, and an anonymized sampling of use cases. And because Claude is a language model, it doesn’t just pull numbers: It reads the text, grades every conversation, flags anomalies with a green or red dot, and explains what it found in plain English.

The command is just a Markdown file, so the format itself is easy to change. I’ve adjusted it about 50 times since I built it. When a feature ships, I add a line, and the next morning it shows up in the report.

Every pulse report lives inside a Claude thread. When a recent report surfaced a bug driving down conversation scores, my next message in that same thread was to fix it. I did not have to create a ticket, but was able to solve it in the same conversation. Over time, Claude also learns the nuances of the system and saves that to memory.

Product research

For all the magic of AI, there is no substitute for talking to users. What people say about your product and how they try to use it is endlessly surprising. Just when I think I’ve shipped the world’s most intuitive feature, a confused user will ask a question from an angle that would never have occurred to me.

That said, there are elements of product research that Claude seriously elevates. Here’s one example: A big part of Spiral’s value proposition is reflecting the user’s writing style in the drafts it generates. There’s a rich academic literature on stylometry, the study of style.

I leaned on Claude to help me wade through the literature for findings relevant to Spiral’s “style transfer” approach. Using the Arxiv model context protocol (MCP), Claude was able to find a dozen recent papers about LLM stylometry. I read their abstracts, then read a handful in full. I cited those papers in the article I wrote for Every, and they’ve been directly informing the new style system I’m building in Spiral. It’s so cool to see academic citations sprinkled across product requirements. For product work where you have a real opportunity to differentiate, it’s worth going the extra mile on research, which is now within reach.

What SaaS survives

AI should open up product management to more people—you don’t need formal PM training when the tool itself can teach you. If you don’t know what metrics to pick for your pulse equivalent, ask Claude for recommendations. If you’ve never analyzed an A/B test, ask Claude how. If you’re not sure whether a feature will move the needle, ask Claude to predict its impact. To paraphrase Nvidia CEO Jensen Huang, AI is the easiest product in history to use, because if you don’t know how to use AI, just ask the AI.

I’ve cancelled several B2B subscriptions since moving my product management work into Claude, which means I’m seeing the SaaSpocalypse play out in my own spending decisions. Yet I’m building a SaaS product. How do I make sure Spiral doesn’t get steamrolled by the frontier model providers?

I believe it’s possible for a SaaS product to survive if it has two main characteristics:

Unique sources of critical data: my database, my analytics, my payment system—services that would be very difficult to rip out.
Products with seamless agent integrations. Github, Stripe, Posthog, and Logfire have played nicely with Claude. One service I inherited from my predecessor didn’t have an MCP, and it was swiftly cancelled.

For Spiral, if we nail style transfer—an inherent limitation of heavily post-trained language models—Spiral becomes the unique source of your written voice in an agentic world. That’s valuable and sticky. Already, API chats outnumber web chats, a milestone that we reached three days after launching the agent that handles Spiral’s API requests. That means that users are not necessarily using Spiral in the Spiral app, but across their workflows.

Good product management is making something people want, to quote Y Combinator. Great products come from inspiration and ingenuity, things that tools and processes—no matter how good—won’t bring you. Perhaps the best thing about this new agent toolset is that it gets rid of the busywork that saps creative energy. There’s more space now for daydreaming and far-fetched ideas. Product management can now be fun.

Read the AI-native product management guide

Marcus Moretti is the general manager of Spiral (@tryspiral). To read more essays like this, subscribe to Every, and follow us on X at @every and on LinkedIn.

For sponsorship opportunities, reach out to [email protected].

Subscribe
