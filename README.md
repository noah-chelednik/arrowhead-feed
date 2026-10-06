# arrowhead-feed

A deterministic daily job feed. Every morning it reads the public job lists of about 140 hiring boards (frontier AI labs, their evaluation and human-data vendors, applied-AI companies, trust-and-safety teams, policy shops), matches each posting against a set of role families and a location rule, drops anything already reported, and writes the new matches to `feed/<date>.md` and `.json`, with stable copies at `feed/latest.md` and `feed/latest.json`.

No LLM is involved in finding. The feed informs; a person decides.

## How it works

1. `config/companies.yaml` lists each board: hiring system (Greenhouse, Ashby or Lever), slug, tier, and an optional `include_if` filter for shared boards.
2. One fetcher per hiring system reads the board's public JSON endpoint.
3. `config/rules.yaml` defines role families (evaluation, human data, trust and safety, AI operations, writing, forward deployed, policy, early career), a short exclusion list, seniority flags, and the location rule (New York corridor, DC, Baltimore, Philadelphia, New Jersey, Boston, or remote US).
4. A posting is a **primary** match when a family appears in its title and it is in range; **secondary** when the family appears only in the description, or the family is one that is too broad to be primary; a **near miss** when it matched a family out of range, or looks AI-related in range but matched no family. Near misses exist so rule gaps are visible.
5. `data/seen.json` records every reported posting so each appears once.
6. `config/manual_watch.yaml` lists boards with no public feed. The output repeats it every week.

## Run

```
pip install -e ".[dev]"
pytest -q
python -m arrowhead_feed run
```

See `CLAUDE.md` for the other commands and the conventions.

## Schedule

`.github/workflows/feed.yml` runs every day at 10:00 UTC, commits the output, and then fails the job if any board could not be read, so a broken fetcher is visible in the Actions tab.

## Verified universe

All slugs in `companies.yaml` were verified against the live APIs on 2026-10-04. The first run fetched 15,993 postings from 138 boards with zero errors. Several wrong-company slugs that return postings are listed at the top of `companies.yaml` so nobody adds them by accident.
