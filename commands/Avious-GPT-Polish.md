---
description: Polish prose with ChatGPT (Codex CLI) using brand voice rules from ~/voice/voice.md
argument-hint: <file> [--inplace | --stdout] [--model <name>]
allowed-tools: Bash(polish-with-gpt:*), Read
---

Polish the file specified in `$ARGUMENTS` by running it through ChatGPT via the `polish-with-gpt` wrapper.

Steps:
1. Run: `polish-with-gpt $ARGUMENTS`
2. If no `--stdout` flag was passed, Read the resulting `.polished.*` file and show the user a brief diff-style summary of what changed (which sentences were tightened, which words swapped). Don't dump the full polished output — they can open the file.
3. If `--stdout` was passed, the polished prose printed to terminal output is the deliverable; just confirm it ran.

The wrapper uses ChatGPT Plus auth (no API cost) and loads brand voice from `~/voice/voice.md` by default, or `./voice.md` if it exists in the working directory. Default model: gpt-5.5 (auto-falls back to gpt-5.4 if unsupported on the account).

If `$ARGUMENTS` is empty, ask the user which file to polish.
