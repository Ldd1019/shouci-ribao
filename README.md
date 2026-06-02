# 每日全球行业情报系统

这是一个真实新闻情报系统，不是 AI 新闻生成器。

系统只从 RSS、官方网站或新闻 API 获取新闻事实。AI 只负责中文翻译、摘要、行业分类和趋势分析，不允许创造新闻、融资事件、收购事件、产品发布或公司动作。

## 默认收件人

```text
1432047156@qq.com
```

## 本地运行

```powershell
cd industry_intelligence
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## .env 配置

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

EMAIL_PROVIDER=qq
EMAIL_USER=1432047156@qq.com
EMAIL_PASSWORD=your_qq_mail_smtp_authorization_code
EMAIL_TO=1432047156@qq.com
EMAIL_FROM_NAME=每日行业情报

LOOKBACK_HOURS=24
MAX_ITEMS_PER_CATEGORY=5
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

它会在每天 UTC 21:00 运行，也就是北京时间每天 05:00。

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
EMAIL_FROM_NAME=每日行业情报
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

云端每天 5 点运行时，GitHub Actions 会使用该授权码自动发信。你本人不需要每天打开邮箱。

## Gmail 备用方案

Gmail SMTP 需要应用专用密码。

步骤：

1. 打开 Google 账号安全设置。
2. 开启两步验证。
3. 进入应用专用密码。
4. 创建 Mail 用途的 16 位授权码。
5. 把授权码配置到本地 `.env` 或 GitHub Secrets 的 `GMAIL_APP_PASSWORD`。

如果使用 Gmail 备用方案，请设置：

```env
EMAIL_PROVIDER=gmail
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_16_digit_gmail_app_password
```

## 扩展行业监控

新增行业时修改：

```text
config/topics.yaml
config/sources.yaml
```

可以继续扩展 AI、机器人、宠物、供应链、创业融资等监控方向。
