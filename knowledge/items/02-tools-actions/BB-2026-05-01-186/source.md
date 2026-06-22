# Source Evidence

- Title: How Pinterest Built a Production MCP Ecosystem
- BestBlogs URL: https://www.bestblogs.dev/en/article/dcf387de
- Original publisher URL: https://blog.bytebytego.com/p/how-pinterest-built-a-production
- Original link text: https://blog.bytebytego.com/p/how-pinterest-built-a-production

## Captured Page Metadata

- Browser title: How Pinterest Built a Production MCP Ecosystem
- Description: The article explores Pinterest's journey in adopting the Model Context Protocol (MCP) to connect AI agents with internal tools like Presto, Spark, and Airflow. It highlights that while MCP provides a standardized communication protocol, the real engineering effort lies in building the surrounding infrastructure. Pinterest made three key architectural bets: deploying cloud-hosted servers for consistent security, using many small domain-specific servers to manage access control and token consumption, and creating a unified deployment pipeline to reduce operational overhead. The security model features two layers of authorization: coarse-grained checks at the network edge via Envoy and fine-grained, tool-level checks using a decorator pattern. The ecosystem is integrated into existing engineer workflows, including an internal chat app, IDE plugins, and CLI agents. As of January 2025, the system handles 66,000 invocations per month, saving an estimated 7,000 hours. The article concludes that the protocol is necessary but insufficient; the platform work around it is what makes a production system viable.
- Date: 05-11

## Evidence Links Captured

- https://www.bestblogs.dev/en/article/dcf387de: https://www.bestblogs.dev/en/article/dcf387de
- https://blog.bytebytego.com/p/how-pinterest-built-a-production: https://blog.bytebytego.com/p/how-pinterest-built-a-production
- https://image.jido.dev/20260511164306_c0acd8c0-dcbb-4462-914c-207889b0bd28_2576x1520.png: https://image.jido.dev/20260511164306_c0acd8c0-dcbb-4462-914c-207889b0bd28_2576x1520.png
- https://image.jido.dev/20260511164306_333c5263-12c0-4e4d-9b13-8d19f9e97055_2474x1600.png: https://image.jido.dev/20260511164306_333c5263-12c0-4e4d-9b13-8d19f9e97055_2474x1600.png
- https://image.jido.dev/20260511164306_d0d5cf78-b1ae-46f3-91d5-e310ad8fa76b_2998x1678.png: https://image.jido.dev/20260511164306_d0d5cf78-b1ae-46f3-91d5-e310ad8fa76b_2998x1678.png
- https://image.jido.dev/20260511164306_bcdfc21a-411f-4eea-ab98-31984a2dbb80_3336x2010.png: https://image.jido.dev/20260511164306_bcdfc21a-411f-4eea-ab98-31984a2dbb80_3336x2010.png
- https://image.jido.dev/20260511164306_33838bcb-4b89-4899-a9fa-192e8920a4f9_2498x1416.png: https://image.jido.dev/20260511164306_33838bcb-4b89-4899-a9fa-192e8920a4f9_2498x1416.png
- https://image.jido.dev/20260511164306_de99cc29-698e-4c6e-aeab-206f5ef376b4_1722x1246.png: https://image.jido.dev/20260511164306_de99cc29-698e-4c6e-aeab-206f5ef376b4_1722x1246.png
- https://image.jido.dev/20260511164306_248d1662-1ada-4da5-8cec-441567c2a9e3_2310x1236.png: https://image.jido.dev/20260511164306_248d1662-1ada-4da5-8cec-441567c2a9e3_2310x1236.png
- https://medium.com/pinterest-engineering/building-an-mcp-ecosystem-at-pinterest-d881eb4c16f1: https://medium.com/pinterest-engineering/building-an-mcp-ecosystem-at-pinterest-d881eb4c16f1
- https://www.anthropic.com/news/model-context-protocol: https://www.anthropic.com/news/model-context-protocol
