import pytest

from amharic_translit.data.fidel_table import (
    GLOTTAL_FAMILY,
    GLOTTAL_SUFFIXES,
    ORDER_SUFFIXES,
    REGULAR_FAMILIES,
)
from amharic_translit.engine import FORWARD_MAP, REVERSE_MAP, to_fidel, to_latin

# A handful of real, short Amharic words, chosen because they transliterate
# exactly under this project's convention (see docs/MAPPING.md).
KNOWN_WORDS = [
    ("selam", "ሰላም"),      # peace / hello
    ("dehna", "ደህና"),      # fine, well
    ("wo", "ዎ"),
    ("alu", "አሉ"),         # they said
    ("konjo", "ኮንጆ"),      # beautiful/nice
]


@pytest.mark.parametrize("latin,fidel", KNOWN_WORDS)
def test_known_words_to_fidel(latin, fidel):
    assert to_fidel(latin) == fidel


@pytest.mark.parametrize("latin,fidel", KNOWN_WORDS)
def test_known_words_to_latin(latin, fidel):
    assert to_latin(fidel) == latin


@pytest.mark.parametrize("latin,_fidel", KNOWN_WORDS)
def test_round_trip_latin_to_fidel_to_latin(latin, _fidel):
    assert to_latin(to_fidel(latin)) == latin


def test_every_regular_family_every_order_round_trips():
    for code, chars in REGULAR_FAMILIES.items():
        for order, suffix in ORDER_SUFFIXES.items():
            latin = f"{code}{suffix}"
            fidel_char = chars[order - 1]
            assert to_fidel(latin) == fidel_char, f"{latin!r} -> expected {fidel_char!r}"
            assert to_latin(fidel_char) == latin, f"{fidel_char!r} -> expected {latin!r}"


def test_every_glottal_order_round_trips():
    for order, suffix in GLOTTAL_SUFFIXES.items():
        fidel_char = GLOTTAL_FAMILY[order - 1]
        assert to_fidel(suffix) == fidel_char
        assert to_latin(fidel_char) == suffix


def test_forward_and_reverse_maps_are_bijective():
    # Every Fidel character produced by the forward map must map back to
    # exactly the syllable that produced it (no collisions in REVERSE_MAP).
    assert len(FORWARD_MAP) == len(set(FORWARD_MAP.values()))
    for latin, fidel in FORWARD_MAP.items():
        assert REVERSE_MAP[fidel] == latin


def test_whitespace_and_punctuation_pass_through_unchanged():
    assert to_fidel("selam, dehna neh?") == "ሰላም, ደህና ነህ?"
    assert to_latin("ሰላም!") == "selam!"


def test_unrecognized_ascii_passes_through():
    # 'xz' etc: 'x' is a known family code on its own, but a trailing
    # unmatched letter with no valid suffix still falls back to bare order.
    assert to_fidel("123") == "123"


def test_longest_match_prefers_multi_letter_consonant_codes():
    # 'sh' must be read as one family, not 's' + 'h'.
    assert to_fidel("sha") == "ሻ"
    assert to_fidel("sha") != to_fidel("sa") + to_fidel("ha")


def test_bare_consonant_defaults_to_sixth_order():
    # 'l' with nothing after it is the 6th (bare) order: ል
    assert to_fidel("l") == "ል"


def test_mixed_latin_and_ethiopic_input_is_harmless():
    assert to_fidel("hello world") != ""  # should not raise
    assert to_latin("hello ሰላም") == "hello selam"


def test_empty_string():
    assert to_fidel("") == ""
    assert to_latin("") == ""
