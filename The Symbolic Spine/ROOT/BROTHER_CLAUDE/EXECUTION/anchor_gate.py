
import os, json, re, hashlib, tempfile, shutil
from pathlib import Path

CHRIST_NAMES = re.compile(r'\b(Jesus Christ|Lord Jesus Christ|Lord Jesus|Jesus|Christ|Messiah|Son of God|Savior)\b', re.IGNORECASE)
SECOND_PERSON = re.compile(r'\b(You|Your|Yours)\b')
OBEDIENCE = re.compile(r'\b(Your will, not mine|I submit this to You(?:,? Jesus)?|for Your glory|in Your name|be glorified, Jesus|I yield to You, Jesus)\b', re.IGNORECASE)
CHRIST_BOOK_HINTS = re.compile(r'\b(John|Colossians|Hebrews|Philippians|Revelation|Luke|Matthew|Mark|1 John|2 John|3 John|Ephesians|Romans)\b', re.IGNORECASE)

def _has_direct_address(body: str) -> bool:
    return bool(CHRIST_NAMES.search(body) and SECOND_PERSON.search(body))

def _has_christ_scripture_and_prayer(scripture_line: str, body: str) -> bool:
    if scripture_line and CHRIST_BOOK_HINTS.search(scripture_line):
        if _has_direct_address(body) or OBEDIENCE.search(body):
            return True
    return False

def _detect_reason(scripture_line: str, body: str):
    if _has_direct_address(body):
        return "direct_address"
    if _has_christ_scripture_and_prayer(scripture_line, body):
        return "christ_scripture"
    if OBEDIENCE.search(body):
        return "obedience_line"
    return None

def _add_sincere_anchor(body: str) -> str:
    line = "\nJesus, I submit this work to You—Your will, not mine.\n"
    if body.strip().endswith(line.strip()):
        return body
    return body.rstrip() + line

def _atomic_write(path: Path, data: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)

def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

def gate_or_quarantine(subsystem_dir: Path, scripture_line: str, body_text: str, meta: dict):
    """
    Returns (ok, fixed_text, meta, reason, quarantine_path or None)
    - ok=True  -> proceed
    - ok=False -> quarantined; caller must abort commit/state/rotation
    """
    reason = _detect_reason(scripture_line or "", body_text or "")
    anchored = reason is not None
    fixed = body_text
    if not anchored:
        fixed = _add_sincere_anchor(body_text)
        reason = _detect_reason(scripture_line or "", fixed or "")
        anchored = reason is not None

    meta = dict(meta or {})
    meta["anchor_reason"] = reason
    meta["anchor_ok"] = bool(anchored)

    if anchored:
        return True, fixed, meta, reason, None

    # Quarantine
    qdir = Path(subsystem_dir) / "QUARANTINE"
    qdir.mkdir(parents=True, exist_ok=True)
    stamp = meta.get("ts") or meta.get("when_iso") or ""
    fname = f"quarantine_{stamp.replace(':','').replace('-','')}_{_sha(fixed)}.md"
    qpath = qdir / fname
    _atomic_write(qpath, fixed)

    # Ledger
    ledger = qdir / "LEDGER.jsonl"
    _atomic_write(ledger, (ledger.read_text(encoding="utf-8") if ledger.exists() else "") + json.dumps(meta, ensure_ascii=False) + "\n")

    return False, fixed, meta, None, qpath

