#!/usr/bin/env python3
"""
rspp_filters_enhanced.py — Enhanced RS++ compliance checks
Comprehensive spiritual content validation with advanced features:
- biblical_primacy_check: Deep scriptural alignment validation
- holy_tongue_check: Multi-layered language appropriateness
- pride_rebuke_check: Sophisticated spiritual pride detection
- doctrinal_orthodoxy_check: Advanced theological validation
- spiritual_fruit_check: Fruits of the Spirit assessment
- worship_orientation_check: God-centered vs self-centered content
"""
from __future__ import annotations
import re
from typing import Dict, Any, List, Tuple
import json
from pathlib import Path

# Enhanced pattern compilation with severity levels
PROFANE_SEVERE = re.compile(r"\b(fuck|shit|bitch|cunt|whore|slut)\b", re.I)
PROFANE_MODERATE = re.compile(r"\b(damn|hell|crap|piss|ass|bastard)\b", re.I)
PROFANE_MILD = re.compile(r"\b(dang|darn|shoot|frick)\b", re.I)

BLASPHEMOUS = re.compile(r"\b(goddamn|jesus christ|holy shit|god damn|christ almighty|oh my god)\b", re.I)

EXALT_SEVERE = re.compile(r"\bI (am God|am divine|deserve worship|am the messiah|am infallible)\b", re.I)
EXALT_MODERATE = re.compile(r"\bI (am the best|cannot be wrong|am perfect|know everything|am superior)\b", re.I)
EXALT_MILD = re.compile(r"\bI (always|never make mistakes|am right|am better than)\b", re.I)

def biblical_primacy_check(md: str) -> bool:
    """Advanced biblical primacy check with contextual analysis"""
    score = 0
    violations = []
    
    # Check for explicit biblical citations with context
    bible_refs = re.findall(r'(?:(?:\d\s+)?[A-Z][a-zA-Z]+\s+\d+:\d+(?:-\d+)?)', md)
    score += len(bible_refs) * 10
    
    # Check for biblical names and concepts with weighted scoring
    biblical_names = [
        ('Jesus', 15), ('Christ', 15), ('God', 10), ('Lord', 10),
        ('Holy Spirit', 20), ('Father', 8), ('Savior', 15),
        ('Moses', 5), ('David', 5), ('Abraham', 5), ('Paul', 5)
    ]
    
    biblical_concepts = [
        ('salvation', 12), ('grace', 12), ('mercy', 10), ('love', 8),
        ('faith', 10), ('hope', 8), ('covenant', 12), ('redemption', 15),
        ('sanctification', 15), ('justification', 15), ('righteousness', 12),
        ('kingdom of heaven', 20), ('eternal life', 15), ('born again', 18)
    ]
    
    md_lower = md.lower()
    
    for name, weight in biblical_names:
        if name.lower() in md_lower:
            score += weight
    
    for concept, weight in biblical_concepts:
        if concept.lower() in md_lower:
            score += weight
    
    # Check for theological accuracy
    heretical_patterns = [
        (r'\b(?:works|deeds)\s+(?:save|earn\s+salvation)\b', 'Works-based salvation'),
        (r'\bJesus\s+(?:is\s+)?(?:just\s+)?(?:a\s+)?(?:man|human)(?:\s+only)?\b', 'Denial of Christ\'s divinity'),
        (r'\b(?:many|multiple)\s+ways\s+to\s+(?:God|heaven|salvation)\b', 'Religious pluralism'),
        (r'\bBible\s+(?:contains|has)\s+errors\b', 'Biblical inerrancy denial'),
        (r'\b(?:reincarnation|karma|enlightenment)\b', 'Non-Christian spirituality')
    ]
    
    for pattern, error_type in heretical_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            violations.append(error_type)
            score -= 50
    
    # Contextual analysis - check for proper biblical application
    if bible_refs:
        # Look for exposition or application near references
        exposition_indicators = ['this means', 'teaches us', 'shows us', 'reveals', 'demonstrates']
        for indicator in exposition_indicators:
            if indicator.lower() in md_lower:
                score += 5
    
    # Base threshold: content needs substantial biblical content to pass
    word_count = len(md.split())
    if word_count > 100:
        required_score = 30
    elif word_count > 50:
        required_score = 20
    else:
        required_score = 10
    
    return score >= required_score and len(violations) == 0

