# Migration notes: small-terminal-admin cleaned source to governed v0.3 dataset

Generated: 2026-05-10T22:20:00+00:00

## Source

- Source file: `terminal-admin-bash-master__small-terminal-admin__sft__en__linux-debian-ubuntu__v0.3.cleaned-bash-heavy.jsonl`
- Source status: cleaned Bash-heavy dataset supplied for migration
- Previous legacy full corpus: removed because it contained incorrect / faulty data and should not remain as the active training source.

## Output

- Output file: `datasets/terminal-admin-bash-master/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.jsonl`
- Output records: 908
- SHA-256: `61d9dc129b965eacb24015dabc9e1598a302f25abae652b4c453ecb0c062e016`
- Governed record-shape schema: `schemas/terminal-admin-bash-master.v0.2.schema.json`
- Validation report: `validation/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.3.governed-bash-heavy.validation-report.md`

## Versioning decision

`meta.dataset_version` is `0.3` because this is the cleaned Bash-heavy dataset content version.

The schema remains `schemas/terminal-admin-bash-master.v0.2.schema.json` because the governed source-record shape did not change. Dataset content version and schema-shape version are intentionally separate.

No separate `v0.3` schema is required unless the governed record shape changes.

## Conversion decisions

- 2026-05-12 governance cleanup corrected metadata and safety/refusal wording for validator alignment without changing record count.
- Multi-turn source records were split into single-pair SFT records to match the current governance linter expectation: exactly one user message and one assistant message per record.
- Exact duplicate user/assistant pairs were removed before the final output.
- Source lineage is preserved under `meta.source`.
- Records are marked `review.status=draft`; this migration does not claim manual semantic review, safety review, or execution validation.

## Record-count summary

| Step | Records |
|---|---:|
| Final governed output records | 908 |

## Non-claims

This migration does not claim that the dataset is production-grade or ready for unattended terminal-agent training. It places the cleaned source material into the repository's governed source-record format and validates that structure plus governance-lint compatibility.
