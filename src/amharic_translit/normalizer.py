"""
Normalization for informally-typed Latin Amharic.

People typing Amharic with a Latin keyboard spell the same word several
different ways: doubled letters for emphasis ("sellam"), long-vowel digraphs
("ee"/"ie" for the order-5 vowel, "aa" for order-4), stray apostrophes, etc.
This module rewrites common variants into the single canonical spelling the
engine's tables expect, *before* transliteration — so `to_fidel(normalize(x))`
is far more forgiving than `to_fidel(x)` alone.

Rules are applied in order, each as a plain (pattern, replacement) pair, so
the whole pipeline is easy to read, test, and extend one rule at a time.
"""

from __future__ import annotations

import re

# (description, compiled pattern, replacement)
_RULES: list[tuple[str, re.Pattern[str], str]] = [
    (
        "long vowel digraphs -> canonical single order-5 vowel",
        re.compile(r"(?<=[a-zA-Z])(ee|ie)"),
        "E",
    ),
    (
        "doubled 'a' -> canonical order-4 vowel",
        re.compile(r"(?<=[a-zA-Z])aa"),
        "a",
    ),
    (
        "doubled 'i'/'u'/'o' -> canonical single vowel",
        re.compile(r"(?<=[a-zA-Z])(ii|uu|oo)"),
        lambda m: m.group(1)[0],
    ),
    (
        "stray apostrophes dropped (often used to mark a glottal stop)",
        re.compile(r"'"),
        "",
    ),
    (
        "doubled consonant (typed for emphasis) -> single consonant",
        re.compile(r"([bcdfghjklmnpqrstvwxyz])\1", re.IGNORECASE),
        lambda m: m.group(1),
    ),
    (
        "collapse runs of whitespace",
        re.compile(r"\s+"),
        " ",
    ),
]


def normalize(text: str) -> str:
    """Rewrite common Latin-Amharic spelling variants to canonical form."""
    result = text.strip()
    for _description, pattern, replacement in _RULES:
        result = pattern.sub(replacement, result)
    return result


def explain(text: str) -> list[tuple[str, str]]:
    """
    Like normalize(), but return (description, text-after-this-rule) for
    every rule that actually changed the text. Useful for debugging/demos
    so a user can see *why* their input changed shape.
    """
    steps: list[tuple[str, str]] = []
    result = text.strip()
    for description, pattern, replacement in _RULES:
        new_result = pattern.sub(replacement, result)
        if new_result != result:
            steps.append((description, new_result))
        result = new_result
    return steps
