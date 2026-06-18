## When to use (full description)

Passively logs Cowork workspace session usage and runs on-demand optimization passes on the three-layer routing structure. Use in three modes. **Install mode:** first time the skill runs in a scaffolded workspace, copy the cross-platform Stop hook into the workspace's `.claude/` so every future session auto-logs. Trigger on /Avious-optimize-workspace or any other mode below if the hook isn't installed yet. **Backfill mode:** at the end of any session (or when the user runs /Avious-handoff), enrich the most recent entry in `05-handoffs/.usage-log.jsonl` with a one-line summary and tags. Trigger on phrases like "log this session", "tag this session", "mark this as a breakthrough/stuck/scope-creep". **Optimize mode:** when the user invokes /Avious-optimize-workspace, read the usage log digest + room READMEs + START_HERE.md and return a ranked punch list of concrete edits (rarely-entered rooms, co-loaded files to promote, skills to register, stale handoffs, task→room mismatches, anti-patterns like orphaned sources / dead-end notes / re-research / room drift). Propose, never apply, until user confirms. Pass `--deep` for full audit, otherwise cap at 10 items. Works cross-platform (macOS, Linux, Windows) — uses Node, which ships with Claude Code.

# Workspace Optimizer

Cowork-workspace meta-skill that watches how you actually use the three-layer scaffold, then proposes concrete edits to keep it honest. Pairs with `/Avious-scaffold` (which creates the structure) and `/Avious-handoff` (which triggers backfill).

## Privacy note — READ BEFORE SHARING

`05-handoffs/.usage-log.jsonl` contains **workspace filenames, one-line task summaries, and tags** for every session run from this folder. It travels with the folder. Before zipping/syncing/sharing this workspace, decide whether to scrub or delete the log. The digest file (`.usage-log.digest.md`) has the same exposure.

## Three modes

### Mode 0 — Install (one-time per workspace)

Before either of the other modes can run, the workspace needs the Stop hook installed. Check `.claude/hooks/log-session.js` and `.claude/settings.json`. If either is missing:

1. Confirm the current workspace is scaffolded (has `05-handoffs/` and `START_HERE.md`). If not, suggest `/Avious-scaffold` first and stop.
2. Create `<workspace>/.claude/hooks/` if missing.
3. Copy `scripts/log-session.js` from this skill's directory to `<workspace>/.claude/hooks/log-session.js`.
4. If `<workspace>/.claude/settings.json` does not exist, copy `scripts/settings.template.json` there as `settings.json`. If it exists, **merge** — add the `Stop` hook entry without clobbering existing hooks/permissions/env. Use Read → Edit, not Write, when merging.
5. Tell the user: "Hook installed. Future sessions in this workspace will auto-log to `05-handoffs/.usage-log.jsonl`. Privacy: filenames and topics are recorded; scrub before sharing."

Skip this mode silently if the hook is already present and current.

### Mode 1 — Backfill (passive)

The Stop hook appends a mechanical entry per session (no LLM cost). Fields like `summary` and `tags` start `null`. This skill's job in backfill mode:

1. Read the last line of `05-handoffs/.usage-log.jsonl`.
2. If `summary` is `null`, write a single sentence (≤120 chars) describing what the session actually accomplished, using the *current* chat context — do not re-read files.
3. If the user named a tag ("breakthrough", "stuck", "scope-creep", "rabbit-hole", "blocked", "shipped"), add it to `tags`.
4. Rewrite that JSONL line in place (read all lines, replace last, write back).
5. **Every 50 entries**, regenerate `05-handoffs/.usage-log.digest.md` (see digest format below).
6. **Warn the user** when the log crosses ~2 MB or ~5000 entries — suggest archiving to `05-handoffs/.usage-log.<YYYY-MM>.jsonl` and starting fresh.

Trigger automatically at the tail of `/Avious-handoff`. Otherwise trigger when the user says things like:
- "log this session", "tag this as [X]", "mark this session [X]"
- "what did we do this session" (then offer to log it)

Never invent a summary if you genuinely don't know — leave it `null` and say so.

### Mode 2 — Optimize (on-demand)

Triggered by `/Avious-optimize-workspace` (optionally with `--deep`).

Procedure:

1. **Read inputs in this order, stop early when sufficient:**
   - `05-handoffs/.usage-log.digest.md` (always)
   - `START_HERE.md`
   - Each `<room>/README.md`
   - Raw `.usage-log.jsonl` *only if* `--deep` or digest insufficient. Read with `tail`/`grep` slices, not whole-file.

2. **Compute (cheaply, in head or with one-liners):**
   - Room enter frequency. Flag rooms entered in <5% of sessions over the digest window → merge/delete candidates.
   - File co-occurrence within sessions in the same room. Flag pairs/triples loaded together ≥3× → propose adding to that room's README "Files to load."
   - Skills frequently invoked in a room → propose adding to that room's "Skills to invoke" list.
   - Task→room mismatches: when a session's `topic` keywords don't match the room actually entered most → propose updating the Task→Room map in `START_HERE.md`.
   - Handoffs in `05-handoffs/active/` with mtime >30 days → propose archiving.

