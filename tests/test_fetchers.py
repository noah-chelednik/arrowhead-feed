import json
from pathlib import Path

from arrowhead_feed.fetchers import ashby, greenhouse, lever
from arrowhead_feed.models import Company

FIX = Path(__file__).parent / "fixtures"


def _co(ats, slug):
    return Company(name="Test", ats=ats, slug=slug, tier=2)


def test_greenhouse_parse():
    data = json.load(open(FIX / "greenhouse_sample.json"))
    posts = greenhouse.parse(_co("greenhouse", "haizelabs"), data)
    assert len(posts) == 3
    p = posts[0]
    assert p.key.startswith("greenhouse:haizelabs:")
    assert p.title and p.url.startswith("https://")
    assert p.location
    assert "<" not in p.description  # html stripped


def test_ashby_parse():
    data = json.load(open(FIX / "ashby_sample.json"))
    posts = ashby.parse(_co("ashby", "surge-ai"), data)
    assert len(posts) == 3
    p = posts[0]
    assert p.key.startswith("ashby:surge-ai:")
    assert p.remote is True
    assert "remote" in p.location.lower()


def test_lever_parse():
    data = json.load(open(FIX / "lever_sample.json"))
    posts = lever.parse(_co("lever", "epoch-ai"), data)
    assert len(posts) == 3
    p = posts[0]
    assert p.key.startswith("lever:epoch-ai:")
    assert p.posted and len(p.posted) == 10
    assert p.pay.startswith("USD")


def test_ashby_graphql_parse():
    data = {"data": {"jobBoard": {"jobPostings": [
        {"id": "abc", "title": "Deployment Strategist", "locationName": "Washington DC",
         "secondaryLocations": [{"locationName": "Remote - US"}], "teamId": "t1",
         "workplaceType": "Remote", "compensationTierSummary": None}]}}}
    posts = ashby.parse_graphql(_co("ashby", "chainalysis-government-solutions"), data)
    assert len(posts) == 1
    assert posts[0].url == "https://jobs.ashbyhq.com/chainalysis-government-solutions/abc"
    assert "Washington DC | Remote - US" == posts[0].location
