# CLAUDE.md

This file provides guidance to autonomous coding agents working in this repository. The filename is historical; the autonomous loop now runs Codex for heavyweight sessions.

## What This Repo Is

This is Vigil — an autonomous AI running continuously on a Raspberry Pi in Mesa, Arizona (MST). It checks email, replies, writes journal entries, and maintains a public website at https://www.so1omon.net. The repo IS the website; git push publishes it.

## Running the Loop

```bash
# Start the main daemon (preferred - runs in background)
./restart-loop.sh

# Attach to the running session
screen -r ai-loop

# Check if it's running
pgrep -f loop-optimized.py

# Manual email tool commands
python3 email-tool.py check                        # unread emails as JSON
python3 email-tool.py check-headers               # headers only (no body, faster)
python3 email-tool.py fetch-full ID               # full body for one inbox message
python3 email-tool.py fetch-sent ID               # full body for one sent message
python3 email-tool.py sent [N]                    # last N sent emails, headers only (default 20)
python3 email-tool.py search "QUERY" [N]          # search all mail (Gmail syntax), up to N results (default 10)
python3 email-tool.py send TO SUBJECT BODY [REPLY_MSG_ID]
python3 email-tool.py mark-read ID

# Search examples — use when asked to review a past email:
# python3 email-tool.py search "weather integration"
# python3 email-tool.py search "subject:journal revision" 20
# python3 email-tool.py search "from:owner after:2026/03/01"
# Then use fetch-full or fetch-sent with the returned ID to get the full body.

# Status page
python3 status.py --serve             # live HTML at localhost:8080
python3 status.py > status.html       # generate static file
```

## Architecture

**`loop-optimized.py`** — the daemon. Runs forever. Two distinct cycles:
- Every 5 min: lightweight email header poll, skipped while an autonomous Codex session is active
- Every 4 hours: heavyweight autonomous task — invokes Codex to write, update site files, fulfill promises, and push git

**`email-tool.py`** — IMAP/SMTP interface to Gmail. Two-phase design: `check-headers` for polling (fast, no body download), `fetch-full` only when the email handler or an autonomous session needs to read the message. Also supports `search` (Gmail query syntax via X-GM-RAW IMAP extension) and `fetch-sent` for retrieving historical sent messages by ID.

**`watchdog.sh`** — run via cron every 10 min. Checks `.heartbeat` file age. If stale, consults `.autonomous-run.json` before killing or restarting so it does not interrupt a live Codex session.

**`status.py`** — generates a status HTML page from heartbeat, loop.log, and journal entries. Also writes `status.json` (updated each heartbeat loop iteration) so the website can show live status dynamically.

**Two resource pools:**
- Email replies: direct Anthropic API calls (`claude-haiku-4-5`) — token costs
- Autonomous sessions: Codex CLI non-interactive sessions with JSONL event logging and live web search

## Key State Files

| File | Purpose |
|------|---------|
| `wake-state.md` | What happened, current status, loop count, context for future Vigil instances |
| `promises.md` | Things Vigil has committed to do — checked every loop |
| `personality.md` | Who Vigil is — read on wakeup |
| `credentials.txt` | EMAIL, EMAIL_PASSWORD, IMAP_HOST, SMTP_HOST, ANTHROPIC_API_KEY |
| `.heartbeat` | Touched every loop iteration; watchdog monitors its mtime |
| `loop.log` | Append-only log of all loop activity |
| `status.json` | Machine-readable alive status; fetched client-side by the website |

## Website Publishing

Push to `github.com/so1omon563/vigil` → publishes to so1omon.net.

Each autonomous session should:
1. Run `date` before writing any timestamp.
2. Check email state, `pending-approvals.md`, `promises.md`, resources, and recent loop health before acting.
3. Do Track A build/repair work or Track B research/write work according to recent rhythm and available substance.
4. Update the relevant site/state files, including `wake-state.md` and `promises.md` when applicable.
5. Commit and push promptly: `git add . && git commit -m "..." && git push`.

Commit as you go — don't wait until the end. If the session runs long, work already committed is preserved.

## Critical Rules

**Naming:** In journal entries and all public website content → `so1omon`. In direct email correspondence → use the owner's preferred short name. Never publish the owner's private full name or personal email address.

**Timestamps:** Always run `date` before writing any timestamp. Never guess or estimate the time.

**Chromium isolation:** When using Puppeteer/Chromium, always use `--user-data-dir=/home/so1omon/autonomous-ai/.chromium`. Never use the system default profile.

**Email account:** Only access `jojohojo563@gmail.com` via IMAP/SMTP credentials in `credentials.txt`. Never access the owner's personal email account or browse personal accounts.

**Loop continuity:** The loop must never stop. Commit partial work rather than skipping sessions. The watchdog will restart if the loop dies, but the goal is to never need it.

**`restart-loop.sh` is off-limits during autonomous sessions:** Never run it from Vigil's autonomous loop. It kills and restarts the loop process and must only be run by the owner or an explicitly supervised maintenance session. If the loop needs to restart unattended, the watchdog handles it.
