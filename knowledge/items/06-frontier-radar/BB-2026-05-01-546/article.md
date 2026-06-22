# Tencent Hunyuan AI Infra New Open Source: Comprehensive Upgrade of HPC-Ops Inference Core Operators

- BestBlogs URL: https://www.bestblogs.dev/article/f8d006eb
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzkwODU2OTQyNQ==&mid=2247497936&idx=1&sn=21a726b8e684ce2e341265a518ab0369
- Source: BestBlogs / 腾讯混元
- Publish time: 2026-06-11 16:35:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 6139

---

更低成本，更高效率，更强性能。

     腾讯混元 HPC-Ops 推理算子库迎来系统级升级，从单点算子进化为覆盖推理全链路的优化能力集合。多项指标全面超越业界主流基线，帮助开发者轻松搭建高吞吐、低时延的大模型推理服务。生产级实力，全面开源，即刻可用！

    

   

  

  
  HPC-Ops 是腾讯混元 AI Infra 团队开源并长期维护的一套工业级、高性能的大模型推理底层算子库。在首轮开源中，HPC-Ops 提供了 Attention、GroupGEMM等在内多个高性能算子，原生支持 BF16 与多种 FP8 量化方案，针对常见的主流推理硬件进行了深度优化。

  为了进一步满足推理系统对动态业务负载的适应性、核心模块对复杂精度和高性能融合算子的需求，HPC-Ops 推出全新更新开源升级，包含五大关键算子。本次升级在主流推理平台上，有效缓解了Attention长尾延迟、显存搬运开销、跨卡通信等实际工程瓶颈，多项性能指标显著优于现有的开源基线。

  

  图 1 HPC-Ops 核心算子升级示意图

  本次升级的主要亮点包括：

  Attention：针对真实负载下长短请求混排导致的计算不均、推理长尾问题，采用运行时动态负载调度方案，实测长文本最高加速2.95x，端到端QPM最高提升17%。

  Router GEMM：以双BF16  GEMM组合实现FP32级高精度计算，兼顾推理精度与GPU算力利用率。精度显著优于常规BF16/TF32方案，对比CuBLAS FP32最高提速3.22x。

  FusedMoE：构建MoE全模块流水线，整合多阶段流程、消除显存搬运与内核启动开销。相较vLLM、SGLang等主流框架，性能提升1.2x～1.6x。

  Fused AllReduce+Norm：深度融合跨GPU通信、残差叠加与归一化计算。对比NCCL、FlashInfer主流方案，性能实现1.04x～1.68x提速。

  Sampler：将解码阶段的采样计算（原本需要十多个操作算子）融合为2个CUDA Kernel，大幅减少调度、读写与同步冗余开销。相较vLLM提速4.0x～7.5x、较FlashInfer提速1.9x～4.7x，补齐推理末端短板。

  HPC-Ops 希望持续开放来自真实业务场景验证的高性能算子能力，为社区提供更贴近生产实践的推理算子优化参考，帮助开发者更高效地构建和优化大模型推理系统，欢迎大家参与开源共建！

  👉 HPC-Ops GitHub 项目地址：https://github.com/Tencent/hpc-ops

  
   
    
     核心算子更新详解

    

   

  

  随着大模型推理系统在业务侧的应用不断深入，推理优化面临的负载形态、精度要求和系统瓶颈也更加复杂。为了在真实复杂业务场景中进一步提升推理性能，HPC-Ops 本次更新围绕两大核心工程思想进行了全面升级：一、深度适配线上复杂负载（应对多精度计算与长短请求混排）；二、多算子联合优化。本次更新内容主要包含以下五大核心算子：

  Attention：动态调度负载均衡，根治推理长尾延迟

  线上推理存在请求长度实时波动、batch 内长短请求混杂等特征。对于均匀长度负载，传统静态 split-kv 已经可以稳定工作；但一旦进入长上下文混合负载，静态策略就需要在长序列吞吐和短序列开销之间做固定权衡：长序列需要更大的 split-kv 才能充分并行，短序列则只需要少量拆分，固定策略很难同时兼顾。针对此问题，HPC-Ops对 Attention调度机制完成全面升级，将传统固定任务划分模式，迭代为更适配动态业务的运行时动态调度方案。

  该方案先将所有推理请求按统一Tile粒度拆分，依据全局Tile总量均衡分配各CTA任务规模，再通过贪心装桶算法实现Tile任务极致均分，从源头杜绝计算单元负载失衡问题。在执行链路中，Task Assign 模块会在每次推理前生成专属任务映射表，各层Attention Kernel依据映射表精准领取并执行对应任务，最终由Combine Kernel统一合并split-kv计算结果，实现全流程负载均衡、高效协同运算。

  

  图 2 Attention动态调度示意图

  本能力由腾讯混元AI Infra团队与NVIDIA联合优化打磨，围绕动态负载建模、Tile粒度适配、CTA任务均衡策略完成多轮精细调优。目前该能力已同步适配HPC-Ops与FlashInfer仓库，可直接落地应用于线上真实推理场景。

  Router GEMM：双BF16重构FP32计算，兼顾高精度与高性能

  在MoE路由、稀疏Attention等模块中，普遍存在激活为BF16，权重为FP32的高精度GEMM计算。若将权重降精度参与计算，其精度难以满足MoE Router、Attention Score等数值敏感算子，会直接影响模型效果；若将激活升精度至 FP32 或 TF32，则需引入逐元素类型转换的额外带宽与算力开销，且纯FP32计算只能使用CUDA Core运算单元，硬件利用率受限。

  针对上述问题，HPC-Ops提出双BF16 GEMM组合模拟FP32精度的优化方案：离线阶段将 FP32 权重拆分为高位 BF16 与低位残差 BF16 两组张量，即W ≈ W_high + scale × W_low（缩放因子scale取 1/256，对齐BF16的8位尾数）。推理阶段执行两次 BF 16 GEMM 并做线性组合，激活值全程保持 BF16，无需类型转换，且两路矩阵乘均运行在 BF16 Tensor Core 上，算力利用率得以充分释放。

  更进一步，实现时我们将双路计算融合至单一 Kernel：输入数据仅搬运一次，通过双寄存器累加器分别缓存两路中间结果，Epilogue 阶段经一次FMA修正出高精度结果写出到显存，全程无中间结果的 HBM往返开销。

  

  图 3 Router gemm算子原理和设计架构图

  FusedMoE：全算子流水线重构，极致压缩推理开销

  HPC-Ops对MoE完整推理链路进行深度融合与执行逻辑重排，重构全新流水线架构，将路由与索引预处理、Gate-Up GEMM、激活量化、Down GEMM、Top-K 加权聚合五大核心阶段，整合为紧凑高效的一体化执行链路，彻底解决传统方案多阶段拆分带来的冗余开销问题。

  在路由与索引预处理阶段，采用共享内存分块统计，为每个专家预留连续显存输出区间，大幅降低大规模 Token 输入场景下的索引构建成本。在Gate-Up GEMM计算阶段，可直接通过路由索引读取原始输入数据，省去独立Gather数据搬运步骤；同时取消Warp Specialization，由同一Warp Group完成数据搬运与计算任务，将访存延迟掩盖逻辑从CTA内软件流水线，升级为跨CTA硬件调度，显著提升单SM可驻留线程块数量，最大化硬件资源利用率。

  推理过程中，激活量化结果按专家维度紧凑写入显存，保障 Down GEMM 无缝读取、高效计算，并在推理末端完成 Top-K 加权聚合。全流程通过 PDL 技术串联为无气泡执行链路，显著消除频繁Kernel启动带来的冗余开销。

  Fused AllReduce+Norm：通信计算深度融合，打通张量并行瓶颈

  针对张量并行场景下，通信、残差计算、归一化拆分执行导致的性能损耗，HPC-Ops 联合腾讯网络平台部，创新实现AllReduce通信、残差相加、RMSNorm归一化的全链路融合计算，封装为NVLink原生一体化操作：RMSNorm(AllReduce(x) + residual, weight)。双方围绕通信拓扑优化、P2P同步机制、计算与通信融合逻辑完成协同打磨，让原本分段执行的离散链路，实现一体化、高效率运行。

  该能力基于 CUDA 多播 (multimem) 与P2P点对点技术构建，原生支持 BF16 精度与单节点多GPU部署环境，采用Reduce-Scatter + All-Gather的 two-shot 高效执行策略。同时针对不同推理场景提供两套差异化实现方案，适配性更强：

  ➡️ 高吞吐版本（fuse_allreduce_rmsnorm_high_throughput）依托NVSwitch多播机制完成归约计算，适配大规模 Token 的 Prefill 预处理场景；

  ➡️ 低延迟版本（fuse_allreduce_rmsnorm_low_latency）基于Lamport P2P机制，通过PDL实现双Kernel重叠执行，适配小批量Token的Decode推理场景。

  Sampler：极致大算子融合，终结后处理性能瓶颈

  针对传统采样后处理多Kernel串联、流程碎片化、冗余开销大的问题，HPC-Ops推出 fused_sampler算子，重构大模型推理后处理逻辑。该算子将主流框架中十余个零碎 Kernel串联实现的重复惩罚、温度缩放、Top-K、Top-P、Softmax、随机采样的全流程能力，端到端融合为2个核心CUDA Kernel，并封装为单一算子。针对差异化业务场景提供更加精简专用内核，算子内可自动适配调度，最大化释放GPU算力潜力。

  本次优化的性能增益主要来自五大维度：

  1. 全流程内核融合，将采样场景全局词表大小的 GPU 加载次数压缩至 1 次，且计算访存充分掩盖；

  2. 在 GPU 内部闭环完成重复惩罚掩码计算，无需CPU-GPU数据拷贝，消除了重复惩罚阶段的最大开销；

  3. 采用细粒度并行策略，将单请求拆分至多线程块并行执行，小批次场景并发度提升，推理延迟大幅降低；

  4. 优化Top-K计算逻辑，当Max Top-K ≤64时，通过局部堆归并替代全局阈值扫描或拒绝采样，避免全词表重复读取，减少比较次数；

  5. 合并计算链路，将Top-K归约过程与Softmax最大/求和计算融合，进一步削减加载和计算开销。

  
   
    
     性能结果

    

   

  

  实验设置：以下性能数据均在CUDA13环境采集，PyTorch版本为Torch2.11.0+cu130。各算子按照对应线上典型规格、并行配置和精度格式进行单算子测试；图中 latency 均表示算子级耗时，数值越低代表性能越好。

  Attention：

  在 Decode 阶段，请求长度实时波动和 batch 内长短请求混排会带来明显的负载不均。基于真实场景数据，动态调度方案在单 batch 长文本场景下单算子最高加速 2.95x，在混合长度 batch 场景下加速 1.59x~1.76x；端到端服务压测中，QPM 最高提升 17%。该能力已同步适配 HPC-Ops 与 FlashInfer，可直接用于在线推理中的长尾延迟治理。

  

  图 4 Attention性能对比图

  Router GEMM：

  在 N=192、K=4096 的典型路由 GEMM 测试中，HPC-Ops Router GEMM 在 M=2~4096 范围内最大绝对误差不超过 0.00177；TF32(cuBLAS) 对应最大绝对误差最高约 0.06464，约为 HPC-Ops 的数十倍。性能方面，HPC-Ops 相比 FP32(cuBLAS) 在 M=512 处最高获得 3.22x 加速，在 M=4096 处仍保持 2.86x 加速；相比 TF32(cuBLAS) 也可获得最高约 1.78x 的性能收益，适合 MoE Router GEMM 等精度敏感场景。

  

  图 5 Router GEMM误差对比图

  

  图 6 Router GEMM性能对比图

  FusedMoE：

  基于DeepSeek-V3、Hy3 preview、Qwen3-235B等典型MoE模型实测，在per-tensor FP8配置下，HPC-Ops FusedMoE相比vLLM CUTLASS、vLLM Triton 和SGLang当前实现，TP=8/EP=1场景整体获得约1.5x~1.6x的性能收益，TP=1/EP=8 场景获得约1.2x~1.5x的性能收益，并保持输出精度一致。

  

  图 7 FusedMoE性能对比图

  Fused AllReduce+Norm：

  该融合算子测试覆盖了8~32k tokens的TP8张量并行场景。小token场景下，低延迟模式可将通信后处理链路压缩到约9~13us；大token场景下，高吞吐模式借助NVSwitch multicast能力获得更高带宽利用率。相比NCCL与FlashInfer同类路径，实测最高获得约1.68x的性能收益，有效缓解张量并行通信及后处理瓶颈。

  

  图 8 Fused AllReduce+Norm性能对比图

  Sampler：

  以下展示了三种Sampler方法基于两组真实业务参数在不同batch下的性能。简单的温度采样（Temperature Sampling）场景下，HPC-Ops Sampler 相比 vLLM/PyTorch 与 FlashInfer 平均提升约 5.2x、2.6x；启用了各种采样测量的完整采样（Full Sampling)场景下，相比 vLLM/PyTorch 与 FlashInfer 平均提升约 5.4x、2.6x。可以看出无论batch大小和场景复杂度，采样算子均有较大的性能收益。

  

  图 9 Sampler性能对比图

  
   
    
     结语

    

   

  

  从首轮开源聚焦单点高性能算子能力，到本轮实现推理全链路核心能力的系统性升级，HPC-Ops 已从单一高性能算子库，全面迭代进化为覆盖大模型推理全流程、兼顾精度与速度、适配规模化生产落地的系统级推理优化能力集合。

  本次所有优化能力，均沉淀于腾讯混元 AI Infra 团队长期的线上生产实践，深度适配真实、复杂的大规模推理业务场景，且全部正式开源、面向社区开放共享。

  未来，团队将持续深耕大模型推理底层核心技术，持续迭代优化 HPC-Ops 能力体系，助力全球研究者与工程团队以更低成本、更高效率搭建高吞吐、低时延的大模型推理服务，推动大模型推理系统性能边界不断突破。

  推荐阅读：

  1、 腾讯混元AI Infra核心技术重磅开源：推理吞吐提升30%

  2、清华联合混元斩获MLSys 2026 MoE模型推理优化竞赛冠军，NPU推理提速4.1倍
