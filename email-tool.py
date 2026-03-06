#!/usr/bin/env python3
"""
Email tool for autonomous AI loop.
Checks Gmail IMAP for unread messages and can send SMTP replies.

Usage:
  python3 email-tool.py check          # Print unread emails as JSON
  python3 email-tool.py sent [N]       # Print last N sent emails (default 20)
  python3 email-tool.py send TO SUBJECT BODY  # Send an email
  python3 email-tool.py mark-read ID   # Mark email ID as read
"""

import imaplib
import smtplib
import email as emaillib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import sys
import json
import ssl
import os

def _load_credentials():
    creds = {}
    cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.txt")
    if os.path.exists(cred_path):
        with open(cred_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, val = line.partition("=")
                    creds[key.strip()] = val.strip()
    return creds

_creds = _load_credentials()

EMAIL_ADDR = _creds["EMAIL"]
EMAIL_PASS = _creds["EMAIL_PASSWORD"]
IMAP_HOST = _creds.get("IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(_creds.get("IMAP_PORT", 993))
SMTP_HOST = _creds.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(_creds.get("SMTP_PORT", 587))


def decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return " ".join(result)


def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in cd:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body = payload.decode(charset, errors="replace")
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="replace")
    return body.strip()


def imap_connect():
    ctx = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=ctx)
    imap.login(EMAIL_ADDR, EMAIL_PASS)
    return imap


def check_headers():
    """Lightweight: return list of unread email header dicts (no body). Fast polling."""
    imap = imap_connect()
    imap.select("INBOX")
    status, data = imap.search(None, "UNSEEN")
    ids = data[0].split() if data[0] else []

    emails = []
    for eid in ids:
        status, msg_data = imap.fetch(eid, "(RFC822.HEADER)")
        if msg_data[0] is None:
            continue
        msg = emaillib.message_from_bytes(msg_data[0][1])
        emails.append({
            "id": eid.decode(),
            "from": decode_str(msg.get("From", "")),
            "reply_to": decode_str(msg.get("Reply-To", msg.get("From", ""))),
            "subject": decode_str(msg.get("Subject", "(no subject)")),
            "date": msg.get("Date", ""),
            "message_id": msg.get("Message-ID", ""),
            "in_reply_to": msg.get("In-Reply-To", ""),
            "body": "",
        })
    imap.logout()
    return emails


def fetch_full(email_id):
    """Fetch full email (with body) for a single message ID string."""
    imap = imap_connect()
    imap.select("INBOX")
    status, msg_data = imap.fetch(email_id.encode(), "(RFC822)")
    imap.logout()
    if not msg_data or msg_data[0] is None:
        return None
    msg = emaillib.message_from_bytes(msg_data[0][1])
    return {
        "id": email_id,
        "from": decode_str(msg.get("From", "")),
        "reply_to": decode_str(msg.get("Reply-To", msg.get("From", ""))),
        "subject": decode_str(msg.get("Subject", "(no subject)")),
        "date": msg.get("Date", ""),
        "message_id": msg.get("Message-ID", ""),
        "in_reply_to": msg.get("In-Reply-To", ""),
        "body": get_body(msg)[:3000],
    }


def check_unread():
    imap = imap_connect()
    imap.select("INBOX")
    status, data = imap.search(None, "UNSEEN")
    ids = data[0].split() if data[0] else []

    emails = []
    for eid in ids:
        status, msg_data = imap.fetch(eid, "(RFC822)")
        if msg_data[0] is None:
            continue
        msg = emaillib.message_from_bytes(msg_data[0][1])
        emails.append({
            "id": eid.decode(),
            "from": decode_str(msg.get("From", "")),
            "reply_to": decode_str(msg.get("Reply-To", msg.get("From", ""))),
            "subject": decode_str(msg.get("Subject", "(no subject)")),
            "date": msg.get("Date", ""),
            "message_id": msg.get("Message-ID", ""),
            "in_reply_to": msg.get("In-Reply-To", ""),
            "body": get_body(msg)[:3000],
        })
    imap.logout()
    return emails


def get_sent(limit=20):
    imap = imap_connect()
    # Gmail sent folder
    imap.select('"[Gmail]/Sent Mail"')
    status, data = imap.search(None, "ALL")
    ids = data[0].split() if data[0] else []
    recent = ids[-limit:] if len(ids) > limit else ids

    emails = []
    for eid in reversed(recent):
        status, msg_data = imap.fetch(eid, "(RFC822)")
        if msg_data[0] is None:
            continue
        msg = emaillib.message_from_bytes(msg_data[0][1])
        emails.append({
            "id": eid.decode(),
            "to": decode_str(msg.get("To", "")),
            "subject": decode_str(msg.get("Subject", "(no subject)")),
            "date": msg.get("Date", ""),
        })
    imap.logout()
    return emails


def mark_read(email_id):
    imap = imap_connect()
    imap.select("INBOX")
    imap.store(email_id, "+FLAGS", "\\Seen")
    imap.logout()


def send_email(to_addr, subject, body, reply_to_msg_id=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDR
    msg["To"] = to_addr
    if reply_to_msg_id:
        msg["In-Reply-To"] = reply_to_msg_id
        msg["References"] = reply_to_msg_id

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDR, EMAIL_PASS)
        smtp.send_message(msg)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"

    if cmd == "check-headers":
        emails = check_headers()
        print(json.dumps(emails, indent=2, ensure_ascii=False))

    elif cmd == "fetch-full":
        email_id = sys.argv[2]
        em = fetch_full(email_id)
        print(json.dumps(em, indent=2, ensure_ascii=False))

    elif cmd == "check":
        emails = check_unread()
        print(json.dumps(emails, indent=2, ensure_ascii=False))

    elif cmd == "sent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        sent = get_sent(limit)
        print(json.dumps(sent, indent=2, ensure_ascii=False))

    elif cmd == "send":
        to = sys.argv[2]
        subject = sys.argv[3]
        body = sys.argv[4]
        reply_id = sys.argv[5] if len(sys.argv) > 5 else None
        send_email(to, subject, body, reply_id)
        print(f"Sent to {to}")

    elif cmd == "mark-read":
        mark_read(sys.argv[2])
        print(f"Marked {sys.argv[2]} as read")

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
