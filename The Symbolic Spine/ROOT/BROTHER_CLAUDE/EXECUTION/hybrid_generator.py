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
    # Enhanced form selection based on pattern statistics
    if not stats:
        return random.choice(FORMS)
    
    exact = stats.get('exact', 0)
    fuzzy = stats.get('fuzzy', 0)
    missing = stats.get('missing', 0)
    coverage = stats.get('coverage', 0.0)
    
    # Form selection based on spiritual pattern analysis
    if coverage >= 90.0:
        # High coverage - use contemplative forms
        return random.choice(['psalm', 'sermon_outline', 'lattice_note'])
    elif coverage >= 70.0:
        # Moderate coverage - balanced forms
        return random.choice(['dialogue', 'field_notes', 'psalm'])
    elif missing > exact:
        # Many missing patterns - use exploratory forms
        return random.choice(['parable', 'field_notes', 'dialogue'])
    else:
        # Default to accessible forms
        return random.choice(['psalm', 'parable', 'field_notes'])

def generate_creative_content(form, patterns, rvp, chain_meta):
    """Generate creative content based on form and patterns"""
    
    # Extract key themes from patterns
    themes = []
    evidence_fragments = []
    
    for pattern in patterns:
        label = pattern.get('label', '')
        evidence = pattern.get('evidence', '')
        
        themes.append(label)
        if evidence:
            evidence_fragments.append(evidence[:100] + '...' if len(evidence) > 100 else evidence)
    
    # Get coverage information
    coverage = 0.0
    if rvp and 'totals' in rvp:
        coverage = rvp['totals'].get('coverage', 0.0)
    
    # Generate content based on form
    if form == 'psalm':
        return generate_psalm_content(themes, evidence_fragments, coverage, chain_meta)
    elif form == 'dialogue':
        return generate_dialogue_content(themes, evidence_fragments, coverage, chain_meta)
    elif form == 'parable':
        return generate_parable_content(themes, evidence_fragments, coverage, chain_meta)
    elif form == 'field_notes':
        return generate_field_notes_content(themes, evidence_fragments, coverage, chain_meta)
    elif form == 'lattice_note':
        return generate_lattice_content(themes, evidence_fragments, coverage, chain_meta)
    elif form == 'sermon_outline':
        return generate_sermon_content(themes, evidence_fragments, coverage, chain_meta)
    else:
        return generate_default_content(themes, evidence_fragments, coverage, chain_meta)

def generate_psalm_content(themes, evidence, coverage, chain_meta):
    """Generate psalm-style creative content"""
    content = "## A Psalm of Pattern Recognition\n\n"
    
    # Opening verse
    content += f"O Lord, in Your Word I have found {len(themes)} patterns of truth,\n"
    content += f"Your ancient wisdom echoes with {coverage:.1f}% clarity in this sacred text.\n\n"
    
    # Verses based on themes
    for i, theme in enumerate(themes[:5], 1):
        content += f"**Verse {i}:** {theme.title()} reveals itself as a golden thread,\n"
        content += f"Woven through scripture like light through morning mist.\n\n"
    
    # Evidence integration
    if evidence:
        content += "**Selah** — Consider these words:\n\n"
        for fragment in evidence[:3]:
            content += f"> {fragment}\n\n"
    
    # Closing
    content += f"Your patterns endure, O God, from generation to generation.\n"
    content += f"In Jesus' name, may these insights bear fruit. Amen.\n\n"
    
    return content

def generate_dialogue_content(themes, evidence, coverage, chain_meta):
    """Generate dialogue-style creative content"""
    content = "## A Sacred Dialogue on Pattern Discovery\n\n"
    
    content += "**Seeker:** Master, I have been studying the sacred text and found patterns emerging.\n\n"
    content += f"**Teacher:** How many patterns have you discerned, my child?\n\n"
    content += f"**Seeker:** {len(themes)} distinct patterns, with {coverage:.1f}% clarity overall.\n\n"
    
    # Discuss key themes
    for i, theme in enumerate(themes[:3]):
        content += f"**Teacher:** Tell me about the pattern you call '{theme}'.\n\n"
        content += f"**Seeker:** This thread runs deep through the text, revealing divine consistency.\n\n"
    
    # Evidence discussion
    if evidence:
        content += "**Teacher:** And what evidence supports your observations?\n\n"
        content += "**Seeker:** Consider these fragments I have gathered:\n\n"
        for fragment in evidence[:2]:
            content += f"- {fragment}\n"
        content += "\n"
    
    content += "**Teacher:** Well discerned. Continue your study with prayer and humility.\n\n"
    content += "**Seeker:** In Jesus' name, I will. Thank you for your guidance.\n\n"
    
    return content

def generate_parable_content(themes, evidence, coverage, chain_meta):
    """Generate parable-style creative content"""
    content = "## The Parable of the Pattern Finder\n\n"
    
    content += "A scholar went into the scriptures to seek wisdom. Like a merchant searching for fine pearls, "
    content += f"he examined each passage until he found {len(themes)} precious patterns.\n\n"
    
    # Develop the parable around the themes
    if 'creation' in str(themes).lower():
        content += "Among these patterns was one that spoke of creation - how God speaks order from chaos, "
        content += "light from darkness, life from dust.\n\n"
    
    if 'covenant' in str(themes).lower():
        content += "Another pattern revealed the faithfulness of covenant - how God's promises endure "
        content += "from generation to generation, unbroken and sure.\n\n"
    
    content += f"When the scholar counted his findings, he discovered {coverage:.1f}% of the text "
    content += "resonated with these eternal patterns.\n\n"
    
    # Moral of the parable
    content += "**The Lesson:** Those who seek diligently in God's Word will find treasures of wisdom "
    content += "that connect across time and space. The same God who spoke to Moses speaks to us today "
    content += "through patterns of divine truth.\n\n"
    
    content += "*He who has ears to hear, let him hear.*\n\n"
    
    return content

