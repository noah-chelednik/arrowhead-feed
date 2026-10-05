"""Command line: run | doctor | check-errors | preview"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from . import config, feed
from .fetchers import fetch


def cmd_run(args) -> int:
    today = date.fromisoformat(args.date) if args.date else date.today()
    result = feed.run(today=today, record_seen=not args.dry_run)
    jpath, mpath = feed.write_outputs(result, today=today)
    print(f"fetched {sum(result.counts.values())} postings from {len(result.counts)} boards; "
          f"{len(result.errors)} errors; new: {len(result.new_primary)} primary, "
          f"{len(result.new_secondary)} secondary, {len(result.new_near_misses)} near misses")
    print(f"wrote {jpath} and {mpath}")
    return 0


def cmd_doctor(args) -> int:
    """Fetch every board and print counts. No rules, no seen-list changes."""
    companies = config.load_companies()
    bad = 0
    for c in companies:
        if not c.enabled or not c.slug:
            continue
        try:
            n = len(fetch(c))
            print(f"ok    {c.ats:10s} {c.slug:40s} {n:5d}  {c.name}")
            if n == 0:
                print(f"warn  empty board: {c.name}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"FAIL  {c.ats:10s} {c.slug:40s}        {c.name}: {str(e)[:120]}")
    print(f"{bad} failures")
    return 1 if bad else 0


def cmd_check_errors(args) -> int:
    """Exit non-zero if the latest feed file recorded fetch errors."""
    files = sorted(config.FEED.glob("*.json"))
    if not files:
        print("no feed files")
        return 1
    with open(files[-1], encoding="utf-8") as f:
        payload = json.load(f)
    errs = payload.get("errors") or {}
    if errs:
        print(f"{len(errs)} boards failed in {files[-1].name}:")
        for k, v in errs.items():
            print(f"  {k}: {v}")
        return 1
    print(f"no errors in {files[-1].name}")
    return 0


def cmd_preview(args) -> int:
    """Run one company through the rules and print what would match. Does not
    touch seen.json. Useful when tuning rules.yaml."""
    companies = [c for c in config.load_companies() if c.name.lower() == args.company.lower()
                 or (c.slug or "").lower() == args.company.lower()]
    if not companies:
        print("company not found in config/companies.yaml")
        return 1
    import tempfile
    scratch = Path(tempfile.mkdtemp()) / "seen.json"   # nonexistent: nothing is "seen"
    result = feed.run(companies=companies, record_seen=False, seen_path=scratch)
    payload = {
        "run_at": result.run_at, "date": "preview", "companies_fetched": len(result.counts),
        "postings_fetched": sum(result.counts.values()), "counts": result.counts,
        "errors": result.errors,
        "new_primary": [m.to_dict() for m in result.new_primary],
        "new_secondary": [m.to_dict() for m in result.new_secondary],
        "new_near_misses": [m.to_dict() for m in result.new_near_misses],
        "manual_watch": [],
    }
    print(feed.render_markdown(payload))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="arrowhead-feed")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="fetch, match, dedupe, write feed files")
    r.add_argument("--date", help="override the run date (YYYY-MM-DD)")
    r.add_argument("--dry-run", action="store_true", help="do not update data/seen.json")
    r.set_defaults(fn=cmd_run)
    d = sub.add_parser("doctor", help="fetch every board and report counts")
    d.set_defaults(fn=cmd_doctor)
    e = sub.add_parser("check-errors", help="exit 1 if the latest feed recorded fetch errors")
    e.set_defaults(fn=cmd_check_errors)
    p = sub.add_parser("preview", help="show matches for one company without recording")
    p.add_argument("company")
    p.set_defaults(fn=cmd_preview)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
