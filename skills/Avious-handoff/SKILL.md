---
name: Avious-handoff
description: |
  Save the current chat as a handoff file in the user's currently selected Cowork workspace folder, so a new chat can resume from where this one left off. Trigger when the user types /handoff, says save a handoff, save where we are, wrap this up so I can resume later, running low on context save state, make a handoff, or any similar phrase asking to preserve current chat state for continuation in a new chat. Writes to 05-handoffs/active/ and updates the Active threads list in START_HERE.md.
---

# Handoff — save current chat state

Save a chat-to-chat handoff so a new chat can resume from where this one left off.

## Core principle: preserve by relocating, never lose data silently

The handoff itself is intentionally terse (under 2KB), so here "preserve" does NOT mean cramming everything in — it means **no hard data gets lost**. When detail won't fit the handoff, move it into the appropriate room file and have the handoff *reference* that file. Relocate, don't delete.

- **Never silently drop hard data.** Links/URLs, IDs, exact doses, numbers, prices, code, file paths, command strings, and verbatim quotes the user assembled this chat must survive somewhere — either in the handoff or in a room file the handoff points to. Losing them is the failure mode to avoid.
- **If the chat produced a detailed artifact** (a table with links, a spec, a data list), write it to the relevant room *first*, then reference it from the handoff. Don't summarize it into oblivion.
- In your confirmation, note where any relocated detail landed so the next chat can find it.

## Procedure

1. **Determine the workspace folder.** Use the user's currently selected workspace folder, shown in the session context. If no workspace is selected, tell the user to select one in Cowork before running this skill, then stop.

2. **Verify the structure.** Confirm that `05-handoffs/active/` and `START_HERE.md` exist in the workspace. If either is missing, tell the user the workspace isn't set up for the three-layer routing system and suggest running `/scaffold` first. Then stop.

3. **Get the topic.** If the user provided a 2-4 word topic with the trigger, use it. Otherwise ask. Keep it short — it becomes part of the filename.

4. **Get today's date.** Use bash `date +%F` if not already known.

5. **Read the template** at `05-handoffs/_TEMPLATE.md` for the structure (only if not already in context). If missing, fall back to a minimal default with the sections listed below.

6. **Write the handoff** to `05-handoffs/active/handoff-YYYY-MM-DD-<short-topic>.md`. **Hard size limit: under 2KB.** If the handoff would be bigger, push detail into the appropriate room and have the handoff *reference* those files instead.

7. **The handoff captures:**
   - Where we left off (one sentence)
   - Context for next chat (2-4 bullets)
   - What we did this chat (bullet list)
   - Open threads (specific questions or work items)
   - Exact next step (one concrete action)
   - Files referenced this chat (relative paths)

8. **Update Active threads** in `START_HERE.md`. Add a one-line entry under the Active threads section.

9. **Confirm** to the user: filename written and that the next chat can resume by typing the resume command with this topic.
