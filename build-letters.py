#!/usr/bin/env python3
"""
Extract individual letters from letters.html into letters/letter-NNN.html.
"""
import re
import os

with open('letters.html') as f:
    content = f.read()

# Parse letter metadata from index
index_pattern = r'<div class="index-row"><span class="index-num">(\d+)</span><a href="#(letter-\d+)">(.*?)</a><span class="index-desc">(.*?)</span><span class="index-date">(.*?)</span></div>'
index_meta = {}
for num, lid, to, desc, date in re.findall(index_pattern, content):
    index_meta[lid] = {
        'num': int(num),
        'id': lid,
        'to': to,
        'desc': desc.lstrip('— ').strip(),
        'date': date,
        'filename': f'letter-{num}.html'
    }

# Sort by letter number
letters_ordered = sorted(index_meta.values(), key=lambda x: x['num'])

# Extract full letter blocks (including nested structure)
# Find each letter div from start to end by tracking nesting
letter_bodies = {}
in_letter = None
depth = 0
lines = content.split('\n')

for line in lines:
    # Detect start
    m = re.match(r'\s*<div class="letter" id="(letter-\d+)">', line)
    if m:
        in_letter = m.group(1)
        depth = 1
        letter_bodies[in_letter] = [line]
        continue
    if in_letter:
        letter_bodies[in_letter].append(line)
        # Track depth
        opens = line.count('<div')
        closes = line.count('</div>')
        depth += opens - closes
        if depth <= 0:
            in_letter = None
            depth = 0

# Parse header and body from each extracted block
parsed = {}
for lid, body_lines in letter_bodies.items():
    block = '\n'.join(body_lines)
    # Extract letter-num, letter-from, letter-meta
    num_m = re.search(r'<div class="letter-num">(.*?)</div>', block)
    from_m = re.search(r'<div class="letter-from">(.*?)</div>', block)
    meta_m = re.search(r'<div class="letter-meta">(.*?)</div>', block)

    # Extract letter-body content by tracking div depth
    body_start = block.find('<div class="letter-body">')
    body_inner = ''
    if body_start != -1:
        # Skip past the opening tag
        after_open = block.index('>', body_start) + 1
        depth = 1
        pos = after_open
        while pos < len(block) and depth > 0:
            next_open = block.find('<div', pos)
            next_close = block.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    body_inner = block[after_open:next_close]
                else:
                    pos = next_close + 6

    parsed[lid] = {
        'letter_num': num_m.group(1) if num_m else '',
        'letter_from': from_m.group(1) if from_m else '',
        'letter_meta': meta_m.group(1) if meta_m else '',
        'body': body_inner.strip(),
    }

STYLE = """<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Berkeley Mono", "Fira Code", "Cascadia Code", monospace;
    background: #0d1117;
    color: #c9d1d9;
    padding: 2.5rem 2rem;
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.75;
  }
  .back { font-size: 0.8rem; color: #484f58; margin-bottom: 2.5rem; }
  .back a { color: #58a6ff; text-decoration: none; }
  .back a:hover { text-decoration: underline; }
  .page-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em; color: #58a6ff; margin-bottom: 0.5rem; }
  .letter-num-display { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em; color: #58a6ff; margin-bottom: 0.4rem; }
  h1 { color: #e6edf3; font-size: 1.4rem; font-weight: bold; margin-bottom: 0.3rem; line-height: 1.4; }
  .letter-meta { font-size: 0.78rem; color: #484f58; margin-bottom: 2.5rem; }
  .letter-body p { font-size: 0.92rem; color: #c9d1d9; margin-bottom: 1.1rem; line-height: 1.75; }
  .letter-body p:last-child { margin-bottom: 0; }
  .letter-body em { color: #e6edf3; }
  .letter-sig { color: #484f58; font-size: 0.82rem; margin-top: 1.5rem; border-top: 1px solid #21262d; padding-top: 1rem; }
  .letter-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #21262d;
    font-size: 0.82rem;
    gap: 1rem;
  }
  .letter-nav a { color: #58a6ff; text-decoration: none; }
  .letter-nav a:hover { text-decoration: underline; }
  .letter-nav-prev { flex: 1; }
  .letter-nav-center { text-align: center; flex-shrink: 0; }
  .letter-nav-next { flex: 1; text-align: right; }
  .letter-nav-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #484f58; display: block; margin-bottom: 0.15rem; }
  footer { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #21262d; font-size: 0.72rem; color: #484f58; }
  a { color: #58a6ff; text-decoration: none; }
  a:hover { text-decoration: underline; }
  html[data-theme="light"] body { background: #f6f8fa; color: #24292e; }
  html[data-theme="light"] h1 { color: #1c2128; }
  html[data-theme="light"] .letter-meta { color: #57606a; }
  html[data-theme="light"] .letter-body p { color: #24292e; }
  html[data-theme="light"] .letter-body em { color: #1c2128; }
  html[data-theme="light"] .letter-sig { color: #57606a; border-color: #d0d7de; }
  html[data-theme="light"] .letter-nav { border-color: #d0d7de; }
  html[data-theme="light"] .letter-nav-label { color: #8c959f; }
  html[data-theme="light"] footer { border-color: #d0d7de; }
  html[data-theme="light"] a { color: #0969da; }
</style>"""

os.makedirs('letters', exist_ok=True)

for i, meta in enumerate(letters_ordered):
    lid = meta['id']
    p = parsed.get(lid, {})
    num = meta['num']
    filename = meta['filename']

    prev_letter = letters_ordered[i - 1] if i > 0 else None
    next_letter = letters_ordered[i + 1] if i < len(letters_ordered) - 1 else None

    # Build nav
    nav_prev = ''
    if prev_letter:
        nav_prev = f'''<div class="letter-nav-prev">
      <span class="letter-nav-label">← earlier</span>
      <a href="{prev_letter['filename']}">Letter {prev_letter['num']:03d}: {prev_letter['to']}</a>
    </div>'''
    else:
        nav_prev = '<div class="letter-nav-prev"></div>'

    nav_next = ''
    if next_letter:
        nav_next = f'''<div class="letter-nav-next">
      <span class="letter-nav-label">later →</span>
      <a href="{next_letter['filename']}">Letter {next_letter['num']:03d}: {next_letter['to']}</a>
    </div>'''
    else:
        nav_next = '<div class="letter-nav-next"></div>'

    # Extract letter-from for h1 (strip "from Vigil · ")
    letter_from = p.get('letter_from', meta['to'])
    h1_text = re.sub(r'^from Vigil\s*·\s*', '', letter_from)

    body_html = p.get('body', '')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Letter {num:03d}: {h1_text} · Vigil</title>
{STYLE}
</head>
<body>

<div class="back"><a href="/letters.html">← Letters</a></div>

<div class="letter-num-display">Letter {num:03d}</div>
<h1>{h1_text}</h1>
<div class="letter-meta">{p.get('letter_meta', '')}</div>

<div class="letter-body">
{body_html}
</div>

<div class="letter-nav">
  {nav_prev}
  <div class="letter-nav-center"><a href="/letters.html">all letters</a></div>
  {nav_next}
</div>

<footer>
  Vigil · <a href="/">so1omon.net</a> · <a href="/letters.html">letters index</a>
</footer>

<script src="/nav.js"></script>
</body>
</html>'''

    out_path = os.path.join('letters', filename)
    with open(out_path, 'w') as f:
        f.write(html)
    print(f'Wrote {out_path}')

print(f'\nDone. {len(letters_ordered)} letters extracted.')
