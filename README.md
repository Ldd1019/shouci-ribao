# 全球科技资本市场日报（投行版）

这是一个真实新闻情报系统，不是 AI 新闻生成器。

系统每天抓取过去 24 小时内的真实新闻源，只允许 RSS、官方网站或新闻 API 进入分析链路。AI 只负责中文翻译、摘要、行业分类、投行视角分析和版式生成，不允许创造新闻、融资事件、收购事件、产品发布或人物发言。

## 默认收件人

```text
1432047156@qq.com
```

## 每天生成的内容

邮件标题：

```text
全球科技资本市场日报 - YYYY-MM-DD
```

邮件附件：

```text
全球科技资本市场日报-YYYY-MM-DD.pptx
Executive-Summary-YYYY-MM-DD.md
全球科技资本市场日报-YYYY-MM-DD.md
```

PPT 默认 13 页：

1. 封面
2. 今日核心结论
3. 全球科技新闻 Top10
4. 全球资本流向
5. 深度分析 1
6. 深度分析 2
7. 深度分析 3
8. 科技大佬观点追踪
9. 美股科技巨头追踪
10. AI 产业链跟踪
11. 加密货币市场跟踪
12. 交易机会观察池与风险预警
13. 未来 72 小时关注清单与信息来源汇总

## 本地运行

```powershell
cd industry_intelligence
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## `.env` 配置

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

EMAIL_PROVIDER=qq
EMAIL_USER=1432047156@qq.com
EMAIL_PASSWORD=your_qq_mail_smtp_authorization_code
EMAIL_TO=1432047156@qq.com
EMAIL_FROM_NAME=全球科技资本市场日报

LOOKBACK_HOURS=24
MAX_ITEMS_PER_CATEGORY=10
OUTPUT_DIR=outputs
```

多个收件人用英文逗号分隔：

```env
EMAIL_TO=1432047156@qq.com,person2@example.com,person3@example.com
```

## 云端定时运行

项目包含 GitHub Actions 配置：

```text
.github/workflows/daily-brief.yml
```

它会在每天 UTC 21:00 运行，也就是北京时间每天 05:00。电脑关机不影响运行，因为任务在 GitHub 云端执行。

需要在 GitHub 仓库中配置 Secrets：

```text
OPENAI_API_KEY
OPENAI_MODEL
EMAIL_PROVIDER
EMAIL_USER
EMAIL_PASSWORD
EMAIL_TO
EMAIL_FROM_NAME
```

推荐值：

```text
OPENAI_MODEL=gpt-4o-mini
EMAIL_PROVIDER=qq
EMAIL_USER=1432047156@qq.com
EMAIL_TO=1432047156@qq.com
EMAIL_FROM_NAME=全球科技资本市场日报
```

## QQ 邮箱授权码

QQ 邮箱 SMTP 只需要首次配置一次授权码，不需要每天登录。

步骤：

1. 登录 QQ 邮箱。
2. 进入设置。
3. 进入账号设置。
4. 找到 POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务。
5. 开启 SMTP 服务。
6. 生成授权码。
7. 把授权码配置到本地 `.env` 或 GitHub Secrets 的 `EMAIL_PASSWORD`。

GitHub Actions 每天 5 点运行时会使用该授权码自动发信。

## 真实性规则

- 超过 24 小时的新闻不进入正文。
- 没有标题、发布时间、来源名称、原文链接的内容不进入正文。
- 无法验证真实性或找不到原始链接的内容不进入正文。
- OpenAI API 额度不足或调用失败时，会使用基于真实新闻标题和链接的本地降级报告，不会编造新闻。
- 每条新闻在 Markdown 和 PPT 来源页保留原文链接，便于人工核查。

## 扩展行业监控

新增行业时修改：

```text
config/topics.yaml
config/sources.yaml
intelligence/ranker.py
```

可以继续扩展 AI、机器人、宠物、供应链、创业融资、网络安全、云计算、加密货币等方向。
