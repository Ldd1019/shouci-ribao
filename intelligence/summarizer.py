from __future__ import annotations

import json
import os

import requests


SYSTEM_PROMPT = """
你是中文行业情报分析师。
你只能基于用户提供的 JSON 新闻材料写简报。
禁止创造新闻、融资事件、收购事件、产品发布、公司动作、金额、人物或时间。
如果材料中没有，就写“不足以判断”。
每条新闻必须保留原文链接。
AI只允许做：中文翻译、内容总结、行业分类、趋势分析。
"""


def fallback(grouped: dict) -> str:
    lines = ["1. 今日重点摘要", "", "未配置 OpenAI API，以下为真实新闻源抓取结果，未做 AI 深度总结。", ""]
    section_names = {
        "finance": "2. 金融行业动态",
        "technology": "3. 科技行业动态",
        "pet": "4. 宠物行业动态",
    }

    for key, title in section_names.items():
        lines += [title, ""]
        items = grouped.get(key, [])
        if not items:
            lines += ["过去24小时内可验证新闻不足。", ""]
            continue
        for item in items:
            lines += [
                f"新闻标题：{item['title']}",
                f"来源：{item['source_name']}",
                f"发布时间：{item['published_at']}",
                "简短中文总结：未启用 AI，总结暂缺。",
                f"为什么值得关注：{item['reason_for_selection']}",
                f"原文链接：{item['original_url']}",
                "",
            ]

    lines += [
        "5. 值得关注的优质企业",
        "",
        "未启用 AI，暂不自动筛选。",
        "",
        "6. 趋势判断",
        "",
        "未启用 AI，暂不自动判断。",
        "",
        "7. 数据可信度说明",
        "",
        "本邮件仅收录 RSS 或配置新闻源返回且具备标题、发布时间、来源和链接的条目。",
    ]
    return "\n".join(lines)


def summarize(grouped: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    if not api_key:
        return fallback(grouped)

    prompt = f"""
请根据以下真实新闻源 JSON 生成中文行业情报邮件正文。

必须使用结构：
1. 今日重点摘要
2. 金融行业动态
3. 科技行业动态
4. 宠物行业动态
5. 值得关注的优质企业
6. 趋势判断
7. 数据可信度说明

硬性规则：
- 不允许添加 JSON 中不存在的新闻。
- 不允许推测融资、并购、发布、合作、金额。
- 每条新闻必须包含标题、来源、发布时间、原文链接。
- 如果某类新闻不足，明确写“过去24小时内可验证新闻不足”。
- 趋势判断只能基于已列新闻，不能泛泛编造。

新闻 JSON：
{json.dumps(grouped, ensure_ascii=False, indent=2)}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
