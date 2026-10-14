# job-resumes

Generate tailored resume PDFs from tagged content atoms.

Files of interest:

- data submodule
- `data-examples/`
- `.opencode/skills/` (select-atoms, tailor-summary)
- `.opencode/commands/resume.md` — `/resume <slug>` tailors and builds a resume
- `applications/<slug>/spec.yaml`, which atoms — and which of their bullets or
  courses — to include for one application.
- `templates/resume.cls`
- `scripts/assemble.py`
- `scripts/build.sh <slug>` outputs to `applications/<slug>/resume.pdf`
- `scripts/new-application.sh <slug>` scaffolds `applications/<slug>/jd.md`

## Build

```sh
scripts/build.sh example
```

Requires `uv` and TinyTeX (XeLaTeX). `build.sh` puts TinyTeX's bin on `PATH`.
