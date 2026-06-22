# TogetherAI Open Sources OSCAR: Surpassing TurboQuant! 2-bit KV Cache Quantization for Real-World Serving

- BestBlogs URL: https://www.bestblogs.dev/article/66047258
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=Mzk3NTc1NTU0Mw==&mid=2247508580&idx=1&sn=c0318290e24f95a10445b639cd6208b3
- Source: BestBlogs / 魔搭ModelScope社区
- Publish time: 2026-05-25 17:14:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 8854

---

Together AI开源OSCAR，一种面向真实服务的2-bit KV Cache量化方案，通过注意力感知的旋转技术，在显著降低显存占用和提升推理吞吐的同时，保持了与BF16浮点精度相当的模型性能。

  
   
    
     

     00

引言

     

    

   

   长上下文推理的瓶颈正在从计算量转向显存。每生成一个新token，系统都要反复访问越来越长的历史Key和Value，上下文拉长、batch放大后，KV Cache同时吞掉显存容量和带宽。Together AI开源了OSCAR（Offline Spectral Covariance-Aware Rotation），一套面向长上下文serving的近2-bit KV Cache量化方案，核心思路是：不只追求还原K/V向量本身，而要保住attention真正消费这些KV的方式。已接入SGLang，可用于真实服务链路。在约2.28 effective bits per KV element下接近BF16精度，相比3-bit TurboQuant最高提升40.1分，decode最高约3倍加速，job-level throughput最高约7倍。

  

  
   Together AI开源完整的OSCAR方案： 

   
    
     代码仓库：端到端的校准、旋转矩阵拟合和评估流程，已接入SGLang serving路径 

    

    
     RotationZoo：为多个主流模型预计算的即插即用旋转矩阵（.pt文件），无需自行重新运行校准。

    

   

   目前覆盖Qwen3-4B-Thinking、Qwen3-8B、Qwen3-32B、GLM-4.7-FP8和MiniMax-M2.7

   开源地址：

   
    
     论文：https://arxiv.org/abs/2605.17757

    

    
     项目主页：https://oscar-quantize.github.io/

    

    
     代码：https://github.com/FutureMLS-Lab/OSCAR

    

    
     RotationZoo：https://modelscope.cn/models/togethercomputer/OSCAR-RotationZoo/summary

    

   

  

  
   
    
     

     01

从KV Cache 瓶颈说起

     

    

   

   如果历史KV能稳定压到2-bit，理论上历史缓存的存储开销可以接近缩小8倍。不过，低比特KV Cache真正困难的地方从来不是"能不能压"，而是压缩之后模型推理质量不能塌，系统实现也不能停留在离线实验脚本里。OSCAR的价值正是在这两个问题上同时给出了答案。

   2-bit INT只有4个离散等级，而KV activation里经常会出现少量幅值很大的outlier channel。一旦量化尺度被这些极端通道牵着走，大部分正常值就会挤在很窄的有效区间内，attention分布也随之偏移。普通Hadamard旋转可以把outlier打散，却没有区分模型在attention里真正使用的方向。

   OSCAR 的动机

  

  
   

   图 1：只用 K/V 重建误差判断低比特效果，容易看漏真正的误差传播

   图 1 把 naive INT2、Hadamard-only、clip-only 和 OSCAR 放在同一条误差链路里比较。它想说明的是，原始 K/V 的重建误差并不能充分预测最终生成质量。更直接影响模型表现的，是 attention-score KL、attention block output MSE，以及这些偏差继续传到后续 hidden state 后形成的误差。OSCAR 的优势并不只是让数值分布看起来更平滑，而是把量化噪声尽量推到 attention 相对不敏感的方向上。

   
    
     

     02

