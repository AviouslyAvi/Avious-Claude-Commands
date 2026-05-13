---
name: Avious-compare-and-save
description: >
  Research and generate structured side-by-side comparisons of tools, apps, services, or technologies,
  then save as a markdown file to the user's Obsidian vault. Use this skill whenever the user asks to
  compare two or more things — phrases like "compare X vs Y", "X versus Y", "which is better X or Y",
  "comparison of X and Y", "X or Y for [use case]", "should I use X or Y", "differences between X and Y",
  "pros and cons of X vs Y", or any variant. Also trigger when the user mentions wanting to save a
  comparison to Obsidian, or asks to "compare and save". Even casual phrasing like "what's better, X or Y?"
  or "help me pick between X and Y" should trigger this skill.
---

# Compare and Save

A workflow for researching, drafting, reviewing, and saving structured comparisons to the user's Obsidian vault in Google Drive — always accompanied by an interactive HTML artifact with visual charts.

## Why this skill exists

Avi frequently compares tools, apps, and technologies and saves the results as markdown notes in his Obsidian vault. This skill standardizes that workflow so every comparison is well-researched, consistently formatted, visually rich, and only saved after explicit approval.

## Destination

All comparisons are saved to:
```
/Users/aviouslyavi/Library/CloudStorage/GoogleDrive-avimusicproductions@gmail.com/My Drive/Documents/Fresh Obsidian/
```

## Workflow

### Step 1: Research

Use `WebSearch` to research both (or all) options being compared. Run multiple searches to cover:
- Official sites and feature lists
- Pricing and licensing
- Community sentiment and reviews
- Recent updates or changes (use the current year in queries)

Gather enough information to give a genuinely useful, balanced comparison — not just surface-level bullet points. Pay special attention to quantitative data (pricing tiers, track/feature limits, performance benchmarks, satisfaction scores) since this feeds directly into the charts.

### Step 2: Draft the comparison

Every comparison produces **two outputs**:

#### 2a. Interactive HTML artifact with charts

Create an `.html` file (or `.jsx` if in an environment that renders React) with:

- **Dark theme** (background `#0f0f0f`, light text) for a polished look
- **Tabbed navigation** across sections (Overview, Cost, Capabilities, specific comparison dimensions, Verdict)
- **Visual charts** — always include at least:
  - A **bar chart** for cost/pricing comparison (e.g., total cost of ownership over 1, 3, and 5 years)
  - A **radar chart** for capability scoring across relevant dimensions (scored 0–100)
  - Any other chart type that fits the subject matter (e.g., bar visualization for limits/caps, timeline charts for release history)
- **Feature comparison table** in the Overview tab
- **Verdict section** with clear "Choose X if…" and "Choose Y if…" cards
- **Source attribution** in the footer

For HTML files, use **Chart.js** loaded from CDN (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js`). For JSX files, use **Recharts**. Lazy-initialize charts when their tab is first shown to avoid rendering issues.

The charts should adapt to the subject matter — a DAW comparison might chart track limits and cost over time, while a cloud provider comparison might chart regional availability and pricing per compute unit. Think about what dimensions are most useful to visualize for the specific comparison at hand.

Save this file to the user's workspace folder as `[Option A] vs [Option B].html` (or `.jsx`).

#### 2b. Structured markdown document

Generate the canonical markdown version following this template:

```markdown
# [Option A] vs [Option B] ([Category])

## [Option A]

- **Price**: ...
- **Tech**: ...
- **Key features**: ...
- **Best for**: ...

## [Option B]

- **Price**: ...
- **Tech**: ...
- **Key features**: ...
- **Best for**: ...

## Comparison Table

| | [Option A] | [Option B] |
|---|---|---|
| Row 1 | ... | ... |
| Row 2 | ... | ... |

## Verdict

A clear, opinionated recommendation explaining who should pick which option and why.

## Sources

- [Source 1](url)
- [Source 2](url)
```

The table rows should cover the dimensions that actually matter for the comparison (cost, performance, ease of use, platform support, etc.) — adapt them to the subject matter rather than using a fixed set every time.

### Step 3: Present and ask for approval

Present the interactive HTML/JSX artifact to the user first (link to the file so they can explore the charts), then show the markdown content in chat. Ask:

> **Does this comparison look good? I'll save it to your Fresh Obsidian directory, or I can revise anything first.**

This confirmation step is important — never skip it. The user may want to:
- Add or remove sections
- Correct factual details
- Change the verdict
- Adjust the tone or depth
- Modify the charts

If the user requests changes, revise and present again. Repeat until they approve.

### Step 4: Save to Obsidian

Only after the user explicitly approves, save the markdown file:

- **Path**: `/Users/aviouslyavi/Library/CloudStorage/GoogleDrive-avimusicproductions@gmail.com/My Drive/Documents/Fresh Obsidian/[Option A] vs [Option B].md`
- **Filename**: Use the comparison title (e.g., `Shottr vs Bettershot.md`)
- The HTML artifact stays in the workspace folder for the user to keep or move as they like
- Confirm to the user that both files were saved and where

## Handling edge cases

- **More than two options**: Expand the template naturally — add a section for each option and widen the comparison table. The filename becomes `X vs Y vs Z.md`. Charts should include all options (additional bars, additional radar lines, etc.).
- **Vague requests**: If the user says "compare note-taking apps" without naming specific ones, ask which ones they want compared, or suggest popular options to narrow it down.
- **Already-generated comparison in chat**: If a comparison was already generated earlier in the conversation (before this skill triggered), use that content as the starting draft — don't re-research from scratch unless the user asks to.
- **Non-quantitative comparisons**: Some comparisons (e.g., philosophical frameworks, writing styles) don't lend themselves to pricing or limit charts. In these cases, still create the radar chart for capability scoring and any other visualization that makes sense — even subjective dimensions can be scored and charted usefully. The key is that every comparison gets visual charts, not just the ones with obvious numerical data.
