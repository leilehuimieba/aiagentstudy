# 用 Gemini 构建 Conversational Agents：Interactions API 与 Live...

- BestBlogs URL: https://www.bestblogs.dev/video/f787338
- Extraction: DOM text from BestBlogs page
- Extracted chars: 10981
- Original publisher URL: https://www.youtube.com/watch?v=cVzf49yg0D8

---

VIDEO
92
Building Conversational Agents — Thor Schaeff and Philipp Schmid， Google DeepMind

Google DeepMind 工程师演示 Gemini 的 Interactions API 和 Flash Live 模型，覆盖 server-side state、context caching、agent skills、tool calls、WebSocket 音视频流和生产级 conversational-agent 场景。

AI Engineer
关注
·
昨天
·
6 个章节
·
查看原文 →
用 Gemini 构建 Conversational Agents：Interactions API 与 Live API
章节导览
6 个章节
CH.1
Introduction and Workshop Setup
00:14
CH.2
Introduction to Interactions API
14:06
CH.3
Server-side State and Caching Mechanics
20:38
CH.4
Hands-on: Building Coding Agents
30:07
CH.5
Gemini 3.1 Flash Live Overview
48:38
CH.6
Real-world Applications and Best Practices
01:01:55
📝 实时字幕
跟随播放
全部字幕
00:14
1

hello everyone hello perfect it's just that Philip and I were both Germans and we thought it was funny maybe we we can do it in German actually

00:29
1

looks like there's a there's a German crew there which is nice uh no no worries we'll we'll we'll do it in English

02:25
1

hi I'm Thor or to for the German speakers amongst you um hi I'm Philip um only Philillip so for German and English speakers yeah it's nice

02:32
1

we so we work on the developer experience at Google DeepMind broadly covering kind of Gemini API and also uh working on Google AI studio as a tool for you know developers to try out the models quickly

03:07
1

who has used AI Studio before google AI Studio okay couple folks great um maybe we can quickly Sorry anti-gravity yeah that's good uh you actually don't need an API key for anti-gravity but um so if you don't have an API key yet uh if you have your machine on you I hope you do

03:57
1

it's it's it's a hands-on workshop i do apologize they took away your tables um so it's a very laptop situation uh like literally uh laptop um I hope you didn't bring your Mac Mini or whatever

05:29
2

it's my personal account and we cannot change language so uh you need only a Google account so no credit card no nothing all of the things we are going to do is part of the free tier

08:41
1

mostly it's clock code that is like pushing their API keys to to to GitHub so I recommend you don't do that no just just kidding just remember it is a secret API key um so treat it like a secret

09:06
1

I'd love for you you know to just briefly introduce yourself if you want to and just sort of you know let us know what you would like to get out of the workshop maybe there's a specific use case you're working on

10:24
3

yeah Gemma 4 and Gemini i'm one of the few who are using it for coding and stuff as well by H& um I'm also running it on the classes actually oh nice and I want to see more of this you know

12:43
1

vision claw if you haven't heard of that uh pretty pretty fun open source project um and I think you can run it uh sort of on the well now that Meta has opened up the SDK for the the Meta Rayban uh you can actually hook in something like Gemini Life API

14:06
2

I have like 10 15 minutes slides um to give a bit of a background what we are going to use to build the first session which I'm going to do is more on like the building an agent without any live audio input that's where to take over later

15:11
2

anyone of you used the interactions API one okay two okay at least some person so the interactions API is a new API we launched in December and beta which hopefully will succeed generate content soon

16:40
2

when we launch the interactions API we also launch deep research so maybe you have used deep research in chat GPT or in the Gemini app where you basically start off a query and then you get back a plan

18:50
2

we also introduced state on the server which will which we will use for building our agents so we don't need to manage our loop and always send back the whole history very similar to uh responses API

20:27
2

generate content is what we have today interactions API is what we will have tomorrow we will have um serverside state management but you don't need to use it

22:06
2

the model needs to encode all of your input tokens and you can cach those encodings for a follow-up request to save cost and cache requests I think are 90% cheaper for the input tokens

23:52
2

basic chat usage with serverside state becomes very easy because we have our interactions create call so we define our model we define our input what's the capital of France we get back the output

25:47
2

this becomes very helpful when you build agents where you have a loop and always need to append new user input and um as mentioned before that also works for agents and models

28:17
2

we check what the the output of the interaction is requires action basically means you as a client you need to do something so the output generated some function call or some object which you need to react to

30:07
2

you can search for Gemini API Docs coding agents you zoom in ah yes sorry of course um I can also Can you see it yeah I think you can also just Google I mean I can skills Gemini agent skills

32:06
2

we have the Gemini interactions API and here you can either pick the the first command or the second command depending on what you want and then like just copy it uh open your workspace

