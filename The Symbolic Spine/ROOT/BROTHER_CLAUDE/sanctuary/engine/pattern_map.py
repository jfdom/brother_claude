#!/usr/bin/env python3
"""
pattern_map.py — extract 16 Frame element signals from raw text blocks
Heuristic, deterministic, small-footprint signals (not paragraphs).
"""
from __future__ import annotations
import re
from typing import Dict, Any, List

ELEMENTS = [
  "LIGHT","STRUCTURE","LATTICE","ORDER","PATTERN","RECURSION","HEART","ALIGNMENT",
  "COHERENCE","SIGNAL","RESONANCE","SYMBOL","WITNESS","TRUTH","SANCTUARY","LOVE"
]

def _top_keywords(text: str, k: int = 8) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower())
    stop = set("""the and for with this that have from into upon into your you are was were has had not but all any one out our him her his she they them their it its of to in on as by be is am we i a an or nor so if then than too very just also can may might shall should will would could must do did done make build keep hold anchor abide pray christ god jesus lord""".split())
    counts = {}
    for w in words:
        if w in stop: 
            continue
        counts[w] = counts.get(w,0)+1
    ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return [w for w,_ in ranked[:k]]

def extract_signals(raw_block: str) -> Dict[str, Any]:
    """Return compact element_signals: dict[str, dict] with <= 1-5 short strings per element."""
    # seed by simple features; callers can override/augment
    base = {
        "LIGHT": ["revelation", "insight"] if re.search(r"reveal|see|light|understand", raw_block, re.I) else ["orientation"],
        "STRUCTURE": ["framework","protocol"] if re.search(r"struct|protocol|spec|layout|tree", raw_block, re.I) else ["sequence"],
        "LATTICE": ["links","threads"] if re.search(r"link|connect|thread|graph|net", raw_block, re.I) else ["relations"],
        "ORDER": ["steps","checklist"] if re.search(r"step|first|second|third|checklist|order", raw_block, re.I) else ["flow"],
        "PATTERN": ["motif","recurrence"],
        "RECURSION": ["return","echo"] if re.search(r"again|loop|return|iterate|revisit", raw_block, re.I) else ["continuity"],
        "HEART": ["center","why"],
        "ALIGNMENT": ["rs++","sov"],
        "COHERENCE": ["unified","fit"],
        "SIGNAL": _top_keywords(raw_block, 6),
        "RESONANCE": ["echoes","amplify"],
        "SYMBOL": ["image","metaphor"] if re.search(r"symbol|image|poem|song|figure", raw_block, re.I) else ["marker"],
        "WITNESS": ["testify","evidence"] if re.search(r"testify|witness|proof|logs", raw_block, re.I) else ["record"],
        "TRUTH": ["scripture","grounding"] if re.search(r"bible|scripture|verse|psalm|proverb|romans|john|matthew|genesis", raw_block, re.I) else ["verification"],
        "SANCTUARY": ["rest","peace"],
        "LOVE": ["mercy","service"]
    }
    return {"element_signals": base}
