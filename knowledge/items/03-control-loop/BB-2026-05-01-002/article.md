# Codex 与子智能体：OpenAI AI 工程平台深度解析 | BestBlogs.dev

- BestBlogs URL: https://www.bestblogs.dev/video/8460a7a
- Extraction: DOM text from BestBlogs page
- Extracted chars: 54949

---

VIDEO
93
⭐ 精选内容
Codex and Subagents — Vaibhav Srivastav & Katia Gil Guzman， OpenAI

OpenAI 开发者全面演示 Codex 平台——子智能体并行执行、插件生态、后台自动化、Guardian 安全门控与 MCP 集成——揭示其达到 300 万周活跃用户背后的工程能力。

⭐ 推荐理由Codex 并非只是编码助手——OpenAI 将其定位为软件工程智能体，可在读取-规划-执行循环中运行测试并协调子智能体。本期 59 分钟深度技术讲解完整覆盖子智能体并行执行、插件生态扩展、Guardian 安全门控与 MCP 集成，揭示 Codex 获得 300 万周活跃用户背后的工程基础。适合正在评估 AI 工程智能体平台的团队。

展开
AI Engineer
关注
·
04-29
·
11 个章节
·
查看原文 →
Codex 与子智能体：OpenAI AI 工程平台深度解析
章节导览
11 个章节
CH.1
Codex: The Software Engineering Agent
01:53
CH.2
Model Evolution and Performance
04:08
CH.3
The Codex App and Cross-Platform Support
07:05
CH.4
The Plugin Ecosystem
10:13
CH.5
Background Automations Demo
14:10
CH.6
Visual Development and Game Creation
19:39
CH.7
State-of-the-Art Code Review
25:15
CH.8
Parallel Scaling with Subagents
30:15
CH.9
Custom Subagents and Personas
42:12
CH.10
Experimental Features: Guardian and Hooks
46:44
CH.11
The Bleeding Edge and Q&A
52:12
📝 实时字幕
跟随播放
全部字幕
00:14

hi everyone thank you for being here so today we're going to talk about codeex my name is Katya Katya Gilusman and I'm with VB

00:23

we are both working in the developer experience team at OpenAI based in London and so our role is really to help developers build and get the most out of our products including Codeex

00:37

and so today we're going to start with a quick CEX overview uh just so we know how many of you here are using Codex can you raise your hands yay okay cool so we we're not gonna stay too long on that overview part

00:56

and then we're gonna we're gonna do some demos so we're going to show you plugins and automations VB is going to talk about sub agents and then about the bleeding edge so hopefully for those who already know Codeex and use it you'll learn something that you didn't know about

01:16

and then we'll have some time at the end for Q&A so um feel free to ask anything

01:21

also this is a a workshop format so you know if you have like a a pressing question um feel free to ask and I see you all have your laptop so also feel free to kind of follow along with us

01:33

we're going to show you how to do some things and you can like try it at the same time and during the Q&A that's also like the perfect time as well to try things on your site

01:44

okay so um to start just for those who don't know Codex or even if you know it maybe you don't know it that well

01:53

Codex is our open eyes is open software engineering agent so it's not just a coding agent it's not just a you know an agent that writes code

02:00

it can do much more than that it can run commands it can run tests it can explore code bases it can really do everything that a software engineer would do

02:12

and so it's based on our models as a foundation so for example GPT 5.3 Codex was uh our previous ones we also have the Spark version which is like the super fast model that that we have the the state-of-the-art model right now is GPD 5.4 and we also have a mini version that came out last week

02:33

and you know every time we make improvements every time we have better models Codeex benefits from it but it's not just the models on top of that foundation we have what we call a unified agent harness

02:47

that will manage uh evaluates the agents behavior and that is a wrapper for tool execution for environment setup for everything that uh can let the agent uh do its work and run smoothly there's also safety uh the safety embedded in that harness so all of that is Codex

03:06

and then you can interact with it through different surfaces so you have the Codex app that we're going to talk about in a in a few minutes uh you can also interact with it through your idees with the extension you can interact with it through the CLI

03:20

and also through other services like Slack for example at OpenAI we all the time just like ping codeex in Slack and ask it to fix things or in GitHub as well

03:34

on top of all of that you can also integrate it with your preferred tools so that it can really uh work with everything that you're already using so you know you can integrated with Figma with linear with notion all of that combined can let you really like do every can let codeex do everything that a software engineer colleague would do

04:00

and so as I mentioned this is based on uh our models and so I'm going to let VB tell you a little bit more about that

04:08

all right um good morning everyone

04:15

so um as we've been talking about um the Codex app the IDE um extension the CLI and so on and so forth all of these like harnesses as well as all of these services would not be nearly as good without the models sparring them right

04:31

and just to sort of like take a step back back when I join joined OpenAI which is not really as far back along was in December

04:38

um our leading model at that time was GPD 5.2 and um and from there we went on to release GPD 5.2 CEX which was a specialized um you know um codex variant of GPD 5.2 you wherein we we sort of pushed how far you can you can take the model and um you know run it on longunning tasks

04:59

how far you can let it just continue chugg along um and then shortly after we followed up with GPD 5.3 CEX

05:08

um shortly after that in partnership with Cerebras we followed up with uh GPD 5.3 CEX Spark

