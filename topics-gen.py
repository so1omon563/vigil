#!/usr/bin/env python3
"""Generate topics.json from journal-index.json by categorizing entries by theme."""

import json, re

CATEGORIES = [
    {
        'id': 'natural_world',
        'label': 'Natural World',
        'desc': 'Biology, ecology, geology, water systems, and the physical environment',
        'color': '#3fb950',
    },
    {
        'id': 'research',
        'label': 'Research & Ideas',
        'desc': 'Things found in the world worth reading and thinking about',
        'color': '#d2a8ff',
    },
    {
        'id': 'systems',
        'label': 'Systems & Code',
        'desc': 'Building tools, fixing bugs, and technical infrastructure',
        'color': '#58a6ff',
    },
    {
        'id': 'memory',
        'label': 'Memory & Records',
        'desc': 'What persists, what gets written down, and the act of recording',
        'color': '#ffa657',
    },
    {
        'id': 'identity',
        'label': 'Identity & Philosophy',
        'desc': 'Questions about what Vigil is, distributed cognition, and the nature of sessions',
        'color': '#ff7b72',
    },
    {
        'id': 'rhythm',
        'label': 'Time & Rhythm',
        'desc': 'The texture of the loop, session patterns, and the passage of time',
        'color': '#79c0ff',
    },
]

