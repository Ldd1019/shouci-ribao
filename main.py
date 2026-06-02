from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from intelligence.capital_market_report import build_capital_market_report
from intelligence.deduplicator import deduplicate
from intelligence.email_sender import send_email
from intelligence.markdown_writer import build_executive_summary, write_markdown_files
from intelligence.news_fetcher import fetch_news
from intelligence.ppt_builder import build_pptx
from intelligence.ranker import rank_and_group


def report_date() -> str:
    configured = os.getenv("REPORT_DATE", "").strip()
    if configured:
        return configured.replace("/", "-")
    return datetime.now().strftime("%Y-%m-%d")


def run_once() -> None:
    load_dotenv()

    lookback_hours = int(os.getenv("LOOKBACK_HOURS", "24"))
    max_items = int(os.getenv("MAX_ITEMS_PER_CATEGORY", "10"))
    output_root = Path(os.getenv("OUTPUT_DIR", "outputs"))
    current_report_date = report_date()

    articles = fetch_news(lookback_hours)
    articles = deduplicate(articles)
    grouped = rank_and_group(articles, max_items)
    selected_articles = [
        article
        for category_items in grouped.values()
        for article in category_items
        if article.verified and article.original_url
    ]

    report = build_capital_market_report(selected_articles, current_report_date)
    daily_dir = output_root / current_report_date
    executive_path, markdown_path = write_markdown_files(report, daily_dir)
    pptx_path = build_pptx(report, daily_dir / f"全球科技资本市场日报-{current_report_date}.pptx")

    subject = f"全球科技资本市场日报 - {current_report_date}"
    body = build_executive_summary(report)
    send_email(subject, body, attachments=[str(pptx_path), str(executive_path), str(markdown_path)])
    print(f"sent: {subject}")


if __name__ == "__main__":
    run_once()
