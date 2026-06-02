from __future__ import annotations

from intelligence.models import Article


IMPORTANT_TERMS = {
    "finance": [
        "funding",
        "ipo",
        "acquisition",
        "merger",
        "rate",
        "inflation",
        "central bank",
        "earnings",
        "guidance",
        "regulation",
        "payment",
        "fintech",
        "sec",
        "market",
        "crypto",
        "bitcoin",
        "ethereum",
        "etf",
        "stablecoin",
    ],
    "technology": [
        "ai",
        "chip",
        "semiconductor",
        "llm",
        "model",
        "launch",
        "open source",
        "robot",
        "robotics",
        "cloud",
        "security",
        "hardware",
        "nvidia",
        "amd",
        "microsoft",
        "google",
        "meta",
        "amazon",
        "apple",
        "tesla",
        "broadcom",
        "tsmc",
        "data center",
        "agent",
        "battery",
        "ev",
        "renewable",
    ],
    "pet": [
        "pet food",
        "veterinary",
        "acquisition",
        "funding",
        "launch",
        "recall",
        "smart pet",
        "pet health",
        "brand",
        "retail",
    ],
}


def score_article(article: Article) -> Article:
    text = f"{article.title} {article.raw_summary}".lower()
    score = article.trust_score
    matched: list[str] = []

    for term in IMPORTANT_TERMS.get(article.category, []):
        if term in text:
            score += 8
            matched.append(term)

    if any(signal in text for signal in ["exclusive", "breaking", "raises", "raised", "launches", "files", "reports"]):
        score += 10

    article.importance_score = min(score, 100)
    article.reason_for_selection = (
        "匹配重要信号：" + ", ".join(matched[:5])
        if matched
        else "来源可信且属于过去24小时内的相关行业新闻"
    )
    return article


def rank_and_group(articles: list[Article], max_per_category: int) -> dict[str, list[Article]]:
    grouped: dict[str, list[Article]] = {"finance": [], "technology": [], "pet": []}

    for article in articles:
        grouped.setdefault(article.category, []).append(score_article(article))

    for category in grouped:
        grouped[category].sort(key=lambda item: item.importance_score, reverse=True)
        grouped[category] = grouped[category][:max_per_category]

    return grouped
