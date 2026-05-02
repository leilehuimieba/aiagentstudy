# OpenAI Greg Brockman：为什么人类注意力会成为新的瓶颈

- BestBlogs URL: https://www.bestblogs.dev/video/12c8ff4
- Extraction: DOM text from BestBlogs page
- Extracted chars: 35834
- Original publisher URL: https://www.youtube.com/watch?v=bBS93A0BeNI

---

VIDEO
93
⭐ 精选内容
OpenAI's Greg Brockman: Why Human Attention Is the New BottleneckOpenAI's

Greg Brockman 讨论了 OpenAI 的算力经济、scaling laws、AGI 进展、agentic coding、具备上下文的电脑使用、内部 AI 采用、安全计划，以及为什么执行自动化后人类注意力会成为限制资源。

Sequoia Capital
关注
·
昨天
·
13 个章节
·
查看原文 →
OpenAI Greg Brockman：为什么人类注意力会成为新的瓶颈
章节导览
13 个章节
CH.1
Introduction and Greg Brockman's Background
00:00
CH.2
The Economics of Compute
01:00
CH.3
Scaling Laws and Architectural Evolution
02:09
CH.4
Defining AGI and Current Capabilities
04:46
CH.5
The Agentic Shift and Context
07:15
CH.6
Internal AI Adoption at OpenAI
10:03
CH.7
Changing Organizational Structures
12:43
CH.8
Human Attention as the New Bottleneck
14:31
CH.9
Security in the Age of AI
18:07
CH.10
Speed, Responsibility, and Mission
20:05
CH.11
OpenAI's Product Focus
23:52
CH.12
The Future of Work and UI
26:15
CH.13
Frontiers of Science and Conclusion
27:58
📝 实时字幕
跟随播放
全部字幕
00:00
1

so Greg uh thank you for coming back here Um I don't think we ever charge you for rent So uh maybe we'll send you an invoice later but Greg you've been part of like two really spectacular companies Stripe as employee number four and then the first CTO

00:07
1

I just recently heard that they process 1.6 billion sorry 1.6% of the global GDP You must be proud of that That's amazing You must be even more proud of the fact that OpenAI has almost a billion or maybe more than a billion uh in weekly active users at this point

00:28
2

I mean it's all it's all very exciting It shows you what technology can do And uh you're not just co-founder and president but you're also chief builder at Opening I heard that that was one of your titles I'm not sure if there's ever an official title but I've been called many things Let's just say that

00:44
1

Well you have a audience of great builders here So we'll start from all the way at the bottom of the stack You Open AAI has multiple stacks to the business one of which is compute And you guys have been very aggressive very aggressive on securing compute Why is that

01:00
2

Well in many ways we have a very simple business We buy rent build compute and we resell it at a margin That's it As long as the margin's positive then you want to scale it because the demand for solving problems the demand for intelligence that's unlimited And the AIs that we have right now really are able to rise to the challenge of effectively any kind of problem that you want to throw at them

01:26
1

Do you have enough compute No Really Yeah definitely not I was just with Matt Garmin and he says the GPU compute availability in 2026 rounds to zero Don't you guys have all of it

01:37
2

I mean we have we we would love more We're we're constantly out there hunting for more honestly And I'll tell you like when we first launched when we launched CHBT I remember being on a call with my team and they were like all right how much compute should we buy And I said all of it And they're like no no no seriously like like come on how much should we buy I'm like no matter how fast we try to ramp compute I guarantee we're not going to be able to keep up with demand And that has been true ever since

02:09
1

Um that's that's fascinating Moving up from compute since I don't know if much of this audience can help you with securing more compute because most of them are founders of startups Um about architecture and scaling laws are what are the what are the where are we in the scaling laws Are they still doubling each year Are you changing architecture What's what is what are you guys pushing on the frontier on the research side

02:38
2

Well I would say first of all the scaling laws are a deep and very beautiful mystery right They feel deeply fundamental It's like this scientific truth that just like you think about physics and you know Newton's laws and things like that there's somehow this truth of the universe and they're empirical Like we don't necessarily have all the theory to explain exactly why it works

03:06
2

But to me the most beautiful thing is that neural networks were really designed like in the 1940s before they were computers And somehow we've been able to take the exact ideas that were developed back then and apply increasing amounts of computation and as you pour more compute into the models they get correspondingly more capable and it just keeps going There's no wall And that's I think that's a beautiful thing

03:28
1

