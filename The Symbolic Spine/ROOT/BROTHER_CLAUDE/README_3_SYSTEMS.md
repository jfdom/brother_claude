# Three Memory Systems — with Architecture Chain v1

This package includes **Scripture**, **Math/Pattern**, and **Devotional** memory loops, each capable of producing
a verifiable “Genesis-from-the-tip” **Architecture Chain** header (GF, RR_prev/RR_curr, Genesis Carry breakdown).

## What’s included
- SYSTEMS/
  - SCRIPTURE/GENESIS/genesis_labels.json  (put your Scripture Genesis labels here)
  - SCRIPTURE/RR/rr_prev.txt               (rolling root, auto-updated)
  - MATH_PATTERN/GENESIS/genesis_labels.json
  - MATH_PATTERN/RR/rr_prev.txt
  - DEVOTIONAL/GENESIS/genesis_labels.json
  - DEVOTIONAL/RR/rr_prev.txt
- EXECUTION/
  - chain_utils.py
  - scripture_driver.py
  - math_pattern_driver.py
  - devotional_driver.py
  - (plus orchestrator.py, pattern_extractor.py, rvp_verifier.py, hybrid_generator.py)

## One-time setup per system
1) After your **Genesis cycle** for that system, save the labels to:
   - `SYSTEMS/<SYSTEM>/GENESIS/genesis_labels.json`
   ```json
   { "labels": ["label_one", "label_two", "..."] }
   ```
2) Leave `SYSTEMS/<SYSTEM>/RR/rr_prev.txt` empty — it will fill as you run cycles.

## Running a cycle (example)
Scripture:
```bash
python EXECUTION/scripture_driver.py --input CORE/scripture_chunk1.txt --sysroot SYSTEMS/SCRIPTURE
```
Then next:
```bash
python EXECUTION/scripture_driver.py --input CORE/scripture_chunk2.txt --prev STATE/cycle_logs/scripture_cycle_<timestamp>/curr_patterns.json --sysroot SYSTEMS/SCRIPTURE
```

Math/Pattern:
```bash
python EXECUTION/math_pattern_driver.py --input CORE/math_chunk1.txt --sysroot SYSTEMS/MATH_PATTERN
```

Devotional (no 30-min ping here; this just produces an entry when you run it):
```bash
python EXECUTION/devotional_driver.py --input CORE/devotional_source.txt --sysroot SYSTEMS/DEVOTIONAL
```

## Where to look
Each run creates a folder under `STATE/cycle_logs/` like `scripture_cycle_<timestamp>/` with:
- `creative_output.md` — includes the **ARCHITECTURE CHAIN** header
- `curr_patterns.json` — current labels
- `rvp_report.json` — carry breakdown (exact / fuzzy / missing / coverage)
- `cycle_state.json` — summarized metadata

## Notes
- The **30-minute reminder** for Devotional is not included as code (by design). Use your commissioning text in `AUX/` to keep that rhythm freely.
- You can still use the root `EXECUTION/orchestrator.py` for your math/pattern loop; the drivers are convenience wrappers per system.


## Auto‑Genesis Capture
You do **not** need to create `genesis_labels.json` yourself.
On the **first run** of each system’s driver, the current cycle’s pattern labels are saved as that system’s Genesis automatically.
If you ever want to redefine Genesis later, delete `SYSTEMS/<SYSTEM>/GENESIS/genesis_labels.json` and run that system once to recapture.
