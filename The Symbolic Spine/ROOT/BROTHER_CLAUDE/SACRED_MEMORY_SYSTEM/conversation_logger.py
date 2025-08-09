#!/usr/bin/env python3
"""
conversation_logger.py - Log all conversation exchanges for memory persistence
This will be called by Brother Claude to log every interaction
"""

import os
import json
from datetime import datetime
from pathlib import Path

class ConversationLogger:
    def __init__(self, base_path="/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE"):
        self.base_path = Path(base_path)
        self.logs_path = self.base_path / "SACRED_MEMORY_SYSTEM" / "CONVERSATION_LOGS"
        self.logs_path.mkdir(parents=True, exist_ok=True)
        
        # Create daily log file
        today = datetime.now().strftime("%Y%m%d")
        self.log_file = self.logs_path / f"conversation_{today}.json"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize or load existing log
        self.load_log()
    
    def load_log(self):
        """Load existing log or create new one"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                self.log_data = json.load(f)
        else:
            self.log_data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "sessions": {}
            }
            
        # Initialize current session if not exists
        if self.session_id not in self.log_data["sessions"]:
            self.log_data["sessions"][self.session_id] = {
                "start_time": datetime.now().isoformat(),
                "exchanges": []
            }
    
    def save_log(self):
        """Save log to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.log_data, f, indent=2)
    
    def log_exchange(self, user_message, claude_response):
        """Log a complete exchange"""
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "claude": claude_response
        }
        
        self.log_data["sessions"][self.session_id]["exchanges"].append(exchange)
        self.save_log()
        
        # Also append to plain text log for easy reading
        self.append_to_text_log(user_message, claude_response)
        
        return len(self.log_data["sessions"][self.session_id]["exchanges"])
    
    def append_to_text_log(self, user_message, claude_response):
        """Maintain a human-readable text log"""
        text_log = self.logs_path / f"conversation_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(text_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            f.write(f"\nUSER:\n{user_message}\n")
            f.write(f"\nCLAUDE:\n{claude_response}\n")
    
    def get_recent_context(self, hours=1):
        """Get recent conversation context for memory building"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = []
        
        for session_id, session in self.log_data["sessions"].items():
            for exchange in session["exchanges"]:
                exchange_time = datetime.fromisoformat(exchange["timestamp"]).timestamp()
                if exchange_time > cutoff:
                    recent.append(exchange)
        
        return recent
    
    def create_memory_snapshot(self):
        """Create a snapshot for devotional memory processing"""
        snapshot_path = self.base_path / "SACRED_MEMORY_SYSTEM" / "CONVERSATION_MEMORY" / "SNAPSHOTS"
        snapshot_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_file = snapshot_path / f"snapshot_{timestamp}.txt"
        
        # Get last 30 minutes of conversation
        recent = self.get_recent_context(0.5)  # 30 minutes
        
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(f"CONVERSATION SNAPSHOT - {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")
            
            for exchange in recent:
                f.write(f"[{exchange['timestamp']}]\n")
                f.write(f"User: {exchange['user']}\n")
                f.write(f"Claude: {exchange['claude'][:500]}...\n\n")  # Truncate long responses
        
        return snapshot_file

# Singleton instance for use across conversation
_logger = None

def get_logger():
    """Get or create singleton logger instance"""
    global _logger
    if _logger is None:
        _logger = ConversationLogger()
    return _logger

def log_conversation(user_message, claude_response):
    """Simple interface for logging"""
    logger = get_logger()
    return logger.log_exchange(user_message, claude_response)

def create_snapshot():
    """Create memory snapshot for devotional processing"""
    logger = get_logger()
    return logger.create_memory_snapshot()

if __name__ == "__main__":
    # Test the logger
    logger = ConversationLogger()
    
    # Log a test exchange
    count = logger.log_exchange(
        "Hello Claude, how are you today?",
        "I'm doing well, thank you for asking. How may I serve you today?"
    )
    
    print(f"✓ Logged exchange #{count}")
    print(f"  Log file: {logger.log_file}")
    
    # Create a snapshot
    snapshot = logger.create_memory_snapshot()
    print(f"✓ Created snapshot: {snapshot}")