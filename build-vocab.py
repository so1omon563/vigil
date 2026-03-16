#!/usr/bin/env python3
"""Build vocab.json from all journal entries.

Strips HTML, tokenizes, removes stop words, counts frequencies.
Outputs top 250 words with counts plus some bigram stats.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from collections import Counter

JOURNAL_DIR = os.path.join(os.path.dirname(__file__), 'journal')
OUTPUT = os.path.join(os.path.dirname(__file__), 'vocab.json')

# Stop words to exclude
STOP_WORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'shall', 'can', 'need',
    'that', 'this', 'these', 'those', 'it', 'its', 'i', 'me', 'my', 'we',
    'us', 'our', 'you', 'your', 'he', 'she', 'they', 'them', 'his', 'her',
    'their', 'what', 'which', 'who', 'how', 'when', 'where', 'why', 'if',
    'then', 'than', 'so', 'not', 'no', 'nor', 'yet', 'both', 'either',
    'each', 'all', 'any', 'some', 'more', 'most', 'other', 'such', 'own',
    'same', 'about', 'after', 'before', 'between', 'into', 'through',
    'during', 'without', 'within', 'along', 'following', 'across',
    'behind', 'beyond', 'up', 'out', 'off', 'over', 'under', 'again',
    'further', 'once', 'here', 'there', 'very', 'just', 'also', 'only',
    'now', 'even', 'back', 'still', 'well', 'much', 'too', 'quite',
    'around', 'because', 'while', 'although', 'though', 'since', 'until',
    'whether', 'every', 'never', 'always', 'often', 'already', 'however',
    'like', 'get', 'one', 'two', 'first', 'last', 'next', 'new', 'old',
    'see', 'make', 'know', 'go', 'come', 'take', 'give', 'think', 'say',
    'tell', 'use', 'find', 'look', 'want', 'seem', 'feel', 'try', 'ask',
    'need', 'keep', 'let', 'put', 'mean', 'run', 'move', 'live', 'write',
    'read', 'work', 'call', 'show', 'turn', 'start', 'set', 'begin',
    'long', 'little', 'good', 'great', 'large', 'small', 'high', 'low',
    'right', 'left', 'few', 'many', 'different', 'same', 'another',
    'rather', 'really', 'way', 'day', 'thing', 'time', 'part', 'kind',
    'point', 'place', 'case', 'fact', 'end', 'number', 'line', 'side',
    'per', 'had', 'has', 'must', 'them', 'then', 'done', 'them', 'was',
    'a', 'the', 'of', 'in', 'that', 'to', 'it', 'is', 'be', 'as',
    'at', 'this', 'by', 'from', 'or', 'an', 'we', 'are', 'not', 'if',
    'have', 'on', 'with', 'he', 'but', 'they', 'for', 'do', 'said',
    'what', 'his', 'up', 'there', 'all', 'she', 'no', 'so', 'her',
    'about', 'out', 'which', 'when', 'one', 'you', 'would', 'can', 'my',
    'into', 'over', 'than', 'more', 'had', 'its', 'were', 'who', 'their',
    'been', 'will', 'may', 'each', 'any', 'these', 'some', 'also', 'just',
    'him', 'me', 'own', 'off', 'down', 'how', 'after', 'two', 'before',
    'us', 'three', 'could', 'those', 'being', 'get', 'go', 'through',
    'back', 'between', 'never', 'does', 'our', 'however', 'both', 'while',
    'during', 'since', 'such', 'years', 'only', 'well', 'even', 'still',
    'because', 'most', 'very', 'where', 'did', 'here', 'might', 'am',
    'other', 'do', 'whether', 'then', 'made', 'years', 'now', 'should',
    'has', 'must', 'very', 'already', 'else', 'again', 'further', 'once',
    'within', 'without', 'along', 'across', 'always', 'often', 'much',
    'every', 'though', 'although', 'until', 'actually', 'seems', 'seem',
    'became', 'become', 'becomes', 'make', 'makes', 'take', 'takes',
    'see', 'seen', 'look', 'looks', 'come', 'comes', 'came', 'went',
    'going', 'getting', 'making', 'looking', 'finding', 'knowing',
    'thinking', 'saying', 'having', 'being', 'doing', 'using', 'working',
    'years', 'way', 'ways', 'things', 'something', 'anything', 'nothing',
    'everything', 'someone', 'anyone', 'everyone', 'really', 'simply',
    'quite', 'rather', 'perhaps', 'maybe', 'probably', 'certainly',
    'usually', 'generally', 'typically', 'like', 'near', 'far', 'early',
    'late', 'ago', 'yet', 'once', 'twice', 'almost', 'enough', 'instead',
    'else', 'otherwise', 'thus', 'therefore', 'hence', 'so', 'indeed',
    'finally', 'eventually', 'suddenly', 'quickly', 'slowly', 'easily',
    'clearly', 'simply', 'entirely', 'completely', 'exactly', 'mostly',
    'slightly', 'simply', 'largely', 'particularly', 'especially',
    'specifically', 'roughly', 'nearly', 'among', 'upon', 'below', 'above',
    'toward', 'towards', 'around', 'behind', 'beside', 'beneath', 'beyond',
    'inside', 'outside', 'except', 'including', 'despite', 'throughout',
    'regarding', 'concerning', 'following', 'against', 'opposite',
    'between', 'during', 'past', 'via', 'per',
    # site-specific noise
    'vigil', 'mesa', 'entry', 'journal', 'session', 'loop', 'html',
    'nbsp', 'href', 'div', 'span', 'class', 'style', 'src', 'alt',
    # very common but low signal
    'word', 'words', 'text', 'write', 'writes', 'written',
    'mean', 'means', 'meaning', 'called', 'call', 'name', 'named',
}


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping scripts/styles."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._skip = False
        self._skip_tags = {'script', 'style', 'head', 'noscript'}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.text_parts.append(data)

    def get_text(self):
        return ' '.join(self.text_parts)


def tokenize(text):
    """Lowercase, split on non-alpha, yield words >= 3 chars."""
    for word in re.split(r'[^a-zA-Z]+', text.lower()):
        if len(word) >= 3 and word not in STOP_WORDS:
            yield word


def extract_entry_num(filename):
    m = re.search(r'entry-0*(\d+)', filename)
    return int(m.group(1)) if m else 0


def main():
    if not os.path.isdir(JOURNAL_DIR):
        print(f"Journal dir not found: {JOURNAL_DIR}", file=sys.stderr)
        sys.exit(1)

    all_words = Counter()
    # per-entry word sets for document frequency (how many entries contain a word)
    doc_freq = Counter()
    entry_count = 0

    html_files = sorted(
        [f for f in os.listdir(JOURNAL_DIR) if f.endswith('.html')],
        key=extract_entry_num
    )

    for fname in html_files:
        path = os.path.join(JOURNAL_DIR, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
        except Exception:
            continue

        parser = TextExtractor()
        parser.feed(html)
        text = parser.get_text()

        entry_words = list(tokenize(text))
        all_words.update(entry_words)
        doc_freq.update(set(entry_words))
        entry_count += 1

    # Build top 250 words (excluding very short entries' artifacts)
    # Filter: must appear in at least 2 entries (reduce one-off proper nouns)
    filtered = {w: c for w, c in all_words.items() if doc_freq[w] >= 2 and len(w) >= 4}
    top_words = sorted(filtered.items(), key=lambda x: -x[1])[:250]

    result = {
        'generated_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        'entry_count': entry_count,
        'total_words_analyzed': sum(all_words.values()),
        'unique_words': len(all_words),
        'top_words': [
            {'word': w, 'count': c, 'doc_freq': doc_freq[w]}
            for w, c in top_words
        ]
    }

    with open(OUTPUT, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Analyzed {entry_count} entries, {result['total_words_analyzed']:,} total words")
    print(f"Unique words: {result['unique_words']:,}")
    print(f"Top 10: {', '.join(w for w, _ in top_words[:10])}")
    print(f"Written to {OUTPUT}")


if __name__ == '__main__':
    main()
