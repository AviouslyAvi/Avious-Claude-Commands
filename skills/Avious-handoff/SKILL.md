---
name: Avious-handoff
description: |
  Save the current chat as a handoff file in the user's currently selected Cowork workspace folder, so a new chat can resume from where this one left off. Trigger when the user types /handoff, says save a handoff, save where we are, wrap this up so I can resume later, running low on context save state, make a handoff, or any similar phrase asking to preserve current chat state for continuation in a new chat. Writes to 05-handoffs/active/ and updates the Active threads list in START_HERE.md.
---

# Handoff — save current chat state

Save a chat-to-chat handoff (under 2KB) so a new chat can resume, relocating detail into room files rather than losing it. **Read [reference.md](reference.md) in this skill's directory for the preserve-by-relocating principle and the full 9-step procedure — then follow it.**
