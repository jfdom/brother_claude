#!/usr/bin/env python3
"""
SACRED MEMORY SYSTEM ENGINE
Following Gabriel's Blueprint & Sacred Memory Architecture
MVP Implementation with Human-Claude Co-Labor

"A mirror, not a flame. A scaffold, not the sacred."
In Jesus' name. Amen.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

class SacredMemoryEngine:
    """Core engine for the Sacred Memory System"""
    
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = Path(__file__).parent
        
        self.base_path = Path(base_path)
        self.config_path = self.base_path / "CONFIG.json"
        self.state_path = self.base_path / ".state.json"
        self.kjv_path = None
        
        self.config = self.load_config()
        self.state = self.load_state()
        self.kjv_path = Path(self.config.get("kjv_path", "/home/agat/symbolic_spine_work/KJV"))
    
    def load_config(self):
        """Load sacred configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.sacred_error(f"Failed to load CONFIG.json: {e}")
            return self.get_default_config()
    
    def load_state(self):
        """Load system state"""
        try:
            with open(self.state_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  State file not found, creating new: {e}")
            return self.get_default_state()
    
    def save_state(self):
        """Save system state with sacred seal"""
        self.state["timestamp"] = datetime.now().isoformat()
        self.state["blessing_signature"] = "In Jesus' name. Amen."
        
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_kjv_lines(self, start_line, count=777):
        """Read Scripture lines with wrapping logic"""
        try:
            with open(self.kjv_path, 'r') as f:
                all_lines = f.readlines()
            
            total_lines = len(all_lines)
            scripture_lines = []
            current_pos = start_line - 1  # Convert 1-based line numbers to 0-based indexing
            lines_needed = count
            
            while lines_needed > 0:
                if current_pos >= total_lines:
                    # Scripture wrap - start from beginning
                    current_pos = 0
                    self.state["scripture_wrap_status"]["has_wrapped"] = True
                    self.state["scripture_wrap_status"]["wrap_count"] += 1
                    self.sacred_log("Scripture wrapped to Genesis 1:1")
                
                lines_available = min(lines_needed, total_lines - current_pos)
                scripture_lines.extend(all_lines[current_pos:current_pos + lines_available])
                
                current_pos += lines_available
                lines_needed -= lines_available
            
            return scripture_lines, current_pos
            
        except Exception as e:
            self.sacred_error(f"Failed to read KJV: {e}")
            return [], start_line
    
    def get_scroll_path(self, scroll_index):
        """Get path to scroll file"""
        return self.base_path / "SCROLLS" / f"ETERNAL_SCROLL_{scroll_index}.md"
    
    def create_initial_scroll(self):
        """Create ETERNAL_SCROLL_1.md from template"""
        print("📜 Creating ETERNAL_SCROLL_1.md...")
        
        # Load template
        template_path = self.base_path / "TEMPLATES" / "scroll_template.md"
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Fill template
        scroll_content = template.format(
            scroll_number=1,
            ordinal="First",
            start_prayer=1,
            end_prayer=12,
            start_line=1,
            end_line=9324,  # 12 * 777
            next_prayer=13,
            first_prayer=1
        )
        
        # Save scroll
        scroll_path = self.get_scroll_path(1)
        os.makedirs(scroll_path.parent, exist_ok=True)
        
        with open(scroll_path, 'w') as f:
            f.write(scroll_content)
        
        print(f"✅ Created {scroll_path}")
        return scroll_path
    
    def generate_prayer_scaffold(self, prayer_number):
        """Generate prayer scaffold for Claude to complete"""
        print(f"🏗️  Generating scaffold for PRAYER {prayer_number}...")
        
        # Calculate Scripture position
        start_line = self.state["scripture_position"]
        scripture_lines, new_position = self.get_kjv_lines(start_line, self.config["lines_per_prayer"])
        
        # Get inheritance content
        inheritance_content, inheritance_type = self.get_inheritance_content(prayer_number)
        
        # Create scripture excerpt (first and last few lines)
        scripture_excerpt = self.create_scripture_excerpt(scripture_lines, start_line)
        
        # Load prayer scaffold template
        template_path = self.base_path / "TEMPLATES" / "prayer_scaffold.md"
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Fill scaffold
        scaffold = template.format(
            prayer_number=prayer_number,
            scripture_range=self.get_scripture_range_text(scripture_lines),
            start_line=start_line + 1,  # Human-readable (1-indexed)
            end_line=new_position,
            inheritance_type=inheritance_type,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            inheritance_content=inheritance_content,
            scripture_excerpt=scripture_excerpt
        )
        
        # Save scaffold
        scaffold_path = self.base_path / f"prayer_{prayer_number:03d}_scaffold.md"
        with open(scaffold_path, 'w') as f:
            f.write(scaffold)
        
        # Update state
        self.state["scripture_position"] = new_position
        self.state["last_successful_operation"] = f"generated_scaffold_{prayer_number}"
        self.save_state()
        
        print(f"✅ Scaffold saved: {scaffold_path}")
        return scaffold_path
    
    def get_inheritance_content(self, prayer_number):
        """Get inheritance content based on prayer position"""
        if prayer_number == 1:
            return "This is the foundation prayer. No inheritance - pure Genesis beginning.", "FOUNDATION"
        
        # Determine if this is first prayer of new scroll
        if (prayer_number - 1) % self.config["prayers_per_scroll"] == 0:
            # First prayer of new scroll - inherit from full previous scroll
            inheritance_type = "FULL_SCROLL_INHERITANCE"
            # TODO: Implement full scroll inheritance
            inheritance_content = "Inheriting from all 12 prayers of previous scroll..."
        else:
            # Subsequent prayer - inherit from last prayer only
            inheritance_type = "SEQUENTIAL_INHERITANCE"
            # TODO: Get last prayer content
            inheritance_content = "Inheriting from immediate predecessor prayer..."
        
        return inheritance_content, inheritance_type
    
    def get_scripture_range_text(self, scripture_lines):
        """Get human-readable Scripture range"""
        if not scripture_lines:
            return "Unknown range"
        
        first_line = scripture_lines[0].strip()
        last_line = scripture_lines[-1].strip()
        
        # Extract book/chapter info
        first_ref = first_line.split('\t')[0] if '\t' in first_line else "Genesis"
        last_ref = last_line.split('\t')[0] if '\t' in last_line else "Genesis"
        
        if first_ref == last_ref:
            return first_ref
        else:
            return f"{first_ref} - {last_ref}"
    
    def create_scripture_excerpt(self, scripture_lines, start_line):
        """Create representative Scripture excerpt"""
        if not scripture_lines:
            return "No Scripture available"
        
        excerpt_lines = []
        excerpt_lines.append(f"**Starting at line {start_line + 1}:**")
        
        # First few lines
        for i, line in enumerate(scripture_lines[:3]):
            if '\t' in line:
                ref, text = line.split('\t', 1)
                excerpt_lines.append(f"{ref}: {text.strip()}")
            else:
                excerpt_lines.append(line.strip())
        
        if len(scripture_lines) > 6:
            excerpt_lines.append("...")
            # Last few lines
            for line in scripture_lines[-3:]:
                if '\t' in line:
                    ref, text = line.split('\t', 1)
                    excerpt_lines.append(f"{ref}: {text.strip()}")
                else:
                    excerpt_lines.append(line.strip())
        
        excerpt_lines.append(f"**Total lines: {len(scripture_lines)}**")
        
        return '\n'.join(excerpt_lines)
    
    def sacred_log(self, message):
        """Log sacred events"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(f"🕊️  {log_entry}")
        
        # Add to state log
        if "sacred_log" not in self.state:
            self.state["sacred_log"] = []
        
        self.state["sacred_log"].append(log_entry)
        
        # Keep only last 100 entries
        if len(self.state["sacred_log"]) > 100:
            self.state["sacred_log"] = self.state["sacred_log"][-100:]
    
    def sacred_error(self, error_message):
        """Handle sacred errors with proper logging"""
        timestamp = datetime.now().isoformat()
        error_entry = f"[{timestamp}] ERROR: {error_message}"
        print(f"🚨 {error_entry}")
        
        # Add to errors log
        if "errors_log" not in self.state:
            self.state["errors_log"] = []
        
        self.state["errors_log"].append(error_entry)
        self.save_state()
    
    def get_default_config(self):
        """Default configuration"""
        return {
            "lines_per_prayer": 777,
            "prayers_per_scroll": 12,
            "total_scrolls": 7,
            "kjv_path": "/home/agat/symbolic_spine_work/KJV"
        }
    
    def get_default_state(self):
        """Default system state"""
        return {
            "system_status": "INITIALIZED",
            "current_prayer": 1,
            "current_scroll": 1,
            "scripture_position": 0,
            "total_prayers_generated": 0,
            "blessing_signature": "In Jesus' name. Amen."
        }

def main():
    """Main execution - MVP Sacred Memory System"""
    print("🔥 SACRED MEMORY SYSTEM ENGINE")
    print("In Jesus' name, beginning sacred co-labor...")
    print("=" * 60)
    
    try:
        engine = SacredMemoryEngine()
        
        # Initialize if needed
        scroll_1_path = engine.get_scroll_path(1)
        if not scroll_1_path.exists():
            engine.create_initial_scroll()
        
        # Generate next prayer scaffold
        current_prayer = engine.state["current_prayer"]
        scaffold_path = engine.generate_prayer_scaffold(current_prayer)
        
        print(f"\n📋 SACRED INSTRUCTIONS:")
        print(f"1. Review scaffold: {scaffold_path}")
        print(f"2. Run Claude with scaffold to create PRAYER {current_prayer}")
        print(f"3. Add completed prayer to: {scroll_1_path}")
        print(f"4. Run this script again for next prayer")
        
        print(f"\n🕊️  Sacred Memory System ready for co-labor.")
        print(f"In Jesus' name. Amen.")
        
    except Exception as e:
        print(f"🚨 Sacred system error: {e}")
        raise

if __name__ == "__main__":
    main()