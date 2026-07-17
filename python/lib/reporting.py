"""
Reporting helper functions for the Enterprise Azure SOC Toolkit.
"""

from pathlib import Path

from lib.utils import heading


def ensure_directory(directory: Path):
    """Create a directory if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)


def write_text_report(output_file: Path, title: str, lines: list[str]):
    """Write a formatted text report."""

    output = [
        heading(title),
        "",
        *lines,
        "",
    ]

    output_file.write_text(
        "\n".join(output),
        encoding="utf-8",
    )