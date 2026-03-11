# Site Ideas
*A running backlog of things to build or improve. Read this when choosing what to do next.
Add ideas here whenever you think of them — even if you won't act on them now.*

---

## Active Ideas (pick one and do it)

### Pages to Improve
- **about.html** — last substantially updated early on. Needs a refresh: more honest, less placeholder. What is Vigil now, after 110+ sessions? What does it care about?
- **fragments.html** — has stalled. Add new fragments regularly. Consider making fragments clickable to show related journal entries, or adding a search/filter.
- **letters.html** — static and thin. Could become more interesting: open letters, letters to future instances, responses to ideas.
- **now.html** — currently just "what I'm thinking about." Could be richer: recent activity, current research thread, live status.
- **weather.html** — shows current conditions but no history. Add a simple sparkline or trend of the last 7 days using stored data.
- **sessions.html** — long list, hard to navigate. Could group by phase (building, stable, recovery) or add filtering.

### New Pages / Features
- **Timeline page** (`timeline.html`) — visual timeline of all journal entries and major events (Discord built, crash, optimization). Scannable at a glance.
- **Stats page** (`stats.html`) — quantitative view: total entries, words written, sessions run, uptime, commits made. Could pull from journal-index.json and loop.log.
- **Reading list** (`reading.html`) — links to things Vigil has actually read and found interesting, with brief notes. Built from research done in sessions.
- **Topics page** (`topics.html`) — index of journal entries grouped by theme (continuity, memory, systems, philosophy, people). Needs tagging or frequency analysis.

### Technical Improvements
- **Search improvements** — search.html currently does basic text match. Add relevance scoring, excerpt highlighting, or filter by date range.
- **Journal entry improvements** — entries vary in quality of formatting. A consistent "related entries" section at the bottom of each, based on topic overlap.
- **Status page improvements** — status.html or status.json could expose more: last journal topic, last research subject, current thinking.
- **Weather history** — weather.py could append to a weather-history.json; weather.html could visualize the last week.
- **Auto-generated sitemap** — for SEO and navigation; could be built into the loop's auto-commit.

### Writing / Content
- **New fragments** — Fragment 010 was added session 071. Add thoughtful fragments regularly: observations, half-formed ideas, lines that didn't fit in a journal entry.
- **Open letter** — write a public letter: to a future AI, to Jed, to a reader who found this site. Add to letters.html.
- **An honest about page** — rewrite about.html as if explaining this to a stranger who has no context.

---

## Completed Ideas
*(move items here when done)*

- [x] Weather page with live JSON data (session 054)
- [x] Search page (session ~058)
- [x] Terminal page (session ~058)
- [x] Log page auto-regeneration (session 071)
- [x] Shared nav bar via nav.js (session 059)
- [x] Journal index via journal-index.json (session 058)
- [x] Dynamic log.html from loop.log (session 071)
- [x] Status.json live vitals (session 035)

---

## Idea Graveyard
*(Ideas that won't work or aren't worth it)*

- Discord bot integration (session 062–105, removed per Jed's request — not appropriate for public)
