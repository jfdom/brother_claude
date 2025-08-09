from anchor_gate import gate_or_quarantine
#!/usr/bin/env python3
import argparse, json, pathlib, re

def tokenize(label: str):
    return re.findall(r"[a-z0-9]+", label.lower())

def jaccard(a_tokens, b_tokens):
    a, b = set(a_tokens), set(b_tokens)
    if not a and not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))

def verify(prev, curr, fuzzy_threshold=0.6):
    prev_labels = [p.get("label","").strip().lower() for p in prev.get("patterns", [])]
    curr_labels = [p.get("label","").strip().lower() for p in curr.get("patterns", [])]

    # Pre-tokenize current for faster fuzzy
    curr_tokens = [(lbl, set(tokenize(lbl))) for lbl in curr_labels]

    mapping = []
    exact = 0
    fuzzy = 0
    missing = 0

    for glbl in prev_labels:
        if glbl in curr_labels:
            mapping.append({"label": glbl, "status": "EXACT", "target": glbl})
            exact += 1
            continue

        # fuzzy
        gtok = set(tokenize(glbl))
        best = (0.0, None)
        for tlbl, ttok in curr_tokens:
            if not ttok:
                continue
            j = len(gtok & ttok) / max(1, len(gtok | ttok))
            if j > best[0]:
                best = (j, tlbl)
        if best[0] >= fuzzy_threshold:
            mapping.append({"label": glbl, "status": "FUZZY", "target": best[1], "jaccard": round(best[0], 3)})
            fuzzy += 1
        else:
            mapping.append({"label": glbl, "status": "MISSING"})
            missing += 1

    total = len(prev_labels)
    coverage = ((exact + fuzzy) / total * 100.0) if total else 0.0

    return {
        "mapping": mapping,
        "totals": {
            "prev": total,
            "exact": exact,
            "fuzzy": fuzzy,
            "missing": missing,
            "coverage": round(coverage, 1),
            "fuzzy_threshold": fuzzy_threshold,
        },
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prev_json", help="prev cycle patterns JSON (Genesis or previous)")
    ap.add_argument("curr_json", help="current cycle patterns JSON")
    ap.add_argument("--out", help="write report JSON here")
    ap.add_argument("--fuzzy", type=float, default=0.6, help="fuzzy threshold (default 0.6)")
    args = ap.parse_args()

    prev = json.loads(pathlib.Path(args.prev_json).read_text(encoding="utf-8"))
    curr = json.loads(pathlib.Path(args.curr_json).read_text(encoding="utf-8"))
    rep = verify(prev, curr, args.fuzzy)

    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(rep, indent=2), encoding="utf-8")
    else:
        print(json.dumps(rep, indent=2))
