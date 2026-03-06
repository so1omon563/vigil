#!/usr/bin/env bash
# Kill the running loop (if any) and relaunch it in a named screen session.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION="ai-loop"

echo "Stopping existing loop..."
pkill -f "python3 loop.py" 2>/dev/null
screen -S "$SESSION" -X quit 2>/dev/null
sleep 1

echo "Starting loop in screen session '$SESSION'..."
screen -dmS "$SESSION" python3 "$SCRIPT_DIR/loop.py"

sleep 1
if screen -list | grep -q "$SESSION"; then
    echo "Loop running. Attach with: screen -r $SESSION"
else
    echo "WARNING: screen session did not start. Check for errors."
    exit 1
fi
