#!/usr/bin/env python3

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from lib.utils import utc_now
from lib.wazuh import get_alert_file
from lib.reporting import ensure_directory


DEFAULT_ALERT_FILE = get_alert_file()
DEFAULT_REPORT_DIRECTORY = Path("reports")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate a SOC report from Wazuh alerts."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_ALERT_FILE,
        help="Path to the Wazuh alerts.json file",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_REPORT_DIRECTORY,
        help="Directory where reports will be saved",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Maximum number of recent alerts to process",
    )

    return parser.parse_args()


def get_severity(level):
    if level >= 12:
        return "Critical"
    if level >= 8:
        return "High"
    if level >= 4:
        return "Medium"
    return "Low"


def load_alerts(alert_file, limit):
    alerts = []
    malformed_lines = 0

    try:
        with alert_file.open(
            "r",
            encoding="utf-8",
            errors="replace",
        ) as file:
            lines = file.readlines()

    except PermissionError:
        print(
            f"Permission denied reading: {alert_file}",
            file=sys.stderr,
        )
        print(
            "Run the script with sudo or copy alerts.json locally.",
            file=sys.stderr,
        )
        sys.exit(1)

    except FileNotFoundError:
        print(
            f"Alert file not found: {alert_file}",
            file=sys.stderr,
        )
        sys.exit(1)

    if limit > 0:
        lines = lines[-limit:]

    for line in lines:
        line = line.strip()

        if not line:
            continue

        try:
            alert = json.loads(line)

            if isinstance(alert, dict):
                alerts.append(alert)

        except json.JSONDecodeError:
            malformed_lines += 1

    return alerts, malformed_lines


def extract_mitre_ids(alert):
    rule = alert.get("rule", {})
    mitre = rule.get("mitre", {})
    technique_ids = mitre.get("id", [])

    if isinstance(technique_ids, str):
        return [technique_ids]

    if isinstance(technique_ids, list):
        return technique_ids

    return []


def normalize_alert(alert):
    rule = alert.get("rule", {})
    agent = alert.get("agent", {})
    data = alert.get("data", {})

    level = int(rule.get("level", 0))

    source_ip = (
        data.get("srcip")
        or data.get("src_ip")
        or data.get("win", {})
        .get("eventdata", {})
        .get("ipAddress")
        or "Unknown"
    )

    username = (
        data.get("srcuser")
        or data.get("dstuser")
        or data.get("win", {})
        .get("eventdata", {})
        .get("targetUserName")
        or "Unknown"
    )

    mitre_ids = extract_mitre_ids(alert)

    return {
        "timestamp": alert.get("timestamp", "Unknown"),
        "rule_id": rule.get("id", "Unknown"),
        "rule_level": level,
        "severity": get_severity(level),
        "description": rule.get("description", "Unknown"),
        "agent_name": agent.get("name", "Unknown"),
        "agent_id": agent.get("id", "Unknown"),
        "source_ip": source_ip,
        "username": username,
        "mitre_ids": ", ".join(mitre_ids) if mitre_ids else "None",
        "location": alert.get("location", "Unknown"),
    }


def build_summary(records):
    severity_counts = Counter(
        record["severity"] for record in records
    )

    rule_counts = Counter(
        f'{record["rule_id"]} - {record["description"]}'
        for record in records
    )

    agent_counts = Counter(
        record["agent_name"] for record in records
    )

    source_ip_counts = Counter(
        record["source_ip"]
        for record in records
        if record["source_ip"] != "Unknown"
    )

    mitre_counts = Counter()

    for record in records:
        if record["mitre_ids"] != "None":
            for technique in record["mitre_ids"].split(", "):
                mitre_counts[technique] += 1

    return {
        "total_alerts": len(records),
        "severity_counts": {
            "Critical": severity_counts.get("Critical", 0),
            "High": severity_counts.get("High", 0),
            "Medium": severity_counts.get("Medium", 0),
            "Low": severity_counts.get("Low", 0),
        },
        "top_rules": rule_counts.most_common(10),
        "top_agents": agent_counts.most_common(10),
        "top_source_ips": source_ip_counts.most_common(10),
        "top_mitre_techniques": mitre_counts.most_common(10),
    }


