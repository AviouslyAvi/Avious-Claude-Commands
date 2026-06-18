---
name: Avious-week
description: |
  Summarize the current ISO week's auto-generated daily notes from the Learning Roadmap inline in chat. Reads files from 02-notes/auto/ matching the current ISO week and produces a mid-week digest without writing anything to disk. Trigger when the user types /week, says what have I been learning this week, weekly summary, what did I do this week so far, or any phrase asking for a mid-week recap of their learning log. Pairs with the nightly scheduled-tasks job that writes the daily auto-notes.
---

# Week — on-demand current-week summary

Read this week's daily auto-notes from the Learning Roadmap and synthesize them inline — read-only, no file writes. **Read [reference.md](reference.md) in this skill's directory for the full procedure (path, ISO-week computation, synthesis template) and when NOT to use it — then follow it.**
