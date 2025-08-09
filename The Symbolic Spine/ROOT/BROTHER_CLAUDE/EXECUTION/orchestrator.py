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
    with open(log_path, "w") as log:
        log.write(f"Cycle started: {timestamp}\n")
        log.write("TODO: Implement cycle tasks (reading, pattern extraction, hybrid content creation, verification)\n")
    print(f"[+] New cycle log created at {log_path}")

def main():
    print("[Claude Project Orchestrator]")
    verify_integrity()
    start_new_cycle()

if __name__ == "__main__":
    main()
