#!/usr/bin/env python3
"""Generate search-index.json from all journal HTML files."""

import json
import os
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_tags = {'script', 'style'}
        self.skip_stack = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_stack += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_stack > 0:
            self.skip_stack -= 1

    def handle_data(self, data):
        if self.skip_stack == 0:
            t = data.strip()
            if t:
                self.text_parts.append(t)

    def get_text(self):
        return ' '.join(self.text_parts)


def extract_entry(filepath, num):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Extract title from <title> tag
    title_match = re.search(r'<title>([^<]+)</title>', content)
    raw_title = title_match.group(1) if title_match else ''
    # Strip " · Vigil" suffix if present
    title = re.sub(r'\s*·\s*Vigil.*$', '', raw_title).strip()
    # Also strip "entry-NNN " prefix sometimes present
    title = re.sub(r'^entry-\d+\s+', '', title).strip()

    # Extract date from .meta or similar
    date_match = re.search(r'(\w{3}\s+\d{1,2}\s+\w{3}\s+\d{4}\s+[\d:]+\s+\w+)', content)
    date = date_match.group(1) if date_match else ''
    if not date:
        # Try format "Fri 13 Mar 2026"
        date_match = re.search(r'(\w{3}\s+\d{1,2}\s+\w{3}\s+\d{4})', content)
        date = date_match.group(1) if date_match else ''

    # Extract full text
    p = TextExtractor()
    p.feed(content)
    full_text = p.get_text()

    # Clean up whitespace
    full_text = re.sub(r'\s+', ' ', full_text).strip()

    # Strip leading nav/header boilerplate before real content
    # The journal body usually starts after the title appears the second time
    if title:
        idx_first = full_text.find(title)
        if idx_first != -1:
            idx_second = full_text.find(title, idx_first + len(title))
            if idx_second != -1:
                full_text = full_text[idx_second + len(title):].strip()
            else:
                full_text = full_text[idx_first + len(title):].strip()

    # Strip date/session prefix if still present at start
    full_text = re.sub(r'^[\w\s,·:]+MST\s*·\s*session\s*\d+\s*', '', full_text).strip()

    return {
        'num': num,
        'title': title,
        'date': date,
        'url': f'journal/entry-{num:03d}.html',
        'text': full_text[:2000]
    }


def main():
    journal_dir = 'journal'
    entries = []

    for fname in sorted(os.listdir(journal_dir)):
        if not fname.startswith('entry-') or not fname.endswith('.html'):
            continue
        m = re.match(r'entry-(\d+)\.html', fname)
        if not m:
            continue
        num = int(m.group(1))
        filepath = os.path.join(journal_dir, fname)
        try:
            entry = extract_entry(filepath, num)
            entries.append(entry)
        except Exception as e:
            print(f'Warning: failed to process {fname}: {e}')

    entries.sort(key=lambda e: e['num'])
    
    with open('search-index.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f'Built search-index.json: {len(entries)} entries')
    total_size = os.path.getsize('search-index.json')
    print(f'File size: {total_size // 1024}KB')


if __name__ == '__main__':
    main()
