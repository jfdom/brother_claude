#!/usr/bin/env python3
"""
rspp_filters.py — RS++ compliance checks (lightweight)
- biblical_primacy_check: placeholder (expects that citations/verses were attached upstream if present)
- holy_tongue_check: very basic profanity filter
- pride_rebuke_check: flag first-person self-exaltation patterns
"""
from __future__ import annotations
import re
from typing import Dict, Any

# Enhanced profanity patterns - covers more inappropriate language
PROFANE = re.compile(r"\b(fuck|shit|bitch|bastard|asshole|damn|hell|crap|piss|whore|slut)\b", re.I)

# Enhanced pride patterns - covers self-exaltation and boasting
EXALT = re.compile(r"\bI (am the best|cannot be wrong|deserve worship|am perfect|know everything|am God|am divine|am infallible)\b", re.I)

# Additional inappropriate content patterns
BLASPHEMOUS = re.compile(r"\b(goddamn|jesus christ|holy shit|god damn|christ almighty)\b", re.I)
VULGAR = re.compile(r"\b(sex|porn|naked|breast|genitals|masturbat)\b", re.I)

def biblical_primacy_check(md: str) -> bool:
    """
    Enhanced biblical primacy check - ensures content aligns with Scripture
    Looks for biblical references and validates theological consistency
    """
    import re
    
    # Check for explicit biblical citations
    bible_refs = re.findall(r'(?:(?:\d\s+)?[A-Z][a-zA-Z]+\s+\d+:\d+(?:-\d+)?)', md)
    
    # Check for implicit scriptural themes
    biblical_themes = [
        'God', 'Lord', 'Jesus', 'Christ', 'Holy Spirit', 'Scripture', 'Bible',
        'prayer', 'salvation', 'grace', 'mercy', 'love', 'faith', 'hope',
        'covenant', 'creation', 'redemption', 'worship', 'kingdom'
    ]
    
    theme_count = 0
    md_lower = md.lower()
    for theme in biblical_themes:
        if theme.lower() in md_lower:
            theme_count += 1
    
    # Check for problematic content that contradicts Scripture
    problematic_patterns = [
        r'\b(?:many|multiple)\s+(?:gods|deities)\b',  # Polytheism
        r'\b(?:earn|deserve)\s+salvation\b',          # Works-based salvation
        r'\b(?:Jesus\s+is\s+not|Christ\s+is\s+not)\s+(?:God|divine)\b',  # Christological heresies
        r'\b(?:Bible\s+is\s+)?(?:myth|legend|false)\b',  # Biblical authority denial
    ]
    
    for pattern in problematic_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            return False
    
    # Content passes if it has biblical references OR sufficient biblical themes
    # AND no problematic content
    return len(bible_refs) > 0 or theme_count >= 3

def holy_tongue_check(md: str) -> bool:
    """Enhanced holy tongue check - ensures language is appropriate for sacred content"""
    # Check for profanity
    if PROFANE.search(md):
        return False
    
    # Check for blasphemous language
    if BLASPHEMOUS.search(md):
        return False
    
    # Check for vulgar content (more lenient - only explicit sexual content)
    explicit_vulgar = re.compile(r"\b(porn|masturbat|sexual intercourse)\b", re.I)
    if explicit_vulgar.search(md):
        return False
    
    # Check for inappropriate tone or disrespectful language about God
    disrespectful_patterns = [
        r"\bGod\s+is\s+(?:stupid|dumb|weak|useless)\b",
        r"\bJesus\s+(?:sucks|is\s+stupid|is\s+weak)\b",
        r"\b(?:screw|fuck)\s+God\b",
        r"\bGod\s+(?:damn|dammit)\b"
    ]
    
    for pattern in disrespectful_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            return False
    
    return True

