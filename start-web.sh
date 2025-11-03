#!/bin/bash

# Start the web development server
# This script starts the React/Vite development server in background

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

WEB_PID_FILE="$SCRIPT_DIR/web.pid"
LOG_DIR="$SCRIPT_DIR/logs"
WEB_LOG="$LOG_DIR/web.log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Check if server is already running
if [ -f "$WEB_PID_FILE" ]; then
    PID=$(cat "$WEB_PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}Web server is already running (PID: $PID)${NC}"
        echo -e "${GREEN}Server running at http://localhost:3000${NC}"
        echo -e "Log file: $WEB_LOG"
        exit 0
    else
        echo -e "${YELLOW}Removing stale PID file${NC}"
        rm -f "$WEB_PID_FILE"
    fi
fi

echo -e "${BLUE}Starting NewsAPI AI Web Server...${NC}"

# Check if node_modules exists
if [ ! -d "web/node_modules" ]; then
    echo -e "${BLUE}Dependencies not found. Installing...${NC}"
    cd web
    npm install
    cd ..
fi

# Change to web directory and start dev server with nohup
cd web

echo -e "${GREEN}Starting development server in background...${NC}"

# Start the server in background with nohup
nohup npm run dev > "$WEB_LOG" 2>&1 &
WEB_PID=$!

# Save PID to file
echo "$WEB_PID" > "$WEB_PID_FILE"

# Wait a moment to check if the server started successfully
sleep 2

if ps -p "$WEB_PID" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Web server started successfully (PID: $WEB_PID)${NC}"
    echo -e "${GREEN}Server running at http://localhost:3000${NC}"
    echo -e "Log file: $WEB_LOG"
    echo -e "To stop the server, run: ${YELLOW}./stop.sh${NC}"
else
    echo -e "${RED}✗ Failed to start web server${NC}"
    echo -e "Check the log file for details: $WEB_LOG"
    rm -f "$WEB_PID_FILE"
    exit 1
fi