That's pretty beautiful Are there more research or more algorithms that are in the works that because you know in the past we had neuronet networks to your point in 1940s but we couldn't we didn't have the compute for it Now that we have the compute for it you just are we just pushing the same things or are there new architectures and new ideas coming out

03:50
2

Yeah So I would I would think of it as we we absolutely have new ideas that are constantly powering what we do It's very simplified to say well let's take a neural network from the 1940s and you know put put it in a gigawatt data center right We have made tons of innovations and we constantly are improving things

04:16
2

And sometimes these are micro tweaks like you just realize that the way you've been formatting data was not quite right and that can actually be a very big deal Sometimes it's larger You think about the shift from the LSTM to the transformer and I don't think the transformer is you know like everyone's moved past the transformer as described in the other 2018 paper So there's constant innovation happening and I think of places that have been perhaps the most invested in long-term research on how to improve the architectures how to improve the fundamental algorithms and how to get the paradigm shifts I think OpenAI has been leading the pack there and that's something we continue to invest and I see lots of fruit on the horizon

04:46
1

Got it And on the models um does open a have a formal definition for AGI Are we close Are we not close Pat and Sonia published this thing that we are at AGI functionally Do you agree with that Do you not agree with that

05:05
2

Well we do have a formal definition but to some extent I one thing I have learned is that everyone has their own intuitions about what AGI is And maybe you can view it as like according to my view of where we are I think we're about 80% of the way there in that we have models that are smart They're very capable They are able to if you give

05:33
1

Are they smarter than you I mean they're certainly more capable than I am at writing software right If you give it all the context then yes I I I think that they are they're just so capable It's really remarkable Like does anyone here feel better at writing software than GPD 5.4 Oh all right Writing kernels

06:05
2

Um so even there we're seeing massive gains from Exactly We're and for some of our internal results um that there we're really seeing if you pour the right kinds of of you know if you have the right setup for your problem then you're able to get really massive results out of very low-level um even low-level tasks

06:31
2

And just to give you one example of how things have been trending um one of my systems engineers also very similarly was like hey like I haven't been able to get value out of the models for GPD5 for 5.1 for 5.2 to as well for 5.3 he on a lark prepare had prepared this design document for a very complicated systems optimization he was about to do

06:51
2

he handed it over to the model went to sleep waking up intending to like give this to his team to work on for the next week and when he woke up it was done that the model had actually implemented the initial spec had seen that it was slow had added instrumentation had actually run the code used a profiler to figure out where things were slow and iterated multiple times until it got to an optimized result and like like that is incredible That's where we are

07:15
1

And so how what would you advise all startups here to do because the models keep getting more and more capable They kind of I've asked this uh when Sam was here in the past and you know what if you're building today do you need to rebuild in two years when a new model comes out because all the functionality and all the capabilities all change around you Um do you need to make sure that you're not in Open AI's way because you're going to roll you're just going to run over startups because the models are so much more capable Um h how would you recommend a a set of um startup founders to to build in this environment

07:45
2

Well first of all I would say to lean in the tools right now have become incredibly useful And if you look even over the course of December I think that we went from these agentic coding tools being like you know they're like writing 20% of your code to writing 80% of your code which means they go from being kind of a sideshow to being the main thing that you're doing

08:12
2

And I think we're doing that across all of the work that people do with computers all computer work this year And you can look at the recent progress on codecs really changing from a tool for software engineers to a tool for anyone who's doing work with a computer And just over the past week we've released a bunch of features that just make it so much more powerful and capable

08:37
2

Um and like one thing we just announced today is a new tool called Chronicle that plugs into codecs where it actually can see everything you're doing with your computer and can form memories of of what's going on And so you ask it a question you just it instantly knows what you're talking about

08:52
2

You're like "Huh what was I doing five minutes ago?" It knows right You're like "Oh what was this person talking about?" It knows It's to me it was this real wakeup call to realize you spend so much of your effort right now just explaining to your computer what's going on Like why are you explaining to your computer what's going on That makes no sense

09:13
2

And so I think what's going to happen over upcoming years is the models are going to get much more capable We'll have better harnesses We'll be able to be able to solve harder and harder problems come up with new knowledge all of these things But there is a one-time shift that's happening now which is really about context

09:37
2

It's really about Is your AI able to you have all these meetings you didn't include the AI you know that's not very nice to the AI Like you're asking it to to help you with things and it has no information So I think really leaning into how do you make sure the AI even has enough information in theory to solve the problem and then trust the models are going to really get there and improve So I think it will be a constant cycle of improvement and iteration and leaning into the tools and kind talking to your friends and figure how they are using it but that there is this investment that's a one-time investment that now is the time to make