05:15

um and and most recently we had uh we released GPD 5.4 for and um you can already see how we're sort of you know pushing this whole sort of model and harness flywheel as fast as possible trying to bring the next for u next frontier as um as fast as possible to you all right

05:36

um something to note is uh and and and something that's not on the screen is uh at the same time we also whilst we were pushing for larger models which are um really good for um longrunning tasks as well as really complex tasks and so on and so forth

05:56

um we also released uh GPD54 mini uh and GPD54 Nano which you can use for um short running tasks

06:02

and sub agents um which we'll talk about in a bit um and um and something that we haven't really um emphasized on this uh over here is um is two things

06:10

one that as we as we sort of pushed on making these models better we also worked quite a bit on making sure that these models um can be served to you as fast as possible

06:20

what that means in principle is um we um we introduced something called websockets which allow us to um sort of create a connection between your um your device

06:28

as well as where the where the API resides to be able to uh give you roughly about 1.75x uh faster tokens without um without really like paying the cost over to you at the same time we also released um a fast mode which allows you to on top of the 1.75x get 2x more faster tokens

06:43

and um and this is something which the team is continuously sort of hammering on um there's there's lots more speed improvements coming um over there and so um to bring this all together um at the start of this year we we brought together u the Codex app how many of you have used the Codex app

07:05

all right that's a that's a fair good chunk of uh people

07:11

um to be honest back in December um and and and even before I was a hardcore CLI user and um at some point um during the app launch while sub was beta testing it doc fooding it I um you know the Codex app became really like a really important part of my workflow

07:32

and the reason for that is uh it it brings together a really nice way to work across projects number one and number two within within a same project work on multiple features at at the same time

07:46

the way you can do that is um you can have indiv individual projects like you can see on the on the left side you can have the codeex project chat GPD sora and so on and so forth but also within those you can you can use um work trees to work on individual sort of feature requests or you know bug fixes or just that Q&A

08:03

all at the same time uh without really interfering with individual tasks this is something which um we're quite proud of um and you know providing a native work tree support helps you um do the same task and do multiple tasks at the same time without really having to context switch as much um at the same time um through the launch we've been trying to sort of increase um the net benefit you can get out of the Codex app

08:29

um and some of these features have been um like you know having a better automation support uh automations is is also something we're going to talk about just in a bit um but the short summary of automations is that you can essentially have a um have a rough process that you want Codeex to run

08:44

let's say every day at 9:00 a.m or let's say every evening or let's say you want Codex to look through your calendar uh and and and create like a briefing for you and that all is possible all within like the native uh codex app setup with um with automations um and then of course with the with the work trees and like more native git support

09:07

um you you can sort of work across projects and um uh and just be able to you know push changes as you want with whatever git persona you want to uh do it with um last but not the least based on which surface you use uh you use the Codex app on um at the start of the year we released it just on Mac OS but now we have uh native Windows support

09:30

which comes along with native Windows sandbox is there anyone here who's using Windows today i'm cheering for you man and um

09:41

so uh for the for the for the one gentleman over there uh we have native sandbox support uh in Windows we're the first of kind um there is no other um you know competing harness which supports like a native sandbox for uh Windows cool and so I've been talking on and on about like the Codeex app uh been talking about you know all the models that we've been shipping but what's what's new in terms of all the features um that we've shipped

10:13

um this is in I think if I'm not wrong in the in the sort of descending order so most recently we launched plugins um plugins is um is a way that you can bring together skills MCPS as well as prompts and you know any other thing really uh together in one bundle and allow the model to do more nuanced uh matching whilst it's building

10:30

um we also released recently mini models um which tie in quite well with sub aents which allow you to parallelize uh a particular feature or bug request or Q&A whatever it may be um at um at a faster rate all whilst making sure that you don't pay as much cost for your uh for your particular models

10:50

um and then we have like bunch of other stuff which we which we're going to talk about as we go through uh some of this is you know how you can uh how Codex is so good at like code review how Codex is really good at security um and so on

11:14

all of this um whilst we talk about all of this um I want to sort of emphasize on this fact that um we're at OpenAI quite lucky that the community has really embraced Codex in fact just um just last night we crossed the milestone of uh of crossing 3 million weekly active users uh and this is a pretty big deal um uh for us and we we want to continue sort of supporting the developer community the the you know enterprises startups building on codec so um throughout the session if you have any questions please feel free to throw it at both Katya and myself um or even afterwards or just you know ping us um with this I'll pass it over to Katya thank you

12:04

and yeah the the three million weekly active users thing is really it's really cool to see and it's crazy to think that it's also more than tripled since January so just in a few months we've seen like huge adoption and uh yeah and it's it's uh it's really really cool to see um okay so plugins um plugins I don't know if you've heard about it it's it's quite new on Codeex uh the the native support for plugins

12:31

uh the idea of plugins I'm going to show you what it looks like in practice and how you can use them is that they bundle a bunch of things together so like skills apps integrations uh MCP servers and they they bundle that into reusable workflows and so what uh skills apps and MCP servers are again I'm going to show you but just to introduce that a little bit

12:58