OSCAR的设计

     

    

   

   具体到 key，量化误差会通过 QKᵀ 进入 attention logits，所以 OSCAR 使用 query covariance，也就是 QᵀQ，来决定 key 的旋转目标。对于 value，误差会先被注意力权重加权，再进入 attention 输出，因此 OSCAR 采用 score-weighted value covariance，即 VᵀSᵀSV。离线校准时，系统用少量样本估计这些 attention-aware covariance，并为每一层、每一个 head 生成固定旋转矩阵和 clipping 阈值。

   最终旋转可以写成 R = U · Hadamard · bit-reversal。其中，U 用来对齐 attention 相关方向，Hadamard 负责把 outlier 能量摊开，bit-reversal 则让 INT2 分组更加均衡，避免某个 group 被少数通道主导。也就是说，OSCAR 不是简单地“加一个旋转”，而是把旋转、裁剪和分组都放进了 attention 质量这个目标函数里。

   更关键的是，OSCAR 并不是只在离线量化评测里报告分数。它已经进入 SGLang 的服务路径，在运行时维护一个三段式 token pool：

   
    BF16 sink (64 tokens) | INT2 history | BF16 recent (256 tokens)

   

   sink token 和 recent window 继续用 BF16 保存，用来保护 attention sink 与最近上下文；中间占比最大的历史段则保存为旋转后的 INT2。新 token 会先写入 recent window，随着解码向前推进，最老的 recent token 再由融合 Triton kernel 完成 rotate、clip、quantize 和 pack，并降级进入 INT2 history。存储上，每 4 个 2-bit 数值被打包进 1 个 byte。

   decode 阶段，OSCAR 在 GPU 上分别处理 BF16 段和 INT2 段：INT2 kernel 负责 unpack、scale/zero point 反量化以及浮点累加，BF16 kernel 处理 sink/recent，最后再通过 online softmax merge 合并两部分结果。由于它兼容 paged KV、radix prefix cache 和 SGLang 的 fused kernel pipeline，所以 OSCAR 面向的是可落地的企业级workload，而不是只展示论文苍白的error数据。

   

   图 2：OSCAR 从离线校准到在线推理的整体链路

   图 2 展示了这条 pipeline 的完整路径。左侧是校准阶段：系统从少量样本中估计 attention-aware rotation 和 clipping threshold，让 KV activation 在进入 INT2 之前更适合低比特表示。右侧是在线阶段：sink/recent 保留 BF16，中间最长的 history KV 进入旋转后的 INT2 cache，并在 SGLang paged KV 体系里完成真实 serving。换句话说，OSCAR 不是一个孤立量化技巧，而是一整套 2-bit KV Cache 服务方案。

   
    
     
      

      03

评估结果

      

     

    

   

   论文在 Qwen3-4B-Thinking、Qwen3-8B、Qwen3-32B 和 GLM-4.7-FP8 上做了测试，任务覆盖 GPQA、HumanEval、LiveCodeBench v6、AIME25 和 MATH500，32K的generation length，并且每个配置运行 5 次取平均。OSCAR 在 2.28 BPE 下，Qwen3-4B-Thinking 距离 BF16 只差 3.78 分，Qwen3-8B 距离 BF16 只差 1.42 分；到 Qwen3-32B 和 GLM-4.7-FP8 时，整体表现已经基本贴近 BF16。

   对照组的情况要残酷得多：QuaRot-INT2 和 naive INT2 在 reasoning / coding 任务上经常直接失效；TurboQuant 在全层 3-bit K/V、没有 mixed-precision 保护的公平设置下，小模型推理分数也有明显损失。论文还在 128K 长上下文下做了 RULER-NIAH 测试，OSCAR 在 Qwen3-8B 与 GLM-4.7-FP8 上都保持了更稳定的检索能力，说明 attention-aware rotation 不只适用于短 benchmark，也能缓解超长历史中 KV 误差逐步累积的问题。

   系统层面的收益同样直接。相较 BF16 history storage，OSCAR 可以把 KV Cache memory 压低约 8 倍；在 100k context、batch-size-1、full prefix-cache hit 的设置下，decode 最高约 3 倍加速；在大 batch 且显存预算固定时，job-level throughput 最高约 7 倍。prefix cache 命中率越高，更小的 KV footprint 就越能转化为并发吞吐，这对共享系统提示、多轮 Agent 和工具调用循环等长前缀复用场景很有意义。

   
    
     
      

      04

