# Stragglers， Not Failures: How Adaptive Hedged Requests Reduce p99 Latency by 74 Percent

- BestBlogs URL: https://www.bestblogs.dev/article/999ebcec
- Original publisher URL: https://www.infoq.com/articles/adaptive-hedged-requests-p99-latency/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-05-28 17:00:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 23324

---

Key Takeaways

    
     Stragglers, requests that complete slowly rather than fail, are the primary driver of p99 latency in fan-out architectures and retries make them worse by adding load to already-struggling back-ends.

     In a fan-out architecture with one hundred downstream services where each has a one percent straggler rate, sixty-three percent of top-level requests will be delayed by at least one straggler, making individual service health metrics misleading for diagnosing system-level tail latency.

     Static hedge thresholds appear effective in benchmarks but break in production as latency distributions shift with load, deployments, and time of day, requiring continuous manual tuning that rarely happens in practice.

     DDSketch provides O(1), constant-memory quantile estimation, with relative-error guarantees (plus or minus one percent), making it suitable for real-time per-host latency tracking with approximately thirty-five nanoseconds of overhead per request.

     A token bucket budget that caps hedge rate at a configurable percentage of total traffic prevents the load-doubling spiral during genuine outages. Hedging automatically stops when every request is slow, allowing the service to degrade gracefully instead of amplifying the problem.

    

   

   This article grew out of a decade of observing the same pattern in large-scale microservice architectures, fan-out straggler accumulation driving p99 degradation while individual service dashboards showed green. The intervention that consistently worked became the basis for a reusable, zero-configuration implementation described here.

   Most cloud services look healthy in dashboards, where p50 is fast and p90 is acceptable. Then you look at p99 and something is wrong. The instinct is to reach for retries. It seems obvious: If a request is slow, retry it. But this instinct is misleading, because slow requests are not the same as failed requests and conflating the two leads to solutions that make things worse.

   This article walks through the distinction between stragglers and failures, why stragglers accumulate at scale in ways that are invisible to per-service monitoring and how to build an adaptive hedging mechanism that learns your service's latency distribution in real time, racing around slow requests instead of retrying them, while preventing load amplification during genuine outages.

   
   The approach is grounded in the paper "The Tail at Scale" (Dean and Barroso 2013) and uses DDSketch (Masson, Rim, and Lee 2019) for real-time quantile estimation. A reference implementation is available as an open-source Go library at GitHub.

   The results presented here come from a reproducible benchmark simulation: fifty thousand requests against a back-end modeled with lognormal base latency and a five percent straggler probability, parameters chosen to reflect realistic microservice behavior under moderate load. The library is not yet deployed in a production system, but the benchmark is a controlled reproduction of the tail latency pattern observed repeatedly at scale over the past decade. The full simulation is available on GitHub ([go run .]) for anyone who wants to validate or adapt it to their own parameters.

   A failure is a request that doesn't complete. A straggler is a request that completes, but slowly: a garbage collection (GC) pause on the back-end, a hot partition, and a kernel scheduling blip. From the caller's perspective, both damage p99. But they need fundamentally different solutions.

   Retries address failures by sending another request because the first one didn't finish. But if the first request is going to finish, just ten times slower than normal, retrying adds a second request to a back-end that's already under pressure. The back-end now has two requests in flight for the same logical operation and the retry itself may become a straggler, so p99 gets worse, not better.

   The right tool for stragglers is a hedged request: Send a backup while the primary is still in flight and use whichever responds first. The loser is cancelled. You're not waiting for a failure. You're racing around the slow one.

   The key distinction is that retries are reactive (they wait for failure, then resend), while hedges are proactive (they detect slowness and race a backup). For tail latency caused by stragglers rather than failures, hedging is the correct intervention.

   

   Figure.1. Stragglers vs. failure: two different problems. (Image source: created by author)

   Why Stragglers Accumulate at Scale

   The individual straggler rate often looks negligible: one percent slow responses per service. One percent is perfectly fine, until you consider fan-out. In a fan-out architecture, a single user request touches multiple downstream services. The p99 of the system isn't determined by any one service. It is determined by the slowest of all of them:

   P(at least one straggler) = 1 - (1 - p)^n

   With ten downstream calls at a one percent straggler rate, approximately 9.6 percent of top-level requests hit a straggler. When one hundred downstream calls are made, sixty-three percent of top-level requests hit a straggler.

   The majority of your top-level requests will be delayed by at least one straggler, even when each individual service looks perfectly healthy. This issue is why optimizing individual services often doesn't move p99 at the system level. The problem isn't any single service. It's the accumulation. This insight comes from Dean and Barroso's 2013 paper at Google, which remains one of the most practically useful things written about distributed systems latency.

   

   Figure 2. Fan-out amplification. Why individual health metrics lie. (Image source: created by author)

   The Tricky Part: When to Hedge

   Too early and you waste capacity. Too late and you get almost no benefit.

   A static threshold, say fifty milliseconds, looks great in a benchmark with a fixed latency distribution. Production is different. Latency shifts with load, deployments, GC tuning, and time of day. A fifty millisecond threshold that's perfect at 3 am becomes wildly conservative at peak traffic. The distribution shifts up and you're accepting slow responses you could have hedged. A ten millisecond threshold that works at peak becomes wildly aggressive at 3 am. You’re hedging normal requests and adding unnecessary load.

   This is the "know the answer before you configure it" problem. Static thresholds require you to continuously monitor per-service latency and reconfigure as conditions change across every target your client talks to. In practice, this problem rarely happens. The threshold is set once during initial deployment and gradually becomes stale.

   What's needed is a mechanism that learns the latency distribution from live traffic and fires hedges at the right point in the distribution regardless of where it happens to be.

   Preventing Load Amplification

   The obvious concern with hedging is that during a genuine outage (i.e., when the back-end is actually slow, not just occasionally producing stragglers), every request exceeds the hedge threshold. Without a safety valve, you would hedge everything and double back-end load at the worst possible moment.

   The solution is a token bucket budget. Limit the hedge rate to a configurable percentage of total traffic, ten percent, for example. The following formula captures the bucket refill rate:

   refill rate = estimatedRPS x budgetPercent / 100

   At normal operation with a five percent straggler rate, the budget never exhausts. Hedges fire when warranted. During an outage, every request is slow. At one thousand requests per second (RPS) with a ten percent budget, the bucket holds one hundred tokens and exhausts in approximately one second under full-outage conditions, stopping hedging automatically before it can double back-end load. The service degrades gracefully instead of spiraling.

   At a ten percent budget, you are adding at most ten percent extra requests to your back-end, not doubling them. That ten percent only fires when a request is already slow. Normal requests have no cost.

   The Adaptive Mechanism: DDSketch

   To hedge at the p90 of the actual current distribution, you need a real-time quantile estimate per target host, updated on every completed request, with bounded memory and O(1) cost.

   DDSketch (Masson, Rim, and Lee 2019) provides exactly this hedge. It is a streaming quantile sketch with relative-error guarantees: The returned quantile is always within plus or minus one percent of the true value. This point matters because alternatives like the t-digest construction algorithm use rank-error bounds that can be arbitrarily inaccurate at high percentiles, exactly the regime we care about for tail latency.

   DDSketch maps values to logarithmic buckets:

   bucket_index = ceil(ln(value) / ln(gamma))

   where gamma = (1 + alpha) / (1 - alpha) and alpha is the desired relative accuracy. Add is O(1). Memory is constant. The critical-path overhead is approximately thirty-five nanoseconds per request, negligible for any network call. DDSketch operates on positive values; zero-latency responses, which should not occur in practice for network calls, are excluded from the sketch.

   Adapting to Changing Conditions

   A single DDSketch accumulates observations indefinitely. If the back-end slows down for ten minutes and then recovers, the old slow observations remain in the sketch. The hedge threshold stays artificially high and continues firing hedges on requests that don't need them.

   The fix is a tumbling window, two sketches rotating at a fixed interval (thirty seconds, for example). Quantile queries merge both sketches. Because both sketches are merged on every query, the effective observation window spans between one and two rotation intervals, between thirty and sixty seconds at the default setting, giving more stable estimates than a hard-cutoff window while still aging out stale data. When conditions change, whether a deployment, a traffic spike, or a slow GC phase that resolves, the threshold follows the actual distribution as it moves. No manual intervention, no configuration update required.

   Window duration is a tunable trade-off. Shorter windows (ten to fifteen seconds) adapt faster to sudden distribution shifts, such as a deployment or a GC spike, but have fewer observations per window, which can make quantile estimates noisier at low request rates. Longer windows (sixty seconds or more) produce more stable estimates but lag behind distribution changes, potentially firing hedges on requests that no longer need them. The default thirty-second rotation is a reasonable starting point for services above roughly fifty RPS; for lower-traffic services, a longer window ensures the sketch has sufficient observations before they age out.

   

   Figure 3. DDSketch windowed rotation. (Image source: created by author)

   Putting It Together

   The full request flow works as follows:

   
    A request arrives and is dispatched to the target host.

    The DDSketch for that host is queried for the current p90 latency estimate.

    A timer is set for that duration.

    If the primary response arrives before the timer fires, it is returned directly. The sketch is updated with the observed latency. No hedge is needed.

    If the timer fires before the primary responds, check the token bucket. If a token is available, fire a hedge request to the same target using a child context derived from the caller's context.

    Whichever response, primary or hedge, arrives first is returned to the caller. The other is cancelled and its response body drained to release the connection back to the pool.

   

   Both the primary and hedge requests derive from the caller's context. Whichever arrives second is cancelled immediately and its connection released, preventing resource exhaustion regardless of hedge rate.

   

   Figure 4 Hedge: full request decision flow. (Image source: created by author)

   The reference implementation encodes this flow as an HTTP RoundTripper, making it a drop-in replacement for any existing transport with no changes to call sites.

   Zero Configuration. The Transport Learns Latency Automatically

   import "github.com/bhope/hedge"

