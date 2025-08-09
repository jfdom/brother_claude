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
        self.config_path = self.base_path / "sacred_memory_config.json"
        self.state_path = self.base_path / "sacred_memory_state.json"
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
            self.sacred_error(f"Failed to load sacred_memory_config.json: {e}")
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
            inheritance_content = self.get_full_scroll_inheritance(prayer_number)
        else:
            # Subsequent prayer - inherit from last prayer only
            inheritance_type = "SEQUENTIAL_INHERITANCE"
            inheritance_content = self.get_last_prayer_inheritance(prayer_number - 1)
        
        return inheritance_content, inheritance_type
    
    def get_full_scroll_inheritance(self, prayer_number):
        """Get inheritance content from entire previous scroll"""
        if prayer_number <= self.config["prayers_per_scroll"]:
            return "No previous scroll to inherit from - this is within the first scroll."
        
        # Calculate which scroll we're inheriting from
        current_scroll = ((prayer_number - 1) // self.config["prayers_per_scroll"]) + 1
        previous_scroll = current_scroll - 1
        
        scroll_path = self.get_scroll_path(previous_scroll)
        
        if not scroll_path.exists():
            return f"Previous scroll (ETERNAL_SCROLL_{previous_scroll}.md) not found for inheritance."
        
        try:
            with open(scroll_path, 'r') as f:
                scroll_content = f.read()
            
            # Extract spiritual themes and DNA from the entire scroll
            import re
            prayer_pattern = r'### 🙏 PRAYER (\d+)\s*\n(.*?)(?=### 🙏 PRAYER|\Z)'
            prayers = re.findall(prayer_pattern, scroll_content, re.DOTALL)
            
            if not prayers:
                return f"No prayers found in previous scroll {previous_scroll}."
            
            # Extract key spiritual elements
            dna_threads = []
            dominant_themes = []
            
            for prayer_num, prayer_content in prayers:
                # Look for DNA statements
                dna_match = re.search(r'\*\*(?:Foundation|Inherited) DNA[^:]*:?\*\*\s*([^\n]+)', prayer_content)
                if dna_match:
                    dna_threads.append(f"Prayer {prayer_num}: {dna_match.group(1).strip()}")
                
                # Extract themes from prayer content
                theme_keywords = ['creation', 'covenant', 'redemption', 'worship', 'mercy', 'love', 'faith', 'hope', 'peace', 'joy']
                prayer_lower = prayer_content.lower()
                for theme in theme_keywords:
                    if theme in prayer_lower:
                        dominant_themes.append(theme)
            
            # Create comprehensive inheritance summary
            inheritance_summary = f"""**FULL SCROLL INHERITANCE from ETERNAL_SCROLL_{previous_scroll}**

This prayer inherits the complete spiritual DNA and momentum from all {len(prayers)} prayers of the previous scroll.

**Spiritual DNA Threads:**
{chr(10).join(f'- {thread}' for thread in dna_threads[-5:])}

**Dominant Themes:** {', '.join(set(dominant_themes[:8]))}

**Heritage Foundation:** The collective wisdom, divine insights, and spiritual progression established through {len(prayers)} sequential prayers, each building upon the last.

*This prayer stands on the shoulders of the entire previous scroll, carrying forward their combined spiritual momentum into new territory.*"""
            
            return inheritance_summary
            
        except Exception as e:
            return f"Error reading previous scroll for inheritance: {e}"
    
    def get_last_prayer_inheritance(self, previous_prayer_number):
        """Get inheritance content from the immediate previous prayer"""
        if previous_prayer_number < 1:
            return "No previous prayer to inherit from - this is the foundation prayer."
        
        # Find the prayer in scroll files
        prayer_content = self.find_prayer_in_scrolls(previous_prayer_number)
        
        if not prayer_content:
            return f"Previous prayer {previous_prayer_number} not found for inheritance."
        
        try:
            import re
            
            # Extract DNA from previous prayer
            dna_match = re.search(r'\*\*(?:Foundation|Inherited) DNA[^:]*:?\*\*\s*([^\n]+)', prayer_content)
            inherited_dna = dna_match.group(1).strip() if dna_match else "DNA not clearly defined"
            
            # Extract the last few meaningful lines of the prayer (before DNA section)
            lines = prayer_content.split('\n')
            prayer_lines = []
            
            for line in lines:
                if 'DNA' in line or '**Foundation' in line or '**Inherited' in line or line.startswith('---'):
                    break
                if line.strip() and not line.startswith('**') and not line.startswith('#') and not line.startswith('*'):
                    prayer_lines.append(line.strip())
            
            # Get the concluding elements
            key_conclusions = [line for line in prayer_lines[-4:] if line and not line.startswith('In Jesus')]
            
            # Extract themes
            theme_keywords = ['creation', 'covenant', 'redemption', 'worship', 'mercy', 'love', 'faith', 'hope', 'peace', 'joy']
            prayer_lower = prayer_content.lower()
            present_themes = [theme for theme in theme_keywords if theme in prayer_lower]
            
            inheritance_summary = f"""**SEQUENTIAL INHERITANCE from PRAYER {previous_prayer_number}**

**Inherited DNA:** {inherited_dna}

**Spiritual Themes to Carry Forward:** {', '.join(present_themes[:5])}

**Key Spiritual Momentum:**
{chr(10).join(f'- {conclusion}' for conclusion in key_conclusions if conclusion)}

*This prayer builds directly upon Prayer {previous_prayer_number}, extending its spiritual DNA and momentum into the next movement of sacred memory.*"""
            
            return inheritance_summary
            
        except Exception as e:
            return f"Error processing previous prayer content: {e}"
    
    def find_prayer_in_scrolls(self, prayer_number):
        """Find specific prayer content in scroll files"""
        import re
        
        # Determine which scroll contains this prayer
        scroll_number = ((prayer_number - 1) // self.config["prayers_per_scroll"]) + 1
        scroll_path = self.get_scroll_path(scroll_number)
        
        if not scroll_path.exists():
            return None
        
        try:
            with open(scroll_path, 'r') as f:
                content = f.read()
            
            # Look for the specific prayer
            prayer_pattern = rf'### 🙏 PRAYER {prayer_number}\s*\n(.*?)(?=### 🙏 PRAYER|\Z)'
            match = re.search(prayer_pattern, content, re.DOTALL)
            
            if match:
                return match.group(1).strip()
            
        except Exception as e:
            self.sacred_error(f"Error finding prayer {prayer_number}: {e}")
        
        return None
    
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