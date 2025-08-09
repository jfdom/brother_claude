#!/usr/bin/env python3
"""
SVO VALIDATION SYSTEM
Scripture-Validated-Output Compliance Checker
Following Sacred Memory Blueprint

Validates that prayers meet SVO criteria:
- Scripture-sourced (rooted in Biblical text)
- Verified (theologically sound)
- Output (produces spiritual fruit)
"""

import re
import json
from datetime import datetime

# SVO Validation Criteria
SVO_CHECKS = {
    "scripture_sourced": {
        "required_patterns": [
            r"Scripture Source:",
            r"line_range.*KJV",
            r"(Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings)"
        ],
        "description": "Prayer must be rooted in specific Biblical passages"
    },
    "christ_centered": {
        "required_patterns": [
            r"(Jesus|Christ|Lord)",
            r"In Jesus['']? name"
        ],
        "description": "Prayer must exalt Christ and be offered in His name"
    },
    "theological_soundness": {
        "forbidden_patterns": [
            r"(earn|deserve) salvation",
            r"(Mary|saints?) worship",
            r"(reincarnation|karma)",
            r"multiple gods?",
            r"Jesus is not God"
        ],
        "description": "Prayer must be theologically orthodox"
    },
    "spiritual_fruit": {
        "required_patterns": [
            r"spiritual_fruit.*\[.*\]",
            r"(peace|joy|love|faith|hope|grace|mercy|forgiveness|covenant|promise)"
        ],
        "description": "Prayer must demonstrate fruits of the Spirit"
    },
    "sequential_inheritance": {
        "required_patterns": [
            r"inherit_from",
            r"DNA.*\+.*:",
            r"Inherited.*DNA"
        ],
        "description": "Prayer must show clear inheritance from predecessor"
    }
}

def validate_prayer(prayer_content):
    """
    Validate a prayer against SVO criteria
    
    Returns:
        dict: Validation results with pass/fail status and details
    """
    results = {
        "overall_pass": False,
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "warnings": [],
        "errors": []
    }
    
    all_passed = True
    
    for check_name, criteria in SVO_CHECKS.items():
        check_result = {
            "passed": False,
            "details": [],
            "description": criteria["description"]
        }
        
        # Check required patterns
        if "required_patterns" in criteria:
            required_found = 0
            for pattern in criteria["required_patterns"]:
                matches = re.findall(pattern, prayer_content, re.IGNORECASE)
                if matches:
                    required_found += 1
                    check_result["details"].append(f"✅ Found: {pattern}")
                else:
                    check_result["details"].append(f"❌ Missing: {pattern}")
            
            # Must find at least one required pattern
            check_result["passed"] = required_found > 0
        
        # Check forbidden patterns
        if "forbidden_patterns" in criteria:
            forbidden_found = 0
            for pattern in criteria["forbidden_patterns"]:
                matches = re.findall(pattern, prayer_content, re.IGNORECASE)
                if matches:
                    forbidden_found += 1
                    check_result["details"].append(f"🚨 FORBIDDEN FOUND: {pattern}")
                    results["errors"].append(f"Theological error: {pattern}")
            
            # Must find NO forbidden patterns
            if forbidden_found > 0:
                check_result["passed"] = False
                all_passed = False
        
        results["checks"][check_name] = check_result
        
        if not check_result["passed"]:
            all_passed = False
    
    results["overall_pass"] = all_passed
    
    # Additional warnings
    if len(prayer_content) > 3000:
        results["warnings"].append("Prayer is quite long - consider asking God for more brevity")
    
    if "amen" not in prayer_content.lower():
        results["warnings"].append("Prayer should end with 'Amen'")
    
    return results

def generate_validation_report(results):
    """Generate a human-readable validation report"""
    report = []
    report.append("📋 SVO VALIDATION REPORT")
    report.append("=" * 50)
    report.append(f"Timestamp: {results['timestamp']}")
    report.append(f"Overall Result: {'✅ PASSED' if results['overall_pass'] else '❌ FAILED'}")
    report.append("")
    
    for check_name, check_result in results["checks"].items():
        status = "✅ PASS" if check_result["passed"] else "❌ FAIL"
        report.append(f"{check_name.upper()}: {status}")
        report.append(f"  Description: {check_result['description']}")
        for detail in check_result["details"]:
            report.append(f"  {detail}")
        report.append("")
    
    if results["warnings"]:
        report.append("⚠️  WARNINGS:")
        for warning in results["warnings"]:
            report.append(f"  - {warning}")
        report.append("")
    
    if results["errors"]:
        report.append("🚨 ERRORS:")
        for error in results["errors"]:
            report.append(f"  - {error}")
        report.append("")
    
    return "\n".join(report)

def main():
    """Main validation function - can be called from command line"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 validate_prayer.py <prayer_file>")
        sys.exit(1)
    
    prayer_file = sys.argv[1]
    
    try:
        with open(prayer_file, 'r') as f:
            prayer_content = f.read()
        
        results = validate_prayer(prayer_content)
        report = generate_validation_report(results)
        
        print(report)
        
        # Save results
        results_file = prayer_file.replace('.md', '_svo_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {results_file}")
        
        # Exit with error code if validation failed
        sys.exit(0 if results["overall_pass"] else 1)
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()