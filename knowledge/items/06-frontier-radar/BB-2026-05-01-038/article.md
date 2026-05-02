# 训练前沿小模型的全部经验 | Maxime Labonne，Liquid AI

- BestBlogs URL: https://www.bestblogs.dev/video/afa3a1f
- Extraction: DOM text from BestBlogs page
- Extracted chars: 23346
- Original publisher URL: https://www.youtube.com/watch?v=fLUtUkqYHnQ

---

VIDEO
92
⭐ 精选内容
Everything I Learned Training Frontier Small Models — Maxime Labonne， Liquid AI

Maxime Labonne 解释了为什么前沿小模型不能只靠大模型蒸馏，而需要专门的架构、极大的 token 预算、on-policy 对齐和工具调用能力。

⭐ 推荐理由Liquid AI 的 Maxime Labonne 将小模型定义为独立工程问题而非大模型缩小版：内存限制、延迟敏感和任务专一性决定了不同的架构选择（gated short convolutions、压缩 embedding 层）。最反直觉的发现：用 28 万亿 token 训练 350M 参数模型，远超 Chinchilla scaling 假设。还覆盖 on-policy 对齐和工具调用能力两个生产可用门槛。适合关注端侧部署和小参数量 AI 的工程师。

展开
AI Engineer
关注
·
04-29
·
9 个章节
·
查看原文 →
训练前沿小模型的全部经验 | Maxime Labonne，Liquid AI
章节导览
9 个章节
CH.1
Introduction to Liquid AI and Small Models
00:14
CH.2
Key Characteristics of Small Models
01:46
CH.3
Embedding Layers and Parameter Efficiency
02:53
CH.4
LFM2 Architecture and Edge Performance
04:24
CH.5
Scaling Laws and LFM 2.5 Training
06:13
CH.6
Post-Training Strategies: SFT, DPO, and RL
08:27
CH.7
Solving the Doom Looping Problem
10:33
CH.8
Agentic Workflows and Conclusion
14:48
CH.9
Q&A: Deployment and Distillation
17:25
📝 实时字幕
跟随播放
全部字幕
00:14
1

hi everyone my name is Maxim Labon uh in this presentation I want to talk about the lessons I've learned pre-raining small models

00:20
1

um so for context I work at Liquid AI as head of pre-raining at Liquid we mostly focus on edge models for ondevice deployment

00:27
1

and as you can see here we have models from 350 million parameters to 24 billion parameters so this is very very small

00:35
1

and um yesterday we released our new VLM uh 450M and the week before we released the new version of the 350M model for text

00:44
1

um so this is what we do we work across text uh vision and audio and uh yeah the models are available on hugging face if you want to try them out

00:52
1

um in this presentation I want to talk about what separates small models and big models and there are three main characteristics I want to talk about

01:46
1

so first of all uh the small models they are memory bound

01:52
1

um because the hardware is is what it is right on a phone in a car etc uh we can't really use super big models

01:58
1

uh which is why we try to keep the the size quite small and because of that we have low knowledge capacity compared to bigger models

02:04
1

uh then the models are task specific which is great because if you have uh small knowledge capacity you can at least focus on one thing very well

02:10
1

and so that means that they are usually not general purpose chat boards like charg they are a lot more narrow in terms of focus

02:16
1

and they can do something like summarization tool use very very well

02:21
1

uh so that's the second aspect u and the final one is that it's very latency sensitive

02:28
1

and that means that you need to have very very fast uh throughput

02:35
1

So all these characteristics are very important and we'll see in this presentation how they play with each other and how we can do better

02:42
1

um but the main lesson I want you to retain from this presentation is that small models are not just scaled on versions of bigger models

02:47
1

they also have their unique challenges and we will see about how we do it

02:53
1

um in this presentation the first thing I want to talk about is the model architecture because there's a lot of interesting things that we can do here for edge models

02:59
1

um I want to first talk about uh Gemma 3 270M and Quen 3.5 0.8B

03:04
1

