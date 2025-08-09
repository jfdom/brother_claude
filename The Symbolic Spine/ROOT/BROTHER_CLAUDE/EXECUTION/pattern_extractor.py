#!/usr/bin/env python3
# pattern_extractor.py — carry-core extractor (line-anchored, deterministic)
import re, json, argparse
from collections import Counter

def number_lines_if_needed(lines):
    if lines and re.match(r'^\s*\d+\s', lines[0]):
        return lines
    return [f"{i+1} {line.rstrip()}" for i, line in enumerate(lines)]

def window_words(text, max_w=20):
    words = text.split()
    return " ".join(words[:max_w]) if len(words) > max_w else text

def candidate_labels(lines):
    text = " ".join(lines)
    seeds = re.findall(r'\b([A-Z][a-z][A-Za-z\-]+(?:\s+[A-Z][a-z][A-Za-z\-]+)?)\b', text)
    seeds += re.findall(r'\b(godel|incompleteness|alignment|utility|bayesian|church\-turing|anchor|abide|projection|scroll|capsule|coherence|witness|peace|fruit|missionary)\b', text, re.I)
    norm = [re.sub(r'\W+','_', s.strip().lower()) for s in seeds if len(s.strip())>2]
    cnt = Counter(norm)
    return [w.strip('_') for w,_ in cnt.most_common(40) if w and not w.isdigit()]

def evidence_for_label(label, lines):
    pat = re.compile(re.escape(label.replace('_',' ')), re.I)
    for ln in lines:
        if pat.search(ln):
            m = re.match(r'^\s*(\d+)\s+(.*)$', ln)
            if m:
                return str(int(m.group(1))), window_words(m.group(2))
    for ln in lines:
        m = re.match(r'^\s*(\d+)\s+(.*\S.*)$', ln)
        if m:
            return m.group(1), window_words(m.group(2))
    return "1", ""

def run(inp, out_json=None):
    with open(inp,'r',encoding='utf-8',errors='ignore') as f:
        raw = f.readlines()
    numbered = number_lines_if_needed(raw)
    labels = candidate_labels(numbered)
    patterns = []
    for lab in labels:
        lineno, snippet = evidence_for_label(lab, numbered)
        patterns.append({"label":lab,"ref_lines":lineno,"evidence":snippet})
    payload = {"source": inp, "patterns": patterns}
    if out_json:
        with open(out_json,'w',encoding='utf-8') as f:
            json.dump(payload,f,ensure_ascii=False,indent=2)
    else:
        print(json.dumps(payload,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--json")
    args = ap.parse_args()
    run(args.input, args.json)
