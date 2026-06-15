# Avious

Consolidated Claude Code plugin holding every Avious-prefixed slash command and skill.

## Slash commands (`/`)

- `/Avious-GPT-Polish` — polish prose with ChatGPT (Codex CLI) using brand voice rules from `~/voice/voice.md`.
- `/Avious-yt-transcript` — download a YouTube video's transcript with yt-dlp and save it as markdown.

## Skills (auto-trigger)

Cowork workspace routing:
- `Avious-handoff` — save current chat as a handoff file in the active Cowork workspace.
- `Avious-resume` — resume from a saved handoff file.
- `Avious-log` — save the current chat snippet to a room in the workspace.
- `Avious-close` — archive a completed handoff.
- `Avious-index` — re-read the `START_HERE.md` router.
- `Avious-scaffold` — bootstrap the three-layer routing structure in a workspace.
- `Avious-documentation` — create an `.md` guide and save it to one of three preset locations.
- `Avious-workspace-optimizer` — passively log workspace session usage via a cross-platform Stop hook, then run `/Avious-optimize-workspace` for a ranked punch list of routing fixes (rarely-used rooms, files to promote, stale handoffs, anti-patterns).
- `Avious-week` — summarize the current ISO week's auto-generated daily notes from the Learning Roadmap inline in chat (mid-week digest, nothing written to disk).

Prompt utilities:
- `Avious-refine-prompt` — rewrite a draft prompt using Anthropic's prompting best practices.
- `Avious-prompt-coach` — auto-trigger clarifying questions when a request is short or ambiguous.

Prose & research:
- `Avious-eli-canti` — rewrite technical or abstract explanations in Çanti's interest-based, metaphor-first language (no jargon).
- `Avious-simplify-response` — rewrite the previous response in plain, everyday language for a non-technical reader.
- `Avious-compare-and-save` — research and generate a structured side-by-side comparison of tools or services, then save it as markdown to the Obsidian vault.

## Install

This plugin lives at `~/Claude/Plugins/Avious/`. To enable it locally, add it to a marketplace (e.g. `~/.claude/plugins/marketplaces/local-desktop-app-uploads/`) or upload it through the Claude Desktop plugin uploader.
