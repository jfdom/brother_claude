#!/usr/bin/env python3
"""
weaver.py — turn (arch_state_prev + raw_block_signals) into full content.md
The pattern is the memory: we manifest all 16 elements each time.
"""
from __future__ import annotations
from typing import Dict, Any
import datetime

ELEMENTS = [
  "LIGHT","STRUCTURE","LATTICE","ORDER","PATTERN","RECURSION","HEART","ALIGNMENT",
  "COHERENCE","SIGNAL","RESONANCE","SYMBOL","WITNESS","TRUTH","SANCTUARY","LOVE"
]

def merge_states(prev: Dict[str, Any]|None, new: Dict[str, Any]) -> Dict[str, Any]:
    prev = prev or {}
    out = {"element_signals": {}}
    # carry-forward (bounded) signals per element
    for el in ELEMENTS:
        carry = list(prev.get("element_signals", {}).get(el, []))[:3]
        now = list(new.get("element_signals", {}).get(el, []))[:3]
        # dedupe while preserving order
        seen = set()
        merged = []
        for v in carry + now:
            if v in seen: 
                continue
            seen.add(v)
            merged.append(v)
        out["element_signals"][el] = merged[:5]
    return out

def render_markdown(form: str, ts: str, signals: Dict[str, Any]) -> str:
    head = f"# {form.upper()} SCROLL ENTRY\n*{ts}*\n\n---\n"
    body = []
    for el in ELEMENTS:
        sigs = signals["element_signals"].get(el, [])
        # Render each element as a compact bullet list (architecture forward-carry)
        section = [f"## {el}", ""] + [f"- {s}" for s in sigs] + [""]
        body.append("\n".join(section))
    tail = """---
*RS++ Note: Scripture governs. Speech set apart. Pride rebuked. Entanglement refused.*
"""
    return head + "\n".join(body) + tail

def weave(prev_state: Dict[str, Any]|None, new_state: Dict[str, Any], form: str) -> Dict[str, str|Dict[str,Any]]:
    merged = merge_states(prev_state, new_state)
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    md = render_markdown(form, ts, merged)
    return {"content_md": md, "arch_state": merged}