3. **Anti-pattern scan** (always include if found):
   - **Orphaned sources** — files in `01-sources/` (or equivalent input room) never referenced by anything in `02-notes/` / `03-syntheses/` (grep filenames).
   - **Dead-end notes** — files in `02-notes/` never referenced by `03-syntheses/`.
   - **Re-research** — sources with very similar filenames or duplicate URLs in frontmatter.
   - **Forgotten handoffs** — active handoffs >30 days old with no recent session referencing their topic.
   - **Room drift** — files whose content clearly belongs in a different room (e.g. polished output sitting in `02-notes/`).

4. **Output a ranked punch list** (default ≤10, `--deep` = no cap). Format:

   ```
   # Workspace Optimization — YYYY-MM-DD
   Window: last N sessions (from digest) + Y raw entries

   ## Punch list (ranked by impact)

   1. [merge-rooms] `04-archive/` entered in 2/87 sessions. Merge into `05-handoffs/archive/`?
      Edit: delete `04-archive/`, move contents, remove row from START_HERE.md Task→Room map.

   2. [promote-files] In `01-sources/`, `paper-A.pdf` + `paper-B.pdf` co-loaded 6 sessions.
      Edit: add "Frequent co-reads: paper-A.pdf + paper-B.pdf (compare-and-contrast cluster)" to 01-sources/README.md.

   3. [skill-registration] `astrology:natal-chart-reader` invoked 11× in `01-sources/`.
      Edit: add to 01-sources/README.md → Skills to invoke.

   ... (etc)

   ## Anti-patterns
   - [orphaned-source] `01-sources/old-podcast-transcript.md` never cited. Archive or delete?
   - [dead-end-note] `02-notes/sketch-2026-02.md` never rolled into synthesis. Promote or delete?
   - [stale-handoff] `05-handoffs/active/handoff-2026-03-01-X.md` — 75 days old, archive?
   ```

5. **Wait for user confirmation** before applying any edit. Then apply only the ones approved, one Edit at a time. Never batch-apply silently.

## Digest format (regenerated every 50 sessions)

`05-handoffs/.usage-log.digest.md`:

```markdown
# Usage digest — entries 1–50 (2026-04-01 → 2026-05-15)

## Room enter frequency
- 02-notes: 31 (62%)
- 01-sources: 24 (48%)
- 03-syntheses: 11 (22%)
- 00-foundation: 4 (8%)
- 05-handoffs: 9 (18%)

## Top files (by load count)
- 02-notes/foo.md — 14
- 01-sources/bar.pdf — 9
...

## Top skills invoked
- Avious-handoff — 9
- astrology:natal-chart-reader — 11
...

## Tag tallies
- breakthrough: 3, stuck: 5, scope-creep: 2, shipped: 6

## Co-occurrence clusters (files loaded together ≥3 sessions)
- {paper-A.pdf, paper-B.pdf}: 6
- ...

## Window summary
2-3 sentences describing the arc of these 50 sessions.
```

The optimizer always reads this digest first; only descends into raw `.jsonl` on `--deep` or when digest is missing/stale.

## JSONL schema (one line per session)

```json
{
  "v": 1,
  "ts": "2026-05-15T14:32:08Z",
  "session_id": "abc123",
  "duration_s": 1840,
  "rooms": ["02-notes", "01-sources"],
  "files_read": ["02-notes/foo.md", "01-sources/bar.pdf"],
  "files_written": ["02-notes/foo.md"],
  "skills": ["Avious-handoff"],
  "tool_counts": {"Read": 12, "Edit": 3, "Bash": 5, "Write": 1},
  "tokens": {"input": 48210, "output": 3920, "cache_read": 102400},
  "topic": "indexing how foo relates to bar",
  "summary": null,
  "tags": []
}
```

Field rules:
- `v` — schema version, currently `1`. Bump on breaking changes.
- `ts` — UTC ISO-8601.
- `rooms` — derived from unique top-level directory of every entry in `files_read ∪ files_written`. Top-level dirs that don't match the room pattern `^\d\d-` are dropped.
- `topic` — best-effort: first user message truncated to 80 chars, or the `/handoff` topic arg if present.
- `summary` / `tags` — backfilled by this skill; `null`/`[]` if no follow-up session.
- `tokens` — pulled from transcript if hook can parse them; zeros otherwise.

## Log management

- **Retention:** forever, but warn at >2 MB or >5000 lines. When the user accepts, rename to `.usage-log.<YYYY-MM>.jsonl` and start fresh; the optimizer reads the digest only, so old logs need not be loaded.
- **Digest cadence:** regenerate every 50 new entries. The optimizer can also force a regen via `/Avious-optimize-workspace --rebuild-digest`.
- **Atomicity:** the hook uses an `O_EXCL` lockfile (`.usage-log.jsonl.lock`) with a short retry window — works on macOS, Linux, and Windows. The skill, when rewriting the last line for summary backfill, uses the same lock pattern.

## Portability

Once installed, the skill's runtime artifacts live entirely under `<workspace>/.claude/`:
- `.claude/hooks/log-session.js` — Node, cross-platform
- `.claude/settings.json` — project-scoped Stop-hook registration
- `05-handoffs/.usage-log.jsonl` — the log itself
- `05-handoffs/.usage-log.digest.md` — the digest

Copy that set to any other scaffolded Cowork workspace and it works unchanged. No global config required, no hard-coded paths — everything resolves from `$CLAUDE_PROJECT_DIR`.
