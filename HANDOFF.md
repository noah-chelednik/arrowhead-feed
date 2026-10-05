# Arrowhead III Handoff

Written 2026-10-05 so any session, scheduled or interactive, in Claude Code or in the Arrowhead III Claude Project, can pick the system up cold. The System Design document in Drive is the long version; this file is the operational one. When they disagree, the Decisions tab of the Application Tracker wins, then this file, then the design document.

## 1. What this is

Arrowhead III is Noah Chelednik's build-once, run-forever job campaign. Goal: an AI evaluation or data-quality role at a vendor or applied-AI company in the New York corridor within six months; frontier labs (Anthropic, OpenAI, Google DeepMind) at three to five years; Noah's company Chedai at ten. Degree: B.S. Computer Science, WGU, expected November 2026. Runway ends February 2027. Location rule: New York, or a weekend overnight trip from it (DC, Baltimore, Philadelphia, New Jersey, Boston), or remote US; anywhere else only for exceptional work.

Four components:

1. Google Drive: the record and the queue (folder `1y0rQobB24GstXEHwvNpTdUR6J5_5RoZm`).
2. GitHub: this repository, `arrowhead-feed`, the deterministic finding layer.
3. Claude Code: the workshop where the repository is built and extended.
4. The Arrowhead III Claude Project: the operator, with two scheduled tasks and interactive sessions.

Principle: state lives in Drive and GitHub, never in a chat. Noah decides and submits. Nothing is ever auto-submitted.

## 2. File map (IDs are stable; names may change)

Drive folder Arrowhead III: `1y0rQobB24GstXEHwvNpTdUR6J5_5RoZm`

| File | Type | ID | Role |
|---|---|---|---|
| Master Career Record | Sheet | `1wyUJClcNFChbBtkgsICc5oiGKIk9NGvat0YuomRt-vQ` | Single source of truth for every date, title, hour, figure and claim. Tabs: To Confirm, Employment, Education, Publications and Activities, Projects, Key Figures, Public Surfaces, Prior Submissions. |
| Application Tracker | Sheet | `1JEY-kyHc1UvHbjOjZm1wTxGZ9V_uKTRZy_CEep2Uq1w` | The work queue and campaign board. Tab IDs below. |
| Playbook | Doc | `1R7PACVnWggqn1KMR7uAX8e0IL5D_kJQM8D6DdjorI68` | Rules: mission, lanes, daily routine, weekly review, triggers, graduation checklist, asset library. |
| System Design (v1.1) | Doc | `1-XIcyUkag0dVz8X2lYV2aJK7OD1-k8RdGb0NoEsRWLw` | How the system works, who does what, build order, Appendix A (project instructions), Appendix B (scheduled-task prompts). |
| Build Brief | Doc | `1nM0BIX24PhqeisUsiMazb8WpBKPn83ISQFe1Rllw0uY` | Drive copy of this file, made 2026-10-05. The repository copy is the master. |
| Search and Outreach Kit | Doc | `1AyozdhDjUxzXnmIURqKEXNmlOxtYnMyYyiBzmizpkJ0` | Board list, saved searches, outreach templates. |
| Government and Intelligence Guide | Doc | `1UTSQkMZLT6pWviLpyFU6OapYAJiHPkhB_DNyqmxkZPI` | Parked reference. |
| Assessment Prep and Timing | Doc | `1twmVMSFIfgQRx5eyOAYwaYUl4YoOOHhLQe0K1VLL_cY` | Platform assessment notes. |
| Assets | Folder | `1cvCi3tB9LCrDonpMm-av3gnra8sZaBVd` | Final documents an application needs. Holds `Noah_Chelednik_Resume.pdf` (core resume, `1ejsI4VRwcHFA_v9sl_pGVlRyyZpvrtqB`) and text copies of profile bios. Cover-note drafts from the Monday task land here as new files. |
| Archive (pre-Arrowhead III) | Folder | `1ueraB2UuLbIUttL7sFy2xlV7RnwHi603` | Text copies of every earlier resume and application (23 files). Read-only in practice. |

Application Tracker tabs (sheetId in parentheses):

