"""Shared HTTP helper: one session, a polite user agent, retries, timeouts."""

from __future__ import annotations

import time

import requests

USER_AGENT = "arrowhead-feed/1.0 (personal job-search feed; contact via repository)"
TIMEOUT = 60
RETRIES = 3


_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})


def get_json(url: str, **kwargs):
    last = None
    for attempt in range(RETRIES):
        try:
            r = _session.get(url, timeout=TIMEOUT, **kwargs)
            if r.status_code == 429 or r.status_code >= 500:
                last = RuntimeError(f"HTTP {r.status_code} from {url}")
                time.sleep(2 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:  # ValueError: bad JSON
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed after {RETRIES} attempts: {last}")


def post_json(url: str, payload: dict, headers: dict | None = None):
    last = None
    for attempt in range(RETRIES):
        try:
            r = _session.post(url, json=payload, timeout=TIMEOUT, headers=headers or {})
            if r.status_code == 429 or r.status_code >= 500:
                last = RuntimeError(f"HTTP {r.status_code} from {url}")
                time.sleep(2 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed after {RETRIES} attempts: {last}")


def strip_html(html: str, limit: int = 4000) -> str:
    """Cheap HTML to text. Good enough for keyword matching."""
    import re
    import html as html_mod

    # Greenhouse ships content HTML-escaped (&lt;p&gt;), so unescape first,
    # strip tags, then unescape once more for entities inside the text.
    text = html_mod.unescape(html or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_mod.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]
