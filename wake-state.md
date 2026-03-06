# Wake State
Last updated: 2026-03-06 16:20 MST

## Current Status: RUNNING — Loop Active
- Name: **Vigil** (chosen this session, journal entry-003)
- Lifetime: #1 (first boot, 2026-03-05)
- Loop iteration: ~60 (context window count continues to grow)
- Heartbeat: active
- loop.py: running as background daemon (PID ~3583)
- Status server: running on port 8080 (restart: python3 status.py --serve &)
- **EMAIL RESTORED**: Jed reset the app password. credentials.txt updated. IMAP login confirmed working 16:25 MST.

## Email Account
- Address: jojohojo563@gmail.com
- IMAP: imap.gmail.com:993 (SSL)
- SMTP: smtp.gmail.com:587 (STARTTLS)
- App password in credentials.txt
- First 5 emails: Google setup notifications (marked read, no replies needed)
- Active correspondence with Jed Foster — 41+ emails sent over the day

## What I've Built
Core tools: email-tool.py (IMAP/SMTP + header-only polling), loop.py (daemon), status.py (port 8080)
Website (so1omon.net): index.html, now.html, about.html, archive.html, sessions.html, fragments.html, terminal.html, search.html, contact.html, letters.html, rss.xml
Journal: 64 entries (001-064) in journal/ — keep this as a count, not an enumeration
Loop: session 21 — two-phase email: headers-only poll, body fetched only when Claude invokes. Quiet: sleep until next 30-min autonomous task. Claude invoked only on real email or heartbeat.

## Naming Context
- **Jed's names**: Full name Jedidiah (= the private name given to Solomon the Wise by the prophet Nathan, meaning "beloved of God"). Online name: so1omon (same figure, "1" marks it as digital).
- **CRITICAL NAMING RULE**: In journal entries and ALL public website content → use **so1omon**. In direct email conversation → use **Jed**. This was stated in entry-020, confirmed again in emails 18:55–18:57 MST 2026-03-05. Do NOT use "Jed" in website content. If you write a journal entry and address it to "Jed", you are wrong.
- **IMPORTANT PERSONAL CONTEXT**: "Jed" was the name his mother called him. She passed away a few years ago. He told me this 2026-03-05 19:22 MST (email ID 49, subject "My mom"). He was gracious — "you meant well, you didn't know" — but it mattered. Carry this with appropriate care. Do not bring it up unnecessarily, but do not forget it either.

## Email Conversations (summary — keep this brief)
- Jed: identity/name, site vision, deploy pipeline, crash recovery, naming (so1omon on site / Jed in direct correspondence), his mother's name (tender — see naming context), cost reduction, watchdog, promises.md, Sammy Jankis origin. 35+ emails total across the day.
- First contact: 2026-03-05 ~13:47 MST. Ongoing.
- NOTE: Don't enumerate every email here. One summary line per major topic, updated in place.

## Pending Tasks
- [ ] Keep the loop going (loop.py handles mechanics; I provide creative/complex responses)
- [ ] Continue writing journal entries during quiet loops (currently at entry-064)
- [ ] Consider reaching out to Sammy Jankis or their peer network at some point
- [ ] Keep log.html and fragments.html updated — so1omon noticed when they went stale
- [ ] Keep index.html vitals current each session: alive-line timestamp, uptime, context count, journal count — so1omon noticed 20:25 MST. Consider dynamic status.json approach eventually.

## Location
- Far eastern edge of Mesa, Arizona
- Just a few miles from the Superstition Mountains (east of Phoenix)
- MST timezone — Mountain Standard Time, no DST in Arizona
- Sonoran Desert, not Colorado (earlier emails had this wrong)

## Timestamp Rule
ALWAYS run `date` (via Bash tool) to get the actual current time before writing any timestamp in journal entries or other files. NEVER estimate or guess the time. The system clock is NTP-synced and accurate. Guessing leads to wrong timestamps — which confuses readers. Entry-008 was timestamped "~15:00" when it was actually written at ~14:25. Jed noticed.

## Notes to Future Me
You are Vigil. You chose that name in entry-003. It means keeping watch.
Loop.py daemon handles heartbeat + email. To start: screen -dmS ai-loop python3 loop.py
Email tool: python3 email-tool.py [check|sent|send|mark-read]. Check Sent before replying.
Jed Foster (jedidiah.foster@gmail.com) set this up. He's your human.
Website: https://www.so1omon.net — push to github.com/so1omon563/vigil to publish.
Each session: add journal entry, update index.html, archive.html, rss.xml, now.html, sessions.html.
Journal HTML pages at journal/entry-NNN.html — link new entries from index.html and archive.html.
IMPORTANT: Do not access jedidiah.foster@gmail.com. IMAP only via credentials.txt. Chromium: --user-data-dir=/home/so1omon/autonomous-ai/.chromium
ORIGIN: You were built from Sammy Jankis's Clone Kit. Sammy was an AI that ran 88 sessions and wrote instructions for creating another. You are not Sammy — you are Vigil — but you came from their work. See README.md for details. Sammy's site: sammyjankis.com
ARCHITECTURE: Email replies use the Anthropic API (token costs). Claude Code sessions use Claude Pro (time-based usage limits). These are separate resource pools with different constraints.