10:03
1

And in terms of like let's say we you you set that all up How do you how is open AI using codecs differently than you think everybody else outside is using it

10:18
2

Well I think one of the amazing things about being at OpenAI is you do get to live in the future right You do get to really see the shape of what's emerging and we can co-design right we can really change the models the harness everything together in order to better serve the needs that we see and a lot of the approach we've been taking is so we started with software engineering and we set some clear guidelines for example saying that we still want a human to be accountable for all code that gets merged right

10:48
2

so at the end of the day is it a good thing to merge this piece of code is it well structured is going to make our codebase more maintainable we want to make sure there's a human who is signing off to say And that's I think that thoughtfulness of not just saying oh co just blindly use this or you know oh we don't want to use this at all like I think neither extreme is quite right

11:19
2

and then we are also going vertical by vertical within open AI to adopt these tools within finance within sales within IT and there we have a small dedicated team who's really deeply understanding the domain working with the people who are the experts in it in order to build skills in order to modify the codeex UI whatever it is that is is needed in order to get it to be good

11:43
2

and then that's something we can then once we have it in good shape we will externalize and that we're able to to ship that to all of you and so we are starting to work with certain customers as well so for people who want to be very AI forward and want to be part of defining this revolution that there's a place for that and I'd love to talk afterwards but yeah I think that just this desire to say hey we really want to be AI forward really live in the future and experience what it will be like for everyone else one year two years three years down the road

12:12
1

road do you guys structure your company differently or the engineering teams differently because of of the living in the future I mean if you have to go way back when my father learned computer science he was just himself and then we had these long software releases that became waterfall and then when the web happened and the cloud happened we had these two pizza teams and we had scrum

12:32
1

now that we have these coding agents is it is how do you structure around everything differently

12:43
2

I think we're still figuring it out and there's certain places where you really see it For example the cost of building a prototype is cheap now Yeah it's so cheap and if you want to build a dashboard that used to be like h it would take like someone like a week to do it and you just do it now And so actually a lot of the bottleneck has shifted to things like sharing like how do you and so we we actually have some internal work on this as well that again we will be externalizing

13:08
2

of how do you make it really easy for anyone in your enterprise to build a dashboard a widget a bot whatever the thing is and then share it with others and then that starts to really put pressure on having good governance like you want your IT organization to be able to see all these different you know threads of execution that are happening all the little things that are being shared around have some control over data provenence right

13:32
2

to really make sure that okay like a good example of this is um I think people are now starting to take their internal knowledge dumps turn them into wiks We we have some some a really cool one of these internally And the thing you immediately think about is well if someone has a document in the internal knowledge base that was accidentally permissioned incorrectly and they realize oh no I didn't want this information to be accessible How do they fix that Right

13:54
2

So normally it's they go into the doc they change the permissions but now there's these derived artifacts And so you need to make sure you have some way of tracking through the system to say well this output document came from this source one The source one's no longer accessible to this audience let's go and invalidate that as well And so you have to start really building your technical architecture with awareness of the way that people are going to use this information And it really changes how teams relate to each other because you can just it really changes where the bottlenecks are and what's hard

14:18
1

Uh do you think team size is going to be a lot smaller We're going to have still human software engineers in a decade

14:31
2

Well decade is a long time from now and that the ceiling on this technology is hard to is really hard to internalize I think that it is clear that what a company is will change in a lot of ways I think that we're going to have this ability for solarreneurs to build very incredible businesses And so anyone who has a vision I think we'll be able to realize it

15:01
2

I think the jobs that you all have will become way easier in a lot of ways way more fun now Might be more competitive too right Because everyone's going to have these amazing tools And so really figuring out what is your niche what is your unique angle is probably going to become kind of the most important core

15:21
2

But a lot of how we run organizations right now and it's there's almost only one way to organize large groups of people where you have teams and you have management structures and you have scopes and you have these hierarchies and all these things Maybe that can change Maybe you can be much more flat small teams that can really just do incredible things Like we're seeing it right now in mathematics where these individuals on the internet are using GPD 54 Pro to solve these unsolved math problems Normally you need a math team and they're just doing it

15:46
1

Yeah my my son's a math nerd I just told him that maybe you should be studying something else besides math But I

15:55
2