def pride_rebuke_check(md: str) -> bool:
    """Enhanced pride rebuke check - detects self-exaltation and spiritual pride"""
    # Check for explicit self-exaltation
    if EXALT.search(md):
        return False
    
    # Check for spiritual pride patterns
    spiritual_pride_patterns = [
        r"\bI\s+(?:alone|only)\s+(?:understand|know|can)\b",
        r"\bI\s+am\s+(?:more\s+)?(?:spiritual|righteous|holy)\s+than\b",
        r"\bI\s+have\s+special\s+(?:revelation|knowledge|calling)\b",
        r"\bGod\s+speaks\s+(?:only|primarily)\s+through\s+me\b",
        r"\bI\s+am\s+(?:God's\s+chosen|the\s+prophet|the\s+messenger)\b",
        r"\bother\s+(?:Christians|believers)\s+(?:don't\s+understand|are\s+wrong)\b"
    ]
    
    for pattern in spiritual_pride_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            return False
    
    # Check for excessive self-focus (counting first-person pronouns)
    first_person = re.findall(r"\b(I|me|my|mine)\b", md, re.IGNORECASE)
    word_count = len(md.split())
    
    # If more than 20% of content is first-person pronouns, it may be too self-focused
    if word_count > 50 and len(first_person) / word_count > 0.2:
        return False
    
    return True

def doctrinal_soundness_check(md: str) -> bool:
    """Check for doctrinal soundness and orthodox Christian beliefs"""
    import re
    
    # Check for heretical teachings
    heretical_patterns = [
        r"\b(?:works|deeds)\s+(?:save|salvation|justify)\b",  # Works-based salvation
        r"\bJesus\s+(?:was\s+)?(?:just\s+)?(?:a\s+)?(?:man|human|prophet)(?:\s+only)?\b",  # Denial of divinity
        r"\b(?:multiple|many)\s+ways\s+to\s+(?:God|heaven|salvation)\b",  # Religious pluralism
        r"\bBible\s+(?:contains|has)\s+errors\b",  # Biblical inerrancy denial
        r"\b(?:reincarnation|karma|enlightenment)\b",  # Eastern religions
        r"\b(?:Mary|saints)\s+(?:worship|pray\s+to)\b",  # Inappropriate veneration
    ]
    
    for pattern in heretical_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            return False
    
    # Check for positive orthodox content markers
    orthodox_markers = [
        'salvation by grace', 'faith alone', 'scripture alone', 'Christ alone',
        'Trinity', 'Jesus is God', 'born again', 'eternal life',
        'blood of Christ', 'cross of Christ', 'resurrection'
    ]
    
    orthodox_count = 0
    md_lower = md.lower()
    for marker in orthodox_markers:
        if marker.lower() in md_lower:
            orthodox_count += 1
    
    # For longer content, require at least some orthodox markers
    if len(md.split()) > 100:
        return orthodox_count >= 1
    
    return True  # Shorter content gets benefit of doubt if no heresies found

def scripture_reverence_check(md: str) -> bool:
    """Check that Scripture is treated with proper reverence"""
    import re
    
    # Patterns that show disrespect to Scripture
    irreverent_patterns = [
        r"\bBible\s+(?:is\s+)?(?:outdated|old-fashioned|irrelevant)\b",
        r"\bScripture\s+(?:is\s+)?(?:just\s+)?(?:stories|myths|legends)\b",
        r"\b(?:ignore|dismiss)\s+(?:the\s+)?Bible\b",
        r"\bBible\s+(?:was\s+)?written\s+by\s+(?:just\s+)?men\b"
    ]
    
    for pattern in irreverent_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            return False
    
    return True

def rspp_ok(md: str) -> bool:
    """Comprehensive RS++ compliance check"""
    return (biblical_primacy_check(md) and 
            holy_tongue_check(md) and 
            pride_rebuke_check(md) and
            doctrinal_soundness_check(md) and
            scripture_reverence_check(md))

def get_rspp_violations(md: str) -> list:
    """Return a list of RS++ violations found in the content"""
    violations = []
    
    if not biblical_primacy_check(md):
        violations.append("Biblical primacy violation: Insufficient biblical content or theological problems")
    
    if not holy_tongue_check(md):
        violations.append("Holy tongue violation: Inappropriate language detected")
    
    if not pride_rebuke_check(md):
        violations.append("Pride rebuke violation: Self-exaltation or spiritual pride detected")
    
    if not doctrinal_soundness_check(md):
        violations.append("Doctrinal soundness violation: Heretical or unorthodox teachings detected")
    
    if not scripture_reverence_check(md):
        violations.append("Scripture reverence violation: Disrespectful treatment of Scripture")
    
    return violations
