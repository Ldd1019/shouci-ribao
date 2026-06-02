from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class Article:
    title: str
    published_at: str
    source_name: str
    source_url: str
    original_url: str
    category: str
    raw_summary: str
    verified: bool
    trust_score: int
    importance_score: int = 0
    reason_for_selection: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def parse_dt(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
