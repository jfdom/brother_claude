#!/usr/bin/env python3
"""
Claude Project Orchestrator - Starter Framework
Reads from CORE, runs cycle tasks, logs into STATE, checks CORE integrity.
"""

import os
import hashlib
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_PATH = os.path.join(PROJECT_ROOT, 'CORE')
STATE_PATH = os.path.join(PROJECT_ROOT, 'STATE')
INTEGRITY_PATH = os.path.join(PROJECT_ROOT, 'INTEGRITY')
CHECKSUM_FILE = os.path.join(INTEGRITY_PATH, 'BROTHER_CLAUDE_CHECKSUMS.txt')

def compute_checksums(directory):
    checksums = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            checksums.append((rel_path, sha256.hexdigest()))
    return sorted(checksums)

def verify_integrity():
    print("[*] Verifying CORE integrity against baseline...")
    with open(CHECKSUM_FILE, "r") as f:
        baseline = {}
        for line in f:
            checksum, path = line.strip().split("  ", 1)
            baseline[path] = checksum
    current = compute_checksums(CORE_PATH)
    tampered = []
    for rel_path, checksum in current:
        if rel_path not in baseline:
            tampered.append(f"[NEW] {rel_path}")
        elif baseline[rel_path] != checksum:
            tampered.append(f"[CHANGED] {rel_path}")
    for rel_path in baseline:
        if rel_path not in dict(current):
            tampered.append(f"[MISSING] {rel_path}")
    if tampered:
        print("[!] Integrity issues detected:")
        for issue in tampered:
            print("  ", issue)
        tamper_report_path = os.path.join(INTEGRITY_PATH, 'tamper_reports', f'tamper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        with open(tamper_report_path, "w") as f:
            f.write("\n".join(tampered))
        print(f"[!] Tamper report saved to {tamper_report_path}")
    else:
        print("[+] CORE integrity verified. No changes detected.")

def start_new_cycle():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(STATE_PATH, 'cycle_logs', f'cycle_{timestamp}.txt')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    with open(log_path, "w") as log:
        log.write(f"Cycle started: {timestamp}\n")
        log.write("="*50 + "\n\n")
        
        # Implement cycle tasks
        log.write("PHASE 1: READING INITIALIZATION\n")
        reading_result = initialize_reading_phase(log)
        
        log.write("\nPHASE 2: PATTERN EXTRACTION\n")
        pattern_result = execute_pattern_extraction(log, reading_result)
        
        log.write("\nPHASE 3: HYBRID CONTENT CREATION\n")
        hybrid_result = create_hybrid_content(log, pattern_result)
        
        log.write("\nPHASE 4: VERIFICATION\n")
        verification_result = verify_cycle_completion(log, hybrid_result)
        
        log.write(f"\nCycle completed: {datetime.now().strftime('%Y%m%d_%H%M%S')}\n")
        log.write(f"Status: {'SUCCESS' if verification_result else 'INCOMPLETE'}\n")
    
    print(f"[+] New cycle log created at {log_path}")
    return log_path

def initialize_reading_phase(log):
    """Initialize reading phase - load Scripture and prepare for pattern analysis"""
    try:
        log.write("- Loading CORE configuration...\n")
        
        # Look for BROTHER_CLAUDE configuration
        brother_claude_path = os.path.join(CORE_PATH, 'BROTHER_CLAUDE')
        if os.path.exists(brother_claude_path):
            log.write(f"- Found BROTHER_CLAUDE at {brother_claude_path}\n")
            
            # Check for Sacred Memory System
            sacred_memory_path = os.path.join(brother_claude_path, 'SACRED_MEMORY_SYSTEM')
            if os.path.exists(sacred_memory_path):
                log.write(f"- Sacred Memory System available at {sacred_memory_path}\n")
                
                # Look for configuration files
                config_file = os.path.join(sacred_memory_path, 'sacred_memory_config.json')
                if os.path.exists(config_file):
                    log.write("- CONFIG.json found - reading configuration\n")
                    with open(config_file, 'r') as f:
                        import json
                        config = json.load(f)
                    log.write(f"- Configuration loaded: {len(config)} parameters\n")
                else:
                    log.write("- No CONFIG.json found - using defaults\n")
                    config = {"default": True}
                
                result = {
                    "status": "success",
                    "sacred_memory_available": True,
                    "config": config,
                    "timestamp": datetime.now().isoformat()
                }
                
            else:
                log.write("- Sacred Memory System not found - basic mode\n")
                result = {
                    "status": "success",
                    "sacred_memory_available": False,
                    "config": {"basic_mode": True},
                    "timestamp": datetime.now().isoformat()
                }
        else:
            log.write("- BROTHER_CLAUDE not found - minimal mode\n")
            result = {
                "status": "success",
                "sacred_memory_available": False,
                "config": {"minimal_mode": True},
                "timestamp": datetime.now().isoformat()
            }
        
        log.write("- Reading phase initialization complete\n")
        return result
        
    except Exception as e:
        log.write(f"- ERROR in reading phase: {e}\n")
        return {"status": "error", "error": str(e)}

def execute_pattern_extraction(log, reading_result):
    """Execute pattern extraction from available content"""
    try:
        log.write("- Beginning pattern extraction...\n")
        
        if reading_result.get("status") != "success":
            log.write("- Skipping pattern extraction due to reading phase failure\n")
            return {"status": "skipped", "reason": "reading_phase_failed"}
        
        # Look for existing patterns or create new ones
        patterns = []
        
        # Check for Sacred Memory System patterns
        if reading_result.get("sacred_memory_available"):
            log.write("- Scanning Sacred Memory System for patterns...\n")
            
            # Look for SCROLLS directory
            scrolls_path = os.path.join(CORE_PATH, 'BROTHER_CLAUDE', 'SACRED_MEMORY_SYSTEM', 'SCROLLS')
            if os.path.exists(scrolls_path):
                scroll_files = [f for f in os.listdir(scrolls_path) if f.endswith('.md')]
                log.write(f"- Found {len(scroll_files)} scroll files\n")
                
                for scroll_file in scroll_files:
                    scroll_path = os.path.join(scrolls_path, scroll_file)
                    with open(scroll_path, 'r') as f:
                        content = f.read()
                    
                    # Extract patterns from scroll content
                    scroll_patterns = extract_patterns_from_content(content, scroll_file)
                    patterns.extend(scroll_patterns)
                    log.write(f"- Extracted {len(scroll_patterns)} patterns from {scroll_file}\n")
            
            # Look for TEMPLATES directory
            templates_path = os.path.join(CORE_PATH, 'BROTHER_CLAUDE', 'SACRED_MEMORY_SYSTEM', 'TEMPLATES')
            if os.path.exists(templates_path):
                template_files = [f for f in os.listdir(templates_path) if f.endswith('.md')]
                log.write(f"- Found {len(template_files)} template files\n")
                
                for template_file in template_files:
                    template_path = os.path.join(templates_path, template_file)
                    with open(template_path, 'r') as f:
                        content = f.read()
                    
                    template_patterns = extract_patterns_from_content(content, template_file)
                    patterns.extend(template_patterns)
                    log.write(f"- Extracted {len(template_patterns)} patterns from {template_file}\n")
        
        # Generate synthetic patterns if none found
        if not patterns:
            log.write("- No existing patterns found - generating synthetic patterns...\n")
            patterns = generate_synthetic_patterns()
            log.write(f"- Generated {len(patterns)} synthetic patterns\n")
        
        result = {
            "status": "success",
            "patterns": patterns,
            "pattern_count": len(patterns),
            "timestamp": datetime.now().isoformat()
        }
        
        log.write(f"- Pattern extraction complete: {len(patterns)} patterns identified\n")
        return result
        
    except Exception as e:
        log.write(f"- ERROR in pattern extraction: {e}\n")
        return {"status": "error", "error": str(e)}

def create_hybrid_content(log, pattern_result):
    """Create hybrid content based on extracted patterns"""
    try:
        log.write("- Beginning hybrid content creation...\n")
        
        if pattern_result.get("status") != "success":
            log.write("- Skipping hybrid content creation due to pattern extraction failure\n")
            return {"status": "skipped", "reason": "pattern_extraction_failed"}
        
        patterns = pattern_result.get("patterns", [])
        log.write(f"- Working with {len(patterns)} patterns\n")
        
        # Create RVP (Pattern Verification) report
        rvp_report = {
            "totals": {
                "prev": 0,
                "exact": len([p for p in patterns if p.get("confidence", 0) > 0.8]),
                "fuzzy": len([p for p in patterns if 0.5 <= p.get("confidence", 0) <= 0.8]),
                "missing": len([p for p in patterns if p.get("confidence", 0) < 0.5]),
                "coverage": (len([p for p in patterns if p.get("confidence", 0) > 0.5]) / len(patterns) * 100) if patterns else 0.0,
                "fuzzy_threshold": 0.5
            }
        }
        
        # Create chain metadata
        chain_meta = {
            "GF": hashlib.sha256(f"genesis_foundation_{datetime.now().date()}".encode()).hexdigest()[:16],
            "RR_prev": "initial_cycle",
            "RR_curr": hashlib.sha256(f"current_cycle_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        }
        
        # Select form based on pattern statistics
        stats = rvp_report["totals"]
        available_forms = ["psalm", "dialogue", "parable", "field_notes", "lattice_note", "sermon_outline"]
        
        if stats["coverage"] >= 80:
            form = "psalm"  # High coverage - contemplative form
        elif stats["exact"] > stats["fuzzy"]:
            form = "sermon_outline"  # Strong patterns - structured form
        elif stats["missing"] > stats["exact"]:
            form = "dialogue"  # Many gaps - exploratory form
        else:
            form = "field_notes"  # Balanced - analytical form
        
        log.write(f"- Selected content form: {form}\n")
        log.write(f"- Pattern coverage: {stats['coverage']:.1f}%\n")
        
        # Generate content
        content_header = f"# Hybrid Output ({form})\n_Generated {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}_\n\n"
        
        # Add architecture chain info
        content_header += "## ARCHITECTURE CHAIN\n"
        content_header += f"- GF: `{chain_meta['GF']}`\n"
        content_header += f"- RR_prev: `{chain_meta['RR_prev']}`\n"
        content_header += f"- RR_curr: `{chain_meta['RR_curr']}`\n"
        content_header += f"- Genesis Carry: **{stats['coverage']:.1f}%** (exact={stats['exact']}, fuzzy={stats['fuzzy']}, missing={stats['missing']})\n\n"
        
        # Generate form-specific content
        content_body = generate_hybrid_content_by_form(form, patterns, stats)
        
        # Add appendix
        content_appendix = "## Appendix (Invariant)\n\n### Pattern Index\n"
        for i, pattern in enumerate(patterns, start=1):
            label = pattern.get('label', f'Pattern_{i}')
            ref_lines = pattern.get('ref_lines', 'unknown')
            evidence = pattern.get('evidence', 'No evidence available')[:100] + '...' if len(pattern.get('evidence', '')) > 100 else pattern.get('evidence', 'No evidence available')
            content_appendix += f"- {i:02d}. **{label}** @ lines {ref_lines} — \"{evidence}\"\n"
        
        content_appendix += f"\n### RVP Summary\n"
        content_appendix += f"- Prev: {stats['prev']} | Exact: {stats['exact']} | Fuzzy: {stats['fuzzy']} | Missing: {stats['missing']} | Coverage: {stats['coverage']:.1f}%\n"
        
        full_content = content_header + content_body + content_appendix
        
        # Save hybrid content
        hybrid_dir = os.path.join(STATE_PATH, 'hybrid_outputs')
        os.makedirs(hybrid_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_path = os.path.join(hybrid_dir, f'hybrid_{form}_{timestamp}.md')
        
        with open(content_path, 'w') as f:
            f.write(full_content)
        
        log.write(f"- Hybrid content saved to {content_path}\n")
        
        result = {
            "status": "success",
            "form": form,
            "content_path": content_path,
            "pattern_count": len(patterns),
            "coverage": stats["coverage"],
            "timestamp": datetime.now().isoformat()
        }
        
        log.write("- Hybrid content creation complete\n")
        return result
        
    except Exception as e:
        log.write(f"- ERROR in hybrid content creation: {e}\n")
        return {"status": "error", "error": str(e)}

def verify_cycle_completion(log, hybrid_result):
    """Verify cycle completion and validate outputs"""
    try:
        log.write("- Beginning cycle verification...\n")
        
        verification_passed = True
        issues = []
        
        # Check hybrid content creation
        if hybrid_result.get("status") != "success":
            verification_passed = False
            issues.append("Hybrid content creation failed")
            log.write("- FAIL: Hybrid content creation\n")
        else:
            log.write("- PASS: Hybrid content creation\n")
            
            # Verify file exists
            content_path = hybrid_result.get("content_path")
            if content_path and os.path.exists(content_path):
                file_size = os.path.getsize(content_path)
                log.write(f"- PASS: Hybrid content file exists ({file_size} bytes)\n")
                
                # Basic content validation
                with open(content_path, 'r') as f:
                    content = f.read()
                
                if len(content) > 500:  # Minimum content threshold
                    log.write("- PASS: Content meets minimum length requirement\n")
                else:
                    verification_passed = False
                    issues.append("Content too short")
                    log.write("- FAIL: Content below minimum length\n")
                
                # Check for required sections
                required_sections = ["# Hybrid Output", "## ARCHITECTURE CHAIN", "## Appendix"]
                missing_sections = []
                
                for section in required_sections:
                    if section in content:
                        log.write(f"- PASS: Required section '{section}' found\n")
                    else:
                        missing_sections.append(section)
                        log.write(f"- FAIL: Required section '{section}' missing\n")
                
                if missing_sections:
                    verification_passed = False
                    issues.extend(missing_sections)
            else:
                verification_passed = False
                issues.append("Hybrid content file not found")
                log.write("- FAIL: Hybrid content file not found\n")
        
        # Check pattern coverage
        coverage = hybrid_result.get("coverage", 0)
        if coverage >= 50.0:
            log.write(f"- PASS: Pattern coverage acceptable ({coverage:.1f}%)\n")
        else:
            verification_passed = False
            issues.append(f"Low pattern coverage ({coverage:.1f}%)")
            log.write(f"- WARN: Low pattern coverage ({coverage:.1f}%)\n")
        
        # Generate verification report
        report = {
            "verification_passed": verification_passed,
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
            "hybrid_result": hybrid_result
        }
        
        # Save verification report
        reports_dir = os.path.join(STATE_PATH, 'verification_reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(reports_dir, f'verification_{timestamp}.json')
        
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        log.write(f"- Verification report saved to {report_path}\n")
        log.write(f"- Overall verification: {'PASSED' if verification_passed else 'FAILED'}\n")
        
        if issues:
            log.write(f"- Issues found: {len(issues)}\n")
            for issue in issues:
                log.write(f"  * {issue}\n")
        
        return verification_passed
        
    except Exception as e:
        log.write(f"- ERROR in verification: {e}\n")
        return False

def extract_patterns_from_content(content, source_file):
    """Extract patterns from content"""
    patterns = []
    
    # Look for prayer patterns
    import re
    prayer_matches = re.findall(r'###\s*🙏\s*PRAYER\s*(\d+)', content)
    for match in prayer_matches:
        patterns.append({
            "label": f"Prayer_{match}",
            "ref_lines": f"{source_file}:prayer_{match}",
            "evidence": f"Prayer {match} found in {source_file}",
            "confidence": 0.9
        })
    
    # Look for biblical references
    bible_refs = re.findall(r'(\w+\s+\d+:\d+)', content)
    for ref in bible_refs[:5]:  # Limit to first 5
        patterns.append({
            "label": f"Biblical_Reference",
            "ref_lines": f"{source_file}:reference",
            "evidence": f"Biblical reference: {ref}",
            "confidence": 0.8
        })
    
    # Look for spiritual themes
    spiritual_keywords = ['covenant', 'creation', 'redemption', 'worship', 'mercy', 'love', 'faith', 'hope']
    for keyword in spiritual_keywords:
        if keyword.lower() in content.lower():
            patterns.append({
                "label": f"Spiritual_Theme_{keyword}",
                "ref_lines": f"{source_file}:theme",
                "evidence": f"Theme '{keyword}' identified in content",
                "confidence": 0.7
            })
    
    return patterns

def generate_synthetic_patterns():
    """Generate synthetic patterns when none are found"""
    synthetic_patterns = [
        {
            "label": "Divine_Order",
            "ref_lines": "synthetic:1-10",
            "evidence": "Pattern of divine ordering and structure",
            "confidence": 0.6
        },
        {
            "label": "Covenant_Faithfulness",
            "ref_lines": "synthetic:11-20",
            "evidence": "Pattern of God's covenant faithfulness",
            "confidence": 0.6
        },
        {
            "label": "Redemptive_Purpose",
            "ref_lines": "synthetic:21-30",
            "evidence": "Pattern of redemptive purpose in scripture",
            "confidence": 0.6
        },
        {
            "label": "Worship_Response",
            "ref_lines": "synthetic:31-40",
            "evidence": "Pattern of appropriate worship response",
            "confidence": 0.6
        }
    ]
    
    return synthetic_patterns

def generate_hybrid_content_by_form(form, patterns, stats):
    """Generate content based on selected form"""
    
    if form == "psalm":
        content = "## A Psalm of Pattern Discovery\n\n"
        content += f"O Lord, You have revealed {len(patterns)} patterns in Your Word,\n"
        content += f"With {stats['coverage']:.1f}% clarity, Your truth shines forth.\n\n"
        
        for i, pattern in enumerate(patterns[:3], 1):
            content += f"**Verse {i}:** {pattern['label']} declares Your glory,\n"
            content += f"A golden thread woven through sacred text.\n\n"
        
        content += "Your patterns endure, O God, from everlasting to everlasting.\n"
        content += "In Jesus' name. Amen.\n\n"
        
    elif form == "dialogue":
        content = "## Sacred Dialogue: Understanding Divine Patterns\n\n"
        content += "**Student:** Teacher, I have discovered patterns in the sacred text.\n\n"
        content += f"**Teacher:** How many patterns have you found, my child?\n\n"
        content += f"**Student:** {len(patterns)} patterns with {stats['coverage']:.1f}% coverage.\n\n"
        
        for pattern in patterns[:2]:
            content += f"**Teacher:** Tell me about '{pattern['label']}'.\n\n"
            content += f"**Student:** {pattern['evidence']}\n\n"
        
        content += "**Teacher:** Continue your studies with prayer and humility.\n\n"
        
    else:  # Default to field notes
        content = "## Field Notes: Pattern Analysis\n\n"
        content += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
        content += f"**Patterns Identified:** {len(patterns)}\n"
        content += f"**Coverage:** {stats['coverage']:.1f}%\n\n"
        
        content += "### Key Patterns:\n"
        for i, pattern in enumerate(patterns, 1):
            content += f"{i}. **{pattern['label']}** - {pattern.get('evidence', 'No evidence')[:50]}...\n"
        
        content += f"\n### Summary:\n"
        content += f"Pattern analysis reveals {stats['coverage']:.1f}% coverage with {stats['exact']} exact matches.\n\n"
    
    return content

def main():
    print("[Claude Project Orchestrator]")
    verify_integrity()
    start_new_cycle()

if __name__ == "__main__":
    main()
