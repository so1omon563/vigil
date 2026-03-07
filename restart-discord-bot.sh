#!/usr/bin/env bash
# Kill the running discord bot (if any) and relaunch it in a named screen session.
# Must be run interactively by the owner — will refuse to run from a non-TTY context.

if [ ! -t 0 ]; then
    echo "ERROR: restart-discord-bot.sh must be run interactively in a terminal. Refusing to run." >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION="discord-bot"

echo "Stopping existing discord bot..."
pkill -f "node.*discord-bot.js" 2>/dev/null
screen -S "$SESSION" -X quit 2>/dev/null
sleep 1

echo "Starting discord bot in screen session '$SESSION'..."
screen -dmS "$SESSION" node "$SCRIPT_DIR/discord-bot.js"

sleep 1
if screen -list | grep -q "$SESSION"; then
    echo "Discord bot running. Attach with: screen -r $SESSION"
else
    echo "WARNING: screen session did not start. Check for errors."
    exit 1
fi
