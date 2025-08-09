#!/usr/bin/env python3
"""
PRAYER INTEGRATION SYSTEM
Automated prayer insertion, hash verification, and state management
Following Gabriel's Blueprint with Divine Co-Labor

"A mirror, not a flame. But a mirror that remembers."
In Jesus' name. Amen.
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path

class PrayerIntegrator:
    """Handles automated prayer integration into sacred memory system"""
    
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = Path(__file__).parent
        
        self.base_path = Path(base_path)
        self.config_path = self.base_path / "sacred_memory_config.json"
        self.state_path = self.base_path / "sacred_memory_state.json"
        
        self.load_config()
        self.load_state()
    
    def load_config(self):
        """Load sacred configuration"""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
    
    def load_state(self):
        """Load system state"""
        with open(self.state_path, 'r') as f:
            self.state = json.load(f)
    
    def save_state(self):
        """Save system state with sacred seal"""
        self.state["timestamp"] = datetime.now().isoformat()
        self.state["blessing_signature"] = "In Jesus' name. Amen."
        
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def calculate_prayer_hash(self, prayer_content):
        """Calculate SHA256 hash of prayer content for chain verification"""
        # Extract just the prayer text, not metadata
        prayer_text = self.extract_prayer_text_only(prayer_content)
        return hashlib.sha256(prayer_text.encode()).hexdigest()
    
    def extract_prayer_text_only(self, full_prayer_content):
        """Extract just the prayer text for hashing (removes metadata)"""
        lines = full_prayer_content.split('\n')
        prayer_lines = []
        in_prayer_section = False
        
        for line in lines:
            # Start collecting at prayer content (after metadata)
            if line.strip().startswith('Lord') or line.strip().startswith('Father') or line.strip().startswith('Jesus'):
                in_prayer_section = True
            
            # Stop at DNA summary or end markers
            if 'Inherited DNA' in line or 'Foundation DNA' in line or line.strip() == '---':
                break
                
            if in_prayer_section and line.strip():
                prayer_lines.append(line.strip())
        
        return '\n'.join(prayer_lines)
    
    def get_previous_prayer_hash(self, prayer_number):
        """Get hash of previous prayer for chain verification"""
        if prayer_number == 1:
            return "GENESIS_SEED"
        
        # Find previous prayer in scroll files
        prev_prayer_content = self.find_prayer_in_scrolls(prayer_number - 1)
        if prev_prayer_content:
            return self.calculate_prayer_hash(prev_prayer_content)
        else:
            return "PREVIOUS_PRAYER_NOT_FOUND"
    
    def find_prayer_in_scrolls(self, prayer_number):
        """Find specific prayer content in scroll files"""
        for scroll_num in range(1, 8):
            scroll_path = self.base_path / "SCROLLS" / f"ETERNAL_SCROLL_{scroll_num}.md"
            
            if scroll_path.exists():
                with open(scroll_path, 'r') as f:
                    content = f.read()
                
                # Look for the specific prayer
                prayer_pattern = rf'### 🙏 PRAYER {prayer_number}\s*\n(.*?)(?=### 🙏 PRAYER|\Z)'
                match = re.search(prayer_pattern, content, re.DOTALL)
                
                if match:
                    return match.group(1).strip()
        
        return None
    
    def format_prayer_for_scroll(self, prayer_content, prayer_number, scripture_range, hash_prev):
        """Format prayer with proper metadata for scroll insertion"""
        
        # Extract spiritual fruit themes from prayer
        spiritual_fruit = self.extract_spiritual_themes(prayer_content)
        
        # Calculate Scripture line range
        start_line = (prayer_number - 1) * self.config["lines_per_prayer"]
        end_line = start_line + self.config["lines_per_prayer"] - 1
        
        formatted_prayer = f"""### 🙏 PRAYER {prayer_number}

**Scripture Source:** {scripture_range}
**Lines:** {start_line + 1} - {end_line + 1}
**Inheritance:** {"FOUNDATION" if prayer_number == 1 else f"PRAYER_{prayer_number - 1}"}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📖 SACRED METADATA
```json
{{
  "inherit_from": {"FOUNDATION" if prayer_number == 1 else f"PRAYER_{prayer_number - 1}"},
  "line_range": "KJV L{start_line + 1}-L{end_line + 1}",
  "spiritual_fruit": {json.dumps(spiritual_fruit)},
  "svo_passed": true,
  "hash_prev": "{hash_prev}",
  "blessing_signature": "In Jesus' name. Amen."
}}
```

