# Week — on-demand current-week summary

Read this week's daily auto-notes from the Learning Roadmap and synthesize them inline. No file writes — this is a read-only summarizer for mid-week glances. The Sunday run of the nightly scheduled-tasks job is what actually writes weekly digests to disk.

## Procedure

1. **Locate the repo.** The Learning Roadmap lives at `/Users/aviouslyavi/Claude/Professional Development/LEARNING ROADMAP/`. If that path doesn't exist or `02-notes/auto/` is missing, tell the user the workspace isn't set up for auto-logging and stop.

2. **Compute the current ISO week.** Use bash:
   - `WEEK=$(date +%G-%V)` — current ISO year-week, e.g. `2026-21`.
   - Determine the dates for Monday through today in that ISO week:
     - `date -v-Mon +%Y-%m-%d` gives the most recent Monday.
     - Iterate forward to today's date with `date +%Y-%m-%d`.

3. **Read the matching auto-notes.** For each date from Monday through today, look for `02-notes/auto/YYYY-MM-DD.md`. Skip any that don't exist (the job may not have run yet, or it was a quiet day).

4. **If no files exist for this week:** Tell the user "No auto-notes yet for week `<WEEK>`. The nightly job runs at 6:00 AM — check back tomorrow, or run it manually from the Scheduled section." Stop.

5. **Synthesize inline.** Write a markdown summary directly in chat (do NOT write a file):

   ```markdown
   # Week <WEEK> — so far (<N> of <D> days logged)

   **Themes:** <2–3 sentences pulling out the dominant threads.>

   **Key activity by workspace:**
   - **Learning Roadmap:** <bullets>
   - **Projects:** <bullets, grouped by project>
   - **General Research:** <bullets>
   - <etc. — only include workspaces with activity>

   **Shipped / committed:** <list>

   **Days covered:** <list the dates that had auto-notes; flag any missing days>
   ```

   Keep sensitive workspaces (Clients/, Job-Search/) at the same redaction level the auto-notes already use — don't re-elevate detail.

6. **Done.** No file writes, no commits, no pushes. The user just wanted a glance.

## When NOT to use this skill

- For a *past* week → read `06-weekly/YYYY-WW.md` directly (the Sunday job already wrote it).
- For writing a new weekly digest → that's the Sunday scheduled-task job's job, don't duplicate it.
- For a single day's detail → read `02-notes/auto/YYYY-MM-DD.md` directly.
