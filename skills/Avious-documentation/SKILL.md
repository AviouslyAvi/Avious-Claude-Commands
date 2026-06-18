---
name: Avious-documentation
description: Create an .md document/guide and save it to one of four preset locations (Fresh Obsidian Vault, People Documentation, Job Descriptions, or the Notion Documentation database). Use when the user asks to "save as md", "make a guide", "document this", or similar.
argument-hint: "[optional: destination hint and/or title]"
allowed-tools: Write, Bash, Read, AskUserQuestion, mcp__fd70a912-79e2-477b-aa60-4d0caa13609b__notion-create-pages, mcp__fd70a912-79e2-477b-aa60-4d0caa13609b__notion-fetch
---

Turn the current conversation (or `$ARGUMENTS`) into a polished `.md` guide and save it to the location the user selects. **Read [reference.md](reference.md) in this skill's directory for the preserve-don't-degrade principle, the four destinations, the workflow, and notes — then follow it.**