client := &http.Client{
    Transport: hedge.New(http.DefaultTransport),
}
resp, err := client.Get("https://api.example.com/data")

   Tuned With Explicit Options and Observability

   var stats *hedge.Stats

client := &http.Client{
    Transport: hedge.New(http.DefaultTransport,
        hedge.WithPercentile(0.90),
        hedge.WithBudgetPercent(10),
        hedge.WithEstimatedRPS(1000),
        hedge.WithMinDelay(time.Millisecond),
        hedge.WithStats(&stats),
    ),
}

// After requests:
fmt.Printf("hedged=%d total=%d budget_exhausted=%d\n",
    stats.HedgedRequests.Load(),
    stats.TotalRequests.Load(),
    stats.BudgetExhausted.Load(),
)

   When one response wins, the loser's body is drained in a background goroutine up to one megabyte and the connection is released back to the pool, making cancellation safe at scale with no connection exhaustion even under high hedge rates. The transport wraps any existing http.RoundTripper. For gRPC, a UnaryClientInterceptor provides the same adaptive hedging with the same options.

   Hedging LLM Inference: TTFT vs. TTFB

   Adaptive hedging applies naturally to LLM inference, but with one important distinction from standard HTTP services. What constitutes a slow response is different.

   For a typical microservice, latency is measured from request to response. For a streaming LLM endpoint using chunked transfer or SSE, the HTTP response headers arrive almost immediately, often within one to two milliseconds, because the server sends a 200 OK status code as soon as it begins processing. The real cost is Time to First Token (TTFT), which is how long until the first byte of generated content actually arrives. That delay, driven by prefill computation, KV-cache state, and queue depth, is where stragglers live.

   A hedge transport calibrated on header arrival time gets entirely the wrong signal. In benchmarks, the sketch learns an approximate 1.6 millisecond threshold and fires a backup request on virtually every call, one hundred percent overhead, because nearly every request "looks slow" relative to the near-instant header. The hedge is racing on the wrong metric.

   The fix is straightforward but requires hooking into the response body read path rather than the header receipt. Hedge measures latency at the first body byte, not at header receipt, giving the DDSketch the correct signal for prefill-disaggregated architectures where headers and first tokens arrive tens to hundreds of milliseconds apart.

   The practical effect is significant. In a simulated streaming back-end (e.g., 50,000 requests, concurrency 20, lognormal cache-hit TTFT with mean = 15 ms, and stddev = 3 ms) with a twenty percent cache-miss rate modeled as a separate lognormal distribution (e.g., mean = 200 ms and stddev = 25 ms), representing prefill recomputation on a cold KV cache, as shown in the table below:

   End-to-end latency - gateway server (TTFH ~ TTFT, hedge fires while blocked on headers):

   
    
     
      Configuration
      p50
      p90
      p99
      Overhead
     

     
      No hedging
      5.1 ms
      26.3 ms
      28.1 ms
      0%
     

     
      TTFB-calibrated (wrong signal)
      2.6 ms
      13.1 ms
      14.2 ms
      ~100%
     

     
      TTFT-calibrated (hedge)
      4.9 ms
      12.3 ms
      14.0 ms
      17-19.8%
     

    
   

   Time to First Byte (TTFB)-calibrated hedging halves p90 but doubles back-end load and barely touches p99. TTFT-calibrated hedging achieves comparable tail improvement at roughly 19.8 percent overhead and only fires on the slow twenty percent, the actual cache misses, leaving normal requests untouched.

   This approach also makes hedge useful as a complementary observed signal alongside latency predictors in LLM serving infrastructure. Predictors provide a forward-looking estimate based on request characteristics; hedge provides a backward-looking empirical signal from recent per-host TTFT observations via DDSketch. The two are most valuable together: The predictor handles expected load patterns, hedge catches the cases where reality diverges from prediction, such as cache eviction, GC pauses, and noisy neighbors. Basically, the predictor handles load faster than any model can anticipate. The TTFT-calibrated transport is available in the same zero-configuration drop-in style.

   Related Work

   Hedged requests were first described in the paper "The Tail at Scale" (Dean and Barroso 2013), which proposed sending duplicate requests after a brief delay and using whichever responds first. The original paper suggested using a static delay based on the expected p95 or p99 latency.

   The remote procedure call framework, gRPC, has supported request hedging natively via hedgingPolicy in service config for several years. It works well in a pure gRPC environment but requires a static hedgingDelay configured upfront and updated manually when conditions change. It also lacks a budget mechanism to prevent load amplification.

   Netflix's Zuul proxy implements adaptive retries with backoff for its edge gateway, but focuses on failure-driven retries rather than straggler-driven hedging. The retry logic does not maintain per-host latency distributions. Envoy proxy supports request hedging as part of its retry policy, but again uses static timeout configuration rather than adaptive thresholds.

   The approach described here differs by combining three mechanisms, per-host adaptive thresholds via DDSketch (eliminating static configuration), windowed rotation for tracking distribution shifts, and a token bucket budget for safe degradation. The combination is what makes it practical for production without ongoing operational tuning.

   When NOT to Hedge

   Adaptive hedging is not appropriate for all workloads.

   Non-Idempotent Requests

   Hedging sends duplicate requests. If the operation has side effects (e.g., writes, charges, or state mutations), you will execute it twice. Only hedge idempotent operations, or ensure your back-end handles deduplication.

   Single Back-end Services

   Hedging races a backup against the primary. If both go to the same single instance, the hedge adds load to the same machine that's already slow. Hedging is most effective in load-balanced, multi-instance deployments.

   CPU-Bound Back-ends

   If the back-end is slow because it's compute-saturated, adding a hedge request makes saturation worse. Hedging works best when stragglers are caused by transient factors (GC pauses, network jitter, hot partitions) rather than sustained resource exhaustion.

   Very Low Traffic Services

   DDSketch needs observations to produce accurate quantile estimates. At very low request rates (less than one RPS), the sketch may not have enough data to distinguish stragglers from normal variance.

   Services Behind a Shared Rate Limit

   If the back-end enforces a global rate limit, such as a third-party API with a per-account request cap or a per-minute token quota, hedge requests consume that quota. A hedged call that races a backup against the primary may cause two billable or rate-counted requests where one was intended. This point is particularly relevant for LLM inference APIs, where many providers enforce per-account token-per-minute limits; a twenty percent hedge rate against a rate-limited endpoint could trigger throttling that would not have occurred otherwise.

   Benchmark Results

   Fifty thousand requests against a simulated back-end with lognormal base latency (i.e., the mean is five milliseconds and the standard deviation is two milliseconds) and a five percent straggler probability at a ten times multiplier is a realistic model of a cloud microservice under moderate load.

   Benchmark results: hedging strategies vs. no hedging across latency percentiles:

   
    
     
      Configuration
      p50
      p90
      p95
      p99
      p999
      Overhead
     

     
      No hedging
      5.1 ms
      9.0 ms
      18.8 ms
      65.0 ms
      103.8 ms
      0.0%
     

     
      Static 10 ms
      5.0 ms
      9.0 ms
      13.3 ms
      17.5 ms
      61.2 ms
      7.7%
     

     
      Static 50 ms
      5.0 ms
      9.0 ms
      16.5 ms
      54.9 ms
      59.7 ms
      2.1%
     

     
      Adaptive (hedge)
      5.0 ms
      8.9 ms
      12.3 ms
      17.3 ms
      63.5 ms
      8.9%
     

    
   

   With a drop from sixty-five milliseconds to 17.3 milliseconds, a seventy-four percent reduction, p99 matched the best possible hand-tuned static threshold with zero manual configuration. Essentially, p50 is unchanged and normal requests pay no cost.

   The static fifty millisecond threshold barely helped (p99 is still 54.9 milliseconds), because stragglers in this distribution sit well above fifty milliseconds and aren't caught in time. The static ten millisecond threshold matched adaptive performance here, but only because the benchmark's baseline latency happened to sit near ten milliseconds. Shift the distribution, as production inevitably does, and the static threshold becomes either too aggressive or too conservative.

   Conclusion

   Tail latency in distributed systems is a statistics problem, not a code problem. Stragglers accumulate across fan-out architectures in ways that are invisible to per-service monitoring and the standard response, retries, makes them worse.

   Adaptive hedged requests offer a different approach, which includes learning the latency distribution from live traffic using DDSketch, racing a backup around requests that are genuinely slow, and using a token bucket budget to prevent load amplification during outages. The result is a mechanism that matches hand-tuned static thresholds without requiring any manual configuration and, critically, stays accurate as distributions shift.

   The same mechanism extends naturally to LLM inference workloads by measuring true TTFT rather than header receipt time, making it applicable to the growing class of streaming AI back-ends where the standard latency signal is misleading.

   The reference implementation, bhope/hedge on GitHub, provides drop-in HTTP and gRPC support for Go services, with the full benchmark simulation and contribution guidelines available in the repository. The same mechanism extends naturally to LLM inference workloads, but only because the transport measures latency at the right point. By wrapping the response body and recording the sketch sample on the first successful read rather than at header receipt, the hedge timer races on first-token delivery rather than connection establishment. The latency signal has to match where the actual work happens.

   References

   
    Jeffrey Dean and Luiz Andre Barroso. "The Tail at Scale". Communications of the ACM, 56(2):74-80, 2013.

    Charles Masson, Jee E. Rim, and Homin K. Lee. "DDSketch: A Fast and Fully-Mergeable Quantile Sketch with Relative-Error Guarantees". PVLDB, 12(12):2195-2205, 2019.
