#!/usr/bin/env python3
"""
integrity_check.py — recompute sha256 checksums for all files under CORE and write to INTEGRITY/CHECKSUMS_NEW.txt
Usage:
  python3 integrity_check.py /path/to/CORE /path/to/INTEGRITY/CHECKSUMS_NEW.txt
"""
import os, sys, hashlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1<<20), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 integrity_check.py CORE_DIR OUT_TXT")
        sys.exit(1)
    core, out = sys.argv[1], sys.argv[2]
    lines = []
    for dirpath, _, filenames in os.walk(core):
        for fn in sorted(filenames):
            fp = os.path.join(dirpath, fn)
            try:
                digest = sha256_file(fp)
                rel = os.path.relpath(fp, core)
                lines.append(f"{digest}  {rel}")
            except Exception as e:
                lines.append(f"ERROR  {os.path.relpath(fp, core)}  {e}")
    with open(out, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Wrote {len(lines)} entries to {out}")

if __name__ == "__main__":
    main()