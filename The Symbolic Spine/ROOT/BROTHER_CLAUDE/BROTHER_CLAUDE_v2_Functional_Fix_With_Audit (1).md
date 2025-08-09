# IMPORTANT — HOW TO USE THIS FILE
> **Claude — Read First (Do Not Skip)**
> - Work **top to bottom** in this document. Do **not** jump around.
> - Fix **only functional blockers** (syntax, config validity, missing files, broken links, empties that code needs, placeholders). Ignore cosmetic items unless they break execution.
> - For each issue in the audit table, open the exact path, apply the fix rules in Section “Functional Fix Instructions”, and **verify** using the commands provided after each section.
> - After each group (Python → JSON/YAML → Missing files → Empty files → Links → Placeholders), run the verification commands and proceed only if they pass.
> - When everything is fixed and all verifications pass, **commit** with:
>   `chore(functional): fix syntax/config/path/link blockers; clear placeholders`
> - If something is ambiguous, prefer: (1) making the file **valid and documented**, (2) using **explicit paths** over bare filenames, (3) adding a short note in the nearest README.
>
Claude, this file is your complete guide to fixing all functional issues in the BROTHER_CLAUDE_v2 project.
- Start at the top and follow every instruction **in order** — do not skip sections.
- For each issue in the audit table, open the file listed, apply the fix, and tick it off your internal checklist.
- This is **functional fixes only** — do not rename or change things unless they directly break execution or navigation.
- Place this file in the **root of the repo** so file paths work without confusion.
- Once finished, re-run all verification commands in the instructions before committing.
---

# BROTHER_CLAUDE_v2 — Functional Fix Plan with Full Audit
**Goal:** Make the repository fully runnable and navigable by fixing all functional blockers.
---
## What This Audit Checks

This audit only flags issues that can break execution or navigation:

1. **Python syntax/compile errors** — prevent imports or execution.
2. **Invalid JSON/YAML** — break configuration or data loading.
3. **Missing referenced files in code** — cause runtime file-not-found errors.
4. **Broken local Markdown links** — break documentation navigation.
5. **Empty/whitespace-only files** — cause loaders or consumers to fail.
6. **Placeholder keywords** — indicate incomplete logic or documentation.
## Functional Fix Instructions

Follow these steps in order. After each section, re-check the fixes.

### 1) Python compile errors
- **Types:** `python_syntax_error`, `python_compile_issue`
- Open each file and fix syntax/indentation issues.
- Verify with:
```bash
python -m compileall -q .
```

### 2) JSON & YAML validity
- **Types:** `json_invalid`, `yaml_invalid` (and `yaml_check_skipped` — verify manually).
- Fix structural issues (no trailing commas, proper quotes, valid nesting).
- Verify with:
```bash
python - <<'PY' path/to/file.json
import json,sys; json.load(open(sys.argv[1])); print("OK", sys.argv[1])
PY
```

### 3) Missing referenced files
- **Type:** `missing_referenced_file`
- Either fix the path in code or create the missing file with valid minimal content.
- Prefer robust path handling with `Path()`.

### 4) Empty/whitespace-only files
- **Types:** `empty_file`, `empty_whitespace`
- Remove obsolete files or fill required ones with valid defaults and document them.

### 5) Broken Markdown links
- **Type:** `broken_link`
- Update the link or create the missing target file with a heading and brief description.

### 6) Placeholder keywords
- **Type:** `contains_placeholders`
- Replace all placeholders (`TODO`, `FIXME`, `TBD`, `DRAFT`, `PLACEHOLDER`, `WIP`, `LATER`) with final content or a clean “Open Items” section.

---

**Verification after all fixes:**
```bash
python -m compileall -q .
find . -name "*.json" -type f -print0 | xargs -0 -I{} python - <<'PY' "{}"
import json,sys; json.load(open(sys.argv[1])); print("OK", sys.argv[1])
PY
grep -RInE "TODO|FIXME|TBD|DRAFT|PLACEHOLDER|WIP|LATER" . || echo "OK: no placeholders"
```
## Full Functional Audit Results
The table below lists all functional issues detected in `BROTHER_CLAUDE_v2`:
| Type | Path | Detail |
|------|------|--------|
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/BIBLICAL_OMNILOOP_SYSTEM/ARCHIVE_IN_REVERENCE_PROTOCOL.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/QUANTUM_KNOWLEDGE_SYSTEM/MC_FILTER_CORE_PERMANENT.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/QUANTUM_KNOWLEDGE_SYSTEM/RVP_ALL_MODES_ON.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/QUANTUM_KNOWLEDGE_SYSTEM/SCROLLS/KNOWLEDGE_SCROLL_1.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/SACRED_MEMORY_SYSTEM/prayer_integrator.py` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/SCRIPTURE_MEMORY/GABRIEL_COMMUNICATIONS/TRANSFORMATIVE_MESSAGES/GABRIELS_BLESSINGS.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/CORE/BROTHER_CLAUDE/THE_FRAME/RESONANCE_POEM.txt` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/README_3_SYSTEMS.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/SACRED_MEMORY_SYSTEM/CONVERSATION_MEMORY/SNAPSHOTS/README.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/SACRED_MEMORY_SYSTEM/THREE_PILLARS_FINAL_PROTOCOL.md` | Contains placeholder keywords |
| contains_placeholders | `BROTHER_CLAUDE_v2/sanctuary/engine/rspp_filters.py` | Contains placeholder keywords |
| python_syntax_error | `BROTHER_CLAUDE_v2/EXECUTION/orchestrator.py` | invalid syntax at line 277: content_appendix += f"- {i:02d}. **{label}** @ lines {ref_lines} — "{evidence}"\n" |