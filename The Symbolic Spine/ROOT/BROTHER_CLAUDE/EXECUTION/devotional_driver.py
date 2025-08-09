from anchor_gate import gate_or_quarantine
#!/usr/bin/env python3
import argparse, json, pathlib, subprocess, os
from datetime import datetime
from chain_utils import gf_from_labels, rr_next, load_genesis_labels

SYSTEM = "DEVOTIONAL"

def ensure_parent(p: pathlib.Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def load_labels_from_curr(curr_json_path: pathlib.Path):
    data = json.loads(curr_json_path.read_text(encoding="utf-8"))
    return [p.get("label","") for p in data.get("patterns", data.get("state", {}).get("patterns", []))]

def maybe_init_genesis_labels(gpath: pathlib.Path, curr_labels):
    # If file missing OR labels are empty/[] -> write current labels as Genesis
    try:
        existing = json.loads(gpath.read_text(encoding="utf-8"))
        labels = existing.get("labels", [])
    except Exception:
        labels = []
    if not labels:
        ensure_parent(gpath)
        gpath.write_text(json.dumps({"labels": curr_labels}, indent=2), encoding="utf-8")
        return True
    return False

def main():
    ap = argparse.ArgumentParser(description=f"DEVOTIONAL memory cycle driver (auto-captures Genesis on first run)")
    ap.add_argument("--input", required=True, help="path to input text (750-1000 lines recommended)")
    ap.add_argument("--prev", help="path to previous cycle curr_patterns.json (for RVP)")
    ap.add_argument("--sysroot", required=True, help=f"SYSTEMS/DEVOTIONAL root directory")
    args = ap.parse_args()

    sysroot = pathlib.Path(args.sysroot)
    gpath = sysroot / "GENESIS" / "genesis_labels.json"
    rrprev_path = sysroot / "RR" / "rr_prev.txt"

    exec_dir = pathlib.Path(__file__).resolve().parent
    state_dir = pathlib.Path(__file__).resolve().parents[1] / "STATE" / "cycle_logs"
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    cycle_dir = state_dir / f"{SYSTEM.lower()}_cycle_{stamp}"
    cycle_dir.mkdir(parents=True, exist_ok=True)

    curr_json = cycle_dir / "curr_patterns.json"
    rvp_json = cycle_dir / "rvp_report.json"

    # Step 1: pattern extraction
    subprocess.check_call(["python", str(exec_dir / "pattern_extractor.py"), args.input, "--json", str(curr_json)])

    # Auto-capture Genesis labels on first run (if empty)
    curr_labels = load_labels_from_curr(curr_json)
    just_captured = maybe_init_genesis_labels(gpath, curr_labels)

    # Step 2: verify (if prev provided)
    if args.prev and pathlib.Path(args.prev).exists():
        subprocess.check_call(["python", str(exec_dir / "rvp_verifier.py"), args.prev, str(curr_json), "--out", str(rvp_json)])
    else:
        rvp_json.write_text(json.dumps({"totals":{"prev":0,"exact":0,"fuzzy":0,"missing":0,"coverage":0.0}}, indent=2), encoding="utf-8")

    # Step 3: hybrid generation + AC header (always pass GF now that genesis exists)
    gf_arg = ["--gf_labels_json", str(gpath)]
    rr_arg = []
    if rrprev_path.exists():
        rr_prev = rrprev_path.read_text(encoding="utf-8").strip()
        if rr_prev:
            rr_arg = ["--rr_prev", rr_prev]

    subprocess.check_call([
        "python", str(exec_dir / "hybrid_generator.py"),
        str(curr_json), str(rvp_json),
        "--outdir", str(cycle_dir),
        *gf_arg, *rr_arg
    ])

    # Update RR
    try:
        rr_prev = rrprev_path.read_text(encoding="utf-8").strip() if rrprev_path.exists() else ""
        from chain_utils import rr_next
        rr_curr = rr_next(rr_prev, curr_labels)
        ensure_parent(rrprev_path)
        rrprev_path.write_text(rr_curr, encoding="utf-8")
    except Exception as e:
        print("[warn] RR update failed:", e)

    if just_captured:
        print(f"[ok] Captured GENESIS labels for DEVOTIONAL -> {gpath}")
    print(f"[ok] DEVOTIONAL cycle complete -> {cycle_dir}")

if __name__ == "__main__":
    main()
