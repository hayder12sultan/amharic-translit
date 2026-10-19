"""
Command-line interface.

    amharic-translit to-fidel "selam dehna neh"
    amharic-translit to-latin "ሰላም ደህና ነህ"
    amharic-translit normalize "sellaam" --explain
    echo "selam" | amharic-translit to-fidel

Also runnable without installation:
    python -m amharic_translit.cli to-fidel "selam"
"""

from __future__ import annotations

import argparse
import sys

from .engine import to_fidel, to_latin
from .normalizer import explain, normalize


def _read_input(text: str | None) -> str:
    """Use the given text, or read stdin if none was given on the command line."""
    if text is not None:
        return text
    if sys.stdin.isatty():
        raise SystemExit("error: no TEXT given and no input piped on stdin")
    return sys.stdin.read().rstrip("\n")


def _cmd_to_fidel(args: argparse.Namespace) -> None:
    text = _read_input(args.text)
    if args.normalize:
        text = normalize(text)
    print(to_fidel(text))


def _cmd_to_latin(args: argparse.Namespace) -> None:
    text = _read_input(args.text)
    print(to_latin(text))


def _cmd_normalize(args: argparse.Namespace) -> None:
    text = _read_input(args.text)
    if args.explain:
        steps = explain(text)
        if not steps:
            print("(no changes)")
        for description, result in steps:
            print(f"- {description}")
            print(f"  -> {result}")
    else:
        print(normalize(text))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="amharic-translit",
        description="Convert between Fidel (Ethiopic) and Latin-transliterated Amharic.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_fidel = sub.add_parser("to-fidel", help="Latin -> Ethiopic")
    p_fidel.add_argument("text", nargs="?", help="Latin text (or pipe via stdin)")
    p_fidel.add_argument(
        "-n", "--normalize", action="store_true",
        help="normalize spelling variants before converting",
    )
    p_fidel.set_defaults(func=_cmd_to_fidel)

    p_latin = sub.add_parser("to-latin", help="Ethiopic -> Latin")
    p_latin.add_argument("text", nargs="?", help="Ethiopic text (or pipe via stdin)")
    p_latin.set_defaults(func=_cmd_to_latin)

    p_norm = sub.add_parser("normalize", help="clean up informal Latin spelling variants")
    p_norm.add_argument("text", nargs="?", help="Latin text (or pipe via stdin)")
    p_norm.add_argument(
        "-e", "--explain", action="store_true",
        help="show which rules fired, step by step",
    )
    p_norm.set_defaults(func=_cmd_normalize)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
