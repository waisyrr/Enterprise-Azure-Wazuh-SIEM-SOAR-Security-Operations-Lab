#!/usr/bin/env python3

from pathlib import Path

from lib.utils import utc_now
from lib.reporting import ensure_directory, write_text_report

REPORTS_DIR = Path("reports")

def main():
    ensure_directory(REPORTS_DIR)

    timestamp = utc_now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"threat_client_{timestamp}.txt"

    lines = [
        f"Timestamp: {utc_now()}",
        "",
        "Threat Intelligence Client",
        "=========================",
        "VirusTotal API: Not configured",
        "AbuseIPDB API: Not configured",
        "OTX API: Not configured",
        "",
        "Status: Ready for API integration",
    ]

    write_text_report(
        report_file,
        "THREAT INTELLIGENCE CLIENT REPORT",
        lines,
    )

    print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main()