# BB-2026-05-01-256 Summary

## Article

- Title: Building a Secure MCP Server on AWS for a Million-Company B2B Platform
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/fca204e7
- Date: 05-18
- Topic: `04-evaluation-guardrails`
- Tags: MCP, Model Context Protocol, AWS, Go, GraphQL

## Model Mapping

- Blocks: Evaluation, Guardrails, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article details the design and implementation of a secure MCP (Model Context Protocol) server on AWS, built to expose a B2B intelligence platform with over one million company profiles to LLM clients. The authors treat the MCP server as a first-class production interface, not a thin demo wrapper. Key architectural decisions include strict separation of read and write operations at the tool level, a default-deny approach to mutations enforced via a `--allow-mutations` flag, and the use of narrow, well-defined tool contracts with bounded input and output structures. The server, built in Go, uses GraphQL on AWS AppSync as its backend and authenticates via short-lived OIDC tokens. The article also covers a comprehensive testing strategy combining mocked unit tests with real-system validation through MCP Inspector, which uncovered a critical backend Lambda null-pointer error that unit tests missed. The authors argue that for production systems, tool contracts, validation layers, and operational controls matter more than the protocol itself.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
