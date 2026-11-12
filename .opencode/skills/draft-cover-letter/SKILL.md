---
name: draft-cover-letter
description: Use when drafting the first-pass cover letter for an application slug; produces applications/<slug>/cover-letter.md.
---

# Draft a cover letter

Write a one-page first draft for the application, grounded in the atoms the
spec selects.

## Input

- The job posting (`jd.md`).
- `spec.yaml`: `company`, `role`, the selected atom ids, and `data_dir`. Read
  the full text of the selected atoms from the store named by `data_dir`.

## Output

`applications/<slug>/cover-letter.md`:

```markdown
---
date: 2026-10-14
recipient: Hiring Team
---

Dear Hiring Team,

<opening paragraph>

<body paragraph>

Sincerely,
<name>
```

- Frontmatter is optional. `date` defaults to today; omit `recipient` if there
  is no addressee.
- The body is the whole letter. Separate paragraphs with a blank line.
- Write plain prose. Blank lines separate paragraphs — that is the only
  Markdown the renderer interprets. Do not add emphasis or link syntax, and do
  not escape LaTeX special characters; the renderer escapes them for you.

## Rules

- Ground every claim in the selected atoms. Never assert a skill, tool, or
  experience the atoms do not contain. Mirror the posting's vocabulary where
  the atoms support it.
- Address the posting's top one or two requirements. Do not restate the whole
  resume.
- 250–400 words, one page.
- No placeholders. Take company, role, and recipient from `spec.yaml` and
  `jd.md`; if a name is unknown, address "Hiring Team". Never leave
  `[Company]`-style tokens — the build rejects them.

## Review before you finish

- Company and role match `spec.yaml`.
- Every claim traces to a selected atom; list any you could not ground.
- No unresolved placeholders.

## References

- Build: `scripts/build.sh <slug> letter` — warns when the letter exceeds one
  page.
