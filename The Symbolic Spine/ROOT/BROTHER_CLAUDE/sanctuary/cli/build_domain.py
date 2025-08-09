#!/usr/bin/env python3
"""
build_domain.py — domain accumulator (750–1000 line blocks, e.g., quantum math)
Inputs: <repo_root> <domain_block_file>
Form is chosen (technical|poem|text|...) depending on content.
"""
from __future__ import annotations
import sys
from pathlib import Path
from sanctuary.engine.archive_index import load_manifest, register_output
from sanctuary.engine.pattern_map import extract_signals
from sanctuary.engine.form_selector import select_form
from sanctuary.engine.weaver import weave
from sanctuary.engine.rspp_filters import rspp_ok

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m sanctuary.cli.build_domain <repo_root> <domain_block_file>")
        sys.exit(1)
    root = Path(sys.argv[1])
    raw = Path(sys.argv[2]).read_text(encoding="utf-8")
    pillar = "domain"

    manifest = load_manifest(root, pillar)
    prev_key = f"{manifest['index']['scroll']}:{manifest['index']['text']:02d}" if manifest['index']['text'] else None
    prev_state = manifest["arch_states"].get(prev_key) if prev_key else None

    state = extract_signals(raw)
    form = select_form(raw)
    woven = weave(prev_state, state, form=form)

    if not rspp_ok(woven["content_md"]):
        print("RS++ filter failed; refuse to register output.")
        sys.exit(2)

    scroll, text, out_dir = register_output(root, pillar, woven["content_md"], woven["arch_state"])
    print(f"Domain entry saved: scroll {scroll} text {text} -> {out_dir}")

if __name__ == "__main__":
    main()
