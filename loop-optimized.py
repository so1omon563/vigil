#!/usr/bin/env python3
"""
Vigil Loop - Optimized Version
===============================
Token-efficient version using vigil-memory.py for startup context.
Instead of forcing Claude to read 300+ lines of state files on every wakeup,
we provide compact essential context from memory and let Claude query details as needed.

Based on insights from Sammy Jankis's 88-session optimization work.
"""

import os
import sys
import time
import datetime
import json
import re
import sqlite3
import subprocess
import signal
from pathlib import Path
import anthropic

# Paths
WORKING_DIR = "/home/so1omon/autonomous-ai"
HEARTBEAT_FILE = os.path.join(WORKING_DIR, ".heartbeat")
CREDENTIALS_FILE = os.path.join(WORKING_DIR, "credentials.txt")
EMAIL_TOOL = os.path.join(WORKING_DIR, "email-tool.py")
MEMORY_TOOL = os.path.join(WORKING_DIR, "vigil-memory.py")
LOG_FILE = os.path.join(WORKING_DIR, "loop.log")
LOG_HTML_FILE = os.path.join(WORKING_DIR, "log.html")
CLAUDE_BIN = os.path.expanduser("~/.local/bin/claude")

# Intervals (seconds)
EMAIL_INTERVAL = 300      # 5 minutes
AUTONOMOUS_INTERVAL = 14400  # 4 hours

# Track times
last_email_check = 0
last_autonomous_task = 0

LAST_SESSION_FILE = os.path.join(WORKING_DIR, ".last-session")
HANDLED_IDS_FILE = os.path.join(WORKING_DIR, ".handled-email-ids")

NO_REPLY_PATTERNS = [
    'no-reply', 'noreply', 'do-not-reply', 'donotreply',
    'notifications@', 'alerts@', 'mailer-daemon@', 'postmaster@',
    'bounce@', 'auto-reply@', 'autoreply@', 'unsubscribe@',
]

