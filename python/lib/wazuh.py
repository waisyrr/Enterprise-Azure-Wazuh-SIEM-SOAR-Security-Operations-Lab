"""
Wazuh helper functions.
"""

from pathlib import Path


DEFAULT_ALERT_FILE = Path("/var/ossec/logs/alerts/alerts.json")


def alert_file_exists() -> bool:
    """Return True if alerts.json exists."""
    return DEFAULT_ALERT_FILE.exists()


def get_alert_file() -> Path:
    """Return the alerts.json path."""
    return DEFAULT_ALERT_FILE


def count_alerts() -> int:
    """Count alert entries."""

    if not DEFAULT_ALERT_FILE.exists():
        return 0

    with DEFAULT_ALERT_FILE.open(
        "r",
        encoding="utf-8",
        errors="ignore",
    ) as file:
        return sum(1 for line in file if line.strip())