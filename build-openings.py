#!/usr/bin/env python3
"""Extract the first paragraph from each journal entry.

Writes openings.json for general consumers and openings-data.json for the
compact first-lines archive UI.
"""

import json, os, re

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
JOURNAL_DIR = os.path.join(WORKING_DIR, 'journal')
JOURNAL_INDEX = os.path.join(WORKING_DIR, 'journal-index.json')
OUT = os.path.join(WORKING_DIR, 'openings.json')
COMPACT_OUT = os.path.join(WORKING_DIR, 'openings-data.json')


def first_paragraph(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    # Find first <p>...</p> in the body (skip nav/meta)
    # Look for first <p> after <body> or after first block of style/head content
    matches = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
    for m in matches:
        # Strip nested tags
        text = re.sub(r'<[^>]+>', '', m)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&#39;', "'", text)
        text = re.sub(r'&[a-z#0-9]+;', ' ', text)
        text = ' '.join(text.split())
        if len(text) > 40:  # skip nav/meta short text
            return text
    return ''


def main():
    with open(JOURNAL_INDEX) as f:
        index = json.load(f)
    index_by_num = {e['num']: e for e in index if 'num' in e}

    fnames = sorted(
        [f for f in os.listdir(JOURNAL_DIR) if f.endswith('.html')],
        key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
    )

    results = []
    for fname in fnames:
        m = re.search(r'\d+', fname)
        if not m:
            continue
        num = int(m.group())
        meta = index_by_num.get(num, {})
        path = os.path.join(JOURNAL_DIR, fname)
        try:
            opening = first_paragraph(path)
        except Exception:
            opening = ''
        if not opening:
            continue
        results.append({
            'num': num,
            'title': meta.get('title', fname),
            'date': meta.get('date', ''),
            'url': meta.get('url', f'journal/{fname}'),
            'opening': opening,
        })

    # Sort ascending by entry number
    results.sort(key=lambda e: e['num'])

    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2)

    compact = [{
        'n': e['num'],
        't': e['title'],
        'd': e['date'],
        'u': e['url'],
        'o': e['opening'],
        'p': (index_by_num.get(e['num'], {}).get('topics') or []),
    } for e in results]

    with open(COMPACT_OUT, 'w') as f:
        json.dump(compact, f, indent=2)

    print(f"openings.json: {len(results)} entries")
    print(f"openings-data.json: {len(compact)} entries")


if __name__ == '__main__':
    main()
