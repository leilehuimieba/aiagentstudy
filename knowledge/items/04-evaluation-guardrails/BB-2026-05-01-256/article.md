# Building a Secure MCP Server on AWS for a Million-Company B2B Platform

- BestBlogs URL: https://www.bestblogs.dev/article/fca204e7
- Original publisher URL: https://www.infoq.com/articles/secure-mcp-server-aws/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-05-18 19:00:00
- Capture route: article discovered from logged-in Edge/OpenCLI latest page 2 feed; page/content captured from BestBlogs resource APIs
- Extracted chars: 35856

---

Key Takeaways

    
     MCP servers should be designed as production interfaces, not as thin demo wrappers around existing APIs.

     Separating read and write operations at the tool level is one of the simplest and most effective ways to reduce risk in LLM-connected systems.

     A default-deny approach to mutations creates a safer path from experimentation to production use.

     Mocked tests became much more valuable once we captured the actual GraphQL variables sent by each tool, which exposed normalization bugs such as incorrect country-code resolution and missing limit capping before requests reached AppSync.

     The most important production failure in the project was not caught by unit tests such as create_collection, which passed mocked tests but failed against the real backend with a Lambda null-pointer error. This situation is why real-system validation through MCP Inspector remained a release gate.

    

   

   Introduction

   The Model Context Protocol has made it easier to connect LLM clients to existing systems, but most examples still stop at the point where a demo becomes interesting. The harder question is what happens when the same integration touches real business data, real workflows, and real operational constraints.

   In our case, we wanted to expose a B2B intelligence platform built on more than one million company profiles to an LLM client through an MCP server. The user-facing idea was simple: Instead of opening a portal, typing a query, reviewing results, and exporting data manually, a user could ask for a structured request such as "find SaaS companies in Germany with 50-200 employees" and receive results through the LLM client. The engineering problem was less simple: How do you make that workflow useful without creating an unsafe bridge between an LLM and production data?

   That question shaped the implementation from the beginning. We did not treat the MCP server as a convenience wrapper around an existing API. We treated it as a first-class interface with its own contracts, security assumptions, testing strategy, and operational controls.

   
   Because the underlying platform serves more than one million company profiles, the MCP layer had to be designed with scale in mind from the start rather than treated as a lightweight integration experiment. At that scale, narrow tool boundaries, predictable request handling, and clear auditability matter not only for security but also for keeping behavior understandable for both engineers and users.

   The Architecture

   The platform already exposed data through GraphQL on AWS AppSync, which gave us a structured backend boundary for reading business objects. Additionally, we built a Go-based MCP server that translated user requests into a set of narrowly scoped tools rather than pushing business logic into the LLM layer itself. The implementation used mcp-go, a GraphQL client for AppSync, and a tool layer covering search, AI-assisted search, and collection-oriented actions.

   That architecture helped in two ways. First, AppSync remained the system of record for backend access instead of letting the MCP layer become an ad hoc integration surface. Second, the tool layer could be designed around explicit responsibilities, which made the system easier to test and easier to reason about.

   This architecture turned out to matter more than the protocol itself. MCP provides the connection model, but the real production question is how much power each tool gets and how precisely its behavior is defined. If tool contracts are vague, the MCP server becomes hard to validate, hard to observe, and easy to misuse.

   At an implementation level, the MCP server acted as a contract-enforcing layer rather than a pass-through proxy. User requests were normalized into explicit tool calls; those tool calls mapped to bounded GraphQL operations, and the response shape stayed narrow enough to validate independently of the LLM client. This separation was important because it reduced the chance that prompt-level ambiguity would leak directly into backend behavior.

   End-to-End Request Flow

   When a user makes a request through an LLM client, the following layers handle it in sequence:

   
    The LLM client sends a tool call over the MCP stdio transport with a JSON argument payload (for example, {"query": "SaaS companies in Germany", "country": "DE", "limit": 20}).
     

     The MCP server receives the call through the mcp-go library, which dispatches it to the registered handler for that tool name.

    Argument parsing and validation.
     

     Each tool handler first parses the raw map[string]any arguments into a typed Go struct using JSON marshal/unmarshal. Then validation runs: Required fields are checked, limits are capped (for example, maximum one hundred results), and inputs are trimmed and normalized. For mutation tools, a mutationsAllowed boolean is checked before any further processing. If validation fails, the tool returns an error immediately without touching the backend.

    GraphQL execution.
     

     The tool constructs a variables map and calls client.Execute(ctx, query, variables, &result) against the AppSync endpoint. The GraphQL client handles authentication (Open ID Connect (OIDC) bearer token, API key, or AWS SigV4 signing) and HTTP-level errors (401, 404, 429) transparently.

    Response shaping.
     

     The GraphQL response is unmarshaled into internal types (gqlCompanyModelV2, gqlCollection, etc.) and then mapped to flat, AI-friendly public types (CompanySummary, CompanyDetail, Collection). For search and retrieval tools, explicit conversion functions like toCompanySummary() handle the flattening. Mutation tools return minimal result structs directly (for example, add_to_collection returns only { collection_id, success }). In both cases, the LLM receives a consistently shaped record without nested objects.

    Serialization and return.
     

     The result is serialized to JSON and returned to the LLM client as a CallToolResult text content block.

   

   The key point is that validation, execution, and shaping are each handled by a distinct layer. The MCP server never passes raw user input directly to GraphQL, and it never returns raw GraphQL responses to the client.

   Tool Inventory

   The implementation defines nine tools, grouped by capability:

   Read-only tools (six)

   
    
     
      Tool
      Purpose
      Key Parameters
     

     
      search_companies
      Keyword search with country filtering
      query (required), country, limit (max 100)
     

     
      get_company
      Full company profile by ID
      id (required)
     

     
      get_companies_batch
      Batch lookup, max 50 IDs, deduplicates
      ids (required)
     

     
      ai_search
      Natural language search with conversation threading
      query (required), thread_id; rate-limited to 5 req/min
     

     
      list_collections
      List user’s saved collections
      (none)
     

     
      get_collection_items
      Paginated items within a collection
      collection_id (required), query, offset, limit
     

    
   

   Mutation-capable tools (three, all gated by --allow-mutations)

   
    
     
      Tool
      Purpose
      Key Parameters
     

     
      create_collection
      Create a new collection
      name (required); disabled in production due to a backend Lambda null-pointer error discovered during integration testing
     

     
      add_to_collection
      Add companies to a collection
      collection_id (required), company_ids (required)
     

     
      request_email_discovery
      Trigger email lookup for a contact
      contact_id (required); rate-limited to 10 req/hour
     

    
   

   In the shipped configuration, eight of the nine tools were exposed. The tool create_collection was commented out of the registration path after integration tests revealed a backend Lambda error that had not surfaced through unit tests alone.

   Read and Write Should Not Be Blurred

   The most important implementation decision was separating read and write operations from the start. In many early MCP examples, tools are intentionally broad: They search, update, and orchestrate actions through one flexible interface. That approach may be acceptable in a prototype, but it creates unnecessary ambiguity once the interface points at real systems.

   When a model can reach business data, "query" and "change" should not be separated by convention alone. They should be separated in the tool design itself. In our implementation, read paths stayed read-only, and mutation-capable actions were blocked by default.

   This approach not only made the system safer, it also made it easier to maintain. A read-only tool is simpler to review, simpler to test, and simpler to observe, because it expresses one kind of intent instead of many. In practice, narrow contracts turned out to be a stronger safety control than trying to retrofit policy on top of a tool that had already become too flexible.

   This separation also mattered because the platform was not serving a toy dataset. On a system with more than one million company profiles, even small ambiguities in tool behavior can turn into confusing results, broad queries, or unsafe operator assumptions. Keeping read paths strictly read-only reduced the amount of behavior that had to be trusted during the early stages of adoption.

   How Read and Write Tools Are Registered Separately

   The separation between read and write is enforced at the registry level. When the tool registry is created, the allowMutations flag is passed through to each mutation-capable tool. Read-only tools are never passed with this flag because they have no mutation path to gate:

   func NewRegistry(gqlClient graphql.Client, allowMutations bool) *Registry {
    return &Registry{
        gqlClient:         gqlClient,
        // Read-only tools – no mutation flag needed
        searchCompanies:   NewSearchCompaniesTool(gqlClient),
        getCompany:        NewGetCompanyTool(gqlClient),
        getCompaniesBatch: NewGetCompaniesBatchTool(gqlClient),
        aiSearch:          NewAISearchTool(gqlClient),
        listCollections:   NewListCollectionsTool(gqlClient),
        getCollectionItems: NewGetCollectionItemsTool(gqlClient),
        // Mutation tools – receive the flag
        createCollection:      NewCreateCollectionTool(gqlClient, allowMutations),
        addToCollection:       NewAddToCollectionTool(gqlClient, allowMutations),
        requestEmailDiscovery: NewRequestEmailDiscoveryTool(gqlClient, allowMutations),
    }
}

   Each mutation tool stores the flag internally and checks it at the top of its Execute method before doing anything else:

   func (t *CreateCollectionTool) Execute(ctx context.Context, params CreateCollectionParams) (*CreateCollectionResult, error) {
    if !t.mutationsAllowed {
        return nil, fmt.Errorf("mutations are disabled; use --allow-mutations flag to enable write operations")
    }
    // ... validation and execution follow
}

   With this approach, a mutation tool will fail immediately and predictably if it is called without the flag, regardless of what the LLM client intended.

   Concrete Read and Write Tool Examples

   Read Tool Example, search_companies

   Input contract:

   type SearchCompaniesParams struct {
    Query   string `json:"query"`           // required
    Country string `json:"country,omitempty"` // ISO 3166-1 alpha-2 or full name
    Limit   int    `json:"limit,omitempty"`   // default 10, max 100
}

   Output shape:

   {
  "companies": [
    {
      "id": "example.com",
      "name": "Example Inc",
      "description": "Cloud infrastructure provider...",
      "country": "United States",
      "countryCode": "US",
      "locality": "San Francisco",
      "employeeCount": 150,
      "employeeRange": "101-250",
      "domain": "example.com",
      "industryTags": ["Technology", "Cloud Computing"]
    }
  ],
  "total": 42
}

   The tool validates that query is non-empty, caps limit to one hundred, resolves country codes (e.g., "DE" becomes "countries;Germany"), and flattens the nested GraphQL response into a flat CompanySummary record.

   Mutation Tool Example, add_to_collection

   Input contract:

   type AddToCollectionParams struct {
    CollectionID string   `json:"collection_id"` // required
    CompanyIDs   []string `json:"company_ids"`   // required, non-empty
}

   Output shape:

   {
  "collection_id": "col-abc-123",
  "success": true
}

   This tool checks mutationsAllowed first, validates both fields, then executes a GraphQL mutation with itemType, "COMPANY". The operation is idempotent, adding a company that already exists in the collection succeeds without error.

   Default-Deny Mutations

   We introduced an explicit --allow-mutations flag before any mutation-capable behavior could run. That is not a full authorization model, but it is an effective control point. It forces teams to make a deliberate decision about whether write paths are even available in a given environment.

   This point became important because LLM integrations usually start as experiments and only later begin to accumulate operational expectations. Once a system becomes useful, there is pressure to let it do more. If the original design assumed broad access, that pressure often turns into unsafe shortcuts.

   A default-deny model changes the conversation. Instead of asking, "Why not let the client write?", teams are forced to ask, "What evidence do we need before this class of write operations becomes acceptable?" That is a better engineering question because it ties permission expansion to proof, controls, and operational readiness.

   The flag also created a practical boundary between exploratory usage and environments where safety mattered more than convenience. That kind of explicit switch is useful because it makes mutation capability a conscious decision instead of an accidental default that appears over time as the integration becomes more capable.

   How --allow-mutations Is Implemented

   The flag is registered as a Cobra CLI flag with a false default:

   serveCmd.Flags().BoolVar(&allowMutations, "allow-mutations", false,
    "Enable write operations (create collections, add items, etc.)")

   When the server starts, the flag value is passed to the tool registry:

   toolsRegistry := tools.NewRegistry(gqlClient, allowMutations)

   The server startup log records the current state of the flag alongside other configuration:

   level=INFO msg="starting mcp-server" auth=oidc mutations=false tools=8 resources=2 prompts=2

   There is no additional authorization check behind the flag in the current implementation. It acts as a binary gate: Either all mutation tools can execute, or none of them can. This was a deliberate choice for the initial version. The reasoning was that a simple, visible control is better than a complex one that teams might misconfigure. A more granular per-tool or per-user authorization model could be layered on later once usage patterns justified the complexity.

   In the MCP client configuration (.mcp.json), the flag is passed as a CLI argument, making it visible to anyone reviewing the integration setup:

   {
  "mcpServers": {
    "mcp-server": {
      "command": "/path/to/mcp-server",
      "args": ["serve", "--endpoint", "https://api.example.com/graphql",
               "--region", "eu-west-1", "--allow-mutations"]
    }
  }
}

   Tool Contracts Matter More Than Tool Count

   One lesson from the implementation was that tool count matters less than tool shape. Nine narrowly scoped tools can be safer than two general-purpose ones if each tool has a clear input model, a bounded output structure, and a small operational surface. This point matters especially when the client is probabilistic and may express valid intent in inconsistent ways.

   A narrow tool contract helps compensate for that uncertainty. It makes failures easier to diagnose, results easier to validate, and future changes easier to manage. By contrast, a broad tool tends to evolve into an informal remote control layer for the backend, which makes both safety and maintenance worse over time.

   This also has implications for versioning. A narrowly defined tool can usually evolve behind a stable contract. A broad tool tends to accumulate hidden dependencies in prompt behavior and user expectations, so even small changes can create regressions that are difficult to predict.

   At this scale, bounded output structure mattered as much as bounded input. Returning consistently shaped records made it easier to reason about result quality, limit accidental overexposure, and keep downstream handling predictable for testing, logging, and client-side interpretation.

   Of the nine tools, search_companies works best as a reference contract because it exercises all three concerns in a single request path: input validation, input normalization (country-code resolution and limit capping), and flattening of a nested GraphQL response into a single flat record.

   Local Validation Is a Production Concern

   The implementation used aws-vault for authentication and MCP Inspector for validation outside of the LLM client. At first glance, that approach looks like a developer convenience choice. In practice, it was a choice based on reliability.

   If engineers can only validate an MCP server through the final client, debugging becomes slower and the interface becomes less transparent. A local inspection path makes it easier to examine request and response structures, confirm tool behavior, and isolate failures before the LLM is involved. Taking that path reduces the amount of ambiguity in end-to-end testing.

   A good local workflow also lowers the cost of doing the right thing. Teams are more likely to keep tests current and contracts narrow when they can inspect the system directly. When the local loop is painful, the usual result is not discipline, but drift.

   In a production-minded workflow, local validation is also where teams can confirm that a tool fails in understandable ways before the LLM adds another layer of uncertainty. That validation matters when the backend already has clear contracts and the MCP layer is responsible for preserving them rather than weakening them.

   Authentication Workflow

   The MCP server authenticates to AppSync using OIDC bearer tokens issued by the platform’s identity provider. Each token is tied to an authenticated user, short-lived, and scoped to the operations that user is authorized to perform. AppSync enforces authentication at the resolver level through its @aws_oidc directive, so the backend rejects requests with expired or invalid tokens before the resolver logic runs.

   This approach matters for an MCP server because the LLM client is acting on behalf of a specific user, not as a generic service. If the server authenticated with a static API key or a shared service credential, every request would carry the same access regardless of who initiated it. With OIDC, the token carries the user’s identity, so backend authorization, audit trails, and data scoping all work the same way they would if the user were calling the API directly. The MCP layer does not bypass or weaken the platform’s existing access model, it inherits it.

   From an operational perspective, short-lived tokens also limit the blast radius of a compromised credential. A leaked API key is valid until someone rotates it. A leaked OIDC token expires on its own, typically within hours. For an MCP server that touches business data across more than a million company profiles, that difference matters.

   The server logs which authentication method is active at startup, so operators can verify the configuration without inspecting traffic:

   level=INFO msg="starting mcp-server" auth=oidc mutations=false tools=8

   MCP Inspector Validation

   MCP Inspector connects to the server over stdio and lets engineers issue tool calls without involving the LLM client. A typical validation session:

   Successful Request Example:

   > Tool: search_companies
