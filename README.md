# job-resumes

Generate tailored resume and cover-letter PDFs from tagged content atoms.

Files of interest:

- data submodule
- `data-examples/`
- `.opencode/skills/` (select-atoms, tailor-summary, draft-cover-letter)
- `.opencode/commands/resume.md` — `/resume <slug>` tailors and builds a resume
- `.opencode/commands/cover-letter.md` — `/cover-letter <slug>` drafts and builds
  a cover letter; it will not overwrite an existing manuscript
- `applications/<slug>/spec.yaml`, which atoms — and which of their bullets or
  courses — to include for one application.
- `applications/<slug>/cover-letter.md`, the hand-editable letter manuscript
  (the source of truth; build artifacts never overwrite it)
- `templates/resume.cls`, `templates/coverletter.cls`
- `scripts/assemble.py`, `scripts/assemble-letter.py`
- `scripts/build.sh <slug> [resume|letter|both]`
- `scripts/new-application.sh <slug>` scaffolds `applications/<slug>/jd.md`

## Build

```sh
scripts/build.sh example            # resume.pdf
scripts/build.sh example letter     # cover-letter.pdf
scripts/build.sh example both       # both
```

Requires `uv` and TinyTeX (XeLaTeX). `build.sh` puts TinyTeX's bin on `PATH`.
