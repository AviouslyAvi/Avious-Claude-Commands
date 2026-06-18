# Scaffold — bootstrap a workspace with the three-layer structure

Create the full three-layer routing system in a fresh Cowork workspace.

## Procedure

1. **Determine the workspace folder** from the session context. If no workspace is selected, tell the user to select one in Cowork first, then stop.

2. **Check for existing structure.** Look for `START_HERE.md` at the workspace root. If it exists, ask the user whether to overwrite or abort. Default to abort.

3. **Ask the project type** via AskUserQuestion (or list options):
   - **Relationship** — rooms: 00-foundation, 01-conversations, 02-journal, 03-plans, 04-astrology
   - **Code** — rooms: 00-foundation, 01-decisions, 02-experiments, 03-plans
   - **Writing** — rooms: 00-foundation, 01-drafts, 02-research, 03-published
   - **Research** — rooms: 00-foundation, 01-sources, 02-notes, 03-syntheses
   - **Custom** — ask for a comma-separated list of room names. They must follow `NN-name` format.

4. **Always create:**
   - `05-handoffs/active/`
   - `05-handoffs/archive/`
   - `05-handoffs/_TEMPLATE.md` (standard handoff template)
   - `CLAUDE.md` (operating procedure)
   - `START_HERE.md` (router with task→room map customized to chosen rooms)

5. **For each chosen room, create** `<room>/README.md` (Layer 2 context file with placeholder sections: Room purpose, What lives here, Files to load, Files to skip, Skills to invoke, Pipeline, When to leave this room). The user fills these in over time.

6. **START_HERE.md must contain:** title, three-layer explanation, loading protocol, task→room map, slash-style triggers, an Active threads section with placeholder, and a Last updated line.

7. **CLAUDE.md must contain:** the architecture explanation, token discipline rules, where things go (per room), handoff protocol, subagent delegation rules.

8. **Confirm** to the user: list the rooms created, the path to `START_HERE.md`, and tell them to edit the room READMEs to match their project.