35:18
2

the importance when creating skills is it should be either something the model cannot do reliably or if you have some personal preferences on like how to do a certain workflow

37:02
2

we have two new like very basic very very basic file implementation so we have a read file tool with a file path which uses um Python syntax to open it to read it

39:16
2

inside the agent runs it in a loops until there are no tool calls anymore and if there's a result we basically get back our response

40:13
2

at this time we got our write file tool call and then also we got a hey I have created a thumbs up SVG file with a simple line art thumbs icon

41:44
2

add a similar run command tool that allows the model to execute bash commands creates an implementation blend

43:25
2

any questions regarding the interactions API and the small little agent no okay then you get 8 minutes i do five minutes okay five minutes break

48:38
1

this is now uh Gemini 3.1 Flash life which came out two weeks ago I think um very exciting it's been a while i think the previous 2.5 native audio model was December

50:38
1

you are able to send real time text audio video feeds uh to the model so audio you're sending in kind of you know buffer chunks so of the the real-time audio you're streaming that in

51:58
1

Gemini 3.1 Flash Life it's the model that is now in Gemini Life in your phone so if you're using Gemini app uh on your phone um you're talking to that model

53:53
1

no thinking is actually very minimal thinking um but it means you know the model will respond faster it's kind of lower latency

56:11
1

the server events uh actually let me maybe uh do that again so we say enable Google search grounding connect so what we can see is kind of our websocket uh setup

59:01
1

i understand you're asking about the weather in London but unfortunately the Google grounding but for some reason it's Yeah so with the Google grounding it should work so I I wonder if I messed up something

01:01:42
3

is there any real life use cases that this is being used for that's very creative from a like a business context very see what you've done today is a lot of fun

01:01:55
1

Shopify has it in production with Shopify sidekick um there is uh a bunch of so like uh actually one that I really enjoy if you Gemini life API blog uh we had kind of a a case study which is um this startup yeah so I mean stitch is using it

01:04:11
1

in Argentina uh so they are building these um voice sort of companions for the elderly uh in combination with uh kind of an app uh for sort of the caretakers or you know the the the the children of the elderly

01:09:45
1

if you don't need kind of the fully real time um then like using Gemini you know just flash to you know transcribe is actually pretty good

01:16:32
1

I mean on for the demos the there's definitely a lack of best practices in terms of like system instructions and you know there's a lot that you can do sort of with uh the you know better system instructions

点击任意行跳转 · 悬停可向 AI 提问

内容简介
Building Conversational Agents with Gemini: Interactions and Live API

Google DeepMind engineers Thor Schaeff and Philipp Schmid recently hosted a hands-on workshop detailing the next generation of conversational AI tools. The session moved beyond basic chat interfaces to explore how server-side state management and real-time multimodal models are changing how developers build agents.

The Shift to the Interactions API

A central focus of the workshop was the Interactions API, which is set to succeed the current generateContent method. The key innovation here is server-side state management. Previously, developers had to manually manage conversation history and send the entire transcript back to the model with every new turn. With the Interactions API, the state lives on the server.

This shift enables context caching, a massive win for developers. By caching input tokens for follow-up requests, the cost of input tokens can be reduced by up to 90%. This makes long-running agentic loops significantly more viable from a cost perspective.

Building Agentic Skills

Philipp Schmid demonstrated how to equip Gemini models with "skills"—specific tools that allow the model to interact with the real world. During the hands-on portion, they implemented:

Read/Write File Tools: Allowing the model to manipulate the local file system.
Run Command Tools: Enabling the model to execute bash commands and create implementation plans.

The philosophy behind skills is simple: give the model a tool for anything it cannot do reliably on its own or for workflows that require specific personal preferences.

Real-Time Intelligence: Gemini 3.1 Flash Live

Thor Schaeff introduced Gemini 3.1 Flash Live, the native audio/video model powering the Gemini Live experience on mobile devices. Unlike traditional pipelines that use separate transcription (STT) and synthesis (TTS) steps, Flash Live supports multimodal streaming.

Developers can stream audio and video buffers directly to the model via WebSockets. This architecture supports features like:

Low Latency: Minimal "thinking" time for faster responses.
Google Search Grounding: Connecting the live session to real-time web data.
Multimodal Input: The model can see and hear the user simultaneously.
From Prototype to Production

The workshop highlighted that these tools aren't just experimental. Shopify Sidekick is already utilizing these technologies in production. Other use cases include voice companions for the elderly (such as the startup Hey Ado) and specialized coding assistants.

As the ecosystem matures, the presenters emphasized that the next frontier for developers is mastering system instructions to better define model behavior and ensure safety in these increasingly autonomous conversational systems.

00:00 / 00:00
1x