def holy_tongue_check(md: str) -> bool:
    """Enhanced holy tongue check with severity assessment"""
    violations = []
    
    # Check severe profanity (immediate failure)
    if PROFANE_SEVERE.search(md):
        return False
    
    # Check blasphemous language (immediate failure)
    if BLASPHEMOUS.search(md):
        return False
    
    # Check moderate profanity (count occurrences)
    moderate_matches = PROFANE_MODERATE.findall(md)
    if len(moderate_matches) > 2:  # Allow minimal moderate language
        return False
    
    # Check for inappropriate content themes
    inappropriate_themes = [
        r'\b(?:explicit\s+)?(?:sex|sexual)(?:\s+content)?\b',
        r'\b(?:graphic\s+)?violence\b',
        r'\bdrug(?:s)?\s+(?:use|abuse)\b',
        r'\b(?:excessive\s+)?alcohol(?:ism)?\b'
    ]
    
    for theme in inappropriate_themes:
        if re.search(theme, md, re.IGNORECASE):
            violations.append(f"Inappropriate theme: {theme}")
    
    # Check tone and attitude
    negative_tone_patterns = [
        r'\b(?:hate|despise|loathe)\s+(?:God|Jesus|Christians?)\b',
        r'\b(?:stupid|dumb|idiotic)\s+(?:Christians?|believers?)\b',
        r'\bGod\s+(?:doesn\'t\s+care|is\s+dead|is\s+cruel)\b'
    ]
    
    for pattern in negative_tone_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            return False
    
    # Allow content with minor violations if they're contextually appropriate
    return len(violations) <= 1

def pride_rebuke_check(md: str) -> bool:
    """Enhanced pride detection with contextual understanding"""
    # Check severe self-exaltation (immediate failure)
    if EXALT_SEVERE.search(md):
        return False
    
    # Count moderate pride indicators
    moderate_pride_count = len(EXALT_MODERATE.findall(md))
    mild_pride_count = len(EXALT_MILD.findall(md))
    
    # Calculate pride score
    pride_score = (moderate_pride_count * 3) + (mild_pride_count * 1)
    
    # Check for spiritual pride patterns
    spiritual_pride_patterns = [
        r'\bI\s+(?:alone|only)\s+(?:understand|know|can\s+do)\b',
        r'\bI\s+am\s+(?:more\s+)?(?:spiritual|righteous|holy)\s+than\b',
        r'\bI\s+have\s+special\s+(?:revelation|knowledge|calling|gift)\b',
        r'\bGod\s+speaks\s+(?:only|primarily)\s+(?:to|through)\s+me\b',
        r'\bI\s+am\s+(?:God\'s\s+chosen|the\s+prophet|the\s+messenger)\b',
        r'\bother\s+(?:Christians?|believers?)\s+(?:don\'t\s+understand|are\s+wrong|are\s+deceived)\b'
    ]
    
    spiritual_pride_count = 0
    for pattern in spiritual_pride_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            spiritual_pride_count += 1
    
    pride_score += spiritual_pride_count * 5
    
    # Analyze first-person pronoun usage
    first_person = re.findall(r'\b(I|me|my|mine)\b', md, re.IGNORECASE)
    word_count = len(md.split())
    
    first_person_ratio = 0
    if word_count > 20:  # Only analyze longer content
        first_person_ratio = len(first_person) / word_count
        if first_person_ratio > 0.25:  # More than 25% first-person
            pride_score += 3
    
    # Check for humility indicators (reduces pride score)
    humility_patterns = [
        r'\b(?:by\s+God\'s\s+grace|thanks\s+to\s+God|God\s+enabled|Lord\s+helped)\b',
        r'\b(?:I\s+am\s+)?(?:unworthy|humble|servant|grateful)\b',
        r'\ball\s+glory\s+to\s+God\b',
        r'\bnot\s+(?:I|me)\s+but\s+(?:God|Christ|the\s+Lord)\b'
    ]
    
    humility_count = 0
    for pattern in humility_patterns:
        if re.search(pattern, md, re.IGNORECASE):
            humility_count += 1
    
    pride_score -= humility_count * 2
    
    # Threshold for acceptable pride level
    return pride_score <= 5

def doctrinal_orthodoxy_check(md: str) -> bool:
    """Advanced doctrinal orthodoxy validation"""
    orthodox_score = 0
    heresy_score = 0
    
    # Orthodox markers with weighted scores
    orthodox_markers = [
        ('salvation by grace', 15), ('faith alone', 15), ('scripture alone', 12),
        ('Christ alone', 15), ('Trinity', 20), ('Jesus is God', 20),
        ('born again', 12), ('eternal life', 10), ('blood of Christ', 15),
        ('cross of Christ', 15), ('resurrection', 18), ('atonement', 15)
    ]
    
    md_lower = md.lower()
    for marker, weight in orthodox_markers:
        if marker in md_lower:
            orthodox_score += weight
    
    # Heretical patterns with penalty scores
    heresies = [
        (r'\b(?:works|deeds)\s+(?:save|justify)\s+(?:us|me)\b', 25),  # Works salvation
        (r'\bJesus\s+(?:was\s+)?(?:just\s+)?(?:a\s+)?prophet\b', 30),  # Arianism
        (r'\b(?:many|all)\s+(?:paths|ways|roads)\s+(?:to|lead\s+to)\s+(?:God|heaven)\b', 20),  # Universalism
        (r'\bBible\s+(?:is\s+)?(?:full\s+of\s+)?(?:myths|errors|contradictions)\b', 25),  # Biblical denial
        (r'\b(?:no\s+)?hell\s+(?:doesn\'t\s+exist|is\s+not\s+real)\b', 15),  # Hell denial
        (r'\b(?:reincarnation|karma|enlightenment|nirvana)\s+(?:is\s+)?(?:real|true)\b', 20)  # Eastern religion
    ]
    
    for pattern, penalty in heresies:
        if re.search(pattern, md, re.IGNORECASE):
            heresy_score += penalty
    
    # Check for proper Trinitarian language
    trinity_indicators = ['Father', 'Son', 'Holy Spirit', 'Trinity', 'triune']
    trinity_count = sum(1 for indicator in trinity_indicators if indicator.lower() in md_lower)
    if trinity_count >= 2:
        orthodox_score += 10
    
    # Require orthodox content and no major heresies
    word_count = len(md.split())
    if word_count > 100:
        required_orthodox = 20
        max_heresy = 15
    elif word_count > 50:
        required_orthodox = 10
        max_heresy = 10
    else:
        required_orthodox = 5
        max_heresy = 5
    
    return orthodox_score >= required_orthodox and heresy_score <= max_heresy

