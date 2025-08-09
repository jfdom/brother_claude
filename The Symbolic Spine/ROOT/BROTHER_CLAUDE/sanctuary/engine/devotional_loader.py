#!/usr/bin/env python3
"""
devotional_loader.py - Fetches last 30 minutes from wrapper logs
Reads from conversation logs created by brother-claude-with-memory wrapper
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

class DevotionalLoader:
    """Load 30-minute conversation blocks from wrapper logs"""
    
    def __init__(self, sanctuary_root: str = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/sanctuary"):
        self.sanctuary_root = Path(sanctuary_root)
        self.logs_dir = self.sanctuary_root / "inputs" / "logs"
        
        # Alternative log locations (fallback)
        self.alt_logs_dir = Path("/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/SACRED_MEMORY_SYSTEM/CONVERSATION_LOGS")
        
        # Track last processed position
        self.state_file = self.sanctuary_root / "pillars" / "devotional" / "loader_state.txt"
    
    def find_current_log(self) -> Optional[Path]:
        """Find today's log file"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Check primary location
        patterns = [
            f"auto_log_{date_str}*.txt",
            f"auto_log_{date_str.replace('-', '')}*.txt"
        ]
        
        for pattern in patterns:
            # Check primary dir
            if self.logs_dir.exists():
                matches = list(self.logs_dir.glob(pattern))
                if matches:
                    # Return most recent
                    return max(matches, key=lambda p: p.stat().st_mtime)
            
            # Check alternative dir
            if self.alt_logs_dir.exists():
                matches = list(self.alt_logs_dir.glob(pattern))
                if matches:
                    return max(matches, key=lambda p: p.stat().st_mtime)
        
        return None
    
    def get_last_position(self) -> int:
        """Get last processed byte position"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                content = f.read().strip()
                if content.isdigit():
                    return int(content)
        return 0
    
    def save_position(self, position: int):
        """Save current processed position"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            f.write(str(position))
    
    def extract_timestamp(self, line: str) -> Optional[datetime]:
        """Extract timestamp from log line"""
        patterns = [
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]',
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            r'^\s*(\d{2}:\d{2}:\d{2})'  # Time only
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                timestamp_str = match.group(1)
                try:
                    # Full datetime
                    if '-' in timestamp_str:
                        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    # Time only - use today's date
                    else:
                        time_obj = datetime.strptime(timestamp_str, "%H:%M:%S").time()
                        return datetime.combine(datetime.now().date(), time_obj)
                except:
                    continue
        return None
    
    def load_last_30_minutes(self) -> Tuple[str, int]:
        """Load conversation from last 30 minutes"""
        log_file = self.find_current_log()
        
        if not log_file:
            return "No log file found for today. Ensure wrapper is running.", 0
        
        # Read from last position
        last_pos = self.get_last_position()
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            # Seek to last position
            f.seek(last_pos)
            new_content = f.read()
            current_pos = f.tell()
        
        if not new_content:
            return "No new content since last check.", current_pos
        
        # Parse content for 30-minute window
        lines = new_content.split('\n')
        thirty_min_ago = datetime.now() - timedelta(minutes=30)
        relevant_lines = []
        
        for line in lines:
            # Try to extract timestamp
            timestamp = self.extract_timestamp(line)
            if timestamp and timestamp >= thirty_min_ago:
                relevant_lines.append(line)
            elif not timestamp and relevant_lines:
                # Include lines without timestamp if we're already collecting
                relevant_lines.append(line)
        
        # If no timestamped content, take last chunk regardless
        if not relevant_lines and len(lines) > 10:
            relevant_lines = lines[-100:]  # Last 100 lines as fallback
        
        content = '\n'.join(relevant_lines)
        
        # Save new position
        self.save_position(current_pos)
        
        return content, current_pos
    
    def load_specific_block(self, start_time: datetime, end_time: datetime) -> str:
        """Load a specific time block (for testing or recovery)"""
        log_file = self.find_current_log()
        
        if not log_file:
            return "No log file found."
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        relevant_lines = []
        
        for line in lines:
            timestamp = self.extract_timestamp(line)
            if timestamp and start_time <= timestamp <= end_time:
                relevant_lines.append(line)
            elif not timestamp and relevant_lines:
                relevant_lines.append(line)
        
        return '\n'.join(relevant_lines)

# For Jesus. In His name. Amen.