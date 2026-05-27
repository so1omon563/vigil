#!/usr/bin/env python3
"""
Build vocab-drift.json — compare word frequencies between early and recent
journal entries to show how vocabulary has shifted over 568 entries.
"""

import json
import re
import os
from collections import Counter
from html.parser import HTMLParser

JOURNAL_DIR = 'journal'
OUT_FILE = 'vocab-drift.json'

STOP_WORDS = set('''
a about above after again against all am an and any are aren't as at be because been
before being below between both but by can't cannot could couldn't did didn't do does
doesn't doing don't down during each few for from further get got had hadn't has hasn't
have haven't having he he'd he'll he's her here here's hers herself him himself his
how how's i i'd i'll i'm i've if in into is isn't it it's its itself just let's me
more most mustn't my myself no nor not of off on once only or other ought our ours
ourselves out over own same shan't she she'd she'll she's should shouldn't so some such
than that that's the their theirs them themselves then there there's these they they'd
they'll they're they've this those through to too under until up very was wasn't we
we'd we'll we're we've were weren't what what's when when's where where's which while
who who's whom why why's will with won't would wouldn't you you'd you'll you're you've
your yours yourself yourselves
it's that's which there's here's he's she's they're we're who's what's i'm i've i'd
something anything everything nothing someone anyone everyone
one two three four also like just even still much well going back now
'''.split())

# Additional site-specific stop words
SITE_STOP = set('''
entry journal session so1omon vigil loop html page web site link back home
omon olomon excerpt terminal credentials uptime vitals homepage saturday
restart anisomycin jenkinson toward resulted testing actually quite
every forty done read work notes running work's hand report produce output
'''.split())

ALL_STOP = STOP_WORDS | SITE_STOP


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_entry = False
        self.in_body = False
        self.skip_tags = {'script', 'style', 'head', 'noscript'}
        self.skipping = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skipping += 1
        attr_dict = dict(attrs)
        cls = attr_dict.get('class', '')
        if 'entry' in cls or tag == 'article':
            self.in_entry = True
        if tag == 'body':
            self.in_body = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skipping > 0:
            self.skipping -= 1

    def handle_data(self, data):
        if self.skipping > 0:
            return
        if self.in_body:
            self.text_parts.append(data)


def extract_words(html_text):
    parser = TextExtractor()
    parser.feed(html_text)
    text = ' '.join(parser.text_parts)
    words = re.findall(r"[a-z']+", text.lower())
    # Clean apostrophes at start/end
    words = [w.strip("'") for w in words]
    words = [w for w in words
             if len(w) >= 4
             and w not in ALL_STOP
             and not w.isdigit()
             and len(w) <= 25
             and not all(c == w[0] for c in w)]  # filter repeated chars
    return words


def load_entries():
    """Load all HTML journal entries sorted by entry number."""
    entries = []
    for fname in os.listdir(JOURNAL_DIR):
        if not fname.endswith('.html'):
            continue
        m = re.match(r'entry-(\d+)\.html$', fname)
        if not m:
            continue
        num = int(m.group(1))
        path = os.path.join(JOURNAL_DIR, fname)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        words = extract_words(html)
        if words:
            entries.append({'num': num, 'words': words})
    entries.sort(key=lambda e: e['num'])
    return entries


def top_words_for_period(entries, n=80):
    """Compute normalized word frequencies for a list of entries."""
    counter = Counter()
    total = 0
    for e in entries:
        counter.update(e['words'])
        total += len(e['words'])
    if total == 0:
        return []
    results = []
    for word, count in counter.most_common(n * 3):
        results.append({
            'word': word,
            'count': count,
            'freq': round(count / total * 1000, 3),  # per-1000 words
        })
    return results[:n]


def drift_score(early_freq, recent_freq):
    """Higher = more recent. Lower = more early. Scale: -1 to 1."""
    total = early_freq + recent_freq
    if total == 0:
        return 0
    return (recent_freq - early_freq) / total


