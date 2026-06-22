# Source Evidence

- Title: Stop Manual Log Checking: Diagnose Bugs with AI + MCP in One Click
- BestBlogs URL: https://www.bestblogs.dev/en/article/3e018134
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzkzMjYzNjkzNw==&mid=2247636147&idx=1&sn=e6b40b0258db9e9c5fc5fd3eadd9d140
- Original link text: https://mp.weixin.qq.com/s?__biz=MzkzMjYzNjkzNw==&mid=2247636147&idx=1&sn=e6b40b0258db9e9c5fc5fd3eadd9d140

## Captured Page Metadata

- Browser title: Stop Manual Log Checking: Diagnose Bugs with AI + MCP in One Click
- Description: Based on the practical experience of the Dewu technology team, this article proposes an engineering solution for automating backend bug diagnosis using AI. The core idea is to encapsulate the fixed and time-consuming process of 'checking logs → extracting key information → scanning code → locating the problem' through the MCP (Model Context Protocol) and Claude Code's Skill mechanism. The article first explains the principles and configuration of the log platform MCP, allowing AI to obtain dynamic log data in real-time. It then focuses on the design of the /log-diagnosis Skill, including its complete execution chain (from traceId time estimation, paginated log retrieval, cross-service analysis to code localization), core capabilities (automatic token management, cross-service analysis, code linkage), and detailed installation and configuration steps. Through a real-world SQL bug case, the article demonstrates how AI automatically pulls logs, reconstructs the call chain, extracts SQL, and discovers a subtle bug caused by inconsistent field logic, ultimately locating the code and providing a fix. Finally, the article summarizes the key points for diagnosis efficiency and highlights the core idea: transforming an engineer's experience and workflow into reusable AI capabilities is the core competitiveness of engineers in the AI era.
- Date: 05-13

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/3e018134: https://www.bestblogs.dev/en/article/3e018134
- https://mp.weixin.qq.com/s?__biz=MzkzMjYzNjkzNw==&mid=2247636147&idx=1&sn=e6b40b0258db9e9c5fc5fd3eadd9d140: https://mp.weixin.qq.com/s?__biz=MzkzMjYzNjkzNw==&mid=2247636147&idx=1&sn=e6b40b0258db9e9c5fc5fd3eadd9d140
- https://{your-t1-aigw-domain}/api/v1/mcp/log-mcp/sse: https://{your-t1-aigw-domain}/api/v1/mcp/log-mcp/sse
- https://{your-pre-aigw-domain}/api/v1/mcp/log-mcp/sse: https://{your-pre-aigw-domain}/api/v1/mcp/log-mcp/sse
- https://{your-prd-aigw-domain}/api/v1/mcp/log-mcp/sse: https://{your-prd-aigw-domain}/api/v1/mcp/log-mcp/sse
- https://{your-oversea-aigw-domain}/api/v1/mcp/log-mcp/sse: https://{your-oversea-aigw-domain}/api/v1/mcp/log-mcp/sse
