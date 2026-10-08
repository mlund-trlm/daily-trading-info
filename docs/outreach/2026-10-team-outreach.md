# Team Outreach: Existing Automation Inventory (Oct 2026)

**Goal:** collect what each team has already built. This is the starting point for the DTI project (Jira AIP-9).
**Context:** Nick's agent check-ins (Sept 28–Oct 7) and the 10/8 kickoff.

## Teams chat groups

| Chat | Members | Known jobs / status | Open gaps to resolve |
|---|---|---|---|
| **DTI Automation – Team 1** | Zach Hoffman, Oliver Bieling, Adam Dunaief, Colin Liotta | Colin: add/deletes. Zach: next-day earnings. Adam: prior-day/premarket earnings (automation in progress, screenshots still faster). M&A news rotates every 3 weeks (5 jobs, 4 people); Oliver is covering Eli's M&A over the holidays. Oliver also took the biotech calendar from Eli (he has Bloomberg) | Who owns lock-ups/quiet periods? (unanswered 9/30; Eli now says he has lock-ups). What is Oliver's regular job? Is Eli on Team 1 or Team 3? |
| **DTI Automation – Team 2** | Kyle Musser, David Fayn, Charles Alexe *(skip Alexander Ball, who has left the firm)* | Kyle: splits/dividends, script done, first automated email was set for Mon 10/5. Charles: secondary offerings (NewsEdge keyword filter; plans a PR scraper → dashboard/LLM email; the PR login token expires every 24h). David: activist/M&A chatter, manual by choice; logs tickers and sends after the close | Did Kyle's 10/5 automated send go out cleanly? |
| **DTI Automation – Team 3** | Grant Houde, Erik Hennenfent, Leo Gregory, Eli Levi | Grant: short reports. Erik + Leo: spin-offs, symbol changes, de-SPACs. Eli: IPO lock-ups (not started, token budget). Biotech moved to Oliver (Team 1). No automation status given on 9/30 | Status of everything |
| **DTI Automation – Team 4** | Kyle Tsai, Travis Roux, *+11 others (full roster needed)* | Focused earnings is ~90% automated (Kyle Tsai). Still manual (Travis): entering tickers/running the code, checking call/report times, printing and handing out sheets (up to 1 hr in earnings season), emailing the firm. Mag 7 Bloomberg numbers aren't automated | Who owns IPOs, CEFs/uplistings, econ calendar, and the conference-call calendar, and what's their status? |
| **DTI Automation – Team 5** | **TBD**: get the current roster from Nick (the guide lists Ivan Fediv and Will Titus, but that list is ~2 yrs old) | Top gainers/losers (EOD email + Google Sheet log), trade write-ups. No check-in yet | Everything |

**Before creating the chats:** confirm the Team 4 and Team 5 rosters, and which team Eli is on, with Nick or by reading the DTI email senders.

## Messages

### Team 1
> Hey all, I'm Mike Lund. I'm now full-time as a Forward Deployed Engineer, and Nick has me building out the Daily Trading Info automation so it's fully automated by year-end. I'm not starting from scratch; I want to build on what you've already done.
>
> From Nick's check-in I have: Colin on add/deletes, Zach on next-day earnings, Adam on prior-day/premarket earnings (Adam, I hear you've started an automation), and M&A news on a 3-week rotation. Could each of you reply with:
> 1. Your job(s), and who's on M&A rotation right now
> 2. What's automated vs. still manual, and roughly how long it takes each day
> 3. Your code, scripts, prompts, or workflow. Drop files here or point me to a repo or folder, even if it's half-built
> 4. Data sources you use, and any that break or are unreliable
> 5. Blockers (access, logins, Bloomberg, token budget, etc.)
>
> Two open questions: who's currently on lock-ups/quiet periods? And Oliver, what's your regular job? I hear you picked up the biotech calendar from Eli. Thanks, appreciate it!

### Team 2
> Hey all, I'm Mike Lund. I'm full-time as a Forward Deployed Engineer now, and Nick has me building the Daily Trading Info automation (target: fully automated by year-end). Nick says you're the furthest along, so I'd love to use your work as a model.
>
> - **Kyle:** did the automated splits/dividends email go out on Monday? Can you share the script, how you run it (schedule, machine), and how you checked it?
> - **Charles:** can you send over your NewsEdge filter terms and anything you've built toward the PR scraper? I'd like to help with the 24-hour token problem.
> - **David:** I agree that chatter needs judgment. Could you share your source list and a few recent examples of what you sent? That'll help me build something that surfaces candidates for you to review, not replace your judgment.
>
> For everyone: what's still manual, how long it takes each day, which data sources are unreliable, and any blockers. Files, repo links, or rough notes are all fine. Thanks!

### Team 3
> Hey all, I'm Mike Lund. I'm full-time as a Forward Deployed Engineer now, and Nick has me building the Daily Trading Info automation (target: fully automated by year-end). I want to build on what you've already done rather than start over.
>
> From Nick's check-ins I have: Grant on short reports, Erik + Leo on spin-offs/symbol changes/de-SPACs, and Eli on IPO lock-ups (biotech moved to Oliver). Could each of you reply with:
> 1. Your job, and how you split it if it's shared (Erik/Leo)
> 2. What's automated vs. manual today, and roughly how long it takes each day
> 3. Any code, scripts, prompts, or workflows. Rough or half-built is fine
> 4. Your sources (Grant, I'd especially like your list of short-seller sites; some may block our IPs, which we can work around)
> 5. Blockers
>
> Eli, I know you're tight on token budget. Don't burn it on lock-ups; I can pick that one up. Just send me the site you screenshot from. Thanks!

### Team 4
> Hey all, I'm Mike Lund. I'm full-time as a Forward Deployed Engineer now, and Nick has me building the Daily Trading Info automation (target: fully automated by year-end).
>
> **Focused earnings:** Kyle Tsai, can you share the code and how you run it? Travis, thanks for the list of what's still manual. Printing and handing out sheets is clearly the biggest time sink, and that's the first thing I'll go after. Also, the call/report-time checks, the email to the firm, and the Mag 7 Bloomberg numbers: which sources do you check those against?
>
> **Everyone else:** who owns IPOs, closed-end funds/uplistings, the econ calendar, and the conference-call calendar, and where does each one stand? Please reply with your job, what's automated vs. manual, how long it takes, your sources, and any code or prompts (rough is fine). Thanks!

### Team 5
> Hey all, I'm Mike Lund. I'm full-time as a Forward Deployed Engineer now, and Nick has me building the Daily Trading Info automation (target: fully automated by year-end). We haven't connected yet, so I'm reaching out directly.
>
> Top gainers/losers is the most judgment-heavy job, so I'd like to understand how you do it today:
> 1. Who owns it, and how is the work split?
> 2. How you pick the names (market cap, volume, headline source?) and how you handle stocks that gap down and then recover intraday
> 3. What's automated vs. manual, and how long it takes each day (email + Google Sheet log)
> 4. Any code, scripts, prompts, or sources, even rough ones
> 5. Blockers
>
> Thanks, looking forward to working with you!