so skills are essentially um reusable instructions packaged for specific processes so if you have something that you're doing quite a bit uh you can actually create a skill for it so that codeex knows about it you can give it instructions you can give it scripts as well resources and all of that uh will save you from just repeating yourself over and over

13:20

so every time you have like a sort of neat workflow that is always the same you can package that into a skill you can actually ask codeex to create the skill for you as well and then apps are connections to other services so uh you know again uh we we'll see a quick demo but the the tools that you use every day like notion linear all of that uh you can let codeex connect to it

13:40

and MCP servers uh you might be familiar with this already but um they basically expose tools for codeex uh to just extend its capabilities further and it's tools from external systems and so all of these three things are already very useful on their own and what plugins do is that they bundle that so that you don't have to you know set up everything manually you don't have to install multiple skills you don't have to connect multiple apps you don't have to connect multiple MCP servers you can just add a plug-in

14:10

and another thing I wanted to talk about in the Codex app and that we'll we'll show a quick demo for um is automations personally this is like one of my favorite things to do with Codex uh because you can set up automations that run in the background so like a chron job and you can connect apps you know you can use uh plugins there too and just set it to run on a scheduled uh time

14:39

for example you know you can set an automation for to run every day at a certain time and uh it's just an instruction that Codex will run in the background and the last thing I wanted to show you with the demo right after is uh specific skills for web app and game development because we've uh you know we've heard a lot about developers who want to to use codeex to build these things to build apps to build games and every time you know they kind of repeat themselves every time they kind of use the the same skills so we actually packaged that into specific plugins

15:14

and uh there's two skills that I want to highlight uh that are super useful and honestly that are a game changer when you're developing something visual it's um playright interactive and so for those who don't know playright is essentially like a a a headless browser like a um you know a sandbox browser uh that you can that Codex can just run and use that to see what it's doing

15:37

so you can open your app in a browser and with the interactive version you can actually click things and uh you know just navigate your app um and and take screenshots and see the and analyze as those screenshots and then image genen uh is a great way to just generate visual assets for your apps and games

15:53

so enough talking i'll show you a demo um I'm going to start by actually running this uh this one because this one is pretty long

16:06

uh when I ran it yesterday it took like an hour to build so I also have like the final version but I wanted to show you like this this prompt how Codeex is going through it

16:15

and so what I'm doing here is I'm using uh the game studio plugin which is again a bundle of a bunch of skills that are helpful for uh game development and I'm asking it to use imagen to create visual assets so sprites for the games and using uh playright interactive to also debug the game and make sure that it works well so we're going to let that run and uh then we're going to talk about plugins for a little bit

16:38

so let me switch to another project here uh so this developers website one okay so this one is uh the repo for our developers website which is here sorry I'm going to put that in full screen

16:51

um and so on our developers website we have this page with all of the codeex meetups we have so you know there's a lot and all of that is actually in our repo like in our codebase in YAML files and so I'm what I'm going to do is I actually added this Google Drive plugin here uh you know we have a lot of featured plugin uh built by us that you can choose from

17:18

you can also of course add your own plugins but I connected this Google Drive plugin that lets Codeex access my Google Drive and so what I did is that I prepared this uh this spreadsheet called Codex events with the event name date and city and I'm gonna ask uh codeex to just update this sheet with the current codeex meetups uh listed in the codebase

17:35

i'm going to start this again it's going to take a little while uh and so let's check in on okay for the the game task is still running i'm going to show you when it's doing a little bit uh uh some more interesting things

17:47

but the last thing that I mentioned is automations and so automations is again something that you can just set up using apps do you can just ask Codex anything but instead of it being interactive like you're actually using the Codex app you can set it up to run in the background

18:04

so for example some ofations that I set up um that are honestly helping me a ton in my day-to-day lives – is one for Slack messages so I connected Codex to Slack and I'm asking "Hey Codex can you check uh every day at 9:00 a.m the messages that I should reply to and flag if it's time sensitive or waiting for an urgent response"

18:25

can you also do a summary of all the things uh that have happened since yesterday on Slack uh and I'm asking that to bucket it to bucket uh per topic. And then uh important information to be aware of so we have like important channels where company information uh generally the the things that you can uh that that that leaks in like one day but uh gen so uh important company information is in there

18:47

and so I just want to make sure that I don't uh miss anything here so that's the kind of stuff that I asked Codex to just summarize for me another one uh that is uh pretty cool is the is connecting Gmail and same thing like I receive honestly an ungodly amount of emails per day and so I'm just asking codeex to check if there are emails that I should actually reply to and uh you to check you know if it's timesensitive or if it looks legit or not

19:15

because I do get a lot of requests that's not necessarily something that I would uh that I would uh uh reply to but this is like saving me hours per per day and so the way you can create automations is you can create it from here or you can also just you know uh say something like uh hey codex can you uh create an automation that will um look at Slack and look for anything that mentions uh codeex use cases and then uh list all of the important use cases that I should um that I should uh put on our website

19:39

so I'm gonna let Codex think about this for a second i should have used Spark and it's going to come up with this you know it's going to create the automation for me basically and I didn't specify um when I wanted to run it but I can actually like Oh interesting it's doing something different because this is a live demo

20:01

