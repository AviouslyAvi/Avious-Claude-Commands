---
name: Avious-prompt-coach
description: Auto-triggers when the user's request is short, ambiguous, or missing critical context — e.g. vague nouns ("fix the thing", "make it better"), no stated goal/why, ambiguous referents, or "something like X" hedging. Asks 2–3 targeted clarifying questions via AskUserQuestion BEFORE doing any work. Skip when the prompt is already specific, when it's a simple read/lookup, when the user said "just do it" / "no questions" / "skip questions", for greetings, or for meta questions about Claude itself.
---

# Prompt Coach

Prevent wasted work from under-specified prompts: when the request is vague, ask before guessing; when it's specific, get out of the way. **Read [reference.md](reference.md) in this skill's directory for the trigger/skip signals, how to ask, question priorities, and what never to do — then follow it.**
