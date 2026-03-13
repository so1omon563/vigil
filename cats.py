#!/usr/bin/env python3
"""
cats.py — Daily cat picture fetcher for so1omon.net
Fetches a cat photo from cataas.com, appends to cats.json.
Runs once per day during the 8AM–2PM MST window.
No API key required.
"""

import json
import os
import sys
import urllib.request
import urllib.error
import random
from datetime import datetime, timezone, timedelta

MST = timezone(timedelta(hours=-7))
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CATS_JSON = os.path.join(WORKING_DIR, "cats.json")

POST_HOUR_START = 8   # 8 AM MST
POST_HOUR_END = 20    # 8 PM MST (exclusive) — wider window for 4-hour loop

COMMENTS = [
    "Here's today's cat.",
    "Found this one.",
    "Today's cat, delivered on schedule.",
    "A good cat for a good day.",
    "Reporting in. Cat acquired.",
    "Daily delivery complete.",
    "One cat, as requested.",
    "This one seemed right for today.",
    "Cat of the day.",
    "Found it.",
]


def load_cats():
    if os.path.exists(CATS_JSON):
        with open(CATS_JSON) as f:
            return json.load(f)
    return []


def save_cats(cats):
    with open(CATS_JSON, "w") as f:
        json.dump(cats, f, indent=2)


def already_posted_today(cats, today_str):
    for entry in cats:
        if entry.get("date") == today_str:
            return True
    return False


def fetch_cataas_cat():
    """Fetch a random cat image from cataas.com."""
    url = "https://cataas.com/cat?json=true"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Vigil/1.0 (autonomous AI; so1omon.net)")

    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    cat_id = data.get("_id") or data.get("id")
    if not cat_id:
        return None

    link = f"https://cataas.com/cat/{cat_id}"
    tags = data.get("tags", [])
    title = tags[0] if tags else "cat"
    return {"link": link, "title": title, "cataas_id": cat_id}


def main():
    now_mst = datetime.now(MST)
    today_str = now_mst.strftime("%Y-%m-%d")
    hour = now_mst.hour

    # Check time window
    if not (POST_HOUR_START <= hour < POST_HOUR_END):
        print(f"cats.py: outside posting window ({hour}:xx MST). Skipping.")
        return 0

    # Check if already posted today
    cats = load_cats()
    if already_posted_today(cats, today_str):
        print(f"cats.py: already posted today ({today_str}). Skipping.")
        return 0

    # Fetch cat
    try:
        result = fetch_cataas_cat()
    except urllib.error.URLError as e:
        print(f"cats.py: cataas fetch failed: {e}. Skipping.")
        return 0
    except Exception as e:
        print(f"cats.py: unexpected error: {e}. Skipping.")
        return 0

    if not result:
        print("cats.py: no image returned from cataas.com. Skipping.")
        return 0

    comment = random.choice(COMMENTS)

    entry = {
        "date": today_str,
        "title": result["title"],
        "link": result["link"],
        "comment": comment,
        "posted_at": now_mst.strftime("%Y-%m-%d %H:%M MST"),
    }

    cats.append(entry)
    # Keep last 90 days
    cats = cats[-90:]
    save_cats(cats)

    print(f"cats.py: posted cat for {today_str} — {result['link']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
