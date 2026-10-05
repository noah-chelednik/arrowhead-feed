"""Run the feed: fetch every enabled company, apply rules, dedupe against
data/seen.json, write feed/<date>.json and feed/<date>.md.

The run never stops on a single company failure; failures are recorded in the
output and reported by `check-errors` so the Actions job can turn red after the
commit lands.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from . import config
from .fetchers import fetch
from .models import Company, Match, Posting
from .rules import evaluate, is_near_miss, is_primary, is_secondary, norm

TIER_NAMES = {
    1: "Frontier lab",
    2: "Lab vendor / eval / safety",
    3: "Applied AI / corridor employer",
    4: "Tooling / infrastructure",
    5: "Trust and safety / platform",
    6: "Policy / research / think tank",
    7: "Journalism / publishing",
    8: "Academic / library / digital humanities",
    9: "Program / fellowship",
}

MAX_NEAR_MISSES = 60


@dataclass
class RunResult:
    run_at: str
    counts: dict[str, int] = field(default_factory=dict)        # company -> postings fetched
    errors: dict[str, str] = field(default_factory=dict)        # company -> error
    new_primary: list[Match] = field(default_factory=list)
    new_secondary: list[Match] = field(default_factory=list)
    new_near_misses: list[Match] = field(default_factory=list)
    seen_added: int = 0


def _include(company: Company, p: Posting) -> bool:
    if not company.include_if:
        return True
    hay = norm(p.department + " " + p.title)
    return any(norm(x) in hay for x in company.include_if)


def load_seen(path: Path) -> dict:
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_seen(path: Path, seen: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(seen, f, indent=0, sort_keys=True)
        f.write("\n")


def run(companies: list[Company] | None = None, rules: dict | None = None,
        seen_path: Path | None = None, today: date | None = None,
        record_seen: bool = True) -> RunResult:
    companies = companies if companies is not None else config.load_companies()
    rules = rules or config.load_rules()
    seen_path = seen_path or config.DATA / "seen.json"
    today = today or date.today()
    seen = load_seen(seen_path)
    result = RunResult(run_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))

    for c in companies:
        if not c.enabled or not c.slug:
            continue
        try:
            postings = fetch(c)
        except Exception as e:  # noqa: BLE001 - we want every failure recorded
            result.errors[c.name] = str(e)[:300]
            continue
        result.counts[c.name] = len(postings)
        for p in postings:
            if not _include(c, p):
                continue
            m = evaluate(p, rules)
            is_new = p.key not in seen
            if is_primary(m):
                if is_new:
                    result.new_primary.append(m)
            elif is_secondary(m):
                if is_new:
                    result.new_secondary.append(m)
            elif is_near_miss(m, rules):
                if is_new and len(result.new_near_misses) < MAX_NEAR_MISSES:
                    result.new_near_misses.append(m)
            else:
                continue
            if is_new and record_seen:
                seen[p.key] = today.isoformat()
                result.seen_added += 1

    if record_seen:
        save_seen(seen_path, seen)
    # Stable ordering: tier, then company, then title.
    for lst in (result.new_primary, result.new_secondary, result.new_near_misses):
        lst.sort(key=lambda m: (m.posting.tier, m.posting.company, m.posting.title))
    return result


def write_outputs(result: RunResult, out_dir: Path | None = None, today: date | None = None,
                  manual_watch: list[dict] | None = None) -> tuple[Path, Path]:
    out_dir = out_dir or config.FEED
    out_dir.mkdir(parents=True, exist_ok=True)
    today = today or date.today()
    manual_watch = manual_watch if manual_watch is not None else config.load_manual_watch()
    stem = today.isoformat()
    # Feed files are never rewritten. A second run on the same day gets a suffix.
    n = 1
    while (out_dir / f"{stem}.json").exists() or (out_dir / f"{stem}.md").exists():
        n += 1
        stem = f"{today.isoformat()}-run{n}"
    jpath = out_dir / f"{stem}.json"
    mpath = out_dir / f"{stem}.md"

    payload = {
        "run_at": result.run_at,
        "date": today.isoformat(),
        "file_stem": stem,
        "companies_fetched": len(result.counts),
        "postings_fetched": sum(result.counts.values()),
        "counts": result.counts,
        "errors": result.errors,
        "new_primary": [m.to_dict() for m in result.new_primary],
        "new_secondary": [m.to_dict() for m in result.new_secondary],
        "new_near_misses": [m.to_dict() for m in result.new_near_misses],
        "manual_watch": manual_watch,
    }
    text_json = json.dumps(payload, indent=1, ensure_ascii=False) + "\n"
    text_md = render_markdown(payload)
    with open(jpath, "w", encoding="utf-8") as f:
        f.write(text_json)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(text_md)
    # latest.json and latest.md are stable-address copies of the newest run so a
    # reader can fetch one fixed URL. They are the only files in feed/ that get
    # overwritten.
    (out_dir / "latest.json").write_text(text_json, encoding="utf-8")
    (out_dir / "latest.md").write_text(text_md, encoding="utf-8")
    return jpath, mpath


def _row(d: dict) -> str:
    flags = ", ".join(d["seniority_flags"]) if d["seniority_flags"] else ""
    fam = ", ".join(d["families"] or d["secondary"])
    pay = f" | {d['pay']}" if d.get("pay") else ""
    loc = d["location"] or "location not stated"
    flag_txt = f" | flags: {flags}" if flags else ""
    return f"- **{d['company']}** (T{d['tier']}): [{d['title']}]({d['url']}) | {loc}{pay} | {fam}{flag_txt}\n"


def render_markdown(payload: dict) -> str:
    out = [f"# Arrowhead feed, {payload['date']}\n\n"]
    out.append(f"Run at {payload['run_at']}. Fetched {payload['postings_fetched']} postings from "
               f"{payload['companies_fetched']} boards. New this week: "
               f"{len(payload['new_primary'])} primary, {len(payload['new_secondary'])} secondary, "
               f"{len(payload['new_near_misses'])} near misses.\n\n")
    if payload["errors"]:
        out.append("## Boards that failed this run\n\n")
        for k, v in payload["errors"].items():
            out.append(f"- {k}: {v}\n")
        out.append("\n")
    out.append("## New primary matches (family in title, in range)\n\n")
    if not payload["new_primary"]:
        out.append("None.\n")
    tier = None
    for d in payload["new_primary"]:
        if d["tier"] != tier:
            tier = d["tier"]
            out.append(f"\n### Tier {tier}: {TIER_NAMES.get(tier, '')}\n\n")
        out.append(_row(d))
    out.append("\n## New secondary matches (family only in the description)\n\n")
    if not payload["new_secondary"]:
        out.append("None.\n")
    for d in payload["new_secondary"]:
        out.append(_row(d))
    out.append("\n## Near misses (logged so the rules can be tuned)\n\n")
    if not payload["new_near_misses"]:
        out.append("None.\n")
    for d in payload["new_near_misses"]:
        out.append(_row(d))
    if payload.get("manual_watch"):
        out.append("\n## Manual watch (no public feed; check by hand)\n\n")
        for w in payload["manual_watch"]:
            out.append(f"- {w.get('name')}: {w.get('careers_url')}" + (f" ({w['notes']})" if w.get("notes") else "") + "\n")
    return "".join(out)


def summary_counts(result: RunResult) -> Counter:
    c = Counter()
    for m in result.new_primary:
        for fam in m.families:
            c[fam] += 1
    return c