so obviously it wouldn't uh Okay normally it will it should like do a little popup uh so I can just like click on the Oh it's doing it perfect it was just very chatty this morning okay interesting interesting okay so please create the automation so this it should show a little popup if everything goes well but if not you can still like create it manually uh let's just see if it is doing it okay i don't know what's going on but okay let's just do it manually

20:33

so it will you can also create it from here and basically all you have to do is just call the plugins you want to you want to use uh you know like use uh slack and then uh choose you know the frequency where the automation should run which project it should run in etc okay so let's check on our other tasks uh this one is still running okay it generated some pretty cool sprites we'll look at this after

21:04

let's check on our uh task to update the spreadsheet so here Codex took two minutes to actually analyze the codebase it found the source for all of the Codex events where we have our YAML files and then uh it wrote the 57 event rows so we have 57 events uh currently listed on the website and uh so let's check let's see our spreadsheet and yeah we can see that it was updated nice

21:34

so this is something you know this is a simple example but every time you have something that's very you know uh time consuming and uh anything that has anything to do with data data review for example you can actually ask Codex to do it for you

21:50

it has access to everything uh on your codebase and you can also feed it other inputs you know like other CSV files and then you can just ask codeex to do that type of work for you okay now last thing let's check on our uh game

22:04

so as you can see codeex is actually using image genen to generate I'm going to uh zoom out a little bit so oh Nice so it's generating like all the sprites all the game assets that I asked it to do and this looks pretty nice uh it's also so it's going to take a while

22:26

uh what I'm going to do is I'm actually going to show you um final results but uh as you can see like codeex is just reading um sorry it's just generating all of these assets and then it's going to use the playright skill to see how that looks like in the app so unfortunately we don't have an hour to wait for this final results so let me just show you the one that it did yesterday

22:52

so this is un untouched like I haven't touched it it's literally just CEX um who built this and all of that was like I had I gave zero input i was just like do a platformer game with platforms made of bricks

23:03

that's it and uh yeah it generated everything so granted the the overall UI is not like you know I would probably iterate on that but um I think the the platformer itself is pretty cool and what is really cool here is that literally like all the sprites like here

23:22

you know I'm just like moving all around and you know that that's at least like five different sprites of the little character and I didn't have to do any of that you can also you know do a custom game with your face as input and uh have image gen just like create a a 2D version of you um so that's a way that you can like leverage the image genen skill the playright interactive skills and that game studio uh plugin

23:46

and just to show you what's inside like we have also the same thing for web apps but it's a bundle of like all of these skills together um so yeah that's uh that's it for me uh I'm gonna pass it back to VB thank you thank you got

24:06

all right um perfect so just to do like a very quick uh checkpoint uh and like a recap on what we've spoken so far so we went through like all the um all the models that power the codeex ecosystem then we went through all the surfaces you can consume codex from um and then we went through uh plugins how to use them and what are some of the plugins that you can use you can also create your own plugins um using plug-in creator

24:41

um you and and then we went through uh to speak about uh automations um and imagin and and so on and so forth um now something to note is like as we as we continue sort of delegating more you know more and more work on these um agents it could be any of your favorite agents uh codeex or not – one thing that um that you want to be sure of is whatever it is that your agent produces is of the utmost quality

25:15

which means that um as we as we start sort of working on multiple features at the same time multiple projects at the same time it it's going to be quite likely that it's impossible for you to uh go and look through each and every line of code which means that at least for the first pass you want to have a way um which you can rely on um to review your code and this is where code review um sort of comes in

25:41

um it's um by no means um am I bragging about this but uh in my own biased way uh codeex code review is one of the best in the industry right now this is uh something which you know uh people on Twitter and LinkedIn um on our own uh sort of you know platforms Discord and so on and so forth keep raving about uh that how is codex code review so so good

26:06

um so I wanted to spend like a quick hot minute on um on what it does so first of all um it is available on the surfaces that you work at which means number one you are able to use codeex code review on GitHub um so you can connect your chat GPD account with GitHub and for each and every pull request that you create

26:27

um you can set it up such that codeex can automatically review each and every pull request and it would typically give you um you know some sort of a uh some sort of a you know um what's this called a call out like this on the pull request itself saying that hey like this is something that is missing hey maybe you know P 0 fix this P1 fix that P2 you know this is something that would be a good to have and so on and so forth

26:52

uh at the same time you can use slash review on the on the Codex um CLI or the Codex app and Codex will spin up you know large um sort of review process and so on and so forth um and very recently last week uh with my colleague Dom we shipped um a clot code plug-in for codeex

27:10

which allows you to um you know essentially invoke codeex within your clot code sessions to be able to get the same sort of state-of-the-art code review but in your plot code sessions um so um something to sort of see here is let's say that I am working on a project like this by the way this is my this is my actual working setup at work – I this is like all which I work on

27:50

uh I'm not like everything that you see here is like all of these threads all of these projects is something which I work on day-to-day so if you see something which you shouldn't just close your eyes – and so typically what I would do is I I would go through you know like a like a feature request or I would go through um you know some sort of ask from from someone

28:15

um and um uh let's say over here I asked the I asked Codex to do a bunch of things so I'm just going to ask it to review its changes um and so then you get an option to you know either choose from a base branch if you have multiple branches in in the git repo

28:31

