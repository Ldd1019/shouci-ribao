from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime
from typing import Any

import requests

from intelligence.models import Article


SYSTEM_PROMPT = """
你是全球科技资本市场投行晨会分析师。
你只能基于用户提供的真实新闻 JSON 输出分析。
严禁编造新闻、股价、融资、并购、财务数据、人物发言、监管动态或来源。
如果材料不足，必须写“今日无可靠更新”或“未找到可靠来源，不纳入本日报”。
所有结论必须绑定过去24小时内的可验证来源。
输出必须是中文，且必须是合法 JSON。
"""


TRACKED_COMPANIES = ["NVDA", "AMD", "MSFT", "GOOGL", "META", "AMZN", "AAPL", "TSLA", "PLTR", "AVGO", "SMCI", "TSM"]
TRACKED_PEOPLE = ["Elon Musk", "Jensen Huang", "Sam Altman", "Mark Zuckerberg", "Jeff Bezos", "孙宇晨", "Vitalik Buterin", "Cathie Wood"]
TRACKED_SECTORS = ["AI", "半导体", "机器人", "新能源", "互联网", "云计算", "网络安全", "加密货币"]


def article_dicts(articles: list[Article]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for article in articles:
        result.append(
            {
                "title": article.title,
                "published_at": article.published_at,
                "source_name": article.source_name,
                "original_url": article.original_url,
                "category": article.category,
                "raw_summary": _short(article.raw_summary, 260),
                "importance_score": article.importance_score,
                "reason_for_selection": article.reason_for_selection,
            }
        )
    return result


def _stars(value: int) -> str:
    value = max(1, min(5, value))
    return "★" * value + "☆" * (5 - value)


def _short(value: str, limit: int = 110) -> str:
    text = " ".join((value or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _contains(article: Article, keyword: str) -> bool:
    return keyword.lower() in f"{article.title} {article.raw_summary}".lower()


def fallback_report(articles: list[Article], report_date: str) -> dict[str, Any]:
    ranked = sorted(articles, key=lambda item: item.importance_score, reverse=True)
    top = ranked[:10]

    top_news = []
    for index, item in enumerate(top, start=1):
        top_news.append(
            {
                "rank": index,
                "title": item.title,
                "summary": _short(item.raw_summary or item.title, 130),
                "source": item.source_name,
                "published_at": item.published_at,
                "companies": "不足以判断",
                "countries": "不足以判断",
                "importance": _stars(4 if index <= 3 else 3),
                "sector": item.category,
                "sentiment": "中性",
                "bank_view": item.reason_for_selection or "来源可信，需结合后续市场反应观察。",
                "risk": "本地降级模式未做扩展推断，请以原文为准。",
                "url": item.original_url,
            }
        )

    if not top_news:
        top_news.append(
            {
                "rank": 1,
                "title": "今日无可靠更新",
                "summary": "过去24小时内未抓取到满足来源、时间和链接要求的可靠科技资本市场新闻。",
                "source": "系统筛选",
                "published_at": report_date,
                "companies": "无",
                "countries": "全球",
                "importance": _stars(1),
                "sector": "综合",
                "sentiment": "中性",
                "bank_view": "宁可少写，也不使用旧新闻或不可验证信息凑数。",
                "risk": "新闻源不足。",
                "url": "",
            }
        )

    capital_flows = []
    for sector in TRACKED_SECTORS:
        related = [item for item in ranked if _contains(item, sector) or _contains(item, sector.lower())]
        capital_flows.append(
            {
                "sector": sector,
                "heat": _stars(4 if related else 2),
                "capital_attention": "高" if related else "观察",
                "driver": _short(related[0].title, 75) if related else "今日无可靠更新",
                "representative_companies": "见新闻原文" if related else "不足以判断",
                "outlook": "跟踪后续公告、财报、监管或资金流信息，不基于旧信息外推。",
            }
        )

    deep_dives = []
    for item in top[:3]:
        deep_dives.append(
            {
                "event": item.title,
                "what_happened": _short(item.raw_summary or item.title, 150),
                "why_important": item.reason_for_selection,
                "supply_chain_impact": "不足以判断",
                "revenue_impact": "不足以判断",
                "profit_impact": "不足以判断",
                "valuation_impact": "不足以判断",
                "sentiment_impact": "中性偏观察",
                "short_term_opportunity": "仅作为观察逻辑，不构成买卖建议。",
                "long_term_logic": "需要等待更多官方数据验证。",
                "core_risk": "信息不足或市场反应可能与新闻方向不一致。",
                "source": item.source_name,
                "url": item.original_url,
            }
        )
    while len(deep_dives) < 3:
        deep_dives.append(
            {
                "event": "今日无可靠更新",
                "what_happened": "未找到足够可靠来源。",
                "why_important": "不使用不可验证信息补齐。",
                "supply_chain_impact": "不足以判断",
                "revenue_impact": "不足以判断",
                "profit_impact": "不足以判断",
                "valuation_impact": "不足以判断",
                "sentiment_impact": "不足以判断",
                "short_term_opportunity": "无",
                "long_term_logic": "无",
                "core_risk": "数据不足",
                "source": "系统筛选",
                "url": "",
            }
        )

    return {
        "title": "全球科技资本市场日报",
        "subtitle": "Technology & Capital Market Daily Briefing",
        "date": report_date,
        "core_conclusions": [
            "本报告仅保留具备标题、发布时间、来源和原文链接的新闻。",
            "OpenAI 不可用时，系统自动降级为真实新闻源基础框架，不编造事实。",
            "重点关注 AI、半导体、加密货币、机器人和美股科技巨头的可验证事件。",
            "未找到可靠来源的事件不纳入正文。",
        ],
        "top_news": top_news,
        "capital_flows": capital_flows,
        "deep_dives": deep_dives,
        "leader_views": [
            {
                "person": name,
                "role": "重点跟踪人物",
                "latest_comment": "今日无可靠更新",
                "translation": "今日无可靠更新",
                "source": "系统筛选",
                "published_at": report_date,
                "attention": _stars(1),
                "sector": "科技/资本市场",
                "impacted_companies": "不足以判断",
                "bank_view": "未找到可靠来源，不纳入投资依据。",
                "credibility": _stars(1),
            }
            for name in TRACKED_PEOPLE
        ],
        "mega_cap_tracking": [
            {
                "ticker": ticker,
                "news": "今日无可靠更新",
                "sentiment": "中性",
                "short_term": "观察",
                "long_term": "等待官方信息",
                "rating": "★★★☆☆ 观察",
            }
            for ticker in TRACKED_COMPANIES
        ],
        "ai_chain": [
            {"layer": "模型层", "beneficiaries": "不足以判断", "losers": "不足以判断", "trend": "跟踪模型发布与商业化数据"},
            {"layer": "算力层", "beneficiaries": "不足以判断", "losers": "不足以判断", "trend": "跟踪 GPU、数据中心、电力约束"},
            {"layer": "芯片层", "beneficiaries": "不足以判断", "losers": "不足以判断", "trend": "跟踪 HBM、先进封装、代工产能"},
            {"layer": "应用层", "beneficiaries": "不足以判断", "losers": "不足以判断", "trend": "跟踪付费转化和企业部署"},
        ],
        "crypto": {
            "btc": "今日无可靠更新",
            "eth": "今日无可靠更新",
            "sol": "今日无可靠更新",
            "trx": "今日无可靠更新",
            "stablecoins": "今日无可靠更新",
            "etf_flows": "今日无可靠更新",
            "regulation": "今日无可靠更新",
            "institutional": "今日无可靠更新",
            "risks": "高波动、监管和流动性风险仍需跟踪。",
        },
        "opportunity_pool": {
            "short_term": [{"target": "无明确建议", "logic": "仅观察新闻催化", "catalyst": "可靠来源不足", "risk": "不构成买卖建议", "watch": "等待新公告"}],
            "mid_term": [{"target": "无明确建议", "logic": "等待趋势确认", "catalyst": "财报/监管/发布会", "risk": "估值波动", "watch": "资金流向"}],
            "long_term": [{"target": "无明确建议", "logic": "关注产业链确定性", "catalyst": "订单/收入/利润验证", "risk": "竞争与周期", "watch": "官方数据"}],
        },
        "risk_alerts": ["政策监管风险", "地缘政治风险", "财报和指引风险", "估值泡沫风险", "供应链风险", "行业竞争风险"],
        "next_72h": {
            "24h": ["跟踪公司公告、SEC文件、监管动态"],
            "48h": ["跟踪财报、发布会、行业会议"],
            "72h": ["跟踪宏观数据、ETF资金流、供应链新闻"],
        },
        "sources": [{"source": item.source_name, "title": item.title, "published_at": item.published_at, "url": item.original_url} for item in ranked[:30]],
    }


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned).strip()
    return json.loads(cleaned)


def build_capital_market_report(articles: list[Article], report_date: str | None = None) -> dict[str, Any]:
    report_date = report_date or datetime.now().strftime("%Y-%m-%d")
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    max_articles = int(os.getenv("OPENAI_MAX_ARTICLES", "15"))

    if not api_key:
        return fallback_report(articles, report_date)

    prompt = f"""
请基于以下过去24小时内真实新闻 JSON，生成《全球科技资本市场日报（投行版）》结构化 JSON。

硬性要求：
- 只使用输入新闻，不得编造。
- 所有输出中文。
- 每条新闻必须保留来源、原始标题、发布时间、链接。
- 无可靠更新时写“今日无可靠更新”。
- 禁止明确买卖建议，只能给观察逻辑。
- 输出必须是合法 JSON，不要 Markdown。

请输出以下字段：
title, subtitle, date, core_conclusions, top_news, capital_flows, deep_dives,
leader_views, mega_cap_tracking, ai_chain, crypto, opportunity_pool, risk_alerts, next_72h, sources。

新闻 JSON：
{json.dumps(article_dicts(articles[:max_articles]), ensure_ascii=False, separators=(",", ":"))}
"""

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "temperature": 0.1,
                    "max_tokens": 3500,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                },
                timeout=120,
            )
            response.raise_for_status()
            parsed = _extract_json(response.json()["choices"][0]["message"]["content"])
            parsed.setdefault("date", report_date)
            return parsed
        except requests.HTTPError as exc:
            last_error = exc
            status = exc.response.status_code if exc.response is not None else None
            if status != 429 or attempt == 2:
                break
            time.sleep(5 * (attempt + 1))
        except Exception as exc:
            last_error = exc
            break

    print(f"Capital market report fallback used: {last_error}")
    return fallback_report(articles, report_date)
