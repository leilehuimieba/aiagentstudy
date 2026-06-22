# Innovations from Google I/O 26 on Google Cloud

- BestBlogs URL: https://www.bestblogs.dev/article/d7f4c3b7
- Original publisher URL: https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud/
- Source: BestBlogs / Google Cloud Blog
- Publish time: 2026-05-20 08:00:00
- Capture route: article discovered from logged-in Edge/OpenCLI browser session; page/content captured from BestBlogs resource APIs
- Extracted chars: 16732

---

At Google Cloud Next ‘26, we unveiled the blueprint for the Agentic Enterprise, sharing our eighth-generation TPUs, Gemini Enterprise Agent Platform, a fully reimagined Agentic Data Cloud, Workspace Intelligence, and security built for the AI era. 

    Today at Google I/O, we’re delivering a new set of powerful AI innovations and models — and putting them directly in the hands of Google Cloud customers via Gemini Enterprise and Google Workspace:

    
     
      Gemini 3.5: Our latest family of models combines frontier intelligence with action – starting with Gemini 3.5 Flash. 

     

     
      Gemini Omni: Our new model is a leap forward in world understanding, multimodality, and editing, letting you generate any output from any input, starting with video. 

     

     
      Google Antigravity: Google Antigravity’s expanded capabilities and new integration with Agent Platform bring agentic development to your entire organization.

     

     
      Gemini Spark: For Gemini Enterprise and Workspace customers, Gemini Spark is your 24/7 personal AI agent that helps you work more efficiently by autonomously taking action on your behalf, under your direction. 

     

     
      Google Workspace: Google Pics, our new image generation and editing tool, and new voice features in Gmail, Docs and Keep, help reimagine how you work.

     

     
      Managed Agents API on Agent Platform: Allows developers to build and run custom agents inside secure, Google-hosted environments that seamlessly integrate with Agent Platform.

     

     
      CodeMender: A powerful AI security agent provided through Agent Platform, CodeMender can help find and fix vulnerabilities in your code.

     

    

    Expand what’s possible with Gemini 3.5

    We’re kicking off the Gemini 3.5 series with the release of 3.5 Flash, which delivers frontier performance for agents and coding, excelling at complex long-horizon tasks that deliver real-world utility. Google DeepMind engineered these models from the ground up using our purpose-built AI infrastructure. This unique co-design of the model and hardware allows us to train deeper reasoning capabilities faster and more efficiently with every new generation.

    
     
      Gemini 3.5 Flash delivers intelligence that rivals large flagship models on multiple dimensions at speeds you have come to expect from the Flash series. It’s our strongest agentic and coding model yet, outperforming Gemini 3.1 Pro on key benchmarks (Terminal-Bench 2.1: 76.2%, GDPval-AA: 1656 Elo, MCP Atlas: 83.6%) and leading in multimodal understanding (CharXiv: 84.2%). 3.5 Flash offers a balance of performance and speed, ideal for tackling long-horizon agentic tasks, often at less than half the cost of comparable models.

     

    

    
     
      Gemini 3.5 Pro is currently in testing and will be coming next month.  

     

    

    We have partnered closely with leading organizations across industries to validate the Gemini 3.5 series within their own environments.

   

  

  
   
    
     
      
       
        
       

      
      

     

     
      
     

    

   

  

  
   
    Gemini 3.5 Flash is rolling out today:

    
     
      Developers can build agents using Gemini 3.5 Flash on the Gemini Enterprise Agent Platform, or use it in your projects in Google AI Studio and Antigravity. 

     

     
      Business users can start using Gemini 3.5 Flash in the Gemini Enterprise app to help discover, create, and use the best of Google AI in their workflows starting today.

     

    

    Generate high-quality video content with Gemini Omni

    Gemini Omni is a groundbreaking new model that produces dynamic video content by blending text, audio, image, and video inputs. Building on how Nano Banana reimagined what you can do with images, Gemini Omni delivers a highly intuitive approach to video creation and editing using natural language. 

    This capability redefines how enterprises produce and refine visual media with intuitive creation and precise editing. Whether you are developing interactive virtual try-ons for e-commerce, streamlining complex post-production workflows, or generating tailored video narratives, Gemini Omni helps your team unlock entirely new ways to create content and drive deeper customer engagement. 

   

  

  
   
    
     
      
       
        
       

      
      

     

     
      
     

    

   

  

  
   
    Gemini Omni Flash will be rolling out in the coming weeks to developers and enterprise customers via the Gemini API and Agent Platform API. 

    Make everyone a builder with Google Antigravity

    Google Antigravity empowers the next era of enterprise builders. It enables your organization to transform how applications are built, deployed, and managed. 

    With Gemini 3.5 Flash, Antigravity delivers exceptional computational efficiency. This translates to more rapid development cycles and reduced operational costs for production-scale AI initiatives. Today, we are announcing new tools including:

    
     Enterprise security and compliance: Google Cloud customers can now access Antigravity through Agent Platform. By inheriting Google Cloud’s standard data privacy protections and Terms of Service, this ensures your customer data is in your control and agent activity runs within your secure cloud boundary by default.

     Antigravity 2.0 desktop app: At the core of the expanded Antigravity platform is Antigravity 2.0, a new standalone desktop app for builders that provides a centralized workspace to steer, customize, and orchestrate agents. For example, imagine managing a product launch and using Antigravity 2.0 to deploy simultaneous, agent-driven execution across critical project phases, including automated code generation for your website, creation of on-brand assets, and personalized customer email development. 

    

   

  

  
   
    
     
      
       
      

     
     
      
       Sequences shortened throughout

      

     

    

   

  

  
   
    
     Antigravity CLI: For developers who want a more lightweight interface for rapidly building and deploying agents, we are also launching an Antigravity CLI that is tightly integrated with the desktop app. 

    

    We’re using Antigravity every day to build at Google, and we’ve already seen Cloud customers and partners using it, too:

    “In modern enterprise architecture, the real bottleneck is the cognitive load on the engineer. Antigravity, augmented by Gemini within Accenture’s scaled agentic execution, abstracts away infrastructure complexity and automates delivery mechanics. By moving to a standalone application and consumption model, Google Cloud is making high-velocity engineering accessible at scale—enabling our best-in-class talent to focus on innovation and building resilient digital cores for our clients.” - Chetna Sehgal, Senior Managing Director and Global Practice Lead, Accenture Google Business Group

    “Antigravity isn't just an assistant; it’s a core component of our technical DNA. Its ability to simulate user environments via the agentic browser has revolutionized our QA process, while the agent manager has streamlined our entire pipeline. Today, more than half of our production-ready code is generated through these agentic workflows, proving that the future of software isn't just AI-assisted—it’s AI-driven." - Nikunj Shanti, CTO, AirAsia Next

    “Antigravity has transformed how our internal and Forward Deployed Engineering teams operate by enabling governed, autonomous software engineering workflows that adhere to Deloitte's enterprise security standards at massive scale. This capability allows us to rapidly accelerate the deployment of high-fidelity, AI-powered solutions for our clients and drive innovation across industries." - Faruk Muratovic, US AI & Engineering Strategy and Services Leader at Deloitte

    "Antigravity has fundamentally shifted our team from manual coding to high-level orchestration. By leveraging the agentic reasoning of Gemini, we’ve moved beyond simple code completion to a governed, autonomous workflow that maintains architectural integrity through every sprint. The ability to transform a functional requirements document directly into high-fidelity code while automating unit tests and documentation has drastically reduced our concept-to-deployment lifecycle. Antigravity acts as an autonomous coding partner that empowers our engineers to shift from manual syntax entry to governed, intelligent execution." - John O'Rourke, Technical Director, AI Implementation, Monks 

    "We're moving past simple AI code completion to true agent orchestration. By using Google Antigravity to run engineering pipelines in the background, our teams eliminate traditional development friction, allowing us to build custom client solutions and deliver value at unprecedented speed." - Vikas Agarwal, CTIO, PwC Advisory, PwC US and Global

    “WPP has integrated Antigravity into WPP Open, our agentic marketing platform to supplement our product development lifecycle. Leveraging the power of Gemini, it has streamlined workflows, automated repetitive tasks and empowered engineering teams to deliver high-quality solutions for our clients, faster.” - Callum Anderson, Head of Engineering, WPP Open

    To get started, download Antigravity and log in to the desktop application or Antigravity CLI using your standard Google Cloud credentials. Antigravity will be available in Gemini Enterprise in the coming months. 

    Gemini Spark, your 24/7 personal AI agent 

    To realize its full potential, AI must serve as the connective tissue that empowers every individual within your enterprise. This requires intelligent personal agents that grasp your specific business context – like what you’re working on, who you’re working with, and even your writing style. These agents can autonomously execute multi-step workflows on your behalf, with your permission, freeing your teams from routine, manual processes so they can focus on the high-impact, strategic innovation that drives your business forward.

    Gemini Spark in Gemini Enterprise is our new 24/7 personal agent that can work in the background across Workspace, custom connectors, and the open web. It enables you to: 

    
     Delegate complex work: Set recurring tasks, teach the agent new skills, and let it execute multi-step work on your behalf. 

     Maintain complete control: Spark proactively sends critical updates and requires explicit approval for high-risk actions like sending emails. 

     Personalize your agent-led experience: The more you use Spark, the better it learns your unique preferences and interactions to become a more accurate, helpful extension of your work style. 

     Connect to your tools and apps: Spark can use your existing Gemini Enterprise connectors, including Microsoft Sharepoint, OneDrive, ServiceNow, and many others.

     Security and governed sandbox: Spark operates in a fully managed, secure runtime on Google Cloud, meaning you get enterprise-grade security without ever having to manage the underlying infrastructure. Every task executes in a fresh, strictly isolated, ephemeral VM to help ensure data never overlaps between sessions. To protect your enterprise, all traffic routes through our secure Agent Gateway that enforces Data Loss Prevention (DLP) policies, while user credentials remain fully encrypted and are never exposed directly to the agent.

    

   

  

  
   
    
     
      
       
      

     
     
      
       Draft an email to stakeholders with Spark in Gemini Enterprise

      

     

    

   

  

  
   
    Spark can assist with tasks for many different processes in your organization to help teams focus on more strategic work. For example:

    
     
      Spark can identify a new product request related to critical functionality that needs to be fixed before launch and requires a major timeline change. In the background, it can automatically suggest code changes by working with Antigravity, create a Jira ticket for the development team to review the changes, cross-reference your team’s documents to recalculate the launch timeline, and update the internal status across relevant Sheets and Docs. It can then draft an email to relevant stakeholders confirming the actions it took and updating the team.

     

     
      Spark can help someone working in IT operations by monitoring system health via ServiceNow, checking for relevant tickets. When it detects a recurring critical issue, it creates an escalated Jira ticket to the developer team, drafts a comprehensive incident report in Docs, and pings the IT manager via Chat to review and approve the stakeholder communication plan.

     

     
      For salespeople, Spark can proactively prepare for client meetings by pulling account history from Salesforce and recent support tickets from Zendesk. Identifying a potential churn risk, Spark drafts a tailored account retention strategy in Docs and a customer-ready email, awaiting explicit user approval to send.

     

    

    Gemini Spark in the Gemini Enterprise app is rolling out to customers soon. Gemini Spark in Google Workspace will be available soon in preview for business customers in the Gemini app.

    Reimagine how you get work done with Google Workspace

    Today, we also announced new ways AI can help you accomplish even more directly in your Workspace apps, available in preview for business customers this summer: 

    
     
      Google Pics: Our new AI-powered image generation and editing tool gives you precise control over your images. Pics allows you to easily move, resize, and transform individual objects as well as modify and translate text independently. Built right into apps like Drive, Docs, and Slides, it makes complex editing easy so teams can quickly update global marketing campaigns, swap out products in a photo, or resize backgrounds to fit different ad layouts.

     

     
      Voice capabilities in Gmail, Docs and Keep: Brainstorm, organize and execute tasks hands-free in your favorite apps. You can quickly find a project due date from your inbox, iterate on a draft of your weekly report, or turn a messy brain dump into a structured list. 

     

    

    Unlock developer velocity with fully managed agents

    With the Managed Agents API on Agent Platform, builders can now instantly spin up custom agents that reason, call tools, and execute code inside secure, Google-hosted remote environments using a single API call. This allows technical teams to offload complex infrastructure management and focus entirely on agent behavior. Managed Agents API will automatically inherit Agent Platform's enterprise-grade data privacy, governance, and security protections.

    Visit the documentation to get started.

    Secure the Agentic Enterprise

    Advanced models, such as Gemini 3.5, unlock powerful new capabilities across your enterprise, including transforming AI security and vulnerability detection. Strategic risk mitigation, robust compliance, and trusted AI deployment are critical for sustained business growth. 

    In addition to sharing our findings and mitigations with the larger security and AI community, we are integrating CodeMender into Agent Platform. CodeMender is an AI code security agent, originally developed by Google DeepMind. Leveraging Agent Platform capabilities and advanced Gemini models, CodeMender autonomously identifies vulnerabilities within your code. It then recommends precise fixes, securely tests them, and can apply patches and necessary changes across dependent systems, with your approval. This entire process automates secure deployment while ensuring your developers retain control. 

    Several Gemini Enterprise customers are already testing CodeMender, and we will have more to share about expanded availability soon. 

    We are also making significant strides in ensuring platform trust and safety for synthetically generated media with a new AI Content Detection API, rolling out today on Agent Platform. This provides businesses with a powerful method to identify AI-generated content from both Google and other popular models, supporting responsible media governance. Learn more about our expanded tools for content transparency and verification.

    Looking ahead 

    With the latest Google Cloud updates unveiled at I/O, we’re making it easier than ever to move from initial idea to meaningful impact. These new tools are designed to streamline your workflows and empower your teams. For a deep dive into all the news and live product demonstrations, catch the full I/O keynote.
