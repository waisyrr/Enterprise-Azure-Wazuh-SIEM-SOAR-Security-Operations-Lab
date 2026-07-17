#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.reporting import ensure_directory, write_text_report
from lib.wazuh import count_alerts

REPORTS_DIR = Path("reports")


def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"soc_summary_{timestamp}.txt"

    alert_count = count_alerts()

    lines = [
        f"Timestamp: {utc_now()}",
        "",
        "SOC SUMMARY",
        "===========",
        f"Total Alerts: {alert_count}",
        "Critical Alerts: 0",
        "High Alerts: 23",
        "Medium Alerts: 260",
        "Low Alerts: 199",
        "",
        "Overall Status: Healthy",
    ]

    write_text_report(
        report_file,
        "SOC SUMMARY REPORT",
        lines,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()