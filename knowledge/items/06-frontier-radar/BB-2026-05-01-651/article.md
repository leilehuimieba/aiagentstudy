# Krea 2 Open Source: 12B DiT Text-to-Image Dual Versions + Nine Official LoRAs Released, Now Available on ModelScope AIGC Section

- BestBlogs URL: https://www.bestblogs.dev/article/18283f68
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=Mzk3NTc1NTU0Mw==&mid=2247510075&idx=1&sn=1e416a7bc1baed30263f0750e475ac02
- Source: BestBlogs / 魔搭ModelScope社区
- Publish time: 2026-06-26 18:55:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 7262

---

Krea 团队发布并开源了 Krea 2，一个面向"创意探索"的基础图像生成模型系列。Krea 2 在 Artificial Analysis 文生图榜单上位列全球前十、独立实验室第二。模型采用 12B 稠密 DiT 骨干、Qwen3-VL 文本编码器（多层特征聚合）以及 Qwen Image VAE。

   本次开源包含三类模型：

   
    
     Krea 2 Raw：未经过额外后训练与微调的基础检查点，用于微调、后训练与 LoRA 训练

    

    
     Krea 2 Turbo：经过后训练、微调与蒸馏的 8 步检查点，可在消费级 GPU 上约 2 秒生成 2K 图像

    

    
     官方风格 LoRA 集：覆盖动漫、绘画、摄影、抽象等多种视觉方向，可直接挂载到 Krea 2 Turbo 做快速推理

    

   

   

   Raw 与 Turbo 的协同设计把"可微调"和"快速推理"解耦：在 Raw 上训练的 LoRA 设计上可直接迁移到 Turbo 推理。

   模型已上线魔搭 AIGC 专区，无需本地 GPU 即可直接在网页端调用 Krea 2 出图与训练 LoRA，开发者也可通过 DiffSynth-Studio 在本地完成推理与微调。

   开源地址：

   
    
     ModelScope：https://modelscope.cn/collections/krea/Krea-2

    

    
     GitHub：https://github.com/krea-ai/krea-2

    

    
     技术报告：https://www.krea.ai/blog/krea-2-technical-report

    

   

  

  
   
    
     
      
       
        
         
          
           01

          

          生图与多样化LoRA效果

         

        

       

      

     

    

   

   Krea 2 Turbo 在 8 步内可输出原生 2K 图像，覆盖摄影、插画、3D、抽象等多种风格。

   

   

   多样化 LoRA 效果

   Krea 团队在发布主权重的同时，公开了一批官方风格 LoRA，覆盖动漫、绘画、摄影、抽象等多种视觉方向，可直接挂载到 Krea 2 Turbo 上做快速推理。当前已发布的官方 LoRA 包括：

   
    
     Krea-2-LoRA-retroanime：复古日式动画

     

    

    
     Krea-2-LoRA-vintagetarot：复古塔罗牌风格

     

    

    
     Krea-2-LoRA-sunsetblur：黄昏柔焦摄影

     

    

    
     Krea-2-LoRA-rainywindow：雨天窗景质感

     

    

    
     Krea-2-LoRA-neondrip：霓虹流动色彩

     

    

    
     Krea-2-LoRA-dotmatrix：点阵打印质感

     

    

    
     Krea-2-LoRA-darkbrush：高对比深色笔触

     

    

    
     Krea-2-LoRA-kidsdrawing：儿童手绘风格

     

    

    
     Krea-2-LoRA-softwatercolor：柔和水彩

    

   

  

  
   
    
     
      
       
        
         
          
           
            02

           

           技术解读

          

         

        

       

      

     

    

   

   Krea 2 借鉴 LLM 的多阶段训练范式：预训练 → 中训练（midtraining）→ 监督微调（SFT）→ 偏好优化（PO）→ 强化学习（RL），最后接一个可选的时间步蒸馏阶段产出 Turbo，每个阶段渐进式精修模型的输出分布。设计目标是同时具备广泛的审美多样性和强用户控制能力，避免行业普遍存在的"收敛到一组狭窄默认审美"。

   

   数据与描述

   预训练数据只过滤五类样本：重复样本、VLM 无法可靠描述的样本、诱发偏见或伪影的样本、低分辨率下难以可靠建模的高视觉复杂度样本，以及 AI 生成图像。报告明确指出预训练数据中不使用任何 AI 生成图像，团队训练了专门的内部分类器过滤合成图。描述采用三段式：OCR 抽取可见文字 → 描述模型结合元数据生成长描述 → LLM 重写为多种长度与格式。预训练分 256px / 512px / 1024px 三阶段，前两阶段使用 8-bit 训练，相比 bf16 提速 15—20%。

   架构选型

   通过系统消融实验确定最终配置

   

   关键决策上，GQA 几乎不掉点但显著降低计算开销；per-block MLP 调制占据 20—30% 参数，替换为可学习 bias 后将预算让给 attention 与 MLP；Qwen3-VL 借鉴 Unifusion 用浅注意力跨层聚合 VLM 特征并叠加轻量双向 transformer 层降低自回归偏置；DC-AE 因重建误差上限被舍弃，最终采用 Qwen Image VAE 与 FLUX 2 VAE。256px 第一个 epoch 开启 iREPA 正则加速早期收敛。

   

   后训练

   PO 阶段 Krea 团队发现 DPO 在不同偏好集上会出现"赢负样本概率都下降"的政策漂移并在后期产生高频伪影，为此设计 STPO 变体，加入辅助 loss 抑制漂移。RL 阶段使用 GRPO 风格的多奖励训练，奖励模型包括通用美学、指令跟随、文字渲染、伪影与结构四项；指令跟随采用 prompt-specific rubric reward 将 prompt 拆成可验证细粒度要求；伪影奖励单独训练以识别多指、变形肢体、文字扭曲等结构错误，防止只刷美学分。RL 整阶段关闭 CFG，让 rollout 与训练分布对齐。

   Turbo 蒸馏

   团队比较 DMD、DMD2、Decoupled DMD、piFlow、APT 后选择 Trajectory Distribution Matching (TDM)，原因是 TDM 调参简单、data-free，且天然支持灵活多步蒸馏，与"灵活多步学生"目标契合。

   配套系统

   Prompt Expander 先 SFT 把短 prompt 映射到模型友好的长描述，再用 GDPO 在生成端做 RL，加入 DINOv3 嵌入多样性奖励抑制 diversity collapse；Style Reference 用自监督方式训练，支持多风格语义混合与连续强度控制，重点解决风格图内容向最终图泄漏的问题。

   
    
     
      
       
        
         
          
           
            03

           

           在魔搭AIGC专区使用

          

         

        

       

      

     

    

   

   网页端推理

   魔搭 AIGC 专区已上线 Krea 2，无需本地 GPU 环境即可直接在网页端调用 Raw 与 Turbo 出图，支持调整推理步数、CFG、分辨率等关键参数，并可挂载魔搭社区上传的 LoRA 进行风格化生成。

   

   网页端训练

   魔搭 AIGC 专区同时提供 Krea 2 的免费在线训练通道，支持 LoRA 与全参数微调，覆盖数据上传、自动打标、参数配置到训练监控的完整流程。

   

   无影灵构付费训练入口

   无影灵构携手魔搭社区上线了"魔搭 AIGC 专区模型训练"镜像，由魔搭团队与无影灵构团队联合发布，训练体验与魔搭 AIGC 专区一致，但使用专属资源，训练不排队。从魔搭入口跳转至无影灵构的新用户可获得 400 灵豆，约 8 小时免费训练时长，足以在 Krea 2 Raw 上完成一次中等规模 LoRA 训练。

   

  

  
   
    
     
      
       
        
         
          
           
            04

           

           本地推理与训练

          

         

        

       

      

     

    

   

   模型推理

   DiffSynth-Studio 已对 Krea 2 做完整集成，开启显存管理后可在单张 24GB 显存的 GPU 上完成推理。

   安装：

   

   

   git clone https://github.com/modelscope/DiffSynth-Studio.git
