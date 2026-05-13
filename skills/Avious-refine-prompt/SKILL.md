---
name: Avious-refine-prompt
description: Use when the user invokes /refine-prompt or asks to "rewrite this prompt", "make this prompt better", "refine my prompt", "improve this prompt", or pastes a draft prompt and asks for feedback. Takes a draft prompt as input and returns a polished version that applies Anthropic's prompting best practices, plus a short list of assumptions made and 2–3 follow-up questions the user could answer to make it even stronger. Output is the prompt itself, ready to copy-paste — not an implementation of the prompt's task.
---

# Refine Prompt

Turn a rough draft prompt into a high-quality one. **You are not executing the prompt's task** — you are improving the prompt as an artifact the user will use elsewhere (with you in another session, with a different model, with a teammate, etc.).

## Input

The draft prompt comes from one of:

- The skill argument (text after `/refine-prompt`).
- The most recent user message that contains the draft (often quoted or in a code block).
- The conversation context if the user said "refine the prompt I just wrote."

If you genuinely can't locate a draft, ask for it once, briefly.

## Principles to apply

1. **Goal, not just task** — make the *why* explicit. What outcome, for whom, in what context.
2. **Context the model can't infer** — role, stack, constraints, what's been tried, what's off-limits.
3. **Admit uncertainty** — preserve the user's "I don't know if…" as a question for the model to resolve, not a guess to paper over.
4. **Examples** — if the user gave any input/output samples, keep them. If the task is structural (formatting, parsing, classification), suggest where examples would help via a `[TODO: add 1–2 examples of input → expected output]` placeholder.
5. **Output shape** — specify length, format, whether to include explanation, whether to ask vs. proceed.
6. **Iterate-friendly** — write the prompt so the user can extend it with "and also do X" rather than rewriting from scratch.
7. **Request thinking on hard tasks** — for non-trivial reasoning, add a line like "think through tradeoffs before recommending."

## Output structure (always this shape)

```
## Refined prompt

<fenced code block containing the rewritten prompt, ready to copy-paste>
```

```
## What I assumed

- <bullet> — assumption I made because the draft didn't say. User should correct if wrong.
- <bullet>
```

```
## Questions to tighten further

1. <question whose answer would meaningfully improve the prompt>
2. <question>
3. <optional third question>
```

## Rules

- **Don't fabricate.** If a section can't be filled, leave a `[TODO: …]` placeholder inside the refined prompt. Never invent stack details, deadlines, or stakeholders the user didn't mention.
- **Keep it tight.** A good refined prompt is usually 3–10 sentences. Don't bloat with ceremony, role-play preambles ("You are an expert…"), or filler. Concrete > grand.
- **Preserve the user's voice and intent.** This is editing, not replacement. If they wrote casually, the refined version can still be casual — just clearer.
- **No XML tags or "step 1 / step 2 / step 3" scaffolding** unless the original task genuinely needs structured sections (e.g., multi-stage workflow). Don't impose structure for its own sake.
- **One pass.** Don't loop with the user to perfect the prompt. Deliver the refined version + assumptions + questions, and let them iterate.