精度表现

      

     

    

   

   

   图 3：主结果表，多种 KV 量化方法在同一评测设置下对比

   

   图 4：AIME25 32K 生成场景下，OSCAR 与 KIVI / Kitty 的专项比较

   图 3 是论文的核心结果表，把 BF16、Saw-INT4、TurboQuant、QuaRot-INT2、Naive INT2 和 OSCAR 放在四个模型、五个任务上比较。BF16 作为精度上界；Saw-INT4 是 4-bit 强参考，BPE 为 4.25；TurboQuant 在这里采用无 mixed-precision 保护的全层 3-bit K/V，BPE 为 3.25；QuaRot-INT2 与 Naive INT2 则代表接近 2-bit 的旋转基线和朴素基线，BPE 约为 2.25；OSCAR 的运行预算为 2.28 BPE。

   这张表真正要看的不是某一个任务的波动，而是低比特方案能否跨模型稳定工作。以 Qwen3-4B-Thinking 为例，TurboQuant mean 为 31.74，QuaRot-INT2 只有 1.40，Naive INT2 为 0.00；OSCAR 达到 71.86，距离 BF16 只差 3.78，并且比 TurboQuant 高 40.1 分。在 Qwen3-8B 上，OSCAR mean 为 69.42，BF16 为 70.84，TurboQuant 为 56.88。到了 Qwen3-32B 和 GLM-4.7-FP8，OSCAR 与 BF16 基本持平。

   图 4 专门看 AIME25 这个高难数学推理任务，同时加入 KIVI-KV2、Kitty 和 OSCAR 的对比。由于 KIVI 和 Kitty 没有可直接用于 long context run 的 framework 支持，论文选取了它们唯一在 32K 下汇报的 AIME25 结果。在 Qwen3-8B 上，OSCAR 以 2.38 BPE 达到 66.67，几乎追平 BF16 的 66.00，并明显高于 KIVI-KV2 与 Kitty；在 Qwen3-32B 上，OSCAR 达到 74.00，略高于 BF16 的 72.59，也超过 Kitty 的 69.26。这说明 OSCAR 的优势不只体现在与 TurboQuant 的比较中，在现有 KV-cache 量化方法里，它也能以接近 2-bit 的预算守住困难数学推理能力。

   
    
     

     05

系统加速

     

    

   

   

   图 5：100k 长上下文下的 decode 加速与 batch throughput

   图 5 关注 100k 上下文时的系统性能。在 batch-size-1 且 full prefix-cache hit 的纯 decode 场景里，OSCAR 最高带来约 3 倍加速；当显存预算固定、batch size 继续增大时，INT2 history 让 KV footprint 明显下降，从而把 job-level throughput 推高到最多约 7 倍。它的含义很直白：OSCAR 不只是精度曲线好看，也确实减轻了显存和带宽压力。

   

   图 6：prefix cache 命中率提升后，吞吐前沿继续外移

   图 6 展示了 prefix-cache hit ratio 对端到端 serving throughput 的影响。横轴是单用户吞吐，纵轴是单 GPU 吞吐；从关闭 cache，到 normal cache，再到接近 100% warmup replay，吞吐前沿会逐步向外扩张。由于 OSCAR 保留标准 paged KV / prefix cache 抽象，共享系统提示、多轮 Agent、工具调用链路这类长前缀高复用场景可以直接吃到收益。

   还有一点值得注意：OSCAR 并没有通过“少数层保留高精度”来换分。很多低比特方法在部署时会把第一层、最后一层或若干敏感层保留在更高 bit，这会抬高平均 bit 数，也会让 kernel 和 cache layout 更复杂。OSCAR 的设置更接近真实服务：历史 KV 主体统一使用 INT2，只在 sink 和 recent 两个很小窗口保留 BF16。这让它更容易接进 paged cache、prefix cache 和批量调度。

   
    
     
      

      06

快速实践

      

     

    

   

  

  
   用OSCAR在SGLang上部署2-bit KV Cache推理

   1. 下载预计算旋转矩阵

   

   

   pip install modelscope
modelscope download --model zzz879978/OSCAR-RotationZoo \
    --include "Qwen3-8B/**" --local_dir ./oscar_rotations

   

   

   2. 启动SGLang推理服务

   克隆OSCAR仓库并配置环境后，使用预计算旋转矩阵启动服务：

   

   

   SGLANG_ENABLE_MIXED_KV_WINDOWS=1 \
