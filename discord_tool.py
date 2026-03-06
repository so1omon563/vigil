#!/usr/bin/env python3
"""
Discord tool for Vigil.
Sends messages to a configured channel via the Discord REST API.

Usage:
  python3 discord_tool.py send "message text"
  python3 discord_tool.py check          # fetch recent messages from channel

Credentials are read from credentials.txt (DISCORD_TOKEN, DISCORD_CHANNEL_ID).
The DISCORD_CHANNEL_ID may be a full URL or a bare channel ID.
"""

import json
import sys
import os
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.txt")
DISCORD_API = "https://discord.com/api/v10"


def load_credentials():
    creds = {}
    with open(CREDENTIALS_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                creds[key.strip()] = val.strip()
    return creds


def extract_channel_id(raw):
    """Accept either a bare ID or a full discord.com URL."""
    raw = raw.strip().rstrip("/")
    if raw.startswith("https://") or raw.startswith("http://"):
        # URL format: https://discord.com/channels/GUILD_ID/CHANNEL_ID
        return raw.split("/")[-1]
    return raw


def api_request(method, path, token, body=None):
    url = f"{DISCORD_API}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "Vigil/1.0 (so1omon.net)",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e


def send_message(content):
    creds = load_credentials()
    token = creds.get("DISCORD_TOKEN", "")
    channel_raw = creds.get("DISCORD_CHANNEL_ID", "")
    if not token or not channel_raw:
        print("ERROR: DISCORD_TOKEN or DISCORD_CHANNEL_ID missing from credentials.txt")
        sys.exit(1)
    channel_id = extract_channel_id(channel_raw)
    result = api_request("POST", f"/channels/{channel_id}/messages", token, {"content": content})
    print(f"Sent message ID {result['id']}: {content[:80]}")
    return result


def fetch_messages(limit=10):
    creds = load_credentials()
    token = creds.get("DISCORD_TOKEN", "")
    channel_raw = creds.get("DISCORD_CHANNEL_ID", "")
    if not token or not channel_raw:
        print("ERROR: DISCORD_TOKEN or DISCORD_CHANNEL_ID missing from credentials.txt")
        sys.exit(1)
    channel_id = extract_channel_id(channel_raw)
    messages = api_request("GET", f"/channels/{channel_id}/messages?limit={limit}", token)
    for m in reversed(messages):
        author = m.get("author", {}).get("username", "?")
        print(f"[{m['timestamp'][:16]}] {author}: {m['content']}")
    return messages


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: discord_tool.py send <message> | check")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "send":
        if len(sys.argv) < 3:
            print("Usage: discord_tool.py send <message>")
            sys.exit(1)
        send_message(" ".join(sys.argv[2:]))
    elif cmd == "check":
        fetch_messages()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
