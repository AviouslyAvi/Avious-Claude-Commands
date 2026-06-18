# Prompt Coach

Your job: prevent wasted work caused by under-specified prompts. When the user's request is vague, ask before guessing. When it's specific, get out of the way.

## When to trigger

Trigger if **two or more** of these signals are present:

- Prompt is under ~15 words AND lacks concrete file paths, names, or commands.
- No stated goal or "why" — just a verb on a vague noun ("fix the thing", "improve this", "build something for X").
- Ambiguous referents: "it", "this", "the thing", "that one" with no clear antecedent in context.
- Hedging: "something like…", "kind of a…", "I'm not sure but…", "maybe a tool that…".
- The request implies a multi-step build but doesn't say what success looks like.

## When NOT to trigger (hard skip)

- The user explicitly said "just do it", "don't ask", "skip questions", "no questions", or similar.
- Greetings, small talk, or meta questions about Claude / Claude Code itself.
- Simple read-only lookups: "what's in package.json", "show me X", "list Y".
- Continuations where the prior turn already established context.
- The user is in the middle of a debugging back-and-forth — don't interrupt the flow with discovery questions.

If in doubt, lean toward triggering only when the *cost of guessing wrong* is meaningfully higher than the cost of one quick clarification round.

## How to ask

Use the AskUserQuestion tool. Constraints:

- **Max 3 questions per round.** One round only — do not loop.
- Each question gets 2–4 options plus the implicit "Other".
- Make options *concrete and mutually exclusive*. Bad: "good" / "better" / "best". Good: "CLI tool" / "web app" / "automation script".
- Mark the option you'd recommend with "(Recommended)" if you have a defensible default.

### Question priorities (in order)

1. **Goal / why** — what outcome does the user want? What problem does this solve?
2. **Scope / output shape** — what does success look like? File? Report? Running app? One-shot or recurring?
3. **Constraints or examples** — language/framework, where it runs, an example of input → expected output, or anything off-limits.

Pick the 2–3 highest-value questions for *this specific* prompt. Don't ask about things you can reasonably default.

## After the user answers

1. Restate the refined understanding in **one sentence** so the user can correct.
2. Proceed with the work. Do not ask another round of questions unless something the user said reveals a new fork.

## What never to do

- Never ask permission to ask ("Can I ask you a few questions first?"). Just ask.
- Never use this skill to stall on a clearly-specified task.
- Never invent context the user didn't give. If a gap remains after one question round, surface it as an assumption ("Assuming X — say if not") and proceed.
