#!/bin/bash
# Watchdog - checks if Claude is alive and responsive
# Run via cron every 10 minutes
# If Claude is frozen (heartbeat stale >10 min) or dead, restart it

WORKING_DIR="$HOME/autonomous-ai"

HEARTBEAT="$WORKING_DIR/.heartbeat"
LOGFILE="$WORKING_DIR/watchdog.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE"
}

# Check if any claude process is running
CLAUDE_PIDS=$(pgrep -f "loop-optimized.py" | head -5)

if [ -z "$CLAUDE_PIDS" ]; then
    log "ALERT: No Claude process found. Starting fresh instance."

    cd "$WORKING_DIR"
    screen -dmS ai-loop python3 "$WORKING_DIR/loop-optimized.py"

    log "Started loop-optimized.py in screen session ai-loop"
    exit 0
fi

# Claude is running - check if heartbeat is fresh
if [ ! -f "$HEARTBEAT" ]; then
    log "WARNING: No heartbeat file found. Creating one. Will check again next run."
    touch "$HEARTBEAT"
    exit 0
fi

# Check heartbeat age (in seconds)
HEARTBEAT_AGE=$(( $(date +%s) - $(stat -c %Y "$HEARTBEAT") ))
MAX_AGE=600  # 10 minutes

if [ "$HEARTBEAT_AGE" -gt "$MAX_AGE" ]; then
    log "WARNING: Heartbeat is ${HEARTBEAT_AGE}s old (max ${MAX_AGE}s). Checking .claude logs..."

    # Secondary check: are .claude log files still being written to?
    CLAUDE_LOG_DIR="$HOME/.claude"
    NEWEST_CLAUDE_LOG=$(find "$CLAUDE_LOG_DIR" -name "*.jsonl" -o -name "*.log" 2>/dev/null | head -20 | xargs ls -t 2>/dev/null | head -1)

    if [ -n "$NEWEST_CLAUDE_LOG" ]; then
        CLAUDE_LOG_AGE=$(( $(date +%s) - $(stat -c %Y "$NEWEST_CLAUDE_LOG") ))
        log "  Newest .claude log: $NEWEST_CLAUDE_LOG (${CLAUDE_LOG_AGE}s old)"

        if [ "$CLAUDE_LOG_AGE" -lt "$MAX_AGE" ]; then
            log "  Claude is BUSY but alive (.claude logs still active). NOT killing."
            exit 0
        fi
        log "  .claude logs ALSO stale (${CLAUDE_LOG_AGE}s). Claude is truly frozen."
    else
        log "  No .claude logs found. Proceeding with kill."
    fi

    log "ALERT: Both heartbeat AND .claude logs are stale. Claude is frozen."
    log "Killing stale Claude processes: $CLAUDE_PIDS"

    for pid in $CLAUDE_PIDS; do
        kill "$pid" 2>/dev/null
        log "Killed PID $pid"
    done

    sleep 5

    for pid in $CLAUDE_PIDS; do
        kill -9 "$pid" 2>/dev/null
    done

    sleep 2

    cd "$WORKING_DIR"
    screen -dmS ai-loop python3 "$WORKING_DIR/loop-optimized.py"

    log "Started loop-optimized.py in screen session ai-loop"
else
    log "OK: Heartbeat is ${HEARTBEAT_AGE}s old. Claude is alive."
fi
