"""
The Fidel <-> Latin mapping table. This is the single source of truth for
the whole project: engine.py builds its lookup dictionaries from this data,
and scripts/generate_js_data.py regenerates the web demo's data.js from it.

Amharic's Ge'ez-derived script ("Fidel") is organized into consonant
*families*. Each family has seven members ("orders"), one per vowel sound.
Rather than hand-listing all ~230 individual syllables as isolated
Latin -> Fidel pairs, we store each family as one short string of its
7 characters (in order), plus a short Latin *consonant code* for that
family. The engine then combines a consonant code with an *order suffix*
(see ORDER_SUFFIXES below) to generate every syllable automatically.

This keeps the mapping easy to read, easy to audit, and easy to extend
(adding a family is one line).

Convention, in brief (full rationale in docs/MAPPING.md):
  * Each regular family is written as  <consonant code><order suffix>.
      e.g. family 's' + order-4 suffix 'a'  ->  "sa"  ->  ሳ
  * An uppercase consonant code is the "emphatic" (ejective) counterpart
    of its lowercase twin, e.g. 't' (ተ, plain t) vs 'T' (ጠ, ejective t).
  * Words/syllables that start with a bare vowel (no consonant) use the
    GLOTTAL_FAMILY table instead, keyed directly by vowel letter.
"""

from __future__ import annotations

# --- Vowel orders ---------------------------------------------------------
# Order:        1    2    3    4    5    6     7
# Sound:        ä    u    i    a    e    ɨ     o
ORDER_SUFFIXES: dict[int, str] = {
    1: "e",
    2: "u",
    3: "i",
    4: "a",
    5: "E",   # capital E, to avoid ambiguity with order-1 'e' + order-3 'i'
    6: "",    # the "bare"/6th order consonant carries no vowel letter
    7: "o",
}

# Same seven orders, but for the vowel-only "glottal" family (words/
# syllables with no leading consonant). Deliberately distinct where it
# matters (orders 1, 4, 6) so a bare "a" always means the glottal-family
# order-1 vowel, never a stray order-4 suffix with no consonant attached.
GLOTTAL_SUFFIXES: dict[int, str] = {
    1: "a",
    2: "u",
    3: "i",
    4: "A",
    5: "E",
    6: "I",
    7: "o",
}

# The glottal stop family itself: አ ኡ ኢ ኣ ኤ እ ኦ (orders 1..7)
GLOTTAL_FAMILY: str = "አኡኢኣኤእኦ"

# --- Regular consonant families -------------------------------------------
# code -> 7 Fidel characters, orders 1..7, left to right.
REGULAR_FAMILIES: dict[str, str] = {
    "h":  "ሀሁሂሃሄህሆ",   # h
    "l":  "ለሉሊላሌልሎ",   # l
    "H":  "ሐሑሒሓሔሕሖ",   # emphatic/pharyngeal h
    "m":  "መሙሚማሜምሞ",   # m
    "S":  "ሠሡሢሣሤሥሦ",   # historical śawt (same sound as s today)
    "r":  "ረሩሪራሬርሮ",   # r
    "s":  "ሰሱሲሳሴስሶ",   # s
    "sh": "ሸሹሺሻሼሽሾ",   # sh
    "q":  "ቀቁቂቃቄቅቆ",   # q (ejective k)
    "b":  "በቡቢባቤብቦ",   # b
    "v":  "ቨቩቪቫቬቭቮ",   # v (loanwords)
    "t":  "ተቱቲታቴትቶ",   # t
    "ch": "ቸቹቺቻቼችቾ",   # ch
    "x":  "ኀኁኂኃኄኅኆ",   # historical/liturgical h variant
    "n":  "ነኑኒናኔንኖ",   # n
    "ny": "ኘኙኚኛኜኝኞ",   # ny / gn
    "k":  "ከኩኪካኬክኮ",   # k
    "kh": "ኸኹኺኻኼኽኾ",   # kh (rare)
    "w":  "ወዉዊዋዌውዎ",   # w
    "V":  "ዐዑዒዓዔዕዖ",   # pharyngeal ayin (same sound as glottal family today)
    "z":  "ዘዙዚዛዜዝዞ",   # z
    "zh": "ዠዡዢዣዤዥዦ",   # zh / j (French j)
    "y":  "የዩዪያዬይዮ",   # y
    "d":  "ደዱዲዳዴድዶ",   # d
    "j":  "ጀጁጂጃጄጅጆ",   # j (English j)
    "g":  "ገጉጊጋጌግጎ",   # g
    "T":  "ጠጡጢጣጤጥጦ",   # ejective t
    "CH": "ጨጩጪጫጬጭጮ",   # ejective ch
    "P":  "ጰጱጲጳጴጵጶ",   # ejective p
    "ts": "ጸጹጺጻጼጽጾ",   # ejective ts
    "TS": "ፀፁፂፃፄፅፆ",   # historical ejective ts variant
    "f":  "ፈፉፊፋፌፍፎ",   # f
    "p":  "ፐፑፒፓፔፕፖ",   # p
}

# Consonant codes, longest first, for greedy left-to-right tokenizing.
CONSONANT_CODES_BY_LENGTH: list[str] = sorted(
    REGULAR_FAMILIES.keys(), key=len, reverse=True
)
