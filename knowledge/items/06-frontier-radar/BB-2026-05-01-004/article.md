# 构建未来：Demis Hassabis 谈 AGI 路径、架构缺口与深科技创业 | BestBlogs.dev

- BestBlogs URL: https://www.bestblogs.dev/video/b820e09
- Extraction: DOM text from BestBlogs page
- Extracted chars: 9924

---

VIDEO
93
⭐ 精选内容
How to Build the Future: Demis Hassabis

Google DeepMind CEO Demis Hassabis 解释为何他将 2030 年设为 AGI 时间线，哪些架构缺口仍未解决，蒸馏如何重塑模型部署，以及为何今天创业的创始人必须将 AGI 到来纳入路线图。

⭐ 推荐理由诺贝尔奖得主、DeepMind CEO Demis Hassabis 亲述 AGI 剩余技术缺口：持续学习（灾难性遗忘）、长期推理和高效记忆系统仍未解决。他将锯齿状智能定义为当前智能体最核心的失效模式，并解释蒸馏将使前沿级智能在边缘设备普及。需要将 AGI 时间线纳入产品路线图的创始人和研究者必读，提供了目前最权威的第一手判断。

展开
Y Combinator
关注
·
04-29
·
7 个章节
·
查看原文 →
构建未来：Demis Hassabis 谈 AGI 路径、架构缺口与深科技创业
章节导览
7 个章节
CH.1
Introduction and AGI Outlook
00:00
CH.2
AGI Architecture Gaps
02:01
CH.3
Distillation and Model Efficiency
05:28
CH.4
Agent Evolution and Reasoning
08:00
CH.5
Open Source and Multimodality
11:48
CH.6
AI in Science and Biology
14:01
CH.7
Advice for Deep Tech Startups
15:51
📝 实时字幕
跟随播放
全部字幕
00:00

Continual learning, long-term reasoning, some aspects of memory—these are still unsolved. I think all of these are going to be required for AGI.

00:07

Depending on what your AGI timeline is—mine's like 2030 or something like this—then if you start off on a deep tech journey today, you have to just consider AGI appearing in the middle of that journey.

00:13

It's not bad necessarily, but you have to take that into account. You have to have an active system that can actively solve problems for you to get to AGI.

00:21

So agents are that path, and I think we're just getting going.

00:39

Demis Hassabis has had one of the most unusual careers in tech. He was a chess prodigy as a kid, then designed his first hit video game, Theme Park, at 17.

00:48

He then went back to school, got a PhD in cognitive neuroscience, published foundational work on how memory and imagination work in the brain.

00:56

And then in 2010 co-founded DeepMind with one mission: solve intelligence. And I think they've done it.

01:03

Since then, his lab has gone on to do things most people thought were decades away. AlphaGo beat a world champion at Go.

01:13

AlphaFold cracked protein structure prediction, a 50-year grand challenge in biology, and they gave it away for free to every scientist on Earth.

01:20

That work won him the Nobel Prize in Chemistry last year. Today Demis leads Google DeepMind, where he's building Gemini and pushing toward artificial general intelligence.

01:27

Please welcome Demis.

01:53

When you look at the current paradigm—large scale pre-training, RLHF, chain of thought—how much of the final architecture for AGI do you think we already have and what's fundamentally missing?

02:01

I think the components that you just mentioned, I'm pretty sure will be part of the final architecture for AGI. I can't see a world in which we will realize in a couple of years this was a dead end.

02:14

But there still might be one or two things missing on top of what we already know works. Continual learning, long-term reasoning, some aspects of memory—these are still unsolved.

02:32

It might be that the existing techniques can just scale up to that with some innovation. I don't think it's more than one or two big ideas left that need to be cracked.

02:51

At DeepMind, we work on both those things. Working with a bunch of agentic systems, the wildest thing to me is to what degree it's the same weights over and over.

03:01

This idea of continual learning is interesting because right now we're sort of cobbling it together with duct tape. I studied how the hippocampus works and integrates new knowledge gracefully into the existing knowledge base.

03:31

Our very first Atari program, DQN, mastered Atari games by doing experience replay. We borrowed that from neuroscience and replayed successful trajectories many times.

03:54

Even though we're working on machines, not biological brains, and potentially you could have millions or tens of millions context window, there's still a cost to looking it up and finding the right thing relevant for the specific decision.

04:13

Humans have a few digits of working memory. We have million or 10 million context windows, but we're trying to store everything in that—things that are not important, things that are wrong—it's pretty brute force.

04:51

We've worked on agents since the beginning. Atari work and AlphaGo were agent systems able to accomplish goals on their own, make active decisions, and make plans.

05:28

