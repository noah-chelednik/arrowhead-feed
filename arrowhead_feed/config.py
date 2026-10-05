"""Load config/companies.yaml, config/rules.yaml, config/manual_watch.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import Company

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
DATA = ROOT / "data"
FEED = ROOT / "feed"


def load_rules(path: Path | None = None) -> dict:
    with open(path or CONFIG / "rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_companies(path: Path | None = None) -> list[Company]:
    with open(path or CONFIG / "companies.yaml", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or []
    out = []
    for r in raw:
        out.append(Company(
            name=r["name"],
            ats=r["ats"],
            slug=r.get("slug"),
            tier=int(r.get("tier", 3)),
            careers_url=r.get("careers_url", "") or "",
            nyc=bool(r.get("nyc", False)),
            dc=bool(r.get("dc", False)),
            remote_us=bool(r.get("remote_us", False)),
            notes=r.get("notes", "") or "",
            include_if=list(r.get("include_if", []) or []),
            enabled=bool(r.get("enabled", True)),
        ))
    return out


def load_manual_watch(path: Path | None = None) -> list[dict]:
    p = path or CONFIG / "manual_watch.yaml"
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or []
