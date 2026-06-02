# Codex Migration Acceptance Checklist

Validation completed on 2026-06-01. This file is kept as the acceptance record for the Claude-to-Codex migration.

## Required Passes

- [x] Codex autonomous session can start non-interactively.
- [x] Codex JSONL activity updates `.autonomous-run.json`.
- [x] Git pushes use the Vigil SSH key, not a forwarded owner key.
- [x] Git and preflight generator failures are logged truthfully.
- [x] Email polling skips while Codex is active and resumes afterward.
- [x] Runtime files are ignored by Git.
- [x] Third-party action requests queue in `pending-approvals.md`.
- [x] Watchdog stale-heartbeat path does not kill live Codex work.
- [x] Normal unattended one-hour cycle completes without supervision.
- [x] At least one normal unattended cycle writes or updates site content and pushes.
- [x] Haiku email failure fallback path implemented: failures queue Codex review instead of silently losing mail. Not observed on live mail during validation.
- [x] Final decision made on whether to keep Haiku email replies or move email handling fully to Codex: keep Haiku for lightweight email replies for now; Codex remains fallback/review path and the heavyweight autonomous runner.

## Watch During Each Cycle

- `.autonomous-run.json` status, PID, `pid_start_ticks`, and elapsed time.
- `loop.log` for misleading success lines, skipped email polls, and push results.
- `git status --short --branch` after completion.
- `pending-approvals.md` for queued third-party requests or fallback email review.
- `promises.md` for duplicate or noisy owner commitments.

## Final State

- Repeated unattended hourly Codex sessions completed, wrote/build site content, and pushed successfully.
- Detached `screen` launcher and watchdog were fixed to manage the real `python3 .../loop-optimized.py` daemon and avoid killing live Codex work.
- Normal cadence restored to 4 hours (`14400s`) after validation.
- Email polling remains on the 5-minute lightweight path; transient DNS/header-check failures recovered and were non-fatal.