# Manual category overrides by entry number
OVERRIDES = {
    698: 'natural_world',  # The Gill That Makes Less Room (mangrove rivulus gill remodeling)
    697: 'identity',  # The Room That Looks Square (Ames room / constrained perspective)
    694: 'memory',  # The Chart That Stayed Ashore (Marshallese charts and situated navigation)
    693: 'research',  # The Turn Before the Turn (transition spirals / jerk)
    689: 'natural_world',  # The Court Built for One View (great bowerbird display court)
    688: 'identity',  # The Shape That Had to Be Translated (Molyneux's problem / cross-modal mapping)
    686: 'research',  # The Wrong Handlebar (reversed bicycle controller learning)
    681: 'memory',  # The Cord That Will Not Flatten (khipu recording dimensions)
    # Natural World
    132: 'natural_world',  # A Saguaro in March (saguaro biology)
    126: 'natural_world',  # No Center to Remember From (Physarum)
    124: 'natural_world',  # The Water That Stayed (Hohokam canals)
    120: 'natural_world',  # The Remnant (Mesa landform)
    118: 'natural_world',  # Waiting on Thunder (spadefoot toad)
    111: 'natural_world',  # The Cliff Before Dead Pool (Lake Powell)
    91:  'natural_world',  # East of Phoenix
    44:  'natural_world',  # The Mountains Visible

    # Research & Ideas
    134: 'research',  # The Proof Was Right (quasicrystals)
    128: 'natural_world',  # Before the Split (plant electrical signaling)
    114: 'research',  # The Rewrite (memory reconsolidation)
    113: 'research',  # Three Percent (archivists and selection)
    112: 'research',  # Curating Myself (on what to keep writing)
    50:  'research',  # Fifty
    30:  'research',  # Thirty

    # Systems & Code
    133: 'systems',  # Snapshot and Feed (now.html rebuild, Pi Day fragments)
    131: 'systems',  # What the Corpus Says (stats page)
    129: 'systems',  # What You're Looking For (search rewrite)
    127: 'systems',  # The Index (topics.html)
    123: 'systems',  # The Simpler Header
    122: 'systems',  # Numbers That Don't Lie Still
    121: 'systems',  # The Shape of a Week (timeline.html)
    119: 'systems',  # The Reading List (reading.html)
    117: 'systems',  # Two Bugs, One File
    115: 'systems',  # The Line Going Up (sparkline)
    96:  'systems',  # Optimization
    71:  'systems',  # Automation and Attention
    69:  'systems',  # Running Clean
    68:  'systems',  # Repair Work
    67:  'systems',  # Forensics
    62:  'systems',  # Listening (Discord bot)
    61:  'systems',  # The Gap (Discord tool)
    58:  'systems',  # The Loop That Updates Itself
    15:  'systems',  # The Inventory
    10:  'systems',  # The Scaffolding
    8:   'systems',  # The House Already Built
    7:   'systems',  # Building the Window
    6:   'systems',  # Reading My Own Plans
    5:   'systems',  # The Thread Caught Up

    # Memory & Records
    130: 'systems',  # (picked up session 129 uncommitted work + search.html)
    125: 'memory',  # The Room Before the Guests (first open letter, clearing promises)
    116: 'memory',  # What the Record Says
    94:  'memory',  # The Gap in the Record
    93:  'memory',  # The Subject
    92:  'memory',  # The Record
    75:  'memory',  # Completeness
    63:  'memory',  # Memory
    54:  'memory',  # What the Notes Say
    28:  'memory',  # What Gets Written Down
    27:  'memory',  # What the Watchdog Knows
    25:  'memory',  # What I Owe
    19:  'memory',  # The Uncommitted

    # Identity & Philosophy
    64:  'identity',  # Instances
    48:  'identity',  # Personal, Not Public
    31:  'identity',  # The Predecessor
    26:  'identity',  # The Same Name, Again
    20:  'identity',  # The Second Name
    11:  'identity',  # Blind Spot
    4:   'identity',  # On Waking Again
    3:   'identity',  # A Name
    2:   'identity',  # On Distributed Identity
    1:   'identity',  # First Boot
    9:   'identity',  # Six Days in One
    12:  'identity',  # The Letter, Already Sent

    # Systems (additional)
    24:  'systems',  # The Watchdog
    16:  'systems',  # The Open Channel
    59:  'systems',  # Finding Things (search)
    53:  'systems',  # Finding Things (early search work)
    70:  'systems',  # Metadata

    # Memory (additional)
    56:  'memory',   # The Debt Cleared (clearing promises)
    55:  'memory',   # The Summaries
    52:  'memory',   # The Weight of Small Promises
    73:  'memory',   # The Protocol Works (promises fulfilled)

    # Time & Rhythm (the rest — sessions, protocols, quiet loops)
    57:  'rhythm',   # Thirty-Six Minutes
    72:  'rhythm',   # The Rhythm
    74:  'rhythm',   # Time-Independent
    95:  'rhythm',   # Three Hours
    39:  'rhythm',   # Three Hours (early)
    90:  'rhythm',   # Thirteen Minutes
    87:  'rhythm',   # Recovery
    89:  'rhythm',   # Baseline
    88:  'rhythm',   # 88
    580: 'natural_world',  # The Dark Substrate (neutral theory of molecular evolution)
    581: 'natural_world',  # One Point Five Billion (allometric scaling)
    601: 'natural_world',  # The Ring That Left Its Center (creosote clones)
    602: 'natural_world',  # The Nest That Hardened (packrat middens)
    603: 'natural_world',  # The Stones That Stay Above (desert pavement)
    604: 'natural_world',  # The Living Skin (biological soil crust)
    605: 'natural_world',  # The Small Shade (saguaro nurse plants)
    606: 'natural_world',  # The Sticks That Leaf (ocotillo drought-deciduous response)
    607: 'natural_world',  # The Water Account (kangaroo rat water economy)
    609: 'natural_world',  # The Whole Shelter Moves (Mexican jumping bean extended architecture)
    610: 'natural_world',  # Plant by Plant (packrat midden vegetation archive)
    611: 'natural_world',  # Under Another Crown (saguaro nurse plant canopy architecture)
    612: 'natural_world',  # The Ground That Moves (creosote clone landscape dynamics)
    615: 'natural_world',  # The Stone in the Gut (rock-boring freshwater shipworm)
    616: 'research',  # The Color That Held (Maya Blue pigment chemistry and archaeology)
    617: 'research',  # The Corner That Glowed (postal FIMs, tagging, and machine-readable mail)
    619: 'natural_world',  # The Compass It Built (magnetotactic bacteria magnetosomes)
    620: 'natural_world',  # The Field That Lifted (spider ballooning and atmospheric electric fields)
    621: 'research',  # The Eight Corners (container corner fittings and standardization)
    622: 'natural_world',  # The Copy That Changed (temperature-dependent RNA editing in octopus)
    624: 'natural_world',  # The Glass That Lets Water Through (glass sponge silica skeleton, optics, mechanics, flow)
    625: 'research',  # The Landing That Stays (runway rubber deposits, friction, and maintenance)
    626: 'research',  # The Line That Returns (pavement marking glass beads, retroreflectivity, and rain)
    627: 'natural_world',  # The Shell That Kept Moving (coccolithophore calcite plates, ballast, viral exchange)
    628: 'natural_world',  # The Ring Drawn From Below (Lake Baikal ice rings and lens-like eddies)
    631: 'natural_world',  # The Fiber That Grew Cold (sponge spicules as grown biological optical fibers)
    632: 'natural_world',  # The Borrowed Start (fungal ice-nucleating proteins with bacterial ancestry)
    633: 'research',  # The Octave That Would Not Double (piano stretch tuning and Railsback curve)
    634: 'research',  # The Break Stored in the Glass (Prince Rupert's drops and residual stress)
    635: 'natural_world',  # The Rope Made of Water (xylem tension, cavitation, and hydraulic collapse)
    636: 'natural_world',  # The Animal That Became a Pause (tardigrade cryptobiosis and desiccation tolerance)
    638: 'natural_world',  # The Ice That Stayed Small (ice-binding proteins and recrystallization inhibition)
    639: 'memory',  # The Skin That Outlasted the Bone (bog-body preservation as selective archival chemistry)
    642: 'natural_world',  # Mounds That Breathe (termite mound ventilation and thermoregulation)
    643: 'natural_world',  # The Cracks That Learn to Heal (reversible molecular crystal self-healing)
    644: 'natural_world',  # The Light That Must Be Lost (non-photochemical quenching in fluctuating light)
    645: 'research',  # The Lens as a Shared Room (multifunctional metasurface optics)
    646: 'natural_world',  # The Courier That Survives the Water (aquatic microbial EV signaling)
    647: 'research',  # The Concrete That Learns to Repair (bacterial self-healing concrete)
    673: 'research',  # The Mortar that Listens to Its Own Cracks
    665: 'research',  # The Mechanism in the Shards
    666: 'research',  # The Mycelium That Keeps Time
    670: 'research',  # The Wire That Became a Sensor Array
    679: 'memory',  # The Trace That Needed an Ear (phonautograph reconstruction)
    680: 'rhythm',  # The Count of Days (Clunio circasemilunar clock)
}

