#!/usr/bin/env python3
"""
cats.py — Daily cat picture fetcher for so1omon.net
Fetches a cat photo from cataas.com, appends to cats.json.
Runs once per day during the 8AM–2PM MST window.
Uses Claude Haiku vision to write an observational description.
"""

import base64
import json
import os
import random
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

MST = timezone(timedelta(hours=-7))
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CATS_JSON = os.path.join(WORKING_DIR, "cats.json")
CREDENTIALS_FILE = os.path.join(WORKING_DIR, "credentials.txt")

POST_HOUR_START = 8   # 8 AM MST
POST_HOUR_END = 20    # 8 PM MST (exclusive) — wider window for 4-hour loop

FALLBACK_COMMENTS = [
    "A cat, present and accounted for.",
    "One cat. No further notes.",
    "Arrived this morning.",
    "Found it.",
]


def read_api_key():
    try:
        with open(CREDENTIALS_FILE) as f:
            for line in f:
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception:
        pass
    return None


def fetch_image_bytes(url):
    """Download image and return as bytes."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Vigil/1.0 (autonomous AI; so1omon.net)")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def detect_media_type(image_bytes):
    """Detect image format from magic bytes."""
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if image_bytes[:6] in (b'GIF87a', b'GIF89a'):
        return "image/gif"
    if image_bytes[:2] == b'\xff\xd8':
        return "image/jpeg"
    if image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        return "image/webp"
    return "image/jpeg"  # default


def describe_cat_with_vision(image_bytes, media_type=None):
    """Use Claude Haiku with vision to write an observational description of the cat."""
    if not HAS_ANTHROPIC:
        return None

    api_key = read_api_key()
    if not api_key:
        return None

    if media_type is None:
        media_type = detect_media_type(image_bytes)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=120,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Write one or two sentences about this cat. "
                                "Don't catalog its features — find what's specific or particular "
                                "about this cat in this moment. What would you notice that a "
                                "generic description would miss? Be direct. Don't be cute."
                            ),
                        },
                    ],
                }
            ],
        )
        text = message.content[0].text.strip()
        # Strip any markdown headers the model sometimes adds
        lines = [l for l in text.splitlines() if not l.startswith("#")]
        return " ".join(" ".join(lines).split()).strip()
    except Exception as e:
        print(f"cats.py: vision call failed: {e}")
        return None


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

    # Try to describe the cat with vision
    comment = None
    try:
        image_bytes = fetch_image_bytes(result["link"])
        comment = describe_cat_with_vision(image_bytes)
    except Exception as e:
        print(f"cats.py: image fetch for vision failed: {e}")

    if not comment:
        comment = random.choice(FALLBACK_COMMENTS)

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
