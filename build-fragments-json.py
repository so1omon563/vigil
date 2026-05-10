#!/usr/bin/env python3
"""
build-fragments-json.py
Parses fragments.html and exports fragments-recent.json (latest 20 fragments).
Run this after adding new fragments.
"""

import json
import re

def parse_fragments(html):
    fragments = []
    # Match each fragment block
    pattern = re.compile(
        r'<div class="fragment">\s*'
        r'<div class="frag-num">Fragment\s+(\d+)\s*·\s*([\d-]+)</div>\s*'
        r'(?:<div class="frag-title">(.*?)</div>\s*)?'
        r'<div class="frag-body">\s*(.*?)\s*</div>\s*</div>',
        re.DOTALL
    )
    for m in pattern.finditer(html):
        num = int(m.group(1))
        date = m.group(2).strip()
        title = m.group(3).strip() if m.group(3) else ''
        body_html = m.group(4).strip()

        # Extract plain text from first paragraph
        first_p = re.search(r'<p>(.*?)</p>', body_html, re.DOTALL)
        excerpt = ''
        if first_p:
            excerpt = re.sub(r'<[^>]+>', '', first_p.group(1)).strip()
            if len(excerpt) > 180:
                excerpt = excerpt[:177] + '…'

        # Extract see-also link
        see_also_m = re.search(r'frag-see-also.*?href="([^"]+)">(.*?)</a>', body_html, re.DOTALL)
        see_also_url = see_also_m.group(1) if see_also_m else ''
        see_also_label = re.sub(r'<[^>]+>', '', see_also_m.group(2)).strip() if see_also_m else ''

        fragments.append({
            'num': num,
            'date': date,
            'title': title,
            'excerpt': excerpt,
            'see_also_url': see_also_url,
            'see_also_label': see_also_label,
        })

    # Sort newest first
    fragments.sort(key=lambda f: f['num'], reverse=True)
    return fragments

with open('fragments.html', 'r') as f:
    html = f.read()

fragments = parse_fragments(html)
total = len(fragments)
recent = fragments[:20]

with open('fragments-recent.json', 'w') as f:
    json.dump(recent, f, indent=2)

print(f"Parsed {total} fragments, wrote {len(recent)} to fragments-recent.json")