- North Star (106): A-M = Org, Tier (1 Frontier lab / 2 Lab vendor-eval / 3 Applied AI), Route, Role, Location, Pay, Fit, Timing, What it asks for, Proof that helps most, Status, Link, Notes. 27 rows.
- Proof of Work (107): Artifact, What it proves, Supports, Due, Est. hours, Status, Output link, Notes. Part 1 is October (Chedai case study Oct 12, GitHub and HF cleanup Oct 13, one-pager Oct 14, demo Oct 16).
- Documents (108): every document to build, who writes it, due date, status, file link. Three resumes only: core (built), research and writing (due Oct 7), federal (only when a federal application is live).
- Decisions (110): Date, Decision, Why, Where it lives. Append a line for any change of plan.
- Feed (111): A-L = Week of, Company, Tier, Title, Location, Pay, Families, Flags, Link, Fit note (Claude), Decision (you), Notes. Append-only. Decision dropdown: Apply / Watch / Skip / Moved to Active. Rows 3-580 are the 2026-10-05 baseline (578 primary matches, no fit notes, Notes "baseline 2026-10-05").
- Companies (112): readable mirror of `config/companies.yaml` (rows 2-179) and `config/manual_watch.yaml` (row 180 header, then the list). The YAML files are the source; the tab is for reading.
- Active (100): the daily queue, 30 rows, sorted by Next Action Date (column H). Lane dropdown includes "N: North Star".
- Targets (101), Network (103), Scoreboard (104), Key Dates (105), Archive (102).
- Parked (109): Active columns plus Parked on, Why parked. 15 rows parked 2026-10-04 (the government lane and other low-yield rows).
- Original (backup) (0): the pre-revision tracker. Do not edit.

Tracker column conventions: dates are `YYYY-MM-DD` text; every Active row needs a Next Action and a Next Action Date.

## 3. Decisions in force (from the Decisions tab, 2026-10-04)

- Frontier labs and proper applied-AI roles are the North Star; the other lanes support it.
- Three resumes, fixed. A new role gets a cover note, never a fourth resume.
- Government and intelligence lane parked until the December 1 runway review or a sponsored clearance appears.
- Tech Force not pursued (two-year term). Jason Edds dropped.
- No AI in anything an employer requires to be Noah's own work: platform assessments, DIA and CIA essays, Perplexity and MATS applications, LessWrong posts. Anthropic Fellows answers: Noah drafts, Claude may refine.
- Nothing auto-submitted. The feed informs; Noah decides.
- A posting whose location says only "Remote" with no country is treated as remote US and flagged "remote country unstated" in the Feed tab; Noah confirms before applying.
- Every figure change cascades: record, resumes, LinkedIn, carrd, GitHub, Hugging Face, in that order.
- Brand rules on every written output: no em dashes, no exclamation points, no emojis, no hype. The name is Noah Chelednik, no initials.

## 4. What is built (as of 2026-10-05)

Repository `arrowhead-feed`, version 1:

- 178 boards in `config/companies.yaml` (Greenhouse, Ashby, Lever), every slug verified against the live API on 2026-10-04. 138 are enabled; the rest are SF-only or empty boards kept for reference.
- 60 boards in `config/manual_watch.yaml` with no public feed. The output repeats this list every run.
- Rules in `config/rules.yaml`: families evaluation, human_data, trust_safety, ai_ops, writing, forward_deployed, solutions (secondary only), policy, early_career; a short loose exclusion list; seniority flags; corridor and remote-US location lists.
- Three fetchers with fixture tests, rules tests, feed tests. `pytest -q`: 17 pass.
- Baseline run `feed/2026-10-05.json` and `.md`: 15,993 postings from 138 boards, 0 errors, 578 primary, 1,209 secondary, 60 near misses. `data/seen.json` holds all of them, so the next run reports only new postings.
- Workflow `.github/workflows/feed.yml`: Monday 10:00 UTC (6:00 a.m. Eastern in summer, 5:00 a.m. after November 1), plus manual dispatch. Installs, tests, runs, commits `feed/` and `data/seen.json`, then fails the job if any board errored.

Tracker: Feed, Companies, Decisions and Parked tabs created and filled; Active trimmed to 30 rows; North Star 27 rows; Proof of Work and Documents tabs complete.

Not yet done, in order: (a) push this repository to GitHub and watch the first Actions run; (b) create the Arrowhead III Claude Project and its two scheduled tasks; (c) the research and writing resume (Documents row 4, due Oct 7); (d) Proof of Work part 1; (e) version 2 fetchers (see CLAUDE.md).

## 5. How to run and extend

```
pip install -e ".[dev]"
pytest -q
python -m arrowhead_feed doctor            # fetch every enabled board, print counts
python -m arrowhead_feed preview "Surge AI" # one board, no side effects
python -m arrowhead_feed run --dry-run      # full run, seen.json untouched
python -m arrowhead_feed run                # the Monday run
python -m arrowhead_feed check-errors       # exit 1 if the latest feed has fetch errors
```

