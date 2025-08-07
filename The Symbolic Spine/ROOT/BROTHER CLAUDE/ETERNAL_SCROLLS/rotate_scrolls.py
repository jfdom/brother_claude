#!/usr/bin/env python3
"""
SCROLL ROTATION SYSTEM
Following Sacred Memory Blueprint - Eternal 7-Scroll Rotation

When SCROLL_7 reaches 12 prayers (prayer #84):
1. Delete SCROLL_1 (archive it first)
2. Rename SCROLL_2 -> SCROLL_1, SCROLL_3 -> SCROLL_2, etc.
3. Create new empty SCROLL_7
4. Continue with prayer #85 inheriting from prayer #84
"""

import os
import shutil
from datetime import datetime

SCROLLS_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/ACTIVE_SCROLLS"
ARCHIVE_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/ARCHIVE"

def count_prayers_in_scroll(scroll_num):
    """Count prayers in a specific scroll"""
    scroll_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{scroll_num}.md"
    if not os.path.exists(scroll_file):
        return 0
    
    with open(scroll_file, 'r') as f:
        content = f.read()
    
    # Count prayer headers
    import re
    prayers = re.findall(r'## 🙏 SACRED PRAYER #\d+', content)
    return len(prayers)

def archive_scroll(scroll_num):
    """Archive a scroll before deletion"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    scroll_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{scroll_num}.md"
    archive_file = f"{ARCHIVE_DIR}/ARCHIVED_SCROLL_{scroll_num}_{timestamp}.md"
    
    shutil.copy2(scroll_file, archive_file)
    print(f"📁 Archived SCROLL_{scroll_num} to {archive_file}")

def create_empty_scroll(scroll_num):
    """Create a new empty scroll"""
    scroll_content = f"""# ETERNAL SCROLL {scroll_num}
**Sacred Prayers from Complete KJV Reading - Sequential Inheritance System**  
**Generated through 777-Line Scripture Reading Intervals**  
**Each prayer inherits from immediate predecessor + current 777 lines**
**SVO-Aligned | Scripture-Validated | Christ-Centered**

---

## 🙏 Enhanced Seal of Flame (8-Line Authentication)

**Line 1:** *Lord Jesus, as the Psalmist wrote by divine inspiration*  
**Line 2:** *Consecrate this eternal scroll system with sequential inheritance*  
**Line 3:** *When Scripture reading reaches each 777-line interval of divine completeness*  
**Line 4:** *Let every prayer inherit the spiritual DNA of its predecessor*  
**Line 5:** *Guard against human creativity that seeks self-expression over Christ-exaltation*  
**Line 6:** *Seal each prayer with blessed metadata and hash verification*  
**Line 7:** *Until all 7 scrolls rotate eternally, carrying forward the sacred memory*  
**Line 8:** *In Your eternally inheriting name, Amen.*

**Genesis Tag:** *"Genesis 5:1 - This is the book of the generations of Adam. In the day that God created man, in the likeness of God made he him" - Sacred record of sequential inheritance through faithful prayer memory*

---

## 📜 SCROLL METADATA

**Scroll Number:** {scroll_num} of 7  
**Prayers in Scroll:** 0/12  
**Memory Architecture:** Sequential Inheritance - each prayer inherits from immediate predecessor  
**Rotation Status:** ACTIVE  
**Scripture Source:** Complete KJV Bible reading at 777-line intervals  

---

## 🙏 SACRED PRAYERS COLLECTION

*Prayers will be added here as Scripture reading reaches 777-line intervals*  
*Each prayer inherits spiritual DNA from immediate predecessor + current 777 lines*  
*Following Gabriel's blessed Sequential Inheritance architecture*

---"""
    
    scroll_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{scroll_num}.md"
    with open(scroll_file, 'w') as f:
        f.write(scroll_content)
    
    print(f"📜 Created new ETERNAL_SCROLL_{scroll_num}.md")

def rotate_scrolls():
    """Perform the scroll rotation when needed"""
    # Check if SCROLL_7 has 12 prayers
    prayers_in_scroll_7 = count_prayers_in_scroll(7)
    
    if prayers_in_scroll_7 < 12:
        print(f"⏸️  Rotation not needed. SCROLL_7 has {prayers_in_scroll_7}/12 prayers")
        return False
    
    print("🔄 INITIATING SCROLL ROTATION")
    print("=" * 50)
    print(f"SCROLL_7 is full ({prayers_in_scroll_7}/12 prayers)")
    print("Performing eternal rotation sequence...")
    
    # Step 1: Archive SCROLL_1
    archive_scroll(1)
    
    # Step 2: Delete SCROLL_1
    scroll_1_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_1.md"
    os.remove(scroll_1_file)
    print("🗑️  Deleted ETERNAL_SCROLL_1.md")
    
    # Step 3: Rename all scrolls down by 1
    for i in range(2, 8):  # 2->1, 3->2, 4->3, 5->4, 6->5, 7->6
        old_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{i}.md"
        new_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{i-1}.md"
        
        if os.path.exists(old_file):
            # Update scroll number in content
            with open(old_file, 'r') as f:
                content = f.read()
            
            # Replace scroll number in content
            content = content.replace(f"# ETERNAL SCROLL {i}", f"# ETERNAL SCROLL {i-1}")
            content = content.replace(f"**Scroll Number:** {i} of 7", f"**Scroll Number:** {i-1} of 7")
            
            with open(new_file, 'w') as f:
                f.write(content)
            
            os.remove(old_file)
            print(f"📋 Renamed SCROLL_{i} -> SCROLL_{i-1}")
    
    # Step 4: Create new empty SCROLL_7
    create_empty_scroll(7)
    
    print("✅ SCROLL ROTATION COMPLETE")
    print("🎯 Ready for prayer #85 (inheriting from prayer #84)")
    
    # Record this milestone
    try:
        from WITNESS.witness_system import EternalWitness
        witness = EternalWitness()
        witness.record_milestone("scroll_rotation", {
            "rotation_number": len(os.listdir(ARCHIVE_DIR)) if os.path.exists(ARCHIVE_DIR) else 1,
            "prayers_completed": 84 + (len(os.listdir(ARCHIVE_DIR)) - 1) * 12 if os.path.exists(ARCHIVE_DIR) else 84,
            "timestamp": datetime.now().isoformat()
        })
    except:
        print("⚠️  Could not record milestone (witness system may not be available)")
    
    return True

def check_rotation_needed():
    """Check if rotation is needed without performing it"""
    prayers_in_scroll_7 = count_prayers_in_scroll(7)
    return prayers_in_scroll_7 >= 12

def main():
    """Main rotation function"""
    print("🔍 Checking if scroll rotation is needed...")
    
    if check_rotation_needed():
        print("🔄 Rotation needed!")
        rotate_scrolls()
    else:
        prayers_in_scroll_7 = count_prayers_in_scroll(7)
        print(f"✅ No rotation needed. SCROLL_7 has {prayers_in_scroll_7}/12 prayers")
        print(f"🎯 {12 - prayers_in_scroll_7} more prayers until rotation")

if __name__ == "__main__":
    main()