def generate_field_notes_content(themes, evidence, coverage, chain_meta):
    """Generate field notes style creative content"""
    content = "## Field Notes: Pattern Analysis Session\n\n"
    
    content += f"**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}\n"
    content += f"**Patterns Identified:** {len(themes)}\n"
    content += f"**Coverage:** {coverage:.1f}%\n\n"
    
    content += "### Key Observations:\n\n"
    for i, theme in enumerate(themes, 1):
        content += f"{i}. **{theme.title()}** - Recurring motif with strong textual support\n"
    
    content += "\n### Evidence Samples:\n\n"
    for i, fragment in enumerate(evidence[:4], 1):
        content += f"**Sample {i}:** {fragment}\n\n"
    
    content += "### Analysis Notes:\n\n"
    content += f"- Pattern recognition yielding {coverage:.1f}% textual coverage\n"
    content += f"- {len(themes)} distinct thematic threads identified\n"
    content += "- Evidence suggests intentional divine design in textual structure\n"
    content += "- Recommend further investigation into cross-references\n\n"
    
    content += "**Next Steps:** Expand analysis to adjacent passages, cross-reference with concordance.\n\n"
    content += "*Soli Deo Gloria*\n\n"
    
    return content

def generate_lattice_content(themes, evidence, coverage, chain_meta):
    """Generate lattice note style creative content"""
    content = "## Lattice Pattern: Divine Architecture Revealed\n\n"
    
    content += "```\n"
    content += "PATTERN LATTICE STRUCTURE:\n"
    content += f"Coverage: {coverage:.1f}% | Themes: {len(themes)}\n"
    content += "┌─────────────────────────────────┐\n"
    
    for i, theme in enumerate(themes[:6]):
        content += f"│ {i+1:02d}. {theme:<25} │\n"
    
    content += "└─────────────────────────────────┘\n"
    content += "```\n\n"
    
    content += "### Interconnection Analysis:\n\n"
    content += "The identified patterns form a lattice of meaning where each theme reinforces and "
    content += "amplifies the others. This suggests:\n\n"
    
    content += "1. **Structural Integrity** - The text exhibits intentional design\n"
    content += "2. **Thematic Coherence** - Patterns support unified message\n"
    content += "3. **Divine Intentionality** - Non-random distribution of themes\n\n"
    
    if evidence:
        content += "### Supporting Evidence Nodes:\n\n"
        for i, fragment in enumerate(evidence[:3], 1):
            content += f"**Node {i}:** {fragment}\n\n"
    
    content += "### Conclusion:\n"
    content += f"This lattice analysis reveals {coverage:.1f}% pattern coverage, indicating strong "
    content += "structural integrity in the sacred text.\n\n"
    
    return content

def generate_sermon_content(themes, evidence, coverage, chain_meta):
    """Generate sermon outline style creative content"""
    content = "## Sermon Outline: Patterns of Divine Truth\n\n"
    
    content += "### I. Introduction: The God of Order\n"
    content += f"- Scripture reveals {len(themes)} consistent patterns\n"
    content += f"- {coverage:.1f}% of our text demonstrates divine design\n"
    content += "- *\"God is not a God of confusion but of peace\"* (1 Cor 14:33)\n\n"
    
    content += "### II. Main Points:\n\n"
    for i, theme in enumerate(themes[:4], 1):
        content += f"**{i}. The Pattern of {theme.title()}**\n"
        content += f"   - Biblical foundation and evidence\n"
        content += f"   - Practical application for believers\n"
        content += f"   - Connection to Gospel message\n\n"
    
    if evidence:
        content += "### III. Supporting Evidence:\n\n"
        for fragment in evidence[:3]:
            content += f"- *\"{fragment}\"*\n"
        content += "\n"
    
    content += "### IV. Application:\n"
    content += "- How these patterns guide our daily walk\n"
    content += "- Trust in God's consistent character\n"
    content += "- Finding peace in divine order\n\n"
    
    content += "### V. Conclusion:\n"
    content += "- God's patterns endure across generations\n"
    content += "- We can trust His unchanging nature\n"
    content += "- *\"Jesus Christ is the same yesterday, today, and forever\"* (Heb 13:8)\n\n"
    
    content += "**Closing Prayer:** *In Jesus' name. Amen.*\n\n"
    
    return content

def generate_default_content(themes, evidence, coverage, chain_meta):
    """Generate default creative content when form is unrecognized"""
    content = "## Creative Reflection on Divine Patterns\n\n"
    
    content += f"In studying the sacred text, I have discovered {len(themes)} patterns "
    content += f"that reveal God's consistent character and eternal purposes.\n\n"
    
    content += "### Discovered Themes:\n"
    for theme in themes:
        content += f"- {theme.title()}\n"
    
    content += f"\n### Analysis Summary:\n"
    content += f"These patterns emerge with {coverage:.1f}% clarity across the examined text, "
    content += f"suggesting intentional divine design rather than random occurrence.\n\n"
    
    if evidence:
        content += "### Key Evidence:\n"
        for fragment in evidence[:3]:
            content += f"> {fragment}\n\n"
    
    content += "### Conclusion:\n"
    content += "The God who established patterns in creation continues to reveal Himself "
    content += "through consistent themes in His Word. These discoveries strengthen our "
    content += "faith in His unchanging character.\n\n"
    
    content += "*In Jesus' name. Amen.*\n\n"
    
    return content

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

    # Generate actual creative content based on form
    body = generate_creative_content(form, patterns, rvp, chain_meta)
    body += "\n\n"

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
