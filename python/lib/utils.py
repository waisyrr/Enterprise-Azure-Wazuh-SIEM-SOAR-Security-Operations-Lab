"""
Common utility functions used throughout the Enterprise Azure SOC Toolkit.
"""

from datetime import datetime, timezone


def utc_now():
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


def utc_timestamp():
    """Return current UTC timestamp string."""
    return utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")


def separator(length=60):
    """Return a separator line."""
    return "=" * length


def heading(title):
    """Return a formatted heading."""
    return (
        f"{separator()}\n"
        f"{title}\n"
        f"{separator()}"
    )