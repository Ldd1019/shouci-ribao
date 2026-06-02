from __future__ import annotations

import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path


SMTP_PROVIDERS = {
    "qq": {"host": "smtp.qq.com", "port": 465},
    "gmail": {"host": "smtp.gmail.com", "port": 465},
}


def recipients() -> list[str]:
    raw = os.getenv("EMAIL_TO", "1432047156@qq.com")
    return [item.strip() for item in raw.split(",") if item.strip()]


def send_email(subject: str, body: str, attachments: list[str] | None = None) -> None:
    provider_name = os.getenv("EMAIL_PROVIDER", "qq").strip().lower()
    provider = SMTP_PROVIDERS.get(provider_name)
    user = os.getenv("EMAIL_USER", "").strip()
    password = os.getenv("EMAIL_PASSWORD", "").strip()
    from_name = os.getenv("EMAIL_FROM_NAME", "全球科技资本市场日报")

    if not provider:
        supported = ", ".join(sorted(SMTP_PROVIDERS))
        raise RuntimeError(f"不支持的 EMAIL_PROVIDER：{provider_name}，可选：{supported}")
    if not user or not password:
        raise RuntimeError("缺少 EMAIL_USER 或 EMAIL_PASSWORD")

    message = MIMEMultipart()
    message["From"] = formataddr((str(Header(from_name, "utf-8")), user))
    message["To"] = ", ".join(recipients())
    message["Subject"] = str(Header(subject, "utf-8"))
    message.attach(MIMEText(body, "plain", "utf-8"))

    for attachment in attachments or []:
        path = Path(attachment)
        if not path.exists() or not path.is_file():
            raise RuntimeError(f"附件不存在：{path}")
        part = MIMEApplication(path.read_bytes(), Name=path.name)
        part.add_header("Content-Disposition", "attachment", filename=path.name)
        message.attach(part)

    with smtplib.SMTP_SSL(provider["host"], provider["port"], timeout=60) as server:
        server.login(user, password)
        server.sendmail(user, recipients(), message.as_string())
