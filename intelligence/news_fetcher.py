from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import feedparser
import yaml

from intelligence.models import Article


def load_sources(path: str = "config/sources.yaml") -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)["sources"]


def normalize(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def parse_entry_datetime(entry) -> datetime | None:
    for key in ("published", "updated", "created"):
        raw = entry.get(key)
        if not raw:
            continue
        try:
            parsed = parsedate_to_datetime(raw)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except (TypeError, ValueError):
            continue
    return None


def is_valid_article(title: str, published_at: datetime | None, link: str) -> bool:
    if not title or not link or not published_at:
        return False
    if link.startswith("javascript:"):
        return False
    if not link.startswith(("http://", "https://")):
        return False
    return True


def fetch_from_source(source: dict, cutoff: datetime) -> list[Article]:
    parsed = feedparser.parse(source["url"])
    articles: list[Article] = []

    for entry in parsed.entries:
        title = normalize(entry.get("title"))
        link = normalize(entry.get("link"))
        summary = normalize(entry.get("summary") or entry.get("description"))
        published_dt = parse_entry_datetime(entry)

        if not is_valid_article(title, published_dt, link):
            continue
        if published_dt < cutoff:
            continue

        articles.append(
            Article(
                title=title,
                published_at=published_dt.isoformat(),
                source_name=source["name"],
                source_url=source["url"],
                original_url=link,
                category=source["category"],
                raw_summary=summary[:700],
                verified=True,
                trust_score=int(source.get("trust", 60)),
            )
        )

    return articles


def fetch_news(lookback_hours: int) -> list[Article]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    result: list[Article] = []

    for source in load_sources():
        if source.get("type") != "rss":
            continue
        try:
            result.extend(fetch_from_source(source, cutoff))
        except Exception as exc:
            print(f"source failed: {source.get('name')} - {exc}")

    return result
