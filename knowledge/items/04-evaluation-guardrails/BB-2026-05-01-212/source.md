# Source Evidence

- Title: Alibaba & Ant Group LoongSuite GenAI Observability Semantic Convention: From Unified Data Language to Large-Scale Implementation
- BestBlogs URL: https://www.bestblogs.dev/en/article/9dae62a9
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247509356&idx=1&sn=b4b26f0b4332fe031b751b750e935ebe
- Original link text: https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247509356&idx=1&sn=b4b26f0b4332fe031b751b750e935ebe

## Captured Page Metadata

- Browser title: Alibaba & Ant Group LoongSuite GenAI Observability Semantic Convention: From Unified Data Language to Large-Scale Implementation
- Description: This article details the LoongSuite GenAI Observability Semantic Convention jointly launched by Alibaba and Ant Group. It first explains the core value of OTel SemConv as a unified observability data language, highlighting its key role in standardizing data metrics, supporting performance, cost, quality, and security governance, and reducing integration costs. The article then focuses on three major enhancements LoongSuite brings to OTel GenAI semantics: First, the addition of Entry/Step Spans to address the issue of overly long Trace chains in Agent long-running tasks, enabling clear display of Agent execution trajectories by round. Second, the addition of Skill semantics to provide observability for the business function aggregation layer, solving pain points such as functional domain attribution, health metric statistics, and link confusion. Third, the addition of Token-level inference observability, which extends observability from the request level down to the Token granularity. By collecting the generation time, sub-stage processes, and candidate probability distribution for each Token, it achieves white-box observability of the inference engine. The article also introduces the accompanying GenAI Utils tool library, which uses a layered and decoupled architecture to encapsulate the complexity of the semantic convention into a simple API, significantly reducing the integration cost for instrumentation library developers. Finally, two real-world cases demonstrate the practical effectiveness of Token-level observability in locating slow Tokens and addressing irrelevant answer issues.
- Date: 05-12

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/9dae62a9: https://www.bestblogs.dev/en/article/9dae62a9
- https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247509356&idx=1&sn=b4b26f0b4332fe031b751b750e935ebe: https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247509356&idx=1&sn=b4b26f0b4332fe031b751b750e935ebe
- https://github.com/open-telemetry/semantic-conventions-genai/issues/86: https://github.com/open-telemetry/semantic-conventions-genai/issues/86
- https://github.com/alibaba/loongsuite-semantic-conventions-genai: https://github.com/alibaba/loongsuite-semantic-conventions-genai
- https://github.com/open-telemetry/semantic-conventions-genai: https://github.com/open-telemetry/semantic-conventions-genai
- https://pypi.org/project/loongsuite-util-genai/: https://pypi.org/project/loongsuite-util-genai/
- https://www.npmjs.com/package/@loongsuite/opentelemetry-util-genai: https://www.npmjs.com/package/@loongsuite/opentelemetry-util-genai
- https://github.com/alibaba/loongsuite-python-agent/blob/main/util/opentelemetry-util-genai/README-loongsuite.rst: https://github.com/alibaba/loongsuite-python-agent/blob/main/util/opentelemetry-util-genai/README-loongsuite.rst
