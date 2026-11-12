"""Shared helpers for reading the atom store and emitting LaTeX text."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# LaTeX special characters. str.translate makes a single pass, so the braces in
# the replacement strings are not re-escaped (a sequential .replace would).
_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
_ESCAPE_TABLE = str.maketrans(_ESCAPES)


def esc(value) -> str:
    """Escape a value for LaTeX text mode."""
    return ("" if value is None else str(value)).translate(_ESCAPE_TABLE)


def load(path: Path):
    """Read a YAML file."""
    with path.open() as fh:
        return yaml.safe_load(fh)


def call(name: str, *args: str) -> str:
    """Emit a macro call with braced arguments: \\name{arg}{arg}."""
    return name + "".join("{" + arg + "}" for arg in args)
