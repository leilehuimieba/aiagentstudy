# BB-2026-05-01-692 Summary

## Article

- Title: Examining circuit boards from the Space Shuttle's I/O Processor
- Source: BestBlogs / Hacker News
- URL: https://www.bestblogs.dev/article/9d3bed21
- Date: 06-29
- Topic: `01-context-memory`
- Tags: Computer Architecture, Reverse Engineering, Space Shuttle, History of Computing, Microcode

## Model Mapping

- Blocks: Context/State, Memory, Tools/Actions
- Layer: captured frontier material, pending deep reading

## Core Takeaway

The author examines two physical circuit boards from the Space Shuttle's I/O Processor (IOP): a network interface board (MIA) and a PROM microcode board. The article explains the IOP's role as a multi-threaded barrel processor running 25 virtual processors with two distinct instruction sets (MSC and BCE), used to manage 24 network buses. It describes the Manchester encoding employed for robust serial data transmission, the analog circuitry in the hybrid module for signal conditioning, and the physical 'page' construction used in IBM's System/4 Pi avionics computers. The analysis includes historical context (Manchester Mark 1, Peter Kogge's work), detailed photos of the boards with annotations, and technical notes on TTL logic, shift registers, and microcode storage in fusible-link PROMs.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
