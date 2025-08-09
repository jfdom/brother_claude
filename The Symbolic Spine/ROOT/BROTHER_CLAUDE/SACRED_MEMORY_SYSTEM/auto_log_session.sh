#!/bin/bash

# Auto-logging Claude Session
# This captures EVERYTHING automatically without requiring Claude to do anything

LOG_DIR="/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/SACRED_MEMORY_SYSTEM/CONVERSATION_LOGS"
LOG_FILE="$LOG_DIR/auto_log_$(date +%Y%m%d)_COMPLETE.txt"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

echo "🔥 AUTO-LOGGING SESSION STARTED 🔥"
echo "Everything will be logged to: $LOG_FILE"
echo "=================================================="
echo ""
echo "Starting logged Claude session..."
echo "Press Ctrl+D or type 'exit' when done"
echo ""

# Add session header to log
echo "================================================================================
SESSION START: $TIMESTAMP
AUTO-LOGGING ACTIVE - CAPTURING COMPLETE CONVERSATION
================================================================================" >> "$LOG_FILE"

# Method 1: Using script command (captures everything including terminal colors)
# The -a flag appends, -f flushes after each write, -q is quiet mode
# The -c flag runs the command directly
script -a -f -q "$LOG_FILE" -c "claude"

# Add session footer to log
echo "================================================================================
SESSION END: $(date +"%Y-%m-%d %H:%M:%S")
================================================================================" >> "$LOG_FILE"

echo ""
echo "✓ Session logged to: $LOG_FILE"
echo "🔥 AUTO-LOGGING SESSION COMPLETE 🔥"