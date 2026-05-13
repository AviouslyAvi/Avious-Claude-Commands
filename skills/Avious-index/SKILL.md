---
name: Avious-index
description: |
  Re-read the START_HERE.md router for the current Cowork workspace to refresh the workspace map and active threads list mid-chat. Trigger when the user types /index, says re-read the index, refresh the map, what's in the workspace again, remind me of active threads, or after any operation that updated START_HERE.md when the user wants the latest state in context.
---

# Index — refresh the workspace map mid-chat

Re-read the Layer 1 router so the workspace map and active threads list are fresh in context.

## Procedure

1. **Determine the workspace folder** from the session context.

2. **Read** `START_HERE.md` at the workspace root.

3. **If no START_HERE.md exists:** Tell the user the workspace isn't set up for the three-layer routing system and suggest `/scaffold` first. Stop.

4. **Briefly state:**
   - Active threads if any
   - Confirm the map is reloaded

5. **Do not** load any room READMEs or other project files. This skill only refreshes the router.