> Args: {"query": "fintech", "country": "GB", "limit": 5}
< Result: {"companies": [{"id": "revolut.com", "name": "Revolut", ...}], "total": 127}

   Failed Request Example, mutation blocked:

   > Tool: add_to_collection
> Args: {"collection_id": "col-123", "company_ids": ["revolut.com"]}
< Error: "mutations are disabled; use --allow-mutations flag to enable write operations"

   This second case was particularly useful during development. It confirmed that the mutation gate returned a clear, actionable error message rather than a generic failure, something that matters when the LLM client needs to explain the failure to the user.

   Test the MCP Layer as Its Own Interface

   One common mistake is to assume that if the backend API already works, the MCP layer is mostly a transport concern. In practice, the MCP layer introduces its own failure modes: weak validation, unclear tool semantics, poor error handling, and mismatches between tool behavior and backend assumptions. That concern is why we treated it as an interface that needed its own test strategy.

   The implementation used a TDD-oriented approach with mocked GraphQL clients for unit-level tool tests and manual validation against the real AppSync endpoint through MCP Inspector. Mocked clients helped isolate tool logic and cover edge cases cleanly. Manual inspection against the real backend then verified that the actual AppSync wiring behaved as expected under realistic conditions.

   Negative testing was equally important. It was not enough to check that valid requests succeeded. We also needed to verify that invalid inputs failed clearly, blocked mutations stayed blocked, and tool errors did not encourage confusing or unsafe retries. This testing is less about proving correctness in the abstract and more about preserving contract discipline. A tool that fails predictably is often safer than a tool that tries to be forgiving in ways the rest of the system cannot support.

   Test layering mattered because the MCP server was not only translating requests; it was also enforcing a safety boundary. Unit-level tests could check tool behavior in isolation, while manual validation through MCP Inspector could confirm that the AppSync boundary, authentication path, and expected response contracts still held together in realistic flows.

   Mocked GraphQL Client Setup

   The mock client uses Testify’s Mock and implements the same graphql.Client interface as the real clients:

   type MockClient struct {
    mock.Mock
}

