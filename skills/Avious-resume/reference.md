# Resume — pick up from a saved handoff

Resume from a saved handoff. Read only that one file. Do not load anything else.

## Procedure

1. **Determine the workspace folder** from the session context.

2. **Get the handoff identifier.** It's whatever the user provided after `/resume` or in the trigger phrase.

3. **If no identifier was provided:** Glob `05-handoffs/active/*.md` and ask the user which one. Don't guess.

4. **Match the identifier** against filenames in `05-handoffs/active/`. If multiple match, ask the user to disambiguate.

5. **Read only the matched handoff file.** Do not read `START_HERE.md`, room READMEs, or any other project files unless the handoff explicitly tells you to. Token discipline is the whole point of the handoff system.

6. **State where we left off in one line.** Use the handoff's "Where we left off" section so the user can confirm we're aligned before continuing.

7. **Continue from the "Exact next step"** in the handoff.

8. **If the handoff lists "Files referenced":** load those only when the next step actually requires them, not preemptively.
