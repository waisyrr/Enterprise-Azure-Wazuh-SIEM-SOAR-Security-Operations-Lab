#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.wazuh import count_alerts
from lib.reporting import ensure_directory, write_text_report
REPORTS_DIR = Path("reports")

def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"daily_health_{timestamp}.txt"

    alert_count = count_alerts()

    lines = [
        f"Timestamp: {utc_now()}",
        f"Total Alerts: {alert_count}",
    ]

    write_text_report(
        report_file,
        "DAILY HEALTH REPORT",
        lines,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()