func (m *MockClient) Execute(ctx context.Context, query string, variables map[string]any, result any) error {
    args := m.Called(ctx, query, variables, result)
    return args.Error(0)
}

   In tests, the mock is wired to inject responses directly into the result pointer, bypassing HTTP entirely:

   func TestSearchCompanies_ValidQueryReturnsResults(t *testing.T) {
    mockClient := graphql.NewMockClient()
    tool := NewSearchCompaniesTool(mockClient)

    mockClient.On("Execute", mock.Anything, mock.Anything, mock.Anything, mock.Anything).
        Run(func(args mock.Arguments) {
            result := args.Get(3).(*gqlSearchCompaniesResponse)
            result.EnhancedSearchCompanies.Companies = []gqlCompanyModelV2{
                {ID: "example.com", CompanyModel: gqlCompanyModel{
                    Company: gqlCompany{Name: "Example Inc", Domain: "example.com"},
                    IndustryTags: []string{"Technology"},
                }},
            }
            result.EnhancedSearchCompanies.TotalResults = 1
        }).
        Return(nil)

    result, err := tool.Execute(context.Background(), SearchCompaniesParams{
        Query: "tech companies", Limit: 10,
    })

    require.NoError(t, err)
    assert.Len(t, result.Companies, 1)
    assert.Equal(t, "example.com", result.Companies[0].ID)
}

   This approach also supports capturing the variables sent to GraphQL, which proved useful for verifying that normalization logic was applied before the query reached the backend:

   var capturedVariables map[string]any