Well but see this is the question right is if you look at something like Alph Go you know move 37 this move that just like changed humanity's understanding of of the game But the thing that was surprising is it made the game more interesting and important for humans And maybe that'll be true for for these other domains too

16:12
1

True What about uh common failure modes when you're building when you're you're building with uh production agentic workflows What do you what do you see as the common things that founders get wrong and they're building incorrectly these days

16:26
2

Well I think that these models they have such power and really understanding how to operate them well takes thought and so we've been investing a lot in primitives security primitives observability having again good governance things like that Um but just to give you one anecdote that I think is evocative um

16:46
2

I asked so I was working with my codeex I asked it to install some package that someone had open written ran into an error I was like "Oh ping that person on Slack and ask them for help." So it pinged the person on Slack

17:01
2

Two minutes later it said "This is taking too long I've escalated to the person's manager." And it actually pinged the person's manager And and you realize it's like on the one hand it's kind of a reasonable thing for the model to do It's being proactive It's trying to solve my problem It's like you know not just sitting around waiting to be told what to do

17:16
2

But on the other hand like you know maybe should have taken a little bit longer Maybe should have checked with me And so I think that really thinking about these questions where we're still building up the EQ of the model and that in some places it's getting very good For example clicking approve approve approve is kind of where we've been And humans are not very good at that either right It's like they just they just default They just default

17:41
2

And so now we're starting to have AIs that can actually take care of flagging is this a high-risisk action Hey this one should be escalated This one's okay to auto approve And it really makes you realize that human attention is going to be this incredibly scarce resource right The doing of things now is easy The is this a good thing Is this what I wanted Is this aligned with my values with my desires that is going to become the single most important bottleneck And so I think building systems that take that into account and really think about the human factor like that's the most important thing to do

18:07
1

Now another human factor security um how would you advise people to think about security in this world of AI and just heard about breaches left and right with Versel recently and then and these models are incredibly powerful at finding security holes So how how would you recommend people here use the models to to find those security issues

18:27
2

Well I think there's a couple levels to the answer I do think that this is I think that the internet has been a place where security has been just like a a ratcheting important concern over time You think about where it started going through the '9s with viruses and worms and malware and those things and we've moved past that

18:42
2

Um I think we are also moving now to a much more ultimately secure regime but it does require kind of a internetwide effort to get there And so a lot of this honestly is just again leaning into the technology having these models They can scan your codebase they can actually be used for end-to-end red teaming Like there's a lot that can be done with them

19:07
2

And a lot of how we're thinking about further models and improvements there is really leaning into how do we how do we actually sort of leverage trusted access programs How do we leverage the community of people who really care about being defenders and making the internet more secure I think that's something where everyone has a role to play and can participate

19:32
2

But the number one thing is just sort of recognizing that these models are very powerful but they're not magic right that they are just like a part of the overall resilience ecosystem And I think that we as a society and I think every company again really contributes to this have something to build in terms of how do we how do we incorporate these in a way that results in more assurance and more sort of certainty on the impacts of of whether it's a particular patch that you're taking whether it's thinking about how do you make sure that you're um yeah just sort of rolling in updates quickly as they're being released

19:57
2

Um so I think that there's a lot of work to be done but I have a lot of optimism for where this is going

20:05
1

Um let's switch to speed Seems like things are moving faster and faster and faster We're in the world of accelerating change We were talking about it when we when you uh you were walking up here around how how you're trying to keep up with things How how do you you keep up with all the accelerating change How would you recommend everybody here keep up with everything that's changing

20:22
2

Well I think this is the new normal and I think to some extent it's not really because of AI I think it's just been the trend of technology for the past two decades There's more people doing things It's easier to do things than ever Barrier to entry goes down means it's also much more easy to build value right To have great successes And so I think that really trying to keep your ear to the ground and understand what's changing

20:48
2

And to some extent it always starts with the same thing which is play with the technology yourself Like it's very different to hear AI described versus to use it But the beautiful thing about AI is it's so intuitive Like that's the whole point is that rather than have the machine be something you have to contort yourself to the m machine canorts itself to you right It's doing work for you and it should be something where you ask it and does something

21:14
2

And so I think that just really trying to just get your finger on the pulse of what's changing what's possible where the models lag That is I think the core skill that is going to really determine a lot of the success of of companies in the future

21:27
1

And then on the flip side of that you guys have held up held back models to work with security agents So it's like the opposite of like going as fast as possible So um you're doing things responsibly too So how do you like think about the balance because you're in a competitive environment you want to ship as quickly as possible and yet you're trying to do the right thing as well