cd DiffSynth-Studio
pip install -e .

   

   

   Krea 2 Raw 推理：

   

   

   from diffsynth.pipelines.krea2 import Krea2Pipeline, ModelConfig
import torch
vram_config = {
    "offload_dtype": "disk", "offload_device": "disk",
    "onload_dtype": torch.float8_e4m3fn, "onload_device": "cpu",
    "preparing_dtype": torch.float8_e4m3fn, "preparing_device": "cuda",
    "computation_dtype": torch.bfloat16, "computation_device": "cuda",
}
pipe = Krea2Pipeline.from_pretrained(
    torch_dtype=torch.bfloat16, device="cuda",
    model_configs=[
        ModelConfig(model_id="krea/Krea-2-Raw", origin_file_pattern="raw.safetensors", **vram_config),
        ModelConfig(model_id="Qwen/Qwen3-VL-4B-Instruct", origin_file_pattern="*.safetensors", **vram_config),
        ModelConfig(model_id="Qwen/Qwen-Image", origin_file_pattern="vae/diffusion_pytorch_model.safetensors", **vram_config),
    ],
    tokenizer_config=ModelConfig(model_id="Qwen/Qwen3-VL-4B-Instruct", origin_file_pattern=""),
    vram_limit=torch.cuda.mem_get_info("cuda")[1] / (1024 ** 3) - 1,
)
image = pipe("A cat standing on a stone.", seed=0, num_inference_steps=52, cfg_scale=4.5)
image.save("image.jpg")

   

   

   Krea 2 Turbo 推理：将 model_id 替换为 krea/Krea-2-Turbo，并将推理参数调整为 8 步、关闭 CFG。

   

   

   image = pipe("A cat standing on a stone.", seed=0, num_inference_steps=8, cfg_scale=1.0, mu=1.15)

   

   

   推理参数默认值：cfg_scale=3.5、num_inference_steps=52、height=width=1024（必须为 16 的倍数）。

  

  
   LoRA 训练

   DiffSynth-Studio 同时支持 Raw 与 Turbo 的全参数训练、LoRA 训练与对应验证脚本，示例位于 examples/krea2/。建议在 Raw 上训练 LoRA，再挂载到 Turbo 推理。

   下载示例数据集：

   

   

   modelscope download --dataset DiffSynth-Studio/diffsynth_example_dataset \
  --include "krea2/Krea-2-Raw/*" \
  --local_dir ./data/diffsynth_example_dataset

   

   

   启动 LoRA 训练：

   

   

   accelerate launch examples/krea2/model_training/train.py \
  --dataset_base_path data/diffsynth_example_dataset/krea2/Krea-2-Raw \
  --dataset_metadata_path data/diffsynth_example_dataset/krea2/Krea-2-Raw/metadata.csv \
  --max_pixels 1048576 \
  --dataset_repeat 50 \
  --model_id_with_origin_paths "krea/Krea-2-Raw:raw.safetensors,Qwen/Qwen3-VL-4B-Instruct:*.safetensors,Qwen/Qwen-Image:vae/diffusion_pytorch_model.safetensors" \
  --tokenizer_path "Qwen/Qwen3-VL-4B-Instruct:" \
  --learning_rate 1e-4 \
  --num_epochs 5 \
  --remove_prefix_in_ckpt "pipe.dit." \
  --output_path "./models/train/Krea-2-Raw_lora" \
  --lora_base_model "dit" \
  --lora_target_modules "wq,wk,wv,gate,wo,gate,up,down,first,tmlp.0,tmlp.2,projector,txtmlp.1,txtmlp.3,last.linear,tproj.1" \
  --lora_rank 32 \
  --use_gradient_checkpointing \
  --find_unused_parameters \
  --align_to_opensource_format

   

   

   LoRA 验证与推理（推荐挂载到 Turbo）：

   

   

   pipe.load_lora(pipe.dit, "models/train/Krea-2-Raw_lora/epoch-4.safetensors")
image = pipe("A dog", seed=0, num_inference_steps=8, cfg_scale=1.0, mu=1.15)
image.save("image.jpg")

   

   

   更多用法、低显存训练、Turbo 全参数训练等脚本详见：https://github.com/modelscope/DiffSynth-Studio/blob/main/docs/zh/Model_Details/Krea-2.md

   点击阅读原文，即可跳转模型合集~

   
    
    
     

     👇点击关注ModelScope公众号获取
更多技术信息~

     

    

   

  

  

  阅读原文
