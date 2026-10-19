# amharic-translit

A small, dependency-free engine (+ CLI, + static web demo) for converting
between the Ethiopic (Fidel) script used for Amharic and a Latin
transliteration scheme close to how people type Amharic on phones and
keyboards that don't have Ethiopic input — plus a light normalizer for
common spelling variants.

## Why

Amharic speakers routinely write Amharic using Latin letters (SMS, social
media, chat). That Latin text is inconsistent — the same word gets spelled
several different ways — which makes it hard to search, index, or feed into
other tools. This project gives that informal Latin convention a precise,
documented, *reversible* definition, and a small engine to convert in both
directions.

## Status

Core (33 consonant families × 7 vowel orders + the vowel-only "glottal"
family) is implemented and round-trip tested. Labialized consonants
(qʷ, kʷ, gʷ, …) and a few rare/obsolete letters are out of scope for v1 —
see `docs/MAPPING.md` for exactly what's covered and how to extend it.

## Project layout

```
amharic-translit/
├── src/amharic_translit/
│   ├── data/fidel_table.py   # the mapping data (source of truth)
│   ├── engine.py             # to_fidel() / to_latin() + tokenizer
│   ├── normalizer.py         # common spelling-variant cleanup
│   └── cli.py                # `amharic-translit` command line tool
├── web/                      # static, dependency-free browser demo
│   ├── index.html
│   ├── app.js
│   └── data.js               # generated from fidel_table.py, do not hand-edit
├── scripts/
│   └── generate_js_data.py   # regenerates web/data.js from the Python table
├── tests/                    # pytest suite
└── docs/
    └── MAPPING.md            # the transliteration convention, documented
```

## Quick start

```bash
pip install -e .
amharic-translit to-fidel "selam dehna neh"
amharic-translit to-latin "ሰላም ደህና ነህ"
amharic-translit normalize "sellaam"
```

## Development

```bash
pip install -e ".[dev]"
pytest
python scripts/generate_js_data.py   # keep web/data.js in sync after editing the table
```
