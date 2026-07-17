#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.reporting import ensure_directory, write_text_report

REPORTS_DIR = Path("reports")

def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"ioc_lookup_{timestamp}.txt"

    iocs = [
        "8.8.8.8",
        "1.1.1.1",
        "192.168.1.100",
    ]

    lines = [
        f"Timestamp: {utc_now()}",
        "",
        "IOC Lookup Results",
        "==================",
    ]

    for ioc in iocs:
        lines.append(f"{ioc} -> No threat intelligence lookup configured")

    write_text_report(
        report_file,
        "IOC LOOKUP REPORT",
        lines,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()