so these models are the smallest version of their respective family and you can see that both of them they adopt a hybrid architecture

03:13
1

uh Gemma 3 has sliding window attention and GQA hybrid um Quen 3.5 has an architecture with gated um delta and gated attention

03:21
1

this is great because this is a lot faster but what I'm interested in here is actually the embedding layer

03:27
1

because if you look at uh the size of the embedding layer compared to uh all the parameters of the model

03:33
1

you see that actually Gemma 3 270M is mostly an embedding layer uh it's 63% of the total parameters

03:39
1

and even co 3.5 0.8b it's it's still like 29% of the parameters

03:44
1

um so that's not super efficient because uh the effective parameters the parameters that are really used for reasoning for knowledge capacity and all that stuff um are not the embedding parameters

03:50
1

um that it's the rest so the effective size is actually a lot smaller

03:56
1

and it means that you could squeeze more reasoning and more performance from the same memory footprint

04:03
1

um and the reason why they do that is because they use distillation uh to train the models

04:10
1

um so they distill these models like those are the uh student models and they have teacher models with a huge vocabulary uh sizes

04:17
1

and this is why um we have these super big um embedding layers

04:24
1

all right uh let's talk about the LFM2 architecture now as you can see the LFM2 architecture is actually not that different uh in terms of um just layers

04:32
1

we also have like a hybrid architecture and this time we have short convolutions and uh GQA

04:39
1

um and I want to talk a bit about well first you can see that um the embedding layer is actually a lot smaller compared to the others

04:46
1

it's like 90% of the parameters so we have more effective uh parameters which is great

04:52
1

and I want to talk about how we created this architecture and we did ondevice profiling

04:58
1

so instead of doing more like theoretical work uh we decided to say like okay let's tried to really implement it on the target hardware

05:04
1

so we had two target hardware here and uh we wanted to see how it performs in real life to be able to optimize um the architecture find the right operators here

05:11
1

and the thing that we found is this gated short convolution block that you can see here and why this is nice it's because it's very very fast

05:18
1

uh the shortcom are a lot faster than all the alternatives you can see here compared to setting window attention from gemma 3 the galet from co 3.5

05:24
1

gated linear attention and group query attention you can see that uh the cost ratio is really in favor of shortcom

05:30
1

which is great because we said that um this is very latency sensitive so this is exactly what we want

05:36
1

so this is quite theoretical but if we look in practice um and we profile uh the inference of these models

05:41
1

you can see here on two CPU um the AMD Ryzen Max Plus 395 and the uh Samsung Galaxy S25 Ultra

05:47
1

um all these models don't have necessarily the same size but it gives you a rough picture

05:53
1

and you can see that the short conf LFM to architecture to be a lot faster and also use uh less memory

05:59
1

um so that's great and you can see also GPU it's not really just for CPU but also on GPU

06:06
1

you can see that it has a lot of uh throughput even at very high uh concurrency levels

06:13
1

all right let's talk a bit about training now so the LFM 2.5 training recipe is quite similar to what you can find find elsewhere in terms of stages

06:21
1

have pre-me training on 28 trillion tokens we have uh supervised fine-tuning preference alignment and reinforcement learning

06:28
1

and here you can see I'm talking about 28 million tokens and I said that we released a model of um 350m parameters last week

06:34
1

um so yeah we pre-train a 350 million parameter model on 28 trillion tokens

06:41
1

if you're familiar with the chinchilla scaling laws that might sound a bit weird because we're supposed to be compute optimal at like I don't know like maybe one billion

06:48
1

not not even one uh trillion parameter i mean um but it's actually not the case

06:54
1

and we see that the performance still um grows when you scale the number of pre-training tokens

07:01
1

and there was a super interesting paper by Robert uh published last week about the test time scaling laws

07:07
1

and you can see here how LFM 2.5M compares to their new scaling laws

07:16
1

you can see chinchilla scaling laws here and the new one that they proposed uh here

07:23
1

and actually we did not pre-train the models on noff tokens we should pre-train even more uh to be optimal according to their laws

