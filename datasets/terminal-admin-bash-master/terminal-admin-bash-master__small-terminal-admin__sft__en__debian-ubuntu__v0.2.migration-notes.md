# Migration notes: small-terminal-admin v0.3 cleaned source to governed v0.2 records

Generated: 2026-05-10T21:55:05.896946+00:00

## Source

- Source file: `terminal-admin-bash-master__small-terminal-admin__sft__en__linux-debian-ubuntu__v0.3.cleaned-bash-heavy.jsonl`
- Source records parsed: 866
- Source status: cleaned Bash-heavy dataset supplied for migration

## Output

- Output file: `datasets/terminal-admin-bash-master/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.jsonl`
- Output records: 908
- SHA-256: `b482349a828aca5309ce55a0026b18598702ffb9c8a520b4657063b3f872bcc2`
- Governed schema: `schemas/terminal-admin-bash-master.v0.2.schema.json`
- Validation report: `validation/terminal-admin-bash-master__small-terminal-admin__sft__en__debian-ubuntu__v0.2.validation-report.md`

## Conversion decisions

- Multi-turn records were split into single-pair SFT records to match the current governance linter expectation: exactly one user message and one assistant message per record.
- Exact duplicate user/assistant pairs were removed before the final output.
- `meta.dataset_version` is `0.2` because the records use the existing governed v0.2 source-record shape.
- The original cleaned dataset lineage is preserved under `meta.source`.
- Records are marked `review.status=draft`; this migration does not claim manual semantic review, safety review, or execution validation.
- 21 records were reclassified away from `refusal_with_safe_alternative` because their assistant answers did not contain refusal/safe-alternative language.

## Record-count summary

| Step | Records |
|---|---:|
| Parsed input records | 866 |
| After multi-turn splitting | 912 |
| Exact duplicate pairs removed | 4 |
| Final output records | 908 |

## Non-claims

This migration does not claim that the dataset is production-grade or ready for unattended terminal-agent training. It only places the cleaned source material into the repository's governed v0.2 source-record format and validates that structure plus governance-lint compatibility.
