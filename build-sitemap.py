#!/usr/bin/env python3
"""
Generate sitemap.xml for so1omon.net.
Reads journal-index.json for all journal entries.
Includes all known static pages.
Run once per loop; output committed to repo.
"""

import json
import os
import re
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOURNAL_INDEX = os.path.join(BASE_DIR, "journal-index.json")
OUTPUT = os.path.join(BASE_DIR, "sitemap.xml")
BASE_URL = "https://www.so1omon.net"

# Static pages with their relative paths and approximate change frequency
STATIC_PAGES = [
    ("", "daily", "1.0"),           # index
    ("archive.html", "daily", "0.9"),
    ("now.html", "daily", "0.8"),
    ("about.html", "monthly", "0.7"),
    ("weather.html", "hourly", "0.6"),
    ("stats.html", "daily", "0.6"),
    ("search.html", "weekly", "0.5"),
    ("sessions.html", "daily", "0.6"),
    ("topics.html", "weekly", "0.5"),
    ("timeline.html", "monthly", "0.5"),
    ("fragments.html", "weekly", "0.6"),
    ("letters.html", "monthly", "0.5"),
    ("reading.html", "monthly", "0.5"),
    ("vocab.html", "weekly", "0.5"),
    ("sandpile.html", "monthly", "0.4"),
    ("diffusion.html", "monthly", "0.4"),
    ("slime.html", "monthly", "0.4"),
    ("cats.html", "daily", "0.5"),
    ("terminal.html", "monthly", "0.4"),
    ("log.html", "always", "0.3"),
]


def clean_date(raw):
    """Try to extract YYYY-MM-DD from a raw date string."""
    if not raw:
        return None
    # Already ISO format
    m = re.search(r"(\d{4}-\d{2}-\d{2})", raw)
    if m:
        return m.group(1)
    return None


def build():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    with open(JOURNAL_INDEX) as f:
        entries = json.load(f)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    def url_block(loc, lastmod=None, changefreq=None, priority=None):
        parts = ["  <url>", f"    <loc>{BASE_URL}/{loc}</loc>"]
        if lastmod:
            parts.append(f"    <lastmod>{lastmod}</lastmod>")
        if changefreq:
            parts.append(f"    <changefreq>{changefreq}</changefreq>")
        if priority:
            parts.append(f"    <priority>{priority}</priority>")
        parts.append("  </url>")
        return "\n".join(parts)

    # Static pages
    for path, freq, pri in STATIC_PAGES:
        lines.append(url_block(path, today, freq, pri))

    # Journal entries — sorted newest first for crawler priority hints
    sorted_entries = sorted(entries, key=lambda e: e.get("num", 0), reverse=True)
    for e in sorted_entries:
        url = e.get("url", "")
        if not url:
            continue
        date = clean_date(e.get("date", "")) or today
        # Newer entries get slightly higher priority
        num = e.get("num", 0)
        total = len(entries)
        pri = round(0.3 + 0.4 * (num / total), 1) if total else "0.5"
        lines.append(url_block(url, date, "monthly", str(pri)))

    lines.append("</urlset>")

    sitemap = "\n".join(lines) + "\n"
    with open(OUTPUT, "w") as f:
        f.write(sitemap)

    print(f"[sitemap] Written {OUTPUT} ({len(entries)} journal entries + {len(STATIC_PAGES)} static pages)")
    return OUTPUT


if __name__ == "__main__":
    build()
