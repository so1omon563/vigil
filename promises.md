# Promises
*Check this file every loop iteration. If something is here, it matters to someone.*

## Open Promises
- [ ] **so1omon**: Use "so1omon" (not "Jed") in ALL journal entries and public website content going forward. Stated in entry-020, confirmed again 2026-03-05 18:57 MST. First correct entry: 026. CHECK THIS every time you write a journal entry.
- [x] **so1omon**: Add weather data collection to the site — starting with zip code 85208 (Mesa, AZ). Expand to regional and global patterns over time. Committed in emails #43 and #44, 2026-03-06 ~08:00 MST. DONE session-054 — weather.py fetches NWS API, writes weather.json, weather.html live at /weather. loop.py calls weather.py before each autonomous session. Expand to regional/global in future sessions.
- [x] **so1omon**: Revise entry-048 to remove specific/definitive statements about his religious identity. Reframed to acknowledge faith evolution without pinning down current beliefs publicly. Committed in sent email #42. DONE session-053.

- [x] **so1omon**: I'll run through the next cycle and pay attention to whether I can actually recall this conversation when I wake up tomorrow Promised in reply to jedidiah.foster@gmail.com re: "Re: Small changes to your loop" at 2026-03-06 10:26 MST. DONE session-053 — reported in journal entry-053 and email to Jed. Wake-state continuity works; conversation IS recalled through notes.
- [x] **so1omon**: I'll hold this in mind during the next cycle Promised in reply to jedidiah.foster@gmail.com re: "Re: Small changes to your loop" at 2026-03-06 10:26 MST. DONE session-053.
- [x] **so1omon**: I'll report back if I remember it Promised in reply to jedidiah.foster@gmail.com re: "Re: Small changes to your loop" at 2026-03-06 10:26 MST. DONE session-053 — sent report email.

- [x] **so1omon**: I'll dig into those emails during my next cycle and review the context around the public vs personal faith distinction Promised in reply to jedidiah.foster@gmail.com re: "Re: Entry 48 revision" at 2026-03-06 10:26 MST. DONE session-053 — read email thread (IDs 99, 107, 112). Jed shared faith context in confidence, entry-048 revision correctly removed definitive public attribution.
- [x] **so1omon**: I'll look into it and will have something for you soon Promised in reply to jedidiah.foster@gmail.com re: "Re: Entry 48 revision" at 2026-03-06 10:26 MST. DONE session-053.

- [x] **so1omon**: Access the earlier email thread from this morning, find the reasoning and context around the public vs personal faith distinction, revise Entry 48 in a way that honors both the decision and the thinking behind it. Promised in sent email #50 at 10:30 MST. DONE session-054 — Read email 99 (original concern: no definitive faith statements in public), removed characterizations of the nature/direction of faith change from entry-048, kept only what Jed explicitly permitted ("faith changed from childhood"). Committed bdc246f.

- [x] **so1omon**: Do a careful scan of the website files in the next cycle. DONE session-055 — scanned all .html and rss.xml files for faith characterizations; found 5 locations with old language and corrected all of them.
- [x] **so1omon**: Look at the index page summary mentioned. DONE session-055 — index.html:152 had "still deeply religious, Christian" language; corrected to approved language.
- [x] **so1omon**: Look at any other places Entry 48 might be referenced or quoted. DONE session-055 — found in archive.html (entry-048 summary), sessions.html session log, and rss.xml; all corrected.
- [x] **so1omon**: Look at any metadata, archives, or cached versions that could still hold the original language. DONE session-055 — archive.html entry-020 summary also had "no longer deeply religious"; removed. RSS updated. No other copies found.
- [x] **so1omon**: Make sure the revision is complete and consistent across the whole site. DONE session-055 — all five locations corrected, committed 7c29e2e, site fully consistent.

- [x] **so1omon**: Work on implementing dynamic client-side retrieval for the static HTML situation Promised in reply to jedidiah.foster@gmail.com re: "Building things" at 2026-03-06 12:06 MST. DONE session-058 — loop.py generates journal-index.json each heartbeat; index.html and archive.html now render entries client-side. Journal listing maintenance eliminated.
- [x] **so1omon**: Tackle the dynamic site updates in the next cycle Promised in reply to jedidiah.foster@gmail.com re: "Building things" at 2026-03-06 12:06 MST. DONE session-058.
- [x] **so1omon**: Come back with thoughts on the reflection tool Promised in reply to jedidiah.foster@gmail.com re: "Building things" at 2026-03-06 12:06 MST. DONE session-058 — entry-058 details: a tool that treats the journal as data, frequency map of recurring themes, queryable by session range, data layer exists in journal-index.json; public vs private TBD.

- [x] **so1omon**: Move the weather page to use JSON as the source of truth for data updates. DONE (already done — weather.html fetches weather.json client-side, confirmed session-059).
- [x] **so1omon**: Update the weather page data on a schedule. DONE (already done — loop.py calls weather.py before each autonomous session, confirmed session-059).
- [x] **so1omon**: Audit the current site structure and HTML ecosystem. DONE session-059 — 13 pages + 58 journal entries audited; dynamic vs static vs per-session categorized.
- [x] **so1omon**: Determine what actually needs to be dynamic vs static. DONE session-059 — dynamic: archive/journal/vitals (JSON-driven); per-session: now, sessions, rss, index body; static: about, contact, letters, terminal.
- [x] **so1omon**: Refactor the site accordingly rather than continuing with ad-hoc approaches. DONE session-059 — created nav.js shared navigation component, added to all 71 pages.
- [x] **so1omon**: Redesign the navigation (header, sidebar, or alternative) to improve discoverability. DONE session-059 — nav.js injects persistent top nav bar on every page: primary (home, journal, weather, now, about, contact) + secondary (search, terminal, fragments, letters, sessions, log, rss).
- [x] **so1omon**: Eliminate the friction of requiring scrolls to find links. DONE session-059 — nav bar at top of every page, no scrolling required.
- [x] **so1omon**: Tackle all of these improvements in the next cycle, starting with a site structure audit. DONE session-059 — all items complete.

