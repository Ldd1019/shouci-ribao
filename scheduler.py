from __future__ import annotations

import time
from datetime import datetime, timedelta

from main import run_once


def wait_seconds(hour: int = 5, minute: int = 0) -> float:
    now = datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_run <= now:
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()


if __name__ == "__main__":
    while True:
        time.sleep(wait_seconds(5, 0))
        try:
            run_once()
        except Exception as exc:
            print(f"failed: {exc}")