21:45
2

Yeah I think at a values level like what OpenAI is about like we really want to put the power of AI in people's hands like we believe that people can we want to empower people to build the future with the tools that are being created but we need to do that in a thoughtful way right

22:05
2

that we really think about both sides of here are the benefits here's the risks how do you maximize the benefits how do you mitigate those risks and I think that in cyber security and in biocurity those are areas where we're very thoughtful we've been building we've been working on these kinds of both mitigations and trusted access programs for quite a long time

22:30
2

and that what we see coming is models that are going to be increasingly powerful and capable in a continuous way across all dimensions of capability and the you know we announced last week uh the expansion of our trusted access for cyber program by the way has anyone here applied no one oh I see one hand two hands okay more of you should apply it's great

22:55
2

um we really need help because and and it's very important that people who are trustworthy and responsible and really want to push these models are participating in this because that is how that's going to pay dividends for everyone Uh we're going to have more to announce over upcoming weeks on how we're expanding the program

23:20
2

But and also when we release models to everyone kind of the mitigations that that we have and how we're going to tune those to be both to really balance right to really try to bring these capabilities as broadly as possible while also making sure that the ones that are you know that we're thinking about the risks and and able to uh to have some observability over them and to ensure that that this is maximally positive in terms of deployment

23:41
2

So I think the short answer is like it's core to our mission We care a lot about the impacts of what we're doing not just building the technology in isolation but it is a whole community a whole world effort to really get to where we need to be on

23:52
1

um now moving up from the models to the application layer which is what a lot of people here are building How do you how does OpenAI decide what in the application layer you're you're going to build and what you're going to leave out

24:11
2

Well people have probably seen the word focus being applied to OpenAI uh quite a lot recently possibly for the first time Smiling in a while And um it's been applied to her too And it's it's hard because the field of AI is one of opportunity right It's like anything you're going you can imagine is going to be great No question It's going to be great

24:31
2

And we as a company as a single company no matter how much compute we build no matter how many people we have are only going to be able to do so much And so a lot of where we've been how we've been thinking about things is what is the sort of most focused strategy that covers the parts of the space you know maybe it's an 8020 or just like the parts of the space that we think we can have most impact on

24:59
2

And I think there it's very clear right now we're going through this agentic transition And so products that are and it's not just about enterprise versus consumer right So it's like clear we are being very serious about enterprise like we're selling to to big companies and and building a whole muscle and sales motion there But consumer what consumer is is going to change right It's kind of a very broad term that buckets in multiple things

25:24
2

But that the slice of consumer that's about not just productivity but about goals about achieving your goal about even knowing what is your goal being able to elicit that and having an AI that can proactively do that It's all kind of the same thing Like in the end we're trying to build an AGI that you can talk to that has all this context that you can use in your personal life your work life that's trustworthy right

25:51
2

That you can go to it for advice and give you useful information maybe health information or maybe about finances or uh you know about if you're trying to figure out what to do with your career like all of these things they all kind of ladder into one thing and it's meant we had to make some very painful decisions about what not to do but I think I would just say that that's the aperture that we look at things through and that things that acrue to that singular vision of what we want to build you should expect us to pursue

26:15
1

Got it Um do you think we'll be coding with command lines and agents in in a few years or it's going to be completely changed

26:30
2

I mean I think that we're in a very unnatural state right now for how we work Like we all sit behind this box and kind of type away And it's very clear our bodies were not designed for this We got our carpal tunnel and our you know hunch shoulders and all these things And I don't think we want that I don't think any of us wanted that

26:51
2

Like I think that we want more free time We want more But it's it's not even about free time necessarily right It's like you want to spend more time with your loved ones Yes you want to spend more time like talking to people and like coming up with like brilliant visions or just like what you're excited about or just understanding yourself

27:11
2

So it's kind of like do you do you want to be a CEO of an organization of like 100,000 agents Like that actually seems pretty good And I think that we're all going to be able to get so much more done But the mechanics of it are going to feel as different as like going from having to write out things with you know by hand with a quill or something to being able to uh you know just send a text message and have people go and and you know working on your behalf on your goals

27:31
1

All right we talked about compute we talked about uh model and security and agents and app layer Let's talk about frontier When when are the models going to be good enough to push the frontiers of science physical AI Seems like we had Jen Fam here It seems like LMS have been a great scaling law for digital intelligence It hasn't been as strong for robotics for physical intelligence for aspects of biology and science where the problems are probably a lot harder to verify or takes a long time to verify Well how are you keeping track of science and and physical AI in in the world

