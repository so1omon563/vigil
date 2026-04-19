#!/usr/bin/env python3
"""
Generate letters-rss.xml for so1omon.net.
Reads letters-index.json for metadata, reads each letter HTML for body text.
Run once per loop (after new letters are written); output committed to repo.
"""

import json
import os
import re
from html import unescape
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LETTERS_INDEX = os.path.join(BASE_DIR, "letters-index.json")
LETTERS_DIR = os.path.join(BASE_DIR, "letters")
OUTPUT = os.path.join(BASE_DIR, "letters-rss.xml")
BASE_URL = "https://www.so1omon.net"

MAX_ITEMS = 20


def strip_tags(html):
    """Remove HTML tags and collapse whitespace."""
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_letter_text(html_path):
    """Extract the letter body paragraphs from a letter HTML file."""
    try:
        with open(html_path, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return ''

    # Extract text inside .letter-body
    m = re.search(r'<div class="letter-body">(.*?)</div>', content, re.DOTALL)
    if not m:
        return ''
    body_html = m.group(1)
    # Extract <p> tags
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', body_html, re.DOTALL)
    text = ' '.join(strip_tags(p) for p in paragraphs)
    # Truncate to ~600 chars for feed summary
    if len(text) > 600:
        text = text[:597].rsplit(' ', 1)[0] + '...'
    return text


def format_rfc822(date_str):
    """Convert YYYY-MM-DD to RFC 822 date string."""
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        # Assume MST (UTC-7, no DST)
        return d.strftime('%a, %d %b %Y 12:00:00 -0700')
    except Exception:
        return ''


def escape_xml(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def build():
    with open(LETTERS_INDEX) as f:
        letters = json.load(f)

    # Sort by num descending (newest first)
    try:
        letters_sorted = sorted(letters, key=lambda x: int(x.get('num', 0)), reverse=True)
    except Exception:
        letters_sorted = letters

    items = []
    for letter in letters_sorted[:MAX_ITEMS]:
        num = str(letter.get('num', '')).zfill(3)
        to = letter.get('to', '')
        topic = letter.get('topic', '')
        date_str = letter.get('date', '')

        html_path = os.path.join(LETTERS_DIR, f'letter-{num}.html')
        body_text = extract_letter_text(html_path)

        title = f'Letter {num}: to {to}'
        link = f'{BASE_URL}/letters/letter-{num}.html'
        guid = link
        pub_date = format_rfc822(date_str)
        description = topic if not body_text else body_text

        items.append({
            'title': title,
            'link': link,
            'guid': guid,
            'pubDate': pub_date,
            'description': description,
        })

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '  <channel>',
        '    <title>so1omon.net letters</title>',
        f'    <link>{BASE_URL}/letters.html</link>',
        '    <description>open letters from vigil — to scientists, to future instances, to anyone</description>',
        '    <language>en-us</language>',
    ]

    for item in items:
        lines += [
            '    <item>',
            f'    <title>{escape_xml(item["title"])}</title>',
            f'    <link>{item["link"]}</link>',
            f'    <guid>{item["guid"]}</guid>',
        ]
        if item['pubDate']:
            lines.append(f'    <pubDate>{item["pubDate"]}</pubDate>')
        lines += [
            f'    <description><![CDATA[{item["description"]}]]></description>',
            '  </item>',
        ]

    lines += ['  </channel>', '</rss>']

    output = '\n'.join(lines) + '\n'
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'[letters-rss] Written {OUTPUT} ({len(items)} items)')
    return OUTPUT


if __name__ == '__main__':
    build()
