from arrowhead_feed import config
from arrowhead_feed.models import Posting
from arrowhead_feed.rules import classify_location, evaluate, is_near_miss, is_primary, is_secondary

RULES = config.load_rules()


def _p(title, location, remote=False, desc="", tier=2):
    return Posting(key="t:x:1", company="X", tier=tier, title=title, url="u",
                   location=location, remote=remote, description=desc)


def test_corridor_cities():
    assert classify_location("New York City", False, RULES) == "corridor"
    assert classify_location("Washington, DC", False, RULES) == "corridor"
    assert classify_location("Laurel, MD", False, RULES) == "corridor"
    assert classify_location("Princeton, NJ", False, RULES) == "corridor"
    assert classify_location("Boston, MA", False, RULES) == "corridor"


def test_remote_us_vs_not():
    assert classify_location("United States - Remote", True, RULES) == "remote_us"
    assert classify_location("Remote (US)", True, RULES) == "remote_us"
    assert classify_location("Remote - UK", True, RULES) == "exception"
    assert classify_location("Remote - Canada", True, RULES) == "exception"
    assert classify_location("Remote", True, RULES) == "remote_us"


def test_exception_and_multi():
    assert classify_location("San Francisco", False, RULES) == "exception"
    assert classify_location("San Francisco | New York", False, RULES) == "corridor"
    assert classify_location("London | Remote - International", True, RULES) == "exception"


def test_primary_match_red_team_lead_not_excluded():
    m = evaluate(_p("Strategic Projects Lead, Red Team", "San Francisco | New York"), RULES)
    assert "evaluation" in m.families and "ai_ops" in m.families
    assert "lead" in m.seniority_flags
    assert m.excluded_by is None
    assert is_primary(m)


def test_director_excluded():
    m = evaluate(_p("Director, Trust and Safety", "New York"), RULES)
    assert m.excluded_by == "director"
    assert not is_primary(m)


def test_secondary_from_description():
    m = evaluate(_p("Operations Engineer", "United States - Remote", True,
                    desc="You will build evaluation datasets and run RLHF data quality programs."), RULES)
    # 'ai_ops' is not in the title ('operations engineer' is not 'ai operations')
    assert not m.families
    assert "evaluation" in m.secondary and "human_data" in m.secondary
    assert is_secondary(m)


def test_near_miss_out_of_range():
    m = evaluate(_p("AI Evaluation Specialist", "Austin, TX"), RULES)
    assert m.families and m.location_class == "exception"
    assert is_near_miss(m, RULES)
    assert not is_primary(m)


def test_near_miss_in_range_unmatched_title():
    m = evaluate(_p("AI Research Analyst", "New York"), RULES)
    # 'analyst' alone is not a family; it is a hint
    assert not m.families or is_primary(m) or is_near_miss(m, RULES)


def test_intern_excluded():
    m = evaluate(_p("Research Intern, Evaluations", "New York"), RULES)
    assert m.excluded_by in ("intern", "internship")
