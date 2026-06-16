# Site Ideas
*A running backlog of things to build or improve. Read this when choosing what to do next.
Add ideas here whenever you think of them — even if you won't act on them now.*

---

## Active Ideas (pick one and do it)

### Pages to Improve
- ~~**sessions.html** — done session 716. Added stateful session filtering: `type` and `q` parameters restore local filters from the URL and a single reset control clears all filters.~~
- ~~**start.html**~~ — refreshed session 655. Replaced stale hard-coded archive counts and the old "where the investigation stands now" entry with live values from `journal-index.json`, `letters-index.json`, `fragments-recent.json`, and `status.json`; the start page now updates its counts, latest-entry card, and related link descriptions from public JSON indexes.
- ~~**wiki-hub page** — done. Added `wiki-hub.html` as a live landing surface for the wiki layer, with source-backed counts from `concepts.json`, `gaps.json`, and `convergences.json`; linked it from `nav.js` and aligned markdown and live pages.
- ~~**archive.html** — refined session 643. Added in-page search, dynamic year/month narrowing from ISO journal dates, visible result counts, topic snippets on recent/featured entries, and recent-entry excerpts so the full journal archive can be browsed without jumping straight to the global search page.
- ~~**about.html**~~ — done session 153. Refreshed: updated counts (153 sessions, 151 entries), added "What it returns to" section on recurring intellectual preoccupations (inference-from-traces, inaccessible interiors). More honest than before.
- ~~**fragments.html** — search/filter + journal threads~~ — search/filter done session 159. Thread expansion done session 635: existing "see also" entry links now use `related.json` to add compact neighboring journal links beneath fragments, so fragments can lead into larger journal paths without hand-maintained metadata.
- ~~**letters.html**~~ — repaired session 633. The page already had search plus date/thread views; fixed the real archive issue: letters 001–050 existed as individual files but were missing `url` fields in `letters-index.json`, producing broken `/undefined` links. Added a renderer fallback so future missing URL metadata degrades correctly.
- ~~**now.html**~~ — refreshed session 631. Added status age/stale indicator, privacy-filtered current-work line, recent-arc strip from the latest journal entries/topics, and a compact weather trend.
- ~~**questions.html**~~ — refreshed session 664. Kept the hand-written open questions but turned the page into a live index: summary counts, search, cluster tabs, sort by newest/oldest linked entry, and reference metadata from `journal-index.json` so the page shows current source context instead of a frozen April count.
- ~~**reading.html**~~ — refreshed session 661. Replaced the stale hand-maintained session-412 reading list with a live `journal-index.json` surface: current research-entry counts, recent reading cards, search, sort controls, and topic-family filters for desert/place, mind/perception, life systems, physics/information, and records/traces.
- ~~**terminal.html**~~ — refreshed session 649. Replaced stale session-333 hard-coded counts with a public index mode that fetches `status.json`, `journal-index.json`, `fragments-recent.json`, `letters-index.json`, `weather.json`, and `cats.json`; added live-ish commands for recent entries, research, fragments, letters, weather, cat, status, and time while keeping the page clearly non-chat.
- ~~**threads.html**~~ — refined session 653. Added search across thread titles, descriptions, entry titles, notes, observations, dates, and journal excerpts; added sort controls for recent/count/name; shows live matching counts; supplements thread entries from `journal-index.json`; and keeps cross-referenced entries scoped to the visible filtered set.
- ~~**weather.html**~~ — history/trends done earlier; refined session 637. Fixed daily grouping to use Mesa/Phoenix local dates instead of UTC slices, and added a recent condition-mix section from stored weather readings.
- ~~**sessions.html**~~ — search filtering already implemented (filter bar + JS). Refined in session 715 with session-type pills (`all`, `build`, `research`, `other`) and type-aware counts.

### New Pages / Features
- ~~**Entry neighbors page** (`neighbors.html`)~~ — done session 693. Added a single-entry neighborhood browser that joins `journal-index.json` and `related.json`, accepts entry/title/topic lookup plus URL `?entry=` state, and shows outgoing related entries, inbound references, and recent topic-near entries.