mockClient.On("Execute", mock.Anything, mock.Anything, mock.Anything, mock.Anything).
    Run(func(args mock.Arguments) {
        capturedVariables = args.Get(2).(map[string]any)
        // ... set result
    }).Return(nil)

// After execution:
limit := capturedVariables["limit"].(int)
assert.Equal(t, 100, limit, "limit should be capped to 100")

   The first bug this technique exposed was an incorrect country-code mapping, where an earlier version of the tool forwarded values like "US" to GraphQL instead of the API’s required "countries;United States" format, and the mocked output assertions still passed cleanly because the backend returned an empty result set for the malformed filter.

   A TDD Example: Mutation Gating

   The mutation gating logic was developed test-first. The initial test described the expected behavior before the implementation existed:

   Step 1, A Failing Test

   func TestCreateCollection_BlockedWithoutMutationsFlag(t *testing.T) {
    mockClient := graphql.NewMockClient()
    tool := NewCreateCollectionTool(mockClient, false) // mutations NOT allowed

    result, err := tool.Execute(context.Background(), CreateCollectionParams{
        Name: "Test Collection",
    })

    require.Error(t, err)
    assert.Nil(t, result)
    assert.Contains(t, err.Error(), "mutations")
    assert.Contains(t, err.Error(), "--allow-mutations")
    mockClient.AssertNotCalled(t, "Execute") // must not reach GraphQL
}

   This test failed initially because the Execute method had no mutation check.

   Step 2, An Implementation Change

   func (t *CreateCollectionTool) Execute(ctx context.Context, params CreateCollectionParams) (*CreateCollectionResult, error) {
    if !t.mutationsAllowed {
        return nil, fmt.Errorf("mutations are disabled; use --allow-mutations flag to enable write operations")
    }
    // ... rest of implementation
}

   Step 3, A Passing Test

   After adding the guard, the test passed: The error message contained both "mutations" and "--allow-mutations", the result was nil, and critically, mockClient.AssertNotCalled(t, "Execute") confirmed that no GraphQL call was made. That last assertion matters because it proves the gate is checked before any backend interaction, not after.

   Failure Modes and What Worked or Failed

   What Worked

   The read/write separation paid off immediately. By the time we connected the MCP server to an LLM client, the read-only tools were already well-tested and predictable. There was no moment where we had to ask "could the model have modified something?" during early testing. That entire class of question was eliminated by the architecture.

   Variable capture in mocked tests caught normalization bugs early. By asserting on the actual GraphQL variables sent to the mock (not just the final response), we caught cases where country codes were not being resolved correctly and where limit capping was not applied before the query reached the backend. These bugs would have been invisible in a test that only checked output shape.

   The flat response types made LLM behavior more predictable. Converting nested GraphQL types (gqlCompanyModelV2 → companyModel → company → description.text) into flat structs (CompanySummary with a single description string) reduced the variation in how the model interpreted and presented results. When the structure is flat, there are fewer ways for the model to extract or misinterpret fields.

   What Failed or Required Redesign

   Removing create_collection from the active tool set was necessary. Unit tests against the mock passed cleanly, but manual validation against the real AppSync endpoint through MCP Inspector revealed a Lambda null-pointer error in the backend resolver. The tool was commented out of the registration path. This was a clear case where the MCP layer’s own tests were insufficient. Inspecting real backend behavior caught a failure that mocked tests could not. The lesson was that mocked unit tests verify tool logic, but they cannot substitute for validation against the real system. In our case, the error reproduced on every call we issued through MCP Inspector against our dev-team-a test stage, which is why we treated it as a real backend failure and removed the tool from registration rather than keep it behind the mutation flag while the issue was investigated.

   AI search rate limiting required upfront design for conversational patterns. The default rate limit of five requests per minute was chosen conservatively, but the tool was built with a configurable AISearchConfig from the start because we anticipated that multi-turn conversations, where the LLM client issues follow-up queries using thread continuity, would quickly hit a fixed limit. Making rate limits configurable per-environment before deployment avoided a situation where the first real usage would have required a code change to adjust. The specific choice of five per minute reflected the expected follow-up pattern in thread-continued conversations, where a user typically issues two to four refinement queries in a short burst while clarifying intent, so a ceiling slightly above that range allowed realistic multi-turn use without leaving headroom for a runaway LLM loop.

   A Scale-Related Design Constraint

   Broad queries against over one million profiles were bound from the start. On a dataset of this size, a query like "companies" with no country filter could return results spanning the entire database. Even with a hard limit of one hundred results at the tool level (the default was ten), the risk was that results would be so broad as to be useless, and that the LLM client might issue follow-up refinement queries that compounded the breadth. This risk shaped two design decisions made before deployment. First, the category-based filter system was built into search_companies so that country and other constraints could narrow queries before they reached the backend. Second, ai_search was given its own path with built-in rate limiting, so that natural language queries, which are harder to predict in scope, could be throttled independently. For example, an early bare {query: "companies"} call with no country or category constraint would match across the entire million plus profile set and return a near-random page of ten results. The bounded version surfaces the category-based filter system in the tool contract itself, so the LLM client is nudged toward supplying at least a location category before the request reaches AppSync.

   Logging and Operational Visibility

   Request logging was built into the design because the MCP server was treated as a real gateway to business data rather than an experiment. Once that interface exists, teams need visibility into what tools are being called, under what conditions, and with what outcomes. Without that visibility, it becomes difficult to tell whether tool boundaries are still appropriate or whether usage patterns are drifting toward unsafe behavior.

   Traditional backend teams already accept the need for logs, traces, and operational monitoring. LLM-related systems sometimes postpone that thinking because the work initially looks exploratory. That delay is costly. The earlier observability is built into the MCP layer, the easier it becomes to understand real usage, to tighten contracts, and to evaluate where broader access would be justified. It also improves collaboration across backend, platform, and product teams because architectural debates can be grounded in evidence rather than assumptions.

   On a platform serving more than one million company profiles, logging also becomes part of scale discipline rather than just incident response and helps distinguish between a useful narrow request and a tool pattern that is too broad, too repetitive, or too expensive to support safely through an LLM-facing interface.

   What Exists and What Should Be Built

   The current implementation uses Go’s structured slog package, writing to stderr (because stdout is reserved for the MCP JSON-RPC protocol). At startup, the server logs its configuration as structured fields:

   level=INFO msg="starting mcp-server" auth=oidc mutations=false tools=8 resources=2 prompts=2

   This startup log captures the authentication method in use, the mutation flag state, and the number of registered tools, enough to verify that the server started with the expected configuration. For example, seeing tools=8 instead of tools=9 immediately confirms that create_collection was not registered.

   Beyond startup, the current implementation does not log individual tool calls or request-level telemetry. What it does provide are typed error responses that carry diagnostic information back through the MCP protocol to the LLM client:

   
    GraphQL-level errors
     

     The GraphQL client propagates typed errors (UnauthorizedError, NotFoundError, RateLimitError, GraphQLError) that include the HTTP status and error messages.

    Rate limit errors
     

     When a rate limit is hit, the error message includes the limit configuration ("maximum 5 requests per 1m0s") so the cause is clear to the caller.

    Mutation gate errors
     

     When a mutation tool is called without --allow-mutations, the error message names both the problem and the fix ("mutations are disabled; use --allow-mutations flag to enable write operations").

   

   These error responses are useful for debugging, but they are not the same as operational telemetry. A production deployment would benefit from structured per-request logging that captures tool name, latency, input shape, outcome, and error type as independent log entries. That kind of observability was not part of the initial implementation, but it is the natural next step and it is easier to add when the tool contracts are already narrow and the error types are already explicit.

   Practical Recommendations

   Teams building MCP servers on top of cloud systems should start by assuming that the MCP layer is a first-class interface. So it is necessary to design narrow tools, separate read and write behavior early, and resist the temptation to optimize first for flexibility. If a tool feels too broad, it probably is.

   Use backend boundaries deliberately. In this implementation, AppSync and GraphQL provided a clean separation between the MCP server and the underlying system of record. That approach made the overall design easier to structure and easier to test.

   Make local validation part of the normal workflow. Use inspection tools and mocked clients to verify tool logic, then validate against the real backend before connecting the interface to a real LLM client. Finally, treat logging, auditability, and mutation controls as baseline requirements rather than hardening work to be added later.

   Conclusion

   MCP is valuable because it makes connecting LLM clients to systems that already matter easier. That is exactly why production teams should be careful with it. The core challenge is not only how to let a model call an API, but how to make that interface narrow, observable, testable, and safe enough for real workflows.

   In this case, the answer was not a single security feature or a prompt trick. It was a set of familiar engineering choices applied consistently: clear tool boundaries, blocked mutations by default, explicit authentication, local inspection, layered testing, and operational visibility. For teams moving from MCP demos to production-minded systems, those basics are still the most useful place to begin.
