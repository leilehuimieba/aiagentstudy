# BB-2026-05-01-387 Summary

## Article

- Title: DuckDB Quack: Client/Server Protocol over HTTP for Multi-User Analytics
- Source: BestBlogs / InfoQ
- URL: https://www.bestblogs.dev/article/66368033
- Date: 05-31
- Topic: `06-frontier-radar`
- Tags: DuckDB, Quack, Client/Server Protocol, Analytics Database, HTTP

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

DuckDB has announced Quack, a new remote protocol over HTTP that allows multiple DuckDB instances to connect to and work with the same database over a network, introducing client-server capabilities to a previously local and embedded database. Quack is designed to be simpler and faster than existing approaches like Arrow Flight SQL, claiming to move large datasets about 3.5× faster. It supports concurrent users, remote analytics, and production-style data services without switching to a heavier database system. The protocol uses DuckDB's native data format and can send a query and return results in a single network round trip for small queries. The Hacker News and Reddit communities responded positively, viewing it as a key step toward shared, multi-user analytics. DuckDB plans to integrate Quack with DuckLake and ship a production-ready release with DuckDB 2.0 later in 2026. The recently released DuckDB v1.5.3 supports Quack as an autoloadable core extension.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
