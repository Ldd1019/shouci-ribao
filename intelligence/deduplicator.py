from __future__ import annotations

import re
from difflib import SequenceMatcher

from intelligence.models import Article


def clean_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^a-z0-9\u4e00-\u9fff ]+", " ", title)
    return " ".join(title.split())


def similar(left: str, right: str) -> bool:
    return SequenceMatcher(None, clean_title(left), clean_title(right)).ratio() >= 0.88


def deduplicate(articles: list[Article]) -> list[Article]:
    selected: list[Article] = []

    for article in sorted(articles, key=lambda item: item.trust_score, reverse=True):
        duplicate = False
        for existing in selected:
            if article.original_url == existing.original_url or similar(article.title, existing.title):
                duplicate = True
                break
        if not duplicate:
            selected.append(article)

    return selected
