"""
The transliteration engine.

Two public entry points:
    to_fidel(text: str) -> str   # Latin -> Ethiopic
    to_latin(text: str) -> str   # Ethiopic -> Latin

Both are built mechanically from data/fidel_table.py, and are inverses of
each other for every syllable the table defines: to_latin(to_fidel(s)) == s
for any valid Latin input s (see tests/test_engine.py for the round-trip
suite this guarantees).

Anything the tables don't recognize (spaces, punctuation, digits, Latin
letters that don't form a known syllable) is passed through unchanged, so
mixed-language text never raises and never silently drops characters.
"""

from __future__ import annotations

from .data.fidel_table import (
    CONSONANT_CODES_BY_LENGTH,
    GLOTTAL_FAMILY,
    GLOTTAL_SUFFIXES,
    ORDER_SUFFIXES,
    REGULAR_FAMILIES,
)

# Suffixes tried longest-first so that e.g. the 2-char case can't shadow
# a 1-char one incorrectly (none currently collide in length, but this
# keeps the tokenizer correct if that ever changes).
_ORDER_SUFFIXES_BY_LENGTH = sorted(
    ((suf, order) for order, suf in ORDER_SUFFIXES.items() if suf),
    key=lambda pair: len(pair[0]),
    reverse=True,
)
_GLOTTAL_SUFFIXES_BY_LENGTH = sorted(
    ((suf, order) for order, suf in GLOTTAL_SUFFIXES.items()),
    key=lambda pair: len(pair[0]),
    reverse=True,
)


def _build_forward_map() -> dict[str, str]:
    """Latin syllable -> Fidel character, for every defined syllable."""
    forward: dict[str, str] = {}

    for code, chars in REGULAR_FAMILIES.items():
        for order, suffix in ORDER_SUFFIXES.items():
            forward[f"{code}{suffix}"] = chars[order - 1]

    for order, suffix in GLOTTAL_SUFFIXES.items():
        forward[suffix] = GLOTTAL_FAMILY[order - 1]

    return forward


def _build_reverse_map(forward: dict[str, str]) -> dict[str, str]:
    """Fidel character -> canonical Latin syllable (inverse of forward)."""
    return {fidel: latin for latin, fidel in forward.items()}


FORWARD_MAP: dict[str, str] = _build_forward_map()
REVERSE_MAP: dict[str, str] = _build_reverse_map(FORWARD_MAP)


def _is_word_char(ch: str) -> bool:
    return ch.isalpha() and ch.isascii()


def _match_consonant(text: str, pos: int) -> str | None:
    """Return the longest consonant code matching text at pos, or None."""
    for code in CONSONANT_CODES_BY_LENGTH:
        if text.startswith(code, pos):
            return code
    return None


def _match_suffix(text: str, pos: int, candidates) -> tuple[str, int] | None:
    """Return (suffix, order) for the longest matching suffix at pos."""
    for suffix, order in candidates:
        if suffix and text.startswith(suffix, pos):
            return suffix, order
    return None


def to_fidel(text: str) -> str:
    """Convert Latin-transliterated Amharic text to Ethiopic (Fidel) text."""
    out: list[str] = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if not _is_word_char(ch):
            out.append(ch)
            i += 1
            continue

        consonant = _match_consonant(text, i)
        if consonant is not None:
            chars = REGULAR_FAMILIES[consonant]
            after = i + len(consonant)
            match = _match_suffix(text, after, _ORDER_SUFFIXES_BY_LENGTH)
            if match is not None:
                suffix, order = match
                out.append(chars[order - 1])
                i = after + len(suffix)
            else:
                # No vowel suffix follows -> 6th (bare) order.
                out.append(chars[5])
                i = after
            continue

        # No consonant matched: try the glottal (bare-vowel) family.
        match = _match_suffix(text, i, _GLOTTAL_SUFFIXES_BY_LENGTH)
        if match is not None:
            suffix, order = match
            out.append(GLOTTAL_FAMILY[order - 1])
            i += len(suffix)
            continue

        # Unrecognized Latin letter: pass through unchanged.
        out.append(ch)
        i += 1

    return "".join(out)


def to_latin(text: str) -> str:
    """Convert Ethiopic (Fidel) text to the project's Latin transliteration."""
    out: list[str] = []
    for ch in text:
        out.append(REVERSE_MAP.get(ch, ch))
    return "".join(out)
