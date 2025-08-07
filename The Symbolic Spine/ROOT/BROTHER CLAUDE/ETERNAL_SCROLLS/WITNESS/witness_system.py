#!/usr/bin/env python3
"""
WITNESS SYSTEM - DIVINE VERIFICATION AND INTEGRITY
Following Sacred Memory Blueprint Phase 4+ requirements

Tracks and verifies:
- Prayer integrity through hash verification
- Sequential inheritance chains
- Scripture coverage completeness
- Scroll rotation integrity
- Divine milestone confirmations
"""

import os
import json
import hashlib
import re
from datetime import datetime

SCROLLS_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/ACTIVE_SCROLLS"
WITNESS_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/WITNESS"
ARCHIVE_DIR = "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/ETERNAL_SCROLLS/ARCHIVE"

class EternalWitness:
    """Divine verification and integrity witness system"""
    
    def __init__(self):
        self.witness_log = []
        self.integrity_issues = []
        self.milestones = []
    
    def verify_hash_chain(self):
        """Verify the hash chain integrity across all prayers"""
        print("🔍 Verifying hash chain integrity...")
        
        prayers = self._get_all_prayers()
        hash_issues = []
        
        for i, prayer in enumerate(prayers[1:], 1):  # Skip first prayer (foundation)
            prev_prayer = prayers[i-1]
            
            # Calculate actual hash of previous prayer
            prev_content = self._extract_prayer_content(prev_prayer)
            actual_hash = hashlib.sha256(prev_content.encode()).hexdigest()
            
            # Get claimed hash from current prayer
            claimed_hash = self._extract_hash_from_prayer(prayer)
            
            if actual_hash != claimed_hash:
                issue = {
                    "type": "hash_mismatch",
                    "prayer_num": i + 1,
                    "claimed_hash": claimed_hash,
                    "actual_hash": actual_hash,
                    "severity": "HIGH"
                }
                hash_issues.append(issue)
                self.integrity_issues.append(issue)
        
        return hash_issues
    
    def verify_sequential_inheritance(self):
        """Verify that each prayer properly inherits from immediate predecessor"""
        print("🧬 Verifying sequential inheritance...")
        
        prayers = self._get_all_prayers()
        inheritance_issues = []
        
        for i, prayer in enumerate(prayers[1:], 1):
            prev_prayer = prayers[i-1]
            
            # Check if prayer mentions inheritance
            has_inheritance = self._check_inheritance_markers(prayer)
            
            if not has_inheritance:
                issue = {
                    "type": "missing_inheritance",
                    "prayer_num": i + 1,
                    "description": "Prayer lacks clear inheritance from predecessor",
                    "severity": "MEDIUM"
                }
                inheritance_issues.append(issue)
                self.integrity_issues.append(issue)
        
        return inheritance_issues
    
    def verify_scripture_coverage(self):
        """Verify complete Scripture coverage with no gaps"""
        print("📖 Verifying Scripture coverage...")
        
        prayers = self._get_all_prayers()
        coverage_issues = []
        expected_line = 1
        
        for i, prayer in enumerate(prayers):
            line_range = self._extract_line_range(prayer)
            if line_range:
                start_line, end_line = line_range
                
                if start_line != expected_line:
                    issue = {
                        "type": "scripture_gap",
                        "prayer_num": i + 1,
                        "expected_start": expected_line,
                        "actual_start": start_line,
                        "gap_size": start_line - expected_line,
                        "severity": "HIGH"
                    }
                    coverage_issues.append(issue)
                    self.integrity_issues.append(issue)
                
                expected_line = end_line + 1
        
        return coverage_issues
    
    def record_milestone(self, milestone_type, data):
        """Record divine milestone confirmations"""
        milestone = {
            "timestamp": datetime.now().isoformat(),
            "type": milestone_type,
            "data": data,
            "witness_signature": self._generate_witness_signature()
        }
        
        self.milestones.append(milestone)
        
        # Save milestone to permanent record
        milestone_file = f"{WITNESS_DIR}/milestone_{len(self.milestones):03d}_{milestone_type}.json"
        with open(milestone_file, 'w') as f:
            json.dump(milestone, f, indent=2)
        
        print(f"📍 Milestone recorded: {milestone_type}")
    
    def generate_integrity_report(self):
        """Generate comprehensive integrity report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_status": "OPERATIONAL" if not self.integrity_issues else "ISSUES_DETECTED",
            "total_prayers": len(self._get_all_prayers()),
            "integrity_checks": {
                "hash_chain": len([i for i in self.integrity_issues if i["type"] == "hash_mismatch"]),
                "inheritance": len([i for i in self.integrity_issues if i["type"] == "missing_inheritance"]),
                "scripture_coverage": len([i for i in self.integrity_issues if i["type"] == "scripture_gap"])
            },
            "issues": self.integrity_issues,
            "milestones": len(self.milestones),
            "divine_confirmations": self._count_divine_confirmations()
        }
        
        return report
    
    def _get_all_prayers(self):
        """Get all prayers from all active scrolls in order"""
        prayers = []
        
        for i in range(1, 8):  # ETERNAL_SCROLL_1 through 7
            scroll_file = f"{SCROLLS_DIR}/ETERNAL_SCROLL_{i}.md"
            if os.path.exists(scroll_file):
                with open(scroll_file, 'r') as f:
                    content = f.read()
                
                # Extract prayers from this scroll
                prayer_pattern = r'## 🙏 SACRED PRAYER #(\d+).*?(?=## 🙏 SACRED PRAYER #|\Z)'
                matches = re.findall(prayer_pattern, content, re.DOTALL)
                
                for match in matches:
                    prayers.append(match)
        
        # Sort by prayer number
        prayers.sort(key=lambda x: int(re.search(r'PRAYER #(\d+)', x).group(1)))
        
        return prayers
    
    def _extract_prayer_content(self, prayer_text):
        """Extract the actual prayer content for hashing"""
        # Remove metadata and extract just the prayer text
        lines = prayer_text.split('\n')
        prayer_lines = []
        in_prayer = False
        
        for line in lines:
            if line.startswith('### '):  # Prayer title
                in_prayer = True
                continue
            elif line.startswith('**') and 'DNA' in line:  # End of prayer
                break
            elif in_prayer and line.strip():
                prayer_lines.append(line.strip())
        
        return '\n'.join(prayer_lines)
    
    def _extract_hash_from_prayer(self, prayer_text):
        """Extract the claimed hash from prayer metadata"""
        hash_match = re.search(r'"hash_prev":\s*"([^"]+)"', prayer_text)
        return hash_match.group(1) if hash_match else None
    
    def _extract_line_range(self, prayer_text):
        """Extract Scripture line range from prayer"""
        range_match = re.search(r'"line_range":\s*"KJV L(\d+)-L(\d+)"', prayer_text)
        if range_match:
            return int(range_match.group(1)), int(range_match.group(2))
        return None
    
    def _check_inheritance_markers(self, prayer_text):
        """Check if prayer has clear inheritance markers"""
        inheritance_patterns = [
            r'inherit_from',
            r'Inherited.*DNA',
            r'DNA.*\+.*:',
            r'carries forward'
        ]
        
        for pattern in inheritance_patterns:
            if re.search(pattern, prayer_text, re.IGNORECASE):
                return True
        
        return False
    
    def _generate_witness_signature(self):
        """Generate cryptographic witness signature"""
        timestamp = datetime.now().isoformat()
        content = f"ETERNAL_WITNESS_{timestamp}_IN_JESUS_NAME"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _count_divine_confirmations(self):
        """Count divine confirmation milestones"""
        return len([m for m in self.milestones if m["type"].startswith("divine_")])

def run_full_verification():
    """Run complete verification suite"""
    print("🔥 ETERNAL WITNESS SYSTEM - FULL VERIFICATION")
    print("=" * 60)
    
    witness = EternalWitness()
    
    # Run all verifications
    hash_issues = witness.verify_hash_chain()
    inheritance_issues = witness.verify_sequential_inheritance()
    coverage_issues = witness.verify_scripture_coverage()
    
    # Generate report
    report = witness.generate_integrity_report()
    
    # Print summary
    print(f"\n📊 VERIFICATION SUMMARY")
    print(f"System Status: {report['system_status']}")
    print(f"Total Prayers: {report['total_prayers']}")
    print(f"Hash Chain Issues: {report['integrity_checks']['hash_chain']}")
    print(f"Inheritance Issues: {report['integrity_checks']['inheritance']}")
    print(f"Scripture Coverage Issues: {report['integrity_checks']['scripture_coverage']}")
    print(f"Divine Milestones: {report['milestones']}")
    
    # Save report
    report_file = f"{WITNESS_DIR}/integrity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved: {report_file}")
    
    if report['system_status'] == "OPERATIONAL":
        print("✅ ALL SYSTEMS OPERATIONAL - GLORY TO GOD")
    else:
        print("⚠️  ISSUES DETECTED - REQUIRES ATTENTION")
        for issue in witness.integrity_issues:
            print(f"  - {issue['type']}: {issue.get('description', 'See details')}")
    
    return report

if __name__ == "__main__":
    run_full_verification()