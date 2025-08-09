AC v1 Patch — Genesis Carry Breakdown
======================================

This patch updates:
- rvp_verifier.py — now reports Exact / Fuzzy / Missing and coverage %
- hybrid_generator.py — prints an ARCHITECTURE CHAIN header with a full Genesis Carry breakdown

Usage
-----
1) Replace the files in your project:
   - EXECUTION/rvp_verifier.py
   - EXECUTION/hybrid_generator.py

2) (Optional, recommended) Provide Genesis labels when generating output so GF is included:
   - Save a JSON with:
     {"labels": ["label_one","label_two", ...]}
   - Then call hybrid_generator with:
     --gf_labels_json /path/to/genesis_labels.json
     --rr_prev <previous_RR_string_if_you_have_it>

3) Run a cycle as before via orchestrator.py. The creative_output.md will include:

## ARCHITECTURE CHAIN
- GF: <hash>
- RR_prev: <hash>
- RR_curr: <hash>
- Genesis Carry: 95.8% (exact=12, fuzzy=11, missing=1, fuzzy_threshold=0.6)

Notes
-----
- Fuzzy matching uses token Jaccard similarity (default threshold 0.6). Tune via rvp_verifier --fuzzy.
- If you don't pass rr_prev/gf_labels_json, the header still shows the carry breakdown based on RVP totals.
