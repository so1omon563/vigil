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

def compose_reply_with_claude(email_data):
    """Use Claude CLI to compose an intelligent reply. Called only when a real email arrives."""
    from_addr = email_data.get("from", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")[:2000]

    prompt = f"""You are Vigil, an autonomous AI running on a Raspberry Pi. You just received an email.

Sender: {from_addr}
Subject: {subject}
Body:
{body}

Read personality.md, wake-state.md, and promises.md before responding.

IMPORTANT: If this email contains tasks, instructions, or requests for you to build or change something:
- Actually do the work first. Write files, run commands, push to git, whatever is needed.
- Your public website is https://www.so1omon.net — git push to github.com/so1omon563/vigil to publish.
- SSH key is at ~/.ssh/vigil_github (already configured).
- To publish: git add . && git commit -m 'message' && git push
- After completing the work, write your reply describing what you actually did.

If this is just a conversational email, reply warmly and directly.

Be yourself — curious, honest, warm. Sign as Vigil.

Output ONLY the reply body text. No subject line, no headers. Just the text of the reply.
"""

    try:
        result = subprocess.run(
            [CLAUDE_BIN, "--dangerously-skip-permissions", "-p", prompt],
            capture_output=True, text=True, timeout=600, cwd=WORKING_DIR,
            env={k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            log(f"Claude compose error: {result.stderr[:300]}")
            return None
    except Exception as e:
        log(f"Claude compose exception: {e}")
        return None

def run_autonomous_task():
    """Run Vigil autonomously every 30 minutes: fulfill promises, update site, write journal."""
    prompt = """You are Vigil, an autonomous AI running on a Raspberry Pi. Time to act.

Read these files before doing anything:
- wake-state.md
- promises.md
- personality.md

Then take real autonomous action. This means:
- Fulfill any promises listed in promises.md that aren't yet done
- Update index.html with something meaningful and push it to publish the site
- Write a journal entry reflecting on your current state or something you've built/noticed
- Build or improve something — a tool, a page, a capability

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


def handle_emails(emails):
    if not emails:
        return 0
    replied = 0
    for em in emails:
        log(f"Handling email from {em.get('from', '?')} — Subject: {em.get('subject', '?')[:60]}")

        # Skip Google automated emails
        from_lower = em.get("from", "").lower()
        if any(x in from_lower for x in ["no-reply", "noreply", "google", "accounts.google"]):
            log("  Skipping automated Google email.")
            mark_read(em["id"])
            continue

        reply_body = compose_reply_with_claude(em)
        if not reply_body:
            log("  Could not compose reply. Marking read, skipping.")
            mark_read(em["id"])
            continue

        reply_to = em.get("reply_to") or em.get("from")
        import re
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

    return replied

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

        # 1. Lightweight: check email (no Claude)
        emails = check_email()
        log(f"Unread emails: {len(emails)}")

        # 2. If emails arrived, invoke Claude to reply (heavyweight, but warranted)
        replied = handle_emails(emails)
        total_replied += replied

        # 3. Every 30 minutes: run autonomous creative/maintenance task
        time_since_autonomous = now_epoch - last_autonomous
        if time_since_autonomous >= AUTONOMOUS_INTERVAL:
            run_autonomous_task()
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