SGLANG_OSCAR_ROTATION_MODE=oscar \
SGLANG_OSCAR_K_ROTATION_PATH=./oscar_rotations/Qwen3-8B/seq20000_prompt83_group128/k_rotation_qqt_r_h_pbr.pt \
SGLANG_OSCAR_V_ROTATION_PATH=./oscar_rotations/Qwen3-8B/seq20000_prompt83_group128/v_rotation_sst_r_h_pbr.pt \
SGLANG_OSCAR_K_CLIP_RATIO=0.96 \
SGLANG_OSCAR_V_CLIP_RATIO=0.92 \
SGLANG_OSCAR_ABSORB_V_ROTATION=1 \
SGLANG_MIXED_KV_PREFIX_TOKENS=64 \
SGLANG_MIXED_KV_RECENT_TOKENS=256 \
HADAMARD_ORDER=128 \
SGLANG_USE_MODELSCOPE=true python -m sglang.launch_server \
  --model-path Qwen/Qwen3-8B \
  --tensor-parallel-size 1 \
  --kv-cache-dtype int2 \
  --kv-cache-quant-group-size 128 \
  --trust-remote-code

   

   

   运行时KV Cache自动维护三段式token池：BF16 sink（64 tokens）+ INT2 history + BF16 recent（256 tokens），历史段统一使用INT2，兼容paged KV和prefix cache。

   3. 从头复现旋转矩阵（可选）

   如需在自定义校准集上拟合旋转矩阵：

   

   

   git clone https://github.com/FutureMLS-Lab/OSCAR.git
cd OSCAR
bash rotation/qwen3-8B/save_qkv_8b.sh        # 阶段1：转储Q/K/V激活值
bash rotation/qwen3-8B/compute_rotation.sh   # 阶段2：拟合注意力感知旋转矩阵

   

   

   目前RotationZoo已覆盖Qwen3-4B/8B/32B、GLM-4.7-FP8和MiniMax-M2.7，更多模型的旋转矩阵将持续更新。

   
    
     
      

      07

写在最后

      

     

    

   

   OSCAR的意义不只是在小模型或短上下文上跑出好分数。论文同时覆盖4B、8B、32B和GLM-4.7-FP8这类不同规模模型；既评估了数学、代码、知识问答等32K推理生成任务，也测试了128K RULER-NIAH长上下文检索。短任务里，它能贴近BF16；长上下文里，它也能让attention分布随历史增长保持更稳定。这说明attention-aware rotation不是只针对某个benchmark调参，而是在处理KV误差随上下文长度累积这个更根本的问题。

   从应用角度看，这对长上下文Agent特别重要。真实Agent往往包含很长的系统提示、工具说明、历史对话和检索内容，不同请求之间还会存在大量共享前缀。如果KV Cache全部用BF16，显存很快会成为天花板；如果直接上朴素INT2，推理链条又可能失真。OSCAR在二者之间给出了一种更系统的折中：长历史用INT2降容量和带宽，关键sink/recent用BF16保稳定，再让prefix cache复用共享前缀。

   TurboQuant仍然是很强的通用online vector quantization方法；OSCAR更专注于attention-aware的2-bit KV serving。两者并非只能二选一，目前OSCAR的attention-aware rotation已经在实现上与llyod-max codebook结合，把压缩率继续推向极限。OSCAR带来的关键启发是：2-bit KV Cache如果要真正上线，旋转不能只追求"有"，而要对准attention；同时，它也必须被放进真实serving系统里一起设计。

   关于团队

   OSCAR由Together AI研究团队开发。第一作者Zhongzhu Zhou是Together AI Senior Research Scientist，悉尼大学博士，研究方向涵盖高效机器学习系统、模型训练与推理的算法系统协同设计以及LLM压缩与量化。团队成员还包括Donglin Zhuang、Jisen Li、Ziyan Chen、Shuaiwen Leon Song、Ben Athiwaratkun和Xiaoxia Wu，分别来自Together AI、悉尼大学和伊利诺伊大学厄巴纳—香槟分校。

   Together AI创立于2022年6月，联合创始人包括苹果前高管Vipul Ved Prakash、斯坦福大模型研究中心主任Percy Liang、芝加哥大学副教授Ce Zhang以及FlashAttention作者Tri Dao。

   点击阅读原文，即可跳转模型链接~

   
    
     

    

   

   
  

  

  阅读原文