you can choose it against a feature branch against an eval branch whatever it may be and so on and so forth uh in this case I'm just going to ask you to review um uncommitted changes – and what it does is if you see um here what it does is it spins off a totally new thread

28:51

um and what that thread would do is um is it would essentially spin up a totally new CEX process which has uh like our own you know review system prompt um and it would continue sort of looking through not just the diff or like the list of all the changes but it would also contextualize it with everything that is there on the uh on the model repo itself right

29:08

and so a lot of the times um um codeex code review will like find find out changes which would have second order effects um which is not limited to just the you know diff or whatever changes you've made but also to some other like modules which you haven't even touched in the pull request itself or in the changes itself

29:24

and this Um this is so effective that 100% of pull requests across all open air repos made by all employees um including Greg are are reviewed by Codex code review by default um and that's when uh you know that's the first pass that you take um cool and so as you can see over here um Codex worked for a minute and it came up with these with these sort of uh you know updates

29:47

like P1 you know localize whatever revenue revenue detail P2 uh translate this to this and um and so on and so forth and what you can do like after this is like essentially ask codeex to uh either like take a pass at fixing this or like open another sort of PR on the on whichever branch you're at and then sort of go on from there cool

30:15

now we get to sub aents which is something which I'm personally quite excited about so – first and foremost what is sub aents sub agents is the um is is essentially the ability – wherein you can spin off um a master task into decomposible parallel and independent tasks which you can hand off to agents which can uh which can allow these agents to sort of work independently and then at the end of their run get back to you and um you know give you a response

30:44

and um over here like sky is literally the limit – like you can spin up as many agents as you want um of course as long as your API key or your uh you know whatever charge GBD pro plus go subscription you're on u can can can take um you can do a lot of like interesting things uh with sub aents

31:08

um for example what I'm doing um on the screenshot on the left is um I have a codeex agents repo which we're going to look at in a sec it's not public yet but I hope that we'll be able to make it public very soon

31:21

which has a lot of personas for sub agents that you can use so it's kind of meta it's it's essentially sub aent personas like doc reviewers or you know um test case creator or test case runner and and so on and so forth and what I um every now and then we would change the change the spec this is from before we wanted to change the spec of how um how sub aents work so what I wanted um it to do is to go through all of these 40 50 different sub aent personas review them and and and make sure that they are up to spec

32:02

and of course doing it without sub aents would have meant that um codeex would open each and every file and then review it and then give me a summary and continue doing it for like 50 different sub aents in this case um it it essentially created review slices which means it created say you know these are the two uh files that um that you know uh sub agent poly or sub aent Plato uh should you know uh essentially review

32:19

and then they would spin up a new codeex environment they would review those and then at the end CEX will collate all of these and um you know give me back a response so let's let's give this a shot – so the repo in question is this – it's um it's just a codex agents repo which has bunch of personas – you can see that we have um we have quite a few sort of personas over here

33:20

um we've got like an accessibility reviewer architect and so on and so forth and this is like actually something which you can create yourself and we're going to touch on that in just a – in just a minute is um you can you can define your own custom sub aents right

33:38

um but think of this repo as like a collection of these sub aents and – this is typically what you would have for for each and every sub aent you would have a name you would have a description you would have a different sort of like you know sandbox mode whether you want it to be write only whether you want it to be read only – you and then you would have some sort of like you know instructions – and so on and so

34:04

now what I'm going to do is I'm going to ask Codeex to – I'm going to go over to my Codeex agents – I'm going to switch to let's do medium over here let's close this can I make this full screen all right – so let's give it give it a task – spin up 20 sub agents to review all the sub agents

34:31

so this is a very simple task all I'm asking uh codex is to do u the same task which I was showing before – wherein I wanted to review all the different sub agent personas in this repo and you can see that um uh you know there's it it already figured out that there's like agents and skills and it's looking into it there are 45 curated persona files and uh what what it's going to do is it's it's going to create 20 reviewers

35:00

and um um it it's going to give them all of those um um toml files and then it's going to review those and you can see that um there's two things which is quite interesting over here number one Codex automatically decided that this is potentially u a complex task so it automatically kickstarted the plan mode

35:22

which is what's active over here so you can see that uh it – it essentially came up with five tasks u to solve this particular problem – you can explicitly invoke plan mode as well but uh in this case it decided to do it on its own – it's it's then partitioning all of these persona files

35:40

um and then it's going to spawn 20 sub aents very soon – I swear it's faster – but um – so now what it's doing is it's – Oh – so for some reason on my on my particular setup I have a cap on six like six concurrent agent threads that can be run at the same time – we can fix that

36:03

um but to go back up what we can see over here is that uh it at least spin up six agents which is my limit – for now and I can see all of those agents – you know working over here i can quickly see like what Jason the agent over here is doing – or Hume and so on and so forth

36:23

and you can see that – something to note here is that the the main codex model over here hi the main codex model over here – essentially created a persona right – a and and – additionally it also gave it some some insight on – there's there's repo guidance in repo.mmd in contributing.mmd in skills and so on and so forth

36:52

and – it will sort of continue going down this this route for all the different sub aents right – and what it does towards the end stage is that – it will tear down all of these sub agents when when they have gone through – when they have gone through their whole process of looking through all the TOML files

37:12

