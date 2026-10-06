# Daily Trading Info Automation — Project Plan

## Context
Each year, first-year traders at Trillium put together about 20 recurring market-info reports by hand. These include earnings calendars, S&P adds/deletes, M&A, IPOs, splits/dividends, top gainers/losers, and more. Each report is defined in `Daily Trading Information Guide.docx`, which is in the repo. Nick Tobye (Chicago) oversees the work. The goal is to automate gathering and formatting these reports. An owner should be able to run the automations, review and edit the output in a dashboard, and then distribute it through the existing channels: mostly an Outlook email blast, plus printed earnings sheets. The project is tracked in Jira project **AIP** (trillium.atlassian.net). AIP has Epic and Task issue types and currently holds only Atlassian's sample items (AIP-1 to AIP-8).

## Decisions (confirmed with Mike)
- **Scope:** all reports, delivered in phases. Phase 1 covers the easiest ones to automate.
- **Review:** human-in-the-loop for now, through a web review dashboard where the owner runs jobs and reviews, edits, and approves output. Full auto-send can come later once the reports prove reliable.
- **Distribution:** Microsoft Graph (O365) sends the approved email. Earnings sheets also get print-ready output (PDF/HTML).
- **Format:** HTML tables in the email body, no attachments, no images.
- **Stack:** Python, in this repo (`mlund-trlm/daily-trading-info`), cloud-hosted, Claude API for summaries and extraction.
- **Jira:** one Epic plus one Task per report, plus infrastructure/access Tasks. Mike is the assignee and Nick Tobye is named in the Epic as business owner.
- **Data access:** unknown for now (TTN API, Bloomberg, paid feeds). Phase 1 uses public sources only, and each paid or licensed source gets its own access Task.

## Architecture
```
dti/
  calendar.py        # trading days/holidays/half-days (pandas_market_calendars)
  sources/           # one fetcher per site/API (iposcoop, nasdaq, yahoo, spglobal, marketbeat, sec_edgar, ...)
  reports/           # one module per report: fetch -> normalize -> render; common Report base class
  llm/               # Claude client + prompts (M&A terms, blurbs, symbol changes); model configurable
  render/templates/  # Jinja2 HTML email templates (bold key numbers, BCAL-style M&A, IPO card, movers)
  store/             # SQLite (Postgres later): runs, drafts, edits, approvals, send log
  delivery/          # graph_mail.py (send), print.py (PDF via headless Chromium), sheets.py (Team 5 log)
  dashboard/         # FastAPI + HTMX: today's reports, Run now, preview, inline edit, Approve->Send / Print
  scheduler.py       # APScheduler on trading days (premarket, 9am, EOD runs)
tests/fixtures/      # saved source HTML/JSON so parsers are tested offline
```
- Every report implements `fetch(date) -> normalize -> render_html()` and saves a draft with its source links, so the reviewer can check facts quickly.
- The dashboard flags low-confidence items, such as LLM-extracted deal terms or sources that disagree, for the reviewer to look at.
- Hosting: one small always-on container (Azure suggested because Trillium is on O365), confirmed with IT. Secrets come from env vars.

## Phases (each report = one Jira Task)
**Phase 1: structured public data (easiest)**
1. Tomorrow's Earnings Calendar, with print-ready sheet (public earnings API/Nasdaq; TTN later if an API exists)
2. Prior Day AH / Premarket Earnings List (sorted by market cap)
3. Splits (Yahoo, cross-checked against Nasdaq)
4. Large Dividends
5. IPO Calendar (IPOScoop, cross-checked against Nasdaq/MarketWatch), in the UMAC card format
6. Lock-Up / Quiet Period Expirations (monthly + daily)
7. Economic Reports Calendar
8. S&P 500 Adds/Deletes (S&P DJI newswire monitor + morning-of-effective-date reminder)

**Phase 2: news + LLM**
9. M&A News, 2x daily (detect, extract terms, compute move, bold format)
10. Daily Top Gainers/Losers, EOD + Google Sheet monthly tab
11. Symbol Changes / De-SPACs / Spin-offs (SEC EDGAR 8-K/Form 25 + Nasdaq Trader symbol-change file + LLM)
12. Secondary Offerings
13. Closed-End Funds / Uplistings (with top holdings)
14. Daily Conference Calls / Events

**Phase 3: judgment-heavy / licensed data**
15. Takeover Chatter Tracker
16. Short Report Tracker
17. Biotech Catalyst Calendar (monthly/weekly)
18. Focused Earnings Analysis (short interest, cc time, options implied move, PE, GOOGL TAC)
19. Trade Category Write-Ups: template/assist only, since traders write these themselves

**Infrastructure/access Tasks:** data-source access audit (TTN API, Bloomberg, MarketBeat/Investing.com ToS); Anthropic API key; Azure app registration (Graph Mail.Send + dashboard SSO); hosting; distribution list(s) and reviewer roster; Google Sheets service account; dashboard MVP; scheduler + trading calendar.

## Jira (AIP)
Epic **AIP-9**. Phase 1 = AIP-10..17, Phase 2 = AIP-18..23, Phase 3 = AIP-24..28, Infra = AIP-29..36.

## Execution order
1. Create the Jira Epic and Tasks in AIP. Use `atlassianUserInfo` to get Mike's accountId, add phase labels (`phase-1/2/3`, `infra`), and put the guide's process steps and output format in each Task's description.
2. Scaffold the repo (pyproject, `dti/` skeleton, Report base class, calendar, store, Jinja2 base template, CLI `dti run <report> --date --dry-run`), then commit and push to `claude/stoic-lovelace-64hf84`.
3. Build the Phase 1 reports one at a time, each with fixture-based tests, then build the dashboard MVP (run/preview/edit/approve, with copy-HTML until Graph access is granted).

## Verification
- `pytest` parsers against saved fixtures, plus a render snapshot test for each report.
- `dti run <report> --date YYYY-MM-DD --dry-run` writes HTML to `out/` to inspect (screenshot with the installed Chromium).
- Run the dashboard locally (`uvicorn dti.dashboard.app:app`): generate, edit, and approve a draft, with Graph sending in sandbox mode to Mike only.
- Run in parallel with the manual process for about 2 weeks and compare it with the reports the traders send. Track misses in Jira.

## Open items (to become Jira Tasks/questions for Nick/IT)
- Is there a TTN or Bloomberg API, and is scraping MarketBeat/Investing.com allowed?
- Who are the email distribution list and the designated owner/reviewers?
- What are the send-time SLAs for each report?
