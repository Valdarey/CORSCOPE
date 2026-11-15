"""Shared helpers."""
from pathlib import Path

def default_report_path(fmt: str) -> Path:
    return Path(f"corscope-report.{fmt}")