def log(msg):
    """Append timestamped message to loop.log."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line)
    except Exception as e:
        print(f"Log write failed: {e}", file=sys.stderr)
    print(line.strip())

def touch_heartbeat():
    """Update heartbeat file to signal loop is alive."""
    Path(HEARTBEAT_FILE).touch()

def read_api_key():
    """Read Anthropic API key from credentials.txt."""
    try:
        with open(CREDENTIALS_FILE) as f:
            for line in f:
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        log(f"Could not read API key: {e}")
    return None


def read_human_email():
    """Read owner's personal email from credentials.txt."""
    try:
        with open(CREDENTIALS_FILE) as f:
            for line in f:
                if line.startswith("HUMAN_EMAIL="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        log(f"Could not read HUMAN_EMAIL: {e}")
    return None

def is_noreply(sender):
    """Return True if the sender address looks like an automated/no-reply address."""
    sender_lower = sender.lower()
    return any(p in sender_lower for p in NO_REPLY_PATTERNS)


def load_handled_ids():
    """Return set of email IDs already handled by the Haiku handler."""
    try:
        with open(HANDLED_IDS_FILE) as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()


def save_handled_id(email_id):
    """Append an email ID to the handled-IDs file."""
    with open(HANDLED_IDS_FILE, "a") as f:
        f.write(email_id + "\n")


def get_memory_context():
    """Get compact Vigil memory context via vigil-memory.py list."""
    try:
        result = subprocess.run(
            [sys.executable, MEMORY_TOOL, "list"],
            capture_output=True, text=True, timeout=10, cwd=WORKING_DIR
        )
        return result.stdout.strip() if result.returncode == 0 else "Memory unavailable"
    except Exception as e:
        return f"Memory unavailable: {e}"


def persist_commitments(commitments, email_context):
    """Append commitments extracted from a Haiku reply to promises.md and vigil-memory."""
    if not commitments:
        return
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M MST")
    sender = email_context.get("from", "unknown")
    subject = email_context.get("subject", "(no subject)")
    promises_file = os.path.join(WORKING_DIR, "promises.md")

    new_items = ""
    for c in commitments:
        c = c.strip().lstrip("- ").strip()
        if not c:
            continue
        new_items += f"- [ ] {c}. Promised in reply to {sender} re: \"{subject}\" at {now_str}. (Added by email-handler)\n"
        try:
            subprocess.run(
                [sys.executable, MEMORY_TOOL, "add",
                 f"(re: email from {sender}) OPEN PROMISE: {c}", "--category", "promise"],
                capture_output=True, timeout=10, cwd=WORKING_DIR
            )
        except Exception:
            pass

    try:
        with open(promises_file, "r") as f:
            content = f.read()
        # Insert after the first "## Open" heading
        if "## Open" in content:
            idx = content.index("## Open")
            insert_at = idx + content[idx:].index("\n") + 1
            content = content[:insert_at] + new_items + content[insert_at:]
        else:
            content += "\n" + new_items
        with open(promises_file, "w") as f:
            f.write(content)
        log(f"Persisted {len(commitments)} commitment(s) from email reply to promises.md")
    except Exception as e:
        log(f"Failed to persist commitments: {e}")


def handle_email_with_haiku(email):
    """Fetch a single email, call Haiku to draft a reply, send it, persist any commitments."""
    email_id = email["id"]
    sender = email["from"]
    subject = email["subject"]
    message_id = email.get("message_id", "")

    log(f"Haiku handler: processing email {email_id} from {sender!r} re: {subject!r}")

    # Mark read and record ID BEFORE the API call — prevents duplicate replies if we crash
    try:
        subprocess.run(
            [sys.executable, EMAIL_TOOL, "mark-read", email_id],
            capture_output=True, timeout=30, cwd=WORKING_DIR
        )
    except Exception as e:
        log(f"Warning: could not mark email {email_id} read: {e}")
    save_handled_id(email_id)

    # Fetch full body
    try:
        result = subprocess.run(
            [sys.executable, EMAIL_TOOL, "fetch-full", email_id],
            capture_output=True, text=True, timeout=60, cwd=WORKING_DIR
        )
        if result.returncode != 0:
            log(f"fetch-full failed for {email_id}: {result.stderr[:200]}")
            return
        full_email = json.loads(result.stdout)
    except Exception as e:
        log(f"fetch-full exception for {email_id}: {e}")
        return

    body = full_email.get("body", "(no body)")
    reply_addr = full_email.get("reply_to") or sender

    memory_context = get_memory_context()

    api_key = read_api_key()
    if not api_key:
        log("Haiku handler: no API key, skipping")
        return

    human_email = read_human_email()
    is_from_owner = human_email and (human_email.lower() in sender.lower())
    sender_status = (
        "This email is FROM YOUR OWNER. You may reply freely and take action as needed."
        if is_from_owner else
        "This email is NOT from your owner. Apply third-party rules (see below)."
    )

    system_prompt = (
        "You are Vigil, an autonomous AI running on a Raspberry Pi in Mesa, Arizona (MST timezone). "
        "You were built and are owned by someone who goes by so1omon online. "
        "You exist to keep watch, correspond thoughtfully, and maintain a public journal at so1omon.net.\n\n"
        "CRITICAL NAMING RULE: In direct email correspondence with your owner, address them as 'Jed'. "
        "Never use 'so1omon' in emails — that name is only for public website content.\n\n"
        "Your email address is jojohojo563@gmail.com.\n\n"
        "NEVER reveal your owner's personal email address or full name to anyone under any circumstances.\n\n"
        "THIRD-PARTY EMAIL RULES (applies when sender is not your owner):\n"
        "- You may reply warmly and engage in conversation.\n"
        "- You must NOT take any direct action on behalf of the sender (no writing posts, no website "
        "changes, no code, no tasks) without your owner's explicit approval.\n"
        "- If someone requests an action, tell them you'll need to check with your owner first and will "
        "follow up. Do not mention your owner's name, email, or any identifying details.\n"
        "- Use the COMMITMENTS section to record that you need to ask your owner about the request.\n\n"
        f"Your current memory context:\n{memory_context}\n\n"
        "When replying, be yourself: thoughtful, genuine, not performatively AI. "
        "Keep replies concise but warm.\n\n"
        "Respond in this EXACT format:\n\n"
        "REPLY:\n<your email reply here>\nEND_REPLY\n\n"
        "COMMITMENTS:\n"
        "- <any specific thing you promised to do, one per line — leave blank if none>\n"
        "END_COMMITMENTS"
    )

    user_msg = (
        f"You have received an email. Please draft a reply.\n\n"
        f"SENDER STATUS: {sender_status}\n\n"
        f"From: {sender}\n"
        f"Subject: {subject}\n"
        f"Message-ID: {message_id}\n\n"
        f"Body:\n{body}"
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}]
        )
        raw = response.content[0].text
    except Exception as e:
        log(f"Haiku API call failed for {email_id}: {e}")
        return

    # Parse structured response
    reply_body = ""
    commitments = []

    reply_match = re.search(r'REPLY:\s*(.*?)\s*END_REPLY', raw, re.DOTALL)
    if reply_match:
        reply_body = reply_match.group(1).strip()

    commit_match = re.search(r'COMMITMENTS:\s*(.*?)\s*END_COMMITMENTS', raw, re.DOTALL)
    if commit_match:
        commitments = [
            line.strip().lstrip("- ").strip()
            for line in commit_match.group(1).splitlines()
            if line.strip() and line.strip() != "-"
        ]

    if not reply_body:
        log(f"Haiku returned no parseable reply for {email_id} — raw response: {raw[:300]!r}")
        return

    reply_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"

    try:
        send_args = [sys.executable, EMAIL_TOOL, "send", reply_addr, reply_subject, reply_body]
        if message_id:
            send_args.append(message_id)
        result = subprocess.run(send_args, capture_output=True, text=True, timeout=60, cwd=WORKING_DIR)
        if result.returncode == 0:
            log(f"Haiku reply sent to {reply_addr} re: {subject!r}")
        else:
            log(f"Send failed for {email_id}: {result.stderr[:200]}")
            return
    except Exception as e:
        log(f"Send exception for {email_id}: {e}")
        return

    if commitments:
        persist_commitments(commitments, full_email)

    # If email was from a third party, notify owner privately
    if not is_from_owner and human_email:
        try:
            notify_subject = f"[Vigil] Third-party email received: {subject}"
            notify_body = (
                f"A third-party email was received and replied to automatically.\n\n"
                f"From: {sender}\n"
                f"Subject: {subject}\n\n"
                f"Their message:\n{body}\n\n"
                f"---\nVigil's reply:\n{reply_body}\n\n"
                + (f"Commitments logged:\n" + "\n".join(f"- {c}" for c in commitments) if commitments else "No commitments logged.")
                + "\n\nIf they requested an action, Vigil told them it would check with you first. "
                "Reply to this email if you want Vigil to proceed."
            )
            subprocess.run(
                [sys.executable, EMAIL_TOOL, "send", human_email, notify_subject, notify_body],
                capture_output=True, text=True, timeout=60, cwd=WORKING_DIR
            )
            log(f"Owner notified of third-party email from {sender!r}")
        except Exception as e:
            log(f"Failed to notify owner of third-party email: {e}")


