from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv

from intelligence.deduplicator import deduplicate
from intelligence.email_sender import send_email
from intelligence.news_fetcher import fetch_news
from intelligence.ranker import rank_and_group
from intelligence.report_builder import build_report


def run_once() -> None:
    load_dotenv()

    lookback_hours = int(os.getenv("LOOKBACK_HOURS", "24"))
    max_items = int(os.getenv("MAX_ITEMS_PER_CATEGORY", "5"))

    articles = fetch_news(lookback_hours)
    articles = deduplicate(articles)
    grouped = rank_and_group(articles, max_items)

    body = build_report(grouped)
    subject = f"每日行业简报 - {datetime.now().strftime('%Y-%m-%d')}"

    send_email(subject, body)
    print(f"sent: {subject}")


if __name__ == "__main__":
    run_once()
