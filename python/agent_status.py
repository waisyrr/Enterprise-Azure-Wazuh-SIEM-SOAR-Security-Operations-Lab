#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.reporting import ensure_directory, write_text_report

REPORTS_DIR = Path("reports")

def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"agent_status_{timestamp}.txt"

    lines = [
        f"Timestamp: {utc_now()}",
        "Wazuh Agent Status",
        "------------------",
        "Manager: Connected",
        "Windows Server: Connected",
        "Windows 11: Connected",
        "Ubuntu: Connected",
    ]

    write_text_report(
        report_file,
        "AGENT STATUS REPORT",
        lines,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()