# BB-2026-05-01-396 Summary

## Article

- Title: All Web, No CLI? How We Transformed StarAgent WebTerminal
- Source: BestBlogs / 阿里云开发者
- URL: https://www.bestblogs.dev/article/8720f502
- Date: 06-01
- Topic: `02-tools-actions`
- Tags: WebTerminal, CLI, Agent, Remote Troubleshooting, AI Programming

## Model Mapping

- Blocks: Tools/Actions, Control Loop, Deliverable
- Layer: captured frontier material, pending deep reading

## Core Takeaway

This article documents the author's complete practice of transforming Alibaba Cloud's StarAgent/Drogo WebTerminal into a CLI tool named 'wt'. The core idea is: WebTerminal continues to handle official authorization and connection links; the 'wt' CLI turns remote shell, file transfer, and interactive programs into callable capabilities; Skills turn troubleshooting experience into executable methods. The article details key technical implementations like wsh/wcp black-screen operations, session multiplexing design, command execution and output capture, file API calls, and the interactive debugging HTTP control plane. Through two acceptance cases—GPU hang analysis and Emacs + eshell + gdb coredump debugging—it demonstrates how an Agent can dynamically execute commands, observe results, and make decisions like an engineer. The article also discusses design trade-offs (why not connect directly via SSH, why not use built-in commands, why use HTTP interaction) and summarizes reusable engineering patterns: abstract the execution plane before solidifying scenarios, decouple authorization from execution, make outputs saveable, parseable, and reviewable, define Skill boundaries and methods, design interactive programs as state machines, and protocolize file transfer.

## Reusable Principle

Use the catalog and this summary as the low-token entry point; open `article.md` only when the full evidence or detailed argument is needed.
