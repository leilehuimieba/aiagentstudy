# BB-2026-05-01-520 Summary

## Article

- Title: AI Doesn't Lack Intelligence, It Lacks Discipline: My Harness Engineering Practice
- Source: BestBlogs / 阿里云开发者
- URL: https://www.bestblogs.dev/article/bab3a35d
- Date: 06-16
- Topic: `01-context-memory`
- Tags: AI Coding, AI Agent, Engineering Practice, LLM, Prompt Engineering

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article systematically introduces an AI coding engineering framework (harness) practiced internally at Alibaba Cloud by the author. The author first points out that the bottleneck in AI coding has shifted from model capability to process engineering. Models are smart enough but unstable, and stability must be provided by an external framework. The article details the five-layer architecture of the harness: a permanent entry layer (CLAUDE.md), an atomic rules layer (7 single-responsibility rules), a role Agent layer (dispatcher scheduling + three-role review + process execution), an on-demand context layer (context/), and an execution support layer (skills/commands/evals). The core design philosophy is to 'manage context like a budget,' combating AI's forgetfulness and uncertainty through responsibility isolation, externalized state, and gating mechanisms. The article also introduces an evaluation platform based on deterministic scoring (zero LLM calls), treating the harness itself as the test subject and quantitatively assessing each execution across 7 dimensions (process completeness, output quality, code correctness, efficiency, security compliance, iteration capability, interface acceptance). Finally, the author candidly discusses the system's boundaries and technical debt, and looks ahead to frontier directions like structured memory layers and code knowledge graphs. The entire article embodies a transferable mindset: any AI workflow with sufficient capability but unstable output can be engineered through layered constraints, externalized state, and deterministic scoring.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