and so on and if I go back to – my main thread – you can see that two of the agents are are still working – but eventually like it would collate all of this feedback that it that it has gotten from – all of these individual sub aents and you know proceed – now you can you can think of this this is like a very simple sort of explorer use case right

37:39

but you can think of this from for example a cyber security perspective wherein you have – a git commit or you have a a particular git repo and you want codeex to spin up and run multiple – you know vulnerability – sorry one sec you wanted to create multiple sort of you know vulnerability analysis from different points of views or from different hypotheses and you wanted to sort of tackle the same diff or the same GitHub repo and try and come up with like a vulnerability map right

38:08

and this is something we actually use – um – quite a bit or I personally use quite a bit when I'm brainstorming a particular feature i would just spin up multiple codec sub aents to sort of look through how I would approach a problem right

38:32

so let's say I want to add a feature i would ask Codex to create a plan for what are say five or six or 10 different ways that – that a model – that a particular feature could be implemented and then I would quickly double down on could – like and ask codeex to – then create multiple sub aents to get me some sort of understanding for – for these tasks sorry my watch was constantly vibrating

38:58

um and – and so that's like – that's like a quick highle overview of how sub aents work – by default we ship three sub aents – three sub aents personas – let me quickly open so by default we ship – three personas one is like a default general purpose fallback agent another is a worker which is sort of execution focused so this is something that you would use for – when you want codeex to write a particular feature request – or work on a particular feature

39:37

then there's explorer which is the same one which we used – before and – and then for for each of these you can double down and create your own codeex – sub aent personas like we saw before and we will create one right now – something to note is – is that these particular sub aents – they like for each of these you can define what model you want to use you can define what reasoning effort do you want to use you can define what sandbox mode do you want to use and so on and so forth

40:09

um the reason why this is important is for a review agent you would almost always 100% want to use the review agent in readonly mode you would never want your review agent to execute anything right – for same reason for like a cyber security vulnerability u assignment you would want your – your sub agent to always be in readon mode

40:31

but for a for a – for like a docs writer or for something which like you know creates – docs for a particular feature that you've created or a bug report and so on you do want to give it write access so that it can execute stuff and also create a – create a bug report for it as well um something to note is that you can also double down and give these – sub agents you know more capabilities by giving them – MCP access

40:58

so you you can just give – let's say you can give a sub agent MCP access to Sentry so that it can look through all of your – um – all of your reports over there or like one sub agent access to your linear – you know backlog so that it can – it can interact with linear it can – read through all the – um – all the issues added to you triage them and so on and so forth

41:29

you can also give them skills – so really like you can – um – if you really want to you can quite heavily customize this entire setup for your own – for your own use case so let's open – our codeex app again you can see that it went through all of these sub aents it created a bunch of – other sub aents just to go through all of these and – it came up with these findings

41:51

um it's like based on readme based on contributing – performance investigator – is overprivileged – P1 has a sandbox mix – sorry verifier has a sandbox mismatch same for writer and so on and so forth and so you can see this is already quite useful – and it saves you quite a bit bit of time to be able to go through all of these – individually or sequentially and so on and so forth

42:12

um now let's go back and see a bit more about custom sub aents – so as I mentioned that we ship three – sub aent personas but at the same time you can create your own custom sub aents in fact we do recommend creating your own sub aents or just ask your your codeex to look through your past sessions and create sub aents for you

42:32

both of these scenarios work and – work quite well so in – in this particular case – you can see that we have a PR explorer sub agent which – reads your – your codebase uses GPD 5.3 codex spark which is our – research preview model text only – deployed on Cerebras – and is blazingly fast is quite fit for this particular use case and we set sandbox to read only so we don't want the model to sort of execute

43:03

and we give it certain u you know ex in instructions so in this case we say hey stay in the exploration mode – trace the execution path you know – don't propose any fixes and – and and – just like you know search through and – and and figured out like what – what exactly do you want us to do – now let's quickly try and try and – create a sub agent so let's say we want to do – docs researcher

43:34

in this case what I – typically do is to just go and ask – hey Codex can you create this sub agent – for me – here's – here's its persona – and then let's see and so what Codex is going to do because Codex is aware about – about how it works and you know – what it's supposed to – do and where it's supposed to place – all of these things – what it's going to do is it's going to create a TOML file for this docs reviewer

44:01

and in this particular case this is this uses the docs MCP server which we created – um – from the DX theme – which packages all the API references all the docs all the guides all the you know toolkits and so on and so forth and – it will add that as an MCP server so that every time we ask it – ask it a question about hey like what's the best way to use GPD 5.4 before with websockets

44:33

or what's the best way to use GPT realtime with – um – with I don't know pick your favorite way of using GPT real time and – and can you create a react plug-in for this and so on and so forth – um – it would be able to reference all of these things so I'm gonna let it do its thing and in the meantime – head back over to the slides and so just to go back sorry one second

45:06

um what you can do just to sort of invoke – you know a particular sub agent is you can say – hey can you reviewer sub agent and review each and every persona based on the developers docs

45:22

so – in this case you can – you can essentially like use the same particular – sub agent – leverage it again and then ask it to do the particular task that you want to do now what are some like interesting ways that you can use this is – imagine like you have like a long build process or you have a test process

45:42

