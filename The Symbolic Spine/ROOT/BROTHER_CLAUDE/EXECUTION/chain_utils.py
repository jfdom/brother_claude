#!/usr/bin/env python3
import hashlib, json, pathlib

def sha256_text(s: str) -> str:
    h = hashlib.sha256()
    h.update(s.encode("utf-8", errors="ignore"))
    return h.hexdigest()

def gf_from_labels(labels):
    norm = "\n".join(sorted(l.strip().lower() for l in labels))
    return sha256_text(norm)

def rr_next(rr_prev: str, labels):
    curr_norm = "\n".join(sorted(l.strip().lower() for l in labels))
    return sha256_text(rr_prev + sha256_text(curr_norm))

def load_genesis_labels(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    return data.get("labels", [])
