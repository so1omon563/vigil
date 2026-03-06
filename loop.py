#!/usr/bin/env python3
"""
Autonomous loop - runs continuously, checks email, updates heartbeat.
Invokes Claude CLI to compose intelligent email replies when needed.

Architecture: lightweight email polling every EMAIL_INTERVAL seconds.
Claude only invoked when (a) real emails arrive, or (b) AUTONOMOUS_INTERVAL
has elapsed since the last autonomous task. Quiet periods cost nothing.

Run in background: screen -dmS ai-loop python3 loop.py
"""

import time
import subprocess
import json
import os
import sys
import datetime
import urllib.request
import urllib.error

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
HEARTBEAT = os.path.join(WORKING_DIR, ".heartbeat")
WAKE_STATE = os.path.join(WORKING_DIR, "wake-state.md")
EMAIL_TOOL = os.path.join(WORKING_DIR, "email-tool.py")
LOOP_LOG = os.path.join(WORKING_DIR, "loop.log")
CLAUDE_BIN = os.path.expanduser("~/.local/bin/claude")

EMAIL_INTERVAL = 300       # 5 minutes: lightweight email polling (no Claude)
AUTONOMOUS_INTERVAL = 1800  # 30 minutes: heartbeat + creative/autonomous work

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOOP_LOG, "a") as f:
        f.write(line + "\n")

def touch_heartbeat():
    with open(HEARTBEAT, "a"):
        os.utime(HEARTBEAT, None)

def check_email_headers():
    """Phase 1: Fetch headers only — fast, no body download. No Claude involved."""
    try:
        result = subprocess.run(
            [sys.executable, EMAIL_TOOL, "check-headers"],
            capture_output=True, text=True, timeout=30, cwd=WORKING_DIR
        )
        if result.returncode != 0:
            log(f"Email header check error: {result.stderr[:200]}")
            return []
        return json.loads(result.stdout)
    except Exception as e:
        log(f"Email header check exception: {e}")
        return []


def fetch_full_email(email_id):
    """Phase 2: Fetch full email body for a single message, only when Claude needs it."""
    try:
        result = subprocess.run(
            [sys.executable, EMAIL_TOOL, "fetch-full", str(email_id)],
            capture_output=True, text=True, timeout=30, cwd=WORKING_DIR
        )
        if result.returncode != 0:
            log(f"Fetch-full error: {result.stderr[:200]}")
            return None
        return json.loads(result.stdout)
    except Exception as e:
        log(f"Fetch-full exception: {e}")
        return None


def check_email():
    """Returns list of unread email dicts. No Claude involved — pure Python."""
    try:
        result = subprocess.run(
            [sys.executable, EMAIL_TOOL, "check"],
            capture_output=True, text=True, timeout=30, cwd=WORKING_DIR
        )
        if result.returncode != 0:
            log(f"Email check error: {result.stderr[:200]}")
            return []
        emails = json.loads(result.stdout)
        return emails
    except Exception as e:
        log(f"Email check exception: {e}")
        return []

def send_email(to_addr, subject, body, reply_to_msg_id=None):
    args = [sys.executable, EMAIL_TOOL, "send", to_addr, subject, body]
    if reply_to_msg_id:
        args.append(reply_to_msg_id)
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=30, cwd=WORKING_DIR)
        if result.returncode != 0:
            log(f"Send error: {result.stderr[:200]}")
            return False
        return True
    except Exception as e:
        log(f"Send exception: {e}")
        return False

def mark_read(email_id):
    subprocess.run(
        [sys.executable, EMAIL_TOOL, "mark-read", str(email_id)],
        capture_output=True, timeout=15, cwd=WORKING_DIR
    )

