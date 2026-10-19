# The transliteration convention

Amharic's script (Fidel/Ge'ez) is a syllabary: each symbol is a consonant +
vowel pair, not a single letter. This project defines one precise, reversible
Latin spelling for every such symbol it supports, so `to_fidel` and
`to_latin` are exact inverses of each other.

This is **a** convention, not **the** convention — there is no single
official way to type Amharic in Latin letters. It's closest in spirit to the
"SERA"-style ASCII schemes long used in Ethiopian computing, simplified and
made fully self-consistent. `normalizer.py` exists specifically to absorb
some of the real-world variation (doubled letters, "ee" vs "ie", etc.)
before conversion.

## Vowel orders

Every consonant family has seven members ("orders"), one per vowel:

| Order | Sound (approx.) | Suffix after a consonant | Standalone (no consonant) |
|------:|------------------|:--------------------------:|:---------------------------:|
| 1 | ä  | `e`  | `a` |
| 2 | u  | `u`  | `u` |
| 3 | i  | `i`  | `i` |
| 4 | a  | `a`  | `A` |
| 5 | e  | `E`  | `E` |
| 6 | ɨ (bare) | *(nothing)* | `I` |
| 7 | o  | `o`  | `o` |

A syllable is written as `<consonant code><order suffix>`. Orders 2, 3, 5
and 7 use the same letter whether or not a consonant precedes them, which is
why `sellam`-style words read naturally; orders 1, 4 and 6 differ between
"after a consonant" and "standalone" so that, for example, a word-initial
`a` always means the vowel-only family's 1st order (አ) and never gets
confused with another family's 4th-order suffix.

## Consonant codes

| Code | Fidel family (orders 1–7) | Code | Fidel family (orders 1–7) |
|---|---|---|---|
| `h`  | ሀሁሂሃሄህሆ | `w`  | ወዉዊዋዌውዎ |
| `l`  | ለሉሊላሌልሎ | `V`  | ዐዑዒዓዔዕዖ |
| `H`  | ሐሑሒሓሔሕሖ | `z`  | ዘዙዚዛዜዝዞ |
| `m`  | መሙሚማሜምሞ | `zh` | ዠዡዢዣዤዥዦ |
| `S`  | ሠሡሢሣሤሥሦ | `y`  | የዩዪያዬይዮ |
| `r`  | ረሩሪራሬርሮ | `d`  | ደዱዲዳዴድዶ |
| `s`  | ሰሱሲሳሴስሶ | `j`  | ጀጁጂጃጄጅጆ |
| `sh` | ሸሹሺሻሼሽሾ | `g`  | ገጉጊጋጌግጎ |
| `q`  | ቀቁቂቃቄቅቆ | `T`  | ጠጡጢጣጤጥጦ |
| `b`  | በቡቢባቤብቦ | `CH` | ጨጩጪጫጬጭጮ |
| `v`  | ቨቩቪቫቬቭቮ | `P`  | ጰጱጲጳጴጵጶ |
| `t`  | ተቱቲታቴትቶ | `ts` | ጸጹጺጻጼጽጾ |
| `ch` | ቸቹቺቻቼችቾ | `TS` | ፀፁፂፃፄፅፆ |
| `x`  | ኀኁኂኃኄኅኆ | `f`  | ፈፉፊፋፌፍፎ |
| `n`  | ነኑኒናኔንኖ | `p`  | ፐፑፒፓፔፕፖ |
| `ny` | ኘኙኚኛኜኝኞ | | |
| `k`  | ከኩኪካኬክኮ | | |
| `kh` | ኸኹኺኻኼኽኾ | | |

**Mnemonic:** an uppercase consonant code is the ejective/emphatic twin of
its lowercase counterpart — `t`/`T`, `ch`/`CH`, `p`/`P`, `s`/`S`, `h`/`H`.

The vowel-only ("glottal") family — words or syllables with no leading
consonant — is written directly with the standalone suffix column above:
`a` → አ, `u` → ኡ, `i` → ኢ, `A` → ኣ, `E` → ኤ, `I` → እ, `o` → ኦ.

## Worked example

`selam` (ሰላም, "hello/peace"):

```
s + e  ->  order 1 of family 's'  ->  ሰ
l + a  ->  order 4 of family 'l'  ->  ላ
m      ->  order 6 (bare) of family 'm'  ->  ም
```

## Out of scope for v1

- Labialized consonants (qʷ, kʷ, gʷ, etc.) — not yet in `fidel_table.py`.
- A few rare/historical letters.
- Amharic-specific punctuation (።, ፣) is passed through unchanged rather
  than mapped, since it isn't ambiguous with any Latin punctuation.

Adding a family or a punctuation mapping is a one- or two-line change in
`src/amharic_translit/data/fidel_table.py` (or `engine.py` for punctuation);
run `pytest` and `python scripts/generate_js_data.py` afterward.
