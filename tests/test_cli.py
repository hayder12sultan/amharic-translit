import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"


def run_cli(args, input_text=None):
    return subprocess.run(
        [sys.executable, "-m", "amharic_translit.cli", *args],
        input=input_text,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(SRC), "PATH": "/usr/bin:/bin"},
    )


def test_to_fidel_argument():
    result = run_cli(["to-fidel", "selam"])
    assert result.returncode == 0
    assert result.stdout.strip() == "ሰላም"


def test_to_latin_argument():
    result = run_cli(["to-latin", "ሰላም"])
    assert result.returncode == 0
    assert result.stdout.strip() == "selam"


def test_to_fidel_reads_stdin_when_no_argument_given():
    result = run_cli(["to-fidel"], input_text="selam\n")
    assert result.returncode == 0
    assert result.stdout.strip() == "ሰላም"


def test_to_fidel_with_normalize_flag():
    result = run_cli(["to-fidel", "--normalize", "sellaam"])
    assert result.returncode == 0
    assert result.stdout.strip() == "ሰላም"


def test_normalize_explain_flag_shows_steps():
    result = run_cli(["normalize", "sellaam", "--explain"])
    assert result.returncode == 0
    assert "->" in result.stdout


def test_no_text_and_no_stdin_is_an_error():
    # No piped input and no argument: should fail cleanly, not hang.
    result = subprocess.run(
        [sys.executable, "-c", (
            "import sys; sys.path.insert(0, %r); "
            "from amharic_translit.cli import main; "
            "sys.stdin.isatty = lambda: True; "
            "main(['to-fidel'])"
        ) % str(SRC)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_unknown_command_exits_nonzero():
    result = run_cli(["not-a-real-command"])
    assert result.returncode != 0
