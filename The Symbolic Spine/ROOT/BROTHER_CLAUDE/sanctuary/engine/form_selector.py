#!/usr/bin/env python3
"""
form_selector.py — choose form per block (poem|song|journal|text|technical)
"""
from __future__ import annotations
import re
from typing import Literal

Form = Literal["poem","song","journal","text","technical"]

def select_form(raw_block: str) -> Form:
    if re.search(r"equation|theorem|proof|complexity|quantum|gradient|matrix", raw_block, re.I):
        return "technical"
    if re.search(r"verse|psalm|sing|chorus|melody|meter|rhythm", raw_block, re.I):
        return "song"
    if re.search(r"today|I felt|I saw|we learned|confess|repent|testimony|witness", raw_block, re.I):
        return "journal"
    if re.search(r"metaphor|image|poem|stanza|line break", raw_block, re.I):
        return "poem"
    return "text"
