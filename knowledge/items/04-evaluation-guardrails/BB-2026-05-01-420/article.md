# Can AI Write Your Code?

- BestBlogs URL: https://www.bestblogs.dev/article/ece06f7a
- Original publisher URL: https://towardsdatascience.com/can-ai-write-your-code/
- Source: BestBlogs / Towards Data Science
- Publish time: 2026-05-26 01:15:35
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 18337

---

What if the real question is no longer whether AI can write code, but whether we can trust the code it writes?

  Over the past few years, ChatGPT and other large language models have become increasingly common in the daily workflow of students, analysts, researchers, and data scientists. Many of us have already used AI tools to generate a Python function, debug an error message, automate a repetitive task, or quickly translate code from one language to another.

  But there is a major difference between asking ChatGPT to write a small helper function and asking it to implement a complex econometric method.

  Can ChatGPT correctly code a Difference-in-Differences model? Can it implement Inverse Probability Treatment Weighting? Can it reproduce a Regression Discontinuity analysis? Can it do this not only in Python, but also in R and Stata?

  That is why the article “Can AI write your code? A case study of ChatGPT’s statistical coding capabilities for quantitative research” by Winberg et al. immediately caught my attention. The paper was published online on January 22, 2026, in Health Economics Review. The authors evaluate ChatGPT-4.0 Pro’s ability to generate code for causal inference tasks in Python, R, and Stata, using benchmark solutions from Causal Inference: The Mixtape by Scott Cunningham.

  Most articles I had previously read on this topic focused on relatively simple programming tasks: small automations, descriptive statistics, data cleaning, basic data analysis, or code generation in languages such as Python, R, and SAS. This study goes further. It asks whether ChatGPT can support quantitative research in more demanding settings, where the code is not just technical but also methodological.

  The authors focus on three widely used causal inference methods:

  
   Difference-in-Differences, also called Diff-in-Diff;

   Inverse Probability Treatment Weighting, or IPTW;

   Regression Discontinuity, or RD.

  

  In this article, I will walk through the study in a structured way. First, we will present what makes this study different for quantitative researchers. Second, we will review the methodology used by the authors. Third, we will look at how ChatGPT’s performance was evaluated. Finally, we will discuss how the Rise of LLMs Has Changed in My Own Way of Working

  What Makes This Study Different?

  Many previous studies have evaluated ChatGPT’s coding ability using subjective assessment. In other words, researchers looked at the generated code and judged whether it seemed correct.

  That approach is useful, but it has a limitation: it depends heavily on the evaluator’s judgment.

  Winberg et al. take a more structured approach. They compare ChatGPT-generated code against standardized reference code and benchmark outputs from Causal Inference: The Mixtape. This allows them to evaluate the code not only based on appearance, but also based on whether it reproduces expected results.

  Another important contribution is that the study includes Stata.

  This matters because many empirical researchers, especially in economics, public policy, and health economics, still use Stata extensively. However, discussions about AI coding assistants often focus mainly on Python and R. By including Stata, the authors evaluate ChatGPT in a language that is highly relevant for applied econometric research but less frequently analyzed in AI coding studies.

  The Methodology Used in the Study

  The authors evaluate ChatGPT-4.0 Pro, the paid version of ChatGPT available at the time of the study. Their goal is to measure how well it performs when asked to code causal inference analyses in Python, R, and Stata.

  They use publicly available data and problem sets from Causal Inference: The Mixtape. This textbook is widely known in applied econometrics and provides examples with code in R, Stata, and Python. According to the study, the reference environments were R 3.6.0, Stata 18, and Python 3.13.

  The authors focus on three causal inference methods:

  
   Difference-in-Differences;

   Inverse Probability Treatment Weighting;

   Regression Discontinuity.

  

  These methods were chosen because they are commonly used in empirical research and require more than simple syntax generation. They require proper data preparation, model specification, and interpretation of outputs.

  The study follows a three-step process.

  Prompting ChatGPT With Econometric Problem Sets

  The first step is to give ChatGPT problem sets and ask it to generate code for the relevant econometric analyses.

  For example, one of the problem sets focuses on Difference-in-Differences. The context is the legalization of abortion in five U.S. states before the nationwide legalization following Roe v. Wade in 1973. The task is to estimate whether early abortion legalization affected gonorrhea incidence among adolescent females aged 15–19.

  Instead of using only a simple post-treatment indicator, the prompt asks ChatGPT to use year-by-treatment interactions to capture dynamic treatment effects over time.

  This type of prompt is more complex than asking for a basic regression. It requires the model to understand the policy context, identify the treatment indicator, structure the interaction terms, and generate appropriate code.

  The authors define similar problem sets for IPTW and RD.

  Asking for Complete Coding Workflows

  In the second step, the authors provide more comprehensive prompts. These prompts ask ChatGPT to reproduce fuller coding tasks from The Mixtape, including data management, econometric analysis, and figure generation.

  This is important because real research workflows are rarely limited to one model command. A researcher usually has to import data, clean variables, create indicators, estimate models, generate tables, produce plots, and compare results.

  By testing complete workflows, the authors evaluate whether ChatGPT can handle the practical complexity of applied quantitative work.

  Running the Code and Comparing Outputs

  In the third step, the generated code is executed in the corresponding programming environment: Python, R, or Stata.

  The authors then compare the outputs produced by ChatGPT-generated code with the benchmark outputs from The Mixtape. 

  How the Prompts Were Generated

  One of the most interesting aspects of the study is the way the prompts were designed.

  The authors recruited four researchers with advanced expertise in econometric methods. Two held PhDs, and two were PhD candidates. Three researchers were assigned to work with one language each: Python, R, or Stata. The fourth researcher replicated the full process across all three languages to validate the results and assess consistency.

  This design is useful because it reflects how researchers might use ChatGPT in practice. Each researcher interacts with the model, generates code, runs it, observes errors, and gives feedback.

  However, this also creates a risk. If each researcher writes prompts independently, the results may reflect differences in prompting style rather than differences in ChatGPT’s coding ability.

  To reduce this bias, the authors standardized the prompts. They collaboratively developed prompts that were clear, structured, and general enough to apply across tasks. The goal was to provide ChatGPT with enough information to solve the problem without overfitting the prompt to one specific task.

  The quality of the output depends heavily on the quality of the prompt. If the prompt is vague, the model may produce generic or incorrect code. If the prompt is too specific, it may perform well on one task but fail to generalize.

  A good prompt should provide context, specify the expected method, define the relevant variables, describe the desired output, and clarify any assumptions.

  The Five Performance Indicators

  The authors evaluate ChatGPT’s performance using five main outcomes: accuracy, efficiency, error output, editing, and consistency.

  Accuracy is measured by comparing the results generated by the ChatGPT-written code with the benchmark outputs from The Mixtape.

  The evaluation is binary: if the result matches the benchmark, it is considered accurate. If it does not, it is considered inaccurate.

  Efficiency is measured by comparing the number of commands used in the ChatGPT-generated code with the number of commands in the standard reference code.

  This is not a perfect measure of efficiency, but it gives a useful approximation. 

  The authors document whether the ChatGPT-generated code produces execution errors.

  This is one of the most practical indicators. When code fails to run, the user must debug it. If the user does not understand the method or the programming language, this can become a major problem.

  Editing refers to cases where the code does not produce an execution error but still requires clarification, additional context, or manual adjustment to obtain the correct output.

  This is particularly important because not all errors are visible. A code block can run without crashing but still produce an incorrect model, a wrong variable transformation, or a misleading figure.

  Consistency is assessed through replication. A fourth researcher repeats the tasks using the same prompts across Python, R, and Stata, with a new ChatGPT account and no prior conversation history.

  The goal is to determine whether ChatGPT produces similar logic and structure when different users submit the same prompts.

  This matters because reproducibility is central to research. If the same prompt produces very different code across sessions, researchers need to document and validate outputs carefully.

  What Did the Study Find?

  The overall conclusion is balanced. Here is a table that summarizes the results.

  
   
  
  Based on the study, ChatGPT performed better in Python and R than in Stata. The authors state that ChatGPT generated accurate code and results in R and Python for most tasks, while Stata was less reliable.

  This result is not entirely surprising.

  Python and R are widely used in data science, statistics, and machine learning. They also have large online communities, extensive documentation, and many publicly available code examples. Since large language models learn from large-scale text and code data, it is reasonable to expect them to perform better in languages with more abundant public examples.

  That said, this interpretation should be treated carefully. The study is not a large-scale benchmark across thousands of tasks. It is a case study based on selected econometric problem sets. Therefore, we should not conclude that ChatGPT is universally better at Python or R than Stata in all contexts.

  A more cautious conclusion is this:

  For the causal inference tasks tested in this study, ChatGPT appeared more reliable in Python and R than in Stata.

  What the Rise of LLMs Has Changed in My Own Way of Working

  What makes this study particularly interesting to me is that it does not address only a theoretical question. It directly connects with what I observe in my own work, both at home and in a professional setting. We used ChatGPT Pro 4.0 in the past, and today we use ChatGPT Pro 5.5. In this section, I want to explain how the adoption of these models has changed the way I work.

  In the past, when I had to conduct a quantitative study or develop a statistical methodology, a large part of the work was spent on literature review. I had to identify the right scientific papers, understand the methods used, compare different approaches, and then decide how to apply them to our own data.

  Today, with ChatGPT, this exploratory phase is much faster. It does not replace the critical reading of scientific papers, but it helps structure the initial research, identify key concepts more quickly, and formulate methodological questions more clearly.

  The change has been even more visible in the workplace, especially in the way we use programming languages.

  Previously, we mainly used SAS for data extraction, preparation, and processing. SAS remains a very efficient tool for handling large volumes of data in a professional environment. However, for statistical modeling, we often relied on R, which was more convenient for estimation, visualization, and methodological experimentation.

  With the rise of LLMs, we gradually decided to move a significant part of our work to Python. This decision was not only driven by the fact that Python is simple and widely used. It also came from a very practical observation: in our experience, tools like ChatGPT generally provide better answers in Python, with fewer errors and more reusable examples.

  We did not conduct a scientific study as structured as the one by Winberg et al., but we reached this conclusion through the feedback of the modelers in our team and as part of a long-term strategic choice. In practice, AI has influenced not only the way we write code but also the infrastructure we use. We moved from an environment centered on SAS Studio and RStudio to a workflow more oriented toward VS Code, because it integrates more easily with tools such as ChatGPT, Claude, and GitHub Copilot.

  This shift may look technical, but it is actually quite deep. AI not only improves productivity. It also influences the languages we choose, the tools we use, and the way we organize our workflows.

  Another concrete example is the collection of external data. In our work, we sometimes need publicly available datasets: INSEE data, climate data, IPCC data, NGFS scenarios for climate stress testing, or other datasets used in ESG risk modeling.

  In the past, this type of task could take several days, sometimes even several weeks. We had to find the right source, understand the structure of the files, download the data, clean it, reformat it, and make it usable for our models. Today, with LLMs, this process can be significantly accelerated.

  Recently, for example, I wanted to retrieve NAF codes from the INSEE website, together with their labels, in a format that could be used directly. In the past, this task would probably have taken me several hours. With a few well-structured prompts, I quickly obtained a script that retrieved the data, cleaned the codes, removed the dots, and produced an Excel file ready to use. This is not only a time gain. It also reduces the friction between an idea and its execution.

  In my view, this is one of the most important contributions of LLMs for statisticians and quantitative analysts. They are very useful for data processing, statistical modeling, mathematical programming, reporting, and formatting results.

  They have also become valuable for producing deliverables: structuring documents, improving explanations, formatting tables, describing figures, and interpreting results. Earlier versions of ChatGPT still made many mistakes in these tasks, especially in technical reasoning and references. Recent models are much better, although they still require careful validation.

   In my work, I see them more as very fast research assistants than as autonomous experts. They can do in a few hours what we might previously have assigned to a research assistant for several days: explore a method, propose code, generate a first version of a chart, rewrite an interpretation, or automate part of a report.

  But this speed comes with one condition: human supervision and validation remain essential.

  The risk of hallucination is not theoretical. A recent example made this very clear: according to the Financial Times, EY Canada withdrew a study used to promote its cybersecurity services after it was found to contain fabricated data, misattributed citations, and even a reference to a McKinsey report that did not exist.

  This is exactly why I find the study by Winberg et al. interesting. It does not simply ask whether ChatGPT can write code. It points to a more important question: under what conditions can we trust AI-generated code?

  For me, the answer is clear. We can use LLMs to work faster, but not to remove the responsibility of the researcher. The researcher still needs to check the assumptions, validate the data, test the code, compare the results with benchmarks, and make sure the interpretation is correct.

  In other words, AI is deeply changing the way we work, but it does not remove the need for expertise. In fact, it makes expertise even more important. The more powerful the tool becomes, the more necessary it is to know when to trust it and when not to.

  Finally, the adoption of AI tools will continue to transform the way we work. Some processes will become more efficient, others will disappear, and more sophisticated workflows will emerge. To remain competitive, we need to keep learning, keep working, and be ready to integrate these tools into our professional lives.

  At the same time, AI will also change the way knowledge is produced and shared. Because these tools improve productivity, an article that once required a month of work can now sometimes be completed in a week. This is a good thing in many ways: it lowers the barrier to writing, helps more people share ideas, and accelerates the circulation of knowledge.

  But it also creates a new challenge. If everyone can produce more content faster, the internet will become even more crowded. The reach of each article may not be the same as before. Some writers may feel discouraged, especially if their work receives less visibility despite the effort behind it.

  In my view, this will create a new form of inequality between those who know how to use AI effectively and those who do not, but also between those who write only to produce content and those who write because they truly care about the subject.

  In the long run, I believe the people who remain will be those who are genuinely passionate, those who want to learn, think deeply, and share knowledge with others. AI may make writing faster, but it will not replace curiosity, discipline, and the desire to contribute something meaningful.

  References

  Winberg, D., Tsai, E., Tang, T., Xuan, D., Marchi, N., & Shi, L. (2026). Can AI write your code? A case study of chatgpt’s statistical coding capabilities for quantitative research. Health Economics Review.
