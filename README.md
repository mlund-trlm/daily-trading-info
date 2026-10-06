# daily-trading-info

Automates the recurring reports in the *Daily Trading Information Guide*: earnings calendars, S&P adds/deletes, M&A, IPOs, splits/dividends, top gainers/losers, and more. Each run produces a **draft**. The report owner reviews and edits it in a dashboard before it goes out over the usual channels (Outlook email blast, printed earnings sheets).

- Plan and phases: [docs/PLAN.md](docs/PLAN.md)
- Tracking: Jira **AIP-9** (Daily Trading Info Automation) at trillium.atlassian.net

## Setup
```bash
pip install -e ".[dev]"
pytest
```

## Usage
```bash
dti list                                      # available reports
dti run <report> --date 2026-10-06 --dry-run  # render HTML to out/ without saving
dti run <report>                              # render + save a draft for review (SQLite, $DTI_DB)
```

## Layout
```
dti/calendar.py      NYSE sessions, holidays, half-days
dti/reports/         one module per report (subclass Report: fetch -> normalize -> render)
dti/sources/         shared fetchers per site/API
dti/render/          Jinja2 email templates (inline styles for Outlook)
dti/store.py         drafts + review/send status
dti/llm/, delivery/  Claude helpers; Graph mail / print / Sheets (to come)
```

## Adding a report
Create `dti/reports/<name>.py` with a `Report` subclass that sets `name`/`title` and implements `fetch()` and `normalize()`. Import it in `dti/reports/__init__.py`, and add a test under `tests/` that uses saved source data in `tests/fixtures/`.
