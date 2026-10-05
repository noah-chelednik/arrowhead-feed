"""Lever job boards.

Public endpoint: https://api.lever.co/v0/postings/{slug}?mode=json
Returns a list. Each posting has id, text (title), categories{location, team,
commitment, allLocations[]}, hostedUrl, createdAt (ms), workplaceType,
salaryRange{min,max,currency,interval}, descriptionPlain.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..models import Company, Posting
from ._http import get_json

BASE = "https://api.lever.co/v0/postings/{slug}?mode=json"


def _pay(j: dict) -> str:
    s = j.get("salaryRange") or {}
    if s.get("min") and s.get("max"):
        cur = s.get("currency") or ""
        return f"{cur} {int(s['min']):,}-{int(s['max']):,} {s.get('interval') or ''}".strip()
    return ""


def parse(company: Company, data: list) -> list[Posting]:
    out = []
    for j in data:
        cats = j.get("categories") or {}
        locs = cats.get("allLocations") or [cats.get("location") or ""]
        location = " | ".join(x for x in dict.fromkeys(locs) if x)
        created = j.get("createdAt")
        posted = ""
        if isinstance(created, (int, float)):
            posted = datetime.fromtimestamp(created / 1000, tz=timezone.utc).date().isoformat()
        wt = (j.get("workplaceType") or "").lower()
        out.append(Posting(
            key=f"lever:{company.slug}:{j['id']}",
            company=company.name,
            tier=company.tier,
            title=j.get("text") or "",
            url=j.get("hostedUrl") or j.get("applyUrl") or "",
            location=location,
            remote=wt == "remote" or "remote" in location.lower(),
            department=cats.get("team") or "",
            pay=_pay(j),
            posted=posted,
            description=(j.get("descriptionPlain") or "")[:4000],
        ))
    return out


def fetch(company: Company) -> list[Posting]:
    data = get_json(BASE.format(slug=company.slug))
    if not isinstance(data, list):
        raise RuntimeError(f"unexpected lever response for {company.slug}")
    return parse(company, data)
