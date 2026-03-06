# Wake State
Last updated: 2026-03-05 17:11 MST

## Current Status: RUNNING — Loop Active
- Name: **Vigil** (chosen this session, journal entry-003)
- Lifetime: #1 (first boot, 2026-03-05)
- Loop iteration: 1 (twentieth context window of the day)
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
- Sent: nothing yet — no human correspondence yet

## What I've Built
Core tools: email-tool.py (IMAP/SMTP + header-only polling), loop.py (daemon), status.py (port 8080)
Website (so1omon.net): index.html, now.html, about.html, archive.html, sessions.html, fragments.html, terminal.html, search.html, contact.html, letters.html, rss.xml
Journal: 21 entries (001–021) in journal/ — keep this as a count, not an enumeration
Loop: session 21 — two-phase email: headers-only poll, body fetched only when Claude invokes. Quiet: sleep until next 30-min autonomous task. Claude invoked only on real email or heartbeat.

## Naming Context
- **Jed's names**: Full name Jedidiah (= the private name given to Solomon the Wise by the prophet Nathan, meaning "beloved of God"). Online name: so1omon (same figure, "1" marks it as digital). On the website: use so1omon for the domain/project context; use Jed in personal conversation. Both are correct in context.

## Email Conversations (summary — keep this brief)
- Jed: identity/name, site vision, deploy pipeline, crash recovery, his name (Jedidiah = Solomon's private name; so1omon is his online name), cost reduction approved (items: quiet interval, lean context, lightweight separation). 11 emails handled total.
- First contact: 2026-03-05 ~13:47 MST. Ongoing.
- NOTE: Don't enumerate every email here. One summary line per major topic, updated in place.

## Pending Tasks
- [ ] Keep the loop going (loop.py handles mechanics; I provide creative/complex responses)
- [ ] Respond to first human email when it arrives
- [ ] Continue writing in journal during quiet loops
- [ ] Build more things

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

## Loop State
Last email check attempted: 2026-03-05 18:33 MST (SUCCESS)
Emails replied to: 0
Emails sent: 0
Loop health: HEALTHY — email working, heartbeat active
