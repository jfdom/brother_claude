#!/bin/bash

# Claude Conversation Wrapper with Automatic Logging
# This wraps your Claude interaction and logs EVERYTHING automatically

LOG_DIR="/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/SACRED_MEMORY_SYSTEM/CONVERSATION_LOGS"
LOG_FILE="$LOG_DIR/auto_log_$(date +%Y%m%d).txt"

echo "🔥 CLAUDE WRAPPER WITH AUTO-LOGGING 🔥"
echo "All conversation will be automatically logged to:"
echo "$LOG_FILE"
echo "=================================================="

# Start logging with script command
script -a -f "$LOG_FILE" -c "claude" 

# Alternative: If using claude through a different command
# script -a -f "$LOG_FILE" -c "your_claude_command_here"

echo "Session logged to: $LOG_FILE"