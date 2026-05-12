# Migration notes: small-debian-admin cleaned source to governed v0.4 dataset

Generated: 2026-05-10T22:20:00+00:00

## Source

- Source file: `debian-admin-bash-sft.v0.3.cleaned-source.jsonl`
- Source status: cleaned Bash-heavy dataset supplied for migration
- Previous legacy full corpus: removed because it contained incorrect / faulty data and should not remain as the active training source.

## Output

- Output file: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.4.jsonl`
- Output records: 932
- SHA-256: `498c49a5d51a55316cdc1ca7be6efbf7263ac95a19de0dece05e71384dbfea55`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.4.validation-report.md`

## Versioning decision

`meta.dataset_version` is `0.4` because this version combines the cleaned v0.3 source, the governance cleanup, shorter dataset naming, and a small curated supplement.

The schema remains `schemas/debian-admin-bash.v0.2.schema.json` because the governed source-record shape did not change. Dataset content version and schema-shape version are intentionally separate.

No separate `v0.4` schema is required unless the governed record shape changes.

## Conversion decisions

- 2026-05-12 governance cleanup corrected metadata and safety/refusal wording for validator alignment without changing record count.
- 2026-05-12 v0.4 naming/supplement pass renamed the active dataset to `debian-admin-bash-sft.v0.4.jsonl` and added 24 curated records focused on Debian/Ubuntu administration gaps.
- Multi-turn source records were split into single-pair SFT records to match the current governance linter expectation: exactly one user message and one assistant message per record.
- Exact duplicate user/assistant pairs were removed before the final output.
- Source lineage is preserved under `meta.source`.
- Records are marked `review.status=draft`; this migration does not claim manual semantic review, safety review, or execution validation.

## Record-count summary

| Step | Records |
|---|---:|
| Migrated governed v0.3 records | 908 |
| Curated v0.4 supplement records | 24 |
| Final governed output records | 932 |

## Non-claims

This migration does not claim that the dataset is production-grade or ready for unattended terminal-agent training. It places the cleaned source material into the repository's governed source-record format and validates that structure plus governance-lint compatibility.