07:29
1

but this is cool because more pre-training works and it works even at the smallest scale

07:36
1

which is great because these models are a lot cheaper to train than u much bigger models

07:41
1

and here you can see a comparison it's not just for pre-training it's like post training uh models

07:49
1

and um you can see that the LFM 2.5 model is uh significantly better than the previous version LFM2 350M on a lot of different benchmarks

07:58
1

so you have uh knowledge with GPQ Diamond you have instruction following with IFB bench you have case report bench which is data extraction

08:03
1

and also a lot of tool use with PFCL and and T2 bench um with this model it's only 350 million parameters

08:10
1

so what we wanted to do is we wanted the model to be very very good at data extraction and at tool use

08:16
1

and the rest if it's not the best model at in code it doesn't matter like people don't use it that way anyway

08:22
1

same for math i think it's really nice to try to target some capabilities and not try to be like average on everything

08:27
1

all right let's talk exactly about that post training um small and big models what the difference

08:34
1

uh we have pretty much the same stage so this is not really in terms of stages that we see a difference it's more about how you do it

08:40
1

so for supervised fine tuning is better if you're actually quite narrow and you focus on some task

08:45
1

um it's true for general purpose person training but it's also true if you do fine-tuning

08:52
1

so you can take one of these models on hugging face and just fine-tune it for your use case

08:56
1

and for example you have a use case where you have a particular function that you want to call this is great this is a excellent use case

09:01
1

like the more narrow you can um you can find it or design it uh the better it is

09:06
1

then we have preference alignment so during pre-raining we have our um own on policy length normalized direct preference optimization algorithm that we quite like

09:12
1

and preference alignment is very nice because it brings you general improvements it's not just about benchmarks it's really like overall

09:21
1

after preference alignment the model is better it sounds better and this is really nice to be able to just improve it overall

09:28
1

and finally we have reinforcement learning and reinforcement learning is extremely efficient even at very small scale

09:36
1

it's a really really important technique that we use everywhere and the main thing is that it's very narrow in terms of focus

09:45
1

so you want to have like as many environments as many task as possible and make sure that um you generalize well thanks to this

09:52
1

um then for small models in particular they're quite sensitive to cold start SFT data

10:05
1

so if you have a particular task in reinforcement learning it's always good to have similar samples and a similar task in your supervised fine-tuning mixture

10:12
1

and this is good feedback that you can see during reinforcement learning something doesn't train very well it's probably because you are missing some call SFT data

10:19
1

maybe the task is too complex for different reasons but um you can try to start again uh from the supervised fine tuning uh stage

10:26
1

add your data and then see if it improves anything

10:33
1

all right but there's a new problem uh with small language models that you might have encountered even with bigger ones and this is doom looping

10:41
1

so the problem with doom looping is as you can see here it's going to start repeating a sequence of words over and over and over and over again

10:47
1

and it just like never stops um so this is a problem all the time but it's particularly a problem if you have small models

10:53
1

if you have reasoning models and if you have complex task if the task is basically too complex for the model

10:59
1

hopefully this recipe is not too complex for this model but this can happen anywhere and you have the three of them at the same time

11:05
1

so if you have a tiny reasoning models on like super difficult math task this is the perfect recipe to have a lot of doom loops

11:11
1

um so this is a unique challenge that you find with small models

11:17
1

uh to give you a concrete example and here I can talk about like how we solve it

11:23
1

the first thing is that we solve it during the preference alignment stage and in particular for the data generation part that we do

11:31
1

so here you can see the pipeline that we use uh to do the data generation the on policy data generation for preference alignment

11:36
1

so we start with prompts like 1 million samples to give you a rough idea and then we use the policy model the model that we want to train with temperature sampling

11:42
1

and we just generate five rollouts because we use temperature sampling these rollouts tend to be a lot more diverse and we expect that not all of them will have doom loops

11:49
1

at least one should not doom loop right and on the other hand we generate just one extra uh roll out with a policy model with temperature zero

