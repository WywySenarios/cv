#!/usr/bin/env python3
"""Assemble a first-draft cover-letter.tex from the manuscript and metadata.

The manuscript (cover-letter.md) is the source of truth and is never rewritten
here; this only renders it. Metadata (company, role) comes from spec.yaml.
"""

from __future__ import annotations

import datetime
import re
import sys

import yaml

from _common import ROOT, call, esc, load

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Leading YAML frontmatter block delimited by --- lines.
_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---[ \t]*\n?(.*)\Z", re.DOTALL)

# A bracketed token that is not a Markdown link: matches [Company] but not
# [text](url). Leftover tokens of this shape are drafting placeholders.
_PLACEHOLDER = re.compile(r"\[[^\]\n]+\](?!\()")

# Sign-off words that open a closing block.
_SIGNOFF = re.compile(
    r"^(sincerely|regards|best regards|best|yours truly|yours|cheers|thank you)[,]?$",
    re.IGNORECASE,
)
_SIGNOFF_INLINE = re.compile(
    r"^(sincerely|regards|best regards|best|yours truly|yours|cheers|thank you)[,]?\s+(.+)$",
    re.IGNORECASE,
)


def split_manuscript(text: str):
    """Split a manuscript into (frontmatter dict, body text)."""
    match = _FRONTMATTER.match(text)
    if not match:
        return {}, text
    return (yaml.safe_load(match.group(1)) or {}), match.group(2)


def paragraphs(body: str):
    """Split body text on blank lines; collapse inner newlines to spaces."""
    blocks = re.split(r"\n[ \t]*\n", body.strip())
    return [" ".join(block.split()) for block in blocks if block.strip()]


def normalize_signoff(value: str) -> str:
    """Render a sign-off with one trailing comma regardless of source punctuation."""
    return value.strip().rstrip(", ") + ","


def split_closing(paras, name):
    """Peel a trailing sign-off block off the body paragraphs.

    Accepts either "Sincerely, Name" in one block or "Sincerely," followed by a
    block holding the name. Returns (body, sign-off, name); when no closing is
    recognised the body is returned untouched with both extras None.
    """
    target = " ".join((name or "").split())
    if not paras or not target:
        return paras, None, None

    last = " ".join(paras[-1].split())
    if last == target and len(paras) >= 2 and _SIGNOFF.match(paras[-2].strip()):
        return paras[:-2], normalize_signoff(paras[-2]), last

    inline = _SIGNOFF_INLINE.match(last)
    if inline and " ".join(inline.group(2).split()) == target:
        return paras[:-1], normalize_signoff(inline.group(1)), target
    return paras, None, None


def fmt_date(value) -> str:
    """Render a frontmatter date, defaulting to today."""
    if value is None or value == "":
        value = datetime.date.today()
    if isinstance(value, datetime.datetime):
        value = value.date()
    if isinstance(value, datetime.date):
        return f"{MONTHS[value.month - 1]} {value.day}, {value.year}"
    return str(value)


def check(body: str, company: str) -> None:
    """Fail on drafting placeholders; warn on a body that never names the company."""
    found = sorted(set(_PLACEHOLDER.findall(body)))
    if found:
        raise SystemExit(
            "cover-letter.md has unresolved placeholders: " + ", ".join(found)
        )
    if company and company.lower() not in body.lower():
        print(
            f"warning: the body never mentions company {company!r}",
            file=sys.stderr,
        )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: assemble-letter.py <slug>", file=sys.stderr)
        return 2
    slug = sys.argv[1]
    app = ROOT / "applications" / slug

    manuscript_path = app / "cover-letter.md"
    if not manuscript_path.exists():
        print(
            f"{manuscript_path.relative_to(ROOT)} not found; draft it first",
            file=sys.stderr,
        )
        return 1

    spec = load(app / "spec.yaml")
    data_dir = ROOT / spec.get("data_dir", "data")
    contact = load(data_dir / "contact.yaml")

    meta, body = split_manuscript(manuscript_path.read_text())
    company = spec.get("company", "")

    check(body, company)

    paras = paragraphs(body)
    if not paras:
        print(f"{manuscript_path.relative_to(ROOT)} has an empty body", file=sys.stderr)
        return 1
    paras, signoff, signer = split_closing(paras, contact.get("name"))

    bits = [contact.get("phone"), contact.get("email")]
    bits += [link["label"] for link in contact.get("links", [])]
    contact_line = " \\;|\\; ".join(esc(bit) for bit in bits if bit)

    parts = [
        call("\\letterheader", esc(contact["name"]), contact_line),
        call("\\letterdate", esc(fmt_date(meta.get("date")))),
        call(
            "\\letterrecipient",
            esc(meta.get("recipient", "")),
            esc(company),
            esc(spec.get("role", "")),
        ),
    ]
    parts += [call("\\letterpara", esc(p)) for p in paras]
    if signoff:
        parts.append(call("\\letterclosing", esc(signoff), esc(signer)))

    document = (
        "\\documentclass{coverletter}\n\\begin{document}\n"
        + "\n".join(parts)
        + "\n\\end{document}\n"
    )

    out = app / "cover-letter.tex"
    out.write_text(document)
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
