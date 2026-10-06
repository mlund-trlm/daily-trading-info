"""Report framework: every daily report is a Report subclass registered by name.

A report run goes fetch -> normalize -> render, and produces a Draft that the
review dashboard shows for editing/approval before anything is distributed.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any, ClassVar

from dti.render import render_template

REGISTRY: dict[str, type["Report"]] = {}


@dataclass
class Flag:
    """Something the reviewer should double-check (LLM-extracted value, sources disagree, ...)."""

    message: str
    item: str | None = None


@dataclass
class Draft:
    report: str
    run_date: date
    subject: str
    html: str
    sources: list[str] = field(default_factory=list)
    flags: list[Flag] = field(default_factory=list)
    empty: bool = False  # nothing to send today ("if applicable" reports)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class Report(ABC):
    name: ClassVar[str]  # registry key / CLI name, e.g. "splits"
    title: ClassVar[str]  # human title, e.g. "Stock Splits"
    template: ClassVar[str] = "table.html"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, "name", None):
            REGISTRY[cls.name] = cls

    def __init__(self, run_date: date):
        self.run_date = run_date
        self.sources: list[str] = []
        self.flags: list[Flag] = []

    @abstractmethod
    def fetch(self) -> Any:
        """Pull raw data from sources. Append each URL used to self.sources."""

    @abstractmethod
    def normalize(self, raw: Any) -> list[dict]:
        """Turn raw data into rows (list of dicts) for the template."""

    def subject(self) -> str:
        return f"{self.title} - {self.run_date:%a %m/%d/%y}"

    def context(self, rows: list[dict]) -> dict:
        """Template variables; override to add columns or sections."""
        return {"title": self.title, "run_date": self.run_date, "rows": rows}

    def run(self) -> Draft:
        rows = self.normalize(self.fetch())
        html = render_template(self.template, **self.context(rows))
        return Draft(
            report=self.name,
            run_date=self.run_date,
            subject=self.subject(),
            html=html,
            sources=list(self.sources),
            flags=list(self.flags),
            empty=not rows,
        )


def get_report(name: str) -> type[Report]:
    import dti.reports  # noqa: F401  (registers built-in reports)

    try:
        return REGISTRY[name]
    except KeyError:
        raise KeyError(f"Unknown report {name!r}. Known: {', '.join(sorted(REGISTRY)) or '(none)'}")