11:56
1

and this one we think that it's going to doom loop and then we give everything to a LLM jury to score all the um rollouts

12:04
1

we pick the best one the one with the highest score as the chosen answer the one with the worst score as the rejected answer

12:10
1

and the idea is that if we have some doom loop here the response for the doom loop will be rejected

12:16
1

so we will train the model during preference alignment to not do loop and this is quite effective

12:21
1

so this is solution number one and then we have solution number two

12:28
1

and this one is about using reinforcement learning with verifiable rewards and we add a bit of engram repetition penalty

12:35
1

uh but you can see that with reinforcement learning with um verifiable rewards it's a very nice way to actually um solve this issue

12:43
1

because if you have a question like a math question like this one you are going to try to extract the final answer

12:51
1

if you do not have a final answer uh you won't get a positive reward

12:58
1

so this is already being taken care of during um reinforcement learning with verifiable rewards

13:05
1

but on top of that you can add a bit of repetition penalty to make sure that um you are going to generate more like less doom loops in general

13:12
1

and same thing we also use temperature sampling here so the rollouts are also quite diverse and it just is less likely that you are going to get like a lot of doom loops

13:18
1

uh all the time so this is the the second uh solution

13:21
1

and that allowed us to uh really reduce the doom loop ratio

13:29
1

so this is a real example with uh LFM 2.5 1.2b thinking which is a small model it's a reasoning model

13:35
1

and on top of that we threw really hard task at it

13:41
1

so you can see that after mid training the doom loop ratio that we calculated across like a lot of benchmarks was about 15% um or even 16%

13:47
1

and then after SFT it it barely moves like SFT is not the right stage to fix this

13:56
1

um we didn't have doom loop examples during the SFT stage but it's not enough uh to get rid of this issue

14:03
1

um after DPO so that was a first solution um it really reduces quite a lot

14:09
1

and you can see that after reinforcement learning the problem is almost non-existent

14:16
1

if today you try to do the same thing with um quen 3.5 0.8b in reasoning mode you will see a lot a lot a lot of doom loops

14:23
1

which is something that people complain about online and that also shows that the quen 3.5 like this tiny model is just a scaledown version of bigger models

14:31
1

and this is not the approach that we're taking here at liquid we want to say okay like the edge models they are their own thing

14:41
1

and um this is also a way to just optimize the entire architecture the entire cross training stack to make sure that uh we treat them as um best as possible

14:48
1

and finally I want to talk about uh next stage next steps for uh all these uh small models with agency reinforcement learning

14:54
1

the final characteristic I didn't mention here is about being memory bound if you're memory bound it means that you have low knowledge capacity

15:01
1

if you have no low knowledge capacity it means that you're going to hallucinate a lot

15:07
1

but a nice way to solve this issue is just providing like web search tools to the model

15:13
1

if you have a tiny model but it's able to Google everything that you um throw at it in terms of like knowledge questions

15:18
1

you're going to have like much much better performance uh than if you just rely on the uh base models

15:25
1

and same thing with a lot of problems that you can uh throw at the model i think that from experience these tiny models are actually very good at agentic task

15:31
1

and this is how we should use them um it doesn't matter if um they don't have the knowledge capacity of big models

15:38
1

what they truly need is really good reasoning capabilities to make sure that they are able to use these tools in a reliable manner

15:46
1

and another point that I haven't mentioned here is that small models are also not very good at long context capabilities

15:53
1

but it's okay because if you have like a recursive um language model environment then you can use Python and and like basically take a shortcut uh to to solve this issue

16:00
1

so most of the issues that you find with small language models can actually be fixed in different ways it just requires more creativity

16:14
1

it just requires thinking about this problem not like you would think about it uh from a bigger model perspective uh but everything about this is fixable

16:20
1

all right so in conclusion some takeaways um I hope I convinced you that edge models have unique challenges

16:26
1

and they are actually interesting from scientific point of view and also production point of view

16:32
1

um if you combine them with agentic tools they tend to perform really really well and this is something that is currently underexplored

