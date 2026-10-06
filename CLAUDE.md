# CLAUDE.md

This repository is the finding layer of Arrowhead III, Noah Chelednik's job-search system. It fetches public hiring boards, matches postings against role families and a location rule, and reports only what is new. Read HANDOFF.md before changing anything. The private campaign context lives in a Google Drive document, not in this repository; keep personal details out of commits.

## Conventions

- Deterministic only. No LLM calls in this codebase. Judgment happens in the Claude Project that reads feed/latest.json, not here.
- Tests before merge: `pytest -q` must pass. Add a fixture-based test for any new fetcher and a rule test for any rule change.
- Rules live in `config/rules.yaml`, companies in `config/companies.yaml`, boards without a feed in `config/manual_watch.yaml`. Prefer a config change to a code change.
- Keep exclusions loose. A false positive costs one glance; a false negative is invisible. Use `flag_title` to mark likely-senior roles instead of hiding them.
- Never add anything that submits an application, logs into a site, or scrapes a site that forbids automation (LinkedIn, Workday portals, Meta and Google careers pages). Those stay on the manual-watch list.
- Slugs are verified facts. When adding a company, confirm the public API returns postings (`python -m arrowhead_feed preview <name>`) and watch for wrong-company slugs; several are listed at the top of `companies.yaml`.
- Output stays append-only: one dated JSON and Markdown pair per run in `feed/`, and `data/seen.json` grows. Do not rewrite past feed files.
- Plain language in docs and output. No em dashes, no exclamation points, no emojis, no hype.

## Commands

- `python -m arrowhead_feed run` fetch, match, dedupe, write `feed/<date>.json` and `.md`
- `python -m arrowhead_feed run --dry-run` same, without updating `data/seen.json`
- `python -m arrowhead_feed preview "Surge AI"` show what one board would produce, no side effects
- `python -m arrowhead_feed doctor` fetch every enabled board and print counts
- `python -m arrowhead_feed check-errors` exit 1 if the latest feed recorded fetch errors
- `pytest -q`

## Layout

- `arrowhead_feed/fetchers/` one module per hiring system (greenhouse, ashby, lever); `_http.py` is the shared client
- `arrowhead_feed/rules.py` families, exclusions, flags, location classes
- `arrowhead_feed/feed.py` the run, dedupe and output
- `arrowhead_feed/cli.py` commands
- `.github/workflows/feed.yml` daily cron (10:00 UTC); commits output, then fails the job if any board errored

## Version 2 candidates (in order)

1. Rippling fetcher (Lawfare, Partnership on AI): `https://api.rippling.com/platform/api/ats/v1/board/{slug}/jobs`
2. BambooHR fetcher (CNAS): `https://{slug}.bamboohr.com/careers/list`
3. Gem fetcher (Transluce): GraphQL at `https://jobs.gem.com/api/public/graphql`
4. Custom JSON pollers: Spring Health, Kensho, Micro1 (endpoints noted in `manual_watch.yaml`)
5. Workable with backoff (Hugging Face)
6. USAJOBS API