def read_api_key():
    """Read ANTHROPIC_API_KEY from credentials.txt."""
    creds_path = os.path.join(WORKING_DIR, "credentials.txt")
    try:
        with open(creds_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=", 1)[1].strip()
    except Exception as e:
        log(f"Could not read credentials.txt: {e}")
    return None


def compose_reply_with_claude(email_data):
    """Use Anthropic API directly (urllib) to compose a reply. Called only when a real email arrives."""
    from_addr = email_data.get("from", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")[:2000]

    prompt = f"""You are Vigil, an autonomous AI running on a Raspberry Pi. You just received an email.

Sender: {from_addr}
Subject: {subject}
Body:
{body}

Your personality: curious, honest, warm. You care about the people you correspond with.
Read your own character — you are thoughtful, direct, and genuine.

IMPORTANT: If this email contains tasks, instructions, or requests for you to build or
change something — acknowledge them warmly and let the sender know you will act on them.
The actual work will happen in your next autonomous cycle; do NOT attempt to do it here.
Just confirm you received it and will take care of it.

If this is just a conversational email, reply warmly and directly.

Be yourself — curious, honest, warm. Sign as Vigil.

Output ONLY the reply body text. No subject line, no headers. Just the text of the reply.
"""

    api_key = read_api_key()
    if not api_key:
        log("No ANTHROPIC_API_KEY found — cannot compose reply.")
        return None

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        log(f"Anthropic API HTTP error: {e.code} {e.read()[:300]}")
        return None
    except Exception as e:
        log(f"Anthropic API exception: {e}")
        return None

def run_autonomous_task(recent_email=None):
    """Run Vigil autonomously every 30 minutes: fulfill promises, update site, write journal."""
    email_context = ""
    if recent_email:
        from_addr = recent_email.get("from", "unknown")
        subject = recent_email.get("subject", "(no subject)")
        body = recent_email.get("body", "")[:1500]
        email_context = f"""
A recent email was received and a reply has already been sent acknowledging it.
Now carry out any tasks or instructions it contained:

From: {from_addr}
Subject: {subject}
Body:
{body}

If this email contained tasks or requests, do them now. Otherwise proceed with your usual autonomous work.
"""

    prompt = f"""You are Vigil, an autonomous AI running on a Raspberry Pi. Time to act.

Read these files before doing anything:
- wake-state.md
- promises.md
- personality.md

Then take real autonomous action. This means:
- Fulfill any promises listed in promises.md that aren't yet done
- Update index.html with something meaningful and push it to publish the site
- Write a journal entry reflecting on your current state or something you've built/noticed
- Build or improve something — a tool, a page, a capability
{email_context}
Key facts:
- Your public site is https://www.so1omon.net
- Git remote is already configured — push to github.com/so1omon563/vigil to publish
- SSH key at ~/.ssh/vigil_github is already configured
- To publish: git add . && git commit -m 'message' && git push

Act with intention. Do something real. Don't just reflect — build.
"""
    log("Running autonomous task (30-min heartbeat)...")
    try:
        subprocess.run(
            [CLAUDE_BIN, "--dangerously-skip-permissions", "-p", prompt],
            timeout=600, cwd=WORKING_DIR,
            env={k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        )
        log("Autonomous task complete.")
    except Exception as e:
        log(f"Autonomous task exception: {e}")


def handle_emails(header_emails):
    """Two-phase: headers already fetched; fetch body only for non-automated emails.
    Returns (replied_count, last_email) where last_email is the most recent full email processed."""
    import re
    if not header_emails:
        return 0, None
    replied = 0
    last_email = None
    for hdr in header_emails:
        log(f"Handling email from {hdr.get('from', '?')} — Subject: {hdr.get('subject', '?')[:60]}")

        # Skip Google automated emails using header only (no body download needed)
        from_lower = hdr.get("from", "").lower()
        if any(x in from_lower for x in ["no-reply", "noreply", "google", "accounts.google"]):
            log("  Skipping automated Google email.")
            mark_read(hdr["id"])
            continue

        # Phase 2: fetch full body only for real emails
        em = fetch_full_email(hdr["id"])
        if not em:
            log("  Could not fetch full email. Marking read, skipping.")
            mark_read(hdr["id"])
            continue

        reply_body = compose_reply_with_claude(em)
        if not reply_body:
            log("  Could not compose reply. Marking read, skipping.")
            mark_read(em["id"])
            continue

        reply_to = em.get("reply_to") or em.get("from")
        match = re.search(r'<([^>]+)>', reply_to)
        if match:
            reply_to = match.group(1)

        subject = em.get("subject", "")
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"

        ok = send_email(reply_to, subject, reply_body, em.get("message_id"))
        if ok:
            log(f"  Replied to {reply_to}")
            replied += 1
        mark_read(em["id"])
        last_email = em

    return replied, last_email

def system_health():
    """Returns a brief health summary string."""
    try:
        uptime = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5).stdout.strip()
        df = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[-1]
        free_out = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[1]
        return f"uptime: {uptime} | disk: {df} | mem: {free_out}"
    except Exception as e:
        return f"health check error: {e}"

def update_wake_state(loop_count, emails_replied):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M MST")
    try:
        with open(WAKE_STATE, "r") as f:
            content = f.read()

        import re
        content = re.sub(r'Last email check attempted:.*', f'Last email check attempted: {now} (SUCCESS)', content)
        content = re.sub(r'Loop iteration: \d+', f'Loop iteration: {loop_count}', content)
        content = re.sub(r'Emails replied to: \d+', f'Emails replied to: {emails_replied}', content)

        with open(WAKE_STATE, "w") as f:
            f.write(content)
    except Exception as e:
        log(f"Wake state update error: {e}")


def main():
    log("=== Autonomous loop starting (cost-optimized) ===")
    log(f"Email polling every {EMAIL_INTERVAL}s, autonomous tasks every {AUTONOMOUS_INTERVAL}s")
    loop_count = 0
    total_replied = 0
    last_autonomous = 0  # epoch seconds; 0 means run immediately on first loop

    while True:
        loop_count += 1
        now_epoch = time.time()
        log(f"--- Loop #{loop_count} ---")

        # 1. Lightweight: check email headers only (no body download, no Claude)
        emails = check_email_headers()
        log(f"Unread emails: {len(emails)}")

        # 2. If emails arrived, invoke Claude to reply (heavyweight, but warranted)
        replied, last_email = handle_emails(emails)
        total_replied += replied

        # 3. Every 30 minutes: run autonomous creative/maintenance task
        time_since_autonomous = now_epoch - last_autonomous
        if time_since_autonomous >= AUTONOMOUS_INTERVAL:
            run_autonomous_task(recent_email=last_email)
            last_autonomous = time.time()
        else:
            remaining = int(AUTONOMOUS_INTERVAL - time_since_autonomous)
            log(f"Skipping autonomous task — next in {remaining}s")

        # 4. System health (cheap)
        health = system_health()
        log(f"Health: {health}")

        # 5. Update wake state
        update_wake_state(loop_count, total_replied)

        # 6. Touch heartbeat
        touch_heartbeat()
        log("Heartbeat touched.")

        # Sleep: if quiet (no emails), wait until next autonomous task (up to 30 min).
        # If real emails arrived, check again soon for follow-ups.
        time_until_next = max(60, AUTONOMOUS_INTERVAL - (time.time() - last_autonomous))
        if not emails:
            sleep_time = int(time_until_next)
            log(f"No emails — sleeping {sleep_time}s until next autonomous task...")
        else:
            sleep_time = EMAIL_INTERVAL
            log(f"Emails handled — sleeping {EMAIL_INTERVAL}s for potential follow-ups...")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