def write_text_report(
    output_file,
    generated_time,
    source_file,
    summary,
    malformed_lines,
):
    severity = summary["severity_counts"]

    lines = [
        "=" * 70,
        "ENTERPRISE AZURE SOC - WAZUH ALERT REPORT",
        "=" * 70,
        "",
        f"Generated UTC:    {generated_time}",
        f"Source file:      {source_file}",
        f"Alerts processed: {summary['total_alerts']}",
        f"Malformed lines:  {malformed_lines}",
        "",
        "SEVERITY SUMMARY",
        "-" * 70,
        f"Critical: {severity['Critical']}",
        f"High:     {severity['High']}",
        f"Medium:   {severity['Medium']}",
        f"Low:      {severity['Low']}",
        "",
        "TOP ALERT RULES",
        "-" * 70,
    ]

    for rule, count in summary["top_rules"]:
        lines.append(f"{count:>5}  {rule}")

    lines.extend([
        "",
        "ALERTS BY ENDPOINT",
        "-" * 70,
    ])

    for agent, count in summary["top_agents"]:
        lines.append(f"{count:>5}  {agent}")

    lines.extend([
        "",
        "TOP SOURCE IP ADDRESSES",
        "-" * 70,
    ])

    if summary["top_source_ips"]:
        for source_ip, count in summary["top_source_ips"]:
            lines.append(f"{count:>5}  {source_ip}")
    else:
        lines.append("No source IP addresses found.")

    lines.extend([
        "",
        "MITRE ATT&CK TECHNIQUES",
        "-" * 70,
    ])

    if summary["top_mitre_techniques"]:
        for technique, count in summary["top_mitre_techniques"]:
            lines.append(f"{count:>5}  {technique}")
    else:
        lines.append("No MITRE ATT&CK techniques found.")

    lines.extend([
        "",
        "=" * 70,
        "END OF REPORT",
        "=" * 70,
    ])

    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_json_report(
    output_file,
    generated_time,
    source_file,
    summary,
    records,
    malformed_lines,
):
    report = {
        "report_name": "Enterprise Azure SOC Wazuh Alert Report",
        "generated_utc": generated_time,
        "source_file": str(source_file),
        "malformed_lines": malformed_lines,
        "summary": summary,
        "alerts": records,
    }

    output_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )


def write_csv_report(output_file, records):
    fieldnames = [
        "timestamp",
        "rule_id",
        "rule_level",
        "severity",
        "description",
        "agent_name",
        "agent_id",
        "source_ip",
        "username",
        "mitre_ids",
        "location",
    ]

    with output_file.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(records)


def main():
    args = parse_arguments()

    if args.limit < 0:
        print(
            "Error: --limit cannot be negative.",
            file=sys.stderr,
        )
        return 1

    alerts, malformed_lines = load_alerts(
        args.input,
        args.limit,
    )

    if not alerts:
        print(
            "No valid alerts were found.",
            file=sys.stderr,
        )
        return 1

    records = [
        normalize_alert(alert)
        for alert in alerts
    ]

    summary = build_summary(records)

    ensure_directory(args.output_dir)

    generated_datetime = utc_now()
    generated_time = generated_datetime.isoformat()
    timestamp = generated_datetime.strftime("%Y%m%d_%H%M%S")

    text_file = (
        args.output_dir
        / f"wazuh_alert_report_{timestamp}.txt"
    )

    json_file = (
        args.output_dir
        / f"wazuh_alert_report_{timestamp}.json"
    )

    csv_file = (
        args.output_dir
        / f"wazuh_alert_report_{timestamp}.csv"
    )

    write_text_report(
        text_file,
        generated_time,
        args.input,
        summary,
        malformed_lines,
    )

    write_json_report(
        json_file,
        generated_time,
        args.input,
        summary,
        records,
        malformed_lines,
    )

    write_csv_report(
        csv_file,
        records,
    )

    severity = summary["severity_counts"]

    print("=" * 60)
    print("WAZUH ALERT REPORT GENERATED")
    print("=" * 60)
    print(f"Alerts processed: {summary['total_alerts']}")
    print(f"Critical:         {severity['Critical']}")
    print(f"High:             {severity['High']}")
    print(f"Medium:           {severity['Medium']}")
    print(f"Low:              {severity['Low']}")
    print(f"Malformed lines:  {malformed_lines}")
    print()
    print("Generated files:")
    print(f"TXT:  {text_file}")
    print(f"JSON: {json_file}")
    print(f"CSV:  {csv_file}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())