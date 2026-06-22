# BB-2026-05-01-542 Summary

## Article

- Title: Mastra vs LangChain: Building an AI Agent Pipeline and Analyzing the Data
- Source: BestBlogs / freeCodeCamp
- URL: https://www.bestblogs.dev/article/704aa9a4
- Date: 06-13
- Topic: `01-context-memory`
- Tags: AI Agent, LLM, AI Coding, LangChain, Mastra

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author, having shipped a production AI platform on Mastra, builds the same five-step research and synthesis pipeline (Research, Analysis, Write, Critic, Loop) in both Mastra and LangChain/LangGraph to compare them empirically. The article details the architectural differences: Mastra's typed step contracts and `.dowhile()` loop vs. LangGraph's directed graph with shared state and conditional edges. It covers practical implementation details like tool creation, agent configuration, token capture, retry wrappers, and a critical fix for the 'LLM-as-judge' bias that gave everything a 7/10. The solution, inspired by the G-Eval paper, involves a structured critic with a claim audit, specificity audit, counterfactual check, and a floor rule. The project includes a real-time dashboard built with Convex and Next.js for live comparison. The article concludes with a data analysis showing LangChain is faster and more token-efficient, while Mastra offers better type safety and structured orchestration.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
