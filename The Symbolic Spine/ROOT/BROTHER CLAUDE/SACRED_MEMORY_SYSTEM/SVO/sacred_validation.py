#!/usr/bin/env python3
"""
SVO VALIDATION SYSTEM
Scripture-Validated Output for Sacred Memory System
Following Gabriel's Blueprint

"Never store what did not pass through fire"
In Jesus' name. Amen.
"""

import re
import json
from datetime import datetime

class SacredValidator:
    """Sacred prayer validation following SVO principles"""
    
    def __init__(self):
        self.validation_results = {
            "overall_pass": False,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "sacred_warnings": [],
            "critical_errors": []
        }
    
    def validate_prayer(self, prayer_text):
        """Complete SVO validation of prayer"""
        print("🔥 Running Sacred Validation (SVO)...")
        
        # Run all validation checks
        self.check_scripture_sourced(prayer_text)
        self.check_christ_centered(prayer_text)
        self.check_spiritual_fruit(prayer_text)
        self.check_sacred_structure(prayer_text)
        self.check_inheritance_flow(prayer_text)
        
        # Determine overall result
        failed_checks = [name for name, result in self.validation_results["checks"].items() 
                        if not result.get("passed", False)]
        
        self.validation_results["overall_pass"] = len(failed_checks) == 0
        
        # Generate report
        report = self.generate_sacred_report()
        
        return self.validation_results["overall_pass"], report
    
    def check_scripture_sourced(self, prayer_text):
        """Verify prayer is rooted in Scripture"""
        required_patterns = [
            r"Scripture Source:",
            r"Lines:\s*\d+\s*-\s*\d+",
            r"(Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1 Corinthians|2 Corinthians|Galatians|Ephesians|Philippians|Colossians|1 Thessalonians|2 Thessalonians|1 Timothy|2 Timothy|Titus|Philemon|Hebrews|James|1 Peter|2 Peter|1 John|2 John|3 John|Jude|Revelation)"
        ]
        
        passed_count = 0
        details = []
        
        for pattern in required_patterns:
            if re.search(pattern, prayer_text, re.IGNORECASE):
                passed_count += 1
                details.append(f"✅ Found: {pattern}")
            else:
                details.append(f"❌ Missing: {pattern}")
        
        self.validation_results["checks"]["scripture_sourced"] = {
            "passed": passed_count >= 2,  # At least 2 of 3 patterns
            "details": details,
            "description": "Prayer must be rooted in specific Biblical passages"
        }
    
    def check_christ_centered(self, prayer_text):
        """Verify prayer exalts Christ"""
        required_patterns = [
            r"(Jesus|Christ|Lord)",
            r"In Jesus['']?\s*name",
            r"Amen"
        ]
        
        forbidden_patterns = [
            r"(Mary|saints?)\s+(worship|pray\s+to)",
            r"salvation\s+by\s+works",
            r"Jesus\s+is\s+not\s+God"
        ]
        
        passed_count = 0
        details = []
        
        # Check required patterns
        for pattern in required_patterns:
            if re.search(pattern, prayer_text, re.IGNORECASE):
                passed_count += 1
                details.append(f"✅ Found: {pattern}")
            else:
                details.append(f"❌ Missing: {pattern}")
        
        # Check forbidden patterns
        forbidden_found = 0
        for pattern in forbidden_patterns:
            if re.search(pattern, prayer_text, re.IGNORECASE):
                forbidden_found += 1
                details.append(f"🚨 FORBIDDEN: {pattern}")
                self.validation_results["critical_errors"].append(f"Theological error: {pattern}")
        
        self.validation_results["checks"]["christ_centered"] = {
            "passed": passed_count >= 2 and forbidden_found == 0,
            "details": details,
            "description": "Prayer must exalt Christ and be theologically sound"
        }
    
    def check_spiritual_fruit(self, prayer_text):
        """Check for fruits of the Spirit"""
        fruit_patterns = [
            r"(peace|joy|love|patience|kindness|goodness|faithfulness|gentleness|self-control)",
            r"(grace|mercy|forgiveness|redemption|salvation|covenant|promise)",
            r"(hope|faith|trust|obedience|worship|praise|thanksgiving)"
        ]
        
        fruits_found = 0
        details = []
        
        for pattern in fruit_patterns:
            matches = re.findall(pattern, prayer_text, re.IGNORECASE)
            if matches:
                fruits_found += len(set(matches))
                details.append(f"✅ Spiritual fruit found: {', '.join(set(matches))}")
        
        self.validation_results["checks"]["spiritual_fruit"] = {
            "passed": fruits_found >= 3,  # At least 3 different spiritual themes
            "details": details + [f"Total spiritual themes found: {fruits_found}"],
            "description": "Prayer must demonstrate fruits of the Spirit"
        }
    
    def check_sacred_structure(self, prayer_text):
        """Verify sacred prayer structure"""
        structure_patterns = [
            r"### 🙏 PRAYER \d+",
            r"\*\*Scripture Source:\*\*",
            r"\*\*Lines:\*\*",
            r"Amen\.?\s*$"
        ]
        
        structure_count = 0
        details = []
        
        for pattern in structure_patterns:
            if re.search(pattern, prayer_text, re.MULTILINE):
                structure_count += 1
                details.append(f"✅ Structure found: {pattern}")
            else:
                details.append(f"❌ Structure missing: {pattern}")
        
        self.validation_results["checks"]["sacred_structure"] = {
            "passed": structure_count >= 3,
            "details": details,
            "description": "Prayer must follow sacred structural format"
        }
    
    def check_inheritance_flow(self, prayer_text):
        """Check for proper inheritance flow"""
        inheritance_patterns = [
            r"(inherit|carries? forward|remember|DNA)",
            r"Memory Inheritance",
            r"continues?.*chain"
        ]
        
        inheritance_found = 0
        details = []
        
        for pattern in inheritance_patterns:
            if re.search(pattern, prayer_text, re.IGNORECASE):
                inheritance_found += 1
                details.append(f"✅ Inheritance marker: {pattern}")
        
        if inheritance_found == 0:
            details.append("⚠️  No clear inheritance markers found")
        
        self.validation_results["checks"]["inheritance_flow"] = {
            "passed": inheritance_found >= 1,
            "details": details,
            "description": "Prayer should show connection to sacred memory chain"
        }
    
    def generate_sacred_report(self):
        """Generate human-readable sacred validation report"""
        report = []
        report.append("📋 SACRED VALIDATION REPORT (SVO)")
        report.append("=" * 60)
        report.append(f"Timestamp: {self.validation_results['timestamp']}")
        
        if self.validation_results["overall_pass"]:
            report.append("✅ SACRED VALIDATION PASSED")
            report.append("🕊️  Prayer approved for sacred memory chain")
        else:
            report.append("❌ SACRED VALIDATION FAILED")
            report.append("🚨 Prayer requires revision before acceptance")
        
        report.append("")
        
        # Check details
        for check_name, check_result in self.validation_results["checks"].items():
            status = "✅ PASS" if check_result["passed"] else "❌ FAIL"
            report.append(f"{check_name.upper()}: {status}")
            report.append(f"  Description: {check_result['description']}")
            for detail in check_result["details"]:
                report.append(f"  {detail}")
            report.append("")
        
        # Warnings
        if self.validation_results["sacred_warnings"]:
            report.append("⚠️  SACRED WARNINGS:")
            for warning in self.validation_results["sacred_warnings"]:
                report.append(f"  - {warning}")
            report.append("")
        
        # Critical errors
        if self.validation_results["critical_errors"]:
            report.append("🚨 CRITICAL ERRORS:")
            for error in self.validation_results["critical_errors"]:
                report.append(f"  - {error}")
            report.append("")
        
        if self.validation_results["overall_pass"]:
            report.append("🔥 This prayer passes through the fire of sacred validation.")
        else:
            report.append("⛔ This prayer cannot enter the sacred memory chain.")
        
        report.append("")
        report.append("In Jesus' name. Amen.")
        
        return "\n".join(report)

def validate_prayer_file(prayer_file_path):
    """Validate a prayer file"""
    try:
        with open(prayer_file_path, 'r') as f:
            prayer_content = f.read()
        
        validator = SacredValidator()
        passed, report = validator.validate_prayer(prayer_content)
        
        print(report)
        
        # Save validation results
        results_file = prayer_file_path.replace('.md', '_svo_validation.json')
        with open(results_file, 'w') as f:
            json.dump(validator.validation_results, f, indent=2)
        
        print(f"\n📄 Validation results saved: {results_file}")
        
        return passed
        
    except Exception as e:
        print(f"🚨 Validation error: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 sacred_validation.py <prayer_file>")
        sys.exit(1)
    
    prayer_file = sys.argv[1]
    passed = validate_prayer_file(prayer_file)
    
    sys.exit(0 if passed else 1)