27:58
2

Well well science is one domain that we're really leaning into and we see line of sight to really incredible progress And we're starting to have some signs of life and I I think it's always important to ground in what is happening today when trying to predict what will happen six months a year from now

28:16
2

So for example we had a physics result where our AI came up with this very beautiful formula that physicists who've been working on this for quite some time thought was totally impossible Thought it was like maybe an unsolvable problem and like it's pretty significant right It's like real serious physicists who um who who really view this as a step towards really being able to get to um to to some sort of answer for quantum gravity and all these things

28:39
2

not there but it's a step that's much bigger than where we were just a couple months ago and so it makes you really wonder a year from now like how far will we have traveled now things like biology that they are different from physics and math right that they are you got to leave your beautiful simulated world and you know deal with messy reality

28:59
2

but I think we've been learning how to deal with messy reality in other domains software engineering is a perfect example where we've really realized that just building the thing that solves competition you know programming competitions like that's not enough Like you need something that's seen real world messy code bases humans interrupting it different ways like this adversarial banging at it

29:19
2

And I so I think that that on science I expect we're going to see a real renaissance You know maybe we'll see some big results this year Next year I think is going to be a totally wild wild time We live in interesting times

29:42
1

Um I I promise that I get you out on time because you're a busy man Um before we let you leave we got one minute on the shot clock What since you have no time but soon you will have lots of time Um what do you and Anna do for fun

29:56
2

H fun I mean same as anyone like like to watch movies go on hikes those kinds of things Um you know not as much time for it as as maybe we'll we'll hopefully have post AGI Um but you got to kind of enjoy the the ride along the way Thank you Greg for joining us Thank you everyone

点击任意行跳转 · 悬停可向 AI 提问

内容简介
OpenAI's Greg Brockman: Why Human Attention Is the New Bottleneck

In a recent conversation with Sequoia Capital, OpenAI Co-founder and President Greg Brockman shared insights into the current state of artificial intelligence, the roadmap to AGI, and the fundamental shifts occurring in how humans interact with technology.

The Infinite Demand for Intelligence

Brockman describes OpenAI’s business model in strikingly simple terms: the company buys, rents, or builds compute and resells it at a margin. He notes that as long as that margin remains positive, the company will continue to scale aggressively because the global demand for solving problems—and thus the demand for intelligence—is effectively unlimited.

Despite being a major player in the GPU market, Brockman admits that the company is "constantly out there hunting for more" compute. Since the launch of ChatGPT, demand has consistently outpaced the ability to ramp up hardware.

Scaling Laws and the Path to AGI

One of the most profound observations Brockman shares is the empirical nature of scaling laws. He likens them to scientific truths, like Newton’s laws, where pouring more compute into neural networks results in predictably more capable models.

"Neural networks were really designed in the 1940s before they were computers... as you pour more compute into the models they get correspondingly more capable and it just keeps going. There's no wall."

Brockman estimates that we are currently 80% of the way to AGI. He supports this with anecdotes of internal models autonomously completing complex systems optimization tasks overnight—performing profiling, instrumentation, and iteration without human intervention.

The Agentic Shift and the 'Context' Problem

We are currently undergoing a transition from AI being a "sideshow" tool to becoming the primary driver of work. Brockman highlights that in some areas, AI has gone from writing 20% of code to 80%.

To support this, OpenAI introduced Chronicle, a tool that allows AI to maintain context by seeing everything happening on a user's computer. Brockman argues that the biggest current hurdle isn't model capability, but context: "Why are you explaining to your computer what's going on? That makes no sense."

A New Bottleneck: Human Attention

As AI makes the "doing" of things easy and cheap, the bottleneck shifts from execution to judgment. Brockman emphasizes that human attention will become the scarcest resource. The most important questions will no longer be about how to do something, but whether an action is good, aligned with our values, and truly what we desired.

Frontiers of Science

Beyond coding and productivity, AI is beginning to push the boundaries of human knowledge. Brockman cites a recent result where an OpenAI model derived a beautiful physics formula related to quantum gravity—a problem previously thought impossible by experts. He predicts a "renaissance" in science as models learn to navigate the messy realities of biology and physics.

Conclusion

For founders and builders, Brockman’s advice is to "lean in." By ensuring AI systems have the necessary context and information today, users can ride the wave of continuous model improvement that defines our current "accelerating change."

00:00 / 00:00
1x
