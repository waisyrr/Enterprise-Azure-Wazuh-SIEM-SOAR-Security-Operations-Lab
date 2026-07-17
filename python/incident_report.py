#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.reporting import ensure_directory, write_text_report

REPORTS_DIR = Path("reports")

def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"incident_report_{timestamp}.txt"

    lines = [
        f"Timestamp: {utc_now()}",
        "",
        "Incident Report",
        "===============",
        "Incident ID: INC-20260716-001",
        "Severity: High",
        "Status: Closed",
        "",
        "Summary:",
        "Multiple failed logon attempts detected.",
        "",
        "Actions Taken:",
        "- Reviewed Wazuh alerts",
        "- Verified endpoint activity",
        "- No malicious persistence found",
        "- Incident closed after investigation",
    ]

    write_text_report(
        report_file,
        "INCIDENT REPORT",
        lines,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()