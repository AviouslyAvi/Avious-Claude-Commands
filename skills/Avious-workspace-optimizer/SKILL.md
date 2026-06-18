---
name: Avious-workspace-optimizer
description: |
  Passively logs Cowork workspace session usage and runs on-demand optimization passes on the three-layer routing structure. Three modes: Install (copy the Stop hook into the workspace's .claude/ so sessions auto-log), Backfill (enrich the latest entry in 05-handoffs/.usage-log.jsonl with a summary + tags — "log this session", "tag as breakthrough/stuck/scope-creep"), Optimize (on /Avious-optimize-workspace, read the usage digest + room READMEs + START_HERE.md and return a ranked punch list of concrete edits). Propose, never apply, until confirmed. Cross-platform via Node.
---

# Workspace Optimizer

Cowork-workspace meta-skill that watches how you use the three-layer scaffold, then proposes edits. Pairs with `/Avious-scaffold` and `/Avious-handoff`. **Read [reference.md](reference.md) in this skill's directory for the full three-mode logic, privacy note, digest/JSONL schemas, and log management — then follow it.**
