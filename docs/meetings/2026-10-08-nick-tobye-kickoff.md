# Kickoff: Mike Lund × Nicholas Tobye

**Date:** Thu, 08 Oct 2026 · **Attendees:** Nicholas Tobye, Mike Lund
**Jira:** AIP-37 (kickoff), epic AIP-9 · **Transcript:** https://notes.granola.ai/t/a9efdfe0-3f9c-499b-bbfb-aac331c8921d-00best9l

## Project overview
- Goal: automate the daily trading info that goes out to traders across 5 teams.
- Rookies do this by hand today, and the output is often inaccurate.
- Nick has already built most of this himself, on the side while trading.
- Most teams already have some automation built, which is a good sign.
- **Target: a fully automated system live before end of year.**

## Automation feasibility by team
- **Teams 1–4:** most tasks can be fully automated.
  - Earnings calendar, adds/deletes, lockup periods, spin-offs, ticker changes, de-SPACs, IPOs, closed-end funds, uplistings, economic reports, and conference call calendars are all straightforward filings.
  - The biotech calendar is already pulled from Bloomberg, so it's essentially done.
  - The short report tracker just needs a curated source list, then a scrape once a day.
    - Some sites block firm IPs; switching to a fresh IP fixes this.
    - The reports eventually come out for free, so speed isn't critical.
  - Focused earnings (Team 4) is already automated. Printing is the only friction left.
- **M&A news:** mostly automatable through the Bloomberg LLM, but API access needs to be confirmed.
- **Takeover chatter:** the hardest to automate, more art than science.
  - There are no reliable tags, and the sources are scattered (e.g. FT, trader rumor).
  - Approach: curate a list of reputable sources and scrape twice a day (morning + afternoon).
- **Top daily gainers/losers (Team 5):** the most subjective and hardest to fully automate.
  - Proposed filter: market cap > $1B, above-average volume, and relevant Bloomberg headline tags.
  - Edge case: stocks that gap down and then recover intraday on news can slip through simple filters.

## Data sources and delivery
- **The Bloomberg API is the primary catch-all source.**
  - It's more reliable than current sources like Yahoo Finance, which errors often.
  - The firm should buy a dedicated Bloomberg API rather than piggyback on individual terminals.
  - Bloomberg's internal LLM can be queried for tagged headlines, SEC filings, and corporate actions.
- An SEC filing API is also needed. Bloomberg and SEC APIs are both known to exist.
- The S&P add/delete feed is likely free directly from S&P.
- **Email is still the right delivery method.**
  - A simple, consistent format sent to a shared distribution list.
  - Traders can build their own dashboards on top. Nick has one that parses email subjects.
- **Key gap rookies miss:** follow-up notifications, e.g. a split's announcement date vs. effective date vs. the actual split day.

## Nick's sources of truth (his existing calendar build)

| Area | Source | Refresh |
|---|---|---|
| Corporate actions (main calendar) | Daily "Upcoming Corporate Actions" email from CorporateActions@trlm.com (read from Deleted Items). Contains Nasdaq Trader alerts (linked to Nasdaq notices) + NYSE corporate actions table | When the calendar opens, then every 20 min; a Power Automate flow creates a 6:00 AM Outlook calendar event from the same email |
| Ticker changes (de-SPACs, merger ticker changes, exchange moves) | The corporate actions email (exchange symbol-change notices). On refresh: StockAnalysis symbol-change list, EODData symbol changes (history), OCC info memos (option symbols), SEC 8-K/6-K/prospectuses (incl. "change of trading symbol" check), press releases (PR Newswire, GlobeNewswire, Business Wire, StockTitan) | Automatic + manual refresh button |
| Spin-off stories (e.g. TORO → AIOK) | Nasdaq Trader alerts + company SEC filings and press releases | Manual refresh (researched) |
| Earnings box (reported / later today / tomorrow) | Schedule: Yahoo Finance earnings calendar. Market cap, price, move since prior close (incl. premarket), and exchange (used to drop OTC names) from Yahoo quotes | Apps Script writes `earnings-today.json` to Google Drive every 15 min pre-open, every 30 min after |
| This week's key earnings | Yahoo weekly earnings calendar (Mon–Fri); Mag 7 = fixed list; semis > $10B via Yahoo company profiles; popular names = ApeWisdom (Reddit top 50) + StockTwits trending | Rebuilt hourly |
| Earnings prep panel (per-ticker click-through) | "Morning Earnings" / "Afternoon Earnings" PDF emails from the Daily Trading Information list, numbers read as written | When the email arrives |
| S&P 500 changes | "Adds / Deletes" emails from the Daily Trading Information list (pasted image of S&P's table, read by Claude, linked back to the email) | When the email arrives |
| IPO lock-ups / quiet periods | Lock-ups: StockAnalysis lock-up calendar (dates/triggers from SEC prospectus, linked). Quiet periods: StockAnalysis recent IPOs, IPO date + 25 days | Daily (Apps Script) |

**Behind the scenes:** History, stories, research, and anything already read are saved in the calendar's own database, so nothing is lost when emails are purged. Outlook connects through Microsoft 365, and the earnings file through Google Drive.

**Tried and dropped:**
- Nasdaq earnings data: it stalls requests from Google's servers.
- Earnings Whispers: paid.
- Wikipedia's S&P changes table: removed from the page.
- Google News for S&P releases.
- An automated SEC filing scan: the SEC blocks Google Apps Script.

## Action items
- [ ] **Mike:** ping one contact per team on Teams to review what each team has already built.
  - Skip Alexander Ball (Team 2); he's no longer at Trillium.
- [ ] **Nick:** send Mike a Claude-generated summary of all the team chats, covering each rookie's job and its current automation status.
- [ ] **Nick:** share his list of reliable data sources. This is the starting point for telling trustworthy feeds apart from weak ones like Yahoo Finance.
- [ ] **Mike:** get added to the Daily Trading Info email blast. Nick submitted the request; if it hasn't happened soon, follow up with Change (or tag both Change and Infrastructure).

## Implications for our plan (Mike's read, to confirm)
- **Integrate before building:** Nick's calendar and the teams' existing automations cover much of Phase 1. The next step is an inventory of what already exists, then fill the gaps and consolidate, rather than rebuilding from scratch.
- **Data sources:** Bloomberg API (dedicated firm license) + an SEC API become the primary sources, replacing the plan's scraping of public sites and Yahoo where possible. Procurement becomes a critical-path item (AIP-29).
- **Delivery:** email to the shared distribution list is still the channel. Subjects need a stable, parseable format, because traders' dashboards (including Nick's) parse them. The review dashboard is still useful as a pre-send QA step, but it's internal tooling, not the product.
- **New requirement: follow-up notifications.** Track each corporate action's life cycle (announced → effective date → event day) and send reminders at each stage. This generalizes the S&P "morning of the effective date" rule to splits, ticker changes, de-SPACs, and lockups.
- **IP blocking:** scrapers need a way to switch to a fresh IP or use a proxy for sites that block the firm's IPs.
- **Deadline:** live before end of year, which overlaps the targeted 12/6 start of 23/5 trading.
