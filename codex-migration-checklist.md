# Codex Migration Acceptance Checklist

Compressed validation window: billing changes tomorrow, so treat the next few cycles as acceptance tests.

## Required Passes

- [x] Codex autonomous session can start non-interactively.
- [x] Codex JSONL activity updates `.autonomous-run.json`.
- [x] Git pushes use the Vigil SSH key, not a forwarded owner key.
- [x] Git and preflight generator failures are logged truthfully.
- [x] Email polling skips while Codex is active and resumes afterward.
- [x] Runtime files are ignored by Git.
- [x] Third-party action requests queue in `pending-approvals.md`.
- [x] Watchdog stale-heartbeat path does not kill live Codex work.
- [ ] Normal unattended one-hour cycle completes without supervision.
- [ ] At least one normal unattended cycle writes or updates site content and pushes.
- [ ] Haiku email failure falls back to queued Codex review instead of silently losing mail.
- [ ] Final decision made on whether to keep Haiku email replies or move email handling fully to Codex.

## Watch During Each Cycle

- `.autonomous-run.json` status, PID, `pid_start_ticks`, and elapsed time.
- `loop.log` for misleading success lines, skipped email polls, and push results.
- `git status --short --branch` after completion.
- `pending-approvals.md` for queued third-party requests or fallback email review.
- `promises.md` for duplicate or noisy owner commitments.

