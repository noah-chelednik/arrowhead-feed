"""Data types shared across the feed."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Company:
    name: str
    ats: str
    slug: Optional[str]
    tier: int
    careers_url: str = ""
    nyc: bool = False
    dc: bool = False
    remote_us: bool = False
    notes: str = ""
    # Optional filter applied before rules: keep only postings whose
    # department/team or title contains one of these strings (case-insensitive).
    # Used for shared boards (Handshake 'HAI', CoreWeave 'Weights & Biases').
    include_if: list[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class Posting:
    key: str                 # "<ats>:<slug>:<id>", stable across runs
    company: str
    tier: int
    title: str
    url: str
    location: str            # raw location string(s), joined with " | "
    remote: bool
    department: str = ""
    pay: str = ""
    posted: str = ""         # ISO date if the ATS gives one
    description: str = ""    # plain text, truncated; used for secondary matching

    def to_public(self) -> dict:
        d = asdict(self)
        d.pop("description", None)
        return d


@dataclass
class Match:
    posting: Posting
    families: list[str]      # families matched on the title
    secondary: list[str]     # families matched only in the description
    location_class: str      # corridor | remote_us | exception | unknown
    seniority_flags: list[str]
    excluded_by: Optional[str] = None

    def to_dict(self) -> dict:
        d = self.posting.to_public()
        d.update(
            families=self.families,
            secondary=self.secondary,
            location_class=self.location_class,
            seniority_flags=self.seniority_flags,
            excluded_by=self.excluded_by,
        )
        return d