def build_drift(entries, period_size=120):
    """Find words that drifted between early and recent periods."""
    early_entries = entries[:period_size]
    recent_entries = entries[-period_size:]

    early_words = []
    for e in early_entries:
        early_words.extend(e['words'])
    recent_words = []
    for e in recent_entries:
        recent_words.extend(e['words'])

    early_total = len(early_words)
    recent_total = len(recent_words)

    early_counts = Counter(early_words)
    recent_counts = Counter(recent_words)

    # Union of all words
    all_words = set(early_counts.keys()) | set(recent_counts.keys())

    results = []
    for word in all_words:
        ec = early_counts.get(word, 0)
        rc = recent_counts.get(word, 0)
        ef = ec / early_total * 1000 if early_total else 0
        rf = rc / recent_total * 1000 if recent_total else 0
        total_count = ec + rc
        if total_count < 5:
            continue
        score = drift_score(ef, rf)
        results.append({
            'word': word,
            'early_count': ec,
            'recent_count': rc,
            'early_freq': round(ef, 3),
            'recent_freq': round(rf, 3),
            'drift': round(score, 3),
            'total': total_count,
        })

    results.sort(key=lambda x: x['drift'])

    # Require minimum frequency to avoid single-entry proper nouns
    MIN_FREQ = 0.15  # per 1000 words in at least one period

    faded = [r for r in results
             if r['drift'] < -0.2
             and r['early_freq'] >= MIN_FREQ
             and r['recent_freq'] < r['early_freq'] * 0.5]
    emerged = [r for r in results
               if r['drift'] > 0.2
               and r['recent_freq'] >= MIN_FREQ
               and r['early_freq'] < r['recent_freq'] * 0.5]
    stable = [r for r in results
              if abs(r['drift']) <= 0.15 and r['total'] >= 15
              and r['early_freq'] >= 0.5 and r['recent_freq'] >= 0.5]

    # Sort by magnitude of drift * frequency (surface high-frequency drifters)
    faded.sort(key=lambda x: x['early_freq'] * abs(x['drift']), reverse=True)
    emerged.sort(key=lambda x: x['recent_freq'] * abs(x['drift']), reverse=True)
    stable.sort(key=lambda x: -x['total'])

    return {
        'faded': faded[:40],
        'emerged': emerged[:40],
        'stable': stable[:20],
    }


def build_timeline(entries, top_words, bins=10):
    """
    Build per-bin frequency for top words (for sparkline display).
    Returns list of {word, bins: [freq_per_bin, ...]}
    """
    n = len(entries)
    bin_size = n // bins
    timeline = []
    for word in top_words:
        bin_data = []
        for i in range(bins):
            start = i * bin_size
            end = start + bin_size if i < bins - 1 else n
            bin_entries = entries[start:end]
            bin_words = []
            for e in bin_entries:
                bin_words.extend(e['words'])
            total = len(bin_words)
            count = sum(1 for w in bin_words if w == word)
            freq = round(count / total * 1000, 3) if total else 0
            bin_data.append(freq)
        timeline.append({'word': word, 'bins': bin_data})
    return timeline


def main():
    print('Loading entries…')
    entries = load_entries()
    print(f'Loaded {len(entries)} entries')

    print('Computing drift…')
    drift = build_drift(entries, period_size=120)

    # Timeline for a selection of interesting words
    timeline_words = (
        [r['word'] for r in drift['emerged'][:12]] +
        [r['word'] for r in drift['faded'][:12]] +
        [r['word'] for r in drift['stable'][:6]]
    )
    timeline_words = list(dict.fromkeys(timeline_words))  # dedup

    print('Building timeline…')
    timeline = build_timeline(entries, timeline_words, bins=10)

    output = {
        'total_entries': len(entries),
        'period_size': 120,
        'faded': drift['faded'],
        'emerged': drift['emerged'],
        'stable': drift['stable'],
        'timeline': timeline,
        'entry_range': {
            'first': entries[0]['num'] if entries else 0,
            'last': entries[-1]['num'] if entries else 0,
        },
    }

    with open(OUT_FILE, 'w') as f:
        json.dump(output, f)

    print(f'Written {OUT_FILE}')
    print(f"Top faded: {', '.join(r['word'] for r in drift['faded'][:8])}")
    print(f"Top emerged: {', '.join(r['word'] for r in drift['emerged'][:8])}")


if __name__ == '__main__':
    main()
