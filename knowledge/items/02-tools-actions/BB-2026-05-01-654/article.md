# Introducing the Recommended Agent in AI Chat with Codex as the current choice

- BestBlogs URL: https://www.bestblogs.dev/article/1b11f03e
- Original publisher URL: https://blog.jetbrains.com/ai/2026/06/codex-is-now-the-recommended-agent-in-jetbrains-ai/
- Source: BestBlogs / The JetBrains Blog
- Publish time: 2026-06-25 22:57:31
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 12792

---

JetBrains AI supports multiple coding agents, including Junie, Codex, Claude Agent, and any ACP-compatible agent you bring yourself. Previously, AI users in JetBrains IDEs started in Chat mode and had to choose an agent themselves.

  As models became more advanced, agents became more capable and their adoption grew. We recognize that agents help users achieve more, so we recommend to use an agent from the get-go.

  To make that experience simpler, we’ve selected a specific agent to be the default. This post explains how we made the choice.

  You can still switch to any other agent at any time.

  
   “JetBrains evaluated coding agents on the things that matter in practice: can they solve real software engineering tasks, quickly and at a cost that makes sense. We’re proud that Codex is the recommended starting point in JetBrains AI. It’s a meaningful step in the shift from AI chat to agents that meet developers where they are, work in the tools they already use, and take on complex, multi-step work.”

  

  Stuart McMeechan, EMEA Deployment Engineering Lead, OpenAI

  Evaluation using real-world development tasks

  We evaluated candidate agents using a benchmark dataset built from real software engineering tasks across three ecosystems: Java (225 tasks), C# (38 tasks), and Python (90 tasks).

  Each task is grounded in a real codebase – with a prompt describing what needs to be done and automated tests that verify the result. Together, these tasks cover bug fixes, feature development, enhancements, and other common development tasks across real applications, libraries, frameworks, and developer tools.

  Data points used for choosing the recommended agent are accessible in the Developer Productivity AI Arena (DPAIA) repository – JetBrains’ open benchmark for evaluating AI coding tools, making the evaluation reproducible. The C# dataset is internal and not publicly available.

  The Java dataset was our primary evaluation set. It’s the largest of the three, spanning 17 repositories across five organizations and covering a broad mix of task types. 

  The С# and Python datasets produced a similar overall ranking of candidate agents, giving us additional confidence that the results were not specific to a single ecosystem.

  Our methodology

  We compared candidates within the same model tier. Our goal was not to find the most powerful model available, but the best agent behavior at comparable model capability and cost. We projected what agent usage would cost, taking into account JetBrains AI token usage. Setups that would push more than 2% of users over $20/month were ruled out before we ranked candidates on quality and latency.

  In choosing which agent to recommend, we focused on three questions:

  
   Can it handle the task? → Here, we measured by solve rate: the percentage of benchmark tasks where all tests passed.

  

  
   Is the cost reasonable? → We looked at the median cost per task.

  

  
   Is it fast enough? → We looked at median end-to-end latency.

  

  These three metrics (solve rate, cost, and latency) formed the basis of our ranking. We also tracked additional signals, including compilation success and average tool calls, but they did not materially affect the results.

  Alongside the offline benchmark, we ran an online A/B test with real users. This experiment served as a validation layer, helping us understand whether the offline results translated into real-world usage. Because it’s difficult to measure task success reliably at scale, we focused on behavioral signals such as engagement and how often users switched to another agent or returned to the chat. The online results were consistent with the offline benchmark, giving us additional confidence in our choice.

  Candidate configurations

  We tested agents available with JetBrains AI (Codex, Junie, and Claude Agent) – across multiple model configurations. Candidates were selected based on prior benchmarking and internal assessment; we focused on the most promising options within each agent’s model family rather than testing every possible setup. Eventually Codex and Junie were shortlisted. 

  Codex – we started with an initial sweep across GPT-5.2 and GPT-5.3. When GPT-5.4 mini became available, it outshined the previous top performer in terms of both solve rate and cost, making the model choice straightforward. The remaining question was reasoning level: medium vs. low. GPT-5.4 mini with default medium reasoning had the best solve rate within reasonable cost range across all three ecosystems and was selected for the final evaluation.

  
   
    
     GPT-5.4-mini comparison

     Medium Reasoning solved more tasks in Java, C#, and Python. Low Reasoning was cheaper and often faster, but the cost and latency gains were not large enough to make up for the more noticeable drop in solve rate. That is why we picked Medium Reasoning.

    

    
     All
     Java
     C#
     Python
    

    
     
      
       All

       Weighted average across ecosystems
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          GPT-5.4-mini low
         

        
        
         
          Solve rate
          39.9%
          35.1%
         

         
          Median latency
          170.40s
          137.82s
         

         
          Median cost
          USD 0.1387
          USD 0.0650
         

        
       

      

     

     
      
       Java

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          GPT-5.4-mini low
         

        
        
         
          Solve rate
          43.9%
          40.4%
         

         
          Median latency
          124.11s
          78.02s
         

         
          Median cost
          USD 0.1292
          USD 0.0615
         

        
       

      

     

     
      
       C#

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          GPT-5.4-mini low
         

        
        
         
          Solve rate
          62.6%
          51.6%
         

         
          Median latency
          142.95s
          87.86s
         

         
          Median cost
          USD 0.1152
          USD 0.0580
         

        
       

      

     

     
      
       Python

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          GPT-5.4-mini low
         

        
        
         
          Solve rate
          20.2%
          14.8%
         

         
          Median latency
          297.72s
          308.43s
         

         
          Median cost
          USD 0.1724
          USD 0.0766
         

        
       

      

     

    

   

  

  Junie - Junie can work with different model providers. We evaluated the Gemini model family, pre-selected based on the Junie team's own benchmarks as the most promising options. Gemini 3 Flash was selected as the winning model.

  
   
    
     Gemini model comparison

     Gemini 3 Flash had the stronger solve rate; Gemini 3.1 Flash Lite was consistently cheaper and faster.

    

    
     All
     Java
     C#
     Python
    

    
     
      
       All

       Weighted average across ecosystems
      

      
       
        
         
          Metric
          Gemini 3 Flash
          Gemini 3.1 Flash Lite
         

        
        
         
          Solve rate
          39.1%
          29.9%
         

         
          Median latency
          147.57s
          110.85s
         

         
          Median cost
          USD 0.1132
          USD 0.0564
         

        
       

      

     

     
      
       Java

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          Gemini 3 Flash
          Gemini 3.1 Flash Lite
         

        
        
         
          Solve rate
          45.2%
          36.3%
         

         
          Median latency
          142.80s
          100.54s
         

         
          Median cost
          USD 0.1053
          USD 0.0551
         

        
       

      

     

     
      
       C#

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          Gemini 3 Flash
          Gemini 3.1 Flash Lite
         

        
        
         
          Solve rate
          58.7%
          41.5%
         

         
          Median latency
          215.87s
          173.97s
         

         
          Median cost
          USD 0.1189
          USD 0.0661
         

        
       

      

     

     
      
       Python

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          Gemini 3 Flash
          Gemini 3.1 Flash Lite
         

        
        
         
          Solve rate
          15.6%
          9.1%
         

         
          Median latency
          130.64s
          109.97s
         

         
          Median cost
          USD 0.1304
          USD 0.0554
         

        
       

      

     

    

   

  

  Final showdown: Junie vs Codex

  The offline results were too close to call on their own. Neither agent dominated across all metrics and ecosystems.

  
   
    
     Codex vs Junie across ecosystems

     The final shortlist compared Codex with GPT-5.4-mini medium against Junie with Gemini 3 Flash.

    

    
     All
     Java
     C#
     Python
    

    
     
      
       All

       Weighted average across ecosystems
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          Gemini 3 Flash
         

        
        
         
          Solve rate
          39.9%
          39.1%
         

         
          Median latency
          170.40s
          147.57s
         

         
          Median cost
          USD 0.1387
          USD 0.1132
         

         
          Cost per successful solve
          USD 0.4941
          USD 0.4337
         

        
       

      

     

     
      
       Java

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          Gemini 3 Flash
         

        
        
         
          Solve rate
          43.9%
          45.2%
         

         
          Median latency
          124.11s
          142.80s
         

         
          Median cost
          USD 0.1292
          USD 0.1053
         

         
          Cost per successful solve
          USD 0.3716
          USD 0.2864
         

        
       

      

     

     
      
       C#

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          Gemini 3 Flash
         

        
        
         
          Solve rate
          62.6%
          58.7%
         

         
          Median latency
          142.95s
          215.87s
         

         
          Median cost
          USD 0.1152
          USD 0.1189
         

         
          Cost per successful solve
          USD 0.2307
          USD 0.2298
         

        
       

      

     

     
      
       Python

       Metric leaders are highlighted
      

      
       
        
         
          Metric
          GPT-5.4-mini medium
          Gemini 3 Flash
         

        
        
         
          Solve rate
          20.2%
          15.6%
         

         
          Median latency
          297.72s
          130.64s
         

         
          Median cost
          USD 0.1724
          USD 0.1304
         

         
          Cost per successful solve
          USD 0.9115
          USD 0.8882
         

        
       

      

     

    

   

  

  We included both in an online A/B test to see which held up better in real-world usage. We tracked activation, churn, and failure rate. Codex came out ahead. That tipped the decision.

  What is next for the recommended agent

  Codex is now the recommended agent, having delivered the strongest combination of solve rate and cost across the tasks we tested. This isn't a permanent decision, however. As models evolve, new agents join, and our benchmark coverage grows, we'll re-evaluate the decision and update our recommendation based on what the data tells us.

  And if a different agent works better for your workflow, you can switch at any time. Our recommendation is a starting point, not a constraint.

  
   Prev post How to Win a Hackathon: Notes From the Judging Table
