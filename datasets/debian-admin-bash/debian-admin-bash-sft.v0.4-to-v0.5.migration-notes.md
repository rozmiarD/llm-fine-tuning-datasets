# Migration notes: debian-admin-bash-sft v0.4 to v0.5

Generated: 2026-05-12

## Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset without adding PostgreSQL or broad database-administration scope.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.4.jsonl`
- Input records: 932
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.5.jsonl`
- Output records: 1000
- SHA-256: `90526e75efae73e90a33c4d736dd87eac0e6b32e4fabed506a344374f7036c95`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.5.validation-report.md`

## Added surfaces

The v0.5 supplement adds 68 curated records:

| Surface | Added records | Purpose |
|---|---:|---|
| SQLite operations | 23 | Local file-database inspection, backup, integrity checks, WAL/locking, safe restore, and SQLite CLI availability. |
| Backup and restore | 22 | rsync/tar/checksum/staging restore/metadata backup workflows with dry-run and guarded restore habits. |
| SSH and authentication | 23 | sshd validation, effective config inspection, authorized_keys permissions, sudoers/user access, key handling, and safe reload/refusal patterns. |

## Scope control

PostgreSQL is intentionally excluded from v0.5. Database coverage is limited to SQLite as a local file-backed operational surface that fits Debian/Ubuntu Bash administration.

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.
