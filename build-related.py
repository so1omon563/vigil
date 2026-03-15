#!/usr/bin/env python3
"""Generate related.json — maps each entry number to up to 4 related entries.

Matching strategy:
  1. Primary: same category from topics.json, sorted by distance, pick up to 4.
  2. Fallback: nearest neighbors by entry number (2 above, 2 below).
"""

import json, os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
TOPICS_FILE = os.path.join(WORKING_DIR, 'topics.json')
JOURNAL_INDEX = os.path.join(WORKING_DIR, 'journal-index.json')
OUT_FILE = os.path.join(WORKING_DIR, 'related.json')

def main():
    with open(TOPICS_FILE) as f:
        topics_data = json.load(f)
    with open(JOURNAL_INDEX) as f:
        index = json.load(f)

    # Build lookup: entry num -> {title, url}
    meta = {}
    all_nums = set()
    for e in index:
        if 'num' in e:
            meta[e['num']] = {'num': e['num'], 'title': e.get('title', f"Entry {e['num']}"), 'url': e.get('url', f"journal/entry-{e['num']:03d}.html")}
            all_nums.add(e['num'])

    # Build: entry num -> list of nums in same category
    entry_to_cat = {}  # num -> category_id
    cat_to_entries = {}  # category_id -> sorted list of nums
    for cat_id, entries in topics_data.get('entries_by_category', {}).items():
        nums = [e['num'] for e in entries if 'num' in e]
        cat_to_entries[cat_id] = sorted(nums)
        for n in nums:
            entry_to_cat[n] = cat_id

    all_sorted = sorted(all_nums)
    related = {}

    for num in all_sorted:
        if num not in meta:
            continue

        cat = entry_to_cat.get(num)
        candidates = []

        if cat:
            # Same category, excluding self, sorted by distance, pick closest 4
            same_cat = [n for n in cat_to_entries.get(cat, []) if n != num]
            same_cat.sort(key=lambda n: abs(n - num))
            candidates = sorted(same_cat[:4], reverse=True)

        # Fallback if we have fewer than 2 candidates: add nearest neighbors
        if len(candidates) < 2:
            idx = all_sorted.index(num)
            neighbors = []
            # Up to 2 above (lower numbered = earlier)
            if idx > 0:
                neighbors.append(all_sorted[idx - 1])
            if idx > 1:
                neighbors.append(all_sorted[idx - 2])
            # Up to 2 below (higher numbered = later)
            if idx < len(all_sorted) - 1:
                neighbors.append(all_sorted[idx + 1])
            if idx < len(all_sorted) - 2:
                neighbors.append(all_sorted[idx + 2])
            for n in neighbors:
                if n not in candidates and len(candidates) < 4:
                    candidates.append(n)
            candidates = sorted(candidates, reverse=True)

        related[str(num)] = [meta[n] for n in candidates if n in meta]

    with open(OUT_FILE, 'w') as f:
        json.dump(related, f, separators=(',', ':'))

    print(f"related.json: {len(related)} entries mapped")

if __name__ == '__main__':
    main()