Today you need bigger models to be smarter, but we're also seeing distillation working where smaller models can be quite a bit faster. Our flash models are finding they're 95% as good as the frontier at one-tenth the price.

06:01

We serve billions of users across Search, Maps, and YouTube. They have to be served fast and efficiently, which gives us an incentive to make flash and flashlight models extremely efficient.

07:20

Small models allow for faster iteration and edge deployment for privacy and security reasons. Robots in your house will want efficient, powerful local models, perhaps orchestrated with bigger models in the cloud.

08:00

Not having continual learning is holding back agents from doing full tasks. They don't adapt well with the context. They need to be able to learn about the specific context you put them in.

08:35

In reasoning, I think we're doing fairly simplistic things. There's scope for monitoring the chain of thought or interjecting midway. Sometimes systems get into loops of thinking.

09:10

You get this "jagged intelligence" where it can solve gold medal IMO problems but make basic elementary math errors. There's something about introspection of its own thought process that's missing.

10:01

We're only in the last couple of months starting to find the really valuable places for agents. It's moving from a toy demonstration to actually adding value to time and efficiency.

10:28

I haven't seen a kid making a hit game that sells 10 million copies yet using these tools. Something is still missing, maybe to do with the tools or the craft required.

11:48

We're huge proponents of open source. AlphaFold was put out for free. We want to create world-leading models for their sizes, and Gemma has had 40 million downloads in two and a half weeks.

12:41

Gemini was built multimodal from the start. We believe we'll gain from that in the long run for world model building, robotics, and digital assistants that need to understand the physical world.

14:01

Isomorphic Labs is trying to build out the drug discovery process beyond AlphaFold. We're about 10 years away from a full virtual cell simulation that is useful for experimental prediction.

14:31

Data is an issue. If we could image a live cell at nanometer resolution without killing it, we could convert biology into a vision problem, which we know how to solve.

15:00

Step one was solve intelligence (AGI), step two was use it to solve everything else. I meant solve "root node" problems in science that unlock whole new branches of discovery.

15:51

For a startup, I recommend intercepting where AI tech is going and combining it with another deep technology area like materials or medicine. This creates defensible value.

16:48

The problems I look for involve massive combinatorial search spaces where brute force fails, a clear objective function to hill climb, and enough data or a simulator.

17:32

We haven't seen genuine massive discovery from AI scientific reasoning yet. It's missing analogical reasoning and the ability to come up with interesting hypotheses, not just solve them.

18:35

If you start a 10-year deep tech journey today, you must consider AGI appearing in the middle of it. Build something that will be useful when that world arrives.

点击任意行跳转 · 悬停可向 AI 提问

内容简介
How to Build the Future: Demis Hassabis

Google DeepMind CEO Demis Hassabis recently joined Y Combinator to discuss the roadmap to Artificial General Intelligence (AGI), the evolution of AI agents, and how AI will fundamentally transform scientific discovery.

The Roadmap to AGI

Demis Hassabis estimates that AGI could be achievable by roughly 2030. While current techniques like large-scale pre-training and RLHF (Reinforcement Learning from Human Feedback) are essential components, several 'big ideas' still need to be solved to reach true AGI:

Continual Learning: Systems must learn to integrate new knowledge gracefully without forgetting previous training.
Long-term Reasoning: Moving beyond simple chain-of-thought to more robust planning and introspection.
Memory: Shifting from brute-force large context windows to more efficient, brain-inspired working memory.
Agents and Model Efficiency

Hassabis emphasizes that the path to AGI is through agentic systems—AI that can make active decisions and plans to accomplish goals. Currently, these agents are held back by their inability to adapt to specific contexts.

To make these systems practical for billions of users, Google DeepMind focuses heavily on distillation. Smaller 'flash' models are now reaching 95% of the capability of frontier models at a fraction of the cost, making them ideal for edge deployment in devices like home robots where privacy and speed are paramount.

Solving 'Root Node' Science

The core mission of DeepMind has always been: Solve intelligence, then use it to solve everything else. Hassabis views AI as a tool to unlock 'root node' problems in science.

One major focus is Isomorphic Labs, which aims to simulate a full 'virtual cell' within the next decade. By converting biological processes into a computational vision and reasoning problem, researchers could predict drug interactions and biological outcomes without exhaustive physical experimentation.

Advice for Founders

For entrepreneurs starting 'deep tech' journeys today, Hassabis offers a clear warning: Assume AGI will appear in the middle of your company's lifecycle.

He recommends building products that intercept the AI curve and applying AI to domains with massive combinatorial search spaces—like materials science or medicine—where brute force fails but AI reasoning can excel.

00:00 / 00:00
1x