16:40
1

we talk about agentic workloads with really big models but it's not necessarily um the best use case it's not necessarily the best fit all the time

16:48
1

and uh yeah finally we're working on LFM3 and we have like a ton of crazy experiments and uh ideas to try so um come work with us if you're interested uh in this space thank you everyone

17:25
2

yes um can you share a bit about how you use these models in your workflow and how how you make the decision about when to use a big model

17:30
1

yeah this is a good question so the question is like how we use this model in the workflows and uh how we decide between small models and big models

17:35
1

so the the main idea here is that you will try to use the small models when you don't have a internet connection for example

17:42
1

so incar deployment is a good example of that because you can't have like a reliable internet connection so it makes sense

17:48
1

uh latency is also a big one if you have a workload that is very latency sensitive uh small models running locally are always going to be better

17:54
1

and another one is is privacy if you use a regulated environment um if you work in finance or healthcare this is also a good one

18:01
2

in your specific workflow is the question i make the models so I like I make the models for other people but uh like in my workflows like not necessarily

18:15
3

have you tried for D looping have you tried like you talked about how 3.5 is a scale down version of big one y have you seen uh the work that you do with RL and all these reduction of the looping on a bigger model being able to be distilled into a smaller model without having to redo the steps

18:22
1

it's a good question i think we need to do some experiments to see like if just distilling from a bigger model translates well in terms of doom looping

18:33
1

i would say no i I don't think so because I think it would be too close to SFT it depends like how you do this distillation

18:40
1

if you stop K and you have like enough K maybe this is uh good enough

18:44
1

um but I I think that it would not completely be solved and you would still need like several patches to make sure that it doesn't happen again right

18:51
1

yeah all right i think I should quit but um I'll be around if you you have other questions thank you very much

点击任意行跳转 · 悬停可向 AI 提问

内容简介
Everything I Learned Training Frontier Small Models

Maxime Labonne, Head of Pre-training at Liquid AI, recently shared the technical journey of building frontier small models designed for edge deployment. His talk breaks down the common misconceptions about small language models (SLMs) and provides a blueprint for making them competitive with much larger counterparts.

The Three Pillars of Edge Models

Small models are defined by three core constraints that dictate their design:

Memory Bound: Hardware on phones or in cars limits model size, resulting in lower inherent knowledge capacity.
Task Specific: Instead of being general-purpose chatbots, SLMs excel when focused on narrow tasks like tool use or summarization.
Latency Sensitive: High throughput is critical for a good user experience on-device.
Rethinking Architecture

Labonne critiqued the common practice of distilling small models from large teachers, which often results in bloated embedding layers. For example, in Gemma 3 270M, the embedding layer accounts for 63% of the total parameters. Liquid AI's LFM2 architecture optimizes for "effective parameters" by using a smaller embedding layer (roughly 10%) and replacing heavy attention mechanisms with gated short convolutions, which offer much higher speed on mobile CPUs and GPUs.

Challenging the Scaling Laws

In a move that defies standard Chinchilla scaling laws, Liquid AI pre-trained a 350M parameter model on 28 trillion tokens. Labonne noted that performance continues to grow far beyond the theoretical compute-optimal point, making these models significantly more capable per parameter than previously thought possible.

Defeating the 'Doom Loop'

One unique failure mode for small reasoning models is doom looping, where a model repeats the same phrase indefinitely. Liquid AI addresses this through:

Preference Alignment: Using a pipeline that explicitly generates and then rejects repetitive answers during the DPO stage.
RL with Verifiable Rewards: Training the model with reinforcement learning that only provides rewards for reaching a final, extractable answer, often paired with n-gram repetition penalties.
The Future is Agentic

Labonne argues that the low knowledge capacity of small models is not a dealbreaker. By giving these models access to agentic tools—such as web search and Python environments—they can "outsource" knowledge and focus their limited parameters on reasoning. This approach allows a tiny model to perform at a frontier level for specific production workloads.

00:00 / 00:00
1x
