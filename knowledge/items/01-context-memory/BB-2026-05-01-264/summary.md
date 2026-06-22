# BB-2026-05-01-264 Summary

## Article

- Title: Introducing the Ettin Reranker Family
- Source: BestBlogs / Hugging Face Blog
- URL: https://www.bestblogs.dev/article/a2de1250
- Date: 05-19
- Topic: `01-context-memory`
- Tags: Reranker, CrossEncoder, Sentence Transformers, Ettin, ModernBERT

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This blog post announces the release of six new Sentence Transformers CrossEncoder rerankers, ranging from 17M to 1B parameters, built on the Ettin ModernBERT encoder suite from Johns Hopkins University. The models are trained using a distillation recipe with pointwise MSE loss, distilling from the mixedbread-ai/mxbai-rerank-large-v2 teacher. The post provides a comprehensive overview including architecture details (ModernBERT backbone with unpadded attention, RoPE, GeGLU, and a 4-module classification head), usage examples with just 3 lines of code, and an end-to-end retrieve-then-rerank pipeline. Extensive benchmark results on MTEB(eng, v2) Retrieval and NanoBEIR show the models achieve state-of-the-art performance at their respective sizes, with the 1B model closely matching its 1.54B teacher. The 17M model beats the 33M ms-marco-MiniLM-L12-v2 by +0.051 NDCG@10 on MTEB, and the 32M model outperforms the 568M BAAI/bge-reranker-v2-m3 by +0.025. Speed benchmarks on H100 GPUs are also provided, along with recommendations for using Flash Attention 2 and bfloat16 for optimal throughput. All models are released under Apache 2.0 license.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
