# BB-2026-05-01-237 Summary

## Article

- Title: A Detailed Breakdown of the Evolution of 17 Agent Architectures for Building LLMs from Scratch
- Source: BestBlogs / 腾讯技术工程
- URL: https://www.bestblogs.dev/article/4ab3a76d
- Date: 05-18
- Topic: `03-control-loop`
- Tags: Agent Architecture, Control Flow Design, agno, LangGraph, Multi-Agent System

## Model Mapping

- Blocks: Goal, Control Loop, Tools/Actions, Evaluation
- Layer: captured frontier material, pending deep reading

## Core Takeaway

Based on the all-agentic-architectures project, this article reimplements 17 Agent architecture patterns using the agno framework. The author's core argument is that the essence of Agent architecture is not prompt engineering or framework DSLs, but control flow design. The article starts with single-shot generation (Reflection), progressively introducing architectures such as Tool Use, the Observe-Act cycle (ReAct), explicit Planning, verification-driven replanning (PEV), multi-agent collaboration, the Blackboard pattern, and the Meta-Controller. Each architecture is uniformly analyzed through six fixed questions (Problem to Solve, State, Topology, Router, Failure Mode, Upgrade Trigger) and comes with a complete agno code implementation. The article emphasizes that the core of architectural evolution is the gradual addition of control capabilities: state modeling, explicit control flow representation, local error truncation, side effect management, and system termination conditions.

## Reusable Principle

Tencent's engineering team delivers a structured breakdown of 17 Agent architecture patterns evolved from scratch, covering everything from single-step execution to multi-agent collaboration. Unlike high-level overviews, this piece focuses on engineering trade-offs, making it a practical reference for developers building LLM-powered systems.
