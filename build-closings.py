#!/usr/bin/env python3
"""
build-closings.py — extract the closing (last substantive paragraph) from each journal entry.
Outputs closings.json parallel to openings.json.
"""

import json
import re
import os
from html.parser import HTMLParser


class ParagraphExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.skip = False
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer'}
        self.skip_depth = 0
        self.paragraphs = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
            self.skip_depth += 1
        if not self.skip and tag == 'p':
            self.in_p = True
            self.current = []

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth -= 1
            if self.skip_depth <= 0:
                self.skip = False
                self.skip_depth = 0
        if tag == 'p' and self.in_p:
            text = ''.join(self.current).strip()
            # Only keep substantive paragraphs (not "← entry-N" nav text etc.)
            if len(text) > 60:
                self.paragraphs.append(text)
            self.in_p = False
            self.current = []

    def handle_data(self, data):
        if self.in_p and not self.skip:
            self.current.append(data)


def extract_closing(filepath):
    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        extractor = ParagraphExtractor()
        extractor.feed(content)
        if extractor.paragraphs:
            return extractor.paragraphs[-1]
        return None
    except Exception as e:
        return None


def main():
    with open('journal-index.json') as f:
        index = json.load(f)

    closings = []
    missing = []

    for entry in index:
        num = entry.get('num') or entry.get('number') or entry.get('id')
        url = entry.get('url') or entry.get('file', '')
        title = entry.get('title', '')
        date = entry.get('date', '')

        # Build file path from URL
        filepath = url.lstrip('/')
        if not os.path.exists(filepath):
            missing.append(num)
            continue

        closing = extract_closing(filepath)
        if closing:
            closings.append({
                'num': num,
                'title': title,
                'date': date,
                'url': url,
                'closing': closing,
            })
        else:
            missing.append(num)

    # Sort descending by num (newest first, matching journal-index.json convention)
    closings.sort(key=lambda x: x['num'], reverse=True)

    with open('closings.json', 'w') as f:
        json.dump(closings, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(closings)} closings to closings.json")
    if missing:
        print(f"Missing/skipped entries: {missing}")


if __name__ == '__main__':
    main()
