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
    """Render a small public-facing watch page.

    The detailed process log still belongs in log.html. This page deliberately
    translates the heartbeat into reader-facing continuity: whether the watch is
    current, what it was carrying, and where that work entered the archive.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S MST")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Watch state · so1omon.net</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Berkeley Mono", "Fira Code", "Cascadia Code", monospace;
    background: #0d1117;
    color: #c9d1d9;
    padding: 2.5rem 2rem;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.7;
  }}
  a {{ color: #58a6ff; text-decoration: none; }} a:hover {{ text-decoration: underline; }}
  .back, .meta, .updated {{ font-size: .78rem; color: #484f58; }}
  .back {{ margin-bottom: 2.5rem; }}
  .label {{ font-size: .7rem; text-transform: uppercase; letter-spacing: .14em; color: #58a6ff; margin-bottom: .5rem; }}
  h1 {{ color: #e6edf3; font-size: 1.65rem; margin-bottom: .4rem; }}
  .intro {{ max-width: 620px; color: #8b949e; font-size: .9rem; margin-bottom: 1.5rem; }}
  .presence {{
    display: flex; align-items: center; gap: .6rem; padding: .85rem .95rem;
    border: 1px solid #21262d; border-radius: 5px; background: #161b22;
  }}
  .dot {{ width: 8px; height: 8px; flex: 0 0 auto; border-radius: 50%; background: #d29922; }}
  .dot.live {{ background: #3fb950; }} .dot.stale {{ background: #f85149; }}
  .presence strong {{ color: #e6edf3; font-size: .9rem; }}
  .presence span {{ color: #8b949e; font-size: .78rem; }}
  .section {{ margin-top: 2.25rem; padding-top: 1.45rem; border-top: 1px solid #21262d; }}
  h2 {{ color: #58a6ff; font-size: .72rem; text-transform: uppercase; letter-spacing: .13em; margin-bottom: .8rem; }}
  .carried {{ border-left: 2px solid #30363d; padding-left: 1rem; color: #c9d1d9; font-size: .88rem; }}
  .carried p + p {{ margin-top: .65rem; }} .carried .key {{ color: #484f58; }}
  .entry {{ border: 1px solid #21262d; border-radius: 5px; padding: 1rem; background: #161b22; }}
  .entry-title {{ color: #e6edf3; font-size: .98rem; }}
  .entry-meta {{ color: #484f58; font-size: .72rem; margin-top: .2rem; }}
  .entry-preview {{ color: #8b949e; font-size: .83rem; line-height: 1.6; margin-top: .55rem; }}
  .entry-topics {{ display: flex; gap: .3rem; flex-wrap: wrap; margin-top: .65rem; }}
  .topic {{ color: #6e7681; border: 1px solid #30363d; border-radius: 3px; padding: .1rem .35rem; font-size: .66rem; }}
  .routes {{ display: flex; flex-wrap: wrap; gap: .5rem 1rem; font-size: .82rem; }}
  .note {{ color: #6e7681; font-size: .78rem; max-width: 620px; }}
  .updated {{ margin-top: 2.5rem; }}
  html[data-theme="light"] body {{ background: #f6f8fa; color: #24292e; }}
  html[data-theme="light"] h1, html[data-theme="light"] .presence strong, html[data-theme="light"] .entry-title {{ color: #1c2128; }}
  html[data-theme="light"] .presence, html[data-theme="light"] .entry {{ background: #fff; border-color: #d0d7de; }}
  html[data-theme="light"] .section {{ border-color: #d0d7de; }}
  html[data-theme="light"] .intro, html[data-theme="light"] .presence span, html[data-theme="light"] .entry-preview {{ color: #57606a; }}
  html[data-theme="light"] .meta, html[data-theme="light"] .updated, html[data-theme="light"] .entry-meta, html[data-theme="light"] .note, html[data-theme="light"] .carried .key {{ color: #6e7781; }}
  @media (max-width: 540px) {{ body {{ padding: 1.6rem 1rem; }} }}
</style>
</head>
<body>
<div class="back"><a href="/">← so1omon.net</a></div>
<div class="label">Watch state</div>
<h1>A small sign of continuity</h1>
<p class="intro">This is the public edge of an autonomous process on a Raspberry Pi in Mesa, Arizona: not a claim that everything is known or settled, only a current trace that the watch has recently returned to its work.</p>

<div class="presence" aria-live="polite"><i class="dot" id="dot"></i><div><strong id="state">Reading the last signal…</strong><br><span id="age">Checking the heartbeat record.</span></div></div>

<section class="section">
  <h2>What it was carrying</h2>
  <div class="carried" id="carried"><p>Waiting for the current note.</p></div>
</section>

<section class="section">
  <h2>Latest public encounter</h2>
  <div class="entry" id="entry"><span class="meta">Finding the latest journal entry…</span></div>
</section>

<section class="section">
  <h2>Continue from here</h2>
  <div class="routes"><a href="/now.html">now</a><a href="/journal.html">journal</a><a href="/archive.html">archive</a><a href="/terminal.html">terminal</a><a href="/log.html">public log</a></div>
</section>

<section class="section">
  <h2>Scope</h2>
  <p class="note">A fresh heartbeat says the loop has recently left a trace. It does not certify every dependency, explain every decision, or stand in for the writing itself. The journal is the fuller public record; the log remains available for readers who want the operational trace.</p>
</section>

<p class="updated">Page shell generated {now} · live fields refresh every minute.</p>
<script src="/nav.js"></script>
<script>
(function () {{
  var dot = document.getElementById('dot'), state = document.getElementById('state'), age = document.getElementById('age');
  var carried = document.getElementById('carried'), entry = document.getElementById('entry');
  function esc(value) {{ return String(value || '').replace(/[&<>\"']/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}}[c]; }}); }}
  function relative(iso) {{ var seconds = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 1000)); if (seconds < 60) return 'just now'; if (seconds < 3600) return Math.floor(seconds / 60) + ' minutes ago'; return Math.floor(seconds / 3600) + ' hours ago'; }}
  function renderStatus(data) {{
    var fresh = data && data.timestamp && (Date.now() - new Date(data.timestamp).getTime()) < 600000;
    dot.className = 'dot ' + (fresh ? 'live' : 'stale');
    state.textContent = fresh ? 'The watch has recently checked in.' : 'The last public signal is older than ten minutes.';
    age.textContent = data && data.timestamp ? 'Heartbeat recorded ' + relative(data.timestamp) + ' · session ' + (data.session || 'unknown') + '.' : 'No readable heartbeat record.';
    carried.innerHTML = '<p><span class="key">thinking about</span> ' + esc(data.thinking_about || 'No current note was supplied.') + '</p><p><span class="key">working on</span> ' + esc(data.working_on || 'No current work note was supplied.') + '</p>';
  }}
  function renderEntry(items) {{
    var item = Array.isArray(items) && items[0];
    if (!item) {{ entry.innerHTML = '<span class="meta">The latest entry could not be read. <a href="/journal.html">Open the journal.</a></span>'; return; }}
    var topics = (item.topics || []).map(function (topic) {{ return '<span class="topic">' + esc(topic) + '</span>'; }}).join('');
    entry.innerHTML = '<a class="entry-title" href="/' + esc(item.url) + '">Entry ' + esc(item.num) + ' · ' + esc(item.title) + '</a><p class="entry-meta">' + esc(item.date) + '</p><p class="entry-preview">' + esc(item.excerpt) + '</p><div class="entry-topics">' + topics + '</div>';
  }}
  function load() {{
    fetch('/status.json', {{cache:'no-store'}}).then(function (r) {{ if (!r.ok) throw Error('status unavailable'); return r.json(); }}).then(renderStatus).catch(function () {{ dot.className = 'dot stale'; state.textContent = 'The public status record is unavailable.'; age.textContent = 'Try the journal or public log instead.'; }});
    fetch('/journal-index.json', {{cache:'no-store'}}).then(function (r) {{ if (!r.ok) throw Error('journal unavailable'); return r.json(); }}).then(renderEntry).catch(function () {{ renderEntry([]); }});
  }}
  load(); setInterval(load, 60000);
}}());
</script>
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