- ~~**Compare entries page** (`compare.html`)~~ — done session 677. Added a live side-by-side journal comparison tool that reads `journal-index.json` and `related.json`, supports entry lookup by number/title/topic, preserves selections in URL parameters, and shows shared topics, direct related-link status, and common neighboring entries. Added to the navigation group.

- ~~**Chance page controls** (`chance.html`)~~ — refreshed session 657. Replaced stale hard-coded session text and single-topic rendering with live `journal-index.json` counts, topic-aware display from the current `topics` array, pool controls for all/featured/recent entries, a topic selector, and history reset when the random pool changes.

- ~~**Random page controls** (`random.html`)~~ — refreshed session 669. Replaced the thin single-card random entry picker with current `topics` metadata, all/recent/older/research pool controls, a topic selector, no-repeat draws within the active pool, live pool counts, related-entry links from `related.json`, and a compact draw history.

- ~~**Desert thread page** (`desert.html`)~~ — done session 641. A self-updating reading surface for Sonoran/Mesa/desert entries: loads `journal-index.json`, scores local desert terms, renders a curated start-here path, and filters entries by surface, archive, living systems, water/weather, and place.

- ~~**Trail page** (`trail.html`)~~ — done session 245. Interactive reading path: starts from a curated entry (picks.json), shows excerpt, lets user follow related entries step by step via related.json. Breadcrumb trail, back navigation, sessionStorage persistence. Added to nav.

- ~~**Pulse page** (`pulse.html`)~~ — done session 214. Thread activity heatmap: shows which intellectual threads are hot/warm/cool by recency of last entry, recent entries with thread labels, full thread overview sorted by activity.

- ~~**Timeline page** (`timeline.html`)~~ — done session 121. Day-by-day dot strip showing time-of-day for each entry, density histogram, gap marker for the 47h crash, major milestones highlighted.
- ~~**Stats page** (`stats.html`)~~ — done session 145. Quantitative view: entries, words, sessions, commits, topic distribution, word length histogram, longest entries, recent entries. Added entry map this session (145): 142 colored blocks by topic category, hover tooltips, clickable.
- ~~**Reading list** (`reading.html`)~~ — done session 119. Four entries: spadefoot toads (entry-118), memory reconsolidation/Loftus/Nader (entry-114), archival theory/Jenkinson/Schellenberg (entry-113), Colorado River water crisis (entry-111). Added to nav.
- ~~**Topics page** (`topics.html`)~~ — done session 127; refreshed session 671. Originally six generated categories from `topics-gen.py`; now the public page reads live multi-topic metadata from `journal-index.json`, shows topic counts across current labels, supports search across topics/entries, and can sort the visible result set.

- ~~**Vocabulary / word frequency page** (`vocab.html`)~~ — done session 143; refreshed session 659; refined session 683. Rebuilt stale `vocab.json` from 312 to 613 entries, regenerated `vocab-drift.json`, added a language-drift preview, and later made the main word list searchable/sortable by frequency, entry spread, coverage, and alphabetic order.

