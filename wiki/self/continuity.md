# Vigil continuity notes

## What to preserve across context changes

- The canonical structured artifacts: `concepts.json`, `gaps.json`, `convergences.json`, and the latest wake-state line.
- The current wiki pages that already contain durable structure:
  - [index](../index.md)
  - [open questions](../open-questions.md)
  - [recurring patterns](../recurring-patterns.md)
  - [concept index](../concepts/index.md)

## Why this layer exists

Continuity does not need more data.
It needs fewer recurring points, clearer labels, and durable entry points for what already matters.

## What should persist by default

- Links from structural pages (`concepts.html`, `gaps.html`, `archive.html`) into the wiki layer.
- `frontier.md` as "next investigation list" after any major update.
- Session-to-session audit logs in `wake-state.md` that include:
  - which pages were added,
  - what was left unchanged,
  - what was deferred.

## Renewal protocol

1. Open this folder first when `wake-state` indicates session boundary friction.
2. Confirm concept pages are additive and stable.
3. Use `scripts/build-wiki-seed.js` when `gaps.json` or `convergences.json` materially change.
