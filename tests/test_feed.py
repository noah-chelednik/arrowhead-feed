import json
from datetime import date
from pathlib import Path

from arrowhead_feed import config, feed
from arrowhead_feed.fetchers import ashby
from arrowhead_feed.models import Company

FIX = Path(__file__).parent / "fixtures"


def test_run_dedupes_and_writes(tmp_path, monkeypatch):
    """Two runs over the same fixture: the second reports nothing new."""
    data = json.load(open(FIX / "ashby_sample.json"))
    company = Company(name="Surge AI", ats="ashby", slug="surge-ai", tier=2)

    def fake_fetch(c):
        return ashby.parse(c, data)

    monkeypatch.setattr(feed, "fetch", fake_fetch)
    seen = tmp_path / "seen.json"
    rules = config.load_rules()

    r1 = feed.run([company], rules, seen_path=seen, today=date(2026, 10, 6))
    assert r1.counts["Surge AI"] == 3
    assert not r1.errors
    first_total = len(r1.new_primary) + len(r1.new_secondary) + len(r1.new_near_misses)
    assert r1.seen_added == first_total

    r2 = feed.run([company], rules, seen_path=seen, today=date(2026, 10, 13))
    assert len(r2.new_primary) + len(r2.new_secondary) + len(r2.new_near_misses) == 0

    j, m = feed.write_outputs(r1, out_dir=tmp_path / "feed", today=date(2026, 10, 6), manual_watch=[])
    payload = json.load(open(j))
    assert payload["date"] == "2026-10-06"
    assert "new_primary" in payload
    text = open(m).read()
    assert text.startswith("# Arrowhead feed, 2026-10-06")


def test_fetch_error_is_recorded(tmp_path, monkeypatch):
    company = Company(name="Broken", ats="lever", slug="nope", tier=3)

    def boom(c):
        raise RuntimeError("HTTP 404")

    monkeypatch.setattr(feed, "fetch", boom)
    r = feed.run([company], config.load_rules(), seen_path=tmp_path / "seen.json")
    assert "Broken" in r.errors


def test_companies_yaml_loads_and_slugs_unique():
    cos = config.load_companies()
    assert len(cos) > 100
    keys = [(c.ats, c.slug) for c in cos if c.slug]
    assert len(keys) == len(set(keys)), "duplicate ats/slug in companies.yaml"
    for c in cos:
        assert c.ats in ("greenhouse", "ashby", "lever", "workable"), c.name
        assert 1 <= c.tier <= 9, c.name


def test_include_if_filter():
    from arrowhead_feed.models import Posting
    c = Company(name="H", ats="ashby", slug="handshake", tier=2, include_if=["HAI"])
    yes = Posting(key="a", company="H", tier=2, title="Ops", url="", location="NYC", remote=False, department="HAI Delivery Ops")
    no = Posting(key="b", company="H", tier=2, title="Ops", url="", location="NYC", remote=False, department="Sales")
    assert feed._include(c, yes) and not feed._include(c, no)


def test_write_outputs_never_overwrites(tmp_path):
    from datetime import date
    from arrowhead_feed.feed import RunResult, write_outputs
    r = RunResult(run_at="2026-10-05T00:00:00+00:00")
    d = date(2026, 10, 5)
    j1, m1 = write_outputs(r, out_dir=tmp_path, today=d, manual_watch=[])
    j2, m2 = write_outputs(r, out_dir=tmp_path, today=d, manual_watch=[])
    assert j1.name == "2026-10-05.json" and j2.name == "2026-10-05-run2.json"
    assert j1.exists() and j2.exists() and m1.exists() and m2.exists()