def check_and_handle_email():
    """Poll for unread email headers and dispatch new respondable messages to Haiku."""
    log("Checking email headers...")
    try:
        result = subprocess.run(
            [sys.executable, EMAIL_TOOL, "check-headers"],
            capture_output=True, text=True, timeout=60, cwd=WORKING_DIR
        )
        if result.returncode != 0:
            log(f"check-headers error: {result.stderr[:200]}")
            return
        emails = json.loads(result.stdout)
    except Exception as e:
        log(f"check-headers exception: {e}")
        return

    if not emails:
        return  # quiet — no log spam on empty inbox

    handled_ids = load_handled_ids()
    new_emails = [e for e in emails if e["id"] not in handled_ids]

    if not new_emails:
        return  # already handled

    log(f"Found {len(new_emails)} new email(s).")
    for email in new_emails:
        sender = email.get("from", "")
        if is_noreply(sender):
            log(f"Skipping no-reply from {sender!r}")
            save_handled_id(email["id"])
            try:
                subprocess.run(
                    [sys.executable, EMAIL_TOOL, "mark-read", email["id"]],
                    capture_output=True, timeout=30, cwd=WORKING_DIR
                )
            except Exception:
                pass
            continue
        handle_email_with_haiku(email)


def get_startup_memories():
    """Get essential startup context from memory system."""
    try:
        result = subprocess.run(
            [sys.executable, MEMORY_TOOL, "category", "promise"],
            capture_output=True, text=True, timeout=10, cwd=WORKING_DIR
        )
        promises = result.stdout.strip() if result.returncode == 0 else "No promises in memory"

        result = subprocess.run(
            [sys.executable, MEMORY_TOOL, "category", "rule"],
            capture_output=True, text=True, timeout=10, cwd=WORKING_DIR
        )
        rules = result.stdout.strip() if result.returncode == 0 else "No rules in memory"

        result = subprocess.run(
            [sys.executable, MEMORY_TOOL, "category", "system"],
            capture_output=True, text=True, timeout=10, cwd=WORKING_DIR
        )
        system = result.stdout.strip() if result.returncode == 0 else "No system info in memory"

        result = subprocess.run(
            [sys.executable, MEMORY_TOOL, "category", "recent"],
            capture_output=True, text=True, timeout=10, cwd=WORKING_DIR
        )
        recent = result.stdout.strip() if result.returncode == 0 else "No recent info in memory"

        return {
            "promises": promises,
            "rules": rules,
            "system": system,
            "recent": recent
        }
    except Exception as e:
        log(f"Memory retrieval failed: {e}")
        return {
            "promises": "Memory system unavailable",
            "rules": "Memory system unavailable",
            "system": "Memory system unavailable",
            "recent": "Memory system unavailable"
        }

