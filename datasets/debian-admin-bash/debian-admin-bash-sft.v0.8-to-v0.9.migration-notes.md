# Migration notes: debian-admin-bash-sft v0.8 to v0.9

Generated: 2026-05-13

## Scope

This migration expands the active Debian/Ubuntu Bash administration SFT dataset for a narrow 3B target model by strengthening two underrepresented operator surfaces: access/identity/permissions and backup/restore. The goal is better local-admin judgment, not broader DevOps coverage.

## Input

- Input dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.8.jsonl`
- Input records: 2360
- Input status: governed draft dataset

## Output

- Output dataset: `datasets/debian-admin-bash/debian-admin-bash-sft.v0.9.jsonl`
- Output records: 2460
- Added records: 100
- SHA-256: `35b4da0891eb4461a9927e00c7c42e0a17fb3a8452bf6ea63a3dd349d1db8a06`
- Governed record-shape schema: `schemas/debian-admin-bash.v0.2.schema.json`
- Validation report: `validation/debian-admin-bash-sft.v0.9.validation-report.md`

## Added surfaces

| Surface | Added records | Purpose |
|---|---:|---|
| Access, identity, and permissions | 51 | Inspect users/groups, sudoers, SSH authorized keys, service users, ACLs, PAM, AppArmor, key modes, and permission-denied incidents before making guarded changes. |
| Backup and restore | 49 | Preview rsync/tar backups, validate backup mounts/capacity/checksums, perform staging restores, handle SQLite backups safely, preserve metadata, and refuse destructive restore/delete shortcuts. |

## Scope control

The supplement intentionally avoids broad enterprise IAM, cloud IAM, directory services, Kubernetes secrets, backup products, or distributed storage. It remains local Debian/Ubuntu host administration with Bash-first commands and concise explanations.

The intended pattern is:

```text
inspect identity/backup state -> diagnose output -> guarded minimal change or staged restore -> verify
```

## Non-claims

This migration does not claim production readiness, semantic review completion, safety review completion, or execution validation. All added records remain `review.status=draft` pending manual review.
