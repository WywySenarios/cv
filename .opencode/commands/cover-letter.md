---
description: Draft and build a first-pass cover letter for an application slug (e.g. /cover-letter acme).
---

Draft a cover letter for the application in `applications/$1/`.

1. Confirm `applications/$1/jd.md` and `applications/$1/spec.yaml` exist. If
   either is missing, stop and say which.
2. If `applications/$1/cover-letter.md` already exists, report that it exists
   and stop. Never overwrite an existing manuscript.
3. Read the job posting and `spec.yaml`.
4. Load the `draft-cover-letter` skill and write
   `applications/$1/cover-letter.md`.
5. Run `scripts/build.sh $1 letter` and report
   `applications/$1/cover-letter.pdf`, or the failure. Tell the user the
   manuscript is `applications/$1/cover-letter.md`, and that editing it and
   re-running `scripts/build.sh $1 letter` rebuilds the PDF.

Never invent atom ids or content. Ground every claim in the selected atoms.
