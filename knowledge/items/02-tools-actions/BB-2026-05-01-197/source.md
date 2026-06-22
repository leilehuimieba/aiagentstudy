# Source Evidence

- Title: Browser Run: now running on Cloudflare Containers， it’s faster and more scalable
- BestBlogs URL: https://www.bestblogs.dev/en/article/e8e66179
- Original publisher URL: https://blog.cloudflare.com/browser-run-containers/
- Original link text: https://blog.cloudflare.com/browser-run-containers/

## Captured Page Metadata

- Browser title: Browser Run: now running on Cloudflare Containers， it’s faster and more scalable
- Description: This article details Cloudflare's migration of its Browser Run service from shared infrastructure with Browser Isolation to its own Cloudflare Containers platform. The move was driven by the need to support rapidly growing demand, particularly from AI agent builders. Key technical challenges included managing global latency between Durable Objects and containers, which was solved by creating regional pools of pre-warmed containers. The most significant architectural change was migrating container state management from Workers KV to D1 and Queues, eliminating race conditions and enabling support for up to 500,000 containers per location through batched writes. The migration resulted in a 4x increase in concurrent browser limits (up to 120), a 50%+ reduction in Quick Action response times, and faster feature delivery, including WebGL and WebMCP support. The article serves as both a technical case study and a demonstration of Cloudflare's dogfooding philosophy.
- Date: 05-13

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/e8e66179: https://www.bestblogs.dev/en/article/e8e66179
- https://blog.cloudflare.com/browser-run-containers/: https://blog.cloudflare.com/browser-run-containers/
- https://developers.cloudflare.com/containers/: https://developers.cloudflare.com/containers/
- https://developers.cloudflare.com/browser-run/quick-actions/: https://developers.cloudflare.com/browser-run/quick-actions/
- https://developers.cloudflare.com/browser-run/: https://developers.cloudflare.com/browser-run/
- https://www.cloudflare.com/learning/access-management/what-is-browser-isolation/: https://www.cloudflare.com/learning/access-management/what-is-browser-isolation/
- https://blog.cloudflare.com/cloudflare-containers-coming-2025/: https://blog.cloudflare.com/cloudflare-containers-coming-2025/
- https://www.cloudflare.com/en-gb/the-net/top-of-mind-security/customer-zero/: https://www.cloudflare.com/en-gb/the-net/top-of-mind-security/customer-zero/
- https://developers.cloudflare.com/kv/: https://developers.cloudflare.com/kv/
- https://developers.cloudflare.com/changelog/post/2026-01-30-kv-reduced-minimum-cachettl/: https://developers.cloudflare.com/changelog/post/2026-01-30-kv-reduced-minimum-cachettl/
- https://developers.cloudflare.com/d1/: https://developers.cloudflare.com/d1/
- https://developers.cloudflare.com/d1/configuration/data-location/#available-location-hints: https://developers.cloudflare.com/d1/configuration/data-location/#available-location-hints
- https://developers.cloudflare.com/d1/platform/limits/#concurrency-and-throughput: https://developers.cloudflare.com/d1/platform/limits/#concurrency-and-throughput
- https://www.cloudflare.com/developer-platform/products/cloudflare-queues/: https://www.cloudflare.com/developer-platform/products/cloudflare-queues/
- https://developers.cloudflare.com/queues/configuration/batching-retries/#batching: https://developers.cloudflare.com/queues/configuration/batching-retries/#batching
- https://chromedevtools.github.io/devtools-protocol/: https://chromedevtools.github.io/devtools-protocol/
- https://developers.cloudflare.com/browser-run/quick-actions/crawl-endpoint/: https://developers.cloudflare.com/browser-run/quick-actions/crawl-endpoint/
- https://developers.cloudflare.com/browser-rendering/get-started/: https://developers.cloudflare.com/browser-rendering/get-started/
- https://developers.cloudflare.com/browser-rendering/rest-api/: https://developers.cloudflare.com/browser-rendering/rest-api/
- https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/: https://developers.cloudflare.com/browser-rendering/rest-api/crawl-endpoint/
- https://agents.cloudflare.com/: https://agents.cloudflare.com/
