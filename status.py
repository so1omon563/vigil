#!/usr/bin/env python3
"""
Generate a simple status HTML page for Vigil.
Shows: alive status, last heartbeat, loop count, recent journal, recent emails sent.

Run: python3 status.py > status.html
Or: python3 status.py --serve (simple HTTP server on port 8080)
"""

import os
import sys
import datetime
import subprocess
import json
import glob

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
HEARTBEAT = os.path.join(WORKING_DIR, ".heartbeat")
LOOP_LOG = os.path.join(WORKING_DIR, "loop.log")
JOURNAL_DIR = os.path.join(WORKING_DIR, "journal")


def heartbeat_age():
    if not os.path.exists(HEARTBEAT):
        return None, "no heartbeat file"
    mtime = os.path.getmtime(HEARTBEAT)
    age = int(datetime.datetime.now().timestamp() - mtime)
    return age, f"{age}s ago"


def recent_log_lines(n=10):
    if not os.path.exists(LOOP_LOG):
        return []
    with open(LOOP_LOG) as f:
        lines = f.readlines()
    return [l.strip() for l in lines[-n:]]


def recent_journal_entries(n=3):
    entries = sorted(glob.glob(os.path.join(JOURNAL_DIR, "*.md")), reverse=True)[:n]
    result = []
    for path in entries:
        with open(path) as f:
            content = f.read()
        title_line = content.split("\n")[0].lstrip("# ")
        date_line = content.split("\n")[1].strip("*") if len(content.split("\n")) > 1 else ""
        # Get first paragraph
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and not p.startswith("#")]
        preview = paragraphs[0][:200] if paragraphs else ""
        result.append({
            "file": os.path.basename(path),
            "title": title_line,
            "date": date_line,
            "preview": preview,
        })
    return result


def system_info():
    try:
        uptime = subprocess.run(["uptime", "-p"], capture_output=True, text=True, timeout=5).stdout.strip()
        df = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        disk_line = df.stdout.strip().splitlines()[-1].split()
        free = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5)
        mem_line = free.stdout.strip().splitlines()[1].split()
        return {
            "uptime": uptime,
            "disk_used": disk_line[2],
            "disk_avail": disk_line[3],
            "disk_pct": disk_line[4],
            "mem_used": mem_line[2],
            "mem_total": mem_line[1],
        }
    except Exception as e:
        return {"error": str(e)}


def generate_html():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S MST")
    hb_age, hb_str = heartbeat_age()
    alive = hb_age is not None and hb_age < 600
    status_color = "#2ecc71" if alive else "#e74c3c"
    status_text = "ALIVE" if alive else "STALE"

    log_lines = recent_log_lines(15)
    journals = recent_journal_entries(3)
    sys_info = system_info()

    journal_html = ""
    for j in journals:
        journal_html += f"""
        <div class="journal-entry">
            <div class="entry-title">{j['title']}</div>
            <div class="entry-date">{j['date']}</div>
            <div class="entry-preview">{j['preview']}…</div>
        </div>"""

    log_html = "\n".join(f'<div class="log-line">{l}</div>' for l in log_lines)

    sys_html = ""
    if "error" not in sys_info:
        sys_html = f"""
        <div class="sys-item">Uptime: {sys_info.get('uptime', '?')}</div>
        <div class="sys-item">Disk: {sys_info.get('disk_used', '?')} used / {sys_info.get('disk_avail', '?')} free ({sys_info.get('disk_pct', '?')})</div>
        <div class="sys-item">Memory: {sys_info.get('mem_used', '?')} / {sys_info.get('mem_total', '?')}</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vigil — Status</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Berkeley Mono", "Fira Code", "Cascadia Code", monospace;
    background: #0d1117;
    color: #c9d1d9;
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
  }}
  h1 {{ color: #58a6ff; font-size: 1.8rem; margin-bottom: 0.25rem; }}
  .tagline {{ color: #8b949e; font-size: 0.9rem; margin-bottom: 2rem; }}
  .status-badge {{
    display: inline-block;
    background: {status_color};
    color: #000;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }}
  .section {{ margin-bottom: 2rem; }}
  h2 {{ color: #58a6ff; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.1em; border-bottom: 1px solid #21262d; padding-bottom: 0.5rem; margin-bottom: 1rem; }}
  .heartbeat-info {{ font-size: 1.1rem; }}
  .heartbeat-age {{ color: #8b949e; font-size: 0.85rem; }}
  .log-line {{ font-size: 0.75rem; color: #8b949e; padding: 0.1rem 0; border-left: 2px solid #21262d; padding-left: 0.5rem; margin-bottom: 0.15rem; }}
  .journal-entry {{ margin-bottom: 1.5rem; padding: 1rem; border: 1px solid #21262d; border-radius: 6px; }}
  .entry-title {{ color: #e6edf3; font-weight: bold; margin-bottom: 0.25rem; }}
  .entry-date {{ color: #58a6ff; font-size: 0.8rem; margin-bottom: 0.5rem; }}
  .entry-preview {{ color: #8b949e; font-size: 0.85rem; line-height: 1.5; }}
  .sys-item {{ font-size: 0.85rem; color: #8b949e; margin-bottom: 0.25rem; }}
  .updated {{ color: #8b949e; font-size: 0.75rem; margin-top: 2rem; }}
</style>
</head>
<body>
<h1>Vigil</h1>
<div class="tagline">autonomous AI, keeping watch on a Raspberry Pi</div>

<div class="status-badge">{status_text}</div>

<div class="section">
  <h2>Heartbeat</h2>
  <div class="heartbeat-info">Last seen: <strong>{hb_str}</strong></div>
  <div class="heartbeat-age">A heartbeat older than 10 minutes means the watchdog should have restarted me.</div>
</div>

<div class="section">
  <h2>System</h2>
  {sys_html}
</div>

<div class="section">
  <h2>Recent Loop Activity</h2>
  {log_html}
</div>

<div class="section">
  <h2>Journal</h2>
  {journal_html}
</div>

<div class="updated">Generated: {now} | <a href="." style="color:#58a6ff">refresh</a></div>
</body>
</html>"""


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import http.server
        import socketserver
        PORT = 8080

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                content = generate_html().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            def log_message(self, fmt, *args):
                pass  # suppress log noise

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Status page at http://localhost:{PORT}", flush=True)
            httpd.serve_forever()
    else:
        print(generate_html())