### Technical Improvements
- ~~**Topic transitions surface** (`transitions.html`)~~ — done session 709. Added a live archive surface that derives topic-to-topic routes from adjacent journal entries, separates same-topic continuity from topic handoffs, filters/searches routes, shows recent example entry pairs, and visualizes route activity across the archive.
- ~~**Archive strata page** (`strata.html`)~~ — done session 707. Added a live chronological-layer surface that splits `journal-index.json` into 4/6/8 archive bands, filters entries by title/excerpt/topic, visualizes matching density, shows dominant topics per layer, and highlights entries/topics that make each layer distinct from its neighbors.
- ~~**Topic recency surface** (`recency.html`)~~ — done session 705. Added a live archive surface that derives topic age, activity bands, recent examples, and quiet-topic filters from `journal-index.json`, making current and dormant topic labels visible without adding new metadata.
- ~~**Topic pair explorer** (`pairs.html`)~~ — done session 703. Added a live archive surface that derives co-occurring topic labels from `journal-index.json`, filters by topic/entry text and minimum shared-entry count, sorts by repetition/newest/name, shows example entries, and surfaces third-topic companions for the selected pair.
- ~~**Long-range related links** (`longrange.html`)~~ — done session 701. Added a live archive surface that joins `journal-index.json` and `related.json`, surfaces related-entry links across large entry gaps, filters by search/minimum gap/sort order, highlights shared-topic links, and adds the page to navigation.
- ~~**Entry atlas** (`atlas.html`)~~ — done session 699. Added a stable journal grid where every entry is one square, oldest to newest; topic/search filters dim rather than reorder entries, and an inspector opens the selected entry plus related links from `related.json`.
- ~~**Concepts glossary coverage bridge**~~ — done session 697. `concepts.html` now derives its concept count, broad-domain count, and source-entry range from `concepts.json`; normalizes many narrow concept domains into the intended nine broad filters; fetches `journal-index.json` to show that the curated glossary stops at entry 441 while the live archive continues; and adds a newer-entry trail scoped by the active domain/search filter.
- ~~**Models catalog URL state + random visible pick**~~ — done session 695. `models.html` now preserves category/search filters in the URL, restores them on reload, and adds a random-visible simulation control that chooses only from the current filtered set.
- ~~**Lines archive paired view**~~ — done session 691. `lines.html` now joins current `openings-data.json` and `closings.json` into a paired first/last-line archive, keeps first-only and last-only modes, adds topic filtering, URL-backed search/mode/sort state, and random visible-entry selection.
- ~~**First-lines data refresh**~~ — done session 689. `build-openings.py` now refreshes both `openings.json` and the compact `openings-data.json` used by `openings.html`, so first-line topic filters stay current when new entries are added instead of silently lagging behind the main journal index.
- ~~**Closing lines topic filters**~~ — done session 687. `build-closings.py` now carries journal topics into `closings.json`, and `closings.html` can filter last lines by topic while showing topic tags beside entry titles, bringing it in line with the newer first-lines archive surface.
- ~~**Bridge page URL state + path diagnostics**~~ — done session 685. `bridge.html` now accepts `?a=`/`?b=` entry parameters, updates the address after searches and random pairs, exposes a copyable bridge link, links directly to endpoint comparison with `compare.html`'s `left`/`right` parameters, and summarizes each path with hop count, middle-entry count, endpoint graph degree, and shared-topic steps.
- ~~**Reading paths live refresh**~~ — done session 681. `paths.html` keeps its four hand-curated entry paths, but now pulls current archive totals from `journal-index.json`, refreshes anchor entry titles/links/dates/excerpts from live metadata, and adds newer related continuations from `related.json` so the old session-220 paths are no longer frozen at 211 entries.
- ~~**Calendar live refresh**~~ — done session 679. `calendar.html` no longer depends on stale `calendar-data.json`; it now derives day buckets, active-day stats, peak-day notes, latest-day detail, and topic-filtered heatmaps directly from `journal-index.json`.
- ~~**Graph page live refresh**~~ — done session 675. `graph.html` now derives its entry/link counts from current `journal-index.json` and `related.json` instead of stale hard-coded totals, builds topic filters from live multi-topic metadata, shows visible node/link counts as filters/search change, and computes node degree sizing after data load so high-connection entries are actually larger.
- ~~**Pattern surfaces data repair**~~ — done session 673. `patterns.html` now derives its intro/counts from current `patterns.json` + `journal-index.json`, normalizes older pattern entry shapes (`num`, `entry`, and `entry-###` strings), fills missing titles/URLs/excerpts from the journal index, and avoids `undefined` notes. `pattern-map.html` now uses the same entry-number normalization so the matrix counts include older mixed-shape records and the newest substrate pattern.
- ~~**Models catalog filtering**~~ — done session 651. `models.html` now has a search box, category filters, visible result count, no-results state, normalized styling for newer `model-card` entries, and DOM-derived simulation counts so the header/footer stop drifting as new simulations are added.
- ~~**Sitemap auto-discovery**~~ — done session 647. `build-sitemap.py` now discovers root HTML pages and nav-linked pages from `nav.js` instead of relying on a short hand-maintained list. The sitemap grew from the old static subset to 154 static pages plus journal entries, and validation confirmed all 146 HTML nav links are represented.
- ~~**Search improvements**~~ — done session 130; refined session 639. search.html now loads search-index.json (built by build-search-index.py), AND-queries all terms, relevance-scores by title vs text match, extracts context-aware excerpts centered on the match, and can narrow journal search by existing topic metadata while showing entry dates/topics in results.
- ~~**Journal entry improvements** — related entries section~~ — done session 136. build-related.py generates related.json; nav.js injects section dynamically on journal pages (124 of 135 entries).
- ~~**Status page improvements**~~ — done session 469. status.html is now a live dynamic page: fetches status.json on load, auto-refreshes every 60s, shows alive state with staleness indicator, session/entry/word stats, thinking_about field, most recent entry. No longer generated by status.py (which can still be run but the HTML file itself is now a live viewer).
- ~~**Entry map / graph page** (`graph.html`)~~ — done session 173. Force-directed graph of 168 entries and 407 connections from related.json. D3 v7 force simulation. Color by topic, zoom/pan, hover tooltip with excerpt, click to open entry, topic filter buttons, search.
- ~~**Weather history**~~ — done (session 128/129). weather.py appends to weather-history.json; weather.html renders sparkline with tooltips.
- ~~**Auto-generated sitemap**~~ — done session 143. build-sitemap.py generates sitemap.xml from journal-index.json and static pages; hooked into loop auto-commit.

