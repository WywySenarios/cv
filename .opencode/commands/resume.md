---
description: Tailor and build a resume for an application slug (e.g. /resume acme).
---

Tailor a resume for the application in `applications/$1/`.

1. Confirm `applications/$1/jd.md` exists. If it does not, stop and ask the user to place the job posting there.
2. Read the job posting.
3. Load the `select-atoms` skill and write `applications/$1/spec.yaml`, setting
   `data_dir` to the atom store (default `data`).
4. Load the `tailor-summary` skill to pick or draft the summary line and set
   `summary:` in the spec.
5. Run `scripts/build.sh $1` and report `applications/$1/resume.pdf`, or the
   failure.

Never invent atom ids or content. If the atom store is missing, say so instead of guessing.
