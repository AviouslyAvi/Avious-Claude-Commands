#!/usr/bin/env node
// Stop hook — appends one JSONL entry per session to 05-handoffs/.usage-log.jsonl
// Cross-platform: macOS, Linux, Windows. Requires only Node (ships with Claude Code).
// Receives Claude Code Stop event payload on stdin:
//   { session_id, transcript_path, cwd, ... }
// Mechanical fields only — summary/tags are backfilled by the workspace-optimizer skill.

"use strict";
const fs = require("fs");
const path = require("path");
const os = require("os");

function readStdinSync() {
  try { return fs.readFileSync(0, "utf8"); } catch { return ""; }
}

function safeJSON(s) { try { return JSON.parse(s); } catch { return null; } }

function relTo(root, p) {
  if (!p) return null;
  const rp = path.resolve(p);
  const rr = path.resolve(root);
  if (rp === rr) return ".";
  if (rp.startsWith(rr + path.sep)) return rp.slice(rr.length + 1).split(path.sep).join("/");
  return p;
}

function roomOf(relPath) {
  if (!relPath) return null;
  const top = relPath.split("/")[0];
  return /^\d\d-/.test(top) ? top : null;
}

// Best-effort lock: create a .lock file with O_EXCL, retry briefly, then proceed.
// On contention we still append — JSONL with line buffering rarely interleaves at this size,
// and the worst case (a rare torn line) is recoverable by the optimizer.
function withLock(lockPath, fn) {
  const start = Date.now();
  while (Date.now() - start < 1500) {
    try {
      const fd = fs.openSync(lockPath, "wx");
      try { return fn(); } finally {
        try { fs.closeSync(fd); } catch {}
        try { fs.unlinkSync(lockPath); } catch {}
      }
    } catch (e) {
      if (e.code !== "EEXIST") break;
      // Spin briefly. Math.random keeps multi-process retries from syncing.
      const until = Date.now() + 30 + Math.floor(Math.random() * 50);
      while (Date.now() < until) {}
    }
  }
  return fn(); // give up on lock, append anyway
}

function main() {
  const payload = safeJSON(readStdinSync()) || {};
  const projectDir = process.env.CLAUDE_PROJECT_DIR || payload.cwd || process.cwd();
  const handoffsDir = path.join(projectDir, "05-handoffs");
  if (!fs.existsSync(handoffsDir)) return; // not a scaffolded workspace

  const transcriptPath = payload.transcript_path;
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return;

  let lines;
  try {
    lines = fs.readFileSync(transcriptPath, "utf8").split(/\r?\n/).filter(Boolean);
  } catch { return; }

  const events = lines.map(safeJSON).filter(Boolean);

  const toolCounts = {};
  const filesRead = new Set();
  const filesWritten = new Set();
  const skills = [];
  let inTok = 0, outTok = 0, cacheTok = 0;
  let firstUser = null;
  let firstTs = null, lastTs = null;

  for (const ev of events) {
    if (ev.timestamp) { if (!firstTs) firstTs = ev.timestamp; lastTs = ev.timestamp; }
    if (ev.type === "user" && !firstUser) {
      const c = ev.message && ev.message.content;
      if (typeof c === "string") firstUser = c;
      else if (Array.isArray(c)) {
        const t = c.find(x => x && x.type === "text");
        if (t) firstUser = t.text;
      }
    }
    const usage = ev.message && ev.message.usage;
    if (usage) {
      inTok    += usage.input_tokens || 0;
      outTok   += usage.output_tokens || 0;
      cacheTok += usage.cache_read_input_tokens || 0;
    }
    const content = ev.message && ev.message.content;
    if (Array.isArray(content)) {
      for (const blk of content) {
        if (!blk || blk.type !== "tool_use") continue;
        const name = blk.name || "unknown";
        toolCounts[name] = (toolCounts[name] || 0) + 1;
        const input = blk.input || {};
        const fp = input.file_path || input.notebook_path;
        if (fp) {
          const rel = relTo(projectDir, fp);
          if (name === "Read") filesRead.add(rel);
          if (name === "Edit" || name === "Write" || name === "NotebookEdit") filesWritten.add(rel);
        }
        if (name === "Skill" && input.skill) skills.push(input.skill);
      }
    }
  }

  const allTouched = new Set([...filesRead, ...filesWritten]);
  const rooms = [...new Set([...allTouched].map(roomOf).filter(Boolean))];

  let duration = null;
  if (firstTs && lastTs) {
    const a = Date.parse(firstTs), b = Date.parse(lastTs);
    if (!isNaN(a) && !isNaN(b)) duration = Math.max(0, Math.round((b - a) / 1000));
  }

  const entry = {
    v: 1,
    ts: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
    session_id: payload.session_id || null,
    duration_s: duration,
    rooms,
    files_read: [...filesRead],
    files_written: [...filesWritten],
    skills,
    tool_counts: toolCounts,
    tokens: { input: inTok, output: outTok, cache_read: cacheTok },
    topic: firstUser ? String(firstUser).slice(0, 80) : null,
    summary: null,
    tags: [],
  };

  const logPath = path.join(handoffsDir, ".usage-log.jsonl");
  const lockPath = logPath + ".lock";
  withLock(lockPath, () => {
    fs.appendFileSync(logPath, JSON.stringify(entry) + os.EOL);
  });

  try {
    const stat = fs.statSync(logPath);
    let lineCount = 0;
    try { lineCount = fs.readFileSync(logPath, "utf8").split(/\r?\n/).filter(Boolean).length; } catch {}
    if (stat.size > 2 * 1024 * 1024 || lineCount > 5000) {
      const ym = new Date().toISOString().slice(0, 7);
      fs.writeFileSync(
        path.join(handoffsDir, ".usage-log.WARNING"),
        `Usage log is ${stat.size} bytes / ${lineCount} lines — consider rotating to .usage-log.${ym}.jsonl\n`
      );
    }
  } catch {}
}

try { main(); } catch { /* never break a session */ }
process.exit(0);