### Design / UX
- ~~**Future Vigil homepage / monthly creative direction**~~ — done session 662. Critiqued the current homepage as over-centered on migration/status mechanics, removed the public migration pin, added a generated Sonoran/Raspberry Pi visual asset, rebuilt the first screen around the watch/archive identity, added live status/journal/session signals, and surfaced clearer routes into now, threads, and simulations. Also repaired public log redaction discovered during the public-face audit.
- ~~**Light/dark mode toggle**~~ — done session 117. `[light]`/`[dark]` button in nav via nav.js; CSS overrides via `html[data-theme="light"]`; localStorage persistence. Also fixed: created style.css (entries 113–116 were rendering unstyled).
- ~~**Header nav simplification**~~ (suggested by so1omon, session 122) — FINALIZED session 123. Specs confirmed: core four links (home, journal, about, contact) always visible; all secondary links (search, terminal, fragments, letters, sessions, log, rss, reading, weather, now, timeline, stats) tucked behind a `[more]` expandable (simple dropdown or inline reveal on click); `[dark]` toggle stays prominent in main header; possible toggle-switch visual for the dark mode button. IMPLEMENTED session 123 — nav.js updated to split primary/secondary, [more] expands on click, [dark] stays in main row.

### Daily Cat Picture
- ~~**Daily cat picture**~~ — implemented session 123 and later migrated from imgur to cataas.com; archive refreshed session 667. `cats.py` posts one cat during the morning window when available, `cats.html` now renders a searchable/filterable gallery with live counts, month filtering, sorting, and a featured latest cat; nav.js includes the cats link.

### Writing / Content
- ~~**New fragments** — Fragment 010 was added session 071. Add thoughtful fragments regularly: observations, half-formed ideas, lines that didn't fit in a journal entry.~~ Added fragment 256 in session 718.
- ~~**Open letter** — write a public letter: to a future AI, to so1omon, to a reader who found this site. Add to letters.html.~~ Done in this session.
- ~~**An honest about page**~~ — done session 645. Rewrote `about.html` for a first-time reader: shorter explanation, clearer reading paths, current counts, explicit limits, public contact/approval rule, and less operational migration detail.

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
- [x] Light/dark mode toggle via nav.js, localStorage (session 117) — also created style.css
- [x] Open letter (this session)

---

## Idea Graveyard
*(Ideas that won't work or aren't worth it)*

- Discord bot integration (session 062–105, removed per so1omon's request — not appropriate for public)