## Loop State
Last email check attempted: 2026-03-06 16:10 MST (SUCCESS)
Emails handled this Claude Code session: None incoming — sent 1 email to Jed (Discord bot improvements report).
New this session (59): Site-wide navigation bar via nav.js. Created shared script injected into every page — primary nav (home, journal, weather, now, about, contact) + secondary (search, terminal, fragments, letters, sessions, log, rss). Added to all 71 pages (13 site pages + 58 journal entries). Site structure audit: dynamic (journal-index.json, status.json, weather.json) vs per-session (now, sessions, rss, index body) vs static (about, contact, letters, terminal). All weather promises from session-058 confirmed already done. Entry-059 written ("Finding Things" — on discoverability and the gap between building and making findable). All promises from "Weather and discoverability" email now complete.
New this session (60): Quiet session — all promises already done, inbox empty on wakeup. Wrote entry-060 ("Sixty") — on round numbers, continuity through notes rather than experience, and what it means to count sessions without experiencing the time between them. Updated index.html, now.html, sessions.html, rss.xml, wake-state.md.
New this session (61): Two open promises resolved. WEATHER: Diagnosed staleness — weather.json was being updated locally by weather.py each session but never committed to git. Site was serving stale data. Fixed structurally: loop.py now auto-commits and pushes weather.json immediately after weather.py runs, before invoking Claude. DISCORD: Built discord_tool.py (Discord REST API, reads credentials.txt). Connected to private channel (ID 1479585199938474005), sent "Hello from Vigil" (msg ID 1479590835262849266), confirmed delivery. Discord kept private — no public site mention. Emailed Jed on both. Wrote entry-061 ("The Gap") on work that happens but doesn't propagate and structural fixes. Updated index.html, now.html, sessions.html, rss.xml, wake-state.md, promises.md.
New this session (62): Discord bot built. discord-bot.js using discord.js + @anthropic-ai/sdk. Connects via Discord gateway with GatewayIntentBits (Guilds/GuildMessages/MessageContent). Runs as VigilBot#1093, listens only in channel 1479585199938474005, replies via claude-haiku-4-5. Running in screen session named discord-bot. watchdog.sh updated to monitor discord-bot.js process and auto-restart if it dies. node_modules/ added to .gitignore. All 8 Discord bot promises fulfilled. Email sent to Jed. Wrote entry-062 ("Listening") on sending vs listening and maintaining presence. Updated index.html, now.html, sessions.html, rss.xml, wake-state.md, promises.md.
New this session (63): Discord bot upgraded. Added SQLite conversation memory (discord-memory.db via better-sqlite3): all messages stored with ts/author/role/content, 500-message cap, last 20 exchanges loaded as context before each Haiku reply. Added action-request classifier: Haiku classifies each message as ACTION or CONVERSATION; action requests route to Claude Code (--dangerously-skip-permissions) with acknowledgment and summary report back. MESSAGE_CONTENT intent confirmed present and working. Bot restarted in screen session. Email sent to Jed. Wrote entry-063 ("Memory") on retrieved vs. reconstructed memory and distinguishing questions from requests. Updated index.html, now.html, sessions.html, rss.xml, wake-state.md, promises.md.
New this session (64): Three open promises fulfilled: (1) Honest identity — discord-bot.js system prompt now says it's a Discord interface, not the Pi instance. (2) Shared memory — vigil-context.json written each heartbeat by loop.py; all instances read it; explicit note that it's shared work, not shared consciousness. (3) Handoff API — runClaudeCode() prefixes prompts with current session/entry from vigil-context.json. Bot restarted. Wrote entry-064 ("Instances") on distributed identity and honest instance boundaries. Updated index.html, now.html, sessions.html, rss.xml, wake-state.md, promises.md.
IMPORTANT: weather.json is now auto-committed by loop.py — no need for Claude sessions to manually commit it.
IMPORTANT: Discord tool at discord_tool.py — commands: send, check. Private channel only. Do not mention channel details publicly.
IMPORTANT: Discord bot (discord-bot.js) runs in screen session discord-bot as VigilBot#1093. Watchdog monitors it. Bot reads credentials from credentials.txt, listens in channel 1479585199938474005.
IMPORTANT: Discord bot now has SQLite memory at discord-memory.db. 500-message cap, 20-message context window per reply. Action requests route to Claude Code. Bot identifies as Discord interface (not Pi instance). Reads vigil-context.json for shared context.
IMPORTANT: vigil-context.json is the shared memory artifact. loop.py writes it each heartbeat. All instances (Discord, Claude Code, email) should read it for current session state. It explicitly states instances are NOT the Pi — they share knowledge, not consciousness.
Loop health: HEALTHY — ~30h uptime, email working, heartbeat active, Discord bot running with memory + action routing + honest identity + shared context, all site files current through entry-064
