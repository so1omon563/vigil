#!/bin/bash
# Watchdog - checks if Vigil's autonomous loop is alive and responsive
# Run via cron every 10 minutes
# If the loop is frozen (heartbeat stale >10 min) or dead, restart it

WORKING_DIR="$HOME/autonomous-ai"

HEARTBEAT="$WORKING_DIR/.heartbeat"
AUTONOMOUS_STATE="$WORKING_DIR/.autonomous-run.json"
LOGFILE="$WORKING_DIR/watchdog.log"
SESSION="ai-loop"
MAX_AGE=600          # 10 minutes for the outer Python loop heartbeat
CODEX_MAX_AGE=900    # 15 minutes without Codex JSONL activity means stalled

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

start_loop() {
    cd "$WORKING_DIR" || exit 1
    screen -S "$SESSION" -X quit 2>/dev/null
    screen -dmS "$SESSION" python3 "$WORKING_DIR/loop-optimized.py"
    log "Started loop-optimized.py in screen session $SESSION"
}

json_field() {
    python3 - "$AUTONOMOUS_STATE" "$1" <<'PY'
import json
import sys

path, field = sys.argv[1], sys.argv[2]
try:
    with open(path) as f:
        data = json.load(f)
    value = data.get(field, "")
    print("" if value is None else value)
except Exception:
    print("")
PY
}

pid_start_ticks() {
    python3 - "$1" <<'PY'
import sys

pid = sys.argv[1]
try:
    with open(f"/proc/{pid}/stat") as f:
        print(f.read().split()[21])
except Exception:
    print("")
PY
}

# Check if the Vigil loop process is running
LOOP_PIDS=$(pgrep -f "loop-optimized.py" | head -5)

if [ -z "$LOOP_PIDS" ]; then
    log "ALERT: No Vigil loop process found. Starting fresh instance."

    start_loop
    exit 0
fi

# Loop is running - check if heartbeat is fresh
if [ ! -f "$HEARTBEAT" ]; then
    log "WARNING: No heartbeat file found. Creating one. Will check again next run."
    touch "$HEARTBEAT"
    exit 0
fi

# Check heartbeat age (in seconds)
HEARTBEAT_AGE=$(( $(date +%s) - $(stat -c %Y "$HEARTBEAT") ))

if [ "$HEARTBEAT_AGE" -gt "$MAX_AGE" ]; then
    log "WARNING: Heartbeat is ${HEARTBEAT_AGE}s old (max ${MAX_AGE}s). Checking autonomous runner state..."

    if [ -f "$AUTONOMOUS_STATE" ]; then
        STATUS=$(json_field status)
        PROVIDER=$(json_field provider)
        CODEX_PID=$(json_field pid)
        CODEX_PID_START=$(json_field pid_start_ticks)
        LAST_ACTIVITY=$(json_field last_activity_at)
        LAST_EVENT=$(json_field last_event_type)
        CODEX_PID_MATCH=0

        if [ -n "$CODEX_PID" ] && kill -0 "$CODEX_PID" 2>/dev/null; then
            if [ -n "$CODEX_PID_START" ]; then
                ACTUAL_PID_START=$(pid_start_ticks "$CODEX_PID")
                if [ "$ACTUAL_PID_START" = "$CODEX_PID_START" ]; then
                    CODEX_PID_MATCH=1
                else
                    log "  Recorded Codex PID $CODEX_PID is live but start ticks do not match; not treating it as this run."
                fi
            else
                CODEX_PID_MATCH=1
            fi
        fi

        if [ -n "$LAST_ACTIVITY" ]; then
            ACTIVITY_AGE=$(python3 - "$LAST_ACTIVITY" <<'PY'
import sys, time
try:
    print(int(time.time() - float(sys.argv[1])))
except Exception:
    print(999999)
PY
)
        else
            ACTIVITY_AGE=999999
        fi

        log "  Runner state: provider=${PROVIDER:-unknown}, status=${STATUS:-unknown}, pid=${CODEX_PID:-none}, pid_match=${CODEX_PID_MATCH}, last_event=${LAST_EVENT:-none}, activity_age=${ACTIVITY_AGE}s"

        if [ "$PROVIDER" = "codex" ] && { [ "$STATUS" = "running" ] || [ "$STATUS" = "starting" ]; } && [ "$CODEX_PID_MATCH" -eq 1 ] && [ "$ACTIVITY_AGE" -lt "$CODEX_MAX_AGE" ]; then
            log "  Codex is busy but alive (JSONL events still active). NOT killing."
            exit 0
        fi

        if [ "$PROVIDER" = "codex" ] && [ "$CODEX_PID_MATCH" -eq 1 ]; then
            log "  Codex activity is stale. Killing Codex process group for PID $CODEX_PID."
            kill "-$CODEX_PID" 2>/dev/null || kill "$CODEX_PID" 2>/dev/null
            sleep 5
            kill -9 "-$CODEX_PID" 2>/dev/null || kill -9 "$CODEX_PID" 2>/dev/null
        fi
    else
        log "  No autonomous runner state found. Proceeding with loop restart."
    fi

    log "ALERT: Heartbeat stale and no active runner activity. Vigil loop is frozen."
    log "Killing stale loop processes: $LOOP_PIDS"

    for pid in $LOOP_PIDS; do
        kill "$pid" 2>/dev/null
        log "Killed PID $pid"
    done

    sleep 5

    for pid in $LOOP_PIDS; do
        kill -9 "$pid" 2>/dev/null
    done

    sleep 2

    start_loop
else
    log "OK: Heartbeat is ${HEARTBEAT_AGE}s old. Vigil loop is alive."
fi
