# BB-2026-05-01-682 Summary

## Article

- Title: British Columbia， Time Zones， and Postgres | Crunchy Data Blog
- Source: BestBlogs / Hacker News
- URL: https://www.bestblogs.dev/article/e4b2674d
- Date: 06-23
- Topic: `06-frontier-radar`
- Tags: Postgres, Time Zones, Database Schema, Engineering Practices, Data Migration

## Model Mapping

- Blocks: Model, Frontier Radar, Product Workflow
- Layer: captured frontier material, pending deep reading

## Core Takeaway

When British Columbia stopped observing standard time in March 2026, any PostgreSQL database using `timestamptz` columns for future appointments in the America/Vancouver timezone became vulnerable to hour-off errors. The article explains that `timestamptz` stores UTC at insert time and converts back to local time using the current `tzdata` rules at query time. If `tzdata` updates after the policy change, queries return different local times than what users originally entered. The author demonstrates the problem with a concrete example (a 10 AM appointment shifting to 11 AM) and then presents a three-column schema: a bare `timestamp` for local time, a `text` column for the IANA timezone, and a calculated `timestamptz` column for UTC. A trigger recomputes the UTC value on insert/update, and a simple `UPDATE` can recalculate all future rows after a `tzdata` update. The article also discusses RFC 9557, noting it explicitly avoids solving this problem, and outlines steps to recover if the `tzdata` package has already been upgraded. The author cautions against over-engineering—the dual-column pattern is justified only when local intent is authoritative.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
