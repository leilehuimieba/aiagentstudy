# We Open-Sourced MiniMax M3

- BestBlogs URL: https://www.bestblogs.dev/article/cecfce08
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzE5MTA3NzcxMQ==&mid=2247488831&idx=1&sn=9dedbe83e4ba0b27e3853808e1a8dbbb
- Source: BestBlogs / MiniMax 稀宇科技
- Publish time: 2026-06-15 22:40:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 3; page/content captured from BestBlogs resource APIs
- Extracted chars: 1711

---

我们在上周五开源了 MiniMax M3 模型权重，同步发布了 MSA（MiniMax Sparse Attention）技术论文。MSA 的架构设计让 M3 在长上下文下的计算成本大幅降低，论文中完整披露了架构与工程实现细节。

  M3 是 MiniMax 的原生多模态旗舰模型，总参数 428B，激活参数 23B。M3 是第一个从 Step 0 开始做多模态混合训练的开源模型。

  训练阶段，我们使用了大量文本、图像和其他模态交错排列的数据，让不同模态的语义空间从预训练阶段就深度融合。这种设计使模型在预训练阶段就建立起统一的跨模态语义空间，也为后续多模态理解、生成和复杂任务融合提供了底层基础。

  发布两周以来，M3 在 Artificial Analysis 综合智能指数排行榜上取得了全球开源模型的最高排名，也收到了来自开发者、研究者和行业用户的大量实测反馈。

  
   
    
     
      
       

      

      
       Vercel CEO Guillermo Rauch 给予 M3 积极评价

      

      
       

      

      
       YC Founder Jinjing Liang 分享 M3 实测体验

      

      
       

      

      
       Happycapy Co-founder Victoria Wu 实测评价

      

      
       

      

      
       Artificial Analysis 综合智能指数开源模型第一

      

      
       

      

      
       GDPval-AA 排行榜开源模型第一

      

      
       

      

      
       Code Arena WebDev 榜单

       跻身帕累托最优模型序列，提供最高性价比

      

      
       

      

      
       Vals.AI 榜单国产模型第一名

       在金融与 Coding 任务上表现亮眼

      

     

    

   

  

  （上下滑动浏览）

  针对访问量激增带来的体验问题，我们在持续优化，目前 M3 的输出速度已从上线时的约 30 TPS 提升至约 80 TPS，接下来还会继续提速 30-40%，模型响应将更加流畅。Token Plan 后台也上线了调用量看板，用户可以直观查看当前用量及剩余额度，方便大家合理规划用量与成本。

  我们听到了大家对模型的期待。在反馈中，最集中的诉求就是模型服务的稳定性、真实负载下持续可用、以及以合理成本规模化部署的可行性——

  随着大模型被广泛应用于生产级任务，许多企业与个人的工作流被 Agent 接管，AI 渗透率快速提升。同时其中有大量的长程复杂任务，有的任务 Agent 能够连续运行数小时甚至数天，Token 消耗随之急剧增长。相应地，越来越多团队开始在模型能力、使用成本与稳定性之间权衡，力求找到最契合自身业务场景的平衡点。

  M3 模型在研发初期便确立了方向：在确保模型能力在复杂推理、长文本、多模态等场景中足够智能的前提下，真正实现对开发者、用户和企业客户的普惠。

  在后续的模型迭代中，我们将持续坚守这一初心，更加开放、加速进步。

  开源地址：

  
   
    Github: github.com/MiniMax-AI/MiniMax-M3

    Hugging Face: huggingface.co/MiniMaxAI/MiniMax-M3

   

  

  MSA 论文：

  arxiv.org/abs/2606.13392

  Intelligence with Everyone.
