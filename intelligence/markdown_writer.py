from __future__ import annotations

from pathlib import Path
from typing import Any


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def build_executive_summary(report: dict[str, Any]) -> str:
    lines = [
        f"# Executive Summary - {report.get('date', '')}",
        "",
        "## 今日核心结论",
    ]
    for item in _list(report.get("core_conclusions"))[:5]:
        lines.append(f"- {item}")

    lines += ["", "## 今日最重要新闻"]
    for item in _list(report.get("top_news"))[:5]:
        item = _dict(item)
        lines.append(f"- {item.get('importance', '')} {item.get('title', '')} | {item.get('sentiment', '中性')} | {item.get('bank_view', '')}")

    lines += ["", "## 未来24小时关注"]
    for item in _list(_dict(report.get("next_72h")).get("24h")):
        lines.append(f"- {item}")

    lines += ["", "完整 PPTX 和 Markdown 版本见附件。"]
    return "\n".join(lines).strip() + "\n"


def build_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        f"# {report.get('title', '全球科技资本市场日报')}",
        "",
        f"**日期：** {report.get('date', '')}",
        "",
        "## 今日核心结论",
    ]
    for item in _list(report.get("core_conclusions")):
        lines.append(f"- {item}")

    lines += ["", "## 全球科技新闻 Top10"]
    for item in _list(report.get("top_news")):
        item = _dict(item)
        lines += [
            f"### {item.get('rank', '')}. {item.get('title', '')}",
            f"- 中文摘要：{item.get('summary', '')}",
            f"- 来源：{item.get('source', '')}",
            f"- 发布时间：{item.get('published_at', '')}",
            f"- 涉及公司：{item.get('companies', '')}",
            f"- 涉及国家：{item.get('countries', '')}",
            f"- 重要性：{item.get('importance', '')}",
            f"- 影响板块：{item.get('sector', '')}",
            f"- 方向：{item.get('sentiment', '')}",
            f"- 投行视角：{item.get('bank_view', '')}",
            f"- 风险提示：{item.get('risk', '')}",
            f"- 原文链接：{item.get('url', '')}",
            "",
        ]

    lines += ["## 全球资本流向"]
    for item in _list(report.get("capital_flows")):
        item = _dict(item)
        lines.append(
            f"- **{item.get('sector', '')}**：热度 {item.get('heat', '')}；资金关注度 {item.get('capital_attention', '')}；驱动：{item.get('driver', '')}；判断：{item.get('outlook', '')}"
        )

    lines += ["", "## 深度分析"]
    for item in _list(report.get("deep_dives")):
        item = _dict(item)
        lines += [
            f"### {item.get('event', '')}",
            f"- 发生了什么：{item.get('what_happened', '')}",
            f"- 为什么重要：{item.get('why_important', '')}",
            f"- 产业链影响：{item.get('supply_chain_impact', '')}",
            f"- 收入影响：{item.get('revenue_impact', '')}",
            f"- 利润影响：{item.get('profit_impact', '')}",
            f"- 估值影响：{item.get('valuation_impact', '')}",
            f"- 市场情绪影响：{item.get('sentiment_impact', '')}",
            f"- 短期交易观察：{item.get('short_term_opportunity', '')}",
            f"- 中长期逻辑：{item.get('long_term_logic', '')}",
            f"- 核心风险：{item.get('core_risk', '')}",
            f"- 来源：{item.get('source', '')} {item.get('url', '')}",
            "",
        ]

    lines += ["## 科技大佬观点追踪"]
    for item in _list(report.get("leader_views")):
        item = _dict(item)
        lines.append(f"- {item.get('person', '')}：{item.get('latest_comment', '')} | 可信度 {item.get('credibility', '')} | {item.get('bank_view', '')}")

    lines += ["", "## 美股科技巨头追踪"]
    for item in _list(report.get("mega_cap_tracking")):
        item = _dict(item)
        lines.append(f"- {item.get('ticker', '')}：{item.get('news', '')} | 情绪 {item.get('sentiment', '')} | 关注等级 {item.get('rating', '')}")

    lines += ["", "## AI产业链跟踪"]
    for item in _list(report.get("ai_chain")):
        item = _dict(item)
        lines.append(f"- {item.get('layer', '')}：受益 {item.get('beneficiaries', '')}；受损 {item.get('losers', '')}；趋势 {item.get('trend', '')}")

    crypto = _dict(report.get("crypto"))
    lines += [
        "",
        "## 加密货币市场跟踪",
        f"- BTC：{crypto.get('btc', '')}",
        f"- ETH：{crypto.get('eth', '')}",
        f"- SOL：{crypto.get('sol', '')}",
        f"- TRX：{crypto.get('trx', '')}",
        f"- 稳定币：{crypto.get('stablecoins', '')}",
        f"- ETF资金流：{crypto.get('etf_flows', '')}",
        f"- 监管动态：{crypto.get('regulation', '')}",
        f"- 机构入场：{crypto.get('institutional', '')}",
        f"- 风险：{crypto.get('risks', '')}",
        "",
        "## 交易机会观察池",
    ]
    pool = _dict(report.get("opportunity_pool"))
    for key, label in [("short_term", "短线投机机会"), ("mid_term", "中线波段机会"), ("long_term", "长线投资机会")]:
        lines.append(f"### {label}")
        for item in _list(pool.get(key)):
            item = _dict(item)
            lines.append(f"- {item.get('target', '')}：逻辑 {item.get('logic', '')}；催化剂 {item.get('catalyst', '')}；风险 {item.get('risk', '')}；关注 {item.get('watch', '')}")

    lines += ["", "## 风险预警"]
    for item in _list(report.get("risk_alerts")):
        lines.append(f"- {item}")

    lines += ["", "## 未来72小时关注清单"]
    next_72h = _dict(report.get("next_72h"))
    for key in ["24h", "48h", "72h"]:
        lines.append(f"### {key}")
        for item in _list(next_72h.get(key)):
            lines.append(f"- {item}")

    lines += ["", "## 信息来源汇总"]
    for item in _list(report.get("sources")):
        item = _dict(item)
        lines.append(f"- {item.get('source', '')} | {item.get('published_at', '')} | {item.get('title', '')} | {item.get('url', '')}")

    return "\n".join(lines).strip() + "\n"


def write_markdown_files(report: dict[str, Any], output_dir: str | Path) -> tuple[Path, Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    date = report.get("date", "")
    summary_path = output / f"Executive-Summary-{date}.md"
    report_path = output / f"全球科技资本市场日报-{date}.md"
    summary_path.write_text(build_executive_summary(report), encoding="utf-8")
    report_path.write_text(build_markdown_report(report), encoding="utf-8")
    return summary_path, report_path
