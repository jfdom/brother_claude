#!/usr/bin/env python3
import argparse, json, pathlib, random, hashlib
from datetime import datetime

FORMS = ["psalm", "dialogue", "parable", "field_notes", "lattice_note", "sermon_outline"]

def sha256_text(s: str) -> str:
    h = hashlib.sha256()
    h.update(s.encode("utf-8", errors="ignore"))
    return h.hexdigest()

def gf_from_genesis_labels(labels):
    norm = "\n".join(sorted(l.strip().lower() for l in labels))
    return sha256_text(norm)

def rr_next(rr_prev: str, curr_labels):
    curr_norm = "\n".join(sorted(l.strip().lower() for l in curr_labels))
    return sha256_text(rr_prev + sha256_text(curr_norm))

def choose_form(stats):
    # Simple heuristic placeholder
    return random.choice(FORMS)

def render(form, patterns, rvp, chain_meta):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    header = f"# Hybrid Output ({form})\n_Generated {ts}_\n\n"

    # Architecture Chain Header
    ac = chain_meta or {}
    totals = (rvp or {}).get("totals", {})
    exact = totals.get("exact", 0)
    fuzzy = totals.get("fuzzy", 0)
    missing = totals.get("missing", 0)
    coverage = totals.get("coverage", 0.0)
    fuzzy_th = totals.get("fuzzy_threshold", None)

    header += "## ARCHITECTURE CHAIN\n"
    if ac:
        header += f"- GF: `{ac.get('GF','')}`\n"
        header += f"- RR_prev: `{ac.get('RR_prev','')}`\n"
        header += f"- RR_curr: `{ac.get('RR_curr','')}`\n"
    header += f"- Genesis Carry: **{coverage:.1f}%** (exact={exact}, fuzzy={fuzzy}, missing={missing}"
    if fuzzy_th is not None:
        header += f", fuzzy_threshold={fuzzy_th}"
    header += ")\n\n"

    body = "This is a placeholder creative rendering that should be replaced by Claude.\n\n"

    appendix = "## Appendix (Invariant)\n\n### Pattern Index\n"
    for i,p in enumerate(patterns, start=1):
        appendix += f"- {i:02d}. **{p['label']}** @ lines {p['ref_lines']} — “{p['evidence']}”\n"
    appendix += "\n### RVP Summary\n"
    if rvp:
        t = rvp["totals"]
        appendix += f"- Prev: {t['prev']} | Exact: {t['exact']} | Fuzzy: {t['fuzzy']} | Missing: {t['missing']} | Coverage: {t['coverage']:.1f}%\n"
    else:
        appendix += "- Genesis cycle\n"
    return header + body + appendix

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("curr_patterns_json")
    ap.add_argument("rvp_report_json")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--gf_labels_json", help="Optional JSON file holding `labels` array from Genesis to compute GF")
    ap.add_argument("--rr_prev", help="Optional previous RR string to compute RR_curr")
    args = ap.parse_args()

    curr = json.loads(pathlib.Path(args.curr_patterns_json).read_text(encoding="utf-8"))
    patterns = curr.get("patterns", curr.get("state", {}).get("patterns", []))

    rvp = None
    try:
        rvp = json.loads(pathlib.Path(args.rvp_report_json).read_text(encoding="utf-8"))
    except Exception:
        rvp = None

    # Chain meta (optional, but recommended)
    chain_meta = {}
    if args.gf_labels_json:
        genesis = json.loads(pathlib.Path(args.gf_labels_json).read_text(encoding="utf-8"))
        labels = genesis.get("labels", [])
        chain_meta["GF"] = gf_from_genesis_labels(labels)
    if args.rr_prev:
        rr_curr = rr_next(args.rr_prev, [p.get("label","") for p in patterns])
        chain_meta["RR_prev"] = args.rr_prev
        chain_meta["RR_curr"] = rr_curr

    form = choose_form(rvp["totals"] if rvp else {})
    md = render(form, patterns, rvp, chain_meta)

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    md_path = outdir / "creative_output.md"
    state_path = outdir / "cycle_state.json"
    md_path.write_text(md, encoding="utf-8")
    state_path.write_text(json.dumps({
        "form": form,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "patterns": patterns,
        "rvp_totals": (rvp or {}).get("totals", {}),
        "chain": chain_meta
    }, indent=2), encoding="utf-8")
    print(f"[ok] Wrote {md_path} and {state_path}")