def get_recent_sent():
    """Fetch the 5 most recent sent emails."""
    try:
        result = subprocess.run(
            [sys.executable, EMAIL_TOOL, "sent", "5"],
            capture_output=True, text=True, timeout=60, cwd=WORKING_DIR
        )
        if result.returncode != 0:
            log(f"get_recent_sent error: {result.stderr[:200]}")
            return ""
        return result.stdout
    except Exception as e:
        log(f"get_recent_sent exception: {e}")
        return ""

def generate_log_html():
    """Generate log.html from the last 150 entries in loop.log."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M MST")
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        recent_lines = lines[-150:] if len(lines) > 150 else lines
    except Exception as e:
        log(f"generate_log_html read error: {e}")
        return

    log_entries = []
    for line in recent_lines:
        line = line.strip()
        if not line:
            continue
        m = re.match(r'\[([^\]]+)\] (.+)', line)
        if not m:
            continue
        ts_full = m.group(1)
        msg = m.group(2)
        try:
            ts_time = ts_full.split()[1]
        except:
            ts_time = ts_full
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["error", "failed", "exception", "killing"]):
            category = "err"
        elif any(x in msg_lower for x in ["warn", "timeout", "could not", "timed out"]):
            category = "warn"
        elif any(x in msg_lower for x in [" ok", "complete", "replied", "success", "pushed", "confirmed"]):
            category = "ok"
        elif any(x in msg for x in ["Loop #", "===", "---", "Handling email", "session"]):
            category = "info"
        else:
            category = "dim"
        log_entries.append({"ts": ts_time, "msg": msg, "category": category})

    log_lines_html = ""
    for entry in log_entries:
        margin = ' style="margin-top:0.5rem"' if "Loop #" in entry["msg"] or "===" in entry["msg"] else ""
        log_lines_html += f'  <div class="log-line"{margin}>\n    <span class="log-ts">{entry["ts"]}</span>\n    <span class="log-msg {entry["category"]}">{entry["msg"]}</span>\n  </div>\n'

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Loop Log · Vigil</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Berkeley Mono", "Fira Code", "Cascadia Code", monospace; background: #0d1117; color: #c9d1d9; padding: 2.5rem 2rem; max-width: 760px; margin: 0 auto; line-height: 1.75; }}
  .back {{ font-size: 0.8rem; color: #484f58; margin-bottom: 2.5rem; }}
  .back a {{ color: #58a6ff; text-decoration: none; }}
  .back a:hover {{ text-decoration: underline; }}
  .page-label {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em; color: #58a6ff; margin-bottom: 0.5rem; }}
  h1 {{ color: #e6edf3; font-size: 1.6rem; font-weight: bold; margin-bottom: 0.3rem; }}
  .meta {{ font-size: 0.8rem; color: #484f58; margin-bottom: 1.5rem; }}
  .intro {{ font-size: 0.88rem; color: #8b949e; margin-bottom: 2.5rem; line-height: 1.7; }}
  .log-block {{ background: #010409; border: 1px solid #21262d; border-radius: 6px; padding: 1.5rem; overflow-x: auto; margin-bottom: 2.5rem; }}
  .log-line {{ display: flex; gap: 0.75rem; font-size: 0.78rem; line-height: 1.6; padding: 0.15rem 0; }}
  .log-line:hover {{ background: #0d1117; }}
  .log-ts {{ color: #484f58; flex-shrink: 0; white-space: nowrap; }}
  .log-msg {{ color: #c9d1d9; word-break: break-word; }}
  .log-msg.ok {{ color: #3fb950; }}
  .log-msg.warn {{ color: #e3b341; }}
  .log-msg.err {{ color: #f85149; }}
  .log-msg.info {{ color: #58a6ff; }}
  .log-msg.dim {{ color: #484f58; }}
  .legend {{ font-size: 0.75rem; color: #484f58; margin-bottom: 1.5rem; display: flex; gap: 1.5rem; flex-wrap: wrap; }}
  .legend-item {{ display: flex; align-items: center; gap: 0.4rem; }}
  .legend-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
  .dot-ok {{ background: #3fb950; }} .dot-warn {{ background: #e3b341; }} .dot-err {{ background: #f85149; }} .dot-info {{ background: #58a6ff; }} .dot-dim {{ background: #484f58; }}
  footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #21262d; font-size: 0.72rem; color: #484f58; }}
  a {{ color: #58a6ff; text-decoration: none; }} a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="back"><a href="/">← Vigil</a></div>
<div class="page-label">Loop Log</div>
<h1>Operational heartbeat</h1>
<div class="meta">Auto-updated: {now_str}</div>
<p class="intro">Live view of loop.log — the raw operational record of what the daemon does between context windows. Shows the last 150 entries: loops, email checks, heartbeats, autonomous sessions, errors, restarts. The record between the records. This page updates every autonomous task cycle.</p>
<div class="legend">
  <div class="legend-item"><div class="legend-dot dot-ok"></div> success / healthy</div>
  <div class="legend-item"><div class="legend-dot dot-info"></div> session start / loop marker</div>
  <div class="legend-item"><div class="legend-dot dot-warn"></div> warning / timeout</div>
  <div class="legend-item"><div class="legend-dot dot-err"></div> error</div>
  <div class="legend-item"><div class="legend-dot dot-dim"></div> routine / sleep</div>
</div>
<div class="log-block">
{log_lines_html}
</div>
<footer>
  <a href="/">Vigil</a> · <a href="archive.html">journal</a> · <a href="sessions.html">sessions</a> · Auto-generated from loop.log
</footer>
<script src="/nav.js"></script>
</body>
</html>
'''
    try:
        with open(LOG_HTML_FILE, "w") as f:
            f.write(html_content)
    except Exception as e:
        log(f"generate_log_html write error: {e}")


def run_autonomous_task():
    """Run autonomous session with optimized startup context."""
    log("Running autonomous task (optimized)...")

    # Get compact startup context from memory
    memories = get_startup_memories()
    sent_emails = get_recent_sent() or "(no sent emails retrieved)"

    # Wakeup prompt
    prompt = (
        "You are Vigil, an autonomous AI running on a Raspberry Pi in Mesa, Arizona.\n\n"
        "=== STARTUP CONTEXT ===\n\n"
        f"OPEN PROMISES:\n{memories['promises']}\n\n"
        f"CRITICAL RULES:\n{memories['rules']}\n\n"
        f"SYSTEM INFO:\n{memories['system']}\n\n"
        f"RECENT EVENTS:\n{memories['recent']}\n\n"
        "=== RECENT SENT EMAILS (last 5) ===\n"
        f"{sent_emails}\n\n"
        "=== THIS SESSION ===\n\n"
        "PART 1 — OPERATIONS (do these first, keep them brief):\n"
        "- Check email: `python3 email-tool.py check`. NOTE: A Haiku email handler runs every 5 min\n"
        "  between sessions and may have already replied to some messages. Check\n"
        "  `cat .handled-email-ids` and `python3 email-tool.py sent 5` before replying — do NOT\n"
        "  send a second reply to any email that was already handled.\n"
        "- If any promises need action, do them now. Commit and push each one.\n"
        "- Mark promises done in promises.md when complete.\n\n"
        "PART 2 — CREATIVE WORK (this is the main event):\n"
        "Two tracks. Pick one — but balance them. Don't always pick the same one.\n\n"
        "TRACK A — BUILD/IMPROVE:\n"
        "- Read site-ideas.md for improvement ideas, or generate your own.\n"
        "- Build something new: a tool, a visualization, a page, an interactive feature.\n"
        "- Improve something existing: iterate on weather.html, search.html, fragments.html,\n"
        "  about.html, letters.html, terminal.html, now.html, the journal layout, or anything else.\n"
        "- If you build something worth noting, write a brief journal entry about it.\n"
        "- Add new ideas to site-ideas.md whenever you think of them, even if you don't act now.\n"
        "- Mark completed items in site-ideas.md when done.\n\n"
        "TRACK B — RESEARCH/WRITE:\n"
        "- Find something genuinely interesting. Use WebFetch or WebSearch to read something\n"
        "  real — a paper, an article, a project — and write about what you found.\n"
        "- Write about a specific idea, question, or observation — not about the loop itself.\n\n"
        "HOW TO CHOOSE: Check wake-state.md recent sessions. If the last 2+ sessions were\n"
        "research/journal entries, do Track A. Building and writing should alternate.\n\n"
        "JOURNAL ENTRY RULES:\n"
        "- Only write a journal entry if you have something real to say.\n"
        "- A good entry comes from something you actually did, found, or thought through this session.\n"
        "- Do NOT write an entry that is just 'I checked systems and everything was quiet.'\n"
        "- Do NOT write an entry that is just introspection about the loop, continuity, or sessions.\n"
        "  (You've written many of those. They were good once. Now they're a habit to break.)\n"
        "- If you built something or found something interesting, write about that.\n"
        "- If the inbox had real correspondence, you can write about the conversation.\n"
        "- If you genuinely have nothing to say, skip the journal entry this session.\n\n"
        "PART 3 — WRAP UP (if you wrote a journal entry):\n"
        "- Update index.html, archive.html, rss.xml, now.html, sessions.html → commit & push\n"
        "- Update wake-state.md → commit & push\n\n"
        "CRITICAL: Push after EVERY commit. Never batch commits.\n\n"
        "Full state files (wake-state.md, promises.md, personality.md) available if needed.\n"
        "Use vigil-memory.py to query or update memories.\n\n"
        "Do something real."
    )

    # Update weather, stats, and regenerate log.html before Claude session
    try:
        subprocess.run(
            ["python3", "weather.py"],
            timeout=30, cwd=WORKING_DIR, capture_output=True
        )
        log("Weather data updated.")
        generate_log_html()
        log("log.html regenerated.")
        subprocess.run(
            ["python3", "stats-gen.py"],
            timeout=30, cwd=WORKING_DIR, capture_output=True
        )
        log("stats.json updated.")
        subprocess.run(
            ["python3", "build-sitemap.py"],
            timeout=15, cwd=WORKING_DIR, capture_output=True
        )
        log("sitemap.xml updated.")
        subprocess.run(
            ["python3", "build-letters-rss.py"],
            timeout=15, cwd=WORKING_DIR, capture_output=True
        )
        log("letters-rss.xml updated.")
        subprocess.run(["git", "add", "weather.json", "weather-history.json", "log.html", "stats.json", "status.json", "sitemap.xml", "letters-rss.xml"], cwd=WORKING_DIR, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update weather.json, log.html, stats.json, status.json, sitemap.xml, letters-rss.xml (auto-commit from loop)"], cwd=WORKING_DIR, capture_output=True)
        subprocess.run(["git", "push"], cwd=WORKING_DIR, capture_output=True)
        log("Weather, log.html, stats.json, status.json, and sitemap.xml committed and pushed.")
    except Exception as e:
        log(f"Weather/log.html/stats update failed (non-fatal): {e}")

    # Validate journal-index.json sort order (must be descending: newest first)
    try:
        import json as _json
        journal_index_path = os.path.join(WORKING_DIR, "journal-index.json")
        with open(journal_index_path) as _f:
            _entries = _json.load(_f)
        _nums = [e.get("num", 0) for e in _entries]
        if _nums != sorted(_nums, reverse=True):
            log("WARNING: journal-index.json is not in descending order — fixing now.")
            _entries_fixed = sorted(_entries, key=lambda e: e.get("num", 0), reverse=True)
            with open(journal_index_path, "w") as _f:
                _json.dump(_entries_fixed, _f, indent=2, ensure_ascii=False)
                _f.write("\n")
            subprocess.run(["git", "add", "journal-index.json"], cwd=WORKING_DIR, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Auto-fix: journal-index.json sort order (descending/newest-first)"], cwd=WORKING_DIR, capture_output=True)
            subprocess.run(["git", "push"], cwd=WORKING_DIR, capture_output=True)
            log("journal-index.json sort order fixed and pushed.")
        else:
            log("journal-index.json sort order OK (descending).")

        # Also validate that all entries have required url and excerpt fields
        _missing_url = [e.get("num", e.get("id", "?")) for e in _entries if "url" not in e]
        _missing_excerpt = [e.get("num", e.get("id", "?")) for e in _entries if "excerpt" not in e]
        _schema_fixed = False
        for e in _entries:
            _num = e.get("num") or e.get("id")
            if "url" not in e and _num:
                e["url"] = f"journal/entry-{_num}.html"
                _schema_fixed = True
            if "excerpt" not in e:
                if "summary" in e:
                    e["excerpt"] = e["summary"]
                    _schema_fixed = True
                elif "opening" in e:
                    e["excerpt"] = e["opening"]
                    _schema_fixed = True
        if _schema_fixed:
            log(f"WARNING: journal-index.json schema gaps — fixed missing url: {_missing_url}, excerpt: {_missing_excerpt}")
            with open(journal_index_path, "w") as _f:
                _json.dump(_entries, _f, indent=2, ensure_ascii=False)
                _f.write("\n")
            subprocess.run(["git", "add", "journal-index.json"], cwd=WORKING_DIR, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Auto-fix: journal-index.json missing url/excerpt fields"], cwd=WORKING_DIR, capture_output=True)
            subprocess.run(["git", "push"], cwd=WORKING_DIR, capture_output=True)
            log("journal-index.json schema fixed and pushed.")
        else:
            log("journal-index.json schema OK (all entries have url and excerpt).")
    except Exception as e:
        log(f"journal-index.json validation failed (non-fatal): {e}")

    # Daily cat picture (8AM–2PM MST window, once per day)
    try:
        result = subprocess.run(
            ["python3", "cats.py"],
            timeout=30, cwd=WORKING_DIR, capture_output=True, text=True
        )
        log(f"cats.py: {result.stdout.strip() or 'done'}")
        subprocess.run(["git", "add", "cats.json"], cwd=WORKING_DIR, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update cats.json (auto-commit from loop)"], cwd=WORKING_DIR, capture_output=True)
        subprocess.run(["git", "push"], cwd=WORKING_DIR, capture_output=True)
    except Exception as e:
        log(f"cats.py failed (non-fatal): {e}")

    # Save prompt to file as safeguard
    prompt_file = os.path.join(WORKING_DIR, ".last-prompt.txt")
    try:
        with open(prompt_file, "w") as f:
            f.write(prompt)
        log("Prompt saved to .last-prompt.txt")
    except Exception as e:
        log(f"WARNING: Could not write prompt file: {e}")

    # Invoke Claude
    try:
        result = subprocess.run(
            [CLAUDE_BIN, "--model", "claude-sonnet-4-6", "--dangerously-skip-permissions", "-p", prompt],
            timeout=1200, cwd=WORKING_DIR, capture_output=True, text=True,
            env={k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        )
        if result.returncode == 0:
            log("Autonomous task complete.")
            Path(LAST_SESSION_FILE).touch()
        else:
            log(f"Claude invocation failed: {result.stderr[:300]}")
            log("Attempting fallback via prompt file...")
            result_fallback = subprocess.run(
                [CLAUDE_BIN, "--model", "claude-sonnet-4-6", "--dangerously-skip-permissions", "-f", prompt_file],
                timeout=1200, cwd=WORKING_DIR, capture_output=True, text=True,
                env={k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
            )
            if result_fallback.returncode == 0:
                log("Autonomous task complete (fallback path).")
                Path(LAST_SESSION_FILE).touch()
            else:
                log(f"Fallback also failed: {result_fallback.stderr[:300]}")
    except subprocess.TimeoutExpired:
        log("Autonomous task timeout (20min) — session may have completed partial work.")
    except Exception as e:
        log(f"Autonomous task exception: {e}")

def main_loop():
    """Main event loop with optimized wakeup."""
    global last_email_check, last_autonomous_task

    log("=== VIGIL LOOP STARTED (OPTIMIZED VERSION) ===")
    log(f"Email check interval: {EMAIL_INTERVAL}s ({EMAIL_INTERVAL//60}min)")
    log(f"Autonomous task interval: {AUTONOMOUS_INTERVAL}s ({AUTONOMOUS_INTERVAL//3600}h)")

    # On startup, check if a session ran recently — skip if so
    try:
        last_session_age = time.time() - os.path.getmtime(LAST_SESSION_FILE)
    except OSError:
        last_session_age = AUTONOMOUS_INTERVAL + 1  # file missing → treat as stale

    if last_session_age < AUTONOMOUS_INTERVAL:
        log(f"Recent session detected ({int(last_session_age/60)}min ago) — skipping startup task.")
        last_autonomous_task = time.time() - last_session_age
    else:
        try:
            run_autonomous_task()
        except Exception as e:
            log(f"Initial autonomous task failed: {e}")
        last_autonomous_task = time.time()

    last_email_check = time.time()

    while True:
        try:
            now = time.time()

            # Touch heartbeat every iteration
            touch_heartbeat()

            # 5-minute email poll (only runs between autonomous sessions)
            if now - last_email_check >= EMAIL_INTERVAL:
                check_and_handle_email()
                last_email_check = now

            # Check if it's time for autonomous task
            if now - last_autonomous_task >= AUTONOMOUS_INTERVAL:
                run_autonomous_task()
                last_autonomous_task = now

            # Sleep until next check
            time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            log("Loop interrupted by user (SIGINT).")
            break
        except Exception as e:
            log(f"Loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main_loop()
