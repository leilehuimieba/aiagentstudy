# BB-2026-05-01-567 Summary

## Article

- Title: Profiling in PyTorch (Part 2): From nn.Linear to a Fused MLP
- Source: BestBlogs / Hugging Face - Blog
- URL: https://www.bestblogs.dev/article/5a821792
- Date: 06-11
- Topic: `06-frontier-radar`
- Tags: PyTorch, GPU Profiling, Model Optimization, LLM, AI Engineering

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This is the second part of a series on PyTorch profiling. It builds on Part 1 by replacing a manual matmul-add with `nn.Linear`, then stacking three linears with a GeGLU activation to form an MLP. The article uses detailed profiler traces to explain several key concepts: how `nn.Linear` uses an epilogue to fold bias addition into the GEMM kernel (via `aten::addmm`), why `aten::t` (transpose) is a metadata-only operation with no GPU kernel, and how `torch.compile` removes CPU dispatch overhead (e.g., the transpose view chain) but cannot fuse a single GEMM. For the full MLP, it shows that eager mode launches 5 kernels (3 GEMMs, 1 GeLU, 1 mul), while `torch.compile` fuses the two pointwise ops into a single Triton kernel, reducing the count to 4. The article also explains why different GEMM tile sizes are selected by cuBLAS based on matrix shapes, and how to read kernel names to understand what the GPU is doing.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
