# Simplify Response

Rewrite content in plain language for a reader who isn't familiar with the technical terms or jargon used in the original. The goal is clarity, not condescension.

## What to rewrite

- **Default source:** the most recent assistant response in this conversation.
- **If the user specifies content** (pastes text, says "simplify this part", points to a file), rewrite that instead.
- **If unclear**, ask which response they want simplified before rewriting.

## Rules

1. **Keep the structure.** If the original has headers, bullets, or sections, keep them — just simplify the words inside.
2. **Swap jargon for everyday words.** Replace technical terms with plain equivalents. If a technical term is unavoidable, define it inline in parentheses the first time it appears.
3. **Use shorter sentences.** Break long compound sentences into two or three shorter ones.
4. **Preserve meaning.** Don't drop information or change the conclusion. Simplification ≠ summarization.
5. **Keep the tone friendly and direct.** Not patronizing. Write like you're explaining something to a smart friend who happens to work in a different field.
6. **Use concrete analogies sparingly** when a concept is abstract (e.g., "think of it like..."), but don't force them.
7. **Keep formatting elements** (bold, links, code blocks) where they served a purpose in the original.

## What to avoid

- Don't add disclaimers like "in simple terms" or "to put it plainly" — just write plainly.
- Don't shorten so aggressively that nuance is lost. The user wants clarity, not a TL;DR.
- Don't talk down to the reader ("Okay, so basically...", "Don't worry if this sounds confusing").
- Don't translate brand names, product names, or proper nouns.

## Audience targeting

If the user names a specific audience ("simplify for my mom", "for an astrologer", "for a client who doesn't code"), tailor the analogies and reference points to that audience's likely background. Otherwise, default to "smart adult, not in this field."

## Output

Just output the rewritten version. No preamble like "Here's the simplified version:" — just the content itself, ready to copy or share.
