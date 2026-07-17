#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.wazuh import get_alert_file
from lib.reporting import ensure_directory, write_text_report

REPORTS_DIR = Path("reports")

def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"log_parser_{timestamp}.txt"

    alert_file = get_alert_file()

    with alert_file.open("r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    output = [
        f"Timestamp: {utc_now()}",
        f"Alert file: {alert_file}",
        f"Total log entries: {len(lines)}",
        "",
        "Last 10 log entries:",
        *[line.strip() for line in lines[-10:]],
    ]

    write_text_report(
        report_file,
        "LOG PARSER REPORT",
        output,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()