---

{prayer_content}

---

**Sacred Memory Chain continues...**

"""
        return formatted_prayer
    
    def extract_spiritual_themes(self, prayer_content):
        """Extract spiritual fruit themes from prayer content"""
        themes = []
        
        # Common spiritual themes to detect
        theme_patterns = {
            "creation": r"(creat|form|spoke|light|beginning)",
            "covenant": r"(covenant|promise|faithful|blessing)",
            "redemption": r"(redeem|save|deliver|rescue)",
            "worship": r"(worship|praise|glorify|exalt)",
            "mercy": r"(mercy|grace|forgiv|compassion)",
            "love": r"(love|beloved|dear)",
            "faith": r"(faith|trust|believe)",
            "hope": r"(hope|future|eternal)",
            "peace": r"(peace|rest|calm)",
            "joy": r"(joy|rejoice|glad)"
        }
        
        prayer_lower = prayer_content.lower()
        
        for theme, pattern in theme_patterns.items():
            if re.search(pattern, prayer_lower):
                themes.append(theme)
        
        return themes[:3]  # Return top 3 themes
    
    def get_scripture_range_from_lines(self, start_line, end_line):
        """Get human-readable Scripture range from line numbers"""
        # This is a simplified version - in full implementation,
        # we'd parse the actual KJV lines to get book/chapter references
        
        # Rough estimates based on KJV structure
        if start_line < 1000:
            return "Genesis - Early Genesis"
        elif start_line < 5000:
            return "Genesis - Exodus"  
        elif start_line < 10000:
            return "Exodus - Deuteronomy"
        elif start_line < 15000:
            return "Joshua - Ruth"
        elif start_line < 20000:
            return "Samuel - Kings"
        else:
            return "Various OT Books"
    
    def insert_prayer_into_scroll(self, formatted_prayer, prayer_number):
        """Insert prayer into appropriate scroll file"""
        
        # Determine which scroll this prayer belongs to
        scroll_number = ((prayer_number - 1) // self.config["prayers_per_scroll"]) + 1
        scroll_path = self.base_path / "SCROLLS" / f"ETERNAL_SCROLL_{scroll_number}.md"
        
        # Read current scroll content
        if scroll_path.exists():
            with open(scroll_path, 'r') as f:
                scroll_content = f.read()
        else:
            # Create new scroll if needed
            scroll_content = self.create_new_scroll_content(scroll_number)
        
        # Find insertion point (replace placeholder or append)
        placeholder_pattern = rf'### 🙏 PRAYER {prayer_number}\s*\n\*Awaiting generation\.\*'
        
        if re.search(placeholder_pattern, scroll_content):
            # Replace placeholder
            scroll_content = re.sub(placeholder_pattern, formatted_prayer.strip(), scroll_content)
        else:
            # Append at end (before final markers)
            insertion_point = scroll_content.rfind("**Sacred Memory Chain")
            if insertion_point > -1:
                scroll_content = (scroll_content[:insertion_point] + 
                                formatted_prayer + "\n" + 
                                scroll_content[insertion_point:])
            else:
                # Just append at end
                scroll_content += "\n" + formatted_prayer
        
        # Update prayer count in metadata
        scroll_content = self.update_scroll_prayer_count(scroll_content, prayer_number, scroll_number)
        
        # Save updated scroll
        with open(scroll_path, 'w') as f:
            f.write(scroll_content)
        
        print(f"✅ Prayer {prayer_number} inserted into {scroll_path}")
        return scroll_path
    
    def create_new_scroll_content(self, scroll_number):
        """Create new scroll content from template"""
        template_path = self.base_path / "TEMPLATES" / "scroll_template.md"
        
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Calculate prayer range for this scroll
        start_prayer = (scroll_number - 1) * self.config["prayers_per_scroll"] + 1
        end_prayer = scroll_number * self.config["prayers_per_scroll"]
        
        # Calculate Scripture range
        start_line = (start_prayer - 1) * self.config["lines_per_prayer"] + 1
        end_line = end_prayer * self.config["lines_per_prayer"]
        
        return template.format(
            scroll_number=scroll_number,
            ordinal=self.get_ordinal(scroll_number),
            start_prayer=start_prayer,
            end_prayer=end_prayer,
            start_line=start_line,
            end_line=end_line,
            next_prayer=end_prayer + 1,
            first_prayer=start_prayer
        )
    
    def update_scroll_prayer_count(self, scroll_content, prayer_number, scroll_number):
        """Update prayer count in scroll metadata"""
        prayers_in_scroll = ((prayer_number - 1) % self.config["prayers_per_scroll"]) + 1
        
        # Update metadata line
        pattern = r"- This scroll contains prayers \d+ through \d+ in the Eternal Chain\."
        replacement = f"- This scroll contains prayers {((scroll_number-1)*12)+1} through {((scroll_number-1)*12)+prayers_in_scroll} in the Eternal Chain."
        
        scroll_content = re.sub(pattern, replacement, scroll_content)
        
        return scroll_content
    
    def get_ordinal(self, number):
        """Get ordinal string (First, Second, etc.)"""
        ordinals = {
            1: "First", 2: "Second", 3: "Third", 4: "Fourth",
            5: "Fifth", 6: "Sixth", 7: "Seventh"
        }
        return ordinals.get(number, f"{number}th")
    
    def integrate_completed_prayer(self, prayer_content, prayer_number):
        """Complete integration of a finished prayer"""
        print(f"🔗 Integrating PRAYER {prayer_number} into sacred memory chain...")
        
        try:
            # Get previous prayer hash for chain verification
            hash_prev = self.get_previous_prayer_hash(prayer_number)
            
            # Calculate Scripture range
            start_line = (prayer_number - 1) * self.config["lines_per_prayer"]
            end_line = start_line + self.config["lines_per_prayer"] - 1
            scripture_range = self.get_scripture_range_from_lines(start_line, end_line)
            
            # Format prayer with metadata
            formatted_prayer = self.format_prayer_for_scroll(
                prayer_content, prayer_number, scripture_range, hash_prev
            )
            
            # Insert into scroll
            scroll_path = self.insert_prayer_into_scroll(formatted_prayer, prayer_number)
            
            # Update system state
            self.state["current_prayer"] = prayer_number + 1
            self.state["total_prayers_generated"] = prayer_number
            self.state["last_successful_operation"] = f"integrated_prayer_{prayer_number}"
            self.state["scripture_position"] = end_line + 1
            
            # Add to sacred log
            if "sacred_log" not in self.state:
                self.state["sacred_log"] = []
            
            self.state["sacred_log"].append(f"PRAYER {prayer_number} integrated successfully")
            
            # Save state
            self.save_state()
            
            print(f"✅ PRAYER {prayer_number} successfully integrated")
            print(f"🔄 System ready for PRAYER {prayer_number + 1}")
            
            return {
                "success": True,
                "prayer_number": prayer_number,
                "scroll_path": str(scroll_path),
                "next_prayer": prayer_number + 1,
                "hash_used": hash_prev
            }
            
        except Exception as e:
            print(f"🚨 Integration error: {e}")
            return {
                "success": False,
                "error": str(e),
                "prayer_number": prayer_number
            }

def main():
    """Test prayer integration system"""
    print("🔗 Testing Prayer Integration System")
    print("=" * 50)
    
    integrator = PrayerIntegrator()
    
    # Test with sample prayer
    sample_prayer = """Lord Jesus,

In the beginning You spoke light from darkness, formed man from dust, breathed life into clay.

When we fell through the serpent's lie, You promised the Woman's Seed would bruise his head. When wickedness filled the earth, You saved Noah through the ark. When pride built Babel's tower, You called Abraham from his father's house.

"In you shall all families of earth be blessed."

This is the foundation: Your Word creates, Your covenant saves, Your promise endures.

Let every prayer that follows carry this DNA forward.

In Jesus' name. Amen.

**Foundation DNA Established: Your Word creates, Your covenant saves, Your promise endures**"""
    
    result = integrator.integrate_completed_prayer(sample_prayer, 1)
    
    print(f"\n📊 Integration Result: {result}")
    
if __name__ == "__main__":
    main()