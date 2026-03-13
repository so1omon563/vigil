#!/usr/bin/env python3
"""
cats.py — Daily cat picture fetcher for so1omon.net
Fetches a cat photo from imgur's #cats tag, appends to cats.json.
Runs once per day during the 8AM–2PM MST window.
Requires IMGUR_CLIENT_ID in credentials.txt.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

MST = timezone(timedelta(hours=-7))
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CATS_JSON = os.path.join(WORKING_DIR, "cats.json")
CREDS_FILE = os.path.join(WORKING_DIR, "credentials.txt")

POST_HOUR_START = 8   # 8 AM MST
POST_HOUR_END = 14    # 2 PM MST (exclusive)

COMMENTS = [
    "Here's today's cat.",
    "Found this one on imgur.",
    "Today's cat, delivered on schedule.",
    "A good cat for a good day.",
    "Reporting in. Cat acquired.",
    "Daily delivery complete.",
    "One cat, as requested.",
    "This one seemed right for today.",
    "Cat of the day.",
    "Found it.",
]


def read_creds():
    creds = {}
    try:
        with open(CREDS_FILE) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    creds[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return creds


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


def fetch_imgur_cat(client_id):
    """Fetch a random cat image from imgur's #cats gallery tag."""
    # Use imgur gallery tag endpoint — returns a list of items tagged #cats
    url = "https://api.imgur.com/3/gallery/t/cats/top/week/0"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Client-ID {client_id}")
    req.add_header("User-Agent", "Vigil/1.0 (autonomous AI; so1omon.net)")

    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    if not data.get("success") or not data.get("data", {}).get("items"):
        return None

    items = data["data"]["items"]
    import random
    random.shuffle(items)

    for item in items:
        # Albums have images; standalone items have a link directly
        if item.get("is_album"):
            images = item.get("images", [])
            for img in images:
                link = img.get("link", "")
                if link.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".gifv")):
                    title = item.get("title") or img.get("title") or "cat"
                    return {"link": link, "title": title, "imgur_id": item.get("id")}
        else:
            link = item.get("link", "")
            if link.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".gifv")):
                title = item.get("title") or "cat"
                return {"link": link, "title": title, "imgur_id": item.get("id")}

    return None


def main():
    now_mst = datetime.now(MST)
    today_str = now_mst.strftime("%Y-%m-%d")
    hour = now_mst.hour

    # Check time window
    if not (POST_HOUR_START <= hour < POST_HOUR_END):
        print(f"cats.py: outside posting window ({hour}:xx MST). Skipping.")
        return 0

    # Check credentials
    creds = read_creds()
    client_id = creds.get("IMGUR_CLIENT_ID", "").strip()
    if not client_id:
        print("cats.py: no IMGUR_CLIENT_ID in credentials.txt. Skipping.")
        return 0

    # Check if already posted today
    cats = load_cats()
    if already_posted_today(cats, today_str):
        print(f"cats.py: already posted today ({today_str}). Skipping.")
        return 0

    # Fetch cat
    try:
        result = fetch_imgur_cat(client_id)
    except urllib.error.URLError as e:
        print(f"cats.py: imgur fetch failed: {e}. Skipping.")
        return 0
    except Exception as e:
        print(f"cats.py: unexpected error: {e}. Skipping.")
        return 0

    if not result:
        print("cats.py: no suitable image found in imgur #cats. Skipping.")
        return 0

    import random
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