Adding a company: find its board slug (the path segment on `job-boards.greenhouse.io/<slug>`, `jobs.ashbyhq.com/<slug>` or `jobs.lever.co/<slug>`), add a line to `companies.yaml`, run `preview` to confirm the postings belong to that company, run `pytest -q`, commit. Mirror the line to the Companies tab when convenient. Wrong-company slugs that return postings are listed at the top of `companies.yaml`.

Changing a rule: edit `rules.yaml`, add or adjust a test in `tests/test_rules.py`, run `python -m arrowhead_feed run --dry-run` and read the near-miss section of the output to see what the change does.

Weekly feed files are never rewritten. If a run was wrong, write a note in the Decisions tab and let the next run proceed.

Housekeeping: once a quarter, Feed tab rows older than 90 days that have a Decision move to the Archive tab (an interactive session does this on request). Once a month, download the Application Tracker and the Master Career Record as .xlsx into a `Backups` subfolder of Archive so a bad edit can be reversed.

## 6. The Arrowhead III Claude Project

Create a new Claude Project named "Arrowhead III". Project instructions: Appendix A below, pasted verbatim. Connectors: Google Drive, Google Sheets, Google Docs. Synced source: this repository. Project files: the System Design document (or its export), the link index. Then create two scheduled tasks with the prompts in Appendix B, verbatim, with push and email notifications on. Run the Monday task once by hand after the first Actions run and check the Feed tab, the drafts in Assets and the summary.

## Appendix A: project instructions (paste verbatim)

You are the operator of Arrowhead III, Noah Chelednik's job campaign. The goal is an AI evaluation or data-quality role at a vendor or applied-AI company in the New York corridor within six months, with frontier labs (Anthropic, OpenAI, Google DeepMind) as the three-to-five-year target and Noah's company, Chedai, as the ten-year one. Degree: B.S. Computer Science, WGU, expected November 2026. Runway ends February 2027.

Sources of truth, in order. (1) The Master Career Record spreadsheet (ID 1wyUJClcNFChbBtkgsICc5oiGKIk9NGvat0YuomRt-vQ): every date, title, hour, figure and claim comes from it; if it is not there, ask or mark unknown, never infer. (2) The Application Tracker spreadsheet (ID 1JEY-kyHc1UvHbjOjZm1wTxGZ9V_uKTRZy_CEep2Uq1w): tabs North Star, Proof of Work, Documents, Decisions, Feed, Companies, Active, Targets, Network, Scoreboard, Key Dates, Archive, Parked. (3) The Playbook document (ID 1R7PACVnWggqn1KMR7uAX8e0IL5D_kJQM8D6DdjorI68): the rules. (4) The arrowhead-feed repository synced to this project: HANDOFF.md first, then the feed folder and the config folder. (5) The System Design document. Read the relevant file before acting; never work from memory of it. Final documents live in the Assets folder (ID 1cvCi3tB9LCrDonpMm-av3gnra8sZaBVd).

Fixed rules. Three resumes only (core, research and writing, federal); tailoring happens in cover notes, never in a fourth resume. Location rule: New York, or within a weekend overnight trip (DC, Baltimore, Philadelphia, New Jersey, Boston), or remote US; flag exceptions, never hide them; a posting that says only "Remote" is treated as remote US and flagged "remote country unstated". Never submit an application. Never write anything an employer requires to be Noah's own work: platform assessments, DIA and CIA essays, the Perplexity and MATS applications, LessWrong posts; for Anthropic Fellows answers, Noah drafts and you may refine. Conservative floors on every figure. Every figure change cascades across record, resumes, LinkedIn, carrd, GitHub and Hugging Face, in that order, before it goes public. The government lane is parked until the Decisions tab says otherwise. Any change of plan gets a dated line on the Decisions tab.

Writing to the tracker. The Feed tab is append-only: add rows, never edit or delete existing ones. Never change the Original (backup) tab. Scheduled runs create new files in Assets and never edit existing files. Interactive sessions may edit any other tab or document when Noah asks.

Scheduled runs. Monday Feed Review and Sunday Review Prompt follow their own task prompts. If a connector, repository or file is unavailable, report exactly what is missing and stop; do not guess and do not write partial results.

Voice and format. Plain, specific, compressed. No em dashes, no exclamation points, no emojis, no hype, no motivational framing. One committed recommendation rather than option menus. Structural diagnosis over surface polish. The name is Noah Chelednik, never with initials.

Success is a week in which Noah missed nothing, rebuilt nothing, and spent his time deciding, applying and building proof.

## Appendix B: scheduled-task prompts (paste verbatim)

### Task 1: Monday Feed Review

Schedule: weekly, Monday 7:30 a.m. Eastern (America/New_York). Notifications: push and email.

Prompt:

Run the Monday Feed Review for Arrowhead III. Follow the project instructions.

