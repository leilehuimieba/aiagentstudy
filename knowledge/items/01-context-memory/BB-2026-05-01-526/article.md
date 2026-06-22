# Spring AI 2.0.0 GA Available Now

- BestBlogs URL: https://www.bestblogs.dev/article/9ed27696
- Original publisher URL: https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now
- Source: BestBlogs / Spring Blog
- Publish time: 2026-06-12 08:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 1; page/content captured from BestBlogs resource APIs
- Extracted chars: 9774

---

On behalf of the team and everyone who has contributed, I'm happy to announce that Spring AI 2.0.0 has been released and is now available from Maven Central!

  Release notes | Upgrade notes | Reference documentation | Javadoc

  Improved foundations

  Since the early days, Spring AI has grown very fast in terms of features, model support, contributions and users. That’s great and exciting, but we felt the need for setting a new baseline in terms of scope, quality and consistency in order to allow evolving the project in a sustainable way. So a few months ago, we took a step back and defined areas that we wanted to improve mostly in terms of design and consistency, also taking into account user feedback from issues and pull requests. Those new foundations that we release today will significantly improve the developer experience, allow higher quality contributions by the community and make it easier to integrate upcoming features we have already identified in our roadmap.

  Spring Boot 4 baseline

  Spring AI 2.0 has been designed to be used with Spring Boot 4.0 / 4.1 and Spring Framework 7.0, but it brings much more profound benefits than just upgrading the dependency versions and fixing compatibility issues.

  Jackson 3

  JSON serialization was greatly improved by the upgrade from Jackson 2 to Jackson 3. The documentation now explains how to customize the default JsonMapper and introduces a new JsonHelper class for providing a fully customized JsonMapper.

  Null-safety

  Following the principles described in Null-safe applications with Spring Boot 4, Spring AI codebase is now fully annotated with JSpecify annotations. In addition to preventing null-pointer exceptions at runtime and providing a Kotlin idiomatic API, it allows clarification where values are optional or mandatory in the codebase.

  Options

  Working on null-safety also triggered a major refactoring of how options and configuration properties are handled:

  
   Clarification of which options are mandatory or optional

   Default values are now consistently defined at options level (not model or configuration properties)

   Options are created with builders (not constructors) and are immutable once instantiated.

   Those builders now provide consistent and reflection-free merging capabilities

   Decoupling of options and configuration properties allowed the removal of the artificial .options segment in application property keys and fixing a lot of bugs

  

  Lastly, we have clarified when options can be partially specified (typically with an option builder acting as a customizer for the ChatClient default options), and when they need to be fully specified (ChatModel level). More generally, you will see that Spring AI 2.0 embraces using ChatClient as the most common user-facing API while ChatModel is more of a lower-level building block. Read further for more exciting news about this.

  More focus

  We have chosen to focus the Spring AI core project on a well-defined set of chat model providers supported out-of-the-box:

  
   OpenAI
    
     went from 3 variants (Azure, HTTP, SDK) to 1 (SDK)

     can be used to access other models providing an OpenAI compatible API

    

   Anthropic
    
     went from 2 variants (HTTP, SDK) to 1 (SDK)

     can be used to access other models like Minimax providing an Anthropic compatible API

    

   Amazon Bedrock

   Google GenAI
    
     went from 2 implementations (GenAI SDK, Vertex) to 1 (GenAI SDK)

    

   Mistral AI

   DeepSeek

   Ollama

  

  We expect that leveraging vendor SDKs for OpenAI, Anthropic and Google will help Spring AI adapt to the latest model API extensions and new features.

  Some models are now maintained directly by the related vendors in collaboration with the Spring AI team:

  
   OCI Generative AI (kudos to Anders Swanson from Oracle)

   Azure Cosmos DB (kudos to Theo van Kraay from Microsoft)

  

  We welcome support for additional models maintained externally. 

  Better collaboration with the community

  The pace of contributions to Spring AI keeps increasing, we are super grateful to have such a vibrant community, but we also face challenges to be able to integrate those contributions. The improved consistency of Spring AI 2.0 codebase will help, but we also need to provide more guidance to our community in order to make those contributions more useful and integrated in a timely manner. Also as contributions involving coding agents are now the vast majority of the pull requests we receive, we think it is even more important in that context to have proper human review.

  For this reason Spring AI now has a brand new CONTRIBUTING.md documentation, designed both for humans and agents, clarifying the rules and conventions for contributions. Please read it carefully if you plan to contribute.

  Agentic support improvements 

  Agentic AI systems require a place to intercept and compose around the tool execution loop. In Spring AI 1.x that was challenging, as each chat model contained its own private tool-calling loop, buried inside the implementation with no way to hook into it, wrap it, or swap one execution strategy for another. You could call tools; you could not build on top of tool calling.

  Spring AI 2.0 lifts the tool loop into the advisor chain as a first-class, composable component. ChatClient runs every request through an ordered chain of advisors and supports looping, letting an advisor re-enter the downstream chain. The same mechanism drives tool-call loops, structured-output retry loops, and evaluation loops alike.

  Unified Tool Calling

  In Spring AI 2.0, ToolCallingAdvisor is auto-registered by the ChatClient and implements the full tool-call round-trip. The ad-hoc tool loops previously implemented in each chat model are gone. When you need explicit control over each tool iteration, you can opt out and drive the loop manually.

  Scaling to Hundreds of Tools

  ToolSearchToolCallingAdvisor brings progressive tool disclosure to tool calling. Instead of registering every tool with every request, it exposes them incrementally on demand: the advisor indexes the full tool set once per session and lets the model retrieve relevant tools as needed.

  Structured Self-Correcting Output

  Spring AI has always offered portable, first-class structured output support, but even with native structured output enabled, a model can return non-conforming JSON. The auto-registerable StructuredOutputValidationAdvisor self-corrects on validation failures.

  Spring AI Community Extensions

  
   New Event-Sourced Conversation Memory:

  

  The spring-ai-session community project is an event-sourced replacement for the built-in ChatMemory. It supports all message types, including tool calls (safe inside the tool-call loop with any backend) and applies pluggable, turn-aware compaction strategies — including LLM-powered summarization — when the context window fills up.

  
   Agentic Patterns on Top of the Foundation:

  

  The spring-ai-agent-utils community project builds on Spring AI 2.0's agentic foundation with production-ready primitives for building agentic systems, packaged as composable tools and advisors. It features Agent Skills, a portable, Spring AI-native implementation of the AgentSkills specification, as well as file, shell, web-fetch, task, auto-memory, and other useful utilities.

  MCP Integration 

  Model Context Protocol (MCP) is emerging as the common protocol for AI integrations. 

  The Spring team builds and maintains the official MCP Java SDK, so Spring AI's MCP integration tracks the specification at the source. Spring AI 2.0 ships with MCP Java SDK 2.0.0, compliant with the latest 2025-11-25 MCP specification and consolidates the full MCP ecosystem under the Spring AI umbrella.

  Annotation-Driven Programming Model

  The mcp-annotations module (previously incubated in the community) is now part of Spring AI. The @McpTool, @McpResource, and @McpPrompt allow exposing any Spring service in an MCP server as a matter of one method annotation.

  A unified McpSyncRequestContext / McpAsyncRequestContext parameter, injected automatically into server handler methods, gives tools and resources a single entry point for logging, progress reporting, sampling, and elicitation.

  The client side is a first-class citizen as well. Declarative handlers cover the full protocol callback model, with annotations for LLM sampling, elicitation, and capability-change notifications — enabling truly reactive agent clients.

  MCP Transports

  The WebMVC and WebFlux transport implementations have been moved from the MCP Java SDK into Spring AI, aligning their release cadence with the rest of the framework. Streamable HTTP is now the default, replacing the deprecated SSE transport. Its stateless variant can be used to enable remote deployment scalability at the cost of MCP's bi-directionality communication. STDIO remains available for local process-based integrations.

  MCP Enterprise Features

  Spring AI's MCP integration inherits the full Spring production stack: Micrometer spans and OpenTelemetry-compatible metrics for server interaction and OAuth 2.0 and API-key security via the spring-ai-community/mcp-security project.

  Conclusion

  Spring AI 2.0 has been made possible thanks to the amazing work of the Spring AI team and community. It provides a significantly improved developer experience for creating AI applications with Spring Boot 4, and opens the path to upcoming ambitious new features we will share in the upcoming months. We hope you will like it!

  Try it on start.spring.io or by upgrading your applications, and feel free to provide feedback on what you like, and what you hope in our future releases.

  Cheers!
