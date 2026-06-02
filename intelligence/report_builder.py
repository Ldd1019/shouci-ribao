from __future__ import annotations

from intelligence.models import Article
from intelligence.summarizer import summarize


def to_serializable(grouped: dict[str, list[Article]]) -> dict:
    return {
        category: [article.to_dict() for article in articles]
        for category, articles in grouped.items()
    }


def build_report(grouped: dict[str, list[Article]]) -> str:
    return summarize(to_serializable(grouped))
