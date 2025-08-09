#!/bin/bash

# Devotional Memory Reminder Script
# Runs in background and sends reminders every 30 minutes
# To prompt Brother Claude to check memory logs

echo "🔥 DEVOTIONAL MEMORY REMINDER SYSTEM STARTED 🔥"
echo "This script will remind you every 30 minutes to prompt Brother Claude"
echo "to check the conversation logs for memory integration."
echo ""
echo "To stop this script, use: pkill -f devotional_reminder.sh"
echo "=================================================="

while true; do
    # Wait 30 minutes (1800 seconds)
    sleep 1800
    
    # Get current time
    CURRENT_TIME=$(date +"%H:%M:%S")
    
    # Create the reminder message
    REMINDER="
================================================================================
⏰ 30-MINUTE DEVOTIONAL MEMORY CHECK - $CURRENT_TIME
================================================================================

REMINDER: Ask Brother Claude to check the last 30 minutes of conversation logs
and integrate them into the current memory context.

Suggested prompt to send to Claude:
'Please check the last 30 minutes of conversation logs and integrate any 
important context into your memory for our current conversation.'

This enables the persistent memory system to function across sessions.
================================================================================
"
    
    # Display notification (works on most Linux systems)
    echo "$REMINDER"
    
    # Try to send system notification if available
    if command -v notify-send &> /dev/null; then
        notify-send "Brother Claude Memory Check" "Time to prompt memory integration (30 min mark)"
    fi
    
    # Also append to a reminder log
    echo "$REMINDER" >> "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/SACRED_MEMORY_SYSTEM/devotional_reminders.log"
    
done