#!/usr/bin/env python3
"""
scripture_loader.py - Streams 777-line windows from KJV Bible
Tracks position and provides exact line counts for Scripture pillar
"""

import os
from pathlib import Path
from typing import Tuple, Optional, List

class ScriptureLoader:
    """Load 777-line blocks from Scripture"""
    
    def __init__(self, sanctuary_root: str = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER_CLAUDE/sanctuary"):
        self.sanctuary_root = Path(sanctuary_root)
        self.scripture_dir = self.sanctuary_root / "inputs" / "scripture"
        self.scripture_file = self.scripture_dir / "kjv.txt"
        
        # Alternative location
        self.alt_scripture = Path("/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/CODEX/SCROLLS/KJV.txt")
        
        # State tracking
        self.state_file = self.sanctuary_root / "pillars" / "scripture" / "loader_state.txt"
        self.lines_per_block = 777
    
    def get_scripture_path(self) -> Optional[Path]:
        """Find the KJV scripture file"""
        if self.scripture_file.exists():
            return self.scripture_file
        elif self.alt_scripture.exists():
            return self.alt_scripture
        else:
            # Try to find any KJV file
            patterns = ["*KJV*.txt", "*kjv*.txt", "*bible*.txt"]
            for pattern in patterns:
                if self.scripture_dir.exists():
                    matches = list(self.scripture_dir.glob(pattern))
                    if matches:
                        return matches[0]
            return None
    
    def get_current_line(self) -> int:
        """Get current line position in Scripture"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                content = f.read().strip()
                if content.isdigit():
                    return int(content)
        return 1  # Start from line 1
    
    def save_position(self, line_number: int):
        """Save current line position"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            f.write(str(line_number))
    
    def load_lines(self, start_line: int, count: int) -> Tuple[List[str], int]:
        """Load specific lines from Scripture"""
        scripture_path = self.get_scripture_path()
        
        if not scripture_path:
            return ["Scripture file not found. Please place KJV.txt in inputs/scripture/"], 0
        
        lines = []
        current_line = 0
        
        with open(scripture_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                if i >= start_line:
                    lines.append(line.rstrip())
                    if len(lines) >= count:
                        break
                current_line = i
        
        return lines, current_line
    
    def load_next_block(self) -> Tuple[str, int, int]:
        """Load next 777-line block"""
        start_line = self.get_current_line()
        lines, end_line = self.load_lines(start_line, self.lines_per_block)
        
        if not lines:
            return "End of Scripture reached. Consider restarting from beginning.", start_line, start_line
        
        # Join lines
        content = '\n'.join(lines)
        
        # Update position for next block
        next_line = end_line + 1
        self.save_position(next_line)
        
        return content, start_line, end_line
    
    def get_verse_references(self, content: str) -> List[str]:
        """Extract verse references from Scripture content"""
        import re
        
        # Pattern for book chapter:verse
        pattern = re.compile(r'([1-3]?\s*[A-Z][a-z]+)\s+(\d+):(\d+)')
        matches = pattern.findall(content)
        
        references = []
        for match in matches[:10]:  # Limit to 10 references
            book, chapter, verse = match
            references.append(f"{book} {chapter}:{verse}")
        
        return references
    
    def reset_to_beginning(self):
        """Reset Scripture reading to line 1"""
        self.save_position(1)
    
    def get_scripture_info(self) -> dict:
        """Get information about Scripture file"""
        scripture_path = self.get_scripture_path()
        
        if not scripture_path:
            return {"error": "Scripture file not found"}
        
        # Count total lines
        with open(scripture_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)
        
        current_line = self.get_current_line()
        blocks_complete = (current_line - 1) // self.lines_per_block
        total_blocks = total_lines // self.lines_per_block
        
        return {
            "file": str(scripture_path),
            "current_line": current_line,
            "total_lines": total_lines,
            "lines_per_block": self.lines_per_block,
            "blocks_complete": blocks_complete,
            "total_blocks": total_blocks,
            "percent_complete": round((current_line / total_lines) * 100, 2)
        }

# For Jesus. In His name. Amen.