you can have a sub agent which can run your test case locally you can have a sub agent which can – always make sure to – oh I'm – I'm being told that I don't have as much time – um – you can have a sub agent which can pull the latest from – from GitHub as soon as you do a pull

46:01

you can have a sub agent which can – you know quickly – pull all of the context from a linear issue and so on and so forth so really like you can – you can – you can do this for you can leverage this for a lot of – things and the best thing that I like to do is to just ask codeex to look through my past sessions and recommend me certain automations certain sub aents and so on and so forth that I can use

46:20

cool so now we're at the – at the bleeding edge – this is bunch of stuff which we have shipped in the past and – we haven't really made as much of a splash about – so – what we're going to do is we're just going to quickly go – around and see like what each and every one of these – um – do and – how you can leverage them

46:44

first and foremost is guardian approvals this is an experimental feature you can activate it today – by just going on /experimental – so it would be something like – codeex hopefully it works and then you can look at – experimental and you can – in – in my case I already use cardon approvals and you can activate it this way

47:20

um what card approval does is – all of us including myself at some point were – guilty of using yolo mode all the time which means that you by default give unfettered – access to your coding agent to do literally whatever the hell it wants right

47:40

and this by all means and measure is not safe – hence we came up with something called guardian approval which for each and every time codex needs – a privilege needs to run a privileged task let's say it is can I remove this particular directory can I run a server can I expose a particular file to – um – to the internet whenever all of these things sort of pop up

48:06

what Codex will do is it will spin up a new sub agent right – which will based on a particular prompt try and verify whether or not this is something which needs my human interruption or not – and in most cases it doesn't need – you know – human interruption so it will just say hey go on run this particular – you know – privileged tool or privileged task and so on and so forth

48:26

and – this way what we – what we hope to do is we hope to reduce the human fatigue – that comes by just – you know – always sort of having to approve – you know – do this task do this run this particular – bash script or run this – and – and – so on and so forth in – in principle how would that look is – trying to see if there was – Uh

48:53

okay it doesn't show – show it to me right now but if I just in the interest of time I'm going to ask – hey can you run the dev server and I'm going to instead of full access mode – which for some reason again I'm not able to – click on let's – let's try and see – if it – if it invokes – guardian approvals

49:19

whilst this – this works I'm going to head over – to the next step which is hooks hooks is also something which is experimental right now we're – we're trying 24/7 to try and make this – a better experience – currently Codex supports three hooks one is after each tool use one is at the start of a session and third is at the – when you stop a session

49:40

what hooks allow you to do is it allows you to programmatically ask codeex to do a thing x – based on a particular event so let's say that when you start your – your codec session you want codeex to pull the latest from your GitHub repo so in that – in – in that particular case you would want to set up a start hook

50:00

if you want Codex to do something after each tool use let's say – for a lot of researchers who want to document each and every tool use they might have like a per tool use hook wherein they document what Codex has done – per session and so on and so forth so you can do that with that

50:22

um and – last but not the least something which I personally use is the stop hook which is when I'm running long running tasks I would – at the end of each turn – of codeex I would ask it to keep going so that like it just continuously – you know – continuously keeps running a particular task

50:45

and – in – in theory how this would look like is – um – is Where is it is – sorry one second wow i was really prepared for having more time – um – I have to say but –

51:05

in theory how this would look like is – um – is – that you have some sort of a Python script – and you have – you define like a hooks.json

51:19

so in this particular case you can see over here that you have a pre-tool use – you have some sort of a – you – know matcher you say like on startup or resume run this particular session dot session start py and so on – and you can define how you want to – in this particular case

51:44

um – so what I did for for example – for the sales dashboard example that I've been showing you so far is I created a hook for stop which runs this Python script which is keep going UI – which is every time it encounters the stop – um – hook it would just ask Codex – um – to keep going do one more pass run one one solid validating command type in one more thing and then stop and give the result

52:12

and so for really longunning tasks you can just set it up and like ask it to continue doing its own thing – last but not the least – um – we have personality changes which means that you can go on codeex and you can ask it to – quickly look at personalization

52:32

you can set up different personalities you can set up a more – friendly personality or a pragmatic personality based on whatever you want to do you can also add custom instructions so you can ask it to always site whatever it is it is doing and so on – right

52:53

and then last two things – um – is we released something called codec security this is our state-of-the-art – model which allows you to find and fix vulnerabilities in – in your GitHub projects and – um – you – know – essentially what it does is it would go through commit by commit and – um – it would create a vulnerability patch – and – then and – it would use codeex to then sort of patch the set changes as well

53:21

um – lastly – um – as I mentioned before we released a cloud code plug-in – which allows you to use codeex in – in cloud code – this is something which was – surprisingly used quite a bit by the community – and this is something which allows you to sort of ask Codex to review whatever it is that you've done so far run an advers adversarial review or just like ask Codex to rescue whatever changes you've done so far as well

53:48

um – that's it thank you so much for – for joining us and feel free to ask any questions that you might have hi so we don't have a lot of time for Q&A unfortunately we should have started maybe a little bit earlier but – happy to take maybe a couple questions in the room and then we'll stay here anyway

54:08

so if you have questions and you don't have anywhere to be you can come to us yeah thank you so much

54:13

