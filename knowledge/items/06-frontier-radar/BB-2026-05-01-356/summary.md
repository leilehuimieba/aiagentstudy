# BB-2026-05-01-356 Summary

## Article

- Title: Nearly 9x Training Acceleration: Residual Stream in DiT Becomes a Convergence Bottleneck
- Source: BestBlogs / 阿里技术
- URL: https://www.bestblogs.dev/article/316ae95e
- Date: 05-26
- Topic: `06-frontier-radar`
- Tags: Diffusion Transformer, DiT, Residual Stream, Cross-Layer Routing, Training Acceleration

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This paper, a collaboration between the LAMDA Lab at Nanjing University and the Alibaba Intelligent Engine Team, systematically analyzes the limitations of standard residual connections in Diffusion Transformers (DiT) within the context of diffusion models. The study finds that fixed-weight residual summation leads to hidden state explosion in deeper layers, gradient attenuation, and inter-layer redundancy, while failing to adapt to the varying information needs of different denoising stages. To address this, the paper proposes Diffusion-Adaptive Routing (DAR), which reframes the residual stream as a learnable, time-dynamic cross-layer information routing mechanism. DAR allows each layer to selectively aggregate information from the outputs of previous layers via softmax routing and introduces timestep awareness, enabling routing weights to adapt dynamically based on the noise stage. To control memory overhead, DAR adopts a chunked aggregation strategy, balancing historical information retention with computational efficiency. On ImageNet 256x256, DAR reduces the FID of SiT-XL/2 from 9.67 to 7.56 and achieves baseline convergence quality with approximately 8.75x fewer training iterations. When combined with REPA, it yields about 2x acceleration in the early training phase. Additionally, DAR demonstrates the ability to preserve high-frequency details in the post-training and distillation of Qwen-Image. This work redefines the residual stream from a default engineering detail to an architectural variable worthy of systematic study.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
