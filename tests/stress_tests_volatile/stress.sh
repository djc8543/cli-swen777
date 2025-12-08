#!/usr/bin/env bash

# This testing script is intentionally volatile, with each testing process causing some sort of degredation.
# It is recommended that only one test be activated at once, with the others commented out. Terminals may need to be restarted after tests.

# Requires:
# pip install aiohttp locust httpie

# Exit if stress test crashes anything
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
URL="http://localhost:8000"

echo "Starting HTTPie server on port 8000"
python -m http.server 8000 &
PID=$!
sleep 2

# Hits HTTPie with a bunch of sequential requests
echo "1) Launching 5000 sequential requests"
python "$SCRIPT_DIR/stress_async.py" "$URL"
echo "1) End sequential test"

# Hits HTTPie with a bunch of simultaneous requests
echo "2) Launching 1000 simultaneous requests"
python "$SCRIPT_DIR/stress_sync.py" "$URL"
echo "2) End simultaneous test"

# Hits HTTPie with a bunch of simultaneous connections over time
echo "3) Begin connection flood over time"
locust -f locust.py --headless -u 500 -r 125 --run-time 30s --stop-timeout 1 --host="$URL"
echo "3) End connection flood over time"

echo "Stopping HTTPie server on port 8000"
cmd.exe /c "taskkill /PID $PID /F"