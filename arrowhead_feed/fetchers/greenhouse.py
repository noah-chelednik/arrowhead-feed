"""Greenhouse job boards.

Public endpoint: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
Returns {"jobs": [...], "meta": {"total": n}}. Each job has id, title, location.name,
absolute_url, updated_at, first_published, departments[], offices[], content (HTML).
"""

from __future__ import annotations

from ..models import Company, Posting
from ._http import get_json, strip_html

BASE = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"


def parse(company: Company, data: dict) -> list[Posting]:
    out = []
    for j in data.get("jobs", []):
        loc = (j.get("location") or {}).get("name") or ""
        offices = [o.get("name") for o in j.get("offices") or [] if o.get("name")]
        location = " | ".join(dict.fromkeys([loc, *offices])) if offices else loc
        depts = [d.get("name") for d in j.get("departments") or [] if d.get("name")]
        remote = "remote" in location.lower()
        pay = ""
        meta = j.get("metadata") or []
        for m in meta:
            name = (m.get("name") or "").lower()
            if "salary" in name or "compensation" in name or "pay" in name:
                if m.get("value"):
                    pay = str(m["value"])[:120]
                    break
        out.append(Posting(
            key=f"greenhouse:{company.slug}:{j['id']}",
            company=company.name,
            tier=company.tier,
            title=j.get("title") or "",
            url=j.get("absolute_url") or "",
            location=location,
            remote=remote,
            department=", ".join(depts),
            pay=pay,
            posted=(j.get("first_published") or j.get("updated_at") or "")[:10],
            description=strip_html(j.get("content") or ""),
        ))
    return out


def fetch(company: Company) -> list[Posting]:
    data = get_json(BASE.format(slug=company.slug))
    return parse(company, data)
