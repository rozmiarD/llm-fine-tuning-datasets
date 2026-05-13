# Documentation map

This directory contains reusable documentation for dataset shape, governance, quality, naming, and accessibility.

## Canonical sources

| Topic | Canonical file | Use for |
|---|---|---|
| Source record shape and message format | [Dataset format](dataset-format.md) | JSONL structure, `messages`, metadata fields, and export expectations |
| Governance and validation model | [Dataset governance](dataset-governance.md) | validation layers, risk levels, answer styles, non-claims, and review rules |
| Record quality bar | [Quality guidelines](quality-guidelines.md) | examples, Debian/Ubuntu consistency, scripting habits, and expansion policy |
| File naming | [Naming convention](naming-convention.md) | dataset file names, field meanings, and versioning |
| Repository-specific workflow | [Repository playbook](repository-playbook.md) | official checkpoint publishing, draft handling, changelog/migration-note policy, and push discipline for this repo only |
| Accessible documentation | [Accessibility guidelines](accessibility-guidelines.md) | readable docs, tables, badges, examples, and visual alternatives |

## Documentation rule

Keep long-form rules in one canonical place and link to them from README files, dataset cards, and validation notes. If a rule changes, update the canonical page first, then update short summaries and generated reports only where needed.