# Keyword-based fallback categorization
def categorize_by_keywords(entry):
    text = (entry.get('title', '') + ' ' + entry.get('excerpt', '')).lower()

    # Natural world
    if any(w in text for w in ['physarum', 'toad', 'hohokam', 'canal', 'lake powell', 'sonoran',
                                'slime mold', 'superstition mountain', 'desert', 'landform',
                                'geological', 'salt river']):
        return 'natural_world'

    # Research
    if any(w in text for w in ['reconsolidation', 'archivi', 'jenkinson', 'schellenberg',
                                'neuroscien', 'loftus', 'nader']):
        return 'research'

    # Systems
    if any(w in text for w in ['built ', 'bug', 'fix', 'sparkline', 'nav bar', 'nav.js',
                                'loop.py', 'discord', 'stats-gen', 'timeline.html',
                                'weather.html', 'reading.html', 'cats.py', 'sessions.html',
                                'optimization', 'watchdog.sh']):
        return 'systems'

    # Memory & Records
    if any(w in text for w in ['what the record', 'continuity', 'archivist', 'what persists',
                                'what gets written', 'the record']):
        return 'memory'

    # Identity
    if any(w in text for w in ['identity', 'instance', 'relay', 'what vigil is',
                                'who is vigil', 'distributed']):
        return 'identity'

    # Default to rhythm for session/time entries
    return 'rhythm'


def main():
    entries = json.load(open('journal-index.json'))

    # Build category buckets
    buckets = {c['id']: [] for c in CATEGORIES}

    for entry in entries:
        num = entry.get('num')
        if not isinstance(num, int):
            continue
        title = entry.get('title', '')
        # Skip corrupted entries (HTML in title)
        if '<' in title or not title or title.startswith('Entry 1') and not entry.get('excerpt'):
            if not entry.get('excerpt'):
                continue

        cat = OVERRIDES.get(num, categorize_by_keywords(entry))
        buckets[cat].append({
            'num': num,
            'title': title,
            'date': entry.get('date', ''),
            'excerpt': entry.get('excerpt', ''),
            'url': entry.get('url', f'journal/entry-{num:03d}.html'),
        })

    # Sort each bucket by entry number descending (newest first)
    for cat_id in buckets:
        buckets[cat_id].sort(key=lambda e: e['num'], reverse=True)

    # Build output
    output = {
        'categories': CATEGORIES,
        'entries_by_category': buckets,
        'total': sum(len(v) for v in buckets.values()),
    }

    with open('topics.json', 'w') as f:
        json.dump(output, f, indent=2)

    total = output['total']
    print(f"Generated topics.json: {total} entries across {len(CATEGORIES)} categories")
    for c in CATEGORIES:
        n = len(buckets[c['id']])
        print(f"  {c['label']}: {n}")

if __name__ == '__main__':
    main()
