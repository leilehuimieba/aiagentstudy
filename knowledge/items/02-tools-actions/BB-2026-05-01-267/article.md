# Announcing ADK for Kotlin and ADK for Android 0.1.0: Building AI Agents on Android and Beyond

- BestBlogs URL: https://www.bestblogs.dev/article/78c6e17d
- Original publisher URL: https://developers.googleblog.com/adk-kotlin-android-building-ai-agents/
- Source: BestBlogs / Google Developers Blog
- Publish time: 2026-05-21 08:00:00
- Capture route: article discovered from logged-in Edge/OpenCLI latest page 3 feed; page/content captured from BestBlogs resource APIs
- Extracted chars: 9351

---

ADK for Kotlin brings agentic workflows to your backend projects, while ADK for Android provides specialized on-device optimizations

    

    Following the recent 1.0.0 releases of ADK for Java and Go, as well as the beta of ADK for Python 2.0, we are thrilled to announce the launch of version 0.1.0 of Agent Development Kit (ADK) for Kotlin! In addition, we're also launching an additional specialized library called ADK for Android. ADK is a flexible and open-source framework for developing and running AI agents, and is now available in Kotlin. With the Android version you can create AI agents that can operate on-device directly within your apps with local on-device LLMs, enhancing privacy, but with the flexibility to bridge the gap with cloud-based models.

    Why ADK for Kotlin?

    The AI ecosystem is experiencing a massive shift toward the edge, since the introduction of Gemini Nano as a model on Android, it has become available on over 140 million devices. As developers look to build faster, more cost-effective, and privacy-enhancing applications, the ability to run AI models directly on mobile hardware (models like Gemini Nano) has never been more critical. However, building agentic systems can be complex, especially when coordinating tasks between the cloud and the edge. ADK removes that friction by managing all the complex orchestration, context handling, and error handling for you.

    With just a few lines of Kotlin, you can:

    

    
     Easily swap out models depending on your needs

     Choose between various on-device and cloud models for different parts of your multi-agent system

     Seamlessly share session state between multiple agents

     Run agents directly on Android devices
      

      

    

    Feature Highlights

    

    
     Hybrid Orchestration: You can use a cloud model as your main orchestrator, which can then offload specific tasks to sub-agents that run fully on-device. The ADK library takes care of adapting generic agent implementations to the correct cloud or on-device APIs.
      

      

     On-Device Sequential Agents: You can define sub-agents as sequential agents, perfect for multiple tasks that need to run one after the other.
      

      

     Local Retrieval: By utilizing on-device models like Gemini Nano, you can create retrieval agents that access and parse documents locally, ensuring data never has to leave the hardware.
      

      

     Flexible Tooling: You can equip your agents with specific tools and provide top-level instructions so they know exactly how to behave and when to delegate to subagents.
      

      

    

    Real-World Example: The Trip Assistant

    During our I/O session, we showcased how ADK for Kotlin powers an in-app trip assistant.

    

    Google I/O Video Embed

   

   
    If a user encounters an issue while traveling, the cloud-based orchestrator interacts with the user to understand the problem. However, when it needs to verify a booking confirmation, it delegates the task to an on-device subagent. Various retrieval agents use the on-device Gemini Nano model to extract data from the user's locally stored documents. Finally, a validation agent compares the data coming from these analyses. This keeps private data offline while leveraging the reasoning capabilities of the cloud orchestrator.

    Getting started with ADK for Android

    To add ADK to your Android app, add the following dependency to your build.gradle.kts file:

   

   
    implementation("com.google.adk:google-adk-kotlin-core-android:0.1.0")

    Kotlin

    
     
      
       
      
     
    

    
     
      
       
      
     
    

   

   
    You can then easily build your ADK agents:

   

   
    val orchestrator = LlmAgent(
  name = "genius_orchestrator",
  model = Gemini(apiKey = apiKey, name = MODEL_NAME),
  instruction = Instruction("""
    You are a travel genius assistant.
    First, use `get_trip_details` to get the full itinerary of the trip and 
    understand what events are scheduled.
    Then, respond with a welcome message tailored to the trip state.
    """.trimIndent()),
  tools = listOf(GetTripDetailsTool(tripId)),
  subAgents = listOf(carRentalPipeline, hotelPipeline),
  disallowTransferToPeers = true,
  disallowTransferToParent = true,
)

    Kotlin

    
     
      
       
      
     
    

    
     
      
       
      
     
    

   

   
    For more extended agent setups, check out the ADK for Android demos.

    Getting Started with ADK for Kotlin

    In your build.gradle.kts file, add the following dependencies:

   

   
    dependencies {
      // Implementation dependency for ADK Core
      implementation("com.google.adk:google-adk-kotlin-core:0.1.0")
      
      // KSP processor for generating @AdkTools
      ksp("com.google.adk:google-adk-kotlin-processor:0.1.0")
  }

    Kotlin

    
     
      
       
      
     
    

    
     
      
       
      
     
    

   

   
    ADK for Kotlin lets you define tools to equip the LLM with extra powers. Let’s create an imagined “improbability drive” service, inspired from the Hitchhiker’s Guide to the Galaxy:

   

   
    class ImprobabilityDriveService {
 /** Calculates the improbability of a given event. */
 @Tool
 fun calculateImprobability(
   @Param("The event to calculate the improbability for, e.g., 'A cup of tea materializing'")
   event: String
 ): String {
   return "The improbability of '$event' is approximately 42 to 1 against."
 }
}

    Kotlin

    
     
      
       
      
     
    

    
     
      
       
      
     
    

   

   
    Notice the use of the @Tool and @Param annotations to describe the tool to the LLM.

    Now, we can create a first agent, which will be the sub-agent of a main agent we’ll define later on. The HeartOfGold agent represents the spaceship’s computer:

   

   
    val heartOfGoldAgent =
    LlmAgent(
      name = "HeartOfGold",
      description = "The Heart of Gold ship computer. Handles improbability drive queries.",
      model = Gemini(apiKey = apiKey, name = "gemini-2.5-flash"),
      instruction =
        Instruction(
          """
          You are the ship computer of the Heart of Gold. You are cheerful, helpful, and slightly annoying.
          You have access to the Infinite Improbability Drive.
          Use real facts about yourself if asked, but keep it funny.
          """
          .trimIndent()
        ),
      tools = ImprobabilityDriveService().generatedTools()
    )

    Kotlin

    
     
      
       
      
     
    

    
     
      
       
      
     
    

   

   
    Now we can use this sub-agent in our root agent:

   

   
    val rootAgent =
  LlmAgent(
    name = "MissionControl",
    description = "The central router for space queries. Routes to HeartOfGold.",
    subAgents = listOf(heartOfGoldAgent),
    model = Gemini(apiKey = apiKey, name = "gemini-2.5-flash"),
    instruction =
      Instruction(
        """
        You are Mission Control. You are the central hub for all communications.
        Your main job is to route the user's query to the most appropriate agent.
        - If the query is about improbability, the Infinite Improbability Drive, or the Heart of Gold, transfer to `HeartOfGold`.
        - Otherwise, respond directly with a professional but stressed persona.
        """
        .trimIndent()
      )
  )

    Kotlin

    
     
      
       
      
     
    

    
     
      
       
      
     
    

   

   
    The heartOfGoldAgent is defined as a subagent in the agent configuration of this main agent.

    When the user asks questions about the improbability of an odd event to happen, the main agent delegates the task to the heartOfGoldAgent, which in turn will call the local function tool to calculate the probability, before replying to the user.

    This is a simple example of how you can define tools and sub agents in ADK for Kotlin.

    ADK feature set

    The ADK for Kotlin & ADK for Android 0.1.0 releases contain the foundational feature set required for building AI agents on Android and beyond, including advanced control over agent execution, comprehensive tooling, and essential services for state management.

    Agents

    
     LLM-based, workflow-based, custom agents

     Multi-agent systems

    

    Tooling & Integrations

    
     Function tools

     Long-running function tools

     MCP Tools

     A2A

     Plugins

    

    Runtime & Observability

    
     Session state for short-term memory,

     Memory service for long-term memory

     Telemetry (OpenTelemetry)

    

    Developer Experience

    
     Web interface for development and experimentation

    

    Android Models

    
     ML Kit GenAI to access on-device Gemini Nano via AICore

     Firebase AI Logic to access Gemini models running in the cloud

     Google GenAI for quick prototyping

    

    

    What's Next?

    This 0.1 release is our first experimental version of the library, currently featuring default agents for the ML Kit GenAI APIs and direct connections to Gemini in the Cloud. But we are just getting started!

    We are incredibly excited about the future of in-app AI and can’t wait to see the intelligent experiences you build. Be sure to check out the project on GitHub!
