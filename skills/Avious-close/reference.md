# Close — archive a completed handoff

Archive a handoff that's no longer active. Move it from `active/` to `archive/` and update the Active threads list.

## Procedure

1. **Determine the workspace folder** from the session context.

2. **Get the handoff identifier.** It's whatever the user provided after `/close`.

3. **If no identifier was provided:** Glob `05-handoffs/active/*.md` and ask the user which one to close.

4. **Match the identifier** against filenames in `05-handoffs/active/`. If multiple match, ask to disambiguate.

5. **Move the file** from `05-handoffs/active/` to `05-handoffs/archive/` using bash `mv`. Do not delete — archive only.

6. **Update START_HERE.md.** Read it, find the line in the Active threads section pointing to the now-archived handoff, and remove only that line. If Active threads becomes empty, replace it with the placeholder `- _none_`.

7. **Confirm** to the user: filename moved and Active threads updated.
