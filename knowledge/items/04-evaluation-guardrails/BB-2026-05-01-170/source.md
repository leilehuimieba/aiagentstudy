# Source Evidence

- Title: Agent Infra Practice Review: How Kimi Built the Database Service Behind Its Agent
- BestBlogs URL: https://www.bestblogs.dev/en/article/70ea435c
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=Mzg5NTc0MjgwMw==&amp;mid=2247521814&amp;idx=1&amp;sn=49ceeed78a26438ade5d5b706623e88f&amp;scene=21#wechat_redirect
- Original link text: 如何做 AI Agent 喜欢的基础软件

## Captured Page Metadata

- Browser title: Agent Infra Practice Review: How Kimi Built the Database Service Behind Its Agent
- Description: This article, written by PingCAP co-founder and CTO Huang Dongxu, reviews the collaboration details of TiDB Cloud becoming the database provider for Kimi K2.6 Agent website building service. The article first points out that the core competition in the second half of the Agent era lies in stably and continuously delivering services, rather than model capabilities themselves. Kimi K2.6 targets general users, providing a full-process service from code generation to online hosting. Its core challenge lies in infrastructure costs under massive long-tail tenants. The article compares the architectural differences between traditional Serverless databases (such as Supabase, Neon) and TiDB Cloud: the former assigns real database instances to each Agent, with costs scaling linearly; the latter achieves extreme elasticity and cost control through a virtual database layer and underlying distributed KV storage. The article summarizes three core strategic decisions: minimizing the friction for Agents to use Infra tools (second-level creation), unifying the tech stack to improve the success rate of generated code, and achieving extremely low costs through architectural innovation. Finally, the author points out that "one agent, one sandbox, one storage, one database" has become a common paradigm for AI Agent teams.
- Date: 05-12

## Evidence Links Captured

- 如何做 AI Agent 喜欢的基础软件: https://mp.weixin.qq.com/s?__biz=Mzg5NTc0MjgwMw==&amp;mid=2247521814&amp;idx=1&amp;sn=49ceeed78a26438ade5d5b706623e88f&amp;scene=21#wechat_redirect
- 当我们在谈论 Agent Infra 时我们在谈论什么: https://mp.weixin.qq.com/s?__biz=MzI3MjI4Njk0Ng==&amp;mid=2247484665&amp;idx=1&amp;sn=b08ce859156089648bc12c4d3311353b&amp;scene=21#wechat_redirect
