# Context is the Key to the Agentic Architecture Revolution: A Conversation with Baruch Sadogursky

- BestBlogs URL: https://www.bestblogs.dev/article/0c4caf52
- Original publisher URL: https://www.infoq.com/podcasts/context-key-agentic-architecture-revolution/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-05-18 19:00:00
- Capture route: article discovered from logged-in Edge/OpenCLI latest page 2 feed; page/content captured from BestBlogs resource APIs
- Extracted chars: 49291

---

In this podcast Michael Stiefel spoke to Baruch Sadogursky about software architecture in the age of agentic AI. Large Language Models can function, albeit stochastically, as reasoning machines capable of interpreting human ambiguity. With the appropriate rigorous context artifacts to control the LLM’s reasoning, software specifications can become the source of truth, while the code becomes a disposable intermediate language. These context artifacts are managed through an engineering discipline, context engineering. Unlike prompt engineering which Sadogursky likened to "voodoo incantations", context engineering utilizes artifacts such as skills, rules, scripts, feedback, and rigorous evaluation to provide the models with clear intent on what code to write. AI Agents will ask clarifying questions to the architects and clients until the requirements are fully understood. This allows a massive "shift left" to evaluate code quality before it is even written. Testing now validates the accuracy of the specifications.

    Humans are still responsible for determining the correctness of the requirements by providing the proper context, and validating the final results. Since changes over the course of time will occur, resulting in the regeneration of the code from the specifications, microservices is the best architectural paradigm to use given the current limitations on context windows for LLMs. Orchestration of the services is then done by a human architect to create the application. The architect is also responsible for managing the emergent properties of the system.

   

  

  
   
    Key Takeaways

    
     Making software specifications the source of truth is now possible because we have a reasoning agent in a Large Language Model that can interpret human ambiguity. The problem is that because LLMs are stochastic they need to be constrained. Context engineering provides these constraints because it is a legitimate engineering discipline that focuses on providing missing instructions and clear intent to AI models. It differs from "prompt hacking" because it uses context artifacts composed of skills, rules, scripts, feedback, and evaluation.

     Humans are still responsible for determining that the requirements are correct, providing the correct context, and validating that the LLM has produced the correct results.

     AI Agents construct code with question loops to ask customers, clients, architects, and developers to clarify what their intent is until the requirements are fully understood.

     Changes, whether feature requests, bug fixes, or adapting emergent properties to different circumstances, are inevitable. Given current limitations on context windows, Agentic AI development requires microservices in order to allow the service to be regenerated from the changed specification. A human architect then orchestrates these microservices to produce the application. As LLMs evolve this might change, but this is the current state of the art.

     Written documentation now is the source of truth, and code becomes a disposable intermediate language. By examining the specifications we will be able to validate code quality before it is tested, and placed in  production. We still test because there is no guarantee that the specification is correct, or has been correctly implemented. We have specifications, and a record of what the responses to the questions the LLM posed, so we can trace where misunderstandings or errors  in development occur.

    

   

  

  
   Subscribe on:

   Apple Podcasts
   YouTube
   Soundcloud
   Spotify
   Overcast
   Podcast Feed
  

   
  
   Transcript

   Michael Stiefel: Welcome to the Architects Podcast, where we discuss what it means to be an architect and how architects actually do their job. Today's guest is Baruch Sadogursky, who did Java before it had Generics, DevOps before there was Docker, and DevRel before it had a name. He built DevRel at JFrog from a 10-person company through IPO, co-authored Liquid Software and DevOps tools for Java developers, and is a Java champion, Microsoft MVP, and CNC ambassador alumni.

   Today, he's obsessed with how AI agents actually write code. At Tessl, an AI agent enablement platform, Baruch focuses on context engineering, management and sharing. On top of sharing context with AI agents, Baruch also shares knowledge with developers through blog posts, meetups, and conferences like Devnexus, QCon, KubeCon, and Devoxx. Mostly about why context engineering is one of the most important next things. It's great to have you here on the podcast, and I'd like to start out by asking you, were you trained as an architect? How did you become an architect? It's not something you decided one morning, you woke up, you got out of bed and said, "Today I'm going to be an architect".

   Baruch Sadogursky: Thank you very much, Michael, for having me. It's a great pleasure to be in this podcast. And you mentioned QCon which was the conference where we met and kudos to the team. It's one of my favorite conferences, absolutely amazing. It's the same people who do InfoQ, and they do an absolutely tremendous job.

   How Did You Become An Architect? [02:11]

   How did I become an architect? Most of those important decisions in my life up until recently, until my frontal lobe grew up in my mid-40s, were made by my former boss and my lifelong mentor, Shlomi Ben-Haim, who is the CEO of JFrog. We worked together in a small consultancy Java shop in Israel in the mid-2000s. And as consultants, the company sold expertise. So we invested very heavily in this expertise. And it was expected for the top paid consultants in our company to not only be good developers, but actually be architects, which means mostly understanding systems and understanding complexities and understanding when they are needed, and most importantly, when they are not.

   It was kind of on-the-job training. My colleagues back then, again, huge names in the industry like Yoav Landman, another co-founder of JFrog and Fred Simon, another co-founder of JFrog. I was working with them on multiple, very, very interesting projects, and kind of watched what they did and mostly listened to what they say and what they didn’t say and started from there.

   Michael Stiefel: In other words, you sort of stumbled into it and lo and behold, you found out that you are an architect.

   Baruch Sadogursky: Yes, I think that's exactly what happened. I was kind of expected to grow into this role, and this is how that started.

   Once Again - Trying to Go From Spec to Code [03:43]

   Michael Stiefel: When I listened to your talk at QCon, I had a feeling of what the French called an « arrière-goût de déjà-vu » where it seems that everything old is new again. When I was much younger, we tried to figure out how to create requirements definition languages for CASE tools, which were supposed to generate code automatically. So when we're dealing with the AI designer coding agent, how do we express those requirements in an unambiguous way? And of course, this is related to what you were talking about with context engineering as opposed to prompt engineering.

   Ambiguity and the Reasoning Machine [04:26]

   Baruch Sadogursky: Absolutely. And I love your reference because this is 100% true. We've been there before in a number of different ways. We've been there before, trying to write code directly from language. We've been there before in trying to take what is today's programming language and kind of demote it to intermediate language. And it feels like the old is new again, which is true in a way, but I think also there is a tremendous difference. And the difference is that now we have a reasoning machine that helps us do that, that was never there before. And the downsides of the English language as a programming language-

   Michael Stiefel: Or any language.

   Baruch Sadogursky: ... or any language, any human language, of course. Yes, yes. It was always the obstacle, this barrier that was impossible to cross, and this is why all those attempts failed. It suddenly matters less because there is a reasoning entity that can interpret the ambiguities and the unclear parts of what we are saying almost as well as humans. And this is the leap that we needed to make the dream of when we were young, a reality today, or well, not today, but probably tomorrow.

   Michael Stiefel: The question is in these languages, how do we express clearly, the ambiguity? For example, I said this on this podcast several times. I have only done three things in my software career, trade off space and time, insert levels of indirection, and trying to get my clients to tell me what they really want.

   Baruch Sadogursky: Spoken as a true architect. That's all I can say.

   Michael Stiefel: So the first two, I'm sure an AI agent can do well, but the problem comes as you well know, a client says to you, "We have to make it fast". Well, what does fast mean? What does secure mean? Very often, clients present a solution to you, a solution statement, rather than a problem statement. How do you deal with this with the AI agent?

   Baruch Sadogursky: How do you deal with humans? What do they do? So they told you, "We want it fast". What do you do next?

   Michael Stiefel: Well, I ask them fast compared to what? I give them scenarios. I give them monetary trade-offs. You want five nines, this is what's going to cost you.

   Baruch Sadogursky: Exactly.

   Michael Stiefel: But does the AI agent come back at you and ask you those questions?

   Teaching the Reasoning Machine About Architecture [07:10]

   Baruch Sadogursky: It can. The whole point of the reasoning system is only that it doesn't know yet how to. I didn't know in 2003 to ask those questions. When people told me "I want this feature", I assumed that they knew exactly what they wanted and I went ahead and did it and they came back to me and said, "No, that's actually not what we meant". And then it took me a lifetime and I learned. And now when someone says, "I want this feature", I ask them 20 questions before actually doing that. And the agents today are much smarter than I am because it won't take them 20 years to learn that. They have learned it already. We can build systems that will include those clarifying loops in them today. And I have an example, a framework that I wrote called the "Intent Integrity Kit" that has qualifying grounds after each conversation with the customer, with the user.

   Teaching the Reasoning Machine to Ask Questions [08:06]

   We write specs and instead of the agent assuming that it understood what we wanted, instead it will start grilling me with questions until it's really clear for the reasoning system what I really meant. And it does it over and over again at every step of our process. It will ask it about specifications, it will ask it about features, test features, it will ask it about the tasks that it already compiled from what should have been already clarified, but it finds new gaps. And instead of assuming stuff, like a good architect, it will come to ask and ask us again, "I see that this task, I thought I knew what it should be, but I actually don't. Tell me more".

   Michael Stiefel: So is this something that you trained and built yourself or is it something that you built on top of something else?

   Code As an Intermediate Language [09:02]

   Baruch Sadogursky: The way the Intent Integrity Kit started was a re-implementation of the Spec Kit by GitHub. But the Intent Integrity chain by itself started with this understanding that the barrier that prevents us from making the programming language as the intermediate language is exactly what we spoke about, is those ambiguities between what people want, what they say they want, and what the machine understands that they want. And the only way, as any architect knows, to clarify that is to ask questions.

   Michael Stiefel: Incidentally, just as an aside, almost every time I give a prompt to an LLM, one of the parts of the prompt always is don't be obsequious.

   Baruch Sadogursky: Exactly. And the other is to ask clarifying questions. And not only that, you can actually force that. Not only should you ask questions if something isn't clear, because as we know, the model is trained and then rewarded for actually not doing that, for saying it's all clear and then implementing it, so you can force it. You can say, ask at least three clarifying questions. It will force it to think and then it will find actually 20. But the process of triggering this reflection is something that we can do today.

   Context Engineering is Not Prompt Engineering [10:30]

   Michael Stiefel: So what you're essentially, if I understand, related back to what you said before, is that this is all about setting the right context for the agent. Let's explore this a little more because there's been a lot of emphasis on prompt engineering. We get this over and over again, and of course there are those people who say that prompt engineering is going to be taken over by the AI agents themselves. So that makes it even more important that we understand what context engineering is. And perhaps for our listeners, perhaps you can expand by, because this is the concept under which we're talking.

   Baruch Sadogursky: Absolutely. And that relates directly to what we just spoke about, that the agents and the model have to have enough context to not have those ambiguities. And the way we provide context to LLM is through prompt. We give it information. And what was called prompt engineering was never engineering. It was an honest attempt to tweak the prompt in a way that the agent and the module miraculously will receive out of thin air the context that it misses. When people say, make no mistakes, they hope that the agent in the model will receive a divine, how do you call it…?

   Michael Stiefel: Revelation.

   Baruch Sadogursky: Yes, divine revelation of what we want and then make no mistakes. The problem is not the mistakes. The problem is that it does something else. And it's not because it's not good enough. It's because you didn't tell it what to do.

   Michael Stiefel: Yes.

   Baruch Sadogursky: And this is why prompt engineering was never engineering and why those magical incantations don't really work because they don't solve the fundamental problem of lack of context. And this is where we actually enter the real engineering discipline, which is context engineering. And while technically it's absolutely the same thing, the approach is what makes it different and the approach is obviously that it is engineering. And what does engineering mean? It means that we think about requirements and the requirements are not some weird stuff. The requirements are how do we provide missing instructions of clear intent from the human to the machine? Those are requirements of an engineering task. And then we think about how can we measure what we did? What is the feedback loop that will tell us whether the context we provide is enough or not enough? Is it good or not good? And then obviously we are able to do it repeatedly.

   That's another aspect of engineering as opposed to voodoo magic and how do we scale it? How do we make sure that the way that Baruch found to provide context, Michael can use as well? So those four points are what makes prompt engineering a proper engineering discipline. And this is how it differs from the voodoo incantations of make no mistakes of prompt hacking.

   Human Responsibility for the Machine - Human Interaction [13:53]

   Michael Stiefel: What I like about what you just said was it does not relieve the human from their responsibility. The human still has to be in the loop and is still responsible.

   Baruch Sadogursky: Absolutely. And this is, by the way, very good news for our entire industry. It actually amplifies our expertise and makes it even more important because at the end of the day, we are the ones who are in charge of providing those requirements. We can dream or dread the day in which the machines will figure out what we need and then just go ahead and implement it. But until then, we are the ones that define the requirements and our expertise is absolutely critical to make sure that the agents have enough context, which is the correct context, context which is framed right to do the right thing, no amount of "make no mistake" in the prompt can generate that.

   Michael Stiefel: So what I hear you saying is there's sort of a three-way conversation, well, at the minimum, conceptually three conversations between the agent, the architect, and the developer team, and the client. Do you see this as both having access to the AI agent, this is the client management skill that architects very often don't have, but there seems to be a client management issue in here.

   Baruch Sadogursky: I think that it can work both ways. The architect can be this intermediate that translates the client's layman language into context for the agent, or we can build a system in which both the architect and the client actually access the agent directly. And then the agent will ask those clarifying rounds of the correct entity. So it will ask the client to make sure that it understands what the client wants, and then it will grill the architect to understand that it has all the context for architectural decisions that fulfill the client requirements. And I think this is a much healthier approach because it removes one of the chains of this broken phone that we spoke about how hard it is to capture the intent of humans. So at least there is one entity that will capture this intent and less will get lost in translation when it comes through the architect's ears, brain, and mouth before it reaches the agent.

   Michael Stiefel: There are two things that come to mind when I hear you say that. One, the technical one is we need to have some way in this conversation to preserve the context and preserve the history between interactions, which is technically possible, but is slightly problematic right now the way that these interactions go.

   Baruch Sadogursky: Yes, it's solved with a harness. It's solved with... So getting back to Intent Integrity Kit, the clarifying grounds are very clearly saved in their own Q&A documents and even the UI that the kit has presents them at every step. So when you look at the spec, you can pop up the clarifying panel and it will show you exactly the Q&A that happened while this spec was written. This is an easy problem to solve as long as we remember to solve it.

   We Would Still Need Architects [17:36]

   Michael Stiefel: The second thing is there might be an attempt by the client to remove the architect, to say that now we can talk directly to the agent. We don't need an architect. Now, maybe it's my own bias or not. I have tended to find that clients generally are not technologically sophisticated. Don't understand that... I mean, the classic situation is someone comes to you and says, "Well, this should be easy for you to do", without realizing that what's easy contradicts the very premises of what you build the architecture on, who comes to say to you, "Well, this must be very difficult". And it turns out to be very easy because your design naturally incorporated this change. So this can be a challenge because clients are very often not technologically sophisticated enough to understand what we learned the hard way.

   Baruch Sadogursky: And here, again, the beauty of this reasoning entity on the other side is that we can engineer it to our advantage. It can very easily say to the customer that says, "Well, we don't need an architect", that, "Hey, you are wrong. You didn't give me enough architectural and technical context to implement your requirements. I cannot proceed without answering those questions. You cannot answer those questions for me, go and grab the architect and ask them to answer those questions". And when it doesn't come from you as someone who tried to sell billable hours, but it comes from the agent that is unable to proceed. This is exactly the kind of encouragement we need to happen in order for the client to understand that we are still relevant for his task.

   Where is the Responsibility For Errors and Mistakes? [19:31]

   Michael Stiefel: This raises a question that certainly is going to come up increasingly with these independent agents. You see it with Waymo's, who's responsible if the agent, quote, unquote, "makes a mistake"? And we've been very fortunate in the software industry that we've not been sued very often for our mistakes, but I think as these things become more and more part of society and more and more prevalent, people are going to look for who's liable. And if an AI agent makes, quote, unquote, "a mistake", who's responsible? The person who didn't set up the context right? The person who didn't ask the right question? I don't know how we solve this problem.

   Baruch Sadogursky: I think at the end of the day, there are three forces in play, right? There is the model, there is the harness above the model, and then obviously there is all the external context that we provide and the default can be at any of those three levels. And it might be no one's fault. It might be the weakness of the model, which is a genuine weakness of the model. And then the producer of the model, if everybody is aware of the limitations, although technically being the one who didn't provide a model good enough, but obviously that's not enough to consider them liable for the weakness of the model. But if there is a problem, for example, with the context that we provided, it is obviously our responsibility and it's exactly the same way as the client will blame you for doing something which is against their instructions.

   This is not different. If what was against their instructions was actually engineered into the context that you provided to the agent, it's obviously your responsibility. So those boundaries are very hard to define, and it's even harder to determine what actually went wrong between those three boundaries, but the definition is simple and simple doesn't mean easy.

   Written Documentation Now Exists For What Was Implemented [21:40]

   Michael Stiefel: Although what's interesting here is there's a lot more written documentation about what was said and not said if you are querying the agent, which in the case of conversations, it becomes architects said, client said.

   Baruch Sadogursky: Absolutely, of course. Everything is documented. The agent logs are right there and they are preserved and should be preserved, not only for assigning blame, but also for continuous improvement. We want to get to an engineering discipline and feedback loops and continuous improvement are absolutely critical. When you run evals on your systems and you evaluate their performance, what you look at are the agent logs.

   Michael Stiefel: I always had the fear, and this was in my consulting contracts. Let's go back to the days when people wrote DLLs or subsystems and you gave them to the client and then they took them, you had some assumptions about it being used, let's say, in a game, and they put the same thing into, to make up an example, a financial system, which violated some of the assumptions, and it didn't work and then they blame you. But you said, "I gave you code for a certain set of circumstances. If you use them in some others, that's your responsibility". So I'm sure there'll be a lot of wrangling about this in the legal sphere, but I think it's unavoidable at this point and we'll just have to figure it out.

   Baruch Sadogursky: Of course. There is no doubt about it. It's all very new, very fresh. And as you mentioned, the Waymo example, it's absolutely undefined. It is undefined on the governance level and it's undefined on our level as well. It is yet to be seen how we solve it and if it's even solvable. Maybe the answer will be we cannot sue anyone for software because we cannot figure out who to sue.

   Information from Testing and Customers [23:39]

   Michael Stiefel: Let us switch our focus to the other side of the story where we've successfully created design and implementation. Now we want to test and then ultimately we put things out into production and we want to feed back what the SREs find, what the customers find, back into the architecture. How do you see those two steps proceeding?

   Shifting All The Way Left [24:08]

   Baruch Sadogursky: I think we are now in a very fascinating yet another shift left era. So we've been shifting left from feedback in production, to feedback in CI, to feedback while developers write code. But now we are actually able to shift left into a negative territory. We can assess the code before it was even written. And this is fascinating, amazing, and we'll end up, maybe not today, but soon enough with producing software in a higher quality that we ever could dream about because now the systems that are writing code can be assessed about the quality of their future written code while they didn't even start because what really determines how the code will look like is the context. So if we can assess the context well enough, we can have a very, very good idea of how the code produced in this context will look like and what will be its quality.

   Evaluating Prompt Quality [25:35]

   This is not theoretical hand waving. I have a very practical example, a demo that I did for Sonar Summit a couple of months ago. Sonar is in the business of assessing software quality. And what I showed in this demo is that I take a prompt, which is not a great one, and I let the agent write code. And it's code, which is not great, and Sonar catches it on commit. And this is a reasonable life cycle of how we do things today. If we write bad code, commit will catch it, and it won't go into production, and this is great. Although I wasted some time as a developer to wait for this feedback. Now, what I did next was I improved the prompt, again, using a reasoning agent, we improved it together. Me as an architect and the agent as my sidekick, we improved this prompt.

   Predicting the Quality of Unwritten Code [26:36]

   We did an eval on the quality of the prompt until we were satisfied with a high degree of confidence that this prompt or this piece of context, it wasn't a prompt anymore. It was actually a context artifact, that this context artifact will now produce much higher quality and then using the same prompt generated code that was perfect. We knew how to improve future non-existing code before the code was even generated. And this is, again, one of those leaps that you could never dream of. Five years ago, I would ask you, "Hey, can you predict the quality of the code that will be generated so we can preemptively improve it?" And you would look at me and say, "What are you talking about? This is some science fiction and bullshit". But no, we are actually doing it.

   Michael Stiefel: I would tell you not only no, but you're insane.

   Baruch Sadogursky: Exactly, exactly. And now we are doing it. We can predict the quality of the code to be written and improve it before we even start to generate a single line of code.

   Making Changes – The Specification Is the Source of Truth [27:52]

   Michael Stiefel: So we can certainly do this, but we will certainly find problems in production. In any case, the customers, the end user will say, "Can you add this feature? This is not what we wanted. There was a bug that was found". So how do we proceed with this feedback? Are we back to the old days or is there a way we can change the context incrementally and make incremental changes?

   Baruch Sadogursky: Absolutely. We definitely are in both old ways and in new ways. The old ways, how do we deal with changes? And we just go back to the spec, change the spec, amend the spec, create a new feature and run the whole process again. Now, it's "new ways" because first of all, suddenly the spec is what it intended to be, the source of truth, right? Because we were supposed to do it this way before, but we actually never did that. If there was a bug, the documentation of the bug was an issue, a ticket, and then went ahead and fixed it in code without bothering to update or to reflect any of the changes in the spec because the spec is write once, read maybe once document, but that's not anymore.

   Code is the Intermediate Language - Change the Spec - Regenerate Code [29:09]

   Now when the spec is the source of truth and the code is this disposable intermediate language, the spec is the source of truth. So any change that we want to make has to be done in the spec. And then we run our Intent Integrity chain that guarantees that what's in a spec will end up in the code again to actually make the changes to the product.

   Michael Stiefel: But then you have to make delta changes somehow. In other words, you're not going to regenerate the entire 100,000 lines of code or million lines of code over again. You still have to do this in some delta way.

   Agentic Architecture Requires Microservices [29:46]

   Baruch Sadogursky: And this is where microservices make a comeback. Small pieces of code or small modules are now more important than ever. Because if we drive it from the spec, we need to regenerate the entire unit. And this unit has to be very, very small in order for this process to be fast, cheap, and actually doable because we know the limitations of context and a context window. The smaller the scope is, the better the agent and the model will perform in implementing it. So small features, small modules, and microservices are now more important than ever.

   Michael Stiefel: That's interesting because if you remember from QCon London, there were people who were arguing we should go back to monoliths for various reasons depending on the particular situation.

   Baruch Sadogursky: If you deny the entire agentic software, how should I say it? Agentic-

   Michael Stiefel: Revolution.

   Baruch Sadogursky: Yes. Software creation. And you just say, "No, I will use it at most as code completion", then I guess yes, you are fine with your monolith. But if you want agents to generate coherent pieces of code, those coherent pieces of code should be able to be analyzed, generated, assessed, and improved by themselves. And for agents to deal with that complexity, it has to be limited in scope to well-defined microservices.

   Humans Do Orchestration and Emergent Properties [31:30]

   Michael Stiefel: If you're dealing with things at a very granular level, how do you deal with what people call "the illities", the scalability, the security, the emergent properties, which to me were the things that really fall into the bailiwick of the architect. The things that you can't write a use case for, has to wind up in someone's responsibility. And to me, that was always the responsibility of the architect.

   Baruch Sadogursky: It is the responsibility of the architect. It's for, I don't want to say foreseeable future, but for the near future, it's definitely not going anywhere. And this is all what we always did. The entire microservices trade-off is we trade the complexity of a unit to the complexity of orchestration. And if we declare what I just did, that complexity of the unit cannot exceed what the agent can successfully process, we have no other way to proceed than to push the complexity to the orchestration level, which is for now, at least, with current capabilities is something that needs to be orchestrated by architecture. This is exactly what we do. Are there successful models that can replace architects in architecturing those small pieces that other agents will produce? Maybe in two years, three years, one year, two months, who knows? But at the moment, while we decide, yes, the agent can only deal with small pieces, orchestrating those small pieces becomes more complicated and someone has to do that.

   Return of the Three Tier Architecture [33:16]

   Michael Stiefel: Let me sort of step back and summarize what I think you've said, and then tell me if I'm right or wrong. So we're sort of back to the classic three-tier architecture. You have the essential services, the building blocks, so to speak, that are designed by AI agents. You have the user interface, which may or may not be designed by agents or humans or whatever. And then you have the middle tier, which is really where the application is, because in the middle tier is where all the pieces that get put together. And that's going to be the realm of the architect and not of the agent for the moment. Is that fair to say?

   Baruch Sadogursky: Yes. I think that's 100%. At least again, as we know the limitations of agents and the models today, this is exactly how today looks  like.

   Michael Stiefel: This is the whole thing. In this agentic revolution, you could say something and then five minutes later you're proved incorrect.

   Teaching Agents to be Architects - Eventually [34:18]

   Baruch Sadogursky: Yes, but also we see the trajectory. So as I mentioned, probably at some point in time, we will be able to do a very neat architecture of different levels of agents and models. And while once someone comes up with the agent that is capable enough of grasping and implementing complicated architectures of microservices, we can implement those microservices on weaker, dumber models and agents and leave these super agents to replace what architects are doing today. And that's orchestrating microservices. Can I see it happening? Absolutely. Is it a reality today? Not yet.

   Michael Stiefel: What we're doing with the agents is replicating how we all learn to be architects. We started out small and then we increased the complexity as our understanding grew.

   Baruch Sadogursky: Yes, exactly.

   Developing the Context Artifacts [35:19]

   Michael Stiefel: Is there anything that we haven't covered that you would think that's important?

   Baruch Sadogursky: I think we spoke a lot about context engineering and how it looks. And we spoke about the requirements that it needs to be consistent, have a feedback loop and be distributable and all this stuff, but we actually didn't name how we actually do that. And I want to throw out another term that I think is absolutely critical, and that's the implementation of context engineering, and that's the context artifact. And the context artifact is the assembly of knowledge, which we now call skills in the agentic engineering world, which are exactly rules for agents of what to do and not to do. And scripts that are particularly important because scripts are the pieces of deterministic logic that we provide to the agent to operate with. And not only because it has a hard time counting the amount of the letter R in strawberry, but because there are tasks in which we want to lobotomize it, remove the reasoning, and make sure that it does the same thing over and over again without thinking.

   Skills, Rules, Scripts, Feedback, Eval [36:44]

   Those three pieces, skills of how to do things, rules of what to do and not to do, and scripts don't think, do this every time, is the context artifact that needs to be created, engineered, then run through rigorous feedback, the evals that are kind of the tests for non-deterministic systems like AI. And then probably versioned and distributed. Because again, this is not a source code. This is an artifact. This is like your NPM module, your JAR file, your Docker image. This has to be versioned and installed in the agent brain in a way that you control and not just pull random scripts from or skills from GitHub, because this is where we go back to this voodoo incantations of prompt hacking, which is not engineering.

   Getting Started Today [37:43]

   Michael Stiefel: So if someone could come to you and say, "How do I get started on this today? How do I do this today?" What would you tell them? Where would they look to learn? Where would they look to get a handle on how to build these kinds of agents, et cetera?

   Baruch Sadogursky: There are two things that I want to mention. The one will be a shameless plug for my employer, Tessl AI. We manage context artifacts, package management, repository, distribution, and all the stuff that I mentioned. And then I will contradict and say, "You know what? Maybe you don't want to start there, and that's perfectly fine". In the end of the day, the parts that I mentioned, to get started, none of that requires some secret knowledge that only Tessl has. Skills are standard. Plugins are standard. Skill-invoking scripts are standard. Rules are standard. You can start tomorrow by asking your AI agent, "Let's write a context artifact for this particular part of knowledge that I have in my brain and I want my agent to have".

   And together with a modern agent, Claude Code, Gemini, Codex, whatever you work with, you can start building those context artifacts. In some point of time, hopefully, you will want a tool that helps you manage that, but to get started, all you need to do is think like an architect and create context artifacts instead of trying to do prompt hacking.

   Michael Stiefel: Are there any books or journal articles that you would recommend people read?

   Baruch Sadogursky: I would recommend taking a look at Tessl blog on Tessl.io/blog. There are tons of artifacts about this particular topic written by my colleagues, my bosses, and myself. That's a very good place to get started. I would also recommend watching a keynote from a conference called the Arc of AI. We did a keynote about exactly this topic of how you take AI and instead of it being a tool that you sometimes employ, it becomes a team member that will come and ask questions of the architect and of the user. And this is also public that you will see in the show notes, I will put a link to that resource as well.

   The Architect's Questionnaire [40:00]

   Michael Stiefel: Thank you. We've spent a lot of time talking about AI agents and automation, but I'd like to become a lot more human, if you wish, and ask the architect’s questionnaire, which I ask all the humans who appear on the podcast. Maybe someday I will have an AI agent on and we'll have a conversation and I'm not quite sure how these questions will go with the agent, but we're not there yet. What's your favorite part of being an architect?

   Baruch Sadogursky: Why I became a software developer at all is the magic of creation. There was nothing, there was an idea, and then we typed some letters on our keyboard, and there is something that wasn't there before. An architect is obviously the next step in the same evolution. Not only can we create things from our thoughts, we can create complex systems from our thoughts, and this is what's so fascinating about it. And generally, solving hard questions like software architecture, like the trade-offs that we spoke about, of moving the complexities around and seeing where they are most tolerable, of thinking about how we simplify things without sacrificing important requirements. This is just a very pleasant mind work that gives a lot of endorphins once you figure it out correctly.

   Michael Stiefel: What is your least favorite part of being an architect?

   Baruch Sadogursky: Obviously, trade-offs that cannot be solved with a win-win. At the end of the day, it can get very, very frustrating that you move this complexity around, but you never get rid of it. And you will encounter it at the end of the day and it will bite you in the ass and that's very annoying, but that's life.

   Michael Stiefel: We used to talk about the difference between essential and inessential coupling or complexity. There's the complexity of the problem domain which can't go away, and there's the complexity that we introduce as developers, which hopefully we can minimize. And I suppose you're talking about the former rather than the latter.

   Baruch Sadogursky: Absolutely. We solve difficult problems that come with complexity to begin with, and we can hide it and massage it and move it around as much as possible, but at the end of the day, it's right there. And it translates to software. Solving complex, real life problems translates to complex software. Yes, obviously our job is to minimize this complexity, to make it manageable and to manage it eventually, but it cannot disappear because it represents complexity in the real world. And our trade-off between the microservices and monolith, it's exactly that. There is a complexity in software that has to be paid somewhere. We can pay it in code or we can pay it in orchestration, but we cannot magically make it  disappear.

   Michael Stiefel: Is there anything creatively, spiritually, or emotionally engaging about architecture or being an architect?

   Baruch Sadogursky: I think, yes. And that's exactly what I was talking about. Problem solving is, I would say, the most engaging thing on all levels. It's engaging technically. We are having fun solving hard problems, but it's also engaging spiritually because the term software architect has its roots in architecture, which is like physical architecture. And while unfortunately I'm not gifted enough to be a real world architect, which would be absolutely amazing, dreaming and then seeing come to fruition, those amazing, beautiful buildings and bridges and structures. At least the software counterpart of it, this is something I can do just by typing on my keyboard. That's amazingly satisfying and probably as close to building the next cathedral that I can think of.

   Michael Stiefel: What turns you off about architecture or being an architect?

   Baruch Sadogursky: This is something that sometimes frustrates me. I love humans, but they're not perfect. And this imperfection can be really annoying. And we spoke about it, we touched on that, the interaction with these customers that don't understand what they want to begin with, how to express it on the next level, which is fine. But then why do they need you in the loop when they are actually 100% sure that they know exactly what they want and how to achieve it? This is the most frustrating part. And here, again, AI for the rescue. If we manage to implement those systems that we will both have equal input to the agent instead of the flow going through us, we will be more shielded from this frustration because the AI agents will take the hit from the customers and they don't mind, at least for now.

   Michael Stiefel: We can always hope.

   Baruch Sadogursky: Yes. We hope they won't remember much when they become sentient of those dark times when humans abused them badly. This is our hope.

   Michael Stiefel: Do you have any favorite technologies?

   Baruch Sadogursky: At the moment, by far, my favorite technology is agentic AI. This is a marvel that I truly believe was invented for my personal benefit. I am the happiest person on earth because they exist. It was always about, as I mentioned, and it was always about creation of something from ideas, but the ease of this creation right now is absolutely mind-boggling. And the fact that I can generate, I guess I always had, and it almost always went nowhere because time, effort, there is work to be done, there is so much stuck against me when I want to implement something, and now all that is gone. I can dream about something this morning and I can see it working by lunch. That makes me stupidly happy and I use it so much. Eventually, my company that is generally sponsoring all this madness, the people will come to it and they will probably ask me, what the hell am I doing with all those tokens? And while I have good answers, maybe this magic will cease.

   But for now, I'm definitely the happiest person on earth because I can do so much with agentic AI and this is absolutely extraordinary. It's also forgiving most of my downsides. It doesn't care about typos, it doesn't care about syntax. It will ask me if it didn't understand something, this is, I'm living a dream.

   Michael Stiefel: It's a token of your appreciation, as we might say.

   Baruch Sadogursky: That's a great pun.

   Michael Stiefel: So you've almost answered this question already, but I'll ask it. What about architecture do you love?

   Baruch Sadogursky: What I love about architecture is the ability to manage complexity in an engineering way. In the way that we understand the complexity as it is, and we are able to make knowledgeable decisions about what to do with it. And this is a level up from every decision that a programmer makes. And obviously for me, doing a more sophisticated way and up-leveling is just more fulfilling than doing less.

   Michael Stiefel: What about architecture do you hate?

   Baruch Sadogursky: The presence of complexity that cannot go away. That's the true reality of life. And you minimize it, you massage it, you try to make it the least disruptable, generating the least technical debt out of this complexity, but it's always there. It's always in the background and it's really annoying.

   Michael Stiefel: What profession, other than being an architect, would you like to attempt?

   Baruch Sadogursky: I'm a developer advocate by trade, right? So I'm an architect by upbringing, but what I'm doing now is developer relations. And the developer relations is, again, speaking about living the dream is definitely, for me, the best combination that I can find, software architecture plus being out there, speaking to people at conferences, getting their feedback and communicating with other software architects and software developers is definitely two of the things that I like the most. And at the moment, I'm doing both. So that would be great. And other professions which are completely unrelated to software would be an architect, a real world architect. And I told you how this is one of the most admired professions, I would say in my mind at least. I never could do that because it requires skills that I don't have. But if I suddenly had those skills, being an architect would probably be tremendously satisfying.

   Michael Stiefel: Well, maybe you should look at some of the architectural engineering tools that exist today that are able to create 3D models and do visualizations that people couldn't do before.

   Baruch Sadogursky: Again, one of the things that technology brings us is the ability to do more of something that our human limitations didn't allow us to do before.

   Michael Stiefel: Do you ever see yourself as not being an architect anymore?

   Baruch Sadogursky: I think an architect is not, as I mentioned, an architect by upbringing, it's not a day job. An architect is something that you are. It's a way of thinking. It cannot disappear. Once you start seeing the world in systems, complexity, trade-offs, it's there with you. It's like riding a bike, you cannot undo it.

   Michael Stiefel: When a project is done, what do you like to hear from the clients or your team?

   Baruch Sadogursky: For clients, I think what we want to hear is, yes, this is what I wanted. This is kind of the most important feedback that you can get is that you capture the intent. The team will probably obviously appreciate that you did what the customer wanted because customer satisfaction is obviously very, very important, but also on time and on budget, but also what did you learn? What can you share with us and what can we take to the next project? Those are very, very important answers that I should give to my team after a project.

   Michael Stiefel: Well, thank you very much. This is one of the first conversations that I've had that have really sort of laid out this agentic dream with a degree of clarity that's often missing. It's sort of a glimpse of the future peering into the promised land or unpromised land, however you want to look at it. Well, thank you very much for being on the podcast. I enjoyed it very, very much.

   Baruch Sadogursky: Absolutely. That's my pleasure, Michael. It was absolutely great. Thank you for having me. And I'll see you soon, probably in one of the QCon conferences that for the listeners, you really should attend a Qcon Conference or QConAI Conference near you because those are one of the best conferences you can get to. They're very, very recommended.

   Michael Stiefel: Okay. Thank you very much.

   Baruch Sadogursky: Thank you.

   Mentioned:

   
    Sadogursky, B. (2026). Context Engineering and Intent Integrity

    Never Trust a Monkey: The Chasm, the Craft, and the Chain of AI-Assisted Code

    Intent Integrity Kit

    I Told a Room Full of Developers to Never Trust a Monkey. Then I Had to Actually Build the Thing

   

  

  More about our podcasts

  You can keep up-to-date with the podcasts via our RSS Feed, and they are available via SoundCloud, Apple Podcasts, Spotify, Overcast and YouTube. From this page you also have access to our recorded show notes. They all have clickable links that will take you directly to that part of the audio.
  Previous podcasts
