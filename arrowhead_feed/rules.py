"""Matching rules: role families, exclusions, seniority flags, location classes.

Everything here is deterministic and driven by config/rules.yaml so the rules
can be tuned without touching code. Matching is case-insensitive substring
matching on normalized text.
"""

from __future__ import annotations

import re

from .models import Match, Posting

_WS = re.compile(r"\s+")


def norm(s: str) -> str:
    s = (s or "").lower().replace("&", " and ")
    s = re.sub(r"[\-_/,()]+", " ", s)
    return _WS.sub(" ", s).strip()


def _any(text: str, terms: list[str]) -> bool:
    return any(t in text for t in terms)


def families_in(text: str, families: dict[str, list[str]]) -> list[str]:
    t = norm(text)
    return [fam for fam, terms in families.items() if _any(t, [norm(x) for x in terms])]


def classify_location(location: str, remote_flag: bool, rules: dict) -> str:
    """corridor | remote_us | exception | unknown"""
    loc = norm(location)
    if not loc:
        return "unknown"
    corridor = [norm(x) for x in rules["location"]["corridor"]]
    remote_us = [norm(x) for x in rules["location"]["remote_us"]]
    remote_not_us = [norm(x) for x in rules["location"]["remote_not_us"]]
    parts = [p.strip() for p in loc.split("|")]
    classes = []
    for p in parts:
        if _any(p, corridor):
            classes.append("corridor")
        elif "remote" in p:
            if _any(p, remote_not_us):
                classes.append("exception")
            elif _any(p, remote_us) or p.strip() == "remote":
                classes.append("remote_us")
            else:
                # "Remote" with an unknown qualifier; the flag decides.
                classes.append("remote_us" if remote_flag else "exception")
        else:
            classes.append("exception")
    if "corridor" in classes:
        return "corridor"
    if "remote_us" in classes:
        return "remote_us"
    return "exception"


def evaluate(p: Posting, rules: dict) -> Match:
    title = norm(p.title)
    fams = families_in(p.title, rules["families"])
    sec_only = set(rules.get("secondary_only_families", []))
    secondary = [f for f in fams if f in sec_only]
    fams = [f for f in fams if f not in sec_only]
    if not fams and not secondary and p.description:
        strong = {k: v for k, v in rules["families"].items() if k in rules.get("description_families", [])}
        secondary = families_in(p.description, strong)
    excluded = None
    for term in rules.get("exclude_title", []):
        if norm(term) in title:
            excluded = term
            break
    flags = [term for term in rules.get("flag_title", []) if norm(term) in title]
    loc_class = classify_location(p.location, p.remote, rules)
    return Match(
        posting=p,
        families=fams,
        secondary=secondary,
        location_class=loc_class,
        seniority_flags=flags,
        excluded_by=excluded,
    )


def is_primary(m: Match) -> bool:
    """A primary match: a family in the title, in range, not excluded."""
    return bool(m.families) and m.location_class in ("corridor", "remote_us") and not m.excluded_by


def is_secondary(m: Match) -> bool:
    """Worth a look: description-only family match in range, or a primary
    family in range that carries a seniority flag."""
    if m.excluded_by or m.location_class not in ("corridor", "remote_us"):
        return False
    return bool(m.secondary) and not m.families


def is_near_miss(m: Match, rules: dict) -> bool:
    """Logged so rule gaps are visible: a family match outside the location
    rule, or an in-range title with an AI-ish word but no family."""
    if m.excluded_by:
        return False
    if m.families and m.location_class == "exception":
        return True
    if not m.families and not m.secondary and m.location_class in ("corridor", "remote_us"):
        return _any(norm(m.posting.title), [norm(x) for x in rules.get("near_miss_hints", [])])
    return False
