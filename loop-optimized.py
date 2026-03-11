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
        "- Check email: `python3 email-tool.py check`. If unread messages exist, fetch and reply.\n"
        "  Check sent mail first (`python3 email-tool.py sent 5`) to avoid duplicate replies.\n"
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

    # Update weather and regenerate log.html before Claude session
    try:
        subprocess.run(
            ["python3", "weather.py"],
            timeout=30, cwd=WORKING_DIR, capture_output=True
        )
        log("Weather data updated.")
        generate_log_html()
        log("log.html regenerated.")
        subprocess.run(["git", "add", "weather.json", "log.html"], cwd=WORKING_DIR, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update weather.json and log.html (auto-commit from loop)"], cwd=WORKING_DIR, capture_output=True)
        subprocess.run(["git", "push"], cwd=WORKING_DIR, capture_output=True)
        log("Weather and log.html committed and pushed.")
    except Exception as e:
        log(f"Weather/log.html update failed (non-fatal): {e}")

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
