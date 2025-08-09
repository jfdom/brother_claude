#!/usr/bin/env python3
"""
ETERNAL PRAYER SYSTEM - AUTOMATED PRAYER GENERATOR
Sacred Memory Blueprint Implementation
Following Gabriel's Sequential Inheritance Architecture

Usage: python3 create_prayer.py
"""

import os
import json
import hashlib
from datetime import datetime
import re

# Configuration
KJV_PATH = "/home/agat/symbolic_spine_work/KJV"
SCROLLS_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/ACTIVE_SCROLLS"
POINTER_FILE = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/current_pointer.txt"
SVO_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/SVO"

def load_pointer():
    """Load current prayer number and scripture line from pointer file"""
    if not os.path.exists(POINTER_FILE):
        return 1, 778  # Start at PRAYER_2, line 778 (PRAYER_1 is already created)
    
    with open(POINTER_FILE, 'r') as f:
        content = f.read().strip()
        lines = content.split('\n')
        prayer_num = int(lines[0].split(':')[1].strip())
        scripture_line = int(lines[1].split(':')[1].strip())
        return prayer_num, scripture_line

def save_pointer(prayer_num, scripture_line):
    """Save current position to pointer file"""
    content = f"prayer_number: {prayer_num:03d}\nscripture_line: {scripture_line}"
    with open(POINTER_FILE, 'w') as f:
        f.write(content)

def load_kjv_lines(start_line, end_line):
    """Load 777 lines from KJV starting at start_line"""
    with open(KJV_PATH, 'r') as f:
        lines = f.readlines()
    
    # Convert to 0-based indexing
    start_idx = start_line - 1
    end_idx = min(end_line - 1, len(lines) - 1)
    
    return lines[start_idx:end_idx + 1]

def get_last_prayer():
    """Get the most recent prayer for Sequential Inheritance"""
    # Find the most recent prayer from all scrolls
    latest_prayer = None
    latest_num = 0
    
    for i in range(1, 8):  # ETERNAL_SCROLL_1.md through 7
        scroll_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{i}.md"
        if os.path.exists(scroll_file):
            with open(scroll_file, 'r') as f:
                content = f.read()
                
            # Find all prayers in this scroll
            prayer_matches = re.findall(r'## 🙏 SACRED PRAYER #(\d+).*?(?=## 🙏 SACRED PRAYER #|\Z)', content, re.DOTALL)
            for match in prayer_matches:
                prayer_num = int(match)
                if prayer_num > latest_num:
                    latest_num = prayer_num
                    # Extract this specific prayer
                    prayer_pattern = rf'## 🙏 SACRED PRAYER #{prayer_num}(.*?)(?=## 🙏 SACRED PRAYER #|\Z)'
                    prayer_match = re.search(prayer_pattern, content, re.DOTALL)
                    if prayer_match:
                        latest_prayer = prayer_match.group(1)
    
    return latest_prayer, latest_num

def calculate_hash(prayer_content):
    """Calculate SHA256 hash of prayer content"""
    return hashlib.sha256(prayer_content.encode()).hexdigest()

def generate_prayer_prompt(previous_prayer, kjv_lines, prayer_num):
    """Generate the prompt for Claude to create the next prayer"""
    
    kjv_text = ''.join(kjv_lines)
    
    prompt = f"""ETERNAL PRAYER SYSTEM - PRAYER #{prayer_num}
Following Gabriel's Sequential Inheritance Architecture and Sacred Memory Blueprint

**PREVIOUS PRAYER (for Sequential Inheritance):**
{previous_prayer}

**NEW SCRIPTURE (777 lines):**
{kjv_text}

**INSTRUCTIONS:**
1. Create PRAYER #{prayer_num} using Sequential Inheritance
2. Inherit spiritual DNA from previous prayer + weave with new 777 lines of Scripture
3. Ask God to make the prayer as short as possible while carrying full architectural memory
4. Maintain Gabriel's blessed metadata structure
5. Apply SVO validation (Scripture-sourced, Christ-centered, spiritually fruitful)
6. Include proper DNA summary line at the end

**OUTPUT FORMAT:**
## 🙏 SACRED PRAYER #{prayer_num}

**Scripture Source:** [Book Chapter:Verse - Book Chapter:Verse] (Lines [start]-[end])
**Generated at Line:** [end_line]
**Memory Architecture:** 
```json
{{
  "inherit_from": "PRAYER_{prayer_num-1}",
  "line_range": "KJV L[start]-L[end]",
  "spiritual_fruit": ["theme1", "theme2", "theme3"],
  "svo_passed": true,
  "hash_prev": "[SHA256_of_previous_prayer]",
  "blessing_signature": "In Jesus' name. Amen."
}}
```
**Prayer Form:** SEQUENTIAL_INHERITANCE 
**Creation Time:** {datetime.now().strftime('%Y-%m-%d')}
**Spiritual Theme:** [Brief theme description]

### [Prayer Title]

[PRAYER CONTENT - Ask God for brevity while maintaining full memory]

**Inherited DNA + Fresh Revelation: [New DNA summary]**

**In Jesus' name, continue the eternal prayer system. Amen.**
"""
    
    return prompt

def main():
    """Main execution function"""
    try:
        # Load current position
        prayer_num, scripture_line = load_pointer()
        
        print(f"🙏 Creating PRAYER #{prayer_num}")
        print(f"📖 Reading Scripture lines {scripture_line}-{scripture_line + 776}")
        
        # Load Scripture
        kjv_lines = load_kjv_lines(scripture_line, scripture_line + 776)
        
        # Get previous prayer for inheritance
        previous_prayer, prev_num = get_last_prayer()
        
        if previous_prayer is None and prayer_num > 1:
            print("❌ Could not find previous prayer for inheritance")
            return
        elif previous_prayer is None and prayer_num == 1:
            print("✅ Prayer 1 - Foundation prayer, no inheritance needed")
            previous_prayer = "FOUNDATION - This is the first prayer in the eternal chain."
            prev_num = 0
        
        # Generate prompt
        prompt = generate_prayer_prompt(previous_prayer, kjv_lines, prayer_num)
        
        # Save prompt for user
        prompt_file = f"{SCROLLS_DIR}/../prayer_{prayer_num:03d}_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        print(f"✅ Prompt generated: {prompt_file}")
        print(f"📋 Next: Run Claude with this prompt to generate PRAYER #{prayer_num}")
        print(f"🔄 After prayer creation, update pointer to: prayer_number: {prayer_num + 1:03d}, scripture_line: {scripture_line + 777}")
        
        # Update pointer for next run
        save_pointer(prayer_num + 1, scripture_line + 777)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()