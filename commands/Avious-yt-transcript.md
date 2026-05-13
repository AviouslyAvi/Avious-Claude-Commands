---
description: Download a YouTube video's transcript with yt-dlp and save it as markdown
argument-hint: <youtube-url> [optional save path or filename]
allowed-tools: Bash, Write, Read
---

Fetch the transcript for the YouTube video at the URL in `$ARGUMENTS` using yt-dlp.

Steps:
1. Extract the URL from `$ARGUMENTS`. If a second argument is provided, treat it as the destination path or filename for the saved transcript. Otherwise ALWAYS save to `/Users/aviouslyavi/Downloads/` using the video title as the filename (sanitized, ending in `.md`). Do not ask — this is the default destination.
2. Run yt-dlp to download English auto-subs only (no video):
   ```
   yt-dlp --write-auto-sub --skip-download --sub-lang en --sub-format vtt -o "/tmp/yt_%(id)s.%(ext)s" "<URL>"
   ```
3. Locate the resulting `.vtt` file in `/tmp/` and clean it into plain text using this Python one-liner pattern (strip WEBVTT headers, timestamps, inline tags, and dedupe rolling-caption lines):
   ```python
   import re
   text = open(vtt_path).read()
   lines, seen = [], set()
   for line in text.split('\n'):
       if '-->' in line or line.startswith(('WEBVTT','Kind:','Language:')) or not line.strip():
           continue
       clean = re.sub(r'<[^>]+>', '', line).strip()
       if clean and clean not in seen:
           seen.add(clean)
           lines.append(clean)
   ```
4. If the user wanted a title for the file but didn't give one, fetch the title via `yt-dlp --get-title <URL>`.
5. Save the cleaned transcript as a `.md` file at the requested location. Do not add commentary, headers, or frontmatter unless the user asked for them — just the cleaned transcript text.
6. Report back the saved path as a markdown link, plus a one-line summary if useful.

Notes:
- If auto-subs aren't available, try `--write-sub` (manual subs) before giving up.
- Clean up the temp `.vtt` after saving.
