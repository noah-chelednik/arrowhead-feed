"""One fetcher per hiring system. Each returns a list of Posting."""

from __future__ import annotations

from typing import Callable

from ..models import Company, Posting
from . import ashby, greenhouse, lever

FETCHERS: dict[str, Callable[[Company], list[Posting]]] = {
    "greenhouse": greenhouse.fetch,
    "ashby": ashby.fetch,
    "lever": lever.fetch,
}


def fetch(company: Company) -> list[Posting]:
    fn = FETCHERS.get(company.ats)
    if fn is None:
        raise ValueError(f"no fetcher for ats={company.ats!r} ({company.name})")
    return fn(company)