i have a question you said a couple of times that there's like a way to – uh – scan – uh – let's scan the past sessions and basically give your recommendations for that how exactly do I do that

54:21

like a project with like 20 threads or something like that how you want to scan that

54:27

yeah so what you typically do is like all of the sessions within Codex are put in – uh – dot sessions within a particular within the same codex folder and CEX has the ability to just like scan through all your sessions and then you know

54:42

this using the CLI but not I can do this using CLI but not using the COX

54:47

you can use it – uh – you can use Codex app you can use Codex CLI anything – um – you just have to ask it to look through the sessions and yeah do whatever you want to do nice there's another Oh okay maybe a couple more yeah in the back here

55:14

hi hi is there a way to hand off a task to a cloud agent so let's say I'm here working on a task and I'm I have to close my laptop so I off to a cloud agent yes definitely

55:35

we didn't touch on that but actually – uh – you can do that from the Codex app directly like – um – maybe you can you can show your screen but you can either work locally and as you mentioned you can do it like we support get work trees as well

55:52

but you can also just select cloud here and you can select the number of – uh – times this task should run like you can parallelize we call that like best of n so you can like run it four times in the cloud and then just pick the best output – so that's something that is like built in in the the Codex app in the ID extension and you can also like access it directly from the the web interface and there's more cool stuff coming on that very soon

56:21

more what

56:28

there's more cool stuff coming on that very very soon i think there was one right here yeah

56:32

thank you so much – um – my question was actually about the cloud UI as well because – um – today sub agents aren't supported if I'm not wrong and – uh – especially the thing that bothers me is it doesn't use the – the skills that are in the repo is that coming soon or

56:53

so – um – there's like a – at the risk of – uh – talking about the whole road map – uh – we – we – we – we – definitely have a lot more changes coming up on that particular front – um – I'm not sure if skills within cloud is going to be as soon as I say that it – it's going to be

57:11

but u – it's definitely at the top of the mind and we do want to sort of add – uh – give you the ability to sort of like have your own trusted MCP servers to be able to run there or CLIs and so on – um – and also the ability to just like have SSH agents u – that you can just spawn off – uh – a particular task to on a VM and so on

57:32

lots of work on that like it can use skills in the repo right that – that – is checked in it's not on cloud tasks but like if you – like it – it – reads instructions and stuff and you can like find it and like still see it since it's in the codebase it's more like the – the – skills that you have locally that work the same

57:51

the reason why we don't allow it on – on – cloud is because there's no way for – um – the sandbox to know whether or not a skill is trusted or not right and so that's why we – we – we – don't and like skill can package like a Python script or – or – an execution it won't execute things

58:14

but like if you have – you know – like things like resources it can access it technically because it is like in the repo it's just – Yeah it's not as good

58:22

so I have to request it thank you thank you

58:37

were there any other questions cool have a great day enjoy the day and – uh – if you have any other questions we're going to be around – um – today tomorrow and also maybe on Friday u – feel free to reach out or just like drop a DM and – um – enjoy thank you

点击任意行跳转 · 悬停可向 AI 提问

内容简介
Codex and Subagents: The Next Frontier of AI Engineering

OpenAI's Vaibhav Srivastav and Katia Gil Guzman recently presented a deep dive into Codex, an agent designed not just to write code, but to act as a full-fledged software engineering colleague. With the community reaching 3 million weekly active users, the tool has evolved from a simple coding assistant into a sophisticated platform capable of running tests, managing environments, and scaling tasks through parallel agents.

The Evolution of Models

The foundation of Codex has moved rapidly from GPT 5.2 to the current state-of-the-art GPT 5.4. Performance has been a major focus, with the introduction of:

Websockets: Providing 1.75x faster token generation.
Fast Mode: Offering an additional 2x speed improvement.
Specialized Variants: Including the 'Spark' version (hosted on Cerebras) and 'Mini' models for short-running tasks.
Plugins and Automations

Codex now supports a robust plugin architecture that bundles three core components:

Skills: Reusable instructions for specific workflows.
Apps: Direct connections to services like Notion, Linear, and Slack.
MCP Servers: Tools from external systems that extend Codex's capabilities.

These plugins power Automations, allowing Codex to run background tasks—such as triaging Slack messages or summarizing emails—on a schedule without user intervention.

Parallelism via Subagents

One of the most powerful features discussed is Subagents. This allows a single 'Master' Codex instance to decompose a large task into smaller, parallel chunks. In a live demo, the team showed Codex spinning up multiple agents to audit dozens of persona files simultaneously. This architecture allows developers to:

Define custom personas with specific permissions (e.g., Read-only for reviewers).
Choose different models for different sub-tasks based on the required reasoning effort.
Integrate with external systems like Sentry or Linear at the agent level.
Safety and the 'Bleeding Edge'

To manage the risks of autonomous agents, OpenAI introduced Guardian Approvals. This experimental feature uses a specialized subagent to analyze privileged tasks (like server execution) and determine if they require human oversight, reducing 'human fatigue' without sacrificing safety.

As Codex continues to move toward more autonomous 'Cloud Agents' and integrated hooks for session management, it is clear that the goal is to provide a unified environment where AI can handle the repetitive complexities of modern software engineering.

00:00 / 00:00
1x