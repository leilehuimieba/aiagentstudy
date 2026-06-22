# Cloudflare Introduces Flagship: an Edge-Native Feature Fl...

- BestBlogs URL: https://www.bestblogs.dev/en/article/e36d0437
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 3627
- Original publisher URL: https://www.infoq.com/news/2026/05/cloudflare-flagship-openfeature/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global

---

Cloudflare recently announced the closed beta of Flagship, a new feature flag service built directly into its global edge platform. The service lets teams control feature rollouts and experiment with changes without redeploying code, while evaluating flags locally in Cloudflare Workers rather than calling external flag services.

Built on OpenFeature, Flagship lets developers control feature visibility in their applications without redeploying code. Developers can define flags with targeting rules and percentage-based rollouts, and then evaluate them directly in their Workers via a native binding.

According to Cloudflare, the service built on the global edge platform removes network round-trip times and enables sub-millisecond evaluation at the edge. Rohan Mukherjee, system engineer at Cloudflare, and Abhishek Kankani, head of emerging technology and incubation at Cloudflare, write:

Flagship supports the patterns you'd expect from a feature flag service and the ones that become critical when AI-generated code is landing in production daily. Flag values can be boolean, strings, numbers, or full JSON objects — useful for configuration blocks, UI theme definitions, or routing users to different API versions without maintaining separate code paths.

Source: Cloudflare blog

OpenFeature is a CNCF open standard that provides a vendor-neutral API for feature flagging, allowing applications to integrate with different flag management systems without changing application code. Pete Hodgson, head of technology at Tribe AI, comments on LinkedIn:

Welcome to the OpenFeature party, Cloudflare! (...) More validation that delivery platforms powered by open standards are a win for the platform vendor, a win for their customers, and a win for the industry overall. Less vendor lock-in, less wasted effort re-implementing common features, and more opportunity for deep extensions from the community.

Announced during the Cloudflare Agent Week, Flagship supports targeting rules and gradual rollouts, and aligns with the OpenFeature standard, positioning it as a native alternative to third-party feature flag platforms for applications already running on Cloudflare, particularly those operating AI-driven or agent-based workloads that require low latency and rapid iteration.

Each flag can include multiple rules, evaluated in order of priority: the first matching rule determines the variation, and the rule may include conditions and an optional percentage rollout. Mukherjee and Kankani explain how flag rollout works:

Unlike gradual deployments, which split traffic between different uploaded versions of your Worker, feature flags let you roll out behavior by percentage within a single version that is serving 100% of traffic. Any rule can include a percentage rollout. Instead of serving a variation to everyone who matches the conditions, you serve it to a percentage of them.

On Reddit, many highlighted the zero-latency edge evaluation as the main benefit, with the native integration with Workers reducing operational overhead compared to external feature flag services such as LaunchDarkly and Split.io. User thejord_it comments:

Feature flags are becoming commoditized infrastructure, like caching or logging. Cloudflare, Vercel (with Edge Config), and eventually AWS will all have native flag evaluation. The "feature flag as a $100K/year SaaS" era is ending.

Cloudflare has also made available a browser client provider that prefetches selected flags, caches them with a configurable TTL, and evaluates them synchronously from the local cache. Flagship is currently available in closed beta.
