from amharic_translit.engine import to_fidel
from amharic_translit.normalizer import explain, normalize


def test_double_a_collapses_to_order4_vowel():
    assert normalize("taa") == "ta"


def test_ee_and_ie_both_collapse_to_capital_e():
    assert normalize("tee") == "tE"
    assert normalize("tie") == "tE"


def test_doubled_consonant_collapses():
    assert normalize("sellam") == "selam"


def test_apostrophes_are_dropped():
    assert normalize("k'ebele") == "kebele"


def test_whitespace_is_collapsed():
    assert normalize("selam   dehna") == "selam dehna"


def test_normalize_then_to_fidel_matches_direct_canonical_spelling():
    assert to_fidel(normalize("sellaam")) == to_fidel("selam")


def test_normalize_is_idempotent():
    once = normalize("sellaam neH")
    twice = normalize(once)
    assert once == twice


def test_explain_returns_empty_for_already_canonical_text():
    assert explain("selam") == []


def test_explain_reports_each_firing_rule_in_order():
    steps = explain("sellaam")
    descriptions = [d for d, _ in steps]
    assert any("order-4" in d for d in descriptions)
    assert any("doubled consonant" in d for d in descriptions)
    # final result of the last step matches normalize()'s output
    assert steps[-1][1] == normalize("sellaam")