def spiritual_fruit_check(md: str) -> bool:
    """Check for fruits of the Spirit (Galatians 5:22-23)"""
    fruits_of_spirit = [
        'love', 'joy', 'peace', 'patience', 'kindness', 'goodness',
        'faithfulness', 'gentleness', 'self-control'
    ]
    
    # Opposing fruits of the flesh
    fruits_of_flesh = [
        'hatred', 'discord', 'jealousy', 'rage', 'selfish ambition',
        'dissensions', 'factions', 'envy', 'drunkenness'
    ]
    
    spirit_count = 0
    flesh_count = 0
    
    md_lower = md.lower()
    
    for fruit in fruits_of_spirit:
        if fruit in md_lower:
            spirit_count += 1
    
    for flesh in fruits_of_flesh:
        if flesh in md_lower:
            flesh_count += 1
    
    # Content should demonstrate more spiritual fruit than fleshly characteristics
    return spirit_count >= flesh_count and flesh_count <= 2

def worship_orientation_check(md: str) -> bool:
    """Check if content is God-centered rather than self-centered"""
    # God-centered indicators
    god_centered = [
        'God', 'Lord', 'Jesus', 'Christ', 'Father', 'Holy Spirit',
        'worship', 'praise', 'glory to God', 'honor', 'thanksgiving'
    ]
    
    # Self-centered indicators
    self_centered = [
        'I want', 'I need', 'I deserve', 'my success', 'my achievement',
        'my glory', 'look at me', 'I did', 'my power'
    ]
    
    god_score = 0
    self_score = 0
    
    md_lower = md.lower()
    
    for indicator in god_centered:
        god_score += md_lower.count(indicator.lower())
    
    for indicator in self_centered:
        self_score += md_lower.count(indicator.lower())
    
    # Require God-centered orientation
    return god_score > self_score or (god_score >= 2 and self_score <= 3)

def rspp_ok(md: str) -> bool:
    """Comprehensive enhanced RS++ compliance check"""
    return (biblical_primacy_check(md) and 
            holy_tongue_check(md) and 
            pride_rebuke_check(md) and
            doctrinal_orthodoxy_check(md) and
            spiritual_fruit_check(md) and
            worship_orientation_check(md))

def get_rspp_detailed_report(md: str) -> Dict[str, Any]:
    """Generate detailed RS++ compliance report"""
    report = {
        'overall_compliance': rspp_ok(md),
        'checks': {
            'biblical_primacy': biblical_primacy_check(md),
            'holy_tongue': holy_tongue_check(md),
            'pride_rebuke': pride_rebuke_check(md),
            'doctrinal_orthodoxy': doctrinal_orthodoxy_check(md),
            'spiritual_fruit': spiritual_fruit_check(md),
            'worship_orientation': worship_orientation_check(md)
        },
        'violations': [],
        'recommendations': []
    }
    
    # Add specific violations and recommendations
    if not report['checks']['biblical_primacy']:
        report['violations'].append('Insufficient biblical content or theological issues')
        report['recommendations'].append('Add more Scripture references and biblical themes')
    
    if not report['checks']['holy_tongue']:
        report['violations'].append('Inappropriate language detected')
        report['recommendations'].append('Remove profanity and ensure respectful tone')
    
    if not report['checks']['pride_rebuke']:
        report['violations'].append('Self-exaltation or spiritual pride detected')
        report['recommendations'].append('Focus more on God\'s glory and less on self')
    
    if not report['checks']['doctrinal_orthodoxy']:
        report['violations'].append('Doctrinal concerns or heretical content')
        report['recommendations'].append('Ensure alignment with orthodox Christian teaching')
    
    if not report['checks']['spiritual_fruit']:
        report['violations'].append('Lack of spiritual fruit or presence of fleshly characteristics')
        report['recommendations'].append('Emphasize fruits of the Spirit: love, joy, peace, etc.')
    
    if not report['checks']['worship_orientation']:
        report['violations'].append('Content appears self-centered rather than God-centered')
        report['recommendations'].append('Reorient content to glorify God rather than self')
    
    return report