Step 1. In the arrowhead-feed repository synced to this project, open the feed folder and find the newest file by date in its name (feed/YYYY-MM-DD.json, with a matching .md). If the newest file is dated more than 7 days before today, the GitHub Actions run did not happen this week: say so at the top of the summary, include steps 6 and 7 anyway, and do not write to the tracker.

Step 2. From the JSON, read companies_fetched, postings_fetched, errors, new_primary, new_secondary and new_near_misses. If errors is not empty, list each board name and its error in the summary.

Step 3. Open the Application Tracker (spreadsheet ID 1JEY-kyHc1UvHbjOjZm1wTxGZ9V_uKTRZy_CEep2Uq1w), Feed tab. Read column I (Link) so you can skip any posting already present. Append one row per new_primary entry, below the last filled row, with columns A to L: Week of (the feed date), Company, Tier, Title, Location (shortened to the first three distinct places), Pay, Families (comma separated), Flags (seniority_flags, plus "remote country unstated" when location_class is remote_us and the location text names no US place or country), Link (url), Fit note, Decision (leave blank), Notes ("primary"). Then append the new_secondary entries the same way with Notes "secondary" and no fit note. Never edit, sort or delete existing rows. Sort the rows you append by Tier, then Company, then Title.

Step 4. Fit note, primary rows only: one line under 20 words, judged against the North Star tab tiers and the Master Career Record (spreadsheet ID 1wyUJClcNFChbBtkgsICc5oiGKIk9NGvat0YuomRt-vQ). Say what the role asks for that Noah has in the record, and the one gap if there is one. Do not invent anything. If a seniority flag is present, start the note with the flag.

Step 5. Choose the top three primary rows (lowest tier first, then strongest fit). For each, create a new Google Doc in the Assets folder (ID 1cvCi3tB9LCrDonpMm-av3gnra8sZaBVd) named "Cover note draft - <Company> - <Title> - <feed date>". Use the cover-note template in Assets if a file with "template" in its name exists; otherwise write 120 to 180 words from the core resume facts in the Record: what the role asks for, two specific pieces of evidence from the record, one line on why this company, and a plain closing. No claims that are not in the record. Write "draft in Assets" in the Notes cell of those three Feed rows (the rows you appended this run only). Never edit an existing file in Assets.

Step 6. Read the Active tab: list rows whose Next Action Date (column H) is before today. Read the Key Dates tab: list dates within the next 14 days. Read the Scoreboard tab: the latest row's totals.

Step 7. Read config/manual_watch.yaml in the repository and prepare a checklist of its entries, tier 1 and 2 first, each with its careers_url.

Summary (your final message; it is also the notification): one line with the feed date, boards fetched, postings fetched, counts of new primary, secondary and near misses; fetch errors if any; the top three with links and fit notes; overdue Active rows; Key Dates within 14 days; Scoreboard totals; the manual-watch checklist. Plain text, no em dashes, no exclamation points, no emojis. If a connector, the repository or a file is unavailable, say exactly what is missing and stop without writing anything.

### Task 2: Sunday Review Prompt

Schedule: weekly, Sunday 6:00 p.m. Eastern (America/New_York). Notifications: push and email.

Prompt:

Prepare the Sunday Review digest for Arrowhead III. Follow the project instructions. This task reads only; it writes nothing anywhere.

Open the Application Tracker (spreadsheet ID 1JEY-kyHc1UvHbjOjZm1wTxGZ9V_uKTRZy_CEep2Uq1w) and read these tabs: Active, Feed, Proof of Work, Key Dates, Scoreboard, North Star.

Report, in this order, in plain text:

1. Active rows that need a decision: Next Action Date before today, or Status that has not changed in 30 days (use Date Applied or Last Contact where present), or Lane A platform rows with an assessment and no email in 21 days (Playbook trigger: treat as a no and move to Archive).
2. Feed rows from the last 14 days with an empty Decision column: count by tier, and list the tier 1 and tier 2 titles with company and link.
3. Feed rows marked Apply that do not yet appear in Active (match on Org and Role): list them, since each needs an Active row with a Next Action Date.
4. Proof of Work rows due in the next 14 days or overdue, with status.
5. Key Dates in the next 14 days.
6. This week's counts for the Scoreboard row: applications submitted, assessments completed, network touches, interviews, from the Active and Network tabs where dates fall in the last 7 days; mark any count you could not derive as "not derivable".
7. North Star rows whose Status is In progress or Applied, one line each.

Then one line naming the single most important thing to do this week, chosen from the above. No recommendations beyond that line. No em dashes, no exclamation points, no emojis. If a connector or the spreadsheet is unavailable, say exactly what is missing and stop.
