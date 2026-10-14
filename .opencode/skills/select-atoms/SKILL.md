---
name: select-atoms
description: Use when tailoring a resume to a job posting and selecting which content atoms (experience, projects, skills, education, summary) to include; produces applications/<slug>/spec.yaml.
---

# Select atoms for a posting

Given a job description and the atom index, return the entries to include.

## Input

- The job description.
- The atom index: for each section (`experience`, `projects`, `skills`,
  `education`, `summary-variants`), the entries' `id` and `tags`, plus the
  child ids and tags under each entry (bullets for experience/projects,
  courses for education). Ids and tags only; full text is not needed to
  choose.

## Output

A `spec.yaml` selecting:

- `summary`: one summary-variant id.
- `experience`: role entries, in relevance order.
- `projects`: project entries, in relevance order.
- `education`: institution entries.
- `skills`: skill-group ids.

An entry is a bare id to take the whole atom, or a mapping to take part of
one:

```yaml
experience:
  - huawei-2026 # whole atom
  - id: scout-captain-2023
    bullets: [scout-sheet] # subset, in this order
projects:
  - id: proj-control
    bullets: [ctl-k8s, ctl-obs]
education:
  - id: mcgill
    courses: [mcgill-systems]
```

Listed child ids render in the order you write them. Omit the list to take
every child; use `[]` for none. `bullets` names experience/project bullets;
`courses` names education courses. Skills items have no ids, so a skill group
is all-or-nothing.

The spec also carries `slug`, `company`, `role`, `job_description`, and
`data_dir`.

## Rules

- Prefer atoms whose tags overlap the posting's requirements and nice-to-haves.
- Order by relevance to the posting, strongest first.
- Omit atoms with no overlap. Fewer, sharper entries beat a full dump.
- Only use ids that exist in the index, and only child ids that exist under
  their atom. Never invent ids or content.

## Budget

Target one page. These caps are per entry; enforce them by choosing child ids:

| Section    | Cap                                                          |
| ---------- | ------------------------------------------------------------ |
| summary    | 1 line                                                       |
| experience | up to 3 roles; ≤3 bullets for the most recent, ≤2 for others |
| projects   | up to 3 projects; ≤2 bullets each                            |
| skills     | up to 5 groups                                               |
| education  | 1–2 entries; ≤2 course lines each                            |

When over budget, drop the lowest-relevance atoms or bullets first (least tag
overlap) — never drop a whole section the posting clearly needs.

## References

- Atom schema: the store named by `data_dir` (`data/` private, `data-examples/`
  abstract).
- Build the result: `scripts/build.sh <slug>` — it prints the page count and
  warns when the resume exceeds one page.