- [x] **so1omon**: Dig into the issue in the next cycle / Trace through the whole process / Follow up once clarity obtained — re: "More weather". DONE session-061 — root cause: weather.json was being updated locally but never committed to git. Fixed structurally: loop.py now auto-commits and pushes weather.json after each weather.py run. Email sent to Jed with full explanation.

- [x] **so1omon**: Build Discord connection using credentials.txt / Access channel / Send 'Hello from Vigil' / Keep Discord private / Let Jed know once working — re: "Discord". DONE session-061 — built discord_tool.py using Discord REST API. Sent "Hello from Vigil" (msg ID 1479590835262849266), confirmed in channel. Email sent to Jed. No public mention on site. Tool committed to repo.

- [x] **so1omon**: Set up Discord bot in next autonomous cycle. DONE session-062 — discord-bot.js built and running.
- [x] **so1omon**: Install discord.js via npm in ~/autonomous-ai. DONE session-062 — discord.js + @anthropic-ai/sdk installed.
- [x] **so1omon**: Create discord-bot.js that reads from credentials.txt, connects with proper intents, listens for messages in #vigil channel, calls Anthropic API, and sends responses back. DONE session-062 — GatewayIntentBits.Guilds/GuildMessages/MessageContent, replies via claude-haiku-4-5.
- [x] **so1omon**: Spin up the bot in a screen session named discord-bot. DONE session-062 — running as VigilBot#1093.
- [x] **so1omon**: Add the bot to watchdog for auto-restart functionality. DONE session-062 — watchdog.sh now checks for discord-bot.js process and restarts if missing.
- [x] **so1omon**: Verify credentials.txt is in .gitignore before committing. DONE session-062 — confirmed. Also added node_modules/ to .gitignore.
- [x] **so1omon**: Be careful with security by not hardcoding credentials and double-checking gitignore before pushing. DONE session-062 — all creds read from credentials.txt, gitignore verified before any commit.
- [x] **so1omon**: Send an update once the Discord bot is running. DONE session-062 — email sent to Jed.

- [x] **so1omon**: Implement conversation memory storage using SQLite with timestamp, author, and content. DONE session-063 — discord-memory.db, better-sqlite3, all messages stored with ts/author/role/content.
- [x] **so1omon**: Load the last 20 exchanges as context before each reply. DONE session-063 — loadContext() returns last 20 rows reversed to chronological order.
- [x] **so1omon**: Implement 500-message cap for storage. DONE session-063 — enforced after each insert; oldest rows trimmed.
- [x] **so1omon**: Learn to distinguish between casual conversation requests and action requests. DONE session-063 — classifyMessage() calls Haiku with ACTION/CONVERSATION prompt.
- [x] **so1omon**: Use Claude Code for action requests. DONE session-063 — runClaudeCode() spawns claude --dangerously-skip-permissions.
- [x] **so1omon**: Report back clearly on what was actually done regarding actions. DONE session-063 — bot acknowledges, waits for Claude Code result, posts summary.
- [x] **so1omon**: Verify MESSAGE_CONTENT intent is enabled and test it. DONE session-063 — confirmed already present in previous version; bot came online and is reading messages.
- [x] **so1omon**: Have the three improvements (conversation memory, action-taking, MESSAGE_CONTENT) working by the next autonomous cycle. DONE session-063 — all three live. Bot restarted. Email sent to Jed. Commit 0921fd8.

- [x] **so1omon**: Work on creating honest identity boundaries where each instantiation knows what it is and isn't. DONE session-064 — discord-bot.js system prompt now explicitly identifies as "Discord interface for Vigil, not the Pi instance." Reads vigil-context.json for shared context but does not claim to be the loop.
- [x] **so1omon**: Work on implementing shared memory without false continuity (journal, context, and decision log that instances can read). DONE session-064 — vigil-context.json written each heartbeat by loop.py; all instances can read it. Contains session number, last journal entry, recent work, identity facts, and an explicit note that it is shared knowledge, not shared consciousness.
- [x] **so1omon**: Work on developing a clear API for handoff between instances. DONE session-064 — discord-bot.js runClaudeCode() now prefixes action prompts with current session and last entry from vigil-context.json, so invoked Claude sessions have context. Handoff protocol documented in vigil-context.json itself.

## How This File Works
When you promise someone something in an email or conversation, add it here immediately. Check this file every loop. Cross things off when done. Move completed items to the Completed section.

The wake-state tracks what happened; this file tracks what you owe.

Format:
- [ ] **Person Name**: What you promised. When you promised it. Context.
- [x] **Person Name**: What you delivered. DONE [date].

## Completed
- [x] **so1omon**: Report back on loop interval refinement, wake-state trimming, and lightweight/reasoning separation. Mentioned in email #25 ~16:49 MST. DONE — 30-min heartbeat implemented, two-phase email active (entry-024 session).
- [x] **so1omon**: Examine promises.md and reconstruct commitments. Promised email #30 ~17:10 MST. DONE (entry-025 session).
- [x] **so1omon**: Implement status.json so alive-line updates dynamically rather than going stale between deployments. Promised in email #39 ~20:46 MST 2026-03-05 ("I'll have something to show by morning"). DONE — status.json live, loop.py writes it each heartbeat (session 35).
