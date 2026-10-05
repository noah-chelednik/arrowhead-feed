"""Ashby job boards.

Public posting API: https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true
Returns {"jobs": [...]}. Each job has id, title, location, secondaryLocations[],
department, team, isRemote, jobUrl, publishedAt, descriptionPlain, compensation.

Some companies disable the posting API but keep the hosted board. For those the
hosted GraphQL works (no descriptions):
POST https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams
"""

from __future__ import annotations

from urllib.parse import quote

from ..models import Company, Posting
from ._http import get_json, post_json

BASE = "https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"
GRAPHQL = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams"
GRAPHQL_QUERY = """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {
    jobPostings { id title locationName secondaryLocations { locationName } teamId employmentType compensationTierSummary workplaceType }
  }
}
"""


def _pay(j: dict) -> str:
    comp = j.get("compensation") or {}
    for k in ("scrapeableCompensationSalarySummary", "compensationTierSummary"):
        v = comp.get(k)
        if v:
            return str(v)[:120]
    return ""


def parse(company: Company, data: dict) -> list[Posting]:
    out = []
    for j in data.get("jobs", []):
        if j.get("isListed") is False:
            continue
        locs = [j.get("location") or ""]
        locs += [s.get("location") or "" for s in j.get("secondaryLocations") or []]
        location = " | ".join(x for x in dict.fromkeys(locs) if x)
        out.append(Posting(
            key=f"ashby:{company.slug}:{j['id']}",
            company=company.name,
            tier=company.tier,
            title=j.get("title") or "",
            url=j.get("jobUrl") or j.get("applyUrl") or "",
            location=location,
            remote=bool(j.get("isRemote")) or "remote" in location.lower(),
            department=", ".join(x for x in [j.get("department"), j.get("team")] if x),
            pay=_pay(j),
            posted=(j.get("publishedAt") or "")[:10],
            description=(j.get("descriptionPlain") or "")[:4000],
        ))
    return out


def parse_graphql(company: Company, data: dict) -> list[Posting]:
    out = []
    board = ((data.get("data") or {}).get("jobBoard") or {})
    for j in board.get("jobPostings") or []:
        locs = [j.get("locationName") or ""]
        locs += [s.get("locationName") or "" for s in j.get("secondaryLocations") or []]
        location = " | ".join(x for x in dict.fromkeys(locs) if x)
        out.append(Posting(
            key=f"ashby:{company.slug}:{j['id']}",
            company=company.name,
            tier=company.tier,
            title=j.get("title") or "",
            url=f"https://jobs.ashbyhq.com/{quote(company.slug)}/{j['id']}",
            location=location,
            remote=(j.get("workplaceType") or "").lower() == "remote" or "remote" in location.lower(),
            department="",
            pay=str(j.get("compensationTierSummary") or "")[:120],
            posted="",
            description="",
        ))
    return out


def fetch(company: Company) -> list[Posting]:
    url = BASE.format(slug=quote(company.slug, safe=""))
    try:
        data = get_json(url)
        if isinstance(data, dict) and "jobs" in data:
            return parse(company, data)
    except RuntimeError:
        pass
    # Fallback: hosted board GraphQL (posting API disabled or 404).
    payload = {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {"organizationHostedJobsPageName": company.slug},
        "query": GRAPHQL_QUERY,
    }
    data = post_json(GRAPHQL, payload, headers={"Content-Type": "application/json"})
    if not ((data.get("data") or {}).get("jobBoard")):
        raise RuntimeError(f"ashby board not found: {company.slug}")
    return parse_graphql(company, data)
