"""
Threat Intelligence helper functions.
"""


def is_private_ip(ip: str) -> bool:
    """Simple private IP check."""

    return (
        ip.startswith("10.")
        or ip.startswith("172.")
        or ip.startswith("192.168.")
        or ip in ("127.0.0.1", "localhost")
    )


def reputation(ip: str) -> str:
    """Placeholder reputation lookup."""

    if is_private_ip(ip):
        return "Internal"

    return "Unknown"