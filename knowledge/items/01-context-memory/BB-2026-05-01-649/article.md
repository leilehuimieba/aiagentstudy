# Water Cooler Small Talk， Ep. 11: Overfitting in RAG evaluation

- BestBlogs URL: https://www.bestblogs.dev/article/2d145514
- Original publisher URL: https://towardsdatascience.com/water-cooler-small-talk-ep-11-overfitting-in-rag-evaluation/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-06-26 23:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 11666

---

Water Cooler Small Talk is a special kind of small talk, typically observed in office spaces around a water cooler. There, employees frequently share all kinds of corporate gossip, myths, legends, inaccurate scientific opinions, indiscreet personal anecdotes, or outright lies. Anything goes. In my Water Cooler Small Talk posts, I discuss strange and usually scientifically invalid opinions that I, my friends, or some acquaintance of mine have overheard in their office that have literally left us speechless.

  So, here’s the water cooler opinion of today’s post:

  
   We’ve built a RAG app that is playing out really well. We are now in the evaluation stage, and it’s going great because through all the testing we keep identifying issues and fixing them. We’re already at a 97% score.

  

  Now, I want you to pause for a second and think about what might be wrong with this statement. 🤔 Because on the surface, it sounds perfectly reasonable. Finding issues and fixing them sounds like exactly what a good evaluation process should do, doesn’t it? Responsible, even. So what is really happening?

  The problem here is subtle but fundamental. If you are using your evaluation process to identify issues and then fixing those issues, and then re-evaluating on the same set of tests, you are unfortunately not really evaluating anymore. The evaluation set has one key property that makes it so useful: the model has never seen it before. Each time you fine-tune based on its results and then re-evaluate on the same set, you strip away a little more of that property. In other words, the evaluation set has quietly become part of the development process and is now more of a training set.

  But doing this properly is easier said than done. In practice, running the evaluation process properly may be genuinely exhausting. In particular, when talking about running evaluations for RAG apps, meaning that the evaluation set is a set of questions and answer pairs, rather than a historical dataset, doing it the right way may be very tiring and time-consuming. Nonetheless, failing to run the evaluations properly results in a very familiar ML issue: overfitting.

  What about overfitting?

  Let’s take a step back and do a little detour to ML basics.

  
   
  
  In machine learning, a model is built using data that is typically split into a training set, a validation set, and a test set. More specifically, the model is first fit on the training set, which is the data used to indicate what kind of model we need to use and accordingly adjust the model’s parameters. In its simplest form, the training set consists of x and y pairs of data, and our goal is to come up with a y = f(x) model that optimally fits the available x and y data.

  Once that is done, the trained model is used to predict outcomes on the validation set. In particular, for each x in the validation set, we generate a predicted y = f(x) based on the selected model, then check how it compares with the actual y of the validation set, and then adjust our model accordingly.

  At the very end, and after having decided on which model we want to ultimately proceed based on the validation step, we also run it on the test set. The goal of the test set is to see how well the final model generalises to data it has never seen before by calculating its scores, and this is why the test set should only be used once.

  
  We do all this because our goal isn’t to fit the training set, but rather what the training set represents. In this way, we can create models that learn the underlying patterns well enough to make accurate predictions on new, unseen data (the test set).

  Unfortunately, sometimes we fail to do so, and instead of creating models that fit the general case, we create models that just fit a narrow training set without generalising. This is what we call overfitting. As a result, the model performs exceptionally well on the training set, achieving impressive scores, but poorly on anything new.

  
   
  
  The trick here is that the test set is meaningful only if the model has genuinely never seen it before. The moment you use it to make a decision about the model, even an apparently small one, you have compromised it and essentially merged it with the training set.

  But after this little detour to ML basics, let’s get back to our original water cooler opinion.

  This is where things get particularly relevant for those of us building and evaluating AI applications.

  In my series on evaluating RAG pipelines, we talked a lot about retrieval metrics: Precision@k, Recall@k, MRR, NDCG@k, and so on. Nevertheless, all those fancy metrics are only ever as useful as the evaluation set you apply them to. It turns out that the line between evaluation and test sets in RAG can blur surprisingly easily. I would attribute part of this to the fact that, unlike a simple regression model, AI models and RAG pipelines are far from intuitive to us. We have little real intuition for how the model is actually fitting to the data, and as a result, we may get carried away and tune the system based on the test set without even realizing we did so.

  The team in our water cooler story is doing exactly this. They identify issues during evaluation, fix them, and re-evaluate on the same question-answer pairs. Naturally, in every iteration, the evaluation scores improve because essentially they are now fitting the AI app on the test set.

  In particular, here are the most common ways this can happen in RAG:

  
   Tuning prompts on the evaluation set: This is probably the most common pattern, and it is exactly what happened in our water cooler story. You run an evaluation, notice that certain question types consistently fail, and adjust your system prompt or retrieval logic to fix them. Then you re-evaluate on the very same set. Of course, the scores improve; you may even manage to get an impressive 100% score.

   Cherry-picking questions the system already handles well: A more subtle version of the same problem. When building an evaluation set, it is tempting to include examples you already know the system performs well on, especially ones you have informally tested along the way. Over time, the evaluation set drifts toward the system’s strengths and away from its blind spots. The metrics look great, but in reality, no one knows what the actual performance is.

   Building your test questions from the same documents you indexed: If the questions in your evaluation set are written by looking closely at the documents already in your knowledge base, there is a good chance they are implicitly shaped by what you already know is retrievable. In other words, the questions were never truly independent of the data, but again, this is especially hard to realise since we talk about questions and answers in natural language rather than just x and y numbers.

  

  The simple but difficult fix for all of those cases is the same as the classical machine learning solution: keep a genuinely held-out test set that you touch as rarely as possible, build your questions independently of the system’s known behavior, and treat suspiciously good metrics with skepticism. A RAG system that performs beautifully on a small, carefully curated, frequently reused evaluation set is a lot like the student who memorized the past exam papers but is completely unprepared for the first real question that does not look exactly like the ones they have already seen.

  
  If you want to sanity-check your own RAG evaluation setup, here’s a short list of questions worth thinking about and asking yourself honestly:

  
   When I built my evaluation set, did I write the questions independently of the documents in my knowledge base, or did I look at the documents first and write questions I already knew were answerable?

   Have I ever just dropped or replaced a question from my evaluation set because the app kept failing it?

   Do I know roughly how my system performs on questions it has never been tested on before, or only on the same fixed set I keep reusing?

   Is there a part of my evaluation set that has been sitting untouched and unseen by me for a while?

  

  If you answered no to that last one, you may already be the team from today’s water cooler story. 😉

  Overfitting in Real Life: Goodhart’s Law

  Goodhart’s Law, coined by economist Charles Goodhart in 1975, is something like a proverb going as follows:

  
   When a measure becomes a target, it ceases to be a good measure.

  

  This idea originally came from monetary policy, but generalises very well far beyond economics, and it shows up almost everywhere a number is used to judge performance, like KPIs, budgets, and all kinds of numbers. Imagine a car salesman being rewarded for the number of cars they sell each month, and then starting to sell more cars, even at a loss; hospitals trying to reduce the length of stay for patients, then ending up discharging patients too early; citation counts on scientific publications getting gamed, and so on.

  All these examples work with exactly the same underlying mechanism: a quantitative measure is introduced to keep track of something important. For a while, the measure and the real thing move together, and it feels like we can now trust the evolution of the measure for keeping track of the evolution of the real thing. Then people (or systems) start optimising directly for the measure instead of the underlying important thing, and the two quietly come apart. Then the measure starts to improve without the underlying important thing it was meant to represent improving in the same way.

  In AI specifically, this failure mode is called reward hacking, which occurs when an AI system optimises a poorly specified reward without actually reaching the intended outcome. Similarly, in classical ML, overfitting is what happens to a model when the training signal stops representing the real underlying pattern. Goodhart’s Law is what happens to us, the humans designing the system, when our evaluation signal stops representing what we actually care about.

  On my mind

  What I find most interesting about overfitting, particularly in RAG applications, is that it is not really a technical problem. It is primarily a problem of understanding and sticking to the process. It is tempting to jeopardise that process and optimise directly for the scores, especially with RAG datasets that do not look quite like the datasets we are used to in classical ML.

  Nevertheless, this pattern shows up far beyond machine learning and AI. In real life and in machine learning, the antidote is the same: staying consistent and never losing sight of the actual thing you are trying to achieve. In ML and AI, that thing is for the model to genuinely work and produce meaningful results once it is in production and facing real-world data, not just to achieve high scores during evaluation.

  The team in our water cooler story is not doing anything malicious. On the contrary, what they are doing feels like being responsible and fine-tuning the app based on evaluation results. And that is exactly what makes overfitting so dangerous. It does not look like a mistake while it is happening. It only looks like one in hindsight, once the system meets the real world and the scores stop holding up.

  ✨ Thank you for reading! ✨

  
  If you made it this far, you might find pialgorithms useful — a platform we’ve been building that helps teams securely manage organizational knowledge in one place.

  
  Loved this post? Join me on 💌Substack and 💼LinkedIn

  
  All images by the author, except mentioned otherwise
