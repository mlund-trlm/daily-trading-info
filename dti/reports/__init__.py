"""Built-in reports. Import each report module here so it registers itself."""

from dti.reports.base import REGISTRY, Draft, Flag, Report, get_report

__all__ = ["REGISTRY", "Draft", "Flag", "Report", "get_report"]
