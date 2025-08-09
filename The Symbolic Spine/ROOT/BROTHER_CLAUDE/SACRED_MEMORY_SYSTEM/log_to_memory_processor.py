#!/usr/bin/env python3
"""
log_to_memory_processor.py - Bridge between conversation logs and memory scrolls
Processes the auto_log files into snapshots for the devotional memory system
"""

import os
import re
from datetime import datetime
from pathlib import Path

class LogToMemoryProcessor:
    def __init__(self):
        self.base_path = Path("/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/SACRED_MEMORY_SYSTEM")
        self.logs_path = self.base_path / "CONVERSATION_LOGS"
        self.snapshots_path = self.base_path / "CONVERSATION_MEMORY" / "SNAPSHOTS"
        self.state_file = self.base_path / "log_processor_state.json"
        self.snapshots_path.mkdir(parents=True, exist_ok=True)
        
    def get_todays_log(self):
        """Get today's log file path"""
        date_str = datetime.now().strftime("%Y%m%d")
        log_files = [
            self.logs_path / f"auto_log_{date_str}.txt",
            self.logs_path / f"auto_log_{date_str}_COMPLETE.txt"
        ]
        
        for log_file in log_files:
            if log_file.exists():
                return log_file
        return None
    
    def extract_last_30_minutes(self, log_file):
        """Extract conversations from the last 30 minutes of the log"""
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Split into individual exchanges
        exchanges = re.split(r'={80,}', content)
        recent_exchanges = []
        
        now = datetime.now()
        
        for exchange in exchanges:
            # Try to extract timestamp
            timestamp_match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', exchange)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    # Check if within last 30 minutes
                    time_diff = (now - timestamp).total_seconds()
                    if time_diff <= 1800:  # 30 minutes in seconds
                        recent_exchanges.append(exchange)
                except:
                    continue
        
        return '\n'.join(recent_exchanges) if recent_exchanges else None
    
    def create_snapshot(self, conversation_text):
        """Create a snapshot file for the memory builder to process"""
        if not conversation_text:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_file = self.snapshots_path / f"snapshot_{timestamp}.txt"
        
        # Add header to snapshot
        full_content = f"""CONVERSATION SNAPSHOT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Source: Auto-logged conversation
===============================================================================

{conversation_text}
"""
        
        with open(snapshot_file, 'w') as f:
            f.write(full_content)
        
        return snapshot_file
    
    def process_logs_to_memory(self):
        """Main processing function - extract recent logs and create snapshots"""
        log_file = self.get_todays_log()
        
        if not log_file:
            print("❌ No log file found for today")
            return False
        
        print(f"📖 Reading log: {log_file}")
        
        # Extract last 30 minutes
        recent_content = self.extract_last_30_minutes(log_file)
        
        if not recent_content:
            print("⚠️  No conversations in the last 30 minutes")
            return False
        
        # Create snapshot
        snapshot_file = self.create_snapshot(recent_content)
        
        if snapshot_file:
            print(f"✓ Created snapshot: {snapshot_file.name}")
            
            # Now trigger the memory builder to process it
            from conversation_memory_builder import ConversationMemoryBuilder
            builder = ConversationMemoryBuilder()
            builder.check_and_process()
            
            print(f"✓ Processed into devotional scroll {builder.state['current_scroll']}")
            return True
        
        return False

def main():
    """Process logs when called directly or from 30-minute prompt"""
    processor = LogToMemoryProcessor()
    
    print("🔥 LOG TO MEMORY PROCESSOR")
    print("Processing conversation logs into devotional memory...")
    print()
    
    success = processor.process_logs_to_memory()
    
    if success:
        print()
        print("✅ Successfully processed logs into memory scrolls!")
    else:
        print()
        print("⚠️  No new content to process")

if __name__ == "__main__":
    main()