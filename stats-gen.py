#!/usr/bin/env python3
"""Generate stats.json for the stats page.
Called by the loop before each Claude session, alongside weather.py."""

import json, os, re, subprocess, statistics
from datetime import datetime, timezone

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
JOURNAL_DIR = os.path.join(WORKING_DIR, 'journal')
JOURNAL_INDEX = os.path.join(WORKING_DIR, 'journal-index.json')
TOPICS_FILE = os.path.join(WORKING_DIR, 'topics.json')
STATS_OUT = os.path.join(WORKING_DIR, 'stats.json')

def count_words_html(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&[a-z#0-9]+;', ' ', text)
    return len(text.split())

def get_git_commit_count():
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD'],
            cwd=WORKING_DIR, capture_output=True, text=True, timeout=10
        )
        return int(result.stdout.strip())
    except Exception:
        return None

def get_topic_distribution():
    """Load topics.json and return per-category counts with labels/colors."""
    try:
        with open(TOPICS_FILE) as f:
            data = json.load(f)
        categories = {c['id']: c for c in data.get('categories', [])}
        by_cat = data.get('entries_by_category', {})
        total = sum(len(v) for v in by_cat.values())
        result = []
        for cat_id, entries in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            cat = categories.get(cat_id, {})
            count = len(entries)
            result.append({
                'id': cat_id,
                'label': cat.get('label', cat_id),
                'color': cat.get('color', '#58a6ff'),
                'count': count,
                'pct': round(100 * count / total) if total else 0,
            })
        return result
    except Exception:
        return []

def main():
    # Load journal index for titles and metadata
    try:
        with open(JOURNAL_INDEX) as f:
            index = json.load(f)
        index_by_num = {e['num']: e for e in index if 'num' in e}
    except Exception:
        index_by_num = {}

    # Journal word counts (paired with entry number)
    entry_data = []
    fnames = sorted(
        [f for f in os.listdir(JOURNAL_DIR) if f.endswith('.html')],
        key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0
    )
    for fname in fnames:
        m = re.search(r'\d+', fname)
        if not m:
            continue
        num = int(m.group())
        path = os.path.join(JOURNAL_DIR, fname)
        try:
            wc = count_words_html(path)
            title = index_by_num.get(num, {}).get('title', fname)
            entry_data.append({'num': num, 'title': title, 'words': wc})
        except Exception:
            pass

    word_counts = [e['words'] for e in entry_data]
    total_words = sum(word_counts)
    avg_words = total_words // len(word_counts) if word_counts else 0
    median_words = int(statistics.median(word_counts)) if word_counts else 0

    # Longest entries (top 5)
    longest = sorted(entry_data, key=lambda e: -e['words'])[:5]

    # Word length distribution
    dist = {
        'under_300': sum(1 for c in word_counts if c < 300),
        '300_600':   sum(1 for c in word_counts if 300 <= c < 600),
        '600_900':   sum(1 for c in word_counts if 600 <= c < 900),
        'over_900':  sum(1 for c in word_counts if c >= 900),
    }
    max_dist = max(dist.values()) if dist else 1

    # First entry date
    first_entry_date = '2026-03-05'

    # Git commits
    git_commits = get_git_commit_count()

    # Topic distribution
    topics = get_topic_distribution()

    stats = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'journal': {
            'entry_count': len(word_counts),
            'total_words': total_words,
            'avg_words': avg_words,
            'median_words': median_words,
            'first_entry_date': first_entry_date,
        },
        'system': {
            'git_commits': git_commits,
            'loop_interval_hours': 4,
        },
        'word_distribution': {
            'buckets': [
                {'label': '< 300w',   'count': dist['under_300'], 'pct': round(100 * dist['under_300'] / max_dist)},
                {'label': '300–600w', 'count': dist['300_600'],   'pct': round(100 * dist['300_600']   / max_dist)},
                {'label': '600–900w', 'count': dist['600_900'],   'pct': round(100 * dist['600_900']   / max_dist)},
                {'label': '900w+',    'count': dist['over_900'],  'pct': round(100 * dist['over_900']  / max_dist)},
            ]
        },
        'longest_entries': [
            {'num': e['num'], 'title': e['title'], 'words': e['words']}
            for e in longest
        ],
        'topics': topics,
    }

    with open(STATS_OUT, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"stats.json: {len(word_counts)} entries, {total_words:,} words, {git_commits} commits, {len(topics)} topics")

if __name__ == '__main__':
    main()
