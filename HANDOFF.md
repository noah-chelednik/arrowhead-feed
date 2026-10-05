# arrowhead-feed Handoff

Operational notes for anyone, or any Claude session, picking this repository up cold. The repository is public; it holds code, configuration and the weekly feed output only. The campaign context that uses this feed (goals, decisions, file IDs, scheduled-task prompts) lives in a private Build Brief document in the owner's Google Drive, not here.

## What this is

A deterministic weekly job feed. Every Monday it reads the public job lists of about 140 hiring boards, matches each posting against role families and a location rule, drops anything already reported, and writes the new matches to `feed/<date>.json` and `.md`, plus stable copies at `feed/latest.json` and `feed/latest.md`.

No LLM is involved in finding. The feed informs; a person decides. Nothing here submits an application, logs into a site, or scrapes a site that forbids automation.

## Stable addresses

Readers that need the newest run fetch one of these fixed URLs rather than the project's synced copy, which only updates by hand:

- `https://raw.githubusercontent.com/noah-chelednik/arrowhead-feed/main/feed/latest.json`
- `https://raw.githubusercontent.com/noah-chelednik/arrowhead-feed/main/feed/latest.md`
- `https://raw.githubusercontent.com/noah-chelednik/arrowhead-feed/main/config/manual_watch.yaml`

`latest.json` fields: `run_at`, `date`, `file_stem`, `companies_fetched`, `postings_fetched`, `counts` (per board), `errors` (per board, empty when clean), `new_primary`, `new_secondary`, `new_near_misses` (lists of postings with `company`, `tier`, `title`, `url`, `location`, `remote`, `department`, `pay`, `posted`, `families`, `secondary`, `location_class`, `seniority_flags`, `excluded_by`), and `manual_watch` (the boards with no public feed).

## Layout

- `config/companies.yaml`: the universe with a public feed. 178 boards (Greenhouse, Ashby, Lever), each with slug, tier (1 frontier lab, 2 lab vendor or eval company, 3 applied AI, 4 AI infrastructure, 5 trust and safety, 6 policy and research, 7 media, 8 academic and cultural, 9 aggregator), location flags, an optional `include_if` filter for shared or very large boards, and an `enabled` flag. Every slug was verified against the live API on 2026-10-04. Wrong-company slugs that return postings are listed at the top so nobody adds them by accident.
- `config/manual_watch.yaml`: 60 boards with no public feed. The output repeats this list every run.
- `config/rules.yaml`: role families, a short loose exclusion list, seniority flags that mark rather than hide, near-miss hint words, and the location rule.
- `arrowhead_feed/fetchers/`: one module per hiring system; `_http.py` is the shared client with retries.
- `arrowhead_feed/rules.py`: matching. Primary: a family in the title, in range, not excluded. Secondary: family only in the description, or a family too broad to be primary. Near miss: a family match out of range, or an in-range AI-ish title with no family. Near misses are logged so rule gaps are visible.
- `arrowhead_feed/feed.py`: the run, dedupe against `data/seen.json`, output.
- `data/seen.json`: every posting key already reported. The baseline run of 2026-10-05 (15,993 postings, 138 boards, 0 errors) is recorded, so later runs report only what is new.
- `feed/`: one dated JSON and Markdown pair per run, never rewritten; a second run on the same day gets a `-run2` suffix. `latest.*` are the only files that get overwritten.
- `.github/workflows/feed.yml`: Monday 10:00 UTC plus manual dispatch. Installs, tests, runs, commits `feed/` and `data/seen.json`, then fails the job if any board errored.
- `tests/`: fixture-based fetcher tests, rule tests, feed tests. 19 tests.

## Run and extend

```
pip install -e ".[dev]"
pytest -q
python -m arrowhead_feed doctor             # fetch every enabled board, print counts
python -m arrowhead_feed preview "Surge AI"  # one board, no side effects
python -m arrowhead_feed run --dry-run       # full run, seen.json untouched
python -m arrowhead_feed run                 # the Monday run
python -m arrowhead_feed check-errors        # exit 1 if the latest feed has fetch errors
```

Adding a company: find its board slug (the path segment on `job-boards.greenhouse.io/<slug>`, `jobs.ashbyhq.com/<slug>` or `jobs.lever.co/<slug>`), add a line to `companies.yaml`, run `preview` to confirm the postings belong to that company, run `pytest -q`, commit.

Changing a rule: edit `rules.yaml`, add or adjust a test in `tests/test_rules.py`, run `python -m arrowhead_feed run --dry-run` and read the near-miss section of the output to see what the change does.

If a run was wrong, do not rewrite its files; note it and let the next run proceed.

## Version 2 candidates

See CLAUDE.md: Rippling, BambooHR, Gem, custom JSON pollers, Workable with backoff, USAJOBS.
