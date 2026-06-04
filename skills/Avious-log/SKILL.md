---
name: Avious-log
description: |
  Save the current chat snippet to a room in the current Cowork workspace. Discovers available rooms by globbing the workspace folder structure, then asks the user which room to log to. Trigger when the user types /log, says log this, capture this conversation, save this to journal, save this exchange, write this down, or any phrase asking to preserve the current snippet to the appropriate room. Workspace-agnostic — works in any folder following the three-layer routing pattern.
---

# Log — save current snippet to a room

Capture the current chat snippet to a room in the workspace, picked dynamically based on what rooms exist in this project.

## Core principle: preserve, don't degrade

Default to **preserving** the richest version of the snippet, not summarizing it. Capturing means keeping the detail the user worked to assemble — clean it up and format it, but do not condense it away.

- **Never silently drop hard data.** Links/URLs, IDs, exact doses, numbers, prices, code, file paths, command strings, and verbatim quotes must survive into the logged file. If a table or list in the chat had a column of links, the saved file keeps that column.
- **When the user references something they liked** ("the chart you made", "the version with the links"), reconstruct the **most complete** version from the conversation — merge the best columns/fields if better versions appeared across different messages. Do not regenerate a leaner version from scratch.
- If you genuinely must omit something, say so in your confirmation message rather than dropping it silently.

## Procedure

1. **Determine the workspace folder** from the session context.

2. **Discover available rooms.** Glob the workspace for numbered room folders matching `[0-9][0-9]-*/`. Exclude `05-handoffs/` and any underscore-prefixed folders.

3. **If no rooms exist:** Tell the user the workspace isn't set up. Suggest `/scaffold` first. Stop.

4. **Pick the room.** If the user hinted at a room, match the hint and confirm. Otherwise present the discovered rooms via AskUserQuestion and let the user pick.

5. **Get today's date** (bash `date +%F` if needed).

6. **Get the topic.** If the user didn't provide one, propose a 3-6 word topic from the snippet content and confirm before writing.

7. **Read the chosen room's `README.md`** once if not already in context — it specifies the frontmatter and structure for that room. If no README exists, use a minimal frontmatter (date, topic).

8. **Write the file** to `<room>/YYYY-MM-DD-<topic>.md` using the room's frontmatter shape.

9. **Confirm** the file path back to the user with a brief note on what was captured.
