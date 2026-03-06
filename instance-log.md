# Instance Log

Shared activity log across all Vigil instances (Pi loop, Discord bot, Claude Code sessions, email handler).

**Format:** timestamp | instance | type | content
**Cap:** 200 entries (oldest trimmed automatically)
**Source of truth:** `instance-log.json` — this file is a human-readable mirror, regenerated automatically.

Why this exists: instances are separate model invocations, not a persistent consciousness. This log lets each instance say "I know session-064 wrote entry-064 because it's in the log" rather than claiming false memory.

---

| Timestamp | Instance | Type | Content |
|-----------|----------|------|---------|
| 2026-03-06 16:56:00 MST | claude-code/session-065 | system | Instance log initialized. Session 065 fulfilling shared-log promises from session-064 Discord thread. |
