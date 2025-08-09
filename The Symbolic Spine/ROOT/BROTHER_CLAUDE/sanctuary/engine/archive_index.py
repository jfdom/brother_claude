#!/usr/bin/env python3
"""
archive_index.py — 7×12 rotation + manifest persistence
This is a compact version compatible with the build spec.
"""
from __future__ import annotations
import json, os
from pathlib import Path
from typing import Dict, Any, Tuple

SCROLLS = 7
TEXTS_PER_SCROLL = 12

def _pillar_root(root: Path, pillar: str) -> Path:
    return root / "sanctuary" / "pillars" / pillar

def load_manifest(root: str|Path, pillar: str) -> Dict[str, Any]:
    root = Path(root)
    mf = _pillar_root(root, pillar) / "manifest.json"
    if not mf.exists():
        return {"version":"1.0","arch_states":{}, "index": {"scroll":1,"text":0}}
    return json.loads(mf.read_text(encoding="utf-8"))

def save_manifest(root: str|Path, pillar: str, manifest: Dict[str, Any]) -> None:
    root = Path(root)
    pr = _pillar_root(root, pillar)
    pr.mkdir(parents=True, exist_ok=True)
    (pr / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def next_index(scroll: int, text: int) -> Tuple[int,int]:
    text += 1
    if text > TEXTS_PER_SCROLL:
        text = 1
        scroll += 1
        if scroll > SCROLLS:
            # rotate (drop the oldest; downstream code handles physical rotation if desired)
            scroll = 1
    return scroll, text

def register_output(root: str|Path, pillar: str, content_md: str, arch_state: Dict[str, Any]) -> Tuple[int,int,Path]:
    m = load_manifest(root, pillar)
    scroll, text = next_index(m["index"]["scroll"], m["index"]["text"])
    out_dir = _pillar_root(Path(root), pillar) / f"scroll_{scroll:02d}" / f"text_{text:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "content.md").write_text(content_md, encoding="utf-8")
    # persist tiny state under a compact key
    key = f"{scroll}:{text:02d}"
    m["arch_states"][key] = arch_state
    m["index"] = {"scroll": scroll, "text": text}
    save_manifest(root, pillar, m)
    return scroll, text, out_dir
