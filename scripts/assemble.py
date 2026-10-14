#!/usr/bin/env python3
"""Assemble a tailored resume.tex from a spec and the tagged atom store."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

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
    with path.open() as fh:
        return yaml.safe_load(fh)


def index_by_id(records):
    return {rec["id"]: rec for rec in records}


def entry_id(entry) -> str:
    """A spec entry is a bare id, or a mapping carrying an `id`."""
    return entry if isinstance(entry, str) else entry["id"]


def pick_children(entry, records, key):
    """Select the child records to render for one spec entry.

    A bare id selects every child. A mapping may set `key` to a list of child
    ids; those render in the listed order. A missing or null list selects every
    child, while an empty list selects none (the entry header renders alone).
    """
    if isinstance(entry, str) or entry.get(key) is None:
        return records
    by_id = index_by_id(records or [])
    missing = [cid for cid in entry[key] if cid not in by_id]
    if missing:
        raise SystemExit(f"{entry_id(entry)}: no {key}: {', '.join(missing)}")
    return [by_id[cid] for cid in entry[key]]


def fmt_month(value: str) -> str:
    if value.strip().lower() == "present":
        return "Present"
    year, month = value.split("-")
    return f"{MONTHS[int(month) - 1]} {year}"


def fmt_dates(record) -> str:
    if "dates" in record:
        start, end = record["dates"].split("..")
        return f"{fmt_month(start)} \u2013 {fmt_month(end)}"
    return f"{fmt_month(record['start'])} \u2013 {fmt_month(record['end'])}"


def call(name: str, *args: str) -> str:
    """Emit a macro call with braced arguments: \\name{arg}{arg}."""
    return name + "".join("{" + arg + "}" for arg in args)


def bullet_list(records) -> str:
    if not records:
        return ""
    lines = ["\\begin{cvbullets}"]
    lines += [call("\\cvbullet", esc(rec["text"])) for rec in records]
    lines.append("\\end{cvbullets}")
    return "\n".join(lines)


def build_body(spec, contact, exp, proj, edu, skills, summaries) -> str:
    parts = []

    bits = [contact.get("phone"), contact.get("email")]
    bits += [link["label"] for link in contact.get("links", [])]
    contact_line = " \\;|\\; ".join(esc(bit) for bit in bits if bit)
    parts.append(call("\\cvheader", esc(contact["name"]), contact_line))

    summary = summaries.get(spec.get("summary"))
    if summary:
        parts.append(call("\\cvsummary", esc(summary["text"])))

    if spec.get("experience"):
        parts.append(call("\\cvsection", "Experience"))
        for entry in spec["experience"]:
            role = exp[entry_id(entry)]
            parts.append(
                call(
                    "\\cventry",
                    esc(role["title"]),
                    esc(role["org"]),
                    fmt_dates(role),
                    esc(role.get("location", "")),
                )
            )
            parts.append(
                bullet_list(pick_children(entry, role.get("bullets"), "bullets"))
            )

    if spec.get("projects"):
        parts.append(call("\\cvsection", "Projects"))
        for entry in spec["projects"]:
            proj_rec = proj[entry_id(entry)]
            parts.append(
                call(
                    "\\cventry",
                    esc(proj_rec["name"]),
                    "",
                    fmt_dates(proj_rec),
                    "",
                )
            )
            parts.append(
                bullet_list(pick_children(entry, proj_rec.get("bullets"), "bullets"))
            )

    if spec.get("skills"):
        parts.append(call("\\cvsection", "Skills"))
        parts.append("\\begin{cvbullets}")
        for sid in spec["skills"]:
            group = skills[sid]
            items = ", ".join(esc(item) for item in group["items"])
            parts.append(call("\\cvskill", esc(group["label"]), items))
        parts.append("\\end{cvbullets}")

    if spec.get("education"):
        parts.append(call("\\cvsection", "Education"))
        for entry in spec["education"]:
            school = edu[entry_id(entry)]
            parts.append(
                call(
                    "\\cventry",
                    esc(school["school"]),
                    esc(school["credential"]),
                    esc(f"{school['start']} \u2013 {school['end']}"),
                    esc(school.get("location", "")),
                )
            )
            parts.append(
                bullet_list(pick_children(entry, school.get("courses"), "courses"))
            )

    return "\n".join(parts) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: assemble.py <slug>", file=sys.stderr)
        return 2
    slug = sys.argv[1]
    app = ROOT / "applications" / slug

    spec = load(app / "spec.yaml")
    data_dir = ROOT / spec.get("data_dir", "data")
    contact = load(data_dir / "contact.yaml")
    exp = index_by_id(load(data_dir / "experience.yaml"))
    proj = index_by_id(load(data_dir / "projects.yaml"))
    edu = index_by_id(load(data_dir / "education.yaml"))
    skills = index_by_id(load(data_dir / "skills.yaml"))
    summaries = index_by_id(load(data_dir / "summary-variants.yaml"))

    body = build_body(spec, contact, exp, proj, edu, skills, summaries)
    document = (
        "\\documentclass{resume}\n\\begin{document}\n" + body + "\\end{document}\n"
    )

    out = app / "resume.tex"
    out.write_